import json
from typing import List, Dict, Any, Generator
from openai import OpenAI
from backend.config import settings
from backend.models import StockResearchJob, ResearchLog
from backend.agent.skills import get_tool_schemas, search_web, browse_page

class AgentRuntime:
    """
    OpenClaw-inspired Persistent Agent Runtime engine executing an autonomous stateful ReAct stream loop.
    """
    def __init__(self, job_id: int, db_session, system_prompt: str):
        self.job_id = job_id
        self.db = db_session
        self.system_prompt = system_prompt
        self.client = OpenAI(base_url=settings.openai_base_url, api_key=settings.openai_api_key)
        
        # Load loaded model identifier from LM Studio directly if set to generic default
        self.model = settings.model_name
        if self.model == "default":
            try:
                models = self.client.models.list().data
                self.model = models[0].id if models else "gemma-2-9b-it"
            except Exception:
                self.model = "local-model"

        self.messages: List[Dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def _append_log(self, log_type: str, content: str):
        """Persist structured events directly to database transaction logs."""
        try:
            log_item = ResearchLog(job_id=self.job_id, log_type=log_type, content=content)
            self.db.add(log_item)
            self.db.commit()
        except Exception as e:
            self.db.rollback()

    def run_stream(self, prompt: str, max_iterations: int = 8) -> Generator[str, None, str]:
        """
        Execute streaming tool-augmented conversation cycle yielding JSON/SSE message events.
        Returns the final consolidated text output string.
        """
        self.messages.append({"role": "user", "content": prompt})
        self._append_log("thought", f"Initializing research step for objective: {prompt[:100]}...")
        
        iteration = 0
        final_response_content = ""

        while iteration < max_iterations:
            iteration += 1
            yield json.dumps({"type": "status", "content": f"Cycle {iteration}/{max_iterations} execution started..."})
            
            try:
                response_stream = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    tools=get_tool_schemas(),
                    stream=True
                )
            except Exception as e:
                err_msg = f"LLM Server connection exception: {str(e)}"
                self._append_log("error", err_msg)
                yield json.dumps({"type": "error", "content": err_msg})
                return final_response_content

            collected_content = ""
            tool_calls_agg: Dict[int, Dict[str, Any]] = {}

            for chunk in response_stream:
                delta = chunk.choices[0].delta if chunk.choices else None
                if not delta:
                    continue
                
                # Stream normal text tokens
                if delta.content:
                    collected_content += delta.content
                    yield json.dumps({"type": "thought", "content": delta.content})

                # Aggregate native tool calling deltas
                if delta.tool_calls:
                    for tc in delta.tool_calls:
                        idx = tc.index
                        if idx not in tool_calls_agg:
                            tool_calls_agg[idx] = {"id": tc.id, "type": "function", "function": {"name": tc.function.name or "", "arguments": ""}}
                        if tc.function and tc.function.arguments:
                            tool_calls_agg[idx]["function"]["arguments"] += tc.function.arguments

            # Check if model finished generation with standard message content
            if collected_content.strip():
                self._append_log("thought", collected_content.strip())
                final_response_content = collected_content.strip()

            # If no tools invoked, execution cycle terminates successfully
            if not tool_calls_agg:
                self.messages.append({"role": "assistant", "content": collected_content})
                break

            # Format tool call invocation block to store in history schema cleanly
            assistant_msg = {"role": "assistant", "content": collected_content or None, "tool_calls": list(tool_calls_agg.values())}
            self.messages.append(assistant_msg)

            # Invoke target skills autonomously
            for tc in tool_calls_agg.values():
                fn_name = tc["function"]["name"]
                raw_args = tc["function"]["arguments"]
                tc_id = tc["id"]
                
                yield json.dumps({"type": "tool_call", "content": f"Invoking skill '{fn_name}' with arguments: {raw_args}"})
                self._append_log("tool_call", f"Skill={fn_name} | Args={raw_args}")
                
                # Safely parse JSON arguments string
                try:
                    args_dict = json.loads(raw_args) if raw_args else {}
                except Exception:
                    args_dict = {}

                # Execute Python Skill mapped dynamically
                observation = ""
                if fn_name == "search_web":
                    query_str = args_dict.get("query", "")
                    observation = search_web(query_str)
                elif fn_name == "browse_page":
                    url_str = args_dict.get("url", "")
                    observation = browse_page(url_str)
                else:
                    observation = f"Requested tool '{fn_name}' is not recognized by the autonomous runtime engine."

                yield json.dumps({"type": "tool_result", "content": f"Skill output length: {len(observation)} chars."})
                self._append_log("tool_result", f"Skill={fn_name} | Output Snippet={observation[:400]}")
                
                # Append tool execution observation outcome back into persistent message history
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tc_id,
                    "name": fn_name,
                    "content": observation
                })

        return final_response_content

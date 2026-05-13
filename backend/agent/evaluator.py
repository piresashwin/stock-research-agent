import os
import json
from typing import Generator
from backend.models import StockResearchJob
from backend.agent.runtime import AgentRuntime

def get_checklist_content() -> str:
    """Read root stock picking checklist verification instructions markdown securely with fallback checking paths."""
    paths_to_check = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "prompts", "stock_picking_checklist.md")),
        os.path.abspath(os.path.join(os.getcwd(), "prompts", "stock_picking_checklist.md")),
        "/app/prompts/stock_picking_checklist.md"
    ]
    for p in paths_to_check:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                continue
    return "Stock-Picking Checklist: Quality-at-Value Framework triggers."

def evaluate_stock_verdict(job_id: int, symbol: str, db) -> Generator[str, None, str]:
    """
    Phase 2 Core Orchestrator: Ingests Phase 1 compiled data alongside explicit framework checklists to calculate scores.
    Yields live SSE JSON block strings and returns final structured JSON verdict block.
    """
    job = db.query(StockResearchJob).filter(StockResearchJob.id == job_id).first()
    gathered_data = job.gathered_data if job else "Fundamental data not available."

    checklist_markdown = get_checklist_content()
    
    system_instruction = f"""You are an elite, definitive Investment Verdict Evaluator Agent.
Your objective is to systematically audit the gathered fundamental data for stock symbol: {symbol} using the strict rules of the stock picking checklist.

### GATHERED PHASE 1 DATA:
{gathered_data}

### EVALUATION CHECKLIST RULES:
{checklist_markdown}

INSTRUCTIONS:
1. Systematically evaluate each Pass/Fail criteria (assigning ✓, ≈, or ✗).
2. Assess downside margin of safety and business moat categories.
3. You MUST output your final answer as a pure, valid JSON object matching exactly the following schema structure without markdown formatting or surrounding triple backticks:

{{
  "scores": {{
    "quality": "PASS or FAIL",
    "valuation": "BUY or HOLD or WAIT",
    "moat": "Weak / Moderate / Strong score",
    "management": "STRONG or GOOD or ADEQUATE or WEAK"
  }},
  "checklist_log": [
    {{"metric": "ROIC >15%", "status": "✓ or ≈ or ✗", "note": "Brief context"}},
    {{"metric": "Debt/Equity <0.5x", "status": "✓ or ≈ or ✗", "note": "Brief context"}}
  ],
  "target_entry_price": "₹[calculated discount price]",
  "verdict": "BUY or HOLD or WAIT or SKIP",
  "reasoning": "Single sentence high-level rationale justifying the final recommendation."
}}
"""

    runtime = AgentRuntime(job_id=job_id, db_session=db, system_prompt=system_instruction)
    
    prompt = f"Analyze the gathered parameters for {symbol} against the framework checklist and generate the definitive JSON structured verdict payload."
    
    final_verdict_str = ""
    for chunk in runtime.run_stream(prompt=prompt, max_iterations=2, enable_tools=False):
        yield chunk

    # Intercept final assistant reasoning message containing content strings safely
    assistant_msgs = [m for m in runtime.messages if m.get("role") == "assistant" and m.get("content")]
    raw_content = assistant_msgs[-1].get("content", "") if assistant_msgs else "{}"
    
    # Strip conversational text preambles to isolate target block securely between outer curly braces
    cleaned_json_str = raw_content.strip()
    start_idx = cleaned_json_str.find("{")
    end_idx = cleaned_json_str.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        cleaned_json_str = cleaned_json_str[start_idx:end_idx+1]

    # Validate JSON compilation string schema structure
    try:
        json.loads(cleaned_json_str)
        final_verdict_str = cleaned_json_str
    except Exception:
        # Provide clean fallback framework verdict if model JSON parsing breaks
        final_verdict_str = json.dumps({
            "scores": {"quality": "MARGINAL", "valuation": "WAIT", "moat": "Moderate", "management": "ADEQUATE"},
            "checklist_log": [{"metric": "Overall Parse Integrity", "status": "≈", "note": "Model response format validation failed."}],
            "target_entry_price": "N/A",
            "verdict": "WAIT",
            "reasoning": "Raw output string format malformed. Manual verification required."
        })

    if job:
        job.verdict_json = final_verdict_str
        job.status = "completed"
        db.commit()
        
    yield json.dumps({"type": "verdict", "content": final_verdict_str})
    return final_verdict_str

# Stock Deep Research Agent: Context & Architecture Documentation

This document serves as the **Master Agent Context** for the Stock Deep Research Agent repository. Any autonomous AI agent, developer assistant, or pair-programming LLM working on this codebase MUST read this document to understand the underlying architectural patterns, execution boundaries, and design constraints before proposing modifications.

---

## 🏛️ High-Level System Architecture

The platform operates as a decoupled, multi-phase agentic pipeline built to conduct professional fundamental analysis and stock evaluation using local LLMs served via **LM Studio** (using its standard OpenAI-compatible API protocol).

```
┌────────────────────────────────────────────────────────┐
│               Host Operating System                    │
│                                                        │
│   ┌──────────────────────┐    ┌────────────────────┐   │
│   │ LM Studio Local LLM  │    │ SQLite DB File     │   │
│   │ (Port 1234 / Open-   │    │ research_agent.db  │   │
│   │  AI API Protocol)    │    └─────────▲──────────┘   │
│   └──────────▲───────────┘              │              │
│              │                          │ Volume Mount │
│              │ HTTP Proxy               │              │
├──────────────┼──────────────────────────┼──────────────┤
│              │                          │              │
│   ┌──────────▼──────────────────────────▼──────────┐   │
│   │       FastAPI Backend Runtime Container        │   │
│   │       (mcr.microsoft.com/playwright/python)    │   │
│   │                                                │   │
│   │  ┌─────────────────┐      ┌─────────────────┐  │   │
│   │  │ Phase 1 Agent   │◄────►│ Phase 2 Agent   │  │   │
│   │  │ (The Gatherer)  │      │ (The Evaluator) │  │   │
│   │  └────────┬────────┘      └────────┬────────┘  │   │
│   └───────────┼────────────────────────┼───────────┘   │
│               │ SSE Log Stream         │ JSON Verdict  │
│               ▼                        ▼               │
│   ┌────────────────────────────────────────────────┐   │
│   │        React / Vite Testing Dashboard          │   │
│   │        (Port 3000 Container Proxy)             │   │
│   └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 Execution Environment & Container Strategy

### 1. Zero-Build Layer Injection
To eliminate custom Docker layer compilation times, the project avoids custom static `build:` Dockerfiles. Instead, `docker-compose.yml` mounts source code directly into pre-built production base images at runtime:
- **Backend Service**: Directly uses `mcr.microsoft.com/playwright/python:v1.42.0-jammy`. On boot, it dynamically runs `pip install -r backend/requirements.txt` and launches the live-reloading `uvicorn` instance.
- **Frontend Service**: Uses standard lightweight `node:20-alpine`, mapping `./frontend` source code directly into `/app` and executing `npm install && npm run dev`.

### 2. Networking Traps & Interlocks
- **LM Studio Routing**: Because LM Studio binds to the host operating system interface on port `1234`, containerized backend services accessing it MUST use the `http://host.docker.internal:1234/v1` address rather than `localhost` or `127.0.0.1`.
- **Database Mounting**: The SQLite file (`research_agent.db`) is mounted natively as a host file volume to guarantee that state logs persist permanently even if containers are destroyed or restarted.

---

## 📦 Core Directory & Module Layout

```text
stock-research-agent/
├── agent_context.md                  # This file (Master context documentation)
├── docker-compose.yml                # Declarative zero-build volume container composition
├── research_agent.db                 # Persistent local SQLite ledger file
├── prompts/                          # Underlying prompt system constraints
│   ├── stock_picking_checklist.md    # Scoring logic triggers & margin of safety formulas
│   └── stock_research_template.md    # 7-section structured output target schema
├── backend/                          # Python FastAPI service & agent loop core
│   ├── __init__.py
│   ├── config.py                     # Centralized Pydantic configuration loader
│   ├── models.py                     # SQLAlchemy ORM definitions (StockResearchJob, ResearchLog)
│   ├── database.py                   # Thread-safe SQLite engine pooling & sessions
│   ├── main.py                       # REST API routers & Server-Sent Events generator
│   ├── agent/                        # Persistent agentic loop modules
│   │   ├── __init__.py
│   │   ├── skills.py                 # Pydantic schemas, Playwright web-scraping & DuckDuckGo APIs
│   │   ├── runtime.py                # ReAct stream interceptor & autonomous execution loop
│   │   ├── researcher.py             # Phase 1 Gatherer orchestration script
│   │   └── evaluator.py              # Phase 2 Checklist Matrix parser script
│   └── tests/                        # Comprehensive unit test suites
│       ├── test_database.py
│       ├── test_skills.py
│       ├── test_agents.py
│       └── test_api.py
└── frontend/                         # Premium React SPA testing console
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/
        ├── main.jsx
        ├── index.css                 # Slate dark glassmorphism design tokens & log layout
        └── App.jsx                   # Live Stream Terminal window & tabbed scorecard workspace
```

---

## 🧠 Autonomous Logic & Agent Execution Runtime

The agent logic relies on an **OpenClaw-inspired stateful persistent runtime engine** implemented in `backend/agent/runtime.py`. It operates as a state-machine intercepting streamed tool-use deltas:

### Phase 1: The Gatherer (`researcher.py`)
- **System Objective**: Driven entirely by `prompts/stock_research_template.md`. Instructed to behave as an aggressive parameters collector.
- **Behavioral Loop**: Sends reasoning text blocks (`Thought:`) live over SSE. If parameters are undisclosed on primary sites, it autonomously utilizes `search_web` to discover alternative target documentation links, opens them via `browse_page`, captures clean text summaries as internal observations, and repeats its cycle until the complete 7-section document layout is emitted.

### Phase 2: The Evaluator (`evaluator.py`)
- **System Objective**: Evaluates compiled Phase 1 text alongside `prompts/stock_picking_checklist.md`.
- **Behavioral Loop**: Performs rigid numeric checking against financial formulas (ROIC > 15%, Debt/Equity ratios, margin of safety drops). It concludes by generating a valid, clean JSON structured object containing explicit sub-category badges and checklist log evaluation matrices.

---

## 🔌 API Endpoints & Server-Sent Events (SSE) Mechanics

The backend exposes a highly robust REST layer integrated with long-polling streams:

| HTTP Method | Path | Description | Payload / Response |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/research` | Initialize or reset deep research job tracker row. | Req: `{"symbol": "SUNPHARMA"}`<br>Res: `JobResponse` object. |
| **GET** | `/api/research/{symbol}/stream` | **Server-Sent Events (SSE)** core connection. Pushes thoughts, tool results, and verdicts. | Res: `text/event-stream` chunks formatted as `"data: {...}\n\n"`. |
| **GET** | `/api/research/{symbol}` | Fetches stored state profile, raw extracted metrics, and final JSON structures. | Res: Structured JSON state map containing all `logs`. |
| **GET** | `/api/research` | Catalog array listing all historically tested stock symbols. | Res: Array of `JobResponse` summaries. |

---

## 🛠️ Instructions for Future Extending or Modifying

When adding new features or debugging this codebase, strictly follow these operational patterns:

1. **Adding a New Autonomous Skill / Tool**:
   - Define the Python execution code inside `backend/agent/skills.py`.
   - Update `get_tool_schemas()` in `skills.py` to export its exact OpenAI-compatible JSON schema. Ensure descriptions are descriptive so local LLMs can route requests autonomously.
   - Update the tool invocation router block inside `backend/agent/runtime.py` to safely intercept the function string name and parse incoming argument parameters.
2. **Modifying Database Models**:
   - Update properties inside `backend/models.py`.
   - Since SQLite schema tables do not use complex Alembic migration scripts by default, drop the local `research_agent.db` file or run `Base.metadata.create_all(bind=engine)` to cleanly synchronize updated column layouts during development.
3. **Debugging Streaming Interruption**:
   - Inspect output chunks logged inside `backend/agent/runtime.py`. If a specific local model emits malformed JSON payloads for tool arguments, verify if its instruction templates support native streaming tool calling deltas cleanly.
4. **Preserving Visual Aesthetics**:
   - The React dashboard interface adheres to elite visual design standards. Never replace custom styling with generic templates. Maintain dark mode slate tokens, glassmorphic card overlays, and clean monospace formatting for live streaming execution logs.

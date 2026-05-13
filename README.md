# Stock Deep Research Agent

An autonomous, agentic financial research platform powered by local Large Language Models. Built to conduct multi-phase deep web-research, scrape tabular financial parameters, compute optimal discounted entry price models, and deliver definitive investment recommendations.

---

## ✨ Key Features

- **Fully Autonomous Web Exploration**: Emulates persistent agentic architectures to browse live pages via headless **Playwright** chromium sessions and retrieve documentation references via **DuckDuckGo** organic web queries.
- **Two-Phase Workflow Execution**:
  - **Phase 1 (Agentic Gather)**: Aggressively searches the web to complete all 7 fundamental profiling sections mapping precisely to `prompts/stock_research_template.md`.
  - **Phase 2 (Final Verdict)**: Audits the gathered financials against the strict rules of `prompts/stock_picking_checklist.md` to run criteria formulas (ROIC > 15%, Debt/Equity metrics), evaluate moats, and compute targeted entry discount targets.
- **Real-Time Streaming Interface**: Pushes incoming reasoning tokens (`Thought:` blocks), active tool executions, and state transformations live over **Server-Sent Events (SSE)**.
- **Premium Live Testing Dashboard**: Implements an elite React SPA monitoring interface configured with dark-mode slate glassmorphism design tokens, auto-scrolling execution terminal windows, and rendered status matrices.
- **Zero-Build Containerization**: Direct execution injection mapping workspace source files straight into pre-built official base images (`mcr.microsoft.com/playwright/python` and `node:20-alpine`) at runtime without compiling static Dockerfile layers.

---

## 📋 Prerequisites

1. **LM Studio**: Installed locally with an instruction-following/tool-calling optimized LLM loaded (e.g., Llama 3, Qwen 2.5, or customized Gemma setups).
2. **Docker & Docker Compose**: Configured on your host machine to orchestrate the backend/frontend containers cleanly.

---

## 🚀 How to Run

### Step 1: Configure LM Studio Server
1. Open **LM Studio** on your machine.
2. Navigate to the **Local Server** tab.
3. Ensure the server is actively running on **Port `1234`** and verify that **CORS (Cross-Origin Resource Sharing)** is enabled.

#### 🤖 Configuring the Targeted Model
The application handles model discovery automatically:
- **Auto-Discovery (Default)**: By default, the backend configuration leaves `MODEL_NAME="default"`. Upon initialization, the agent calls the LM Studio `/v1/models` endpoint autonomously and simply routes traffic to whichever local model is actively loaded in your LM Studio session.
- **Manual Override**: If you have multiple models hosted simultaneously and wish to lock execution to a designated model identifier (e.g., `"gemma-4-e2b"` or `"qwen2.5-coder"`), open `docker-compose.yml` and add `- MODEL_NAME=your-model-identifier` under the `backend` service environment variables block.

### Step 2: Boot Containerized Pipelines
Because the project uses execution-environment container injection, running the entire stack requires zero local setup or compilation build time. Simply execute from the project root:

```bash
docker compose up
```

On initial startup, the backend service container will automatically install Python requirements, synchronize headless browser binaries, and launch the hot-reloading FastAPI backend on port `8000`. Simultaneously, the frontend node service will download client dependencies and host the Vite dev console on port `3000`.

### Step 3: Launch Research Dashboard
1. Open your browser and navigate to:
   ```text
   http://localhost:3000
   ```
2. Enter any targeted stock symbol (e.g., `SUNPHARMA`, `INFOTECH`, `TCS`, `HDFCBANK`) into the launcher input bar.
3. Observe live reasoning thought streams on the terminal console while the agent gathers structured data blocks and computes definitive evaluation verdicts!

---

## 📡 REST API Reference

Developers can trigger or integrate deep research workflows programmatically:

### 1. Trigger Deep Research Session
```http
POST /api/research
Content-Type: application/json

{
  "symbol": "SUNPHARMA"
}
```
**Response**: Returns the created or reset tracking job object (`status: "pending"`).

### 2. Stream Real-Time Pipeline Events
```http
GET /api/research/SUNPHARMA/stream
```
**Response**: Yields continuous stream packets formatted as text/event-stream data channels containing real-time logs, thoughts, tool inputs, and phase states.

### 3. Fetch Consolidated State Ledger
```http
GET /api/research/SUNPHARMA
```
**Response**: Retrieves full historical state profiles, compiled fundamental markdown blocks, raw json verdicts, and granular log rows persisted to the swappable SQLite database layer.

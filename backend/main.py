import json
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models import Base, StockResearchJob, ResearchLog
from backend.database import engine, get_db, SessionLocal
from backend.agent.researcher import gather_stock_data
from backend.agent.evaluator import evaluate_stock_verdict

# Ensure database tables are synchronized
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    symbol: str
    run_background: Optional[bool] = False

class JobResponse(BaseModel):
    id: int
    symbol: str
    status: str
    gathered_data: Optional[str] = None
    verdict_json: Optional[str] = None

def run_research_in_background(job_id: int, symbol: str):
    """Executes full agentic collection and scoring lifecycle sequentially inside isolated background workers."""
    print(f"🚀 Spawning isolated background worker queue for target ticker: {symbol} (Job ID: {job_id})", flush=True)
    db = SessionLocal()
    try:
        for _ in gather_stock_data(job_id=job_id, symbol=symbol, db=db):
            pass
        print(f"✅ Phase 1 gathering finalized for {symbol}. Initializing Phase 2 evaluation...", flush=True)
        for _ in evaluate_stock_verdict(job_id=job_id, symbol=symbol, db=db):
            pass
        print(f"🎉 Fully completed deep research task execution for {symbol}!", flush=True)
    except Exception as e:
        print(f"❌ Background worker task exception encountered for {symbol}: {str(e)}", flush=True)
        job = db.query(StockResearchJob).filter(StockResearchJob.id == job_id).first()
        if job:
            job.status = "failed"
            db.commit()
    finally:
        db.close()

@app.post("/api/research", response_model=JobResponse)
def trigger_research_job(req: ResearchRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Initialize a deep research session tracker row for a targeted stock ticker symbol."""
    symbol_upper = req.symbol.strip().upper()
    if not symbol_upper:
        raise HTTPException(status_code=400, detail="Stock symbol cannot be empty.")
        
    job = db.query(StockResearchJob).filter(StockResearchJob.symbol == symbol_upper).first()
    if not job:
        job = StockResearchJob(symbol=symbol_upper, status="pending")
        db.add(job)
        db.commit()
        db.refresh(job)
    else:
        # Reset failed or stale jobs to allow re-triggering testing streams cleanly
        if job.status in ["failed", "completed"]:
            job.status = "pending"
            job.gathered_data = None
            job.verdict_json = None
            # Clear stale historical session logs
            db.query(ResearchLog).filter(ResearchLog.job_id == job.id).delete()
            db.commit()
            db.refresh(job)
            
    # Trigger isolated execution lifecycle if requested specifically by client configuration
    if req.run_background:
        background_tasks.add_task(run_research_in_background, job.id, symbol_upper)
            
    return job

@app.get("/api/research/{symbol}/stream")
async def stream_research_phases(symbol: str, db: Session = Depends(get_db)):
    """
    Server-Sent Events streaming handler pushing continuous real-time thoughts, tool deltas,
    and final evaluation phase verdict JSONs instantly to the frontend developer console.
    """
    symbol_upper = symbol.strip().upper()
    job = db.query(StockResearchJob).filter(StockResearchJob.symbol == symbol_upper).first()
    
    if not job:
        raise HTTPException(status_code=404, detail=f"No active research job found for symbol: '{symbol_upper}'. Call POST /api/research first.")

    async def event_generator():
        # If job is already fully completed, emit final verdict summary directly
        if job.status == "completed" and job.verdict_json:
            yield f"data: {json.dumps({'type': 'status', 'content': 'Historical research session retrieved successfully.'})}\n\n"
            await asyncio.sleep(0.1)
            yield f"data: {json.dumps({'type': 'verdict', 'content': job.verdict_json})}\n\n"
            return

        try:
            # Phase 1 Live Execution Stream
            yield f"data: {json.dumps({'type': 'phase_switch', 'content': f'Initiating Phase 1 Agentic fundamental parameter extraction for {symbol_upper}...'})}\n\n"
            await asyncio.sleep(0.1)
            
            # Since generator executes synchronous network calls, wrap iterations with sleep to unblock Starlette event loops cleanly
            for chunk_str in gather_stock_data(job_id=job.id, symbol=symbol_upper, db=db):
                yield f"data: {chunk_str}\n\n"
                await asyncio.sleep(0.05)

            # Phase 2 Live Execution Stream
            yield f"data: {json.dumps({'type': 'phase_switch', 'content': f'Initiating Phase 2 checklist matrix evaluation for {symbol_upper}...'})}\n\n"
            await asyncio.sleep(0.1)
            
            for chunk_str in evaluate_stock_verdict(job_id=job.id, symbol=symbol_upper, db=db):
                yield f"data: {chunk_str}\n\n"
                await asyncio.sleep(0.05)
                
            yield f"data: {json.dumps({'type': 'status', 'content': 'Deep research pipeline execution fully complete.'})}\n\n"
        except Exception as e:
            err_payload = json.dumps({"type": "error", "content": f"Pipeline interruption: {str(e)}"})
            yield f"data: {err_payload}\n\n"
            if job:
                job.status = "failed"
                db.commit()

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/research/{symbol}", response_model=Dict[str, Any])
def get_research_state(symbol: str, db: Session = Depends(get_db)):
    """Fetch structured full state profiles including final complete data blocks."""
    symbol_upper = symbol.strip().upper()
    job = db.query(StockResearchJob).filter(StockResearchJob.symbol == symbol_upper).first()
    if not job:
        raise HTTPException(status_code=404, detail="Stock research not found.")
        
    logs = db.query(ResearchLog).filter(ResearchLog.job_id == job.id).order_by(ResearchLog.id.asc()).all()
    formatted_logs = [{"timestamp": l.timestamp.isoformat(), "type": l.log_type, "content": l.content} for l in logs]
    
    # Try parsing verdict string directly if stored cleanly
    parsed_verdict = {}
    if job.verdict_json:
        try:
            parsed_verdict = json.loads(job.verdict_json)
        except Exception:
            parsed_verdict = {"raw": job.verdict_json}

    return {
        "id": job.id,
        "symbol": job.symbol,
        "status": job.status,
        "updated_at": job.updated_at.isoformat(),
        "gathered_data": job.gathered_data,
        "verdict": parsed_verdict,
        "logs": formatted_logs
    }

@app.get("/api/research", response_model=List[JobResponse])
def list_researched_stocks(db: Session = Depends(get_db)):
    """Retrieve full history catalog of all researched public stocks."""
    return db.query(StockResearchJob).order_by(StockResearchJob.updated_at.desc()).all()

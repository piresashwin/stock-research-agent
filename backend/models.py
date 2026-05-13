from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class StockResearchJob(Base):
    __tablename__ = "stock_research_jobs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    status = Column(String, default="pending", index=True)  # pending, gathering, evaluating, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    gathered_data = Column(Text, nullable=True)  # Phase 1 completed template markdown
    verdict_json = Column(Text, nullable=True)   # Phase 2 structured JSON verdict

    logs = relationship("ResearchLog", back_populates="job", cascade="all, delete-orphan")


class ResearchLog(Base):
    __tablename__ = "research_logs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("stock_research_jobs.id"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    log_type = Column(String, nullable=False)  # thought, tool_call, tool_result, phase_switch, error
    content = Column(Text, nullable=False)

    job = relationship("StockResearchJob", back_populates="logs")

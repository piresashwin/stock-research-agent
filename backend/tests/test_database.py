import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, StockResearchJob, ResearchLog

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_research_job(db_session):
    job = StockResearchJob(symbol="INFOTECH", status="pending")
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)

    assert job.id is not None
    assert job.symbol == "INFOTECH"
    assert job.status == "pending"
    assert job.gathered_data is None

def test_create_research_log(db_session):
    job = StockResearchJob(symbol="SUNPHARMA", status="gathering")
    db_session.add(job)
    db_session.commit()

    log = ResearchLog(job_id=job.id, log_type="thought", content="Searching for latest quarterly results")
    db_session.add(log)
    db_session.commit()

    assert len(job.logs) == 1
    assert job.logs[0].log_type == "thought"
    assert job.logs[0].content == "Searching for latest quarterly results"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings

# For SQLite, check_same_thread=False is needed when sharing sessions across worker threads
connect_args = {"check_same_thread": False, "timeout": 30} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(
    settings.database_url, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

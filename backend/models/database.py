from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.core.config import settings

# Use SQLite by default for zero-config local run, but allow PostgreSQL override
if settings.DATABASE_URL and settings.DATABASE_URL.startswith("postgresql"):
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    # Use SQLite if no Postgres URL is provided
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sentiment.db"
    # check_same_thread=False is needed for SQLite with FastAPI
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url)

# Session-Factory – wird per Depends(get_db) in die Routes injiziert
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Basisklasse für alle Domain-Entities (User, Message, Quiz, ...)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""Shared pytest fixtures."""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure mock LLM and SQLite for all tests before app import side effects
os.environ.setdefault("LLM_PROVIDER", "mock")
os.environ.setdefault("DATABASE_URL", "sqlite://")

from app.api.deps import get_db, get_llm_client
from app.db.base import Base
from app.main import create_app
from app.services.llm.mock import MockLLM


@pytest.fixture
def db_engine():
    """Create an in-memory SQLite engine for tests."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db_session(db_engine) -> Generator[Session, None, None]:
    """Provide a database session bound to the test engine."""
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = testing_session_local()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def mock_llm() -> MockLLM:
    """Provide a deterministic mock LLM client."""
    return MockLLM()


@pytest.fixture
def client(db_session: Session, mock_llm: MockLLM) -> Generator[TestClient, None, None]:
    """Provide a FastAPI test client with overridden dependencies."""
    application = create_app()

    def _override_get_db() -> Generator[Session, None, None]:
        yield db_session

    application.dependency_overrides[get_db] = _override_get_db
    application.dependency_overrides[get_llm_client] = lambda: mock_llm

    with TestClient(application) as test_client:
        yield test_client

    application.dependency_overrides.clear()

"""FastAPI dependency injection helpers."""

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.database import get_db
from app.repositories.message_repository import MessageRepository
from app.repositories.quiz_repository import QuizRepository
from app.repositories.session_repository import SessionRepository
from app.services.chat_service import ChatService
from app.services.llm.client import LLMClient
from app.services.llm.factory import create_llm_client
from app.services.quiz_service import QuizService


def get_settings_dep() -> Settings:
    """Dependency for application settings."""
    return get_settings()


def get_llm_client(settings: Settings = Depends(get_settings_dep)) -> LLMClient:
    """Dependency for LLM client."""
    return create_llm_client(settings)


def get_session_repository(db: Session = Depends(get_db)) -> SessionRepository:
    """Dependency for session repository."""
    return SessionRepository(db)


def get_message_repository(db: Session = Depends(get_db)) -> MessageRepository:
    """Dependency for message repository."""
    return MessageRepository(db)


def get_quiz_repository(db: Session = Depends(get_db)) -> QuizRepository:
    """Dependency for quiz repository."""
    return QuizRepository(db)


def get_chat_service(
    session_repo: SessionRepository = Depends(get_session_repository),
    message_repo: MessageRepository = Depends(get_message_repository),
    llm_client: LLMClient = Depends(get_llm_client),
) -> ChatService:
    """Dependency for chat service."""
    return ChatService(session_repo, message_repo, llm_client)


def get_quiz_service(
    session_repo: SessionRepository = Depends(get_session_repository),
    quiz_repo: QuizRepository = Depends(get_quiz_repository),
    llm_client: LLMClient = Depends(get_llm_client),
) -> QuizService:
    """Dependency for quiz service."""
    return QuizService(session_repo, quiz_repo, llm_client)


def override_get_db(test_db: Session) -> Generator[Session, None, None]:
    """Override database session for tests."""
    yield test_db

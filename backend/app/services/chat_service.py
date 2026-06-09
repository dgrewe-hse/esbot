"""Chat service orchestrating messages and LLM responses."""

import logging
import uuid
from dataclasses import dataclass

from app.core.exceptions import NotFoundError
from app.db.models import MessageORM, UserSessionORM
from app.domain.enums import MessageRole
from app.repositories.message_repository import MessageRepository
from app.repositories.session_repository import SessionRepository
from app.services.llm.client import LLMClient
from app.services.llm.mock import FALLBACK_MESSAGE

logger = logging.getLogger(__name__)


@dataclass
class MessageExchangeResult:
    """Result of sending a message and receiving a response."""

    user_message: MessageORM
    assistant_message: MessageORM
    degraded: bool = False


class ChatService:
    """Business logic for learning session chat interactions."""

    def __init__(
        self,
        session_repo: SessionRepository,
        message_repo: MessageRepository,
        llm_client: LLMClient,
    ) -> None:
        self._session_repo = session_repo
        self._message_repo = message_repo
        self._llm = llm_client

    def start_session(self, user_id: str, title: str = "New Learning Session") -> UserSessionORM:
        """Create a new learning session."""
        return self._session_repo.create(user_id=user_id, title=title)

    def get_session(self, session_id: uuid.UUID) -> UserSessionORM:
        """Retrieve a session or raise NotFoundError."""
        session = self._session_repo.find_by_id(session_id)
        if session is None:
            raise NotFoundError("Session", str(session_id))
        return session

    def list_sessions(self, user_id: str) -> list[UserSessionORM]:
        """List all sessions for a user."""
        return self._session_repo.find_by_user(user_id)

    def delete_session(self, session_id: uuid.UUID) -> None:
        """Delete a session or raise NotFoundError."""
        deleted = self._session_repo.delete(session_id)
        if not deleted:
            raise NotFoundError("Session", str(session_id))

    def get_message_history(self, session_id: uuid.UUID) -> list[MessageORM]:
        """Return chronological message history for a session."""
        self.get_session(session_id)
        return self._message_repo.get_history(session_id)

    async def send_message(self, session_id: uuid.UUID, content: str) -> MessageExchangeResult:
        """Send a user message, get LLM response, and persist both."""
        session = self.get_session(session_id)
        user_message = self._message_repo.append(session_id, MessageRole.USER, content)

        degraded = False
        try:
            topic = session.title or "general learning"
            assistant_content = await self._llm.explain(topic, content)
        except Exception as exc:
            logger.warning("LLM explain failed for session %s: %s", session_id, exc)
            assistant_content = FALLBACK_MESSAGE
            degraded = True

        assistant_message = self._message_repo.append(
            session_id, MessageRole.ASSISTANT, assistant_content
        )
        self._session_repo.update_metadata(session)

        return MessageExchangeResult(
            user_message=user_message,
            assistant_message=assistant_message,
            degraded=degraded,
        )

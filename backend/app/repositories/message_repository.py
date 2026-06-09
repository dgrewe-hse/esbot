"""Repository for chat message persistence."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MessageORM
from app.domain.enums import MessageRole


class MessageRepository:
    """Data access layer for session messages."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def append(
        self,
        session_id: uuid.UUID,
        role: MessageRole,
        content: str,
    ) -> MessageORM:
        """Append a message to a session."""
        message = MessageORM(
            session_id=session_id,
            role=role.value,
            content=content.strip(),
        )
        self._db.add(message)
        self._db.commit()
        self._db.refresh(message)
        return message

    def get_history(self, session_id: uuid.UUID) -> list[MessageORM]:
        """Return all messages for a session in chronological order."""
        stmt = (
            select(MessageORM)
            .where(MessageORM.session_id == session_id)
            .order_by(MessageORM.created_at.asc())
        )
        return list(self._db.scalars(stmt).all())

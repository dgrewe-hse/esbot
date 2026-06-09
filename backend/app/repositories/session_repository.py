"""Repository for user session persistence."""

import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import UserSessionORM


class SessionRepository:
    """Data access layer for learning sessions."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, user_id: str, title: str = "New Learning Session") -> UserSessionORM:
        """Create and persist a new learning session."""
        session = UserSessionORM(user_id=user_id.strip(), title=title.strip())
        self._db.add(session)
        self._db.commit()
        self._db.refresh(session)
        return session

    def find_by_id(self, session_id: uuid.UUID) -> UserSessionORM | None:
        """Find a session by its unique identifier."""
        return self._db.get(UserSessionORM, session_id)

    def find_by_user(self, user_id: str) -> list[UserSessionORM]:
        """Return all sessions for a given user, newest first."""
        stmt = (
            select(UserSessionORM)
            .where(UserSessionORM.user_id == user_id)
            .order_by(UserSessionORM.last_activity_at.desc())
        )
        return list(self._db.scalars(stmt).all())

    def update_metadata(
        self,
        session: UserSessionORM,
        *,
        title: str | None = None,
        last_activity_at: datetime | None = None,
    ) -> UserSessionORM:
        """Update session metadata such as title or last activity timestamp."""
        if title is not None:
            session.title = title.strip()
        if last_activity_at is not None:
            session.last_activity_at = last_activity_at
        else:
            session.last_activity_at = datetime.now(UTC)
        self._db.commit()
        self._db.refresh(session)
        return session

    def delete(self, session_id: uuid.UUID) -> bool:
        """Delete a session and all associated data via cascade."""
        session = self.find_by_id(session_id)
        if session is None:
            return False
        self._db.delete(session)
        self._db.commit()
        return True

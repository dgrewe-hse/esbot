"""SQLAlchemy ORM models for ESBot persistence."""

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.enums import MessageRole


class UserSessionORM(Base):
    """Persisted user learning session."""

    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(256), nullable=False, default="New Learning Session")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    messages: Mapped[list["MessageORM"]] = relationship(
        back_populates="session", cascade="all, delete-orphan", order_by="MessageORM.created_at"
    )
    quiz_requests: Mapped[list["QuizRequestORM"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class MessageORM(Base):
    """Persisted chat message."""

    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("user_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(16), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["UserSessionORM"] = relationship(back_populates="messages")

    @property
    def role_enum(self) -> MessageRole:
        """Return the message role as an enum."""
        return MessageRole(self.role)


class QuizRequestORM(Base):
    """Persisted quiz generation request."""

    __tablename__ = "quiz_requests"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("user_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session: Mapped["UserSessionORM"] = relationship(back_populates="quiz_requests")
    items: Mapped[list["QuizItemORM"]] = relationship(
        back_populates="quiz_request", cascade="all, delete-orphan"
    )


class QuizItemORM(Base):
    """Persisted quiz question."""

    __tablename__ = "quiz_items"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    quiz_request_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("quiz_requests.id", ondelete="CASCADE"), nullable=False, index=True
    )
    question: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    correct_answer: Mapped[str] = mapped_column(String(500), nullable=False)

    quiz_request: Mapped["QuizRequestORM"] = relationship(back_populates="items")
    submitted_answers: Mapped[list["SubmittedAnswerORM"]] = relationship(
        back_populates="quiz_item", cascade="all, delete-orphan"
    )


class SubmittedAnswerORM(Base):
    """Persisted user answer to a quiz question."""

    __tablename__ = "submitted_answers"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    quiz_item_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("quiz_items.id", ondelete="CASCADE"), nullable=False, index=True
    )
    answer: Mapped[str] = mapped_column(String(500), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    quiz_item: Mapped["QuizItemORM"] = relationship(back_populates="submitted_answers")
    evaluation: Mapped["EvaluationResultORM | None"] = relationship(
        back_populates="submitted_answer", cascade="all, delete-orphan", uselist=False
    )


class EvaluationResultORM(Base):
    """Persisted evaluation feedback for a submitted answer."""

    __tablename__ = "evaluation_results"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    submitted_answer_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("submitted_answers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    is_correct: Mapped[bool] = mapped_column(nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)

    submitted_answer: Mapped["SubmittedAnswerORM"] = relationship(back_populates="evaluation")

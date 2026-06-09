"""Pydantic domain models for validation (no persistence)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.enums import MessageRole


class UserSessionDomain(BaseModel):
    """Domain model for a user learning session."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    user_id: str = Field(..., min_length=1, max_length=128)
    title: str = Field(default="New Learning Session", min_length=1, max_length=256)
    created_at: datetime | None = None
    last_activity_at: datetime | None = None

    @field_validator("user_id", "title")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        """Reject blank strings after stripping whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class MessageDomain(BaseModel):
    """Domain model for a chat message."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    session_id: UUID
    role: MessageRole
    content: str = Field(..., min_length=1, max_length=4000)
    created_at: datetime | None = None

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        """Ensure message content is not empty."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("content must not be blank")
        return stripped


class QuizRequestDomain(BaseModel):
    """Domain model for a quiz generation request."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    session_id: UUID
    topic: str = Field(..., min_length=1, max_length=256)
    created_at: datetime | None = None

    @field_validator("topic")
    @classmethod
    def topic_not_blank(cls, value: str) -> str:
        """Ensure quiz topic is not empty."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("topic must not be blank")
        return stripped


class QuizItemDomain(BaseModel):
    """Domain model for a single quiz question."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    quiz_request_id: UUID
    question: str = Field(..., min_length=1, max_length=1000)
    options: list[str] = Field(default_factory=list)
    correct_answer: str = Field(..., min_length=1, max_length=500)

    @field_validator("question", "correct_answer")
    @classmethod
    def not_blank(cls, value: str) -> str:
        """Ensure required string fields are not blank."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class SubmittedAnswerDomain(BaseModel):
    """Domain model for a user's submitted quiz answer."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    quiz_item_id: UUID
    answer: str = Field(..., min_length=1, max_length=500)
    submitted_at: datetime | None = None

    @field_validator("answer")
    @classmethod
    def answer_not_blank(cls, value: str) -> str:
        """Ensure submitted answer is not empty."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("answer must not be blank")
        return stripped


class EvaluationResultDomain(BaseModel):
    """Domain model for quiz answer evaluation feedback."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None
    submitted_answer_id: UUID
    is_correct: bool
    feedback: str = Field(..., min_length=1, max_length=2000)

    @field_validator("feedback")
    @classmethod
    def feedback_not_blank(cls, value: str) -> str:
        """Ensure feedback is not empty."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("feedback must not be blank")
        return stripped

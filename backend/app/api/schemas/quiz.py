"""Quiz API schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class QuizCreateRequest(BaseModel):
    """Request body for quiz generation."""

    topic: str = Field(..., min_length=1, max_length=256)
    count: int | None = Field(default=None, ge=1, le=10)

    @field_validator("topic")
    @classmethod
    def topic_not_blank(cls, value: str) -> str:
        """Reject blank quiz topic."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("topic must not be blank")
        return stripped


class QuizItemResponse(BaseModel):
    """Single quiz question response."""

    id: UUID
    quiz_request_id: UUID
    question: str
    options: list[str]
    correct_answer: str

    model_config = {"from_attributes": True}


class QuizGenerationResponse(BaseModel):
    """Response after quiz generation."""

    quiz_request_id: UUID
    topic: str
    items: list[QuizItemResponse]
    degraded: bool = False


class AnswerSubmitRequest(BaseModel):
    """Request body for answer submission."""

    answer: str = Field(..., min_length=1, max_length=500)


class EvaluationResponse(BaseModel):
    """Evaluation feedback response."""

    submitted_answer_id: UUID
    quiz_item_id: UUID
    answer: str
    is_correct: bool
    feedback: str
    submitted_at: datetime
    degraded: bool = False

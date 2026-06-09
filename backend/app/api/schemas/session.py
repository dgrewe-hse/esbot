"""Session API schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class SessionCreateRequest(BaseModel):
    """Request body for creating a session."""

    user_id: str = Field(..., min_length=1, max_length=128)
    title: str = Field(default="New Learning Session", min_length=1, max_length=256)

    @field_validator("user_id", "title")
    @classmethod
    def not_blank(cls, value: str) -> str:
        """Reject blank strings."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("must not be blank")
        return stripped


class SessionResponse(BaseModel):
    """Session metadata response."""

    id: UUID
    user_id: str
    title: str
    created_at: datetime
    last_activity_at: datetime

    model_config = {"from_attributes": True}


class SessionListResponse(BaseModel):
    """List of sessions."""

    sessions: list[SessionResponse]

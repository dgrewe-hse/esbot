"""Message API schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from app.domain.enums import MessageRole


class MessageCreateRequest(BaseModel):
    """Request body for sending a message."""

    content: str = Field(..., min_length=1, max_length=4000)

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        """Reject blank message content."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("content must not be blank")
        return stripped


class MessageResponse(BaseModel):
    """Single message response."""

    id: UUID
    session_id: UUID
    role: MessageRole
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageExchangeResponse(BaseModel):
    """Response after sending a message."""

    user_message: MessageResponse
    assistant_message: MessageResponse
    degraded: bool = False


class MessageListResponse(BaseModel):
    """List of messages in a session."""

    messages: list[MessageResponse]

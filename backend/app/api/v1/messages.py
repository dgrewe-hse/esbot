"""Message REST endpoints."""

import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import get_chat_service
from app.api.schemas.message import (
    MessageCreateRequest,
    MessageExchangeResponse,
    MessageListResponse,
    MessageResponse,
)
from app.services.chat_service import ChatService

router = APIRouter()


@router.post(
    "/{session_id}/messages",
    response_model=MessageExchangeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def send_message(
    session_id: uuid.UUID,
    body: MessageCreateRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> MessageExchangeResponse:
    """Send a message and receive an AI-generated response."""
    result = await chat_service.send_message(session_id, body.content)
    return MessageExchangeResponse(
        user_message=MessageResponse.model_validate(result.user_message),
        assistant_message=MessageResponse.model_validate(result.assistant_message),
        degraded=result.degraded,
    )


@router.get("/{session_id}/messages", response_model=MessageListResponse)
def get_messages(
    session_id: uuid.UUID,
    chat_service: ChatService = Depends(get_chat_service),
) -> MessageListResponse:
    """Retrieve full message history for a session."""
    messages = chat_service.get_message_history(session_id)
    return MessageListResponse(messages=[MessageResponse.model_validate(m) for m in messages])

"""Session REST endpoints."""

import uuid

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response

from app.api.deps import get_chat_service
from app.api.schemas.session import SessionCreateRequest, SessionListResponse, SessionResponse
from app.services.chat_service import ChatService

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    body: SessionCreateRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> SessionResponse:
    """Create a new learning session."""
    session = chat_service.start_session(user_id=body.user_id, title=body.title)
    return SessionResponse.model_validate(session)


@router.get("", response_model=SessionListResponse)
def list_sessions(
    user_id: str = Query(..., min_length=1),
    chat_service: ChatService = Depends(get_chat_service),
) -> SessionListResponse:
    """List all sessions for a user."""
    sessions = chat_service.list_sessions(user_id)
    return SessionListResponse(sessions=[SessionResponse.model_validate(s) for s in sessions])


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: uuid.UUID,
    chat_service: ChatService = Depends(get_chat_service),
) -> SessionResponse:
    """Get session metadata by ID."""
    session = chat_service.get_session(session_id)
    return SessionResponse.model_validate(session)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: uuid.UUID,
    chat_service: ChatService = Depends(get_chat_service),
) -> Response:
    """Delete a session and all associated data."""
    chat_service.delete_session(session_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

"""API v1 router aggregation."""

from fastapi import APIRouter

from app.api.v1 import health, messages, quiz, sessions

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(messages.router, prefix="/sessions", tags=["messages"])
api_router.include_router(quiz.router, prefix="/sessions", tags=["quiz"])

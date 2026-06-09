"""Health check endpoint."""

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return application liveness status."""
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }

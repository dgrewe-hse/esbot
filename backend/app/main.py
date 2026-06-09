"""FastAPI application entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import (
    ESBotError,
    LLMServiceError,
    NotFoundError,
    ValidationError,
    llm_service_exception,
    not_found_exception,
    validation_exception,
)
from app.core.logging import setup_logging


def _init_sqlite_schema() -> None:
    """Create tables automatically when using SQLite (tests and performance runs)."""
    settings = get_settings()
    if not settings.database_url.startswith("sqlite"):
        return

    import app.db.models  # noqa: F401 — register ORM models with Base.metadata
    from app.core.database import engine
    from app.db.base import Base

    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan handler for startup and shutdown."""
    setup_logging()
    _init_sqlite_schema()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
    )

    @application.exception_handler(NotFoundError)
    async def handle_not_found(_request: Request, exc: NotFoundError) -> JSONResponse:
        http_exc = not_found_exception(exc)
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})

    @application.exception_handler(ValidationError)
    async def handle_validation(_request: Request, exc: ValidationError) -> JSONResponse:
        http_exc = validation_exception(exc)
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})

    @application.exception_handler(LLMServiceError)
    async def handle_llm_error(_request: Request, exc: LLMServiceError) -> JSONResponse:
        http_exc = llm_service_exception(exc)
        return JSONResponse(status_code=http_exc.status_code, content={"detail": http_exc.detail})

    @application.exception_handler(ESBotError)
    async def handle_esbot_error(_request: Request, exc: ESBotError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    application.include_router(api_router)
    return application


app = create_app()

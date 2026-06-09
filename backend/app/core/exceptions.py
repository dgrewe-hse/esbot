"""Domain and HTTP exception types."""

from fastapi import HTTPException, status


class ESBotError(Exception):
    """Base exception for ESBot domain errors."""


class NotFoundError(ESBotError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: str) -> None:
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' not found")


class ValidationError(ESBotError):
    """Raised when domain validation fails."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class LLMServiceError(ESBotError):
    """Raised when the LLM inference engine is unavailable or returns an error."""

    def __init__(self, message: str = "LLM service unavailable") -> None:
        self.message = message
        super().__init__(message)


def not_found_exception(exc: NotFoundError) -> HTTPException:
    """Map a NotFoundError to an HTTP 404 response."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{exc.resource} not found",
    )


def validation_exception(exc: ValidationError) -> HTTPException:
    """Map a ValidationError to an HTTP 422 response."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=exc.message,
    )


def llm_service_exception(exc: LLMServiceError) -> HTTPException:
    """Map an LLMServiceError to an HTTP 503 response."""
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=exc.message,
    )

"""Smoke tests for application startup."""

import pytest
from app.main import create_app
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit


def test_app_starts():
    """Verify the FastAPI application can be created."""
    application = create_app()
    assert application.title == "ESBot API"


def test_health_endpoint_without_db_override():
    """Verify health endpoint works without database."""
    application = create_app()
    with TestClient(application) as client:
        response = client.get("/api/v1/health")
        assert response.status_code == 200

"""Integration tests for session API endpoints."""

import uuid

import pytest

pytestmark = pytest.mark.integration


def test_health_check(client):
    """Verify health endpoint returns ok."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_session(client):
    """Verify session creation returns 201."""
    response = client.post(
        "/api/v1/sessions",
        json={"user_id": "student-1", "title": "Python Basics"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == "student-1"
    assert data["title"] == "Python Basics"
    assert "id" in data


def test_list_sessions(client):
    """Verify sessions can be listed by user."""
    client.post("/api/v1/sessions", json={"user_id": "student-1"})
    client.post("/api/v1/sessions", json={"user_id": "student-1"})
    response = client.get("/api/v1/sessions", params={"user_id": "student-1"})
    assert response.status_code == 200
    assert len(response.json()["sessions"]) == 2


def test_get_session_not_found(client):
    """Verify 404 for unknown session."""
    response = client.get(f"/api/v1/sessions/{uuid.uuid4()}")
    assert response.status_code == 404


def test_delete_session(client):
    """Verify session deletion returns 204."""
    create_resp = client.post("/api/v1/sessions", json={"user_id": "student-1"})
    session_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/sessions/{session_id}")
    assert response.status_code == 204


def test_create_session_validation_error(client):
    """Verify 422 for invalid input."""
    response = client.post("/api/v1/sessions", json={"user_id": "", "title": "Test"})
    assert response.status_code == 422

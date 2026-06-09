"""Integration tests for message API endpoints."""

import uuid

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture
def session_id(client):
    """Create a session and return its ID."""
    response = client.post("/api/v1/sessions", json={"user_id": "student-1"})
    return response.json()["id"]


def test_send_message(client, session_id):
    """Verify message exchange returns user and assistant messages."""
    response = client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json={"content": "What is a variable?"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_message"]["content"] == "What is a variable?"
    assert data["assistant_message"]["role"] == "assistant"
    assert data["degraded"] is False


def test_get_message_history(client, session_id):
    """Verify message history is returned chronologically."""
    client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json={"content": "First question"},
    )
    response = client.get(f"/api/v1/sessions/{session_id}/messages")
    assert response.status_code == 200
    messages = response.json()["messages"]
    assert len(messages) == 2


def test_send_message_empty_content(client, session_id):
    """Verify 422 for empty message content."""
    response = client.post(
        f"/api/v1/sessions/{session_id}/messages",
        json={"content": "   "},
    )
    assert response.status_code == 422


def test_send_message_session_not_found(client):
    """Verify 404 for unknown session."""
    response = client.post(
        f"/api/v1/sessions/{uuid.uuid4()}/messages",
        json={"content": "Hello"},
    )
    assert response.status_code == 404

"""Integration tests for quiz API endpoints."""

import uuid

import pytest

pytestmark = pytest.mark.integration


@pytest.fixture
def session_id(client):
    """Create a session and return its ID."""
    response = client.post("/api/v1/sessions", json={"user_id": "student-1"})
    return response.json()["id"]


def test_generate_quiz(client, session_id):
    """Verify quiz generation returns items."""
    response = client.post(
        f"/api/v1/sessions/{session_id}/quiz",
        json={"topic": "Python lists", "count": 2},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["topic"] == "Python lists"
    assert len(data["items"]) == 2
    assert data["degraded"] is False


def test_submit_answer(client, session_id):
    """Verify answer evaluation returns feedback."""
    quiz_resp = client.post(
        f"/api/v1/sessions/{session_id}/quiz",
        json={"topic": "Testing"},
    )
    question_id = quiz_resp.json()["items"][0]["id"]
    correct = quiz_resp.json()["items"][0]["correct_answer"]

    response = client.post(
        f"/api/v1/sessions/{session_id}/quiz/{question_id}/answer",
        json={"answer": correct},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["feedback"]


def test_quiz_session_not_found(client):
    """Verify 404 for quiz on unknown session."""
    response = client.post(
        f"/api/v1/sessions/{uuid.uuid4()}/quiz",
        json={"topic": "Testing"},
    )
    assert response.status_code == 404


def test_answer_question_not_found(client, session_id):
    """Verify 404 for unknown question."""
    response = client.post(
        f"/api/v1/sessions/{session_id}/quiz/{uuid.uuid4()}/answer",
        json={"answer": "A"},
    )
    assert response.status_code == 404


def test_quiz_empty_topic(client, session_id):
    """Verify 422 for empty topic."""
    response = client.post(
        f"/api/v1/sessions/{session_id}/quiz",
        json={"topic": "  "},
    )
    assert response.status_code == 422

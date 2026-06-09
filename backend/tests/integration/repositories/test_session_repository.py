"""Integration tests for SessionRepository."""

import uuid

import pytest
from app.domain.enums import MessageRole
from app.repositories.message_repository import MessageRepository
from app.repositories.session_repository import SessionRepository

pytestmark = pytest.mark.integration


def test_create_session(db_session):
    """Verify session is persisted."""
    repo = SessionRepository(db_session)
    session = repo.create(user_id="student-1", title="Test")
    assert session.id is not None
    assert session.user_id == "student-1"


def test_find_by_id(db_session):
    """Verify session can be retrieved by ID."""
    repo = SessionRepository(db_session)
    created = repo.create(user_id="student-1")
    found = repo.find_by_id(created.id)
    assert found is not None
    assert found.id == created.id


def test_find_by_user(db_session):
    """Verify sessions are filtered by user."""
    repo = SessionRepository(db_session)
    repo.create(user_id="student-1")
    repo.create(user_id="student-2")
    sessions = repo.find_by_user("student-1")
    assert len(sessions) == 1
    assert sessions[0].user_id == "student-1"


def test_append_message_and_get_history(db_session):
    """Verify messages can be appended and retrieved in order."""
    session_repo = SessionRepository(db_session)
    message_repo = MessageRepository(db_session)
    session = session_repo.create(user_id="student-1")

    message_repo.append(session.id, MessageRole.USER, "Hello")
    message_repo.append(session.id, MessageRole.ASSISTANT, "Hi there")

    history = message_repo.get_history(session.id)
    assert len(history) == 2
    assert history[0].role == MessageRole.USER.value
    assert history[1].role == MessageRole.ASSISTANT.value


def test_update_metadata(db_session):
    """Verify session metadata can be updated."""
    repo = SessionRepository(db_session)
    session = repo.create(user_id="student-1", title="Old Title")
    updated = repo.update_metadata(session, title="New Title")
    assert updated.title == "New Title"


def test_delete_session_cascades_messages(db_session):
    """Verify deleting session removes associated messages."""
    session_repo = SessionRepository(db_session)
    message_repo = MessageRepository(db_session)
    session = session_repo.create(user_id="student-1")
    message_repo.append(session.id, MessageRole.USER, "Hello")

    deleted = session_repo.delete(session.id)
    assert deleted is True
    assert session_repo.find_by_id(session.id) is None
    assert message_repo.get_history(session.id) == []


def test_delete_nonexistent_session(db_session):
    """Verify delete returns False for unknown session."""
    repo = SessionRepository(db_session)
    assert repo.delete(uuid.uuid4()) is False

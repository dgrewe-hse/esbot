"""Unit tests for UserSession domain model."""

import uuid

import pytest
from app.domain.models import UserSessionDomain
from pydantic import ValidationError

pytestmark = pytest.mark.unit


def test_create_user_session_with_valid_data():
    """Verify session can be created with required fields."""
    session = UserSessionDomain(user_id="student-1", title="Python Basics")
    assert session.user_id == "student-1"
    assert session.title == "Python Basics"
    assert session.id is None


def test_user_id_must_not_be_blank():
    """Verify blank user_id is rejected."""
    with pytest.raises(ValidationError):
        UserSessionDomain(user_id="   ", title="Test")


def test_title_must_not_be_blank():
    """Verify blank title is rejected."""
    with pytest.raises(ValidationError):
        UserSessionDomain(user_id="student-1", title="  ")


def test_user_id_is_stripped():
    """Verify whitespace is stripped from user_id."""
    session = UserSessionDomain(user_id="  student-1  ")
    assert session.user_id == "student-1"


def test_optional_id_field():
    """Verify optional UUID id is accepted."""
    session_id = uuid.uuid4()
    session = UserSessionDomain(id=session_id, user_id="student-1")
    assert session.id == session_id

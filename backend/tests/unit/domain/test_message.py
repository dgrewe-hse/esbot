"""Unit tests for Message domain model."""

import uuid

import pytest
from app.domain.enums import MessageRole
from app.domain.models import MessageDomain
from pydantic import ValidationError

pytestmark = pytest.mark.unit


def test_create_message_with_valid_data():
    """Verify message can be created with required fields."""
    session_id = uuid.uuid4()
    message = MessageDomain(
        session_id=session_id,
        role=MessageRole.USER,
        content="What is recursion?",
    )
    assert message.session_id == session_id
    assert message.role == MessageRole.USER
    assert message.content == "What is recursion?"


def test_content_must_not_be_blank():
    """Verify blank content is rejected."""
    with pytest.raises(ValidationError):
        MessageDomain(
            session_id=uuid.uuid4(),
            role=MessageRole.USER,
            content="   ",
        )


def test_content_max_length():
    """Verify content exceeding max length is rejected."""
    with pytest.raises(ValidationError):
        MessageDomain(
            session_id=uuid.uuid4(),
            role=MessageRole.ASSISTANT,
            content="x" * 4001,
        )


def test_assistant_role():
    """Verify assistant role is accepted."""
    message = MessageDomain(
        session_id=uuid.uuid4(),
        role=MessageRole.ASSISTANT,
        content="Here is an explanation.",
    )
    assert message.role == MessageRole.ASSISTANT

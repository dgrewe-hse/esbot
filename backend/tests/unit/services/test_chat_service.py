"""Unit tests for ChatService with mocked dependencies."""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.core.exceptions import NotFoundError
from app.services.chat_service import ChatService
from app.services.llm.mock import FALLBACK_MESSAGE, MockLLM

pytestmark = pytest.mark.unit


@pytest.fixture
def session_repo():
    """Mock session repository."""
    return MagicMock()


@pytest.fixture
def message_repo():
    """Mock message repository."""
    return MagicMock()


@pytest.fixture
def mock_llm():
    """Mock LLM client."""
    llm = AsyncMock(spec=MockLLM)
    llm.explain.return_value = "Mock explanation"
    return llm


@pytest.fixture
def chat_service(session_repo, message_repo, mock_llm):
    """ChatService with mocked dependencies."""
    return ChatService(session_repo, message_repo, mock_llm)


def test_start_session_calls_repository(session_repo, chat_service):
    """Verify start_session delegates to repository."""
    session_repo.create.return_value = MagicMock()
    chat_service.start_session("student-1", "Test Session")
    session_repo.create.assert_called_once_with(user_id="student-1", title="Test Session")


def test_get_session_raises_not_found(session_repo, chat_service):
    """Verify NotFoundError when session does not exist."""
    session_repo.find_by_id.return_value = None
    with pytest.raises(NotFoundError):
        chat_service.get_session(uuid.uuid4())


@pytest.mark.asyncio
async def test_send_message_stores_user_and_assistant_messages(
    session_repo, message_repo, mock_llm, chat_service
):
    """Verify send_message persists both user and assistant messages."""
    session_id = uuid.uuid4()
    session = MagicMock(id=session_id, title="Python")
    session_repo.find_by_id.return_value = session

    user_msg = MagicMock()
    assistant_msg = MagicMock()
    message_repo.append.side_effect = [user_msg, assistant_msg]

    result = await chat_service.send_message(session_id, "What is a list?")

    assert message_repo.append.call_count == 2
    mock_llm.explain.assert_awaited_once()
    session_repo.update_metadata.assert_called_once_with(session)
    assert result.user_message is user_msg
    assert result.assistant_message is assistant_msg
    assert result.degraded is False


@pytest.mark.asyncio
async def test_send_message_fallback_on_llm_failure(
    session_repo, message_repo, mock_llm, chat_service
):
    """Verify graceful fallback when LLM fails."""
    session_id = uuid.uuid4()
    session = MagicMock(id=session_id, title="Python")
    session_repo.find_by_id.return_value = session
    mock_llm.explain.side_effect = RuntimeError("LLM unavailable")

    user_msg = MagicMock()
    assistant_msg = MagicMock()
    message_repo.append.side_effect = [user_msg, assistant_msg]

    result = await chat_service.send_message(session_id, "Hello")

    assert result.degraded is True
    assistant_call = message_repo.append.call_args_list[1]
    assert assistant_call.args[2] == FALLBACK_MESSAGE


def test_delete_session_raises_not_found(session_repo, chat_service):
    """Verify delete raises NotFoundError when session missing."""
    session_repo.delete.return_value = False
    with pytest.raises(NotFoundError):
        chat_service.delete_session(uuid.uuid4())

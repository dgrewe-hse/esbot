"""Unit tests for QuizService with mocked dependencies."""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.core.exceptions import NotFoundError
from app.services.llm.client import EvaluationDraft, QuizItemDraft
from app.services.quiz_service import QuizService

pytestmark = pytest.mark.unit


@pytest.fixture
def session_repo():
    """Mock session repository."""
    return MagicMock()


@pytest.fixture
def quiz_repo():
    """Mock quiz repository."""
    return MagicMock()


@pytest.fixture
def mock_llm():
    """Mock LLM client."""
    llm = AsyncMock()
    llm.generate_quiz.return_value = [
        QuizItemDraft(
            question="Q1",
            options=["A", "B"],
            correct_answer="A",
        )
    ]
    llm.evaluate_answer.return_value = EvaluationDraft(is_correct=True, feedback="Correct!")
    return llm


@pytest.fixture
def quiz_service(session_repo, quiz_repo, mock_llm):
    """QuizService with mocked dependencies."""
    return QuizService(session_repo, quiz_repo, mock_llm)


@pytest.mark.asyncio
async def test_generate_quiz_persists_items(session_repo, quiz_repo, mock_llm, quiz_service):
    """Verify quiz generation stores request and items."""
    session_id = uuid.uuid4()
    session = MagicMock()
    session_repo.find_by_id.return_value = session

    quiz_request = MagicMock(id=uuid.uuid4())
    quiz_repo.create_quiz_request.return_value = quiz_request
    quiz_repo.add_quiz_items.return_value = [MagicMock()]

    result = await quiz_service.generate_quiz(session_id, "Algorithms", count=1)

    quiz_repo.create_quiz_request.assert_called_once_with(session_id, "Algorithms")
    mock_llm.generate_quiz.assert_awaited_once()
    session_repo.update_metadata.assert_called_once_with(session)
    assert result.degraded is False


@pytest.mark.asyncio
async def test_generate_quiz_fallback_on_llm_failure(
    session_repo, quiz_repo, mock_llm, quiz_service
):
    """Verify fallback quiz items when LLM fails."""
    session_id = uuid.uuid4()
    session_repo.find_by_id.return_value = MagicMock()
    quiz_repo.create_quiz_request.return_value = MagicMock(id=uuid.uuid4())
    quiz_repo.add_quiz_items.return_value = [MagicMock()]
    mock_llm.generate_quiz.side_effect = RuntimeError("LLM down")

    result = await quiz_service.generate_quiz(session_id, "Testing")

    assert result.degraded is True


@pytest.mark.asyncio
async def test_evaluate_answer_not_found(quiz_repo, quiz_service):
    """Verify NotFoundError for unknown quiz item."""
    quiz_repo.find_quiz_item_in_session.return_value = None
    with pytest.raises(NotFoundError):
        await quiz_service.evaluate_answer(uuid.uuid4(), uuid.uuid4(), "A")


@pytest.mark.asyncio
async def test_evaluate_answer_persists_evaluation(session_repo, quiz_repo, mock_llm, quiz_service):
    """Verify answer evaluation is persisted."""
    session_id = uuid.uuid4()
    question_id = uuid.uuid4()

    quiz_item = MagicMock(
        id=question_id,
        question="Q?",
        correct_answer="A",
    )
    quiz_repo.find_quiz_item_in_session.return_value = quiz_item
    submitted = MagicMock(id=uuid.uuid4())
    quiz_repo.submit_answer.return_value = submitted
    evaluation = MagicMock()
    quiz_repo.save_evaluation.return_value = evaluation
    session_repo.find_by_id.return_value = MagicMock()

    result = await quiz_service.evaluate_answer(session_id, question_id, "A")

    quiz_repo.submit_answer.assert_called_once_with(question_id, "A")
    quiz_repo.save_evaluation.assert_called_once()
    assert result.evaluation is evaluation

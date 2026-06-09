"""Unit tests for quiz-related domain models."""

import uuid

import pytest
from app.domain.models import (
    EvaluationResultDomain,
    QuizItemDomain,
    QuizRequestDomain,
    SubmittedAnswerDomain,
)
from pydantic import ValidationError

pytestmark = pytest.mark.unit


def test_create_quiz_request():
    """Verify quiz request can be created."""
    request = QuizRequestDomain(session_id=uuid.uuid4(), topic="Sorting algorithms")
    assert request.topic == "Sorting algorithms"


def test_quiz_request_topic_must_not_be_blank():
    """Verify blank topic is rejected."""
    with pytest.raises(ValidationError):
        QuizRequestDomain(session_id=uuid.uuid4(), topic="  ")


def test_create_quiz_item():
    """Verify quiz item can be created with options."""
    item = QuizItemDomain(
        quiz_request_id=uuid.uuid4(),
        question="What is O(n log n)?",
        options=["Merge sort", "Bubble sort", "Linear search", "Hash lookup"],
        correct_answer="Merge sort",
    )
    assert len(item.options) == 4
    assert item.correct_answer == "Merge sort"


def test_create_submitted_answer():
    """Verify submitted answer can be created."""
    answer = SubmittedAnswerDomain(quiz_item_id=uuid.uuid4(), answer="Merge sort")
    assert answer.answer == "Merge sort"


def test_submitted_answer_must_not_be_blank():
    """Verify blank answer is rejected."""
    with pytest.raises(ValidationError):
        SubmittedAnswerDomain(quiz_item_id=uuid.uuid4(), answer="  ")


def test_create_evaluation_result():
    """Verify evaluation result can be created."""
    result = EvaluationResultDomain(
        submitted_answer_id=uuid.uuid4(),
        is_correct=True,
        feedback="Well done!",
    )
    assert result.is_correct is True
    assert result.feedback == "Well done!"

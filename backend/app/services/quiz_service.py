"""Quiz service for generation and answer evaluation."""

import logging
import uuid
from dataclasses import dataclass

from app.core.config import get_settings
from app.core.exceptions import NotFoundError
from app.db.models import EvaluationResultORM, QuizItemORM, QuizRequestORM, SubmittedAnswerORM
from app.repositories.quiz_repository import QuizRepository
from app.repositories.session_repository import SessionRepository
from app.services.llm.client import LLMClient
from app.services.llm.mock import FALLBACK_MESSAGE

logger = logging.getLogger(__name__)


@dataclass
class QuizGenerationResult:
    """Result of quiz generation."""

    quiz_request: QuizRequestORM
    items: list[QuizItemORM]
    degraded: bool = False


@dataclass
class AnswerEvaluationResult:
    """Result of answer evaluation."""

    submitted_answer: SubmittedAnswerORM
    evaluation: EvaluationResultORM
    degraded: bool = False


class QuizService:
    """Business logic for quiz generation and evaluation."""

    def __init__(
        self,
        session_repo: SessionRepository,
        quiz_repo: QuizRepository,
        llm_client: LLMClient,
    ) -> None:
        self._session_repo = session_repo
        self._quiz_repo = quiz_repo
        self._llm = llm_client

    async def generate_quiz(
        self,
        session_id: uuid.UUID,
        topic: str,
        count: int | None = None,
    ) -> QuizGenerationResult:
        """Generate a quiz for a session topic via the LLM."""
        session = self._session_repo.find_by_id(session_id)
        if session is None:
            raise NotFoundError("Session", str(session_id))

        quiz_count = count or get_settings().quiz_default_count
        quiz_request = self._quiz_repo.create_quiz_request(session_id, topic)

        degraded = False
        try:
            drafts = await self._llm.generate_quiz(topic, quiz_count)
            items_data = [
                {
                    "question": draft.question,
                    "options": draft.options,
                    "correct_answer": draft.correct_answer,
                }
                for draft in drafts
            ]
        except Exception as exc:
            logger.warning("LLM quiz generation failed for session %s: %s", session_id, exc)
            degraded = True
            items_data = [
                {
                    "question": f"Fallback question about {topic}",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A",
                }
            ]

        items = self._quiz_repo.add_quiz_items(quiz_request.id, items_data)
        self._session_repo.update_metadata(session)

        return QuizGenerationResult(
            quiz_request=quiz_request,
            items=items,
            degraded=degraded,
        )

    async def evaluate_answer(
        self,
        session_id: uuid.UUID,
        question_id: uuid.UUID,
        answer: str,
    ) -> AnswerEvaluationResult:
        """Evaluate a user's answer to a quiz question."""
        quiz_item = self._quiz_repo.find_quiz_item_in_session(session_id, question_id)
        if quiz_item is None:
            raise NotFoundError("QuizItem", str(question_id))

        submitted = self._quiz_repo.submit_answer(quiz_item.id, answer)

        degraded = False
        try:
            draft = await self._llm.evaluate_answer(
                quiz_item.question,
                quiz_item.correct_answer,
                answer,
            )
            is_correct = draft.is_correct
            feedback = draft.feedback
        except Exception as exc:
            logger.warning("LLM evaluation failed for question %s: %s", question_id, exc)
            degraded = True
            is_correct = answer.strip().lower() == quiz_item.correct_answer.strip().lower()
            feedback = FALLBACK_MESSAGE if not is_correct else "Correct answer!"

        evaluation = self._quiz_repo.save_evaluation(submitted.id, is_correct, feedback)

        session = self._session_repo.find_by_id(session_id)
        if session:
            self._session_repo.update_metadata(session)

        return AnswerEvaluationResult(
            submitted_answer=submitted,
            evaluation=evaluation,
            degraded=degraded,
        )

"""Repository for quiz-related persistence."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models import EvaluationResultORM, QuizItemORM, QuizRequestORM, SubmittedAnswerORM


class QuizRepository:
    """Data access layer for quizzes and evaluations."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create_quiz_request(self, session_id: uuid.UUID, topic: str) -> QuizRequestORM:
        """Create a quiz request for a session."""
        quiz_request = QuizRequestORM(session_id=session_id, topic=topic.strip())
        self._db.add(quiz_request)
        self._db.commit()
        self._db.refresh(quiz_request)
        return quiz_request

    def add_quiz_items(
        self,
        quiz_request_id: uuid.UUID,
        items: list[dict],
    ) -> list[QuizItemORM]:
        """Persist generated quiz items for a quiz request."""
        orm_items = [
            QuizItemORM(
                quiz_request_id=quiz_request_id,
                question=item["question"],
                options=item.get("options", []),
                correct_answer=item["correct_answer"],
            )
            for item in items
        ]
        self._db.add_all(orm_items)
        self._db.commit()
        for item in orm_items:
            self._db.refresh(item)
        return orm_items

    def find_quiz_item(self, quiz_item_id: uuid.UUID) -> QuizItemORM | None:
        """Find a quiz item by ID."""
        stmt = (
            select(QuizItemORM)
            .options(joinedload(QuizItemORM.quiz_request))
            .where(QuizItemORM.id == quiz_item_id)
        )
        return self._db.scalars(stmt).first()

    def find_quiz_item_in_session(
        self, session_id: uuid.UUID, quiz_item_id: uuid.UUID
    ) -> QuizItemORM | None:
        """Find a quiz item belonging to a specific session."""
        item = self.find_quiz_item(quiz_item_id)
        if item is None:
            return None
        if item.quiz_request.session_id != session_id:
            return None
        return item

    def submit_answer(self, quiz_item_id: uuid.UUID, answer: str) -> SubmittedAnswerORM:
        """Persist a user's submitted answer."""
        submitted = SubmittedAnswerORM(quiz_item_id=quiz_item_id, answer=answer.strip())
        self._db.add(submitted)
        self._db.commit()
        self._db.refresh(submitted)
        return submitted

    def save_evaluation(
        self,
        submitted_answer_id: uuid.UUID,
        is_correct: bool,
        feedback: str,
    ) -> EvaluationResultORM:
        """Persist evaluation feedback for a submitted answer."""
        evaluation = EvaluationResultORM(
            submitted_answer_id=submitted_answer_id,
            is_correct=is_correct,
            feedback=feedback.strip(),
        )
        self._db.add(evaluation)
        self._db.commit()
        self._db.refresh(evaluation)
        return evaluation

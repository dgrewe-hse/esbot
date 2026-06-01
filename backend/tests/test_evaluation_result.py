import pytest
from sqlalchemy.exc import IntegrityError

from app.models.evaluation_result import EvaluationResult
from app.models.submitted_answer import SubmittedAnswer
from app.models.quiz_item import QuizItem
from app.models.quiz_request import QuizRequest
from app.models.user_session import UserSession


def _create_submitted_answer(db_session):
    # builds everything up to a saved SubmittedAnswer
    session = UserSession()
    qr = QuizRequest(topic="Python", difficulty="easy")
    session.add_quiz_request(qr)
    item = QuizItem(question="Question?", correct_answer="Answer")
    qr.add_quiz_item(item)
    answer = SubmittedAnswer(answer="My answer")
    item.add_submitted_answer(answer)
    db_session.add(session)
    db_session.flush()
    return answer


class TestEvaluationResultCreation:

    def test_create_with_valid_data(self):
        ev = EvaluationResult(is_correct=True, feedback="Correct!")
        assert ev.is_correct is True
        assert ev.feedback == "Correct!"
        assert ev.id is None

    def test_create_with_false_result(self):
        ev = EvaluationResult(is_correct=False, feedback="Unfortunately wrong.")
        assert ev.is_correct is False

    def test_feedback_can_be_none(self, db_session):
        answer = _create_submitted_answer(db_session)
        ev = EvaluationResult(is_correct=True, feedback=None)
        answer.set_evaluation(ev)
        db_session.add(ev)
        db_session.flush()
        assert ev.feedback is None
        assert ev.id is not None

    def test_id_assigned_after_flush(self, db_session):
        answer = _create_submitted_answer(db_session)
        ev = EvaluationResult(is_correct=True, feedback="Correct")
        answer.set_evaluation(ev)
        db_session.add(ev)
        db_session.flush()
        assert ev.id is not None
        assert isinstance(ev.id, int)


class TestEvaluationResultValidation:

    def test_null_is_correct_raises(self, db_session):
        answer = _create_submitted_answer(db_session)
        ev = EvaluationResult(is_correct=None, feedback="text")
        answer.set_evaluation(ev)
        db_session.add(ev)
        with pytest.raises(IntegrityError):
            db_session.flush()

    def test_null_submitted_answer_id_raises(self, db_session):
        ev = EvaluationResult(is_correct=True, feedback="Correct")
        db_session.add(ev)
        with pytest.raises(IntegrityError):
            db_session.flush()


class TestEvaluationResultRelationship:
    """1:1 relationship with SubmittedAnswer"""

    def test_submitted_answer_backref(self, db_session):
        answer = _create_submitted_answer(db_session)
        ev = EvaluationResult(is_correct=True, feedback="Correct")
        answer.set_evaluation(ev)
        db_session.add(ev)
        db_session.flush()

        assert ev.submitted_answer is answer
        assert ev.submitted_answer_id == answer.id

    def test_evaluation_appears_on_answer(self, db_session):
        answer = _create_submitted_answer(db_session)
        ev = EvaluationResult(is_correct=True, feedback="Correct")
        answer.set_evaluation(ev)
        db_session.add(ev)
        db_session.flush()

        assert answer.evaluation_result is ev

    def test_one_to_one_unique_constraint(self, db_session):
        answer = _create_submitted_answer(db_session)
        ev1 = EvaluationResult(is_correct=True, feedback="First evaluation")
        answer.set_evaluation(ev1)
        db_session.add(ev1)
        db_session.flush()

        ev2 = EvaluationResult(
            is_correct=False,
            feedback="Second evaluation",
            submitted_answer_id=answer.id,
        )
        db_session.add(ev2)
        with pytest.raises(IntegrityError):
            db_session.flush()


class TestEvaluationResultHelpers:

    def test_set_submitted_answer_links_both_sides(self):
        answer = SubmittedAnswer(answer="My answer")
        ev = EvaluationResult(is_correct=True, feedback="Correct!")
        ev.set_submitted_answer(answer)
        assert ev.submitted_answer is answer
        assert answer.evaluation_result is ev

class TestEvaluationResultBoundaryValues:
    # boundary values for is_correct and feedback
    # is_correct is NOT NULL so None fails, but True/False both work fine
    # feedback is nullable, and empty string is also accepted (different from NULL)

    def test_empty_feedback_string_accepted(self, db_session):
        answer = _create_submitted_answer(db_session)
        ev = EvaluationResult(is_correct=True, feedback="")
        answer.set_evaluation(ev)
        db_session.add(ev)
        db_session.flush()
        assert ev.feedback == ""

    def test_very_long_feedback_accepted(self, db_session):
        answer = _create_submitted_answer(db_session)
        long_feedback = "X" * 5_000
        ev = EvaluationResult(is_correct=False, feedback=long_feedback)
        answer.set_evaluation(ev)
        db_session.add(ev)
        db_session.flush()
        assert len(ev.feedback) == 5_000
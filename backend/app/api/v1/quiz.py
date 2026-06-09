"""Quiz REST endpoints."""

import uuid

from fastapi import APIRouter, Depends, status

from app.api.deps import get_quiz_service
from app.api.schemas.quiz import (
    AnswerSubmitRequest,
    EvaluationResponse,
    QuizCreateRequest,
    QuizGenerationResponse,
    QuizItemResponse,
)
from app.services.quiz_service import QuizService

router = APIRouter()


@router.post(
    "/{session_id}/quiz",
    response_model=QuizGenerationResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_quiz(
    session_id: uuid.UUID,
    body: QuizCreateRequest,
    quiz_service: QuizService = Depends(get_quiz_service),
) -> QuizGenerationResponse:
    """Generate practice questions for a topic within a session."""
    result = await quiz_service.generate_quiz(session_id, body.topic, body.count)
    return QuizGenerationResponse(
        quiz_request_id=result.quiz_request.id,
        topic=result.quiz_request.topic,
        items=[QuizItemResponse.model_validate(item) for item in result.items],
        degraded=result.degraded,
    )


@router.post(
    "/{session_id}/quiz/{question_id}/answer",
    response_model=EvaluationResponse,
)
async def submit_answer(
    session_id: uuid.UUID,
    question_id: uuid.UUID,
    body: AnswerSubmitRequest,
    quiz_service: QuizService = Depends(get_quiz_service),
) -> EvaluationResponse:
    """Submit an answer to a quiz question and receive feedback."""
    result = await quiz_service.evaluate_answer(session_id, question_id, body.answer)
    return EvaluationResponse(
        submitted_answer_id=result.submitted_answer.id,
        quiz_item_id=result.submitted_answer.quiz_item_id,
        answer=result.submitted_answer.answer,
        is_correct=result.evaluation.is_correct,
        feedback=result.evaluation.feedback,
        submitted_at=result.submitted_answer.submitted_at,
        degraded=result.degraded,
    )

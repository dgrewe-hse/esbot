"""LLM client protocol and data transfer objects."""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class QuizItemDraft:
    """Draft quiz item returned by the LLM."""

    question: str
    options: list[str]
    correct_answer: str


@dataclass
class EvaluationDraft:
    """Draft evaluation result returned by the LLM."""

    is_correct: bool
    feedback: str


class LLMClient(Protocol):
    """Protocol for AI inference services (mockable in tests)."""

    async def explain(self, topic: str, user_message: str) -> str:
        """Generate an educational explanation for a user message."""
        ...

    async def generate_quiz(self, topic: str, count: int) -> list[QuizItemDraft]:
        """Generate practice quiz questions for a topic."""
        ...

    async def evaluate_answer(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
    ) -> EvaluationDraft:
        """Evaluate a user's answer to a quiz question."""
        ...

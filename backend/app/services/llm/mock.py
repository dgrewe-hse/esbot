"""Deterministic mock LLM for tests and CI."""

from app.services.llm.client import EvaluationDraft, LLMClient, QuizItemDraft

FALLBACK_MESSAGE = (
    "I am temporarily unable to generate a response. "
    "Please try again in a moment or rephrase your question."
)


class MockLLM:
    """Mock LLM that returns predictable, deterministic responses."""

    async def explain(self, topic: str, user_message: str) -> str:
        """Return a canned explanation."""
        return (
            f"Here is a structured explanation about '{topic}': "
            f"Your question was '{user_message}'. "
            "This is a mock response for testing purposes."
        )

    async def generate_quiz(self, topic: str, count: int) -> list[QuizItemDraft]:
        """Return canned quiz items."""
        items: list[QuizItemDraft] = []
        for index in range(count):
            items.append(
                QuizItemDraft(
                    question=f"What is a key concept of {topic}? (Q{index + 1})",
                    options=["Option A", "Option B", "Option C", "Option D"],
                    correct_answer="Option A",
                )
            )
        return items

    async def evaluate_answer(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
    ) -> EvaluationDraft:
        """Evaluate answer by simple string comparison."""
        is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
        if is_correct:
            feedback = f"Correct! '{user_answer}' matches the expected answer."
        else:
            feedback = (
                f"Not quite. The correct answer was '{correct_answer}'. "
                f"Your answer was '{user_answer}'."
            )
        return EvaluationDraft(is_correct=is_correct, feedback=feedback)


def satisfies_llm_client(client: MockLLM) -> LLMClient:
    """Type-narrowing helper for MockLLM as LLMClient."""
    return client

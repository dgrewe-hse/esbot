"""LiteLLM adapter for Ollama and other compatible inference backends."""

import json
import logging

import litellm

from app.core.config import Settings
from app.services.llm.client import EvaluationDraft, QuizItemDraft

logger = logging.getLogger(__name__)


class LiteLLMAdapter:
    """LLM client implementation using LiteLLM."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._model = settings.ollama_model
        self._api_base = settings.ollama_base_url

    async def _completion(self, prompt: str) -> str:
        """Execute a completion request via LiteLLM."""
        response = await litellm.acompletion(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            api_base=self._api_base,
        )
        content = response.choices[0].message.content
        return content or ""

    async def explain(self, topic: str, user_message: str) -> str:
        """Generate an educational explanation."""
        prompt = (
            f"You are ESBot, an educational assistant. "
            f"Topic: {topic}\n"
            f"Student question: {user_message}\n"
            f"Provide a clear, structured explanation suitable for a student."
        )
        return await self._completion(prompt)

    async def generate_quiz(self, topic: str, count: int) -> list[QuizItemDraft]:
        """Generate quiz questions as structured JSON."""
        prompt = (
            f"Generate exactly {count} multiple-choice quiz questions about '{topic}'. "
            "Return ONLY a JSON array with objects containing keys: "
            "question, options (array of 4 strings), correct_answer. "
            "No markdown, no extra text."
        )
        raw = await self._completion(prompt)
        try:
            data = json.loads(raw)
            return [
                QuizItemDraft(
                    question=item["question"],
                    options=item.get("options", []),
                    correct_answer=item["correct_answer"],
                )
                for item in data
            ]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logger.warning("Failed to parse quiz JSON from LLM: %s", exc)
            return await MockLiteLLMFallback().generate_quiz(topic, count)

    async def evaluate_answer(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
    ) -> EvaluationDraft:
        """Evaluate a student's answer."""
        prompt = (
            f"Evaluate this student answer.\n"
            f"Question: {question}\n"
            f"Correct answer: {correct_answer}\n"
            f"Student answer: {user_answer}\n"
            "Return ONLY JSON with keys: is_correct (boolean), feedback (string)."
        )
        raw = await self._completion(prompt)
        try:
            data = json.loads(raw)
            return EvaluationDraft(
                is_correct=bool(data["is_correct"]),
                feedback=str(data["feedback"]),
            )
        except (json.JSONDecodeError, KeyError, TypeError):
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            feedback = "Correct!" if is_correct else f"The expected answer was: {correct_answer}"
            return EvaluationDraft(is_correct=is_correct, feedback=feedback)


class MockLiteLLMFallback:
    """Internal fallback when LiteLLM response parsing fails."""

    async def generate_quiz(self, topic: str, count: int) -> list[QuizItemDraft]:
        """Return minimal quiz items."""
        return [
            QuizItemDraft(
                question=f"What is important about {topic}?",
                options=["A", "B", "C", "D"],
                correct_answer="A",
            )
            for _ in range(count)
        ]

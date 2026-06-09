"""Factory for creating LLM client implementations."""

from app.core.config import Settings, get_settings
from app.services.llm.client import LLMClient
from app.services.llm.litellm_adapter import LiteLLMAdapter
from app.services.llm.mock import MockLLM


def create_llm_client(settings: Settings | None = None) -> LLMClient:
    """Create an LLM client based on configuration."""
    config = settings or get_settings()
    if config.llm_provider == "mock":
        return MockLLM()
    return LiteLLMAdapter(config)

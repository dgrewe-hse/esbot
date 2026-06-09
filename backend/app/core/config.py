"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the ESBot backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "ESBot API"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://esbot_user:esbot_password@localhost:5432/esbot"

    llm_provider: Literal["mock", "ollama", "litellm"] = "mock"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "ollama/llama3.2"

    message_max_length: int = 4000
    quiz_default_count: int = 3


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


# Konfiguration wird aus .env oder Umgebungsvariablen geladen
class Settings(BaseSettings):
    database_url: str = "postgresql://esbot_user:esbot_password@localhost:5432/esbot"
    app_env: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        case_sensitive=False,
    )


settings = Settings()

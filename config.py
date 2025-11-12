"""Configuration management for Miro to Graph converter."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    miro_access_token: str
    miro_board_id: str
    miro_api_base_url: str = "https://api.miro.com/v2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()

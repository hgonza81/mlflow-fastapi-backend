"""Configuration settings for the FastAPI application.

This module defines the application configuration using Pydantic Settings
to load values from environment variables and .env files.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfigSettings(BaseSettings):
    """Base configuration class with common settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

class APPConfig(BaseConfigSettings):
    """Application configuration settings."""

    env: str | None = None
    debug: bool = False
    model_config = {**BaseConfigSettings.model_config, "env_prefix": "APP_"}

class APIConfig(BaseConfigSettings):
    """API server configuration settings."""

    host: str = "localhost"
    port: int = 8001
    model_config = {**BaseConfigSettings.model_config, "env_prefix": "API_"}

class Settings:  # pylint: disable=too-few-public-methods
    """Main settings container for the application."""

    def __init__(self):
        """Initialize settings by loading configuration from environment."""
        self.app = APPConfig()
        self.api = APIConfig()

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

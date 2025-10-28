from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class BaseConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="backend/.env",
        case_sensitive=False,
        extra="ignore",
    )

class APPConfig(BaseConfigSettings):
    env: str | None = None
    debug: bool = False
    model_config = {**BaseConfigSettings.model_config, "env_prefix": "APP_"}

class APIConfig(BaseConfigSettings):
    key: str | None = None
    url: str | None = None
    host: str = "localhost"
    port: int = 8000
    model_config = {**BaseConfigSettings.model_config, "env_prefix": "API_"}

class Settings:
    def __init__(self):
        self.app = APPConfig()
        self.api = APIConfig()

@lru_cache()
def get_settings() -> Settings:
    return Settings()

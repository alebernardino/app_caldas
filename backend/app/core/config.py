from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "APP Caldas API"
    app_env: str = "dev"
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://app_caldas:app_caldas@db:5432/app_caldas"
    cors_origins: list[str] = ["http://localhost:3000"]

    secret_key: str = "change_me_super_secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    rate_limit_auth: str = "10/minute"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

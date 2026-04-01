from __future__ import annotations

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Frequencia Koinonia API"
    app_env: str = "development"
    api_prefix: str = ""

    database_url: str = "postgresql+psycopg2://koinonia:koinonia@db:5432/koinonia"
    cors_origins: List[str] = ["*"]
    upload_dir: str = "/app/uploads"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return ["*"]
            if raw.startswith("[") and raw.endswith("]"):
                raw = raw.strip("[]")
            return [item.strip().strip('"').strip("'") for item in raw.split(",") if item.strip()]
        return ["*"]


settings = Settings()


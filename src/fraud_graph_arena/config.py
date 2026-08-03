from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class RuntimeRole(StrEnum):
    WEB = "WEB"
    MAINTENANCE = "MAINTENANCE"
    EVALUATOR = "EVALUATOR"
    MIGRATE = "MIGRATE"


class Settings(BaseSettings):
    """Typed operational configuration.

    Gameplay rules deliberately do not live here. Settings choose runtime wiring and
    environment-specific adapters; they do not redefine case or round semantics.
    """

    model_config = SettingsConfigDict(
        env_prefix="FGA_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="forbid",
    )

    app_name: str = "Fraud Graph Arena"
    environment: Literal["development", "test", "production"] = "development"
    runtime_role: RuntimeRole = RuntimeRole.WEB
    api_prefix: str = "/api/v1"
    build_version: str = "0.1.0"
    contract_version: str = "v1"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    round_repository: Literal["memory", "sqlite"] = "sqlite"
    sqlite_path: Path = Path(".fga/fga.sqlite3")
    frontend_dist: Path = Path("apps/web/dist")

    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    @model_validator(mode="after")
    def validate_production_safety(self) -> "Settings":
        if self.environment == "production":
            if self.round_repository == "memory":
                raise ValueError("production requires a durable round repository")
            if "*" in self.allowed_origins:
                raise ValueError("production CORS origins must be explicit")
        if not self.api_prefix.startswith("/"):
            raise ValueError("api_prefix must begin with '/'")
        return self

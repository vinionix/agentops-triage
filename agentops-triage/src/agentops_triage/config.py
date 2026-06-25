"""Application settings."""

from __future__ import annotations

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


LLMProvider = Literal["mock", "openai", "anthropic", "google"]


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_name: str = "AgentOps Triage"
    environment: str = "local"
    llm_provider: LLMProvider = "mock"
    model_name: str = "mock"
    temperature: float = 0.1

    model_config = SettingsConfigDict(
        env_prefix="AGENTOPS_",
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

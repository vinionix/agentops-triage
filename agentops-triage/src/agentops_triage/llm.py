"""Optional LangChain integration layer.

The MVP works in deterministic demo mode by default. This module isolates model
provider code so the triage workflow does not depend directly on one vendor.
"""

from __future__ import annotations

from dataclasses import dataclass

from agentops_triage.config import Settings


@dataclass(slots=True)
class LLMRouter:
    """Thin adapter around LangChain chat models."""

    settings: Settings

    def is_enabled(self) -> bool:
        return self.settings.llm_provider != "mock"

    def invoke_text(self, system_prompt: str, user_prompt: str) -> str:
        """Invoke a chat model through LangChain when configured.

        The method is intentionally small because this project keeps a safe
        deterministic path for demos and tests.
        """

        if not self.is_enabled():
            return ""

        try:
            from langchain.chat_models import init_chat_model
        except Exception as exc:  # pragma: no cover - optional dependency path.
            raise RuntimeError(
                "LangChain provider packages are not available in this environment."
            ) from exc

        model = init_chat_model(
            self.settings.model_name,
            temperature=self.settings.temperature,
        )
        result = model.invoke(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
        return getattr(result, "content", str(result))

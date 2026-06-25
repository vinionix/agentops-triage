"""Experimental Agno adapter.

This module is optional. The main MVP uses LangGraph as the workflow engine and
keeps Agno as an extension point for comparing agent frameworks.
"""

from __future__ import annotations

import os


def build_agno_triage_agent():
    """Build an Agno agent for exploratory usage."""

    try:
        from agno.agent import Agent
    except Exception as exc:  # pragma: no cover - optional dependency path.
        raise RuntimeError("Install the Agno optional dependency first.") from exc

    return Agent(
        name="AgentOps Technical Triage",
        model=os.getenv("AGENTOPS_MODEL_NAME", "openai:gpt-5.5"),
        instructions=(
            "Classify technical support tickets, estimate priority, suggest "
            "safe diagnostic steps and write a concise customer response. "
            "Do not claim certainty when evidence is incomplete."
        ),
        markdown=True,
    )

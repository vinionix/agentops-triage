"""FastAPI application for AgentOps Triage."""

from __future__ import annotations

from fastapi import FastAPI

from agentops_triage.config import settings
from agentops_triage.graph import run_triage
from agentops_triage.schemas import TicketInput, TriageReport


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "AI-oriented technical support triage API using Pydantic, "
        "LangGraph and optional LLM providers."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}


@app.post("/triage", response_model=TriageReport)
def triage(ticket: TicketInput) -> TriageReport:
    return run_triage(ticket)

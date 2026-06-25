"""Pydantic schemas used by the triage workflow."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


ImpactLevel = Literal["low", "medium", "high", "critical"]
TicketChannel = Literal["email", "phone", "chat", "portal", "internal"]
TriageCategory = Literal[
    "network",
    "dns",
    "nat",
    "streaming",
    "auth",
    "hardware",
    "unknown",
]
PriorityLevel = Literal["low", "medium", "high", "critical"]


class TicketInput(BaseModel):
    """Raw ticket sent to the triage workflow."""

    title: str = Field(..., min_length=5, max_length=160)
    description: str = Field(..., min_length=15, max_length=4000)
    channel: TicketChannel = "portal"
    customer_impact: ImpactLevel = "medium"
    service_tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("title", "description")
    @classmethod
    def strip_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("field cannot be empty")
        return cleaned


class AgentTraceItem(BaseModel):
    """Small audit trail entry for explaining agent decisions."""

    agent: str
    action: str
    summary: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class ClassificationResult(BaseModel):
    category: TriageCategory
    signals: list[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)


class PriorityResult(BaseModel):
    priority: PriorityLevel
    reason: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class DiagnosticSuggestion(BaseModel):
    likely_cause: str
    next_steps: list[str]
    escalation_needed: bool = False


class FinalResponse(BaseModel):
    internal_summary: str
    customer_message: str


class TriageReport(BaseModel):
    ticket: TicketInput
    classification: ClassificationResult
    priority: PriorityResult
    diagnostic: DiagnosticSuggestion
    final_response: FinalResponse
    trace: list[AgentTraceItem] = Field(default_factory=list)

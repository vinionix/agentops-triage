"""LangGraph workflow for AgentOps Triage."""

from __future__ import annotations

from typing import TypedDict

from agentops_triage.rules import (
    build_final_response,
    classify_ticket,
    prioritize_ticket,
    suggest_diagnostic,
)
from agentops_triage.schemas import (
    AgentTraceItem,
    ClassificationResult,
    DiagnosticSuggestion,
    FinalResponse,
    PriorityResult,
    TicketInput,
    TriageReport,
)

try:  # Optional at import time to keep demo mode friendly.
    from langgraph.graph import END, START, StateGraph
except Exception:  # pragma: no cover - used when dependency is absent.
    END = START = StateGraph = None  # type: ignore[assignment]


class TriageState(TypedDict, total=False):
    ticket: TicketInput
    classification: ClassificationResult
    priority: PriorityResult
    diagnostic: DiagnosticSuggestion
    final_response: FinalResponse
    trace: list[AgentTraceItem]


def _append_trace(
    state: TriageState,
    agent: str,
    action: str,
    summary: str,
    confidence: float,
) -> list[AgentTraceItem]:
    trace = list(state.get("trace", []))
    trace.append(
        AgentTraceItem(
            agent=agent,
            action=action,
            summary=summary,
            confidence=confidence,
        )
    )
    return trace


def classifier_agent(state: TriageState) -> TriageState:
    ticket = state["ticket"]
    classification = classify_ticket(ticket)
    state["classification"] = classification
    state["trace"] = _append_trace(
        state,
        "classifier_agent",
        "classify_ticket",
        f"Categoria definida como {classification.category}.",
        classification.confidence,
    )
    return state


def priority_agent(state: TriageState) -> TriageState:
    ticket = state["ticket"]
    classification = state["classification"]
    priority = prioritize_ticket(ticket, classification)
    state["priority"] = priority
    state["trace"] = _append_trace(
        state,
        "priority_agent",
        "prioritize_ticket",
        f"Prioridade definida como {priority.priority}.",
        priority.confidence,
    )
    return state


def diagnostic_agent(state: TriageState) -> TriageState:
    ticket = state["ticket"]
    classification = state["classification"]
    priority = state["priority"]
    diagnostic = suggest_diagnostic(ticket, classification, priority)
    state["diagnostic"] = diagnostic
    state["trace"] = _append_trace(
        state,
        "diagnostic_agent",
        "suggest_diagnostic",
        diagnostic.likely_cause,
        0.78,
    )
    return state


def response_agent(state: TriageState) -> TriageState:
    ticket = state["ticket"]
    classification = state["classification"]
    priority = state["priority"]
    diagnostic = state["diagnostic"]
    response = build_final_response(ticket, classification, priority, diagnostic)
    state["final_response"] = response
    state["trace"] = _append_trace(
        state,
        "response_agent",
        "build_customer_response",
        "Resposta final gerada para atendimento.",
        0.8,
    )
    return state


def build_graph():
    """Build and compile the LangGraph state machine."""

    if StateGraph is None:
        raise RuntimeError("LangGraph is not installed. Use sequential fallback.")

    graph = StateGraph(TriageState)
    graph.add_node("classifier", classifier_agent)
    graph.add_node("priority", priority_agent)
    graph.add_node("diagnostic", diagnostic_agent)
    graph.add_node("response", response_agent)

    graph.add_edge(START, "classifier")
    graph.add_edge("classifier", "priority")
    graph.add_edge("priority", "diagnostic")
    graph.add_edge("diagnostic", "response")
    graph.add_edge("response", END)

    return graph.compile()


def run_sequential(ticket: TicketInput) -> TriageState:
    """Run the same workflow without LangGraph."""

    state: TriageState = {"ticket": ticket, "trace": []}
    state = classifier_agent(state)
    state = priority_agent(state)
    state = diagnostic_agent(state)
    state = response_agent(state)
    return state


def run_triage(ticket: TicketInput, use_langgraph: bool = True) -> TriageReport:
    """Run triage and return a validated report."""

    if use_langgraph and StateGraph is not None:
        state = build_graph().invoke({"ticket": ticket, "trace": []})
    else:
        state = run_sequential(ticket)

    return TriageReport(
        ticket=state["ticket"],
        classification=state["classification"],
        priority=state["priority"],
        diagnostic=state["diagnostic"],
        final_response=state["final_response"],
        trace=state.get("trace", []),
    )

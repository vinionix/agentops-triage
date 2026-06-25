"""Command line interface for AgentOps Triage."""

from __future__ import annotations

import argparse
from pathlib import Path

from agentops_triage.graph import run_triage
from agentops_triage.schemas import TicketInput


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run technical ticket triage.")
    parser.add_argument(
        "ticket_file",
        type=Path,
        help="Path to a JSON file containing a support ticket.",
    )
    parser.add_argument(
        "--no-langgraph",
        action="store_true",
        help="Run the sequential fallback instead of LangGraph.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw = args.ticket_file.read_text(encoding="utf-8")
    ticket = TicketInput.model_validate_json(raw)
    report = run_triage(ticket, use_langgraph=not args.no_langgraph)
    print(report.model_dump_json(indent=2))


if __name__ == "__main__":
    main()

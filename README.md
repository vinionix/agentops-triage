# AgentOps Triage

Technical support triage project built with Python, Pydantic, LangGraph, LangChain, Agno, FastAPI and Docker.

The project receives a support ticket and returns a structured triage report with category, priority, diagnostic steps and a customer-facing response.

## Flow

```text
TicketInput
  -> Classifier Agent
  -> Priority Agent
  -> Diagnostic Agent
  -> Response Agent
  -> TriageReport
```

## Stack

- Python
- FastAPI
- Pydantic
- LangGraph
- LangChain
- Agno
- Docker
- pytest

## Local install

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run CLI demo

```bash
python -m agentops_triage examples/sample_ticket.json --no-langgraph
```

## Run API

```bash
uvicorn agentops_triage.main:app --reload
```

## Docker

```bash
docker compose up --build
```

## Main idea

The project separates the triage into small responsibilities. One step classifies the incident, another step estimates priority, another suggests diagnostic actions and the final step prepares the response.

Pydantic validates the input and output contracts. LangGraph organizes the workflow. LangChain and Agno are kept as integration layers so the project can evolve without coupling every file to one framework.

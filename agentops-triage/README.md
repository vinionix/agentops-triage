# AgentOps Triage

AI-oriented technical support triage platform using **Python**, **Pydantic**,
**LangGraph**, **LangChain**, **Agno**, **FastAPI** and optional LLM providers.

The project simulates a first-level support triage workflow: it receives a
technical ticket, classifies the incident, estimates priority, suggests
diagnostic steps and generates a structured response.

## Why this project exists

Support teams deal with repeated incidents: network instability, DNS issues,
NAT problems, streaming access errors, hardware failures and vague customer
reports. This project shows how an agent workflow can organize the first
analysis before a human technician takes over.

## Core workflow

```text
TicketInput
    ↓
Classifier Agent
    ↓
Priority Agent
    ↓
Diagnostic Agent
    ↓
Response Agent
    ↓
TriageReport
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

## Current MVP behavior

The MVP works in **demo mode** by default. That means it can run locally without
external model configuration. The deterministic path is intentional: it makes the
project easy to test, present and explain.

The project also includes an isolated LangChain integration layer and an Agno
adapter so the architecture is ready for real model providers without coupling
the whole application to one vendor.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run the CLI demo

```bash
python -m agentops_triage examples/sample_ticket.json --no-langgraph
```

## Run the API

```bash
uvicorn agentops_triage.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

## Docker

```bash
docker compose up --build
```

## Example API payload

```json
{
  "title": "Cliente com lentidão e perda de pacotes",
  "description": "Cliente relata internet lenta, ping alto e perda de pacotes ao acessar serviços externos.",
  "channel": "portal",
  "customer_impact": "high",
  "service_tags": ["internet", "rede", "latencia"]
}
```

## Main modules

```text
src/agentops_triage/
├── schemas.py        # Pydantic contracts
├── rules.py          # deterministic demo triage rules
├── graph.py          # LangGraph workflow
├── llm.py            # optional LangChain integration layer
├── agno_adapter.py   # optional Agno experiment
├── main.py           # FastAPI app
└── cli.py            # command line demo
```

## How to explain it in an interview

> I built a technical support triage workflow using specialized agents. The
> classifier identifies the incident category, the priority agent estimates
> urgency, the diagnostic agent suggests first checks, and the response agent
> generates a structured answer. LangGraph controls the flow, Pydantic validates
> inputs and outputs, and LangChain/Agno are isolated as integration layers.

## Roadmap

- Add real provider execution using LangChain.
- Add structured output parsing from LLM responses.
- Add ticket history storage.
- Add web UI for triage review.
- Add observability and evaluation datasets.

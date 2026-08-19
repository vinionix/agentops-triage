# Technical Overview — AgentOps Triage

## 1. Purpose

AgentOps Triage is an AI-oriented technical support triage MVP. It models the decision flow that happens when an incident arrives at a support or NOC operation: classify the issue, estimate priority, suggest an initial diagnosis and generate a structured response.

The repository is intentionally organized as a multi-step workflow so each responsibility can be inspected and evolved independently.

## 2. Processing flow

```text
Incoming ticket
      ↓
Classifier
      ↓
Priority analysis
      ↓
Diagnostic stage
      ↓
Response generation
      ↓
Structured triage report
```

The stages are designed to communicate through explicit data models instead of passing unstructured text through one large function.

## 3. Main technologies

- Python
- FastAPI
- Pydantic
- LangGraph
- LangChain
- Agno as an alternative agent experiment
- Docker

## 4. Why a staged architecture

A single prompt can generate a plausible support answer, but it makes behavior harder to inspect. Breaking the task into stages creates several engineering advantages:

- each stage has a narrow responsibility;
- intermediate outputs can be validated;
- failures are easier to locate;
- the workflow can be tested without requiring every component to be intelligent;
- model integrations can be replaced without rewriting the entire API;
- traces can expose how the final answer was produced.

## 5. Data contracts

Pydantic is used to make the input/output shape explicit. The API receives a structured ticket and produces fields such as classification, priority, diagnostic guidance, final response and trace information.

This is important for AI systems because downstream software should not depend on loosely formatted model prose when a typed contract is possible.

## 6. Current AI boundary

The first version of the project prioritizes workflow architecture and code organization. LangChain/LangGraph provide the integration boundary for language models, but the repository should not be interpreted as if every stage already depends on a production LLM.

That distinction is intentional: deterministic or mocked behavior can validate orchestration and data flow before adding model cost, latency and non-determinism.

## 7. API surface

The project exposes a health endpoint and a triage endpoint through FastAPI. FastAPI also provides interactive OpenAPI documentation under `/docs`, making the project easy to exercise manually.

A CLI path is also useful for validating the flow without a browser or HTTP client.

## 8. Evolution path

Useful next stages include:

1. integrate one real local or hosted LLM behind an adapter;
2. define evaluation cases for classification and priority;
3. compare deterministic vs model-driven stages;
4. add retrieval from a technical knowledge base;
5. add confidence/abstention behavior;
6. record latency, token usage and model metadata;
7. add observability for each workflow node;
8. test prompt-injection and malicious-ticket inputs;
9. add human approval for high-risk actions or responses.

## 9. Testing strategy

The architecture supports several layers of testing:

- schema validation tests;
- unit tests for deterministic business rules;
- workflow transition tests;
- API contract tests;
- golden test cases for model outputs;
- end-to-end tests with a real model when enabled.

AI behavior should be evaluated with explicit cases rather than accepted because an example output 'looks good'.

## 10. Portfolio value

AgentOps Triage demonstrates the bridge between previous networking/support experience and AI engineering:

- domain modelling from real operational workflows;
- APIs and typed data contracts;
- agent/workflow orchestration;
- separation of deterministic logic from model integration;
- traceability and evaluation-oriented design;
- an incremental path from MVP architecture to production-style LLM integration.

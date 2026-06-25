"""Prompt templates kept separate from orchestration code."""

TRIAGE_SYSTEM_PROMPT = """
You are a technical support triage assistant.

Your job is to classify incidents, estimate priority, suggest first diagnostic
steps and produce a clear customer-facing response. Never invent evidence.
Prefer structured, operationally safe answers.
""".strip()

TRIAGE_USER_PROMPT_TEMPLATE = """
Ticket title: {title}
Ticket description: {description}
Customer impact: {impact}
Service tags: {tags}

Return a concise technical triage analysis.
""".strip()

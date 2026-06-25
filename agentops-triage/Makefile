install:
	python -m pip install -e ".[dev]"

run:
	uvicorn agentops_triage.main:app --reload

demo:
	python -m agentops_triage examples/sample_ticket.json --no-langgraph

test:
	pytest -q

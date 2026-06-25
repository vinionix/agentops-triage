from agentops_triage.graph import run_triage
from agentops_triage.schemas import TicketInput


def test_triage_network_ticket_without_langgraph():
    ticket = TicketInput(
        title="Cliente com lentidão",
        description="Cliente relata lentidão, ping alto e perda de pacotes.",
        customer_impact="high",
        service_tags=["internet", "rede"],
    )

    report = run_triage(ticket, use_langgraph=False)

    assert report.classification.category == "network"
    assert report.priority.priority == "high"
    assert report.diagnostic.next_steps
    assert report.trace

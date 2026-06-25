from agentops_triage.schemas import TicketInput


def test_ticket_input_strips_text():
    ticket = TicketInput(
        title="  Cliente com lentidão  ",
        description="  Cliente relata lentidão e perda de pacotes na rede.  ",
    )

    assert ticket.title == "Cliente com lentidão"
    assert "perda de pacotes" in ticket.description

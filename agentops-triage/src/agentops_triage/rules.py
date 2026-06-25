"""Deterministic triage rules used by demo mode and tests."""

from __future__ import annotations

from agentops_triage.schemas import (
    ClassificationResult,
    DiagnosticSuggestion,
    FinalResponse,
    PriorityResult,
    TicketInput,
)


CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "dns": ["dns", "dominio", "domínio", "resolve", "resolucao", "resolução"],
    "nat": ["nat", "cgnat", "porta", "port forwarding", "duplo nat"],
    "streaming": ["netflix", "youtube", "prime video", "streaming", "erro e106"],
    "auth": ["login", "senha", "autenticacao", "autenticação", "credencial"],
    "hardware": ["roteador", "onu", "cpe", "cabo", "porta lan", "equipamento"],
    "network": [
        "internet",
        "lentidao",
        "lentidão",
        "latencia",
        "latência",
        "perda",
        "pacote",
        "ping",
        "traceroute",
        "sem conexao",
        "sem conexão",
    ],
}


def normalize_text(ticket: TicketInput) -> str:
    tags = " ".join(ticket.service_tags)
    return f"{ticket.title} {ticket.description} {tags}".lower()


def classify_ticket(ticket: TicketInput) -> ClassificationResult:
    text = normalize_text(ticket)
    scores: dict[str, int] = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        scores[category] = sum(1 for keyword in keywords if keyword in text)

    best_category, best_score = max(scores.items(), key=lambda item: item[1])

    if best_score == 0:
        return ClassificationResult(
            category="unknown",
            signals=["nenhum padrão forte identificado"],
            confidence=0.35,
        )

    signals = [
        keyword
        for keyword in CATEGORY_KEYWORDS[best_category]
        if keyword in text
    ]

    confidence = min(0.95, 0.55 + (best_score * 0.1))
    return ClassificationResult(
        category=best_category, signals=signals, confidence=confidence
    )


def prioritize_ticket(
    ticket: TicketInput, classification: ClassificationResult
) -> PriorityResult:
    text = normalize_text(ticket)

    critical_terms = ["indisponivel", "indisponível", "fora do ar", "todos"]
    high_terms = ["perda de pacote", "sem internet", "cliente parado"]

    if ticket.customer_impact == "critical" or any(term in text for term in critical_terms):
        return PriorityResult(
            priority="critical",
            reason="impacto crítico informado ou indício de indisponibilidade ampla",
            confidence=0.9,
        )

    if ticket.customer_impact == "high" or any(term in text for term in high_terms):
        return PriorityResult(
            priority="high",
            reason="impacto alto ou sinal de falha relevante para operação do cliente",
            confidence=0.82,
        )

    if classification.category in {"network", "nat", "dns", "streaming"}:
        return PriorityResult(
            priority="medium",
            reason="incidente técnico com impacto operacional moderado",
            confidence=0.74,
        )

    return PriorityResult(
        priority="low",
        reason="não há sinal forte de indisponibilidade ou impacto elevado",
        confidence=0.62,
    )


def suggest_diagnostic(
    ticket: TicketInput,
    classification: ClassificationResult,
    priority: PriorityResult,
) -> DiagnosticSuggestion:
    category = classification.category

    if category == "dns":
        steps = [
            "Validar resolução de nomes com nslookup ou dig.",
            "Testar DNS alternativo para isolar falha de resolvedor.",
            "Verificar se outros serviços acessam normalmente por IP.",
        ]
        cause = "falha ou instabilidade de resolução DNS"
    elif category == "nat":
        steps = [
            "Verificar se o cliente está atrás de CGNAT ou duplo NAT.",
            "Validar necessidade de redirecionamento de portas.",
            "Conferir configuração do roteador e endereço WAN recebido.",
        ]
        cause = "restrição de NAT, CGNAT ou encaminhamento de portas"
    elif category == "streaming":
        steps = [
            "Testar acesso ao serviço em outra rede/dispositivo.",
            "Validar DNS, rota e possível bloqueio por detecção de VPN/proxy.",
            "Coletar erro exibido, horário e dispositivo afetado.",
        ]
        cause = "falha de rota, DNS, cache de app ou detecção indevida de proxy"
    elif category == "hardware":
        steps = [
            "Conferir energia, cabos e LEDs do equipamento.",
            "Validar link físico e porta conectada.",
            "Reiniciar equipamento apenas se o procedimento for autorizado.",
        ]
        cause = "falha física, cabo, porta ou equipamento do cliente"
    elif category == "network":
        steps = [
            "Executar ping para gateway e destino externo.",
            "Coletar perda de pacotes, latência e traceroute.",
            "Verificar se a falha afeta um dispositivo ou toda a rede.",
        ]
        cause = "instabilidade de conectividade, perda de pacotes ou rota"
    else:
        steps = [
            "Coletar mais detalhes do ambiente e horário da falha.",
            "Identificar escopo: um usuário, um dispositivo ou todos.",
            "Registrar evidências antes de encaminhar para análise avançada.",
        ]
        cause = "causa ainda indefinida por falta de sinais técnicos"

    return DiagnosticSuggestion(
        likely_cause=cause,
        next_steps=steps,
        escalation_needed=priority.priority in {"high", "critical"},
    )


def build_final_response(
    ticket: TicketInput,
    classification: ClassificationResult,
    priority: PriorityResult,
    diagnostic: DiagnosticSuggestion,
) -> FinalResponse:
    internal = (
        f"Chamado classificado como {classification.category} com prioridade "
        f"{priority.priority}. Causa provável: {diagnostic.likely_cause}."
    )
    customer = (
        "Recebemos o chamado e iniciamos a análise técnica. "
        f"Os primeiros indícios apontam para {diagnostic.likely_cause}. "
        "Vamos validar os testes iniciais e seguir com as próximas ações."
    )
    return FinalResponse(internal_summary=internal, customer_message=customer)

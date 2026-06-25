# Guia de explicação para entrevista

## Pitch curto

O AgentOps Triage é uma plataforma de triagem técnica que recebe chamados de
suporte e usa um fluxo de agentes para classificar o problema, definir prioridade,
sugerir diagnóstico e gerar uma resposta estruturada.

## Como explicar sem se enrolar

> Eu dividi a triagem em agentes especializados. Um agente classifica o chamado,
> outro calcula prioridade, outro sugere diagnóstico e o último gera a resposta.
> O LangGraph organiza a ordem desse fluxo, e o Pydantic valida os dados para
> reduzir saída inconsistente.

## Papel de cada tecnologia

- Python: linguagem principal do MVP.
- Pydantic: valida os contratos de entrada e saída.
- LangGraph: orquestra o fluxo dos agentes.
- LangChain: camada preparada para conectar modelos diferentes.
- Agno: extensão experimental para comparar outro framework de agentes.
- FastAPI: expõe o projeto por HTTP.
- Docker: facilita rodar a aplicação em ambiente isolado.

## Perguntas prováveis

### Por que não usar um prompt único?

Porque fica difícil auditar e explicar. Separar em etapas deixa o sistema mais
controlável e mais fácil de evoluir.

### A IA pode errar?

Sim. Por isso o projeto usa saída estruturada, validação e rastreio das decisões.
A ideia não é confiar cegamente na IA.

### O projeto já usa modelo real?

O MVP roda em modo local determinístico. A camada de integração está preparada
para plugar provedores externos, mas o modo demo é melhor para testes e entrevista.

### Onde entra sua experiência de suporte/redes?

Nos cenários de triagem: lentidão, perda de pacotes, DNS, NAT, streaming,
equipamento e impacto do cliente.

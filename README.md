# AgentOps Triage

AgentOps Triage é um MVP de **triagem técnica com arquitetura orientada a agentes/workflows**. A aplicação recebe um chamado de suporte, separa a análise em etapas e produz uma resposta estruturada com classificação, prioridade, diagnóstico inicial e orientação para atendimento.

O projeto nasceu da interseção entre suporte/redes e Engenharia de IA: pegar um fluxo operacional conhecido e transformá-lo em um sistema que possa evoluir de regras determinísticas para componentes apoiados por LLMs.

## Problema

Em operações de suporte e NOC, um chamado precisa ser entendido antes de ser escalado. Normalmente é necessário responder perguntas como:

- Qual é a categoria do incidente?
- Qual o impacto e a prioridade?
- Qual hipótese técnica deve ser investigada primeiro?
- Quais passos de diagnóstico fazem sentido?
- Como responder ao usuário de forma consistente?

O AgentOps Triage modela esse processo como um pipeline explícito em vez de concentrar toda a decisão em uma única função ou prompt.

## Fluxo interno

```text
Chamado técnico
      ↓
Classifier Agent
      ↓
Priority Agent
      ↓
Diagnostic Agent
      ↓
Response Agent
      ↓
Relatório estruturado + trace
```

Cada etapa possui uma responsabilidade específica e pode ser testada ou substituída separadamente.

## Tecnologias

- Python
- FastAPI
- Pydantic
- LangGraph
- LangChain
- Agno
- Docker
- Git/GitHub

## Exemplo de entrada

```json
{
  "title": "Cliente com lentidão e perda de pacotes",
  "description": "Cliente relata internet lenta, ping alto e perda de pacotes ao acessar serviços externos.",
  "channel": "portal",
  "customer_impact": "high",
  "service_tags": ["internet", "rede", "latencia"]
}
```

A aplicação retorna uma análise estruturada contendo campos como:

- `classification`;
- `priority`;
- `diagnostic`;
- `final_response`;
- `trace`.

## Por que separar em etapas

Uma resposta única gerada por um modelo pode parecer boa, mas é difícil saber **onde** uma decisão ruim aconteceu. O fluxo multi-step permite:

- validar entradas e saídas intermediárias;
- localizar falhas com mais facilidade;
- testar componentes individualmente;
- trocar uma etapa determinística por uma etapa com LLM sem reescrever tudo;
- registrar um trace do processo;
- criar avaliações específicas para classificação, prioridade e diagnóstico.

## Papel das principais ferramentas

### Pydantic

Define e valida os contratos de entrada e saída. Isso reduz dependência de texto livre e torna a API mais previsível para outros sistemas.

### LangGraph

Organiza o workflow e a passagem de estado entre as etapas do processo de triagem.

### LangChain

Funciona como camada preparada para integração com modelos e outros componentes do ecossistema de LLMs.

### Agno

É mantido como experimento de uma abordagem alternativa para construção de agentes.

### FastAPI

Expõe o fluxo como API HTTP e disponibiliza documentação OpenAPI interativa em `/docs`.

## Estado atual da IA

Este projeto foi iniciado como um MVP de arquitetura e estudo. A primeira versão prioriza:

- fluxo de triagem;
- contratos de dados;
- separação de responsabilidades;
- estrutura de agentes/nós;
- API e possibilidade de rastrear o processamento.

A integração com modelos reais pode ser evoluída pela camada preparada para LLMs. O README não trata uma integração futura como funcionalidade já concluída.

## Como rodar localmente

### 1. Clone

```bash
git clone https://github.com/vinionix/agentops-triage.git
cd agentops-triage
```

### 2. Ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Dependências

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
```

### 4. API

```bash
uvicorn agentops_triage.main:app --reload
```

Acesse:

```text
http://localhost:8000/docs
```

## Execução pelo terminal

```bash
python3 -m agentops_triage examples/sample_ticket.json --no-langgraph
```

Esse caminho é útil para testar a triagem sem depender da interface HTTP.

## Como testar rapidamente

### Health check

Use `GET /health` e verifique:

```json
{
  "status": "ok"
}
```

### Triagem

Envie um chamado para `POST /triage` e valide os campos estruturados retornados.

## Direção de evolução

Próximos passos tecnicamente interessantes:

1. integrar um LLM real atrás de uma interface substituível;
2. criar uma suíte de avaliação com chamados conhecidos;
3. medir precisão de classificação e prioridade;
4. adicionar recuperação de uma base técnica;
5. implementar confiança/abstenção;
6. registrar tokens, latência e modelo utilizado;
7. adicionar observabilidade por nó;
8. testar prompt injection e entradas adversariais;
9. manter aprovação humana para ações de maior risco.

## O que este projeto demonstra

- modelagem de um problema operacional real;
- Python e FastAPI;
- contratos de dados com Pydantic;
- arquitetura multi-step;
- LangGraph e preparação para integração com LLMs;
- separação entre lógica determinística e componentes generativos;
- preocupação com avaliação, rastreabilidade e evolução incremental.

## Documentação

- [Technical Overview](docs/TECHNICAL_OVERVIEW.md) — decisões de arquitetura, fronteira atual da IA, estratégia de testes e roadmap técnico.

## Como explicar o projeto em uma entrevista

> AgentOps Triage transforma o processo de triagem de suporte em um workflow explícito. Em vez de pedir para um único modelo decidir tudo, o sistema separa classificação, prioridade, diagnóstico e resposta. Isso permite validar cada etapa, rastrear decisões e integrar LLMs de forma incremental e testável.

## Autor

Desenvolvido por [Vinícius Fidelis](https://github.com/vinionix).

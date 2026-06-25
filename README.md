# AgentOps Triage

AgentOps Triage é um MVP de triagem técnica com IA. A ideia é receber um chamado de suporte, classificar o problema, definir prioridade, sugerir diagnóstico inicial e gerar uma resposta estruturada.

O projeto foi pensado para simular um fluxo parecido com suporte técnico, NOC ou operação de redes.

## O que a aplicação faz?

Você envia um chamado técnico em JSON, por exemplo:

```json
{
  "title": "Cliente com lentidão e perda de pacotes",
  "description": "Cliente relata internet lenta, ping alto e perda de pacotes ao acessar serviços externos.",
  "channel": "portal",
  "customer_impact": "high",
  "service_tags": ["internet", "rede", "latencia"]
}
```

A aplicação retorna uma análise estruturada contendo:

- tipo do problema;
- prioridade;
- possível causa;
- próximos passos de diagnóstico;
- resposta final para atendimento.

## Tecnologias usadas

- Python
- FastAPI
- Pydantic
- LangGraph
- LangChain
- Agno
- Docker
- Git/GitHub

## Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/vinionix/agentops-triage.git
cd agentops-triage
```

### 2. Crie o ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Depois de ativar, o terminal deve mostrar algo parecido com:

```bash
(.venv) usuario@pc:~/agentops-triage$
```

### 3. Instale as dependências

```bash
python3 -m pip install --upgrade pip
python3 -m pip install -e ".[dev]"
```

### 4. Rode a API

```bash
uvicorn agentops_triage.main:app --reload
```

Se tudo estiver certo, a aplicação ficará disponível em:

```text
http://localhost:8000
```

## Como testar no navegador

Abra:

```text
http://localhost:8000/docs
```

Essa página é a documentação interativa da API.

### Teste 1: verificar se a API está ativa

1. Procure a rota `GET /health`.
2. Clique em `Try it out`.
3. Clique em `Execute`.

Resposta esperada:

```json
{
  "status": "ok"
}
```

### Teste 2: executar a triagem

1. Procure a rota `POST /triage`.
2. Clique em `Try it out`.
3. Cole este exemplo no corpo da requisição:

```json
{
  "title": "Cliente com lentidão e perda de pacotes",
  "description": "Cliente relata internet lenta, ping alto e perda de pacotes ao acessar serviços externos. O problema afeta todos os dispositivos da residência.",
  "channel": "portal",
  "customer_impact": "high",
  "service_tags": ["internet", "rede", "latencia"],
  "metadata": {
    "city": "Rio de Janeiro",
    "plan": "residencial"
  }
}
```

4. Clique em `Execute`.
5. Observe o relatório retornado pela API.

## Como rodar pelo terminal

Também é possível testar usando o exemplo salvo no projeto:

```bash
python3 -m agentops_triage examples/sample_ticket.json --no-langgraph
```

## Como entender a resposta

A resposta da triagem pode trazer campos como:

- `classification`: categoria do problema identificado;
- `priority`: prioridade do chamado;
- `diagnostic`: hipótese técnica e próximos passos;
- `final_response`: resposta estruturada para atendimento;
- `trace`: histórico das etapas executadas.

## Fluxo interno do projeto

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
Relatório final
```

Cada etapa possui uma responsabilidade específica. Isso evita concentrar toda a lógica em uma única função ou em um único prompt.

## Papel das principais ferramentas

### Pydantic

Define e valida os formatos dos dados de entrada e saída.

### LangGraph

Organiza o fluxo dos agentes em etapas.

### LangChain

Serve como camada preparada para integração com modelos de linguagem.

### Agno

Fica como experimento para construção de agentes em uma abordagem alternativa.

### FastAPI

Expõe a aplicação como uma API HTTP e gera automaticamente a página `/docs`.

## Observação sobre IA generativa

Este projeto foi iniciado como um MVP de estudo e demonstração. A primeira versão prioriza arquitetura, fluxo de triagem e organização do código. A integração com modelos reais pode ser evoluída a partir da camada preparada para LLMs.

## Como explicar o projeto

AgentOps Triage é uma aplicação de triagem técnica com agentes. Ela recebe um chamado de suporte, separa a análise em etapas, classifica o problema, define prioridade, sugere diagnóstico e gera uma resposta final estruturada. O objetivo é aplicar conceitos de IA e automação em um cenário próximo de suporte técnico e redes.

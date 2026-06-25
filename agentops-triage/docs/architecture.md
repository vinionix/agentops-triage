# Arquitetura do AgentOps Triage

O AgentOps Triage transforma um chamado técnico em um relatório estruturado.

## Fluxo principal

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

## Componentes

### Pydantic

Usado para validar entrada e saída. A ideia é evitar que a aplicação dependa de
texto solto vindo de um modelo de linguagem.

### LangGraph

Usado para representar a triagem como um fluxo de estado. Cada etapa recebe o
estado atual, adiciona uma decisão e passa o resultado para a próxima etapa.

### LangChain

Fica isolado na camada `llm.py`. Isso permite trocar provedores de modelo sem
misturar essa decisão com a regra de negócio do projeto.

### Agno

Fica como adaptador experimental em `agno_adapter.py`. O objetivo é demonstrar
que a mesma ideia de triagem poderia ser explorada em outro framework de agentes.

## Decisão importante

O MVP possui modo determinístico local. Isso é útil para entrevista, teste e
demonstração, porque o projeto funciona mesmo sem provedor externo configurado.

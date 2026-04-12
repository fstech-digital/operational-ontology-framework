# Framework de Ontologia Operacional

Como operar agentes de IA em produção com estado auditável, sem memória persistente no modelo.

> Agentes baseados em LLM se tornam production-ready quando operam dentro de um envelope de controle explícito, não quando o modelo fica mais inteligente.

| | |
|---|---|
| **Autor** | Felipe Silva |
| **Versão** | 2.0 |
| **Licença** | [CC BY 4.0](LICENSE) |
| **Framework completo (13 seções)** | [fstech.digital/framework](https://fstech.digital/framework/) |

🇺🇸 [Read in English](README.md)

---

## Quick Start

```bash
git clone https://github.com/fstech-digital/operational-ontology-framework.git
cd operational-ontology-framework

pip install -r requirements.txt
cp .env.example .env
# Adicione sua ANTHROPIC_API_KEY no .env

python agent.py examples/customer-support
```

```bash
# Crie seu próprio projeto
mkdir meu-projeto
cp templates/_pin.md meu-projeto/
cp templates/_spec.md meu-projeto/
# Edite com as regras do seu domínio e tarefas
python agent.py meu-projeto
```

**Opções:** `--all` (roda todas as tarefas) · `--model claude-haiku-4-5-20251001` (trocar modelo) · `--dry-run` (inspecionar sem chamar LLM)

**Outros providers:** `ADAPTER=openai OPENAI_API_KEY=sk-... python agent.py examples/customer-support --model gpt-4o` (veja `adapters.py`)

---

## O Problema

Agentes LLM em produção enfrentam três problemas estruturais: sem rastro auditável de decisões, perda de estado entre sessões, e autovalidação circular. A solução comum (bancos vetoriais, embeddings) troca um problema por outro: o agente agora lembra de forma difusa, sem garantia de quais fatos sobreviveram.

## A Solução: 4 Artefatos Documentais

A memória vive no filesystem, não no modelo. Quatro arquivos markdown, versionados com git.

| Artefato | Papel | Volatilidade |
|----------|-------|-------------|
| **Pin** | Regras imutáveis, entidades do domínio, rotas de decisão | Muda raramente |
| **Spec** | Checklist de tarefas, estado de execução, aprendizados | Muda toda sessão |
| **Handoff** | Memória de sessão: decisões, resultados, briefing de continuação | Novo arquivo a cada sessão |
| **Facts** | Conhecimento acumulado de longo prazo com metadata | Cresce ao longo do projeto |

**Pin** = o que o projeto *é*. **Spec** = o que *fazer*. **Handoff** = o que *aconteceu*. **Facts** = o que foi *aprendido*.

## Ciclo de Execução

Cinco fases. Cada uma explícita, cada uma gera artefato.

```
Boot (+ Retrieval) → Executar → Write-back → Consolidar → Handoff
     ↑                                                        |
     └────────────────────────────────────────────────────────┘
```

1. **Boot** — Carregar Pin + Spec + Facts + último Handoff. Consultar Fact Store por contexto relevante.
2. **Executar** — Trabalhar nas tarefas. Sinais de degradação: repetição, perda de referências, respostas genéricas, ou >50% da janela de contexto consumida.
3. **Write-back** — Verificar, commitar, marcar concluída, anotar aprendizado. Uma tarefa, um commit.
4. **Consolidar** — Promover fatos da sessão para o Fact Store de longo prazo. Podar fatos stale (>90 dias sem verificação).
5. **Handoff** — Registro estruturado para próxima sessão. Sempre nova sessão, nunca compactação.

## Propriedades Chave

**Agnóstico de modelo.** Roda com Claude, GPT, Gemini, modelos locais. Testado em migrações entre providers com zero perda de estado.

**Soberania de memória.** A memória vive em arquivos versionados que você controla. Trocar de provider amanhã não apaga o estado. Não é feature, é consequência da arquitetura.

**Auditabilidade por design.** Cada decisão registrada com justificativa. Rastreabilidade total via `git log` e `git bisect`.

**O agente escreve sua própria memória.** Write-back não depende de disciplina humana. O agente atualiza a Spec, gera o Handoff, commita as mudanças. A disciplina está no prompt, não no treinamento de pessoas.

## Comparativo

| | **OOF (este)** | **LangChain / LangGraph** | **CrewAI** | **Mem0** | **MemPalace** | **ESAA** | **Letta** | **Palantir Foundry** |
|---|---|---|---|---|---|---|---|---|
| **O que resolve** | Estado auditável entre sessões | Orquestração de chamadas + memória | Orquestração multi-agente | Camada de memória standalone | Recall episódico | Estado para code agents | Runtime com memória OS-like | Ontologia enterprise |
| **Memória vive em** | Filesystem (markdown + git) | Banco vetorial (Chroma, pgvector) | Vetorial + escopos hierárquicos | Vetorial + Graph (Pro) | Verbatim + ChromaDB | Event log (JSONL + SHA-256) | Tiered (core/recall/archival) | Ontologia centralizada |
| **Infra necessária** | Nenhuma (só filesystem) | Banco vetorial + checkpointer | ChromaDB ou similar | Qdrant/Chroma/pgvector | Python + ChromaDB | JSONL + contracts YAML | Docker + providers LLM | Stack proprietário completo |
| **Decisões auditáveis** | Sim (decisões + justificativa + git bisect) | Parcial (logs de execução) | Parcial (memory scopes) | Não (recall por similaridade) | Não (recall probabilístico) | Sim (replay determinístico + hash) | Parcial (agente gerencia) | Sim (digital twin) |
| **Portável entre modelos** | Sim (testado Claude, Gemini, local) | Não (LangGraph runtime) | Não (CrewAI runtime) | Sim (framework-agnostic) | Parcial (local) | Não (code agents) | Parcial (multi-LLM) | Não (vendor lock-in) |
| **Memória de longo prazo** | Sim (Fact Store v2.0) | Via LangMem SDK | Reseta entre runs | Sim (vetorial + graph) | Sim (verbatim store) | Replay de eventos | Sim (archival tier) | Sim (ontologia) |
| **Agente escreve própria memória** | Sim (write-back no ciclo) | Não (persistência externa) | Não (reseta ao sair) | Não (chamadas SDK) | Não (tools MCP) | Não (orchestrator escreve) | Sim (self-editing context) | Não (plataforma gerencia) |
| **Evidência de produção** | 6 meses, 5 agentes, 3 clientes | Fortune 500 via LangSmith | 60% Fortune 500 | SOC 2, HIPAA | 3 dias de existência | Paper publicado, sem produção | Startups | Fortune 100, governos |
| **Custo** | Grátis (CC BY 4.0) | OSS grátis + cloud pago | OSS grátis + Enterprise | $0–249/mês | Grátis | Grátis | $0–200/mês | $M+/ano |

**Diferenças chave:**

- **Frameworks de orquestração** (LangChain, CrewAI) resolvem como agentes chamam ferramentas. OOF resolve como agentes mantêm estado entre chamadas. Complementam-se.
- **Camadas de memória** (Mem0, MemPalace, Letta) resolvem recall (encontrar fatos relevantes). OOF resolve governança (registrar decisões com justificativa, garantir portabilidade).
- **ESAA** compartilha o mesmo princípio (memória fora do modelo, auditável) mas foca em code agents com event sourcing. OOF foca em qualquer domínio de negócio com artefatos documentais.
- **Palantir Foundry** valida a mesma tese em escala enterprise. OOF entrega o mesmo paradigma com infra radicalmente mais simples (markdown + git vs stack proprietário).

## Em Produção

Seis meses, cinco agentes, três clientes. Frota migrou entre versões do Claude, Gemma (local) e providers comerciais mistos. Zero perda de estado em qualquer transição.

**Case externo:** VJ Turrini (consultoria empresarial) adotou em quatro semanas. Agente responde consultas de clientes, organiza agenda e mantém histórico auditável de decisões. Caminho: consulta, confiança, automação.

## Estrutura do Repo

```
├── agent.py                  # Implementação de referência (~400 linhas)
├── adapters.py               # Adaptadores LLM (Anthropic, OpenAI)
├── test_agent.py             # Testes unitários (pytest, 29 testes)
├── templates/
│   ├── _pin.md               # Pin em branco com orientação
│   ├── _spec.md              # Spec em branco com orientação
│   ├── _handoff.md           # Handoff em branco com orientação
│   └── _facts.md             # Fact Store em branco com orientação
├── examples/
│   └── customer-support/     # Projeto fictício completo
│       ├── _pin.md
│       ├── _spec.md
│       ├── _facts.md
│       └── handoffs/
├── requirements.txt          # anthropic>=0.40.0
└── .env.example
```

## Limites

- Não serve para chatbots puros (sem efeitos colaterais = sem necessidade de estado)
- Não serve para protótipos exploratórios (formalizar cedo demais cristaliza hipóteses erradas)
- Não serve para sistemas stateless (FaaS, transformações puras)
- Métricas empíricas (taxa de falha de boot, tempo de recuperação de handoff) estão [declaradas como pendentes](https://fstech.digital/framework/)

## Framework Completo

O framework completo (13 seções) com tríade D+L+A, mapeamento de componentes, protocolo de write-back, soberania de memória, validação N5, e lacunas empíricas declaradas:

**→ [fstech.digital/framework](https://fstech.digital/framework/)**

---

## Sobre a FSTech

Consultoria brasileira. Ontologias executáveis e agentes de IA em produção. O produto é a operação, não o documento.

[Site](https://fstech.digital) · [Newsletter](https://fstech.digital/newsletter/) · [X @fs_tech_](https://x.com/fs_tech_) · [Contato](https://fstech.digital/contato)

---

Framework de Ontologia Operacional v2.0 · Abril 2026 · [CC BY 4.0](LICENSE)

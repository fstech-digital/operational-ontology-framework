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

## Posicionamento

Complementa, não compete com frameworks de orquestração (LangChain, CrewAI, AutoGen). Esses resolvem *como* o agente chama ferramentas. Este resolve *como* o agente mantém estado auditável entre chamadas.

| | Frameworks de orquestração | Este framework |
|---|---|---|
| Resolve | Como agentes chamam ferramentas | Como agentes mantêm estado |
| Memória | Banco vetorial / embeddings | Filesystem / git |
| Dependência | Stack específica | Agnóstico de modelo e infra |

Referências: [Palantir Foundry](https://www.palantir.com/platforms/foundry/) (mesma Closed World Assumption, infra mais simples), [Microsoft Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview) (mesmo conceito, sem vendor lock-in).

## Em Produção

Seis meses, cinco agentes, três clientes. Frota migrou entre versões do Claude, Gemma (local) e providers comerciais mistos. Zero perda de estado em qualquer transição.

**Case externo:** VJ Turrini (consultoria empresarial) adotou em quatro semanas. Agente responde consultas de clientes, organiza agenda e mantém histórico auditável de decisões. Caminho: consulta, confiança, automação.

## Estrutura do Repo

```
├── agent.py                  # Implementação de referência (~200 linhas)
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

# Operational Ontology Framework

How to run AI agents in production with auditable state, no persistent memory in the model.

> LLM-based agents become production-ready when they operate within an explicit control envelope, not when the model gets smarter.

| | |
|---|---|
| **Author** | Felipe Silva |
| **Version** | 2.0 |
| **License** | [CC BY 4.0](LICENSE) |
| **Full framework (13 sections)** | [fstech.digital/framework](https://fstech.digital/framework/) |

🇧🇷 [Leia em português](README.pt-BR.md)

---

## Quick Start

```bash
git clone https://github.com/fstech-digital/operational-ontology-framework.git
cd operational-ontology-framework

pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

python agent.py examples/customer-support
```

```bash
# Start your own project
mkdir my-project
cp templates/_pin.md my-project/
cp templates/_spec.md my-project/
# Edit with your domain rules and tasks
python agent.py my-project
```

**Options:** `--all` (run all tasks) · `--model claude-haiku-4-5-20251001` (change model) · `--dry-run` (inspect without calling LLM)

---

## The Problem

LLM agents in production face three structural problems: no audit trail of decisions, state loss between sessions, and circular self-validation. The common fix (vector databases, embeddings) trades one problem for another: the agent now remembers diffusely, with no guarantee of which facts survived.

## The Solution: 4 Document Artifacts

Memory lives in the filesystem, not in the model. Four markdown files, versioned with git.

| Artifact | Role | Volatility |
|----------|------|-----------|
| **Pin** | Immutable rules, domain entities, decision routes | Rarely changes |
| **Spec** | Task checklist, execution state, learnings | Changes every session |
| **Handoff** | Session memory: decisions, results, continuation briefing | New file each session |
| **Facts** | Long-term accumulated knowledge with metadata | Grows over project lifetime |

**Pin** = what the project *is*. **Spec** = what to *do*. **Handoff** = what *happened*. **Facts** = what was *learned*.

## Execution Cycle

Five phases. Each explicit, each generates an artifact.

```
Boot (+ Retrieval) → Execute → Write-back → Consolidate → Handoff
     ↑                                                        |
     └────────────────────────────────────────────────────────┘
```

1. **Boot** — Load Pin + Spec + Facts + latest Handoff. Query Fact Store for relevant context.
2. **Execute** — Work through tasks. Degrade signal: repetition, lost references, generic responses, or >50% context window consumed.
3. **Write-back** — Verify, commit, mark done, annotate learning. One task, one commit.
4. **Consolidate** — Promote session facts to long-term Fact Store. Prune stale facts (>90 days unverified).
5. **Handoff** — Structured record for next session. Always new session, never compaction.

## Key Properties

**Model-agnostic.** Runs with Claude, GPT, Gemini, local models. Tested across provider migrations with zero state loss.

**Memory sovereignty.** Memory lives in versioned files you control. Switch providers tomorrow, state survives. Not a feature, a consequence of the architecture.

**Auditability by design.** Every decision is recorded with justification. Full traceability via `git log` and `git bisect`.

**Agent writes its own memory.** Write-back doesn't depend on human discipline. The agent updates Spec, generates Handoff, commits changes. The discipline is in the prompt, not in people training.

## Positioning

Complements, doesn't compete with orchestration frameworks (LangChain, CrewAI, AutoGen). Those solve *how* the agent calls tools. This solves *how* the agent maintains auditable state between calls.

| | Orchestration frameworks | This framework |
|---|---|---|
| Solves | How agents call tools | How agents maintain state |
| Memory | Vector DB / embeddings | Filesystem / git |
| Dependency | Specific stack | Model and infra agnostic |

References: [Palantir Foundry](https://www.palantir.com/platforms/foundry/) (same Closed World Assumption, simpler infra), [Microsoft Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/ontology/overview) (same concept, no vendor lock-in).

## In Production

Six months, five agents, three clients. Fleet migrated across Claude versions, Gemma (local), and mixed commercial providers. Zero state loss in any transition.

**External case:** VJ Turrini (business consulting) adopted in four weeks. Agent handles client queries, schedules, and auditable decision history. Path: consultation → trust → automation.

## Repo Structure

```
├── agent.py                  # Reference implementation (~200 lines)
├── templates/
│   ├── _pin.md               # Blank Pin with guidance
│   ├── _spec.md              # Blank Spec with guidance
│   ├── _handoff.md           # Blank Handoff with guidance
│   └── _facts.md             # Blank Fact Store with guidance
├── examples/
│   └── customer-support/     # Complete fictional project
│       ├── _pin.md
│       ├── _spec.md
│       ├── _facts.md
│       └── handoffs/
├── requirements.txt          # anthropic>=0.40.0
└── .env.example
```

## Limits

- Not for pure chatbots (no side effects = no need for state)
- Not for exploratory prototypes (formalizing too early crystallizes wrong hypotheses)
- Not for stateless systems (FaaS, pure transformations)
- Empirical metrics (boot failure rate, handoff recovery time) are [declared as pending](https://fstech.digital/framework/#11.1)

## Full Framework

The complete framework (13 sections) with D+L+A triad, component mapping, write-back protocol, memory sovereignty, N5 validation, and declared empirical gaps:

**→ [fstech.digital/framework](https://fstech.digital/framework/)**

---

## About FSTech

Brazilian consultancy. Executable ontologies and AI agents in production. The product is the operation, not the document.

[Site](https://fstech.digital) · [Newsletter](https://fstech.digital/newsletter/) · [X @fs_tech_](https://x.com/fs_tech_) · [Contact](https://fstech.digital/contato)

---

Operational Ontology Framework v2.0 · April 2026 · [CC BY 4.0](LICENSE)

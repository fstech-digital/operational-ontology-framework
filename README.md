# Operational Ontology Framework — FSTech

**Pin/Spec Protocol v2.** How to run AI agents in production with auditable state, no persistent memory in the model.

> LLM-based agents become production-ready when they operate within an explicit control envelope, not when the model gets smarter.

| | |
|---|---|
| **Author** | Felipe Silva |
| **Version** | 1.0 |
| **Date** | April 2026 |
| **License** | [CC BY 4.0](LICENSE) |
| **Canonical** | [fstech.digital/framework](https://fstech.digital/framework/) |

🇧🇷 **Versão em português:** [fstech.digital/framework](https://fstech.digital/framework/)

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

The agent runs the full cycle: Boot (load Pin + Spec + Handoff), Execute (pick first open task), Write-back (mark done, record learning), and Handoff (generate structured record for the next session).

### Start your own project

```bash
mkdir my-project
cp templates/_pin.md my-project/
cp templates/_spec.md my-project/

# Edit _pin.md with your domain rules
# Edit _spec.md with your tasks

python agent.py my-project
```

---

## 1. Context and Problem

LLM-based agents face three structural problems when they leave the prototype and enter real production.

**Lack of auditability.** There is no structured record of what the agent decided and why. Execution logs show the what, rarely the why. When the agent acts wrong, reconstructing the causal chain is forensics, not engineering.

**State loss between executions.** Each call starts from zero with no context from previous ones. The common attempt is to persist via vector databases or embeddings, which transfers the problem: the agent now remembers diffusely, with no guarantee of which facts survived.

**Circular validation.** The model validates itself. Ask the LLM if the answer is correct, and it confirms. Without an external control layer, validation is noise trained to sound confident.

The Operational Ontology Framework solves all three with a minimal document structure executed in a cycle. No additional infrastructure, no persistent memory in the model, no dependency on a specific stack.

## 2. Central Thesis

> An AI agent is production-ready when it operates within an explicit control envelope, with auditable state between executions, and when memory lives in the document, not in the model.

The framework is model-agnostic (runs with Claude, GPT, Gemini, local models) and infrastructure-agnostic (requires no vector database, specific orchestrator, or custom pipeline). The only dependency is a filesystem and document discipline.

A direct corollary follows: because memory lives in the filesystem and not in the model, the agent is portable across providers without state loss. Switching models tomorrow doesn't erase what it learned yesterday.

## 3. Foundation: The D+L+A Triad

The Operational Ontology rests on a first-principles decomposition: every real management system has three atomic components, no more.

**DATA (D).** Business entities. Leads, customers, projects, contracts, invoices. Everything that exists in the real world and needs representation in the system. Extraction and structuring of knowledge scattered across legacy systems, documents, and operator memories.

**LOGIC (L).** Relationship rules. Scoring, classification, prioritization, activation conditions. Business intelligence mapped so the system can infer. These are the laws governing behavior.

**ACTION (A).** Actionable write-back. Automations, notifications, state updates, messages sent. The stage where insight transforms into real execution in the operational environment.

The classic structure is linear: D to L to A. Practice shows the loop is continuous: actions generate new data, feeding refined logic, producing better actions. Designing a linear system is designing a system that dies on its first cycle.

**Operational implication.** When designing any automation, the canonical question is not "what happens when we execute" but "what happens after the action." If the answer is nothing, the system is linear, and linear means fragile.

**Client metaphor.** A business has nouns (customers, orders, contracts), verbs (bill, notify, query), and grammar (prioritization rules, scoring, escalation). An operating system exists when all business sentences are written and the system knows how to execute them. Data are nouns. Logic is grammar. Actions are verbs.

## 4. Executable Components

The framework implements D+L+A as three minimal document artifacts. Each artifact is a text file, versioned, readable by humans and models.

### 4.1 Pin (Invariant) — D + L

Immutable file describing what the project is. Properties that are true regardless of current state: rules, identity, limits, constraints.

The Pin functions as a system invariant. Projects grow in complexity, but invariants rarely change. When there's doubt about the project, the agent consults the Pin first, because it's the most stable document with the lowest cognitive cost to process.

**What goes in the Pin:**
- Project identity and scope
- Immutable rules (constraints, policies, limits)
- Domain entities with unambiguous definitions
- Decision routes with entry and exit conditions
- Automations (crons, triggers, webhooks) formalized

**What doesn't go in the Pin:**
- Execution state — that's the Spec
- Decision history — that's the Handoff
- Human operator preferences — that's another document

### 4.2 Spec (Behavior) — L + A

Living file describing what to do. Sequential task checklist. The more tasks and dependencies, the faster the document changes, which is why the Spec is more volatile than the Pin.

The Spec is the behavioral space. Each completed task is marked and generates learning. A task marked as completed is immutable — never uncheck. If the result has a defect, create a new corrective task referencing the original. Same principle as Git: commits are immutable, fixes are new commits.

**Self-containment principle.** Every task in a Spec must survive the handoff. Whoever writes the task is rarely who executes it — it could be another agent, another session, another day. A task that depends on implicit context to be understood dies the moment that context dies. Therefore, each Spec entry carries enough metadata for any subsequent executor to know what to do, why it exists, where the demand came from, and the minimum implementation path.

### 4.3 Handoff (Memory) — A to D

Structured record that feeds the next cycle. Not an execution log (the what), but a state record (where we are, why we stopped, what needs to continue).

**Handoff contains:**
- Focus of the ended session
- Decisions made with justification
- Tasks executed with results
- Tasks not executed with reason
- Continuation: re-engagement briefing for the next cycle

**The handoff is the memory.** The model needs no persistent state of its own, because session N's handoff feeds session N+1's boot. Each new cycle begins with complete context in minutes, no vector database, no embeddings, no stateful memory.

A fine distinction matters: this is not "zero persistence." The filesystem persists, the ontology persists, the handoff persists. What's zero is state maintained inside the model. Memory lives in the document, not in the neural network weights.

## 5. Execution Cycle

The framework operates in four phases. Each phase is explicit, each phase generates an artifact.

**Boot → Execute → Write-back → Handoff.** A cycle that closes on itself every session.

### Boot

Load the project's Pin and Spec at session start. In multi-agent systems, boot also loads shared memory (global index) and the latest handoff entry.

### Execute

Resolve tasks in the same session. As many as the session can handle with quality. The limit isn't the number of tasks, it's context degradation. Practical signals: the agent repeats information already stated, loses reference to earlier decisions in the session, or generates generic responses where it was previously specific. In terms of window, operating above 50% of the model's context capacity is the alert zone. FSTech uses 500K tokens as the handoff threshold on models with a 1M window.

**Parallel execution (Wave).** When the Spec has three or more independent tasks, the main agent dispatches sub-agents in parallel with isolated context. The main agent preserves context for orchestration and reasoning. Dependencies are respected: task B depending on A waits for A to complete.

**Isolated context for heavy tasks.** For tasks involving extensive reading (codebase analysis, research, auditing), delegate to a sub-agent even if sequential. The sub-agent operates in fresh context, without accumulating residue. This prevents quality degradation from irrelevant context accumulation.

### Write-back (Atomic Commit)

For each completed task:

- **Verify** before marking done — confirm the task is actually complete, with rigor proportional to risk
- **Commit** one task, one commit. Message references the task. Full traceability via git bisect
- **Mark completed** in the Spec
- **Annotate learning** for the next task, if applicable

**Pre-done verification (Programmatic Gate).** Before marking any task as completed, the agent executes a verification proportional to the action's risk. Low-impact tasks get a coherence re-read. Medium-impact tasks require functional testing. High-impact tasks require adversarial testing, manual review, and explicit discipline against known vulnerability classes. Rigor isn't uniform because the cost of error isn't uniform.

**Canonical anti-pattern.** Verification is not "I ran it and got no error." It's "I tried to break it and couldn't."

### Handoff

End the session when:

- Degradation signals appear: repetition of already-covered information, loss of reference to earlier decisions, generic responses where there was previously specificity, or consumption above 50% of the model's context window
- There's a project or domain change
- The agent enters territory where accumulated context has become noise, not signal

**Procedure: always new session, never compaction.** Compaction is lossy compression. It loses nuance, loses causality, and pays a context cost right at the next session's opening. A new session with boot via Pin and Spec starts light, recovers complete state from what's documented in the filesystem, and preserves fact fidelity.

**Why Handoff is not just another compaction.** Handoff and compaction are two distinct acts. Compaction is an automatic heuristic applied to the entire history, with no goal beyond reducing tokens. Handoff is written with explicit intent of continuity. The asymmetry isn't in the act of writing, it's in the purpose. One is reaction, the other is protocol.

## 6. D+L+A Component Mapping

| Layer | Where it lives | What it contains |
|-------|---------------|-----------------|
| Data (D) | Pin + context inherited from previous Handoff | Entities, rules, initial state |
| Logic (L) | Pin (routes) + Spec (tasks) + Pre-done Gate | Decision rules and external validation |
| Action (A) | Execution + Handoff | Write-back to real system, memory for next cycle |

External validation (Pre-done Gate) is what eliminates circularity. The agent doesn't validate itself on externally verifiable questions. Schema, permissions, dependency state — everything is checked by code, not by model opinion.

## 7. Mandatory Write-Back

> If you think you know something but don't write it down, you only think you know it.
> — Leslie Lamport

Write-back is not just recording. It's the act of thinking itself. Formulating in text reveals gaps, forcing precision that internal thought doesn't require.

Every perception, insight, or decision generates write-back:
- Document update
- Record creation
- State change
- Actionable notification

**Metric:** insight-to-write-back cycle under one day.

**Test:** if it's hard to write, the idea isn't mature yet.

Insight without real system change is computational waste.

## 8. Real Case: FSTech in Production

The framework is not speculation. FSTech operates its internal agent fleet on this framework for six months in production, five active channels, multiple clients.

**Fleet operating under the framework:**
- **Ares** — orchestrator agent on the operator's terminal, executes auditing, refactoring, development, strategic analysis
- **Ontos** — central hub of the fleet, runs on a dedicated server, intermediates communication and orchestrates field agents
- **Finn** — personal financial agent in production for three distinct clients, running in isolated containers, each client with its own Pin
- **Chava** — personal assistant running on a client's notebook, integrated with WhatsApp, calendar, and contacts
- **Ares WhatsApp** — same orchestrator agent on a WhatsApp channel, direct communication with leads and clients

**Technical proof of portability.** Over six months of operation, the fleet migrated between models without losing accumulated state. Ares ran with Claude across different versions, Ontos operates partially on local models (Gemma), Finn mixes commercial providers by client cost. In none of these transitions was accumulated knowledge lost, because it was never in the model.

**Validated external case.** A client company (VJ Turrini, business consulting) faced the classic problem: operational logic concentrated in two people, no structured record. Decisions about clients, schedule, and priorities lived in the partners' memory. The agent (Chava) was configured with its own Pin (business rules, client profiles, service policies) and operational Spec. Adoption happened without imposition: the operator started consulting the agent via WhatsApp for real tasks, verified that responses reflected the business rules, and progressively delegated. In four weeks, the agent was answering client queries, organizing schedules, and maintaining an auditable decision history. The path was consultation, trust, automation. Not the reverse.

## 9. Positioning

The framework doesn't compete with call orchestration frameworks (LangChain, CrewAI, AutoGen). It complements them. Those frameworks solve how the agent calls tools. The Operational Ontology Framework solves how the agent maintains auditable state between calls and executions.

| Aspect | Call orchestration | FSTech Framework |
|--------|-------------------|-----------------|
| Category | Call orchestration | State control and execution |
| Dependency | Specific stack | Model and infra agnostic |
| Auditability | Execution logs | Structured handoff in document |
| Memory | Persistent (vector DB, embeddings) | Documental (filesystem) |
| Relationship | Can run on top of any | Can run underneath any |

**International comparisons:**
- **Palantir Foundry** operates under Closed World Assumption with centralized ontology. FSTech follows the same principle (if it's not documented, it doesn't exist for the system) but replaces the proprietary stack with a versioned filesystem. Same paradigm, radically simpler infrastructure.
- **Microsoft Fabric IQ Ontology** offers operational context for agents via a managed product. FSTech offers the same without single vendor, lock-in, or mandatory SaaS.
- **Skan Agentic Ontology of Work** formalizes ontology as a common language between agents. FSTech goes further by formalizing the execution cycle, not just the vocabulary.

### 9.1 Memory Sovereignty

When memory lives inside the model, inside the provider, inside a proprietary harness, whoever uses the agent doesn't control their own state. Switching providers means starting from zero.

The Operational Ontology Framework solves this by construction. Since memory lives in versioned filesystem artifacts (Pin, Spec, Handoff), the fleet is portable by design. An agent that ran with Claude yesterday can run with Gemini tomorrow, with GPT next week, with a local model after that, and accumulated state remains valid.

This isn't a feature added to attract those who fear lock-in. It's a direct consequence of the initial principle that memory lives in the document.

## 10. N5 Validation

Every framework component passes through **N5**, a proprietary analytical validation methodology developed by FSTech. N5 applies five hierarchical criteria to any solution or system before considering it production-ready. The internal hierarchy prioritizes empirical evidence over theoretical elegance.

The Operational Ontology Framework was validated by all five N5 criteria before publication. Full details of the N5 methodology are available under partnership agreement with FSTech.

## 11. Limits and When Not to Use

An honest framework declares where it doesn't apply.

- **Pure conversational agents** with no side effects on real systems. A FAQ chatbot doesn't need Pin, Spec, or Handoff.
- **Exploratory prototypes** where the goal is discovering whether the problem exists. Formalizing too early crystallizes wrong hypotheses.
- **Truly stateless systems** where each execution is independent. Function as a service, pure transformations, deterministic data pipelines.
- **Teams without write-back discipline.** The framework fails silently when operators ignore registration. But the solution isn't organizational culture — it's agent design.

**On write-back discipline.** The most common objection is that write-back depends on human discipline, and humans forget. The answer is that the agent is the primary operator, not the human. In the correct design, the agent itself executes write-back as part of the cycle: updates the Spec upon task completion, generates the Handoff at session end, commits the changes. The human doesn't need to remember to register because they're not the one registering. The discipline is codified in the agent's prompt, not in the team's routine. The real failure point isn't human forgetfulness — it's a misconfigured agent that didn't receive the instruction to register. This is solved in the Pin, not in people training.

### 11.1 Declared Empirical Gap

The evidence presented (six months of operation, five agents, VJ Turrini case) is operational evidence, not quantitative metrics. This document does not contain: boot failure rate, mean handoff recovery time, or controlled comparison against a baseline without write-back.

The write-back discipline that the framework itself prescribes makes these metrics producible. The raw material exists — it just hasn't been compiled into a public report in this version.

**Empirical roadmap (public commitment):**
- Cycle metrics published in a future version (cycles/week, mean boot time, mean handoff time)
- Controlled comparison against a baseline without write-back
- State preservation study across transitions between three different providers

Read this framework as a mechanism description and invitation to verify, not as a peer-reviewed paper with arbitrated metrics.

## 12. This Document Is a Snapshot

The framework described here is not a final state. It's the April 2026 snapshot of a system that continues to move, precisely through the cycle it describes. Each component is refined by the very write-back it governs.

In triad terms, the framework is Data (document structure), Logic (execution cycle), and Action (mandatory write-back), applied recursively to itself.

## 13. Next Steps

This document is the public version of the framework that FSTech operates internally. The internal version includes:

- Executable Pin and Spec templates by project type
- History-based boot and handoff toolchain
- Adjacent protocols (channel isolation, escalated notification, qualification firewall)
- Full N5 methodology applied to each artifact
- Specific integrations with operational tools

The public version is sufficient for adoption in real projects. Organizations wanting to accelerate adoption can [contact FSTech directly](https://fstech.digital/contato).

---

## About FSTech

FSTech is a Brazilian consultancy focused on operationalizing businesses through executable ontologies and AI agents in production. The product is the operation, not the document.

- **Founder:** Felipe Silva
- **Site:** [fstech.digital](https://fstech.digital)
- **Framework (canonical):** [fstech.digital/framework](https://fstech.digital/framework/)
- **Newsletter:** [fstech.digital/newsletter](https://fstech.digital/newsletter/)
- **X:** [@fs_tech_](https://x.com/fs_tech_)

---

🇧🇷 **Leia em português:** [fstech.digital/framework](https://fstech.digital/framework/)

---

Operational Ontology Framework v1.0 · April 2026 · [CC BY 4.0](LICENSE)

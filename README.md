# Operational Ontology Framework

A public reference for operating AI systems with explicit state, governance and human-controlled action.

> Operational ontology is the control model that connects **Data**, **Logic** and **Action** so AI can work within real organizational constraints.

| | |
|---|---|
| **Publisher** | FSTech |
| **Canonical definition** | https://fstech.digital/ontologia-operacional/ |
| **Technical essay** | https://fstech.digital/framework/ |
| **Status** | Public reference, not production code |
| **License** | [FSTech Public Reference License](LICENSE) |

[Leia em português](README.pt-BR.md)

## Purpose

This repository establishes the public definition, authorship and conceptual boundaries of the Operational Ontology Framework.

It explains:

- why operational state must be explicit;
- how Data, Logic and Action relate;
- which governance problems appear in stateful AI work;
- which principles reduce improvisation and uncontrolled side effects;
- where a conceptual exercise must stop and a governed implementation must begin.

It does not publish the implementation used by FSTech or its clients.

## D+L+A

| Layer | Operational question | Failure mode when absent |
|---|---|---|
| **Data** | What exists, what does it mean and where is the source of truth? | The model guesses entities, state or ownership. |
| **Logic** | Which rules, limits, exceptions and approvals govern decisions? | The model improvises process. |
| **Action** | What may be proposed or executed, by whom and with which evidence? | Automation creates uncontrolled side effects. |

A useful AI response is not yet an operational system. The three layers must remain connected, reviewable and bounded by human authority.

## Public Governance Model

The public method uses four state artifacts:

| Artifact | Role | Volatility |
|---|---|---|
| **Pin** | Stable identity, domain boundaries and non-negotiable rules | Low |
| **Spec** | Current objective, tasks, blockers and acceptance criteria | High |
| **Handoff** | Session continuity: decisions, attempts, results and next action | Append-only |
| **Facts** | Long-term observations with source, date and confidence | Medium |

Reusable procedures may complement these artifacts, but procedures are not state and do not replace authorization, verification or write-back.

## Public Boundary

This repository deliberately contains no:

- production code or executable agent;
- schemas, validators or deployment artifacts;
- private prompts, tools, adapters or integrations;
- client implementations or operational datasets;
- security policies, evaluation suites or commercial playbooks used in delivery.

The public surface describes the thesis. Governed implementation remains context-specific.

## Try the Method

For a small, human-supervised experiment, use the [free Operational Ontology Lite or the Starter Kit](https://fstech.digital/operational-ontology-kit/?utm_source=github&utm_medium=referral&utm_campaign=operational-ontology-public-reference&utm_content=try-kit).

The Starter Kit is currently available in Portuguese. It is designed for manual learning and does not authorize automatic messages, system writes, payments or other external side effects.

## Documentation

- [What is Operational Ontology?](docs/what-is-operational-ontology.md)
- [D+L+A model](docs/dla-model.md)
- [Governance principles](docs/governance-principles.md)
- [Anti-patterns](docs/anti-patterns.md)
- [Conceptual example](docs/conceptual-example.md)

## About FSTech

FSTech designs operational AI systems for organizations that need explicit state, governed action and auditable continuity.

Site: https://fstech.digital

Contact: https://fstech.digital/contato

This repository is a public reference. It is not open-source software and does not include a production implementation.

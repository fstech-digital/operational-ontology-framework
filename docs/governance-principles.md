# Governance Principles

## Explicit State

Current objectives, constraints and unresolved decisions should exist outside the model conversation.

## Human Authority

The system must distinguish drafting, proposing, approving and executing. High-impact actions remain under explicit human authority.

## Source Before Retrieval

Finding information is not the same as determining truth. Every relevant fact needs a source, freshness expectation and owner.

## Verification Before Completion

Producing an answer is not evidence that work happened. Completion requires an observable result appropriate to the action.

## Write-back

Execution should update durable state so the next operator inherits decisions, results, blockers and the next safe action.

## Controlled Change

Stable rules need ownership and a deliberate amendment path. No internal artifact overrides law, security controls or revoked authorization.

## Minimal Scope

Start with one small, recurring routine. Expanding an unverified process only scales ambiguity.

## This Reference Is Not a Safety Specification

Moving from a manual exercise to an implementation requires additional controls. At minimum, the organization must address:

- least privilege and authorization revalidation at execution time;
- untrusted input and prompt-injection boundaries;
- data classification, minimization and retention;
- idempotency, retry safety and rollback or compensation;
- tamper-resistant audit evidence and correlation;
- emergency stop, incident response and ownership.

These controls are not implemented by Markdown artifacts. If an action can affect a person, system, account, payment or external channel, the public reference alone is insufficient.

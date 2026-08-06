# D+L+A Model

D+L+A means Data, Logic and Action.

## Data

Data describes what exists: entities, relationships, states, sources of truth and ownership.

An AI system should not treat retrieved text as automatically true, current or authorized. Source, freshness and responsibility still matter.

## Logic

Logic describes what governs the operation: rules, thresholds, exceptions, priorities, approvals and stop conditions.

Important rules should be explicit and reviewable rather than hidden inside an oversized prompt.

## Action

Action describes what may happen: produce a draft, update internal state, request approval, call a system, escalate or block.

Action authority must be narrower than conversational capability. A model being able to describe an action does not mean it may execute it.

## Verticality

The three layers create value only when connected:

```text
Data -> Logic -> Action -> Evidence -> Write-back
```

Data without Logic becomes an informative dashboard. Logic without Action becomes a policy document. Action without Data and Logic becomes risky automation.

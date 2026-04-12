# Pin — [Project Name]

<!-- 
  PIN = INVARIANT. Properties true regardless of current state.
  This file changes rarely. The agent consults it first when in doubt.
  
  Think of this as the "constitution" of your project.
  Rules here override everything else.
  
  Tips:
  - Be specific. "Handle refunds" is vague. "Auto-approve refunds under $500 within 30 days" is a rule.
  - Define entities with precision. If "customer" can mean 3 things, the agent will guess wrong.
  - Decision routes should have explicit conditions, not just descriptions.
  - If you're unsure whether something belongs here or in Spec, ask: "Does this change weekly?" If yes → Spec.
-->

## Identity

- **Project:** [name — what this project is called]
- **Domain:** [what this project operates on — e.g., "customer billing and support"]
- **Owner:** [who owns this project — person or team]

## Entities

<!-- Define every noun the agent will encounter. Ambiguity here = wrong decisions later. -->

| Entity | Definition | Example |
|--------|-----------|---------|
| | | |

## Rules (Immutable)

<!-- These are laws, not guidelines. The agent must follow them without exception. -->

1. [Rule that never changes regardless of context]
2. [Another invariant rule]

## Decision Routes

<!-- For each recurring decision, define trigger → conditions → actions. 
     The agent should be able to follow this like a flowchart. -->

### [Decision Name]
- **Trigger:** [when this decision activates]
- **Conditions:** [what determines the outcome — be explicit with thresholds]
- **Actions:** [what happens for each outcome]

## Boundaries

<!-- Scope prevents the agent from hallucinating responsibilities it doesn't have. -->

- **In scope:** [what this project covers]
- **Out of scope:** [what this project explicitly does NOT cover]
- **Escalation:** [when and how to escalate to a human]

## Automations

<!-- Recurring actions that happen on schedule or on event. -->

| Trigger | Action | Schedule |
|---------|--------|----------|
| | | |

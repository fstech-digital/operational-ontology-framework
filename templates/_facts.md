# Facts — [Project Name]

<!--
  FACTS = ACCUMULATED MEMORY. Long-term knowledge learned across all sessions.
  This file grows over time. Each fact has metadata for traceability.
  
  Tips:
  - Every fact needs a source. "The API is slow" is opinion. 
    "Stripe webhook averages 3-5s on weekends (observed 2026-04-06, tkt_2901)" is a fact.
  - Confidence levels: verified (tested/confirmed), observed (seen once), inferred (deduced).
  - Review facts older than 90 days. If not re-verified, they may be stale.
  - If a fact contradicts a Pin rule, the Pin wins. Facts are observations, Pins are laws.
  - Parsimony: a Fact Store that only grows is a Fact Store that degrades. Prune regularly.
  
  Format for each fact:
    - [Observation] (source: [where you learned it], [YYYY-MM-DD], confidence: [verified|observed|inferred])
  
  Promotion criteria (session learning → fact):
    - The learning applies beyond a single task
    - It would change how a future agent approaches work
    - It is specific enough to be actionable (not "things went well")
  
  Pruning criteria:
    - Fact is >90 days old and hasn't been re-verified → flag as stale
    - Fact is contradicted by a newer observation → remove or update
    - Fact is about a system/API that no longer exists → remove
  
  The Consolidation phase in agent.py auto-promotes session learnings here
  and flags stale entries. You can also add facts manually.
-->

## Client / Stakeholder Preferences

<!-- Discovered preferences, communication styles, priorities.
     Example: "Customer cust_8a3f prefers email over phone (source: tkt_2898, 2026-04-12, confidence: verified)" -->

## System Behaviors

<!-- Observed behaviors of APIs, integrations, tools — latency, limits, edge cases.
     Example: "Stripe webhook averages 3-5s on weekends (source: 4-week observation, 2026-04-06, confidence: observed)" -->

## Design Decisions

<!-- Decisions and their justifications that transcend a single session.
     Example: "Auto-approve refunds under $500 (source: Pin rule, 3 months zero disputes, confidence: verified)" -->

## Confirmed Patterns

<!-- What works, what fails silently, what to avoid.
     Example: "Tickets with 'billing' + 'double' are almost always duplicate Stripe charges (source: 12 tickets, 2026-03-20, confidence: verified)" -->

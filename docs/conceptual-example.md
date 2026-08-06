# Conceptual Example: Weekly Client Review

This example is intentionally non-executable. It illustrates the D+L+A separation without defining a production implementation.

## Data

- active clients;
- open commitments;
- agreed deadlines;
- last confirmed status;
- named source of truth.

## Logic

- overdue commitments appear before future commitments;
- missing status is labeled for verification rather than inferred;
- no item is marked complete without recorded confirmation;
- sensitive or disputed items are escalated to a human.

## Action

The AI prepares a prioritized draft for human review. It does not contact clients or update the source system.

## Evidence

The reviewer confirms which items are accurate, which require correction and which may proceed.

## Write-back

The approved status and remaining blockers are recorded in the organization's authorized source. A short handoff preserves the next review point.

This exercise can be tested manually with the [Operational Ontology Starter Kit](https://fstech.digital/operational-ontology-kit/?utm_source=github&utm_medium=referral&utm_campaign=operational-ontology-public-reference&utm_content=conceptual-example). Production use requires context-specific controls.

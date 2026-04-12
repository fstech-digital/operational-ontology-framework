# Handoff — [YYYY-MM-DD HH:MM]

<!-- 
  HANDOFF = MEMORY. Structured record for the next session.
  Not a log of what happened (that's git). This is a state record: 
  where we are, why we stopped, what needs to continue.
  
  Tips:
  - Decisions without reasoning are useless. Always include WHY.
  - Continuation must have specific next steps, not "continue working on X".
  - Bad continuation: "Finish the refund feature." 
    Good continuation: "Test refund endpoint with amount=0 and amount>500. 
    Check tkt_2901 in Stripe dashboard for customer cust_8a3f."
  - The next session starts COLD. Write as if the reader knows nothing 
    about what happened today.
-->

## Focus
[One line — the central theme of this session]

## Decisions (with reasoning)

- **[What was decided]**
  → Reason: [why this choice and not another]

## Tasks Executed

- [Task]: [result — success/failure + relevant details]

## Tasks NOT Executed

- [Task]: [reason — skipped, blocked, deferred, ran out of context]

## Continuation

Next session should:
- [Specific action — include file path, endpoint, or test to run]
- [Another concrete next step]

# Skills — [Project Name]

<!--
  SKILLS = REUSABLE PROCEDURES. Expertise the agent accumulates through practice.
  Unlike Facts (what was learned) or Pin rules (what is invariant), Skills describe
  HOW to do something — step-by-step, with verification and tooling.

  Tips:
  - A skill should be self-contained. An agent loading it for the first time should
    be able to execute it without additional context beyond the Pin.
  - Skills improve through write-back. After each execution, update the skill with
    new steps, edge cases discovered, or optimizations found.
  - Keep skills focused. "Handle customer support" is too broad. 
    "Process refund request" or "Onboard new client" is a skill.
  - If a skill hasn't been used in 90+ days, consider archiving it.
  - Skills reference Pin rules as constraints, but never duplicate them.
  - A Fact informs decisions. A Skill executes actions. Don't confuse the two.

  Format for each skill:
    ### [Skill Name]
    - **Trigger:** When this skill activates
    - **Steps:** Numbered sequence with verification checkpoints
    - **Tools:** External resources used (APIs, scripts, templates)
    - **Done when:** Success criteria
    - **Edge cases:** Known exceptions and how to handle them
    - **Last refined:** [date] — what changed

  Promotion criteria (when to create a skill):
    - You've done the same procedure 3+ times
    - The procedure has more than 3 steps
    - Getting it wrong has real consequences
    - A new agent or session would struggle without the instructions

  Archival criteria:
    - Skill hasn't been triggered in 90+ days
    - The underlying system/API it targets no longer exists
    - A newer skill supersedes it
-->

## Core Skills

<!-- Skills used frequently. These are the agent's primary capabilities. -->

### [Skill Name]
- **Trigger:** [when this skill activates — command, pattern, event]
- **Steps:**
  1. [First step with expected outcome]
  2. [Second step]
  3. [Verification checkpoint — what to check before continuing]
  4. [Continue...]
- **Tools:** [APIs, scripts, templates used]
- **Done when:** [specific success criteria]
- **Edge cases:**
  - [Known exception] → [how to handle]
- **Last refined:** [YYYY-MM-DD] — [what changed and why]

## Specialized Skills

<!-- Skills used less frequently but important when triggered. -->

## Archived Skills

<!-- Skills no longer active. Kept for historical reference.
     Move here instead of deleting — preserves the evolution history. -->

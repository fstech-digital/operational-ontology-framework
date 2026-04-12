# Spec — Customer Support Agent

## Current Sprint

### Tasks

- [ ] **Handle ticket tkt_2901** — Customer reports billing double-charge on Pro plan. Check Stripe for duplicate payment. If confirmed, process refund per Pin rules (<=500, within 30 days = auto-approve). Reply with confirmation and expected timeline.
- [ ] **Respond to tkt_2915** — Enterprise customer asking about API rate limits on new endpoint. Check docs at docs.company.com/api/limits. SLA is 1h, ticket created 45min ago.
- [ ] **Triage morning queue** — 6 unread tickets from overnight. Classify by plan tier, assign SLA timers, flag any Enterprise tickets for immediate handling.

### Completed

- [x] **Handle ticket tkt_2898** — Customer wanted plan downgrade from Pro to Free. No active contract. Processed immediately. Confirmation email sent.
  - Learned: Downgrade removes API keys instantly. Should warn customer before processing.

- [x] **Update knowledge base article KB-0042** — Added section about new webhook retry behavior after v2.3 release.
  - Learned: Engineering changelog at changelog.internal is the fastest source for release details.

## Blocked

- [ ] **Resolve tkt_2910** — Customer reports data export failing. Blocked by: Engineering investigating bug ENG-4521. Next check: 2026-04-13.

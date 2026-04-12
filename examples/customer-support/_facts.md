# Facts — Customer Support

## Client / Stakeholder Preferences

- Customer cust_8a3f prefers email over phone for refund confirmations (source: tkt_2898, 2026-04-12, confidence: verified)
- Enterprise clients expect acknowledgment within 30 min even if resolution takes longer (source: SLA review meeting, 2026-03-15, confidence: verified)

## System Behaviors

- Stripe webhook delivery averages 3-5s on weekends, <1s on weekdays (source: observation over 4 weeks, 2026-04-06, confidence: observed)
- Downgrade from Pro to Free removes API keys instantly with no grace period (source: task execution tkt_2898, 2026-04-12, confidence: verified)
- Plaid bank sync can take up to 24h for first connection (source: Plaid docs + customer report, 2026-04-10, confidence: verified)

## Design Decisions

- Auto-approve refunds under $500 within 30 days without human review (source: Pin rule, confirmed by 3 months of zero disputes, confidence: verified)
- Always warn customer about API key deletion before processing downgrade (source: learned from tkt_2898, 2026-04-12, confidence: verified)

## Confirmed Patterns

- Customers who contact support within first 48h of signup have 3x higher retention if responded to within SLA (source: Q1 cohort analysis, 2026-04-01, confidence: observed)
- Tickets mentioning "billing" + "double" are almost always duplicate Stripe charges, not UI bugs (source: pattern across 12 tickets, 2026-03-20, confidence: verified)

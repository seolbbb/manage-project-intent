# Intent Keeper Decision Log

## Status vocabulary

- `proposed`, `accepted`, and `superseded` are allowed.

## Decisions

### DEC-001 — Preserve user intent

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: AI sessions share tools but not the user's implicit intent.
- User intent/value protected: Preserve the reason behind user interventions and tradeoffs.
- Intervention: The user required repeated questions before implementation.
- Options considered: Chat-only context; technical ADRs; a broader human-intent decision log.
- Decision: Maintain the broader human-intent decision log.
- Consequences: New agents must read the rationale before reversing deliberate constraints.
- Reconsider when: The user changes the protected value or its premise no longer applies.
- Supersedes: None
- Superseded by: None

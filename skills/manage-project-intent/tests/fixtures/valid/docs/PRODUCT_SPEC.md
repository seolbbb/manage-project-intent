# Intent Keeper Product Spec

## Document control

- Status: accepted
- Last reviewed: 2026-07-18

## Product intent

- Why this exists: Keep a user's product intent legible across AI sessions.
- User intent to preserve: Later agents must understand why deliberate constraints exist.
- Priority values: Intent fidelity before automatic optimization.
- Non-negotiable tradeoffs: Do not trade away user control for convenience without a new decision.
- Reconsider these choices when: The user explicitly changes the priority or its premise no longer applies.

## Product definition

A local documentation workflow for software projects.

## Users and problems

Solo builders need AI sessions to continue without repeating product decisions.

## Goals and success criteria

A fresh agent can explain the intent, current state, rationale, and next task.

## Scope

### In scope

Local Markdown project records and structural validation.

### Out of scope

External issue trackers and automatic deployment.

## User experience

The agent interviews, plans, records, implements, verifies, and converges documents.

## Functional requirements

Maintain four canonical documents and one actionable Next task.

## Safety, privacy, and data

Never overwrite existing project documents during bootstrap.

## Non-functional requirements

Validation uses the Python standard library and works offline.

## Acceptance criteria

The valid fixture passes validation and broken fixtures fail with precise diagnostics.

## Open questions

None.

# Intent-Preserving Development Skills Roadmap

[Korean canonical source](../ROADMAP.md)

## Document control

- Status: active
- Last reviewed: 2026-07-18
- Working language: English translation; canonical working language: Korean

## Status vocabulary

- `planned`: Accepted future work that has not started.
- `active`: The one phase currently being executed.
- `blocked`: Accepted work that cannot progress until a named condition changes.
- `done`: Exit criteria and verification evidence are complete.
- `superseded`: Intentionally replaced by a linked phase or decision.

## Current phase

- Phase: PHASE-002
- Outcome: Evaluate only workflow stages with real usage evidence as candidates for independent Skills.

## Phases

### PHASE-001 — Harden and rename the core Skill

- Status: done
- Outcome: Strengthen the name, safety guards, validator, and evaluation system while preserving the existing Skill's intent-preservation contract.
- Dependencies: Approved implementation plan and existing `manage-project-specs` source.
- Entry criteria: The user approved complete replacement with `manage-project-intent`, personal opt-in, and a hybrid control layer.
- Exit criteria: Package, unit, behavioral, real-world project, and installation validation pass, and the documents converge on the final state.
- Verification evidence: Official package validation passed; 15 Skill tests and 3 installer tests passed; new-product forward-test, real-world project validator/Goldfish, installed Skill discovery, and exact installation passed on 2026-07-18.

Tasks:

- [x] TASK-001: Materialize the canonical project documents and fix the implementation contract.
- [x] TASK-002: Move and rename the existing Skill into the Git source and strengthen the bootstrapper, validator, and template contracts.
- [x] TASK-003: Add the synchronization tool plus repeatable unit and behavioral evaluation assets.
- [x] TASK-004: After full validation, install the new global Skill and remove the old installation.

### PHASE-003 — Publish the Skill

- Status: done
- Outcome: Publish the intent-preservation methodology and reusable Skill without private-project information.
- Dependencies: PHASE-001 completion and the approved public-upload plan.
- Entry criteria: The public repository name, MIT license, and English and Korean documentation scope were approved.
- Exit criteria: Local checks pass and the public page and remote installation from `main` are verified.
- Verification evidence: English and Korean READMEs passed fresh-agent first-use review; MIT and public GitHub `main` are available; official remote installation, official package validation, source hash comparison, anonymous README access, public hygiene checks, and English canonical-document mirror parity passed on 2026-07-18.

Tasks:

- [x] TASK-007: Implement public documentation and licensing, and publish the Skill at `seolbbb/manage-project-intent`.
- [x] TASK-008: Add English mirrors of the four live operating documents and link them directly from both READMEs.

### PHASE-004 — Make the decision-completion loop explicit

- Status: done
- Outcome: Show consistently in the Skill, public documentation, and behavioral evaluations that repeated questioning is the core loop for eliciting user intent, not a secondary step.
- Dependencies: PHASE-001 and PHASE-003 completion plus a user-confirmed need to make the interview loop more explicit.
- Entry criteria: Evidence confirms that a real Full interview used multiple rounds of consequential questions to determine intent and protected values.
- Exit criteria: The Skill, README, and evaluations express no total interview cap, route terminal states, and explicit delegation boundaries; package, unit, document validation, and installed-copy synchronization pass.
- Verification evidence: Official package validation passed; 16 Skill tests and 3 installer tests passed; canonical document validation passed with errors=0 and warnings=0; README and document local-link check passed; the installed Skill passed package validation and all 16 Skill tests; source/installed manifest was UP-TO-DATE on 2026-07-18.

Tasks:

- [x] TASK-009: Reflect the decision-completion question loop and user delegation boundary in the Skill, public documentation, and behavioral evaluations.

### PHASE-002 — Extract independently valuable intent Skills

- Status: planned
- Outcome: Split out only workflow stages whose independent invocation value is confirmed through repeated evaluation.
- Dependencies: PHASE-001 and PHASE-003 completion plus evidence of repeated independent triggers or irrelevant context loading.
- Entry criteria: At least one candidate has an independent user request and fresh-agent evaluation.
- Exit criteria: Each extracted Skill has its own trigger, contract, and tests and operates without duplication or cycles with the root router.
- Verification evidence: Not available until the phase is done.

Tasks:

- [ ] TASK-005: Evaluate the need to split `elicit-project-intent` and `audit-project-intent` using real usage records.
- [ ] TASK-006: Evaluate the `revise-project-intent`, `advance-project-intent`, and `validate-intent-handoff` candidates and the boundary with specialist Skill adapters.

## Change policy

- Change phase order only after recording the reason and downstream effects.
- Mark work done only from verification evidence.
- Keep future work here; keep only one executable Next task in `PROJECT_STATUS.md`.

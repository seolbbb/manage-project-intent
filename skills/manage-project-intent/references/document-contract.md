# Canonical document contract

Use these documents as distinct views of the project. Do not duplicate entire sections across files.

## Truth model

| Question | Source of truth |
| --- | --- |
| What does the software do now? | Code, tests, observed runtime behavior |
| What should the product do? | `PRODUCT_SPEC.md` |
| What is the intended delivery order? | `ROADMAP.md` |
| What is implemented, verified, blocked, or next? | `PROJECT_STATUS.md` |
| Why was a product or architecture choice made? | `DECISION_LOG.md` |

When sources conflict, preserve both observations, record the drift in `PROJECT_STATUS.md`, and resolve it explicitly. Never rewrite implementation history to make documents appear consistent.

Write prose in the repository's established language or the user's working language for a new project. Keep canonical filenames, structural headings, status values, and identifiers in English so deterministic validation remains portable.

## PRODUCT_SPEC.md

Own the durable target contract:

- Product definition, users, problems, goals, success criteria, and the user's underlying intent.
- Priority values, non-negotiable tradeoffs, and conditions that would justify revisiting them.
- In-scope and out-of-scope behavior.
- User flows and externally visible functional requirements.
- Safety, privacy, data, and destructive-action boundaries.
- Non-functional requirements and acceptance criteria.
- Open questions, which must be `None` or explicitly deferred before implementation.

Change this file before or with a change to intended product behavior. Do not use it as a progress checklist.

## ROADMAP.md

Own future sequencing:

- Use unique `PHASE-###` and `TASK-###` identifiers.
- Use phase states `planned`, `active`, `blocked`, `done`, or `superseded`.
- Give every phase an outcome, dependencies, entry criteria, exit criteria, and verification evidence.
- Mark a phase `done` only when its tasks are complete and evidence exists.
- Keep future candidates here rather than adding multiple Next tasks to status.

## PROJECT_STATUS.md

Own the current observed snapshot:

- Record the last verification date, current branch when useful, current phase, and observed state.
- Use project states `planning`, `active`, `blocked`, or `complete`; keep the snapshot current phase consistent with the roadmap.
- Separate Implemented, In progress, Verification evidence, Drift and gaps, and Blockers.
- Keep exactly one `## Next task` section.
- In canonical projects, the task line must start with one roadmap `TASK-###` ID and include an action.
- Include one acceptance statement and one verification command or method.
- Never claim that a historical hash remains current. Re-read Git state on resume.
- When the project is truly complete, state `None — project complete` and provide completion evidence instead of inventing work.

## DECISION_LOG.md

Own durable rationale:

- Use unique `DEC-###` headings.
- Use decision states `proposed`, `accepted`, or `superseded`.
- Record context, considered options, decision, consequences, and date.
- Record who initiated or intervened, the intent or value being protected, rejected alternatives, and the premise that would justify reconsideration.
- Record only interventions that materially change product value, UX, safety, privacy, priority, compatibility, or architecture. Keep routine wording and implementation corrections out of the permanent decision history.
- Preserve superseded decisions. Set `Superseded by` on the old decision and `Supersedes` on the replacement.
- Do not add entries for routine implementation details unless they constrain future product or architecture work.
- Treat this as a human-intent ledger, not only a technical ADR. A later agent must be able to tell which complexity or restriction is deliberate and why it must not be optimized away casually.

## AGENTS.md integration

Keep the integration small. Add the supplied marked snippet once, adapt validation commands to the repository, and preserve all existing instructions. The snippet routes future sessions to the canonical documents; it does not replace them.

## Same-task update matrix

| Change | Required document updates |
| --- | --- |
| New product or hard contract | All four documents plus `AGENTS.md` routing |
| User-visible requirement change | Product spec, affected roadmap/status, decision log when a decision changed |
| Completed roadmap task | Roadmap and project status with verification evidence |
| Routine bug or refactor | Project status only if it changes tracked progress or the current Next task |
| User intervention or superseded decision | Decision log plus every affected current document |
| Read-only status/audit | No writes |

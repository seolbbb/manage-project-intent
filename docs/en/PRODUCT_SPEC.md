# Intent-Preserving Development Skills Product Spec

[Korean canonical source](../PRODUCT_SPEC.md)

## Document control

- Status: accepted
- Last reviewed: 2026-07-18
- Working language: English translation; canonical working language: Korean

## Product intent

- Why this exists: Prevent the user's implicit intent, value judgments, and reasons for direct intervention from disappearing during implementation and session transitions, even when people use the same AI tools.
- User intent to preserve: Make consequential product decisions explicit through questions before implementation, then separate and preserve the target, current state, future sequence, and decision rationale so a later agent can continue under the same intent without chat history.
- Priority values: User-intent preservation, evidence from the actual repository, no changes before approval, session-independent handoff, and avoidance of unnecessary documentation churn.
- Non-negotiable tradeoffs: Do not make trivial work heavy, guess product/safety/privacy decisions to gain implementation speed, or overwrite the rationale behind earlier decisions.
- Reconsider these choices when: Repeatable evidence shows that another system can provide equivalent or stronger guarantees for intent, rationale, current state, and handoff at a lower operating cost.

## Product definition

`manage-project-intent` is an open-source Codex Skill that manages intent elicitation, plan approval, four canonical documents, current-state tracking, decision revision, execution from one Next task, verification, and Goldfish handoff. It delegates specialized coding, design, GitHub, and deployment procedures to installed specialist Skills while retaining the product-operations control layer.

## Users and problems

- Primary user: Individual developers, product builders, and small development teams using Codex across multiple sessions and projects.
- Problem: Intent and rationale left only in chat disappear in later sessions; target behavior and implemented behavior become mixed; and completion claims and next steps drift without verification evidence.
- Job: Ask enough questions before starting a new project, resume an existing project from its repository and documents, and preserve the reasons behind consequential human interventions for future agents.

## Goals and success criteria

- Classify an ambiguous new product as Full and make no repository changes before approval.
- Distinguish Full, Delta, and Lite work so only the necessary questions and document updates are performed.
- Separate the ownership of `PRODUCT_SPEC.md`, `ROADMAP.md`, `PROJECT_STATUS.md`, and `DECISION_LOG.md`.
- Determine current behavior from code, tests, and observed runtime results; determine target behavior from the Product Spec; preserve conflicts as drift.
- Resume sessions from exactly one verifiable Next task.
- Enable a fresh agent to reconstruct intent, protected decisions, current state, next task, and completion evidence.
- Repeatedly verify approved acceptance scenarios through unit tests and behavioral evaluations.
- Provide installable source through the official Skill installer from a public repository.
- Provide English mirrors of the four canonical documents so public users can read the actual project operating record.
- Describe benefits honestly as intended operational effects, not guaranteed productivity gains, and explain the maintenance cost and application boundaries.

## Scope

### In scope

- Keep the public GitHub repository separate from the global installed copy and provide both a new-install path and a contributor-oriented local synchronization path.
- Provide an MIT license, English and Korean READMEs, and English document mirrors under `docs/en/`.
- Maintain and strengthen the interview, document contract, lifecycle, optional Spec Kit adapter, and templates.
- Safely handle new, legacy, and partial-document states plus arbitrary working languages in the bootstrapper.
- Validate structural and semantic conflicts across roadmap, status, and decisions.
- Provide unit fixtures, fresh-agent behavioral cases, and an anonymized real-world project backtest.
- Preserve candidate Skill extractions and their entry conditions in the roadmap.

### Out of scope

- Public Plugin or Marketplace distribution, an always-on meta Skill, and automatic hooks.
- Notion, Jira, or other external issue-tracker synchronization.
- Physically splitting `elicit-*`, `audit-*`, `revise-*`, `advance-*`, or `validate-*` Skills at this stage.
- Publishing the documents, name, path, features, or decisions of any specific private project.

## User experience

- Activate automatically only for relevant requests or project opt-in signals; do not implicitly intervene in trivial questions, translations, isolated code changes, or unrelated one-off tasks.
- For Full work, investigate the repository, ask one to three consequential questions at a time, and change documents or code only after approval of a decision-complete plan.
- For Delta work, confirm only impacts within the existing contract; for Lite work, avoid permanent document churn.
- Keep `status` and `audit` read-only, and use only one Next task as the scope of `continue`.

## Functional requirements

- Skill metadata includes triggers for intent, values, reasons for intervention, long-running operations, decision changes, and drift audits, plus explicit non-triggers.
- The bootstrapper defaults to dry-run and never overwrites existing files. Applying a legacy three-document migration requires an explicit migration flag, and ambiguous partial document sets stop for audit.
- The validator checks required documents, headings, placeholders, links, IDs, Next task, phase state, completion evidence, decision supersede relationships, and project-completion conflicts.
- Preserve only consequential user interventions in the Decision Log; do not promote wording edits or routine implementation corrections into permanent decisions.
- When Spec Kit is present, use it only as the execution layer for one selected task and converge results back into the four canonical documents.
- The official Skill installer provides new installation from public `main`. The contributor synchronization tool shows differences between source and destination before requiring explicit apply.
- Keep the four Korean documents directly under `docs/` as canonical and update the English mirrors under `docs/en/` in the same change. Both languages preserve identical phase, task, and decision IDs, states, and verification evidence.

## Safety, privacy, and data

- Preserve user repositories and existing documents by default; do not automatically overwrite or migrate them.
- Keep status, audit, Goldfish, and real-world project backtests read-only.
- Do not expose the intended chat answer to a fresh agent during validation.
- Do not require or synchronize external services, credentials, or personal data.
- Do not include private-project identifiers, local paths, source data, or non-public decisions in the public repository.

## Non-functional requirements

- Keep the Skill body as a concise router and separate detailed knowledge into one-level references and executable scripts.
- Use only the Python standard library in runtime scripts and support Windows paths and UTF-8 documents.
- Commands preserve JSON output and report failure reasons with specific issue codes.
- Installation and bootstrap are repeatable and never perform unapproved deletion.
- Do not treat English mirrors as a separate source of product state or decisions; they must be structurally comparable with the canonical documents.

## Acceptance criteria

- The official Skill package validator and all unit tests pass.
- Behavioral cases exist for a new project, Delta, Lite, status/audit, continue, revise, Spec Kit present/absent, and Goldfish; representative fresh-agent runs pass.
- The anonymized real-world project backtest reports the expected compatibility result without changing the target worktree.
- The Skill installs from public `main` into a temporary Codex home and is discovered in the next fresh turn.
- The public README, MIT license, and unauthenticated access are verified.
- Both READMEs link directly to the Korean canonical source and English mirror of all four live operating documents, and both languages have matching IDs, states, and Next task.
- A repository search finds zero private-project names and personal paths.
- The source repository retains exactly one Next task and final verification evidence.

## Open questions

None.

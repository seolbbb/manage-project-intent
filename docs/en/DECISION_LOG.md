# Intent-Preserving Development Skills Decision Log

[Korean canonical source](../DECISION_LOG.md)

## Status vocabulary

- `proposed`: Recorded but not yet accepted.
- `accepted`: Currently governs product or architecture behavior.
- `superseded`: Preserved history that has been replaced by another decision.

## Decisions

### DEC-001 — Preserve user intent as a project artifact

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: Even when people use the same AI tools, user intent and value judgments are what meaningfully differentiate the result, and chat history alone cannot preserve them reliably across sessions.
- User intent/value protected: Require AI to elicit implicit intent before implementation and prevent future agents from optimizing away the user's direct interventions and tradeoff criteria at their discretion.
- Intervention: The user required the Decision Log to preserve not only technical ADRs but also why the user intervened and why a particular choice was made.
- Options considered: Preserve intent only in chat; maintain only technical ADRs; separately maintain the product contract, roadmap, current state, and a decision log of human intent.
- Decision: Maintain four canonical documents and use the Decision Log to preserve human intent and protected values as well as technical rationale.
- Consequences: Record consequential product, UX, safety, privacy, priority, and architecture interventions; exclude routine wording and implementation corrections from permanent decisions.
- Reconsider when: Another system can repeatedly replace the same guarantees for intent, rationale, state, and handoff.
- Supersedes: None
- Superseded by: None

### DEC-002 — Rename the core Skill and keep a Git source of truth

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: Editing only the global installation folder weakens change history, rollback, and future distribution, while the old name emphasizes document management less accurately than the core intent-preservation methodology.
- User intent/value protected: The Skill itself must be traceable and reproducible in the same way its project documents preserve projects.
- Intervention: The user chose the `Skill Projects` Git repository as the source, selected `manage-project-intent` as the root name, and chose not to retain an alias for the old name.
- Options considered: Edit the global installation directly; separate Git source and installed copy; keep both names active; preserve an explicit-call alias; replace completely.
- Decision: Make `skills/manage-project-intent` the Git source, install only a validated copy globally, and then remove `manage-project-specs`.
- Consequences: Installation must provide a dry run and explicit apply, and the old installation cannot be removed before the new installation is verified.
- Reconsider when: Codex provides an official development and synchronization mechanism for personal Skills with equivalent safety and version control.
- Supersedes: None
- Superseded by: None

### DEC-003 — Use project opt-in and a hybrid control layer

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: An always-on meta Skill can make trivial requests unnecessarily heavy, while reimplementing specialized coding, UI, and deployment procedures would duplicate existing Skills.
- User intent/value protected: Apply intent preservation strongly where projects need it without forcing unnecessary procedure on ordinary small requests.
- Intervention: The user chose a personal Skill collection, a hybrid control layer, project opt-in, and evidence-based staged extraction after validation improvements.
- Options considered: Automatically intervene in every development conversation; explicit invocation only; project opt-in; a complete development suite; document operations only; a hybrid control layer that connects specialist Skills.
- Decision: Activate the root Skill only for relevant requests, the AGENTS marker, or existing canonical documents, and delegate actual implementation to available specialist Skills.
- Consequences: This stage does not include an always-on hook or physical extraction of child Skills; extraction occurs only after evidence of independent triggers.
- Reconsider when: Repeated evaluations show missed automatic activation or failure to connect specialist Skills.
- Supersedes: None
- Superseded by: None

### DEC-004 — Publish an open-source Skill

- Status: accepted
- Date: 2026-07-18
- Initiated by: User
- Context: The validated personal Skill should be installable by other Codex users, but the name and details of the private project where the methodology was first used are neither the Skill's product identity nor necessary public evidence.
- User intent/value protected: Share the general intent-preservation methodology without publishing any private project's name, path, features, status, or decisions.
- Intervention: The user explicitly required publishing the Skill in a public GitHub repository with its developer intent, benefits, and usage documented, while omitting any specific private project.
- Options considered: Publish the current repository unchanged; publish a private project as a case study; distribute a project-neutral single-Skill repository; begin with a Plugin.
- Decision: Publish `seolbbb/manage-project-intent` as a public single-Skill repository under the MIT license with English and Korean READMEs. Remove private-project identifiers from the public repository and reconsider Plugin packaging when multiple independent Skills exist.
- Consequences: Public hygiene checks, installation verification from `main`, and honest explanation of benefits and limitations are publishing gates. No separate versioning or release system is added for this publication.
- Reconsider when: Multiple independent Skills emerge or direct GitHub installation repeatedly obstructs adoption and updates.
- Supersedes: None
- Superseded by: None

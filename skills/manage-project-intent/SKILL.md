---
name: manage-project-intent
description: Manage intent-preserving software project workflows by investigating before asking, repeatedly eliciting consequential user goals, values, interventions, and tradeoffs until decisions are complete, classifying Full/Delta/Lite work, enforcing plan approval, maintaining PRODUCT_SPEC.md, ROADMAP.md, PROJECT_STATUS.md, and DECISION_LOG.md, auditing drift, revising decisions, reporting status, and resuming from one concrete next task. Use for new projects, major product or architecture changes, safety/privacy/data/commercial decisions, roadmap or status work, long-running handoffs, requests to continue from repository docs, or repositories opted in through canonical documents or the managed AGENTS marker. Also use when explicitly invoked for smaller work. Do not implicitly trigger for isolated factual questions, translations, trivial fixes, or one-off implementation that does not change the product contract, roadmap, decision history, or documented Next task.
---

# Manage Project Intent

Operate the project from durable repository truth instead of chat history. Apply Intent-Preserving Development: extract the user's implicit goals and value judgments through questions, preserve them separately from implementation state, and make later agents justify any attempt to reverse them. Inspect first, make the plan decision-complete, materialize the product record before implementation, and update status with verification. Act as a hybrid control layer: route implementation, design, review, and deployment work to relevant installed specialist skills when available, while retaining ownership of intent, scope, evidence, and document convergence.

## Establish the operating context

1. Locate the project root and read applicable `AGENTS.md` files.
2. Inspect Git state, manifests, entrypoints, tests, and existing project documents before asking questions.
3. When canonical documents exist, read them in this order:
   `PRODUCT_SPEC.md` -> `PROJECT_STATUS.md` -> `ROADMAP.md` -> relevant entries in `DECISION_LOG.md`.
4. Treat code, tests, and observed runtime behavior as truth for what exists now. Treat `PRODUCT_SPEC.md` as truth for intended behavior. Record conflicts as drift in `PROJECT_STATUS.md`; never silently reconcile them.
5. Preserve user work and existing documentation. For a legacy three-document project, read it compatibly and propose migration before adding or splitting documents.
6. Treat an explicit invocation, the managed `AGENTS.md` marker, or an existing three- or four-document project record as opt-in. Do not introduce the record into an unrelated repository merely because the skill was discovered.

## Identify the intent

Support these natural-language intents; do not require command syntax:

- `start`: establish a new project with the Full workflow.
- `plan`: classify the requested change and produce the appropriate plan.
- `status`: report observed progress and drift without changing files.
- `continue`: scope work to the single concrete Next task in `PROJECT_STATUS.md`.
- `revise`: analyze a changed decision and its downstream effects before editing documents or code.
- `audit`: compare documents, repository state, and verification evidence without changing files.

## Classify the work

- **Full**: Use for a new product, a multi-milestone feature, an architecture migration, or any change to safety, privacy, stored data, licensing, pricing, or another hard product contract.
- **Delta**: Use for a bounded user-facing feature inside an existing contract or one roadmap milestone.
- **Lite**: Use for an internal bug fix, refactor, build/tooling change, or documentation correction that does not change the product contract or roadmap.
- If uncertain between tiers, choose the higher tier. Honor an explicit user tier override after stating any material risk.

Read [references/interview-playbook.md](references/interview-playbook.md) before Full interviews or when material intent is missing. Read [references/lifecycle.md](references/lifecycle.md) for the chosen workflow and lifecycle gates.

## Enforce the planning gate

For Full work:

1. Research repository truth and any current external facts that can materially affect the product.
2. Run the decision-completion interview loop: ask one to three consequential questions, record what each answer changes, identify the next material gap, and repeat. Do not impose a total-round cap. Ask about goals, success, scope, UX, safety, privacy, commercial constraints, failure behavior, value conflicts, and why the user intervenes; decide low-level implementation mechanics independently.
3. Mark every Full interview route as answered, deferred with an owner and trigger, agent-owned by explicit user delegation, or not applicable. Continue until the decision-complete checklist in the interview playbook passes.
4. When the user delegates a domain such as deployment, framework choice, or implementation mechanics, stop asking routine questions in that domain. Reopen it only when a later cross-domain conflict would change a protected product decision, and explain that conflict.
5. Present one complete `<proposed_plan>` and stop for approval. In Plan Mode, make no repository changes.
6. Treat a later request to implement the approved plan as approval to create or update the canonical documents first. Validate them before changing product code.

For Delta work, inspect the current product record, ask only about material gaps, and update only affected documents. For Lite work, make a concise plan and avoid permanent document churn unless the product contract, roadmap, accepted decision, or current Next task actually changes.

## Maintain the project record

Use `docs/PRODUCT_SPEC.md`, `docs/ROADMAP.md`, `docs/PROJECT_STATUS.md`, and `docs/DECISION_LOG.md` as the default canonical paths. Read [references/document-contract.md](references/document-contract.md) before creating, migrating, or editing them.

Write document prose in the existing repository language or, for a new project, the user's working language. Keep canonical filenames, heading contract, and `PHASE-###`/`TASK-###`/`DEC-###` identifiers in English.

- Bootstrap safely with `scripts/bootstrap_project_docs.py`. Run it without `--apply` first; it must not overwrite existing files.
- Validate with `scripts/validate_project_docs.py --root <project> --strict <full|delta|lite>`.
- Keep exactly one concrete Next task in `PROJECT_STATUS.md` and give it an acceptance condition and verification command or method.
- Update implementation status only from current evidence. Never infer completion from a roadmap checkbox alone.
- Preserve consequential user interventions, value tradeoffs, rejected alternatives, and superseded decisions. Link replacement decisions in both directions instead of rewriting history. Do not promote routine wording or implementation corrections into permanent decisions.
- Do not claim that a stored commit hash is the current HEAD. Re-observe Git state on every resume and record dated verification evidence.

## Resume and complete work

For `status`, `audit`, or `continue`, re-observe the repository even when the documents look current. If there is no single actionable Next task, stop and repair the status contract before implementation.

After implementation:

1. Run the repository's required checks.
2. Record exact verification evidence and any remaining drift or blockers.
3. Mark completed roadmap work from evidence, not intent.
4. Select exactly one new Next task that is already represented in the roadmap, unless the project is explicitly complete.
5. Update affected canonical documents in the same task as the implementation.
6. Re-run the document validator and inspect the final diff.

For Full work only, perform the Goldfish check in [references/lifecycle.md](references/lifecycle.md). A fresh subagent receives only the repository and canonical documents. Do not leak the intended answer. If it cannot reconstruct the user's intent and non-negotiable values, the project contract, current state, protected decisions, single Next task, and completion evidence, improve the documents and retry once. Do not claim Full completion after a second failure.

## Integrate Spec Kit only when present

Read [references/speckit-adapter.md](references/speckit-adapter.md) only when `.specify/` or installed `$speckit-*` skills are present, or when the user asks about Spec Kit. Keep the four canonical project documents authoritative; use Spec Kit only for feature-level specification and execution, then converge durable outcomes back into the project record.

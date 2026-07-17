# Intent-Preserving Development Skills Project Status

[Korean canonical source](../PROJECT_STATUS.md)

## Snapshot

- Last verified: 2026-07-18
- Working language: English translation; canonical working language: Korean
- Current phase: PHASE-002
- State: planning
- Repository state: `https://github.com/seolbbb/manage-project-intent` is public on `main`; re-observe Git, public access, and installed Skills on every resume.

## Implemented

- `skills/manage-project-intent` is the Git source of truth, and its frontmatter, UI metadata, AGENTS marker, and Goldfish prompt have converged on the new name.
- The Skill provides contracts for intent, values, consequential intervention, project opt-in, Full/Delta/Lite, four canonical documents, one Next task, the Spec Kit adapter, and a hybrid control layer.
- The bootstrapper provides default dry-run, no overwrite, arbitrary working languages, explicit legacy migration, and rejection of partial document sets.
- The validator checks required phase fields, current phase, project state, completion evidence, decision links and cycles, and completed-project conflicts.
- The synchronization tool compares repository source with the globally installed copy and requires an explicit apply after the default dry-run.
- Nine behavioral evaluation cases specify the multi-round Full interview, explicit delegation boundary, Delta, Lite, status/audit, continue, revise, and Goldfish contracts.
- The Full interview's repeated questioning is an explicit no-total-cap decision-completion loop, with route terminal states and the user delegation boundary converged across the Skill, public README, lifecycle, and behavioral evaluations.
- Global installation and path-free discovery of `manage-project-intent` have been verified.
- English and Korean READMEs explain the developer intent, intended benefits and limitations, four documents, work levels, installation and use, Goldfish, and the Spec Kit boundary.
- The MIT license and public GitHub `main` installation path are available.
- Complete English mirrors of the four operating documents live under `docs/en/`, and both READMEs link directly to the live documents in both languages.

## In progress

- None. PHASE-004 is complete; PHASE-002 extraction work has not started.

## Verification evidence

- Existing baseline: `uv run --with pyyaml python .../quick_validate.py .../manage-project-specs` passed on 2026-07-18.
- Existing baseline: `python -m unittest discover -s .../manage-project-specs/tests -v` passed 5 tests on 2026-07-18.
- Existing real-world project backtest: errors=0, warnings=1 (`LEGACY_THREE_DOC`) on 2026-07-18.
- Project document validation: The existing `manage-project-specs` validator passed with errors=0 and warnings=0 before implementation on 2026-07-18.
- New package validation: `quick_validate.py skills/manage-project-intent` passed on 2026-07-18.
- New deterministic tests: 15 Skill tests and 3 installer tests passed on source; the installed Skill repeated all 15 Skill tests successfully.
- New-project forward-test: A fresh agent classified the empty project as Full, made no changes, and asked exactly three consequential questions.
- Real-world project regression: The new validator reported errors=0 and the expected single `LEGACY_THREE_DOC` warning; the target worktree remained clean.
- Real-world project Goldfish: A fresh agent reconstructed intent, direct interventions, protected constraints, implemented scope, one Next task, and completion evidence without leaked answers.
- Installed discovery: A fresh agent invoked `$manage-project-intent` without a filesystem path and reconstructed this project's goal, phase, and single Next task.
- Installation: Repository and installed manifests matched; `manage-project-intent` exists and `manage-project-specs` no longer exists.
- Final self-validation: Source and installed package checks passed; the project validator passed with errors=0 and warnings=0; the installer dry-run reported UP-TO-DATE; source contained zero Python bytecode artifacts.
- Final prior safety check: The real-world backtest target remained clean and the temporary forward-test repository was removed.
- Public documentation: A fresh agent using only the two READMEs reconstructed the purpose, developer intent, benefits, limitations, installation, invocation, document contract, work levels, non-triggers, and Spec Kit boundary; its first-use ambiguities were addressed before publication.
- Public upload: `https://github.com/seolbbb/manage-project-intent` was created with `PUBLIC` visibility and `main` as the default branch.
- Remote install: The official `skill-installer` downloaded `skills/manage-project-intent` from public `main` into an isolated temporary destination; official package validation passed and `SKILL.md` matched the pushed source by SHA-256.
- Anonymous access: `https://raw.githubusercontent.com/seolbbb/manage-project-intent/main/README.md` returned HTTP 200 without an authorization header.
- Public hygiene: A repository-wide search found no blocked private-project name, local user path, GitHub token prefix, or OpenAI API key marker.
- Bilingual project record: All four English mirrors preserve the canonical phase, task, and decision identifiers, state vocabulary, Next task, and verification evidence; local links resolve from both READMEs and every document pair.
- Decision-completion loop: Official package validation passed; 16 Skill tests and 3 installer tests passed; canonical document validation reported errors=0 and warnings=0; README/document local links passed; the installed Skill passed package validation and all 16 Skill tests; source and installed manifests matched on 2026-07-18.

## Drift and gaps

- None in the completed PHASE-004 scope.

## Blockers

- None.

## Next task

- TASK-005: Evaluate whether `elicit-project-intent` and `audit-project-intent` need independent extraction by using the interview and read-only audit paths in two additional real projects.
- Acceptance: Record evidence showing whether each path has an independent user trigger and recurring dedicated instructions, then preserve the split-or-retain conclusion with its rationale.
- Verify: Compare two pairs of fresh-agent results against the existing behavioral evaluation assertions, and review the no-file-change audit evidence and question quality.

## Resume checklist

1. Read `AGENTS.md` and the four canonical project documents.
2. Re-observe Git status, the current source Skill, installed Skills, tests, and public GitHub state.
3. Compare observed behavior with the product contract and record drift.
4. Confirm that the documented Next task remains singular, actionable, and represented in the roadmap.
5. Implement only that task unless the user explicitly changes scope.
6. Run required verification and update roadmap, status, and decisions in the same task.

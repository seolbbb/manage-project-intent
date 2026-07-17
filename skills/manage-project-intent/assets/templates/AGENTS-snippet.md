<!-- manage-project-intent:start -->
## Project record and continuity

- Read `docs/PRODUCT_SPEC.md`, `docs/PROJECT_STATUS.md`, `docs/ROADMAP.md`, then relevant entries in `docs/DECISION_LOG.md` before product-behavior work.
- Treat code, tests, and observed runtime behavior as truth for current implementation; treat `PRODUCT_SPEC.md` as truth for intended behavior.
- Record conflicts as drift in `PROJECT_STATUS.md` instead of silently choosing one source.
- Keep exactly one concrete Next task with acceptance and verification details in `PROJECT_STATUS.md`.
- Preserve user interventions, protected values, rejected alternatives, and superseded decisions in `DECISION_LOG.md`.
- Update affected project documents in the same task as implementation and run the `$manage-project-intent` document validator before completion.
<!-- manage-project-intent:end -->

# Optional Spec Kit adapter

Use this adapter only when `.specify/`, Spec Kit feature artifacts, or installed `$speckit-*` skills are present, or when the user explicitly requests Spec Kit.

## Ownership boundary

- Keep `PRODUCT_SPEC.md`, `ROADMAP.md`, `PROJECT_STATUS.md`, and `DECISION_LOG.md` as the durable product layer.
- Use Spec Kit artifacts as the execution layer for one selected roadmap task or feature.
- Do not copy the entire product spec into every feature spec.
- Do not require Spec Kit for bootstrap, status, audit, resume, or document validation.

## Mapping

| Project record | Spec Kit use |
| --- | --- |
| Product principles and hard constraints | Constitution input |
| Selected roadmap task and acceptance behavior | Feature specification input |
| Approved technical approach | Plan input |
| Executable work breakdown | Tasks input |
| Cross-artifact consistency | Analyze/checklist input |
| Feature implementation | Implement input |
| Final behavior and verification | Converge back into roadmap/status/decisions |

## Workflow

1. Detect the installed commands rather than assuming command names or availability.
2. Select exactly one active `TASK-###` from `PROJECT_STATUS.md`.
3. Carry its product contract and acceptance criteria into the feature specification.
4. Run the available clarify, plan, tasks, analyze, implement, and convergence steps in their installed form.
5. After verification, merge durable requirement changes into `PRODUCT_SPEC.md`, phase/task state into `ROADMAP.md`, current evidence and Next task into `PROJECT_STATUS.md`, and new rationale into `DECISION_LOG.md`.
6. Run the project-document validator independently of Spec Kit validation.

If Spec Kit and the canonical documents disagree, stop implementation, record the drift, and resolve the product-layer decision first.

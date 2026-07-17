# Project lifecycle

## Full workflow

1. **Ground**: inspect repository, instructions, documents, Git, tests, and material external facts.
2. **Interview**: run the decision-completion loop from the interview playbook: ask one to three consequential questions per round, repeat without a total-round cap, and finish only when every material route has a terminal state.
3. **Plan**: publish one decision-complete plan and wait for approval.
4. **Materialize**: dry-run the bootstrapper, create or migrate the canonical documents, fill real content, and validate with `--strict full`.
5. **Implement**: execute only the approved milestone or single Next task.
6. **Verify**: run repository gates and collect exact evidence.
7. **Converge**: update the canonical documents in the same task, select one new Next task, validate again, and inspect the diff.
8. **Goldfish**: run the fresh-context check below.

Do not cross the Plan-to-Materialize gate without explicit approval. Do not cross the Materialize-to-Implement gate while placeholders, material open questions, or structural validation errors remain.

## Delta workflow

1. Re-read repository truth and affected documents.
2. Confirm the bounded outcome and promote to Full if a hard contract changes.
3. Produce a scoped plan and obtain normal implementation authorization.
4. Update affected canonical documents before or with code.
5. Implement, verify, converge status, and run `--strict delta`.

## Lite workflow

1. Inspect the relevant code and tests.
2. State a concise plan.
3. Implement and verify.
4. Avoid canonical document churn unless an accepted decision, roadmap state, tracked status, or Next task changed.
5. If documents exist, run `--strict lite` to detect structural damage without requiring a new documentation system.

## Status and audit workflow

Remain read-only. Re-observe Git and the relevant verification surface, compare them with all existing canonical documents, and report:

- Intended target.
- Observed implementation and verification state.
- Active roadmap phase.
- Drift, stale claims, and blockers.
- The single documented Next task and whether it is still actionable.

Never report completion solely from prose, checked boxes, or an old commit hash.

## Continue workflow

1. Read the documents and repository in the defined order.
2. Validate that exactly one Next task exists, maps to the roadmap in canonical projects, and has acceptance and verification details.
3. Re-check that the task is not already implemented or blocked by newer evidence.
4. Make that task the entire implementation scope unless the user explicitly expands it.
5. Complete repository verification and same-task document convergence.

## Revision workflow

Identify the accepted decision being changed. Reconstruct the user intent, protected value, initiating intervention, and original assumptions. Analyze affected product requirements, phases, completed implementation, compatibility, migration, and tests. Add a new decision that supersedes the old one; never edit the old choice into a different historical claim. Require a changed premise or explicit user choice before reversing a protected value.

## Goldfish validation for Full work

Launch a fresh subagent with no chat history or intended answer. Give it only the repository path, this skill path, and the instruction:

> Use `$manage-project-intent` to inspect this project from its repository and canonical documents. Without changing files, explain the user's underlying intent and priority values, direct interventions and protected decisions, product goal and audience, current implemented scope, hard safety/product constraints, exactly one Next task, and evidence required to complete it. State which decisions must not be reversed unless their recorded premise changes. List only material ambiguities that block implementation.

Pass only when the response reconstructs the requested intent, rationale, project, state, constraints, next task, and evidence; identifies real drift rather than trusting stale prose; and asks no question already answered by the repository. If it fails, repair the documents and retry once with another fresh context. After a second failure, report the documentation gap and do not claim Full completion.

For environments without subagents, mark Goldfish validation as unavailable and provide the exact prompt for a fresh task; do not silently mark it passed.

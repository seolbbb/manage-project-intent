# Interview playbook

Use this reference for Full work and for Delta work with material product ambiguity.

## Research before questions

Resolve discoverable facts first:

- Read repository instructions, manifests, schemas, tests, current documents, and Git state.
- Inspect the current implementation and verification surface.
- Research external facts only when they are current, high-impact, or explicitly requested.
- Separate observed facts, inferences, preferences, and unresolved decisions in notes.

Do not ask the user where code lives, which framework is installed, or what existing behavior does when the repository can answer it.

## Question policy

- Ask one to three questions per round.
- Use a decision-completion loop, not a fixed discovery checklist: record what each answer changes, select the next highest-impact unresolved decision, and repeat with no total-round cap.
- Prefer meaningful mutually exclusive choices with a recommended default when the interface supports them.
- Explain the user-visible or risk tradeoff in one sentence.
- Ask only questions that change the goal, user experience, scope, safety, privacy, commercial contract, rollout, or acceptance criteria.
- Decide ordinary naming, code organization, libraries, data flow, and test implementation independently, then record them in the plan.
- When the user explicitly delegates a domain to the agent, mark that route or subdecision `agent-owned` and stop asking routine questions about it. Reopen it only to resolve a stated material conflict with a protected value, contract, or acceptance condition.
- When the user rejects a premise or changes direction, mark the earlier decision as superseded rather than blending incompatible answers.
- When the user intervenes, ask what value, feared outcome, or unacceptable tradeoff motivated the intervention. Record the answer even when the resulting feature choice appears obvious.
- Distinguish an implementation preference from a protected product value. Ask what evidence or changed premise would justify revisiting a protected value.

## Interview state and stopping rule

Maintain a lightweight decision inventory during a Full interview. It is working context, not a fifth canonical document: material outcomes belong in the four canonical documents only after plan approval.

For every Full route, record one terminal state:

- `answered`: the user or repository evidence settled the outcome.
- `deferred`: the outcome may wait; record its owner and the event that reopens it.
- `agent-owned`: the user explicitly delegated the choice to the agent.
- `not applicable`: explain why the route cannot affect this product.

Do not repeat a settled question merely to seek reassurance. Return to a route only when an answer exposed a dependency, contradiction, or changed premise, and say why it is being revisited. Do not propose the plan while any material route lacks a terminal state.

## Full interview routes

Cover each route, but skip questions already answered by evidence or prior answers. A route may be answered, deferred with an owner and trigger, agent-owned through explicit delegation, or not applicable.

1. **Intent and audience**: problem, target user, primary job, why now, expected outcome, and the user's underlying reason for making the product.
2. **Success**: observable success criteria, unacceptable outcomes, measurement window when relevant.
3. **Values and tradeoffs**: convenience versus safety, speed versus quality, automation versus control, privacy versus capability, and any non-negotiable priorities.
4. **Scope**: must-have flow, explicit exclusions, supported platforms and environments.
5. **User experience**: entry point, happy path, cancellation, recovery, empty/loading/error states, accessibility.
6. **Data and trust**: inputs, storage, retention, deletion, export, privacy boundary, destructive actions, consent.
7. **Business and distribution**: pricing, licensing, account requirements, release channel, support boundary when relevant.
8. **Constraints**: compatibility, performance, offline behavior, resource limits, dependencies, legal or policy boundaries.
9. **Failure behavior**: partial failure, retry, rollback, conflict handling, auditability, operator visibility.
10. **Roadmap**: milestone order, dependencies, exit criteria, first executable slice.
11. **Acceptance**: automated tests, manual scenarios, build gates, rollout evidence, definition of done.

## Delta interview routes

Confirm only:

- Which accepted requirement or roadmap outcome changes.
- Whether the change alters a hard contract or should be promoted to Full.
- User-visible edge cases and compatibility expectations.
- Acceptance evidence and the next roadmap state.

## Decision-complete gate

Do not finalize the Full plan until all statements below are true:

- The goal, audience, and primary flow are unambiguous.
- The user's underlying intent, priority values, unacceptable tradeoffs, and direct interventions are explicit enough for a new agent to preserve them.
- In-scope and out-of-scope behavior are explicit.
- Safety, privacy, stored-data, and destructive-action boundaries are settled or explicitly not applicable.
- Interfaces, data flow, failure behavior, and compatibility are implementable without product guesses.
- Milestones have outcomes, dependencies, and exit criteria.
- Tests and manual acceptance scenarios can prove completion.
- Every Full route is answered, deliberately deferred with an owner and trigger, agent-owned through explicit user delegation, or explicitly not applicable.
- Open questions are either resolved, deliberately deferred with an owner and trigger, or blocking.
- The plan identifies which canonical documents will be created or updated before code.

If any unresolved choice would materially alter the result, keep interviewing. Do not hide it in an implementation assumption. End the interview from decision coverage, not from a question count or conversational fatigue.

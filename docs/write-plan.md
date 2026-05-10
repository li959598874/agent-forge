# Write Plan

Write Plan creates a decision-complete Markdown plan before implementation starts. It is an explicit planning workflow: the user asks for a plan, the agent grounds itself in the available environment, resolves intent and implementation decisions, then writes a local plan artifact that another engineer or agent can execute without hidden chat context.

Use it when a task is broad, ambiguous, risky, cross-cutting, or needs agreement before source files change. Skip it for small direct edits, quick answers, or work the user has already asked you to implement immediately.

## Invocation

Invoke the skill explicitly in Codex-compatible environments:

```text
$write-plan "Plan the authentication refactor before editing files"
```

Natural-language constraints are part of the request:

```text
$write-plan "Plan the billing export change. Keep compatibility risks visible."
```

For larger work, ask for the depth you need in the task text:

```text
$write-plan "Create a decision-complete plan for the plugin release process. Inspect local docs and manifests first."
```

## Behavior Contract

Write Plan separates planning from execution:

1. Explore relevant local context with non-mutating actions.
2. Resolve discoverable facts from files, configs, schemas, tests, logs, and current implementation.
3. Ask only questions that materially change the plan, confirm an important assumption, or choose between real tradeoffs.
4. Define the implementation shape clearly enough to execute: scope, success criteria, key changes, interfaces, data flow, edge cases, tests, rollout, and compatibility constraints when relevant.
5. Write one local Markdown plan artifact.
6. Reply briefly with the plan path and any essential caveat.

Except for creating or updating the plan artifact, the workflow does not edit repo-tracked files, apply patches, run formatters that rewrite files, perform migrations, or execute the implementation.

## Exploration Rules

Start with targeted inspection unless no local environment is available or the request itself is contradictory. Prefer reading the repository over asking the user for facts the environment can answer.

Discoverable facts include paths, existing APIs, schemas, config values, test layout, dependency choices, and current behavior. If multiple plausible answers remain after inspection, ask with concrete candidates and a recommended default.

Preferences and tradeoffs are different. Ask early when the answer depends on user intent, such as compatibility policy, acceptable migration cost, rollout risk, UX priority, or which constraint matters most.

## Plan Artifact

Write the plan in the user's current conversation language. Before writing, check whether a relevant local plan already exists. If one does, ask whether to refine the existing plan or start a fresh one.

Default path:

```text
.agent-work/plan-<short-slug>.md
```

Choose a short lowercase hyphenated slug from the work, such as `auth-timeout`, `checkout-copy`, or `dash-counter`.

Use this base shape unless the task needs extra sections:

```markdown
# <Clear Title>

## Summary
- <Goal, success criteria, current state, and intended outcome>

## Key Changes
- <Implementation changes grouped by subsystem or behavior>
- <Important API, interface, type, data shape, or I/O changes>

## Test Plan
- <Tests, manual acceptance scenarios, and validation commands>

## Assumptions
- <Assumptions, defaults, and unresolved but accepted constraints>
```

Optional sections such as `Risks`, `Edge Cases`, `API / Data Shape`, or `Migration / Compatibility` are useful when they prevent execution mistakes. Keep the plan compact and execution-ready: group by behavior, name exact paths or symbols only when needed, and avoid inventing policy that the user did not request.

## Composition

Write Plan is an upstream workflow primitive. It produces a durable local plan that a human, the base agent, or another workflow skill can execute later. Other skills should treat the plan as context, not as permission to make changes outside the user's request.


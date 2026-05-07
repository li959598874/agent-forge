# Markdown Plan Contract

## Artifact Rule

RalPlan writes one final artifact:

```text
.agent-work/plans/<slug>/plan.md
```

Use `--dir` to replace `.agent-work`. Use `--name` to replace `<slug>`.

## File Naming

Use a lowercase hyphenated slug:

- Prefer `--name` when supplied.
- Otherwise derive from the task in 2-6 words.
- Avoid dates in the slug unless needed to disambiguate.
- If `plan.md` already exists, do not overwrite silently. Ask whether to replace it or choose a new slug.

## Required Sections

Use `assets/plan-template.md` as the starting structure. Keep the final plan concise but complete enough for a future agent to execute without relying on hidden chat context.

Required sections:

1. Task
2. Goals
3. Non-Goals
4. Evidence
5. Decisions
6. Assumptions
7. Execution Slices
8. Validation
9. Risks And Rollback
10. Open Questions
11. Intent Drift Check

## Execution Slice Rules

Each slice should be independently understandable:

- Give a short title.
- State the objective.
- List likely files or areas.
- Define completion criteria.
- Include validation for that slice when known.

Do not over-specify every shell command unless the command is central to correctness. RalPlan plans work; execution skills decide exact implementation mechanics.

## Evidence Rules

Record facts and sources that shaped the plan:

- Local files read, with relevant paths.
- Commands run for discovery.
- Official docs or primary sources, when used.
- Clear labels for inference versus directly observed fact.

This section replaces the need for a separate machine-readable handoff.

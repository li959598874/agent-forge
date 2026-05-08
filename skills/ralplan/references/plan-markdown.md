# Markdown Plan Contract

## Artifact

Write one file: `.agent-work/plans/<slug>/plan.md`. `--dir` replaces `.agent-work`; `--name` replaces `<slug>`. If it exists, ask whether to replace it or choose a new slug.

## Required Sections

Use `assets/plan-template.md`. Keep the plan concise and executable without hidden chat context.

Required headings: Task, Process Budget, Goals, Non-Goals, Evidence, Decisions, Assumptions, Execution Slices, Validation, Risks And Rollback, Open Questions, Intent Drift Check.

## Execution Slice Rules

Each slice needs a title, objective, touchpoints, completion criteria, and known validation. Avoid shell commands unless central to correctness.

## Evidence Rules

Record shaping facts: local files, discovery commands, official docs or primary sources, and inference labels. This replaces a separate handoff.

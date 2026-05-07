# RalPlan

RalPlan is a planning skill for turning ambiguous software or workflow requests into an approved Markdown execution plan. It is intentionally narrow: it clarifies, plans, and writes a plan file after approval. It does not implement code, perform final review, commit changes, or create parallel JSON handoff files.

## Skill Location

```text
skills/ralplan/
  SKILL.md
  agents/openai.yaml
  references/workflow.md
  references/plan-markdown.md
  assets/plan-template.md
```

## When To Use

Use RalPlan when a task needs planning before implementation:

- The requirement is ambiguous or underspecified.
- Scope boundaries, non-goals, or acceptance criteria need to be clarified.
- The task may touch multiple files, modules, systems, or workflow phases.
- The user wants a durable plan artifact for future execution.
- The user invokes `$ralplan` directly.

Do not use RalPlan when the user is asking for immediate implementation, a final code review, a commit, or a purely informational answer.

## Invocation

RalPlan supports CLI-style options while also accepting natural-language instructions and inferred intent.

```text
$ralplan [--scale auto|tiny|small|medium|large]
         [--depth auto|lite|standard|deep]
         [--agents off|auto|on]
         [--research off|auto|on]
         [--dir .agent-work]
         [--name <slug>]
         "<task>"
```

Example:

```text
$ralplan --scale medium --depth standard --agents auto --name auth-refactor "Plan the authentication refactor"
```

Natural-language examples are also valid:

```text
$ralplan Keep this lightweight and do not use subagents. Plan how to clean up the logging module.
```

```text
$ralplan Do a deep architecture plan and check latest official docs before drafting the migration plan.
```

## Option Normalization

The first workflow step is to normalize options from three sources:

1. Structured CLI-style flags.
2. Explicit natural-language preferences.
3. Implied intent from the task.

The skill must echo the normalized options before continuing:

```text
Normalized RalPlan options:
- scale: medium (inferred from cross-module scope)
- depth: standard (natural language requested a normal plan)
- agents: auto (default)
- research: off (no current external facts requested)
- dir: .agent-work (default)
- name: auth-refactor (derived)
```

Structured flags have the highest priority, followed by explicit natural language, then inferred intent, then defaults. If an inferred option materially affects the process and is uncertain, the agent should ask before proceeding.

## Options

### `--scale`

Controls planning size and artifact richness.

- `auto`: infer from the task.
- `tiny`: local, low-risk, easily reversible task.
- `small`: narrow task with limited uncertainty.
- `medium`: cross-file or cross-module planning with meaningful ambiguity.
- `large`: architecture, migration, multi-phase, or high-risk planning.

### `--depth`

Controls interview detail.

- `auto`: infer from task complexity and requirement detail.
- `lite`: ask only blocking questions.
- `standard`: ask enough to freeze scope and acceptance.
- `deep`: probe goals, non-goals, alternatives, risks, rollout, and validation.

### `--agents`

Controls optional read-only subagent exploration.

- `off`: do not use subagents.
- `auto`: use subagents only when the task benefits from context isolation.
- `on`: use subagents when the active environment supports them.

Subagents are for read-heavy exploration only. RalPlan does not delegate write tasks.

### `--research`

Controls external research.

- `off`: do not browse or use external sources.
- `auto`: research only when needed for correctness.
- `on`: use external research, preferring official documentation and primary sources.

### `--dir`

Sets the scratch directory for the final plan. The default is:

```text
.agent-work
```

### `--name`

Sets the plan slug. If omitted, RalPlan derives a lowercase hyphenated slug from the task.

## Workflow

RalPlan always follows the write flow:

1. Normalize options and echo them in the conversation.
2. Ground minimally by reading project instructions, top-level structure, manifests, test entry points, and directly relevant files.
3. Classify task complexity using change surface, ambiguity, failure cost, and validation width.
4. Assess how detailed the user's requirement already is.
5. Ask only unresolved clarification questions.
6. Draft the plan in the conversation.
7. Wait for user approval.
8. Write the final Markdown plan.
9. Report the plan path and remaining assumptions or validation gaps.

If the user says "just draft" or "do not write yet", RalPlan should stop before the approval/write step for that turn. This is not a separate mode option.

## Interview Depth

Interview depth depends on both task complexity and requirement detail.

Requirement detail levels:

- `high detail`: the user already supplied goals, non-goals, constraints, acceptance criteria, relevant files, and preferred tradeoffs.
- `medium detail`: the user supplied a clear goal and some constraints, but acceptance, risks, or boundaries are incomplete.
- `low detail`: the user supplied intent but not scope, success criteria, constraints, or authorization.

Question volume should be proportional:

| Scale | Typical Questions |
| --- | --- |
| `tiny` | 0-2 |
| `small` | 1-3 |
| `medium` | 2-5 |
| `large` | staged interview batches |

This is a ceiling, not a quota. A large task with high-detail requirements should not receive a ceremonial long interview. A small task with low-detail requirements still needs boundary and acceptance questions before drafting.

## Subagent Policy

Use subagents only when the active environment allows them and they materially help preserve main-context quality.

Default behavior:

- `tiny` and `small`: no subagents.
- `medium`: at most one read-only explorer.
- `large`: consider repo exploration, official-doc research, and a critic pass.

Subagents should return concise facts, evidence, file paths, source links, risks, and confidence. The main agent owns synthesis and all user communication.

## Plan Artifact

RalPlan writes one final artifact:

```text
.agent-work/plans/<slug>/plan.md
```

Use `--dir` to change `.agent-work`. Use `--name` to change `<slug>`.

RalPlan does not create:

- `plan.json`
- handoff JSON
- state JSON
- `.gitignore`

Both humans and future agents should read the same Markdown file.

If the target `plan.md` already exists, the agent must not overwrite it silently. It should ask whether to replace the file or choose a new slug.

## Plan Sections

The final plan should follow `skills/ralplan/assets/plan-template.md` and include:

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

The Evidence section is important. It records local files read, commands run for discovery, official docs or primary sources used, and whether a statement is observed fact or inference. This replaces any separate machine-readable handoff.

## Development Notes

The skill is validated with the system skill-creator validator:

```bash
python3 /home/liwb/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/ralplan
```

When changing RalPlan, keep `SKILL.md` concise. Put detailed workflow rules in `references/`, and keep user-facing documentation in this file.

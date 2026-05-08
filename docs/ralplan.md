# RalPlan

RalPlan is a planning skill for turning ambiguous software or workflow requests into an approved Markdown execution plan. It is intentionally narrow: it clarifies, plans, and writes one plan file after user approval. It does not implement code, perform final review, commit changes, or create parallel JSON handoff files.

RalPlan is the first Agent Forge workflow primitive. It applies the project principle documented in [design-principles.md](design-principles.md): use only as much process as the task warrants.

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

Use RalPlan only when the user explicitly asks for planning:

- The user invokes `$ralplan` directly.
- The user clearly asks to create a plan before implementation.
- The user clearly asks for a durable plan artifact for future execution.

Do not use RalPlan for general clarification, immediate implementation, a final code review, a commit, or a purely informational answer.

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

Examples:

```text
$ralplan --scale small --depth lite --agents off "Plan a logging cleanup"
```

```text
$ralplan --scale medium --depth standard --agents auto --name auth-refactor "Plan the authentication refactor"
```

```text
$ralplan --scale large --depth deep --agents on "Plan the plugin release process"
```

Natural-language controls are valid:

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
- research: on (default)
- dir: .agent-work (default)
- name: auth-refactor (derived)
```

Structured flags have the highest priority, followed by explicit natural language, inferred intent, and defaults. If an inferred option materially affects the process and is uncertain, the agent should ask before proceeding.

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

Controls whether read-only subagent exploration is allowed.

- `off`: do not use subagents.
- `auto`: let the agent decide from task facts; stay local when local grounding is enough.
- `on`: use subagents as the preferred exploration path for broad or read-heavy work.

When enabled, RalPlan organizes read-only exploration around independent evidence lanes such as modules, repositories, architecture layers, source types, risks, or critic passes. With `on`, the main agent should fan out useful lanes before drafting and preserve its own context for synthesis. RalPlan does not delegate write tasks.

### `--research`

Controls research-backed evidence lanes. Default: `on`.

- `off`: do not browse or use external sources.
- `auto`: let the agent decide whether source checks are needed.
- `on`: keep source checks available, preferring official documentation and primary sources.

Research usually runs inside subagent exploration. If subagents are unavailable, the main agent may perform the minimum required source checks and record sources in Evidence.

### `--dir`

Sets the scratch directory for the final plan. The default is:

```text
.agent-work
```

### `--name`

Sets the plan slug. If omitted, RalPlan derives a lowercase hyphenated slug from the task.

## Workflow

RalPlan always follows the approval-gated write flow:

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

- `off`: no subagents.
- `auto`: the agent decides from task evidence; `tiny` and `small` usually stay local, while broader work can split into evidence lanes.
- `on`: broad or read-heavy discovery is subagent-first, split by module, subsystem, source type, risk area, official-doc research, or critic pass.

Subagents should return concise facts, evidence, file paths, source links, risks, and confidence. The main agent preserves context quality, owns synthesis, and handles all user communication.

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
2. Process Budget
3. Goals
4. Non-Goals
5. Evidence
6. Decisions
7. Assumptions
8. Execution Slices
9. Validation
10. Risks And Rollback
11. Open Questions
12. Intent Drift Check

The Evidence section is important. It records local files read, commands run for discovery, official docs or primary sources used, and whether a statement is observed fact or inference. This replaces any separate machine-readable handoff.

## Development Notes

Validate repository and skill packaging with:

```bash
python3 scripts/validate.py
```

If you use an external Codex skill validator, run it according to that validator's own installation path.

When changing RalPlan, keep `SKILL.md` concise. Put detailed workflow rules in `references/`, and keep user-facing documentation in this file.

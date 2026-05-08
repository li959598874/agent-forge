# Plan

Plan is a planning skill for turning ambiguous software or workflow requests into an approved Markdown execution plan. It is intentionally narrow: it clarifies, drafts, waits for confirmation, and upgrades one local Markdown file into an execution plan. It does not implement code, perform final review, commit changes, or create parallel JSON handoff files.

Plan is the first Agent Forge workflow primitive. It applies the project principle documented in [design-principles.md](design-principles.md): use only as much process as the task warrants.

## Skill Location

```text
skills/plan/
  SKILL.md
  agents/openai.yaml
```

## When To Use

Use Plan only when the user explicitly asks for planning:

- The user invokes `$plan` directly.
- The user clearly asks to create a plan before implementation.
- The user clearly asks for a durable plan artifact for future execution.

Do not use Plan for general clarification, immediate implementation, a final code review, a commit, or a purely informational answer.

## Invocation

Plan supports preset flags while also accepting natural-language instructions and inferred intent.

```text
$plan [--low|-l|--medium|-m|--high|-h|--max|-x] "<task>"
```

Examples:

```text
$plan --low "Plan a logging cleanup"
```

```text
$plan -m "Plan the authentication refactor"
```

```text
$plan --high "Plan the plugin release process"
```

```text
$plan -x "Plan this architecture migration"
```

Natural-language controls are valid:

```text
$plan Keep this lightweight and do not use subagents. Plan how to clean up the logging module.
```

```text
$plan Create a deep plan for the plugin release process and use subagents for broad exploration.
```

## Preset Normalization

The first workflow step is to normalize the preset from:

1. Structured preset flags.
2. Explicit natural-language preferences.
3. Implied intent from the task.
4. The agent's intelligent default.

The skill must echo the normalized preset before continuing:

```text
Normalized Plan preset:
- preset: medium (inferred from cross-module scope)
```

If the user does not provide a preset, the agent decides. If an inferred choice materially affects process and is uncertain, the agent asks before continuing.

## Presets

| Preset | Short | Purpose |
| --- | --- | --- |
| `--low` | `-l` | Minimal local grounding and only blocking questions. |
| `--medium` | `-m` | Standard planning for normal feature, cleanup, or cross-file work. |
| `--high` | `-h` | Deeper exploration, staged clarification, and read-only subagents when available. |
| `--max` | `-x` | Broad exploration, read-only multi-agent research/critic lanes when available, and deep confirmation. |

Presets are process ceilings, not quotas. A detailed high-risk request can still move quickly, and a small vague task may still need one or two boundary questions.

## Workflow

Plan follows an approval-gated draft-to-plan flow:

1. Normalize the preset and echo it in the conversation.
2. Ground by reading project instructions, structure, manifests, test entry points, and directly relevant files.
3. Ask only unresolved clarification questions.
4. Write a draft artifact with `Status: Draft`.
5. Report a short draft summary, path, and decisions needing confirmation.
6. Wait for user confirmation or revisions.
7. Upgrade the same Markdown file to `Status: Execution Plan`.
8. Report the plan path and remaining assumptions or validation gaps.

If the user says "just draft" or "do not write yet", Plan should stop before the upgrade step for that turn.

## Clarification Questions

Questions must be clear enough that the user is not forced to choose without understanding the tradeoff. Each question needs:

- A clear question text.
- Meaningful option labels.
- A one-sentence option description.
- A way for the user to provide their own answer.

When the host provides `request_user_input`, use it and rely on its free-form option. In plain text, include an explicit `User-provided answer` option.

## Plan Artifact

Plan writes one artifact:

```text
.agent-work/plans/<slug>/plan.md
```

The slug is derived automatically from the task. If the path already exists, Plan chooses a safe suffix unless the user clearly asks to continue that existing draft.

Every artifact uses a stable shell:

- `Status: Draft` or `Status: Execution Plan`

Plan does not create:

- `draft.md`
- `plan.json`
- handoff JSON
- state JSON
- `.gitignore`

Both humans and future agents should read the same Markdown file.

## Adaptive Content

Plan does not require fixed body headings. The agent should choose readable Markdown structure based on the task and preset.

Draft content must cover requirement description, key decisions, suggestions or tradeoffs, open questions, and the confirmation gate.

Execution plan content must cover goals and non-goals, confirmed decisions and assumptions, execution approach, validation, risks and rollback where relevant, open questions or `None`, and an intent drift check.

## Development Notes

Validate repository and skill packaging with:

```bash
python3 scripts/validate.py
```

If you use an external Codex skill validator, run it according to that validator's own installation path.

When changing Plan, keep the core prompt in `SKILL.md`. Do not split workflow rules or artifact rules into extra files unless the prompt becomes too large to maintain safely.

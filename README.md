# Agent Forge

[中文说明](README.zh-CN.md)

Agent Forge explores a lighter way to orchestrate agents. Instead of forcing every request through a heavy planning or delegation pipeline, it gives the user explicit controls for how much process a task should receive while still allowing the agent to make sensible default decisions.

The goal is simple: small tasks should stay small, and complex tasks should have a clear path to deeper clarification, research, and read-only exploration when that extra structure is useful.

The repository contains Codex-compatible workflow assets for turning ambiguous requests into approved Markdown execution plans, with the main orchestration choices exposed directly:

- task scale
- clarification depth
- subagent usage
- external research

## Quick Start

From a local checkout, inspect the available assets:

```bash
cd agent-forge
find skills -maxdepth 2 -type f
```

Current assets:

| Asset | Type | Description |
| --- | --- | --- |
| [ralplan](skills/ralplan/SKILL.md) | Skill | Clarifies ambiguous tasks and produces an approved Markdown execution plan with explicit complexity controls. |

## Using RalPlan

Invoke the skill explicitly in Codex-compatible environments:

```text
$ralplan --scale medium --depth standard --name auth-refactor "Plan the authentication refactor"
```

RalPlan always follows the same flow:

1. Normalize structured options, natural-language preferences, and inferred intent.
2. Gather minimal project context.
3. Ask only the clarification questions still needed.
4. Draft the plan in the conversation.
5. Write the final Markdown plan after user approval.

Its control surface is intentionally small:

- `--scale auto|tiny|small|medium|large`: controls how much planning surface the agent assumes.
- `--depth auto|lite|standard|deep`: controls how much clarification the agent performs.
- `--agents off|auto|on`: controls whether read-only subagent exploration is allowed.
- `--research off|auto|on`: controls whether external research is allowed.

This keeps lightweight tasks from being forced through a heavy process while still allowing deeper orchestration when the task warrants it.

Read the complete guide in [docs/ralplan.md](docs/ralplan.md).

## Repository Layout

```text
skills/
  ralplan/          # RalPlan workflow skill
docs/
  ralplan.md        # Human-facing guide for the ralplan skill
```

## Extension Points

This repository is intended to grow incrementally. Planned categories:

- `skills/`: reusable Codex skills with `SKILL.md`, optional references, templates, and UI metadata.
- `hooks/`: future lifecycle hooks or automation entry points.
- `agents/`: future reusable agent role prompts and coordination patterns.
- `docs/`: human-facing usage guides and design notes.

Keep new additions scoped and documented. Prefer one focused asset over a broad framework.

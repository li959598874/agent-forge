# Agent Forge

[中文说明](README.zh-CN.md)

Agent Forge is a workspace for crafting reusable agent workflow assets: skills, hooks, agent roles, templates, and workflow documentation.

The project keeps each capability small, explicit, and verifiable. A workflow asset should have a clear entry point, a narrow responsibility boundary, and enough documentation for both human users and future agents to use it without hidden context.

## Quick Start

From a local checkout, inspect the available assets:

```bash
cd agent-forge
find skills -maxdepth 2 -type f
```

Current assets:

| Asset | Type | Description |
| --- | --- | --- |
| [ralplan](skills/ralplan/SKILL.md) | Skill | Clarifies ambiguous tasks and produces an approved Markdown execution plan. |

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

Read the complete guide in [docs/ralplan.md](docs/ralplan.md).

## Repository Layout

```text
skills/
  ralplan/          # First workflow skill in this repository
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

# Agent Forge

[中文说明](README.zh-CN.md)

Agent Forge is a Codex-first plugin for user-controlled, low-intrusion, composable multi-agent workflow orchestration through skills. It provides workflow primitives that users can invoke, combine, and ignore independently instead of forcing every request through one fixed process.

The guiding rule is simple: users control the workflow, skills stay composable, and agent orchestration should add structure only when it improves the result.

## Why This Exists

Existing agent orchestration workflows can be useful, but they often force every request through a fixed process. That creates avoidable token cost, adds ceremony to small tasks, and can interfere with a user's existing skills or local workflow.

Agent Forge is built around four constraints:

- **User-controlled flow**: workflows are explicit skills, not hidden interception rules.
- **Low intrusion**: the plugin ships skills and documentation without changing hooks, global config, or unrelated tools.
- **Composable skills**: each skill should solve one workflow problem and remain usable alongside the user's own skills.
- **Multi-agent orchestration**: subagents are optional lanes for exploration, risk review, tests, docs research, or future workflow roles when the task benefits from parallel context.

## Current Status

This repository currently publishes one plugin and one skill:

| Asset | Purpose |
| --- | --- |
| `agent-forge` plugin | Codex plugin wrapper for Agent Forge workflow assets. |
| `$write-plan` skill | Creates decision-complete Markdown plans before implementation starts. |

Write Plan is the current workflow primitive. Future workflow assets should follow the same contract: explicit invocation, low default ceremony, clean composition with other skills, and no surprise changes outside the requested scope.

## Install

Add this GitHub repository as a Codex plugin marketplace:

```bash
codex plugin marketplace add li959598874/agent-forge --ref main
```

Then open Codex and install Agent Forge from the plugin directory:

```text
/plugins
```

Select the `Agent Forge` marketplace, open the `agent-forge` plugin, and choose `Install plugin`.

After a stable release tag exists, prefer a pinned release ref instead of `main`:

```bash
codex plugin marketplace add li959598874/agent-forge --ref <release-tag>
```

## Quick Start

Invoke Write Plan explicitly in Codex-compatible environments:

```text
$write-plan "Plan the authentication refactor before editing files"
```

Natural-language constraints are part of the request:

```text
$write-plan "Plan the logging cleanup. Keep compatibility risks visible."
```

For broader work, ask for the necessary planning depth in the task text:

```text
$write-plan "Create a decision-complete plan for the plugin release process. Inspect local docs and manifests first."
```

Write Plan saves one local Markdown artifact:

```text
.agent-work/plan-<short-slug>.md
```

## Workflow

Write Plan keeps planning separate from implementation:

1. Explore the local environment without mutating source files.
2. Ask only questions that change the plan, confirm important assumptions, or choose between real tradeoffs.
3. Specify the implementation shape clearly enough for another engineer or agent to execute.
4. Save a decision-complete Markdown plan.
5. Reply briefly with the plan path and any essential caveat.

Read the complete Write Plan guide in [docs/write-plan.md](docs/write-plan.md). The design principles are documented in [docs/design-principles.md](docs/design-principles.md).

## Repository Layout

```text
.agents/
  plugins/
    marketplace.json        # GitHub marketplace entry for Agent Forge
.codex-plugin/
  plugin.json               # Codex plugin manifest
.github/
  ISSUE_TEMPLATE/           # GitHub issue forms
  workflows/validate.yml    # Repository validation workflow
docs/
  design-principles.md      # Workflow philosophy and guardrails
  design-principles.zh-CN.md
  write-plan.md             # English Write Plan guide
  write-plan.zh-CN.md       # Chinese Write Plan guide
scripts/
  validate.py               # Repo-local validation checks
skills/
  write-plan/               # Write Plan workflow skill
```

## Development

There is no compiled build step. Validate repository structure, manifests, docs, and skill contracts with:

```bash
python3 scripts/validate.py
```

The repo-local validator includes skill packaging checks. If you use an external Codex skill validator, run it according to that validator's own installation path.

Also run:

```bash
git diff --check
```

For local plugin development and debugging, use the cross-platform workflow in [docs/local-plugin-development.md](docs/local-plugin-development.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening issues or pull requests. Public behavior changes should update both English and Chinese docs when applicable.

## License

Agent Forge is released under the [MIT License](LICENSE).

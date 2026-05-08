# Agent Forge

[中文说明](README.zh-CN.md)

Agent Forge is a Codex-first workflow plugin for adaptive agent orchestration. It gives users explicit control over how much process a task receives, while still allowing Codex to make conservative default decisions when the user leaves the process budget implicit.

The guiding rule is simple: small tasks should stay small; complex work should have a clear path into deeper clarification, research-backed read-only exploration, and durable local planning.

## Why This Exists

Existing agent orchestration workflows can be useful, but they often force every request through a heavy process. That creates avoidable token cost, adds ceremony to small tasks, and can interfere with a user's existing skills or local workflow. Codex plan mode is intentionally lightweight, but its plan artifact is not written into the repository by default.

Agent Forge is built around three constraints:

- **Explicit process budget**: users can choose a planning preset that controls exploration, clarification depth, subagent use, and research-backed investigation.
- **Adaptive defaults**: when no preset is provided, the agent escalates process only when task evidence justifies it.
- **Low intrusion**: the plugin ships skills and documentation without changing user hooks, global config, or unrelated tools.

## Current Status

This repository currently publishes one plugin and one skill:

| Asset | Purpose |
| --- | --- |
| `agent-forge` plugin | Codex plugin wrapper for Agent Forge workflow assets. |
| `$plan` skill | Clarifies ambiguous tasks, writes a draft, and upgrades it to an approved Markdown execution plan. |

Plan is the first workflow primitive. Future workflow assets should follow the same contract: explicit controls, minimal default ceremony, local artifacts when persistence matters, and no surprise changes outside the requested scope.

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

Invoke Plan explicitly in Codex-compatible environments:

```text
$plan --medium "Plan the authentication refactor"
```

For lightweight tasks, reduce the process budget:

```text
$plan --low "Plan the logging cleanup"
```

Or:

```text
$plan Keep the logging cleanup lightweight and do not use subagents.
```

For architecture or migration work, let the workflow use deeper clarification and official sources:

```text
$plan --high "Plan the plugin release process"
```

Or:

```text
$plan Create a deep plan for the plugin release process and use subagents for broad exploration.
```

Plan writes a draft first, then upgrades the same file after user approval:

```text
.agent-work/plans/<slug>/plan.md
```

## Controls

| Option | Short | Purpose |
| --- | --- | --- |
| `--low` | `-l` | Minimal local grounding, no subagents by default, and only blocking questions. |
| `--medium` | `-m` | Standard planning for normal feature, cleanup, or cross-file work. |
| `--high` | `-h` | Deeper exploration, staged clarification, and read-only subagents when useful. |
| `--max` | `-x` | Broad exploration, multi-agent research/critic lanes when available, and deep confirmation. |

Read the complete Plan guide in [docs/plan.md](docs/plan.md). The design principles are documented in [docs/design-principles.md](docs/design-principles.md).

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
  plan.md                   # English Plan guide
  plan.zh-CN.md             # Chinese Plan guide
scripts/
  validate.py               # Repo-local validation checks
skills/
  plan/                     # Plan workflow skill
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

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening issues or pull requests. Public behavior changes should update both English and Chinese docs when applicable.

## License

Agent Forge is released under the [MIT License](LICENSE).

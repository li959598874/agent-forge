# Repository Guidelines

## Project Structure & Module Organization

This repository is a single-plugin GitHub marketplace for Codex-compatible workflow assets and their human-facing documentation.

- `README.md` and `README.zh-CN.md`: top-level project introductions.
- `.agents/plugins/marketplace.json`: marketplace manifest used by `codex plugin marketplace add`.
- `.codex-plugin/plugin.json`: plugin manifest for the root Agent Forge plugin.
- `docs/`: user guides and design notes.
- `skills/`: the skill package.

## Build, Test, and Development Commands

There is no compiled build step or package-managed test suite at present. Use lightweight repository checks:

```bash
find .agents .codex-plugin skills -maxdepth 4 -type f
```

Lists current marketplace, plugin, and skill files for a quick structure check.

```bash
rg "agent-forge|Agent Forge|ralplan|RalPlan" README.md README.zh-CN.md docs skills .agents .codex-plugin
```

Verifies that documentation, marketplace metadata, plugin metadata, and skill references stay aligned after edits.

```bash
git diff --check
```

Detects trailing whitespace and whitespace errors before commit.

## Coding Style & Naming Conventions

Write Markdown in concise, instructional prose. Use sentence-case paragraphs, fenced code blocks with language hints where helpful, and relative links such as `docs/ralplan.md`. Keep skill directories lowercase and hyphenated when needed, for example `skills/my-skill/`. Preserve bilingual pairing when changing public docs: update both English and Chinese files when the change affects shared user-facing behavior.

## Testing Guidelines

For documentation changes, manually inspect rendered Markdown and run `git diff --check`. For marketplace or plugin manifest changes, validate JSON formatting and confirm the marketplace entry still points at the intended GitHub repository and ref. For skill contract changes, review `skills/<name>/SKILL.md` together with any files under `references/` and `assets/` so the workflow, examples, and final artifact format agree. Name future tests after the behavior they validate if an automated suite is added.

## Plugin Distribution Workflow

Keep this repository as a single-plugin GitHub marketplace unless a future change explicitly introduces multiple plugins. The marketplace manifest should continue to expose the root plugin through `source.source: "url"` and the public repository URL.

Public install instructions should use:

```bash
codex plugin marketplace add li959598874/agent-forge --ref main
```

After a stable release tag exists, prefer a version tag such as `v0.1.0` and update both `.agents/plugins/marketplace.json` and public documentation when the recommended ref changes.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries, for example `Update project README introduction`. Follow that style: start with a verb and describe the changed asset or behavior.

Pull requests should include a brief summary, changed paths, validation performed, and any user-facing behavior changes. Link related issues when available. Add screenshots only for rendered documentation or UI-visible changes.

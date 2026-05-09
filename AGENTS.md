# Repository Guidelines

## Project Structure & Module Organization

This repository is a single-plugin GitHub marketplace for Codex-compatible workflow assets and human-facing documentation.

- `README.md` and `README.zh-CN.md`: top-level bilingual introductions.
- `.agents/plugins/marketplace.json`: marketplace manifest used by `codex plugin marketplace add`.
- `.codex-plugin/plugin.json`: root Agent Forge plugin manifest.
- `docs/`: user guides, design principles, and bilingual behavior docs.
- `skills/`: Codex skill packages. The current skill is `skills/plan/`.
- `scripts/validate.py`: repo-local validation for manifests, docs, and skill packaging.
- `.github/`: issue templates, pull request template, and CI validation workflow.

## Build, Test, and Development Commands

There is no compiled build step or package-managed test suite. Use lightweight repository checks:

```bash
python3 scripts/validate.py
```

Validates required files, JSON manifests, Plan packaging, bilingual docs, and trailing whitespace.

```bash
find .agents .codex-plugin skills docs scripts .github -maxdepth 4 -type f
```

Lists marketplace, plugin, skill, docs, validation, and GitHub community files on POSIX shells. Use an equivalent recursive file listing on other shells.

```bash
rg "agent-forge|Agent Forge|plan|Plan" README.md README.zh-CN.md docs skills .agents .codex-plugin
```

Verifies that docs, marketplace metadata, plugin metadata, and skill references stay aligned when `rg` is installed. Use an equivalent recursive search tool otherwise.

```bash
git diff --check
```

Detects whitespace errors before commit.

If an external Codex skill validator is available, run it according to that validator's own installation path. Do not add machine-specific absolute paths to public docs, contributor docs, or validation scripts.

## Coding Style & Naming Conventions

Write Markdown in concise, instructional prose. Use sentence-case paragraphs, fenced code blocks with language hints where helpful, and relative links such as `docs/plan.md`. Keep skill directories lowercase and hyphenated when needed, for example `skills/my-skill/`.

Preserve bilingual pairing for public behavior docs. When changing shared user-facing behavior, update both English and Chinese files in the same change.

Keep `skills/<name>/SKILL.md` lean. Put reusable output shapes in `assets/`, UI metadata in `agents/openai.yaml`, and introduce `references/` only when the prompt becomes too large to maintain safely in `SKILL.md`.

When the user gives a requirement direction or preference, distill it into stable product and engineering rules. Do not write public docs, validation text, or changelog-style notes as if they are reacting to the latest instruction, and avoid repeating a new rule more than the reader needs.

## Testing Guidelines

For documentation changes, inspect rendered Markdown and run `python3 scripts/validate.py` plus `git diff --check`. For marketplace or plugin manifest changes, validate JSON formatting and confirm the marketplace entry still points at the intended GitHub repository and ref. For skill contract changes, review `SKILL.md`, `assets/`, and `agents/openai.yaml` together so workflow, examples, and final artifact format agree.

Name future automated tests after the behavior they validate if a broader suite is added.

## Plugin Distribution Workflow

Keep this repository as a single-plugin GitHub marketplace unless a future change explicitly introduces multiple plugins. The marketplace manifest should continue to expose the root plugin through `source.source: "url"` and the public repository URL.

Public install instructions should use:

```bash
codex plugin marketplace add li959598874/agent-forge --ref main
```

After a stable release tag exists, prefer a pinned release ref such as `<release-tag>` and update `.agents/plugins/marketplace.json`, `.codex-plugin/plugin.json`, README files, and release notes together when the recommended ref changes.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries, for example `Add GitHub plugin marketplace`. Follow that style: start with a verb and describe the changed asset or behavior.

Pull requests should include a brief summary, changed paths, validation performed, and any user-facing behavior changes. Link related issues when available. Add screenshots only for rendered documentation or UI-visible changes.

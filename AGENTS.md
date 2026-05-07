# Repository Guidelines

## Project Structure & Module Organization

This repository stores Codex-compatible workflow assets and their human-facing documentation.

- `README.md` and `README.zh-CN.md`: top-level project introductions.
- `docs/`: user guides and design notes, currently `ralplan.md` and `ralplan.zh-CN.md`.
- `skills/`: the skill package.

## Build, Test, and Development Commands

There is no compiled build step or package-managed test suite at present. Use lightweight repository checks:

```bash
find skills -maxdepth 2 -type f
```

Lists current skill files for a quick structure check.

```bash
rg "ralplan|RalPlan" README.md docs skills
```

Verifies that documentation and skill references stay aligned after edits.

```bash
git diff --check
```

Detects trailing whitespace and whitespace errors before commit.

## Coding Style & Naming Conventions

Write Markdown in concise, instructional prose. Use sentence-case paragraphs, fenced code blocks with language hints where helpful, and relative links such as `docs/ralplan.md`. Keep skill directories lowercase and hyphenated when needed, for example `skills/my-skill/`. Preserve bilingual pairing when changing public docs: update both English and Chinese files when the change affects shared user-facing behavior.

## Testing Guidelines

For documentation changes, manually inspect rendered Markdown and run `git diff --check`. For skill contract changes, review `skills/<name>/SKILL.md` together with any files under `references/` and `assets/` so the workflow, examples, and final artifact format agree. Name future tests after the behavior they validate if an automated suite is added.

## Commit & Pull Request Guidelines

Recent commits use short, imperative summaries, for example `Update project README introduction`. Follow that style: start with a verb and describe the changed asset or behavior.

Pull requests should include a brief summary, changed paths, validation performed, and any user-facing behavior changes. Link related issues when available. Add screenshots only for rendered documentation or UI-visible changes.

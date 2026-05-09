# Plan

[中文](plan.zh-CN.md)

Plan is a Codex skill for producing a local implementation plan before execution. It explores the current environment, clarifies only decisions that materially affect the plan, writes a draft, waits for user confirmation, then upgrades the same Markdown file to a final checklist.

Plan is planning-only by default. It mutates plan files, not source code, unless the user explicitly asks for implementation.

## Skill Package

```text
skills/plan/
  SKILL.md
  agents/openai.yaml
  assets/
    draft-plan-template.md
    final-plan-template.md
```

## Invocation

Use Plan when the user explicitly invokes `$plan`, asks to plan before implementation, or wants a local checklist that can be executed later.

```text
$plan "Plan the authentication refactor"
```

Natural-language constraints are part of the request:

```text
$plan "Plan the release process. Use read-only subagents if the repository scope is broad."
```

```text
$plan "Plan the logging cleanup and write the plan under .agent-work/planning."
```

## File Rules

Plan stores files in `.agent-work/` unless the user provides another directory. The default filename is:

```text
<yyyyMMdd-HHmm>-<task-slug>.plan.md
```

If a matching draft already exists, Plan updates that draft instead of creating a duplicate. Every plan stays in one Markdown file. A draft uses `status: "draft"`; the confirmed version replaces the same file with `status: "final"`.

Drafts use `skills/plan/assets/draft-plan-template.md`. Finals use `skills/plan/assets/final-plan-template.md`.

## Workflow

1. Ground in local truth before asking questions.
2. Inspect relevant instructions, structure, manifests, schemas, types, tests, fixtures, docs, generated-source boundaries, and existing patterns.
3. Use external research only for current or version-sensitive facts, platform rules, APIs, official docs, standards, or behavior that cannot be trusted from memory.
4. Ask only high-impact questions that cannot be answered through exploration.
5. Write or update the draft plan with Approach Overview, Key Decisions, and Open Questions and Optimization Ideas.
6. Ask the user to confirm or revise the draft direction.
7. After explicit confirmation, rewrite the same file as a final plan with summary, assumptions, execution checklist, validation checklist, risks, safeguards, and completion criteria.
8. Report the plan path and status without duplicating the full local plan in chat unless requested.

## Questions

Questions should lock a meaningful decision, confirm an important assumption, or choose between real tradeoffs. When `request_user_input` is available, use it for plan-changing decisions. In plain text, ask a direct free-form question only when a reasonable multiple-choice shape would be misleading.

Do not ask questions that local inspection can answer. Do not ask "should I proceed?" as a substitute for draft confirmation.

## Subagent Rules

Use subagents as narrow, read-only planning lanes when broad exploration would dilute the main agent's context. Useful lanes include code mapping, test mapping, risk review, and official-docs research.

For exploration subagents, prefer the latest fast, inexpensive model available in the current environment. Ask each subagent for concise findings, relevant paths or URLs, confidence level, and unresolved questions.

The main agent remains responsible for user communication, product decisions, synthesis, and the plan file. Subagents should not decide product intent, finalize tradeoffs, write the plan, implement code, or mutate repository files.

## Quality Bar

Drafts should explain the approach, name supporting repo facts, separate confirmed decisions from recommended defaults, keep open questions limited to blockers, and mark optional optimization ideas as non-blocking.

Final plans should be decision-complete enough for another engineer or agent to execute without hidden chat context. Checklist items should start with imperative verbs and include concrete validation commands, tests, manual checks, or review criteria.

## Validation

Validate repository and skill packaging with:

```bash
python3 scripts/validate.py
```

Also run:

```bash
git diff --check
```

If an external Codex skill validator is available, run it according to that validator's own installation path.

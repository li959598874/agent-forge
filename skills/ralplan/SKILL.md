---
name: ralplan
description: Create an approved local Markdown execution plan. Use when the user invokes $ralplan, asks to clarify requirements, define scope boundaries, interview for decisions, or plan before implementation. Do not use for implementation, final review, commits, or executing a plan.
---

# RalPlan

Planning-only workflow for `$ralplan`.

## Contract

- Syntax: `$ralplan [flags] "<task>"`.
- Do not implement, review, commit, run destructive commands, or execute the plan.
- Normalize options first and echo them briefly. Precedence: flags, explicit natural language, inferred intent, defaults.
- Missing options are `auto`, except `dir`, which defaults to `.agent-work`.
- Ground discoverable facts before asking. Ask only for unresolved preference, authorization, scope, acceptance, validation, or risk decisions.
- Draft in chat, wait for approval, then write exactly one plan: `.agent-work/plans/<slug>/plan.md` unless overridden.
- When research is on, use source-checking evidence lanes for current or external facts that affect the plan.
- Do not create `.gitignore`, hooks, global config, hidden state, or subagent write tasks.

## Flow

1. Normalize task and options.
2. Ground lightly from local instructions, structure, manifests, named files, and obvious docs.
3. Classify scale, interview only blocking gaps, and draft the plan in chat.
4. On approval, write from `assets/plan-template.md`; close with path and remaining assumptions.

## Resources

- `references/workflow.md`: option semantics, scale, interview depth, read-only subagents.
- `references/plan-markdown.md`: final artifact rules; read before writing.
- `assets/plan-template.md`: final plan shape.

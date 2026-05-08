---
name: ralplan
description: Create an approved local Markdown execution plan. Use only when the user explicitly invokes $ralplan or clearly asks to create a plan before implementation. Do not use for general clarification, direct implementation, final review, or commits.
---

# RalPlan

## Purpose

Use this skill to convert an unclear request into a confirmed implementation plan. Keep the skill narrow: clarify, plan, and write one Markdown plan after approval. Do not execute the plan or start review work as part of this skill.

Supported prompt-style syntax:

```text
$ralplan [--scale auto|tiny|small|medium|large]
         [--depth auto|lite|standard|deep]
         [--agents off|auto|on]
         [--research off|auto|on]
         [--dir .agent-work]
         [--name <slug>]
         "<task>"
```

Also support natural-language triggers and implied intent. Normalize structured flags, natural-language preferences, and inferred intent into the same option set before planning. If options conflict, respect explicit structured flags first, then explicit natural language, then inferred intent. Treat missing options as `auto`, except `research`, which defaults to `on`, and `dir`, which defaults to `.agent-work`.

## Operating Contract

- Produce planning output only. Do not make code changes, run destructive commands, create commits, or perform final review.
- Treat options as an explicit process budget. Use no more workflow than the task and user preferences justify.
- Explore facts before asking preference questions when the answer is discoverable from local files, project conventions, or official documentation.
- Ask about preferences, tradeoffs, authorization, and scope boundaries early.
- Present a conversation-only draft before writing any file.
- Write exactly one final plan artifact, a Markdown file, only after user confirmation.
- Make the Markdown plan readable by both users and future agents.
- Use `.agent-work/plans/<slug>/plan.md` by default unless the user provides `--dir` or an explicit path.
- Do not create or update `.gitignore` unless the user explicitly asks.
- Stay low-intrusion: do not install hooks, change global config, override unrelated skills, or create hidden state.

## Workflow

1. **Normalize intent and options.** Identify the task and derive all options from structured flags, natural language, and implied intent. Explicitly echo the normalized options in the conversation before continuing.
2. **Ground minimally.** Read project guidance such as `AGENTS.md`, top-level structure, manifests, test entry points, and relevant docs. Keep this pass proportional to the process budget.
3. **Classify complexity.** Decide scale from change surface, ambiguity, failure cost, and validation width. See `references/workflow.md` for the scale matrix and escalation rules.
4. **Interview only for unresolved decisions.** Match interview depth to both task complexity and how detailed the user's requirement already is. Prefer concise structured questions. If a structured user-input tool is available and permitted by the active mode, use it for short multiple-choice decisions; otherwise ask plain-text questions.
5. **Draft in the conversation.** Summarize task, process budget, goals, non-goals, evidence, decisions, execution slices, validation, risks, and open assumptions. Do not write files at this stage.
6. **Wait for approval, then write.** If the user asks for changes, revise the draft. If the user confirms, write the final Markdown plan.
7. **Close with the artifact path.** After writing, report the plan path and any residual assumptions or validation gaps.

## Subagent Policy

Use subagents for read-heavy exploration when the active environment allows them and the task benefits from context isolation. The main agent should preserve its context for orchestration, synthesis, draft quality, and user communication.

Treat each subagent as an independent evidence lane. Split exploration by task facts such as modules, repositories, independently answerable questions, risk areas, or source types. Keep each subagent prompt bounded and read-only.

For `--agents auto`, decide autonomously from the task evidence and stay local when local grounding is enough. For `--agents on`, prefer subagent-backed exploration for broad or read-heavy work and fan out all useful independent evidence lanes before drafting.

With `--research on`, include source-checking evidence lanes for current external facts, official documentation, primary sources, or standards when they affect the plan. If subagents are unavailable, perform only the minimum necessary source checks in the main context and record sources in Evidence.

Do not delegate write tasks from this skill. Subagents should return facts, file references, risks, and concise summaries; the main agent owns synthesis and user communication.

## Resources

- Read `references/workflow.md` when classifying task size, deciding interview depth, or deciding whether to use subagents.
- Read `references/plan-markdown.md` before writing the final plan artifact.
- Use `assets/plan-template.md` as the final `plan.md` structure.

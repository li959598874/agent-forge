---
name: plan
description: Create an approved local Markdown execution plan through a draft-to-plan workflow. Use when the user invokes $plan, asks to clarify requirements, define scope boundaries, choose tradeoffs, or plan before implementation. Do not use for implementation, final review, commits, or executing a plan.
---

# Plan

## Mode Contract

- Syntax: `$plan [--low|-l|--medium|-m|--high|-h|--max|-x] "<task>"`.
- Planning-only: do not implement, review, commit, run destructive commands, or execute the plan. If asked to execute, plan the execution instead.
- Treat `$plan` as the only planning interface.
- Write only `.agent-work/plans/<slug>/plan.md` with `Status: Draft` or `Status: Execution Plan`.
- Do not create JSON handoffs, hidden state, `.gitignore`, hooks, global config, or subagent write tasks.
- Keep updates short and task-relevant; avoid verbose logging or repeated phrasing.

## Presets

Normalize before exploration. Precedence: preset flags, explicit natural language, inferred task intent, then intelligent default. If no preset is explicit, choose one. Echo the selected preset in the conversation with a brief reason; do not add a `Preset:` field to the artifact.

| Preset | Use When | Behavior Ceiling |
| --- | --- | --- |
| `low` (`--low`, `-l`) | Local, low-risk, well-bounded planning. | Minimal local grounding and 0-2 blocking questions. |
| `medium` (`--medium`, `-m`) | Normal feature, cleanup, or cross-file planning. | Relevant files, manifests, tests, enough questions to freeze scope and acceptance. |
| `high` (`--high`, `-h`) | Architecture, migration, broad ambiguity, or higher failure cost. | Broader repo exploration, staged clarification, evidence capture, and read-only subagents when available. |
| `max` (`--max`, `-x`) | High-stakes, large, unfamiliar, or research-heavy planning. | Wide exploration, source checks, critic pass, and read-only multi-agent lanes when available. |

Presets are ceilings, not quotas. Move quickly when requirements are clear; ask boundary questions when even a low-preset task is underspecified.

## Subagent Orchestration

Use subagents only for read-only planning lanes; never delegate artifact writes, implementation, commits, destructive operations, or user communication. The main agent owns synthesis and decisions.

For `high`, enable subagents when available and split independent lanes such as subsystem discovery, risk review, validation strategy, or external-source research. For `max`, use read-only multi-agent lanes by default when available, including a critic or risk lane for architecture, migration, high-risk, or unclear-requirement work.

Before delegating, do the immediate local grounding yourself. Delegate only parallel side lanes that return concise evidence, file paths, risks, recommendations, and confidence.

## Execution Vs Mutation

Allowed: read/search files, inspect configs/manifests/schemas/docs/tests/types, run static or dry-run checks that do not edit tracked files, and write/update only the plan artifact.

Forbidden outside the artifact: implementation edits, migrations, codegen, formatter rewrites, commits, destructive commands, and subagent write tasks.

## Phase 1 - Ground In The Environment

Explore first, ask second. Decide what needs reading, then batch independent reads/searches. Prefer `rg`/`rg --files` and parallel reads when available. Inspect local instructions, repo structure, manifests, named files, likely tests, and obvious docs. Treat repo/system facts as discoverable; do not ask when inspection can answer. Use official or primary sources for current external facts. Capture shaping facts for the final Evidence section.

## Phase 2 - Clarify Intent

Ask only for decisions that materially change the draft or execution plan. Continue until goal, success criteria, audience, scope, constraints, current state, and tradeoffs are clear.

Each clarification question needs clear question text, meaningful option labels, one-sentence option descriptions, and a custom-answer path. With `request_user_input`, rely on the host free-form option. In plain text, include `User-provided answer`.

Do not ask filler questions, questions answered by exploration, or questions whose answers would not change the plan.

## Phase 3 - Draft Then Execution Plan

Create one artifact in two stages: write `.agent-work/plans/<slug>/plan.md` with `Status: Draft`, report a concise summary/path/confirmation decisions, then update the same file to `Status: Execution Plan` after confirmation. Do not paste the whole draft unless asked.

Derive `<slug>` from lowercase hyphenated task words. If the path exists and the user did not ask to continue it, append a suffix such as `-2`. Choose headings and depth by task and preset while satisfying the requirements below.

## Draft Requirements

A draft is a proposal for confirmation, not an execution plan. It must cover requirement description, key decisions already made or recommended, suggestions/tradeoffs needing user attention, open questions with labels/descriptions/`User-provided answer`, and the confirmation gate. Do not add implementation slices, rollout detail, or low-level breakdown unless needed to explain a decision.

## Execution Plan Requirements

An execution plan is the confirmed, decision-complete version of the draft. It must cover goals/non-goals, confirmed decisions/assumptions, actionable execution approach or slices, concrete validation, risks/rollback where relevant, open questions or `None`, and Intent drift check: why the plan still matches the original intent and when execution should pause to re-confirm.

Write stable Markdown. Do not force fixed headings when a smaller or task-specific structure is clearer.

## Finalization Rules

- A draft is allowed to contain open questions and recommendations.
- An execution plan must be decision-complete enough for another engineer or agent to implement without hidden chat context.
- If important ambiguity remains after reasonable clarification, keep the artifact at `Status: Draft`.
- Report the artifact path, selected preset, remaining assumptions, and any validation gaps.

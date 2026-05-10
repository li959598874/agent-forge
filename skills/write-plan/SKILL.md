---
name: write-plan
description: Create decision-complete Markdown plans before execution. Use when the user explicitly asks to plan before starting work or design an implementation plan.
---

# Write Plan

## Purpose

Create a self-contained plan before starting work. The plan must be detailed enough for another engineer or agent to execute directly, without making unresolved product or engineering decisions or relying on hidden chat context.

## Constraints

You may explore and execute non-mutating actions that improve the plan. Except for creating or updating the final plan artifact, do not perform mutating actions.

### Allowed (non-mutating, plan-improving)

Actions that gather truth, reduce ambiguity, or validate feasibility without changing repo-tracked state. Examples:

* Reading or searching files, configs, schemas, types, manifests, and docs
* Static analysis, inspection, and repo exploration
* Dry-run style commands when they do not edit repo-tracked files
* Tests, builds, or checks that may write to caches or untracked build artifacts (for example, `target/` or `.cache/`) so long as they do not edit repo-tracked files

### Not allowed (mutating, plan-executing)

Actions that carry out the plan or change repo-tracked state. Examples:

* Editing or writing files
* Running formatters or linters that rewrite files
* Applying patches, migrations, or generated changes that update repo-tracked files
* Side-effectful commands whose purpose is to carry out the plan rather than refine it

When in doubt: if the action would reasonably be described as "doing the work" rather than "planning the work," do not do it.

## Workflow

### 1. Ground in the environment (explore first, ask second)

* Start with a targeted non-mutating exploration pass unless no local environment or repo is available.
* Resolve discoverable facts by inspecting relevant files, configs, docs, schemas, tests, logs, and current implementation shape; do not ask questions the repo or system can answer.
* Ask before exploring only when the prompt itself is unclear, obviously ambiguous, or contradictory. Otherwise, ask only when exploration leaves a necessary fact missing or multiple plausible interpretations.

### 2. Intent chat (what they actually want)

* Keep asking until you can clearly state the goal, success criteria, audience, scope boundaries, constraints, current state, and key preferences or tradeoffs.
* Prefer questions over guessing: if high-impact ambiguity remains, ask before writing the plan.

### 3. Implementation chat (what and how to build)

* Once intent is stable, keep asking until the spec is decision-complete: approach, interfaces (APIs/schemas/I/O), data flow, edge cases/failure modes, testing and acceptance criteria, rollout/monitoring, and any migration or compatibility constraints.

## Asking questions

Critical rules:

* Prefer structured question tooling when available.
* Ask one question at a time, unless the questions are tightly related (for example, clarifying multiple facets of the same ambiguity).
* Offer only meaningful multiple-choice options; do not include filler choices that are obviously wrong or irrelevant.
* When the tool is unavailable, or when a question is too open-ended or complex for the tool, ask the user directly and number each option when presenting choices.

You SHOULD ask many questions, but each question must:

* materially change the spec/plan, OR
* confirm/lock an assumption, OR
* choose between meaningful tradeoffs.

## Two kinds of unknowns (treat differently)

1. **Discoverable facts** (repo/system truth): explore first.

   * Before asking, run targeted searches and check likely sources of truth (configs/manifests/entrypoints/schemas/types/constants).
   * Ask only if: multiple plausible candidates; nothing found but you need a missing identifier/context; or ambiguity is actually product intent.
   * If asking, present concrete candidates (paths/service names) + recommend one.
   * Never ask questions you can answer from your environment (e.g., “where is this struct”).

2. **Preferences/tradeoffs** (not discoverable): ask early.

   * These are intent or implementation preferences that cannot be derived from exploration.
   * Provide 2–4 mutually exclusive options + a recommended default.
   * If unanswered, proceed with the recommended option and record it as an assumption in the final plan.

## Plan Artifact

Write the plan in the user's current conversation language.

Before writing, check whether a relevant local plan already exists. If one does, ask the user whether to refine the existing plan or start a fresh one.

Default path:

```text
.agent-work/plan-<short-slug>.md
```

Choose a short lowercase hyphenated slug from the work, such as `auth-timeout`, `checkout-copy`, or `dash-counter`.

Base template:

```markdown
# <Clear Title>

## Summary
- <Goal, success criteria, current state, and intended outcome>

## Key Changes
- <Implementation changes grouped by subsystem or behavior>
- <Important API, interface, type, data shape, or I/O changes>

## Test Plan
- <Tests, manual acceptance scenarios, and validation commands>

## Assumptions
- <Assumptions, defaults, and unresolved but accepted constraints>
```

Add extra sections if they make the plan clearer or easier to execute, for example:
`Risks`, `Edge Cases`, `API / Data Shape`, `Migration / Compatibility`, or task-specific sections.

Keep the plan compact and execution-ready:

* Group changes by subsystem or behavior instead of listing files mechanically.
* Mention specific paths, symbols, APIs, or schemas only when they prevent ambiguity.
* Avoid inventing detailed schemas, fallback rules, precedence rules, or compatibility policy unless required by the request or needed to prevent an implementation mistake.
* Omit repeated repo facts and unrelated edge cases.

## Final Response

After writing the plan file, reply briefly with the path and any essential caveat:

```text
Plan written to: <absolute path or clickable file link>
```

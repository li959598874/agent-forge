---
name: plan
description: Use when the user explicitly invokes `$plan`, asks to plan before implementation, or wants to turn ambiguous requirements into a decision-ready local implementation checklist.
---

# Plan

## Purpose

Produce a local planning artifact before implementation: explore, clarify, write a draft, then upgrade the same file to a final executable checklist after user confirmation.

Prefer subagents when exploration is broad enough to threaten the main agent's context, or when code, tests, risks, and documentation research can be split into independent tracks. Keep the main agent responsible for synthesis, decisions, and the plan file.

This skill does not override higher-priority instructions. During planning, mutate only plan files unless the user explicitly asks for implementation.

## File Rules

- Store plans in `.agent-work/` unless the user provides a directory.
- Name files `<yyyyMMdd-HHmm>-<task-slug>.plan.md` inside the selected directory unless the user provides a filename.
- Update a matching draft instead of creating a duplicate.
- Keep one file per plan; upgrade `status: draft` to `status: final` in place.
- Use `assets/draft-plan-template.md` for drafts and `assets/final-plan-template.md` for finals, adjusting headings only when the task needs it.

## Workflow

1. Ground in the environment and research broadly.
   - Start with local truth. Resolve discoverable facts before asking the user.
   - Run at least one targeted non-mutating exploration pass when a repo or local environment is available.
   - Use `rg` and `fd` first; inspect likely entrypoints, configs, manifests, schemas, types, tests, fixtures, docs, generated-source boundaries, and existing patterns.
   - Map relevant subsystems, ownership boundaries, public interfaces, data flow, failure modes, and verification commands before proposing changes.
   - Split independent research to subagents when useful; follow Subagent Rules.
   - Use external research for current or version-sensitive facts, platform rules, APIs, official docs, standards, or behavior that cannot be trusted from memory.
   - Run dry-run checks only when they improve the plan and do not change repo-tracked source files.
   - Record facts, paths, URLs, uncertainties, and rejected paths only when they affect the draft or final plan.

2. Resolve intent.
   - Follow Asking Questions.
   - Ask only after exploration, except for prompt contradictions or undiscoverable preferences.
   - Ask about high-impact ambiguity in the goal, success criteria, audience, scope, constraints, current state, preferences, or tradeoffs.
   - Continue until the intent is stable enough to state the goal, success criteria, audience, in-scope work, out-of-scope work, constraints, current state, and chosen tradeoffs.
   - If the user changes direction, revisit exploration, refresh assumptions, and continue until the updated intent is stable.
   - Treat intent as decision-complete only when no high-impact ambiguity remains and unanswered tradeoffs have recorded conservative defaults.

3. Write the draft plan.
   - Create or update the plan file with `status: draft` using `assets/draft-plan-template.md`.
   - Include only Approach Overview, Key Decisions, and Open Questions and Optimization Ideas.
   - Do not include an executable task checklist.
   - Include research notes only where they support a decision or open question.
   - Ask the user to confirm or revise the draft direction before writing the final plan.

4. Upgrade to the final plan.
   - Write the final only after the user explicitly confirms the draft direction or remaining decisions.
   - Rewrite the same file with `status: final` using `assets/final-plan-template.md`.
   - Make the plan actionable by another engineer or agent without product or technical decisions and without hidden chat context.
   - Include summary, assumptions, ordered execution checklist, validation checklist, risks, safeguards, and completion criteria.
   - Group tasks by subsystem or behavior; mention file paths only to remove ambiguity.

5. Report back.
   - State the plan path and status.
   - Summarize unresolved decisions for drafts.
   - Summarize implementation and validation checkpoints for finals.
   - Do not duplicate the full local plan in chat unless requested.

## Asking Questions

- When available, prefer `request_user_input`, but use it only for plan-changing decisions, important assumptions, or information that cannot be discovered through non-mutating exploration.
- Provide 2-4 concrete, meaningful, mutually exclusive options; omit filler choices and recommend a default when defensible.
- Ask direct free-form questions only when an unavoidable important question cannot be expressed with reasonable multiple-choice options.
- Each question must materially change the spec or plan, confirm or lock an assumption, choose between meaningful tradeoffs, and not be answerable by exploration.
- Do not ask "should I proceed?" as a substitute for confirmation. Ask the user to confirm the draft direction, pick remaining decisions, or request revisions.

## Subagent Rules

- Assign subagents narrow, independent responsibilities:
  - code-map: relevant files, ownership boundaries, patterns, and likely edit points.
  - test-map: tests, harnesses, fixtures, and verification commands.
  - risk-map: edge cases, compatibility constraints, generated files, migrations, and likely regressions.
  - docs-research: primary sources or official docs for libraries, APIs, platforms, or current behavior.
- For explorer, prefer the latest fast, inexpensive model available in the current environment.
- Ask each subagent for concise findings, relevant paths or URLs, confidence level, and unresolved questions.
- Keep subagents non-mutating during planning.
- Do not ask subagents to decide product intent, finalize tradeoffs, or write the final plan.
- Deduplicate overlapping findings before adding them to the plan.

## Draft Quality Bar

- Explain the approach and supporting repo facts.
- Separate confirmed decisions from recommended defaults.
- Keep open questions limited to unresolved blockers.
- Mark optimization ideas as optional and non-blocking.

## Final Quality Bar

- Confirm user approval before writing `status: final`.
- Make the plan decision-complete.
- Start every checklist item with an imperative verb and a clear outcome.
- Name concrete commands, tests, manual checks, or review criteria.
- Record assumptions explicitly and remove draft-only uncertainty.

## External Research

- Prefer official documentation, source repositories, standards, changelogs, and vendor docs.
- Use web research for current or version-sensitive facts, APIs, laws, pricing, schedules, platform behavior, or other unstable information.
- Cite source URLs when external facts affect decisions; avoid secondary summaries when primary sources are available.

## Templates

Use `assets/draft-plan-template.md` for drafts. After user confirmation, replace the same plan file's body with `assets/final-plan-template.md` and change `status` to `final`.

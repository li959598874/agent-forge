# RalPlan Workflow Reference

## Option Semantics

- `--scale`: controls change-surface assumptions and artifact richness.
  - `auto`: infer from evidence.
  - `tiny`: local, low-risk, easily reversible task.
  - `small`: narrow repo task with limited uncertainty.
  - `medium`: cross-file or cross-module planning with real ambiguity.
  - `large`: architecture, migration, multi-phase, or high-risk planning.
- `--depth`: controls interview detail.
  - `auto`: infer from task complexity and requirement detail.
  - `lite`: ask only blocking questions.
  - `standard`: ask enough to freeze scope and acceptance.
  - `deep`: probe goals, non-goals, alternatives, risks, rollout, and validation.
- `--agents`: controls optional read-only subagent exploration.
- `--research`: controls research-backed evidence lanes. Default `on`; prefer official documentation and primary sources.
- `--dir`: target scratch directory for the final plan. Default `.agent-work`.
- `--name`: stable slug for the plan folder. If absent, derive a short lowercase hyphenated slug from the task.

## Option Normalization

Before grounding or interviewing, normalize all options into one explicit set and echo it to the user. Use this priority order:

1. Structured CLI-style flags, such as `--scale medium` or `--agents off`.
2. Explicit natural-language preferences, such as "keep this lightweight", "do a deep plan", "do not use subagents", or "use the latest official docs".
3. Implied intent from the task, such as high-risk wording, broad architecture scope, "latest docs", or an explicit request for a durable artifact.
4. Defaults.

The echo should be brief and visible in the conversation before further workflow steps:

```text
Normalized RalPlan options:
- scale: medium (inferred from cross-module scope)
- depth: standard (natural language requested a normal plan)
- agents: auto (default)
- research: on (default)
- dir: .agent-work (default)
- name: auth-refactor (derived)
```

If a value is inferred, include the reason. If an inferred value is uncertain and materially affects the process, ask for confirmation before proceeding.

Natural-language examples:

- "quick/lightweight/simple" -> prefer `scale tiny|small`, `depth lite|standard`.
- "deep/thorough/architecture/migration" -> prefer `depth deep`; consider `scale medium|large`.
- "no agents/no subagents/keep it local" -> `agents off`.
- "parallel exploration/use subagents" -> `agents on` unless the active environment forbids it; prefer broad read-only exploration for broad or read-heavy tasks.
- "check latest/current docs" -> keep `research on`; consider `agents on` for broad research.
- "do not browse/no external research" -> `research off`.

RalPlan always follows the same approval-gated write flow: produce a conversation draft, wait for user approval, then write the final Markdown plan. If the user asks to "just draft" or "do not write yet", treat that as a request to stop before the approval/write step for the current turn, not as a persistent mode option.

## Process Budget Rules

The process budget is a ceiling, not a quota.

- Never add interview rounds just because the task is labeled `large`.
- In `agents auto`, use subagents only when task evidence shows useful independent exploration lanes.
- In `agents on`, make subagent-backed exploration the default for broad or read-heavy work so the main agent can preserve context quality for orchestration and synthesis.
- Organize subagent exploration around independent evidence lanes; avoid duplicate exploration unless the lanes intentionally check different evidence.
- Escalate from `auto` only when evidence shows wider change surface, unresolved ambiguity, high failure cost, current external facts, or broad validation needs.
- If the user explicitly sets `--agents off` or `--research off`, respect that unless continuing would be unsafe or impossible; in that case, pause and explain the blocker.
- If the user explicitly asks for a durable local plan, do not stop at a chat-only plan unless they later revise that request.

## Complexity Classification

Classify with four dimensions:

| Dimension | Low Signal | High Signal |
| --- | --- | --- |
| Change surface | One file, one config, documentation-only | Cross-module, API, data model, build/test infrastructure |
| Ambiguity | Clear goal and success criteria | Unclear owner, scope, behavior, or user preference |
| Failure cost | Easy rollback, low user impact | Data loss, production risk, security, money, legal/compliance |
| Validation width | One obvious check | Multiple environments, integration tests, manual QA, staged rollout |

Use the highest meaningful signal:

- `tiny`: all dimensions low. Do minimal grounding, ask 0-2 questions, no subagents.
- `small`: one dimension moderate. Do short grounding, ask focused questions, no subagents by default.
- `medium`: multiple moderate dimensions or one high dimension. If subagents are enabled, split only the independent read-heavy lanes that evidence supports.
- `large`: architecture, migration, or high-risk work. If subagents are enabled, split by module, subsystem, source type, risk area, critic pass, or source-check lane.

Explicit user options override automatic classification. For example, `--scale tiny --depth deep` means a small surface with deeper clarification; `--scale large --agents off` means broad planning without subagent delegation.

## Grounding Pass

Before interviewing, inspect only enough context to avoid asking discoverable questions:

- Project guidance: `AGENTS.md`, `.AGENTS.md`, or equivalent local instructions.
- Top-level directories and manifests: package files, solution files, build configs, test configs.
- Existing planning or workflow conventions when obvious.
- Files directly named by the user.

For unstable or external facts, include source checks when the fact affects the plan. Prefer official documentation and primary sources.

## Interview Rules

Ask questions only for decisions the agent cannot responsibly infer. Prioritize:

- Goal and success definition.
- Non-goals and scope boundaries.
- Authorization: what the agent may decide versus what needs confirmation.
- Constraints: compatibility, delivery timeline, dependencies, coding/test limits.
- Acceptance criteria and validation expectations.
- Risk tolerance and rollback expectations.

Keep question volume proportional to both scale and requirement detail.

Assess requirement detail before asking:

- `high detail`: the user already supplied goals, non-goals, constraints, acceptance, relevant files, and preferred tradeoffs. Ask only for contradictions or blocking gaps.
- `medium detail`: the user supplied a clear goal and some constraints, but acceptance, risks, or boundaries are incomplete. Ask a focused batch.
- `low detail`: the user supplied intent but not scope, success criteria, constraints, or authorization. Use a deeper interview, even for a small task.

Question volume by scale is a ceiling, not a quota:

- `tiny`: 0-2 questions.
- `small`: 1-3 questions.
- `medium`: 2-5 questions, grouped by decision area.
- `large`: staged interview; ask the first blocking batch, then refine after evidence.

Adjust within those ceilings:

- For high-detail requirements, reduce questions and proceed to the draft once readiness is sufficient.
- For low-detail requirements, use the full allowance for the scale and ask the next staged batch only after grounding or user answers reveal more gaps.
- If task scale is small but requirement detail is low, ask boundary and acceptance questions before drafting.
- If task scale is large but requirement detail is high, do not perform a ceremonial long interview; validate assumptions and move to a draft.

Prefer multiple-choice or short structured questions when the answer space is known. Include an explicit recommended option when useful.

## Draft Approval Gate

The conversation draft must include:

- Task summary.
- Process budget and why it is appropriate.
- Goals and non-goals.
- Evidence already gathered.
- Key decisions and assumptions.
- Proposed execution slices.
- Validation approach.
- Risks and rollback.
- Open questions, if any.

Do not write the plan file until the user confirms the draft.

## Subagent Use

`--agents` controls exploration permission and delegation posture:

- `off`: do not use subagents.
- `auto`: let the main agent decide from task facts; stay local when local grounding is enough.
- `on`: use subagents as the preferred exploration path for broad, read-heavy, or research-backed work, then synthesize in the main context.

Use subagents for read-heavy work that would otherwise pollute the main context:

- Repo fact finding.
- Test and build surface discovery.
- Official documentation research.
- Risk or plan critique.

Design exploration lanes from the work shape. Good boundaries include modules, repositories, architecture layers, source families, independent risks, and critic passes. For `agents on`, fan out all useful independent lanes before drafting; for `agents auto`, use only the lanes whose value is clear from the task evidence.

Give each subagent a bounded, self-contained prompt. Ask for evidence with file paths, commands, source links, and confidence level. Do not ask subagents to edit files for this skill.

The main agent must preserve context quality, synthesize the plan, and own the approval conversation.

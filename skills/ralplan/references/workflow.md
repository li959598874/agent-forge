# RalPlan Workflow Reference

## Option Semantics

- `--scale`: Controls change-surface assumptions and artifact richness.
  - `auto`: Infer from evidence.
  - `tiny`: Local, low-risk, easily reversible task.
  - `small`: Narrow repo task with limited uncertainty.
  - `medium`: Cross-file or cross-module planning with real ambiguity.
  - `large`: Architecture, migration, multi-phase, or high-risk planning.
- `--depth`: Controls interview detail.
  - `lite`: Ask only blocking questions.
  - `standard`: Ask enough to freeze scope and acceptance.
  - `deep`: Probe goals, non-goals, alternatives, risks, rollout, and validation.
- `--agents`: Controls optional read-only subagent exploration.
- `--research`: Controls external research. If enabled, prefer official documentation and primary sources.
- `--dir`: Target scratch directory for the final plan. Default `.agent-work`.
- `--name`: Stable slug for the plan folder. If absent, derive a short lowercase hyphenated slug from the task.

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
- research: off (no current external facts requested)
- dir: .agent-work (default)
- name: auth-refactor (derived)
```

If a value is inferred, include the reason. If an inferred value is uncertain and materially affects the process, ask for confirmation before proceeding.

Natural-language examples:

- "quick/lightweight/simple" -> prefer `scale tiny|small`, `depth lite|standard`.
- "deep/thorough/architecture/migration" -> prefer `depth deep`; consider `scale medium|large`.
- "no agents/no subagents/keep it local" -> `agents off`.
- "parallel exploration/use subagents" -> `agents on` unless the active environment forbids it.
- "check latest/current docs" -> `research on`.
- "do not browse/no external research" -> `research off`.

RalPlan always follows the same write flow: produce a conversation draft, wait for user approval, then write the final Markdown plan. If the user asks to "just draft" or "do not write yet", treat that as a request to stop before the approval/write step for the current turn, not as a persistent mode option.

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
- `medium`: multiple moderate dimensions or one high dimension. Consider one read-only explorer.
- `large`: architecture/migration/high-risk work. Consider multiple read-only exploration passes and a critic pass.

Explicit user options override automatic classification. For example, `--scale tiny --depth deep` means a small surface with deeper clarification; `--scale large --agents off` means broad planning without subagent delegation.

## Grounding Pass

Before interviewing, inspect only enough context to avoid asking discoverable questions:

- Project guidance: `AGENTS.md`, `.AGENTS.md`, or equivalent local instructions.
- Top-level directories and manifests: package files, solution files, build configs, test configs.
- Existing planning or workflow conventions when obvious.
- Files directly named by the user.

For unstable or external facts, browse only when the user asks for current information or when high-stakes accuracy depends on current official sources.

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

- `high detail`: The user already supplied goals, non-goals, constraints, acceptance, relevant files, and preferred tradeoffs. Ask only for contradictions or blocking gaps.
- `medium detail`: The user supplied a clear goal and some constraints, but acceptance, risks, or boundaries are incomplete. Ask a focused batch.
- `low detail`: The user supplied intent but not scope, success criteria, constraints, or authorization. Use a deeper interview, even for a small task.

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
- Goals and non-goals.
- Evidence already gathered.
- Key decisions and assumptions.
- Proposed execution slices.
- Validation approach.
- Risks and rollback.
- Open questions, if any.

Do not write the plan file until the user confirms the draft.

## Subagent Use

Use subagents for read-heavy work that would otherwise pollute the main context:

- Repo fact finding.
- Test and build surface discovery.
- Official documentation research.
- Risk or plan critique.

Give each subagent a bounded, self-contained prompt. Ask for evidence with file paths, commands, source links, and confidence level. Do not ask subagents to edit files for this skill.

The main agent must synthesize the plan and own the approval conversation.

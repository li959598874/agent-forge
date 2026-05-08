# RalPlan Workflow Reference

## Options

Normalize before grounding and echo values plus reasons. Priority:

1. CLI-style flags.
2. Explicit natural language.
3. Inferred task intent.
4. Defaults.

| Option | Values | Note |
| --- | --- | --- |
| `--scale` | `auto`, `tiny`, `small`, `medium`, `large` | Surface and artifact richness. |
| `--depth` | `auto`, `lite`, `standard`, `deep` | Interview detail. |
| `--agents` | `off`, `auto`, `on` | Read-only subagent exploration. |
| `--research` | `off`, `auto`, `on` | Source checks; default `auto`. |
| `--dir` | path | Plan root; default `.agent-work`. |
| `--name` | slug | Plan folder slug. |

## Complexity Classification

Classify by the strongest signal across surface, ambiguity, failure cost, and validation width.

| Scale | Use When | Interview Ceiling | Subagent Default |
| --- | --- | --- |
| `tiny` | Local, low-risk, obvious validation. | 0-2 questions | Off |
| `small` | Narrow repo task, limited uncertainty. | 1-3 questions | Off unless requested |
| `medium` | Cross-file/module or one high-risk dimension. | 2-5 questions | Auto for useful read-heavy lanes |
| `large` | Architecture, migration, phased, or high-risk work. | Staged batches | Split by module, risk, source, or critic lane |

## Interview Rules

Ask only for decisions that cannot be responsibly inferred. Prefer short structured questions about goals, non-goals, scope, authorization, constraints, acceptance, validation, risk, and rollback. High-detail requests need only contradiction checks; low-detail requests need boundary and acceptance questions before drafting.

## Draft Approval Gate

If the user says "just draft" or "do not write yet", stop before writing for that turn. If they request a durable local plan, do not stop at chat-only output unless they revise that request.

## Subagent Use

`off` means no subagents. `auto` uses only valuable independent read-heavy lanes. `on` prefers them for broad discovery, official-doc research, risk checks, or critique when allowed. Prompts stay bounded and read-only. The main agent owns synthesis and communication.

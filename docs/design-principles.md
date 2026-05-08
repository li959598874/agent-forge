# Design Principles

Agent Forge exists to make agent orchestration proportional to the task. It should help Codex spend more process only when that process improves the result.

## Product Thesis

Agent workflows need a process budget. Without one, small edits can become expensive ceremonies and large architecture work can still lack durable decisions. Agent Forge exposes that budget directly instead of hiding it behind a fixed pipeline.

The project optimizes for:

- **Light tasks stay light**: avoid interviews and subagents when a local answer is enough.
- **Heavy tasks get structure**: use clarification, evidence, decomposition, and risk checks when ambiguity or failure cost is high.
- **Users keep control**: explicit flags and natural-language preferences override automatic inference.
- **Local artifacts matter**: approved plans should be written into the workspace when the user wants durable execution context.
- **Low intrusion wins**: do not install hooks, override unrelated skills, or modify user configuration unless explicitly requested.

## Process Budget Model

| Budget | Typical use | Default behavior |
| --- | --- | --- |
| `low` | One local, low-risk change | Minimal context and no subagents. |
| `medium` | Narrow or normal planning with limited ambiguity | Short grounding and enough questions to freeze scope. |
| `high` | Cross-file, architecture, migration, or higher-risk planning | Deeper interview, evidence capture, and optional read-only lanes. |
| `max` | Broad, high-stakes, or research-heavy planning | Wide exploration, staged plan, and optional critic pass. |

The model is not a bureaucracy. It is a ceiling for process. A high-detail large task can move quickly, and a small low-detail task can still require one or two boundary questions.

## Orchestration Boundaries

Agent Forge assets should be composable with a user's existing setup:

- Prefer explicit invocation, such as `$plan`, over implicit interception.
- Keep persistent outputs in predictable local paths.
- Avoid hidden machine-only state when a Markdown artifact can carry the same context.
- When subagents are explicitly enabled, use them broadly for read-heavy exploration and keep the main agent focused on orchestration and synthesis.
- When subagents are not explicitly enabled, let the agent decide from task facts whether context-isolated exploration is worth the overhead.
- Prefer official documentation and primary sources when current external facts matter.

## Current Implementation

Plan implements the first slice of this model: planning. It clarifies ambiguous work, writes a draft, waits for approval, and upgrades one Markdown plan file. It intentionally does not implement the plan, commit changes, or perform final code review.

## Roadmap

Future work should stay incremental:

- Add additional workflow skills only when they solve a distinct user problem.
- Add execution or review workflows only after their boundaries are explicit.
- Keep plugin distribution as a single marketplace entry until multiple plugins are justified.
- Add automation only when it verifies repository contracts without increasing user setup cost.

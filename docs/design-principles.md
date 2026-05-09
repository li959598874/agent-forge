# Design Principles

Agent Forge is a user-controlled, low-intrusion, composable multi-agent workflow plugin for Codex. It treats skills as workflow primitives that can be invoked separately, combined when useful, and ignored when the current task does not need them.

## Product Thesis

Agent workflows should be explicit and proportional. Users should decide when a workflow starts, while each skill should decide only the process needed for its own responsibility. Multi-agent orchestration is valuable when it improves exploration, risk coverage, validation, or synthesis; it should not become ceremony for every request.

The project optimizes for:

- **User control**: workflows start from explicit skill invocation or clear user intent.
- **Low intrusion**: do not install hooks, rewrite global configuration, override unrelated tools, or mutate files outside the requested scope.
- **Skill composition**: design each skill with a narrow responsibility, stable public surface, and behavior that can coexist with other user or plugin skills.
- **Multi-agent leverage**: use subagents as bounded lanes for code mapping, tests, risks, docs research, critique, or future workflow roles when parallel context improves the result.
- **Local artifacts**: write durable workspace files when they help humans or later agents continue work without hidden chat context.

## Workflow Boundaries

Agent Forge assets should be easy to adopt and easy to stop using:

- Prefer explicit commands such as `$plan` over implicit interception.
- Keep outputs in predictable local paths.
- Keep machine-specific state out of public docs, manifests, and generated artifacts.
- Let skills compose through clear artifacts and documented behavior rather than private side channels.
- Keep the main agent responsible for synthesis, user communication, and final decisions.
- Use official documentation and primary sources when current external facts affect workflow decisions.

## Current Primitive

Plan is the first workflow primitive. It explores the environment, clarifies decisions, writes a draft plan, waits for confirmation, and upgrades the same Markdown file to a final execution checklist. It is planning-only by default and uses subagents only as read-only planning lanes.

## Roadmap

Future work should stay incremental:

- Add workflow skills only when they solve a distinct user problem.
- Keep skill contracts small enough to combine without surprising side effects.
- Add execution, review, or release workflows only after their boundaries are explicit.
- Keep plugin distribution as a single marketplace entry until multiple plugins are justified.
- Add automation only when it verifies repository contracts without increasing user setup cost.

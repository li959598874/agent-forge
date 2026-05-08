# TODO

This checklist tracks planned Agent Forge work. Keep items concise, scoped, and aligned with the project principle: lightweight tasks stay lightweight, while complex work can opt into deeper orchestration.

## Planned Features

### Plugin Setup And Usage Guidance Skill

- [ ] Create a skill that guides users through Agent Forge plugin setup, installation checks, and first-use workflow selection.
- [ ] Cover common paths: fresh install, marketplace update, installed-skill discovery, and choosing when to use `$ralplan`.
- [ ] Keep the skill low-intrusion: it should inspect and explain before suggesting configuration changes.
- [ ] Document the skill in English and Chinese user docs.
- [ ] Add validation coverage for the new skill package and metadata.

Acceptance criteria:

- Users can invoke one skill to understand how to configure and use Agent Forge.
- The skill does not assume machine-specific paths or modify global Codex configuration without explicit approval.
- The workflow explains when to use lightweight local handling versus deeper planning.

### User Preference Configuration

- [ ] Design a portable configuration contract for user preferences.
- [ ] Support default work artifact paths, including plan output roots and future workflow output directories.
- [ ] Support multi-agent model preferences, including default explorer/research/critic lane model choices when the host environment exposes model controls.
- [ ] Support default values for workflow parameters such as `scale`, `depth`, `agents`, `research` lane policy, `dir`, and naming conventions.
- [ ] Define precedence rules across explicit prompt flags, project configuration, user configuration, and built-in defaults.
- [ ] Add documentation and examples for safe configuration.
- [ ] Add validation or schema checks for configuration files.

Acceptance criteria:

- Users can set stable preferences without editing skill internals.
- Explicit user prompt options always override configured defaults.
- Configuration remains optional and does not affect unrelated skills or tools.
- Forks and contributors can validate configuration examples with repo-local checks.

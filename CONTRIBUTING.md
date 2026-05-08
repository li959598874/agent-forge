# Contributing

Thanks for helping improve Agent Forge. This project is intentionally small: changes should make Codex workflow orchestration more explicit, adaptive, and low-intrusion.

## Good Contributions

Useful contributions usually fit one of these categories:

- Improve the `$ralplan` workflow contract or plan artifact quality.
- Clarify public documentation in English and Chinese.
- Add focused validation that protects plugin, marketplace, or skill packaging.
- Propose new workflow assets with clear boundaries and low default ceremony.

Avoid broad framework work unless the problem is concrete and the user-facing behavior is already defined.

## Development Setup

No package install is required for the current repository.

```bash
python3 scripts/validate.py
git diff --check
```

If you use an external Codex skill validator, run it according to that validator's own installation path.

## Documentation Expectations

Public behavior changes should update both `README.md` and `README.zh-CN.md` when relevant. Detailed RalPlan behavior should stay aligned across:

- `docs/ralplan.md`
- `docs/ralplan.zh-CN.md`
- `skills/ralplan/SKILL.md`
- `skills/ralplan/references/`
- `skills/ralplan/assets/plan-template.md`

Keep prose concise, professional, and implementation-oriented.

## Pull Requests

Before opening a pull request:

1. Keep the change focused.
2. Update docs and manifests that describe the changed behavior.
3. Run the validation commands above.
4. Include a summary, changed paths, validation performed, and user-facing behavior changes.

Commit messages should be short and imperative, for example `Refine RalPlan process budget`.

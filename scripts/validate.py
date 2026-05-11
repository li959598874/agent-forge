#!/usr/bin/env python3
"""Validate Agent Forge repository contracts with stdlib-only checks."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
TEXT_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".py", ""}
LINUX_HOME_PREFIX = "/" + "home" + "/"
MAC_HOME_PREFIX = "/" + "Users" + "/"
WSL_MOUNT_PREFIX = "/" + "mnt" + "/"
SYSTEM_SKILL_PATH = "." + "codex/skills/" + ".system"
MACHINE_PATH_PATTERNS = [
    re.compile(re.escape(LINUX_HOME_PREFIX) + r"[A-Za-z0-9._-]+/"),
    re.compile(re.escape(MAC_HOME_PREFIX) + r"[A-Za-z0-9._-]+/"),
    re.compile(re.escape(WSL_MOUNT_PREFIX) + r"[A-Za-z]/"),
    re.compile(r"[A-Za-z]:\\"),
    re.compile(re.escape(SYSTEM_SKILL_PATH)),
]
IGNORED_TEXT_PARTS = {".git", ".agent-work", ".codex", ".venv", "__pycache__"}


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def require_file(path: str) -> Path:
    target = ROOT / path
    if not target.is_file():
        ERRORS.append(f"missing required file: {path}")
    return target


def read_text(path: str) -> str:
    target = require_file(path)
    if not target.is_file():
        return ""
    return target.read_text(encoding="utf-8")


def load_json(path: str) -> dict:
    target = require_file(path)
    if not target.is_file():
        return {}
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        ERRORS.append(f"invalid JSON in {path}: {exc}")
        return {}


def check_required_files() -> None:
    required = [
        "README.md",
        "README.zh-CN.md",
        "AGENTS.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "SUPPORT.md",
        "CHANGELOG.md",
        "TODO.md",
        "TODO.zh-CN.md",
        ".gitignore",
        ".agents/plugins/marketplace.json",
        ".codex-plugin/plugin.json",
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/workflows/validate.yml",
        "docs/design-principles.md",
        "docs/design-principles.zh-CN.md",
        "docs/write-plan.md",
        "docs/write-plan.zh-CN.md",
        "scripts/validate.py",
        "skills/write-plan/SKILL.md",
        "skills/write-plan/agents/openai.yaml",
    ]
    for path in required:
        require_file(path)


def check_manifests() -> None:
    plugin = load_json(".codex-plugin/plugin.json")
    if plugin:
        expected = {
            "name": "agent-forge",
            "license": "MIT",
            "skills": "./skills/",
        }
        for key, value in expected.items():
            if plugin.get(key) != value:
                ERRORS.append(f".codex-plugin/plugin.json expected {key}={value!r}")
        repository = plugin.get("repository", "")
        if not repository.startswith("https://github.com/"):
            ERRORS.append(".codex-plugin/plugin.json repository should be a GitHub HTTPS URL")
        prompts = plugin.get("interface", {}).get("defaultPrompt", [])
        if not any(str(prompt).startswith("$write-plan ") for prompt in prompts):
            ERRORS.append("plugin default prompts should include a Write Plan invocation example")
        legacy_prompt_flags = ("--low", "--medium", "--high", "--max")
        if any(any(flag in str(prompt) for flag in legacy_prompt_flags) for prompt in prompts):
            ERRORS.append("plugin default prompts should not expose legacy planning preset flags")

    marketplace = load_json(".agents/plugins/marketplace.json")
    plugins = marketplace.get("plugins", []) if marketplace else []
    if len(plugins) != 1:
        ERRORS.append("marketplace should expose exactly one plugin")
        return

    entry = plugins[0]
    source = entry.get("source", {})
    repository = plugin.get("repository", "").rstrip("/") if plugin else ""
    expected_source_url = f"{repository}.git" if repository else ""
    expected_ref = os.environ.get("AGENT_FORGE_EXPECTED_REF")
    actual_ref = source.get("ref")
    checks = {
        "name": entry.get("name") == "agent-forge",
        "source.source": source.get("source") == "url",
        "source.url": source.get("url") == expected_source_url,
        "source.ref": actual_ref == expected_ref
        if expected_ref
        else isinstance(actual_ref, str) and bool(actual_ref.strip()) and "<" not in actual_ref,
    }
    for label, ok in checks.items():
        if not ok:
            ERRORS.append(f"marketplace entry has unexpected {label}")


def check_skill_contract() -> None:
    skill = read_text("skills/write-plan/SKILL.md")
    if not skill.startswith("---\n"):
        ERRORS.append("skills/write-plan/SKILL.md must start with YAML frontmatter")
    else:
        parts = skill.split("---", 2)
        frontmatter = parts[1] if len(parts) > 2 else ""
        for field in ("name: write-plan", "description:"):
            if field not in frontmatter:
                ERRORS.append(f"skills/write-plan/SKILL.md missing frontmatter field {field}")
        if "decision-complete Markdown plans before execution" not in frontmatter:
            ERRORS.append("Write Plan description should mention decision-complete Markdown plans before execution")
    required_skill_markers = [
        "## Purpose",
        "## Constraints",
        "## Workflow",
        "## Asking questions",
        "## Plan Artifact",
        "## Final Response",
        "Treat any execution or modification as executing the plan itself.",
        "Except for creating or updating the final plan artifact, do not perform mutating actions.",
        "Before writing, check whether a relevant local plan already exists.",
        ".agent-work/plan-<short-slug>.md",
        "## Test Plan",
        "decision-complete",
    ]
    for marker in required_skill_markers:
        if marker not in skill:
            ERRORS.append(f"Write Plan skill missing prompt marker: {marker}")

    openai_yaml = read_text("skills/write-plan/agents/openai.yaml")
    for expected in ("display_name:", "short_description:", "default_prompt:"):
        if expected not in openai_yaml:
            ERRORS.append(f"skills/write-plan/agents/openai.yaml missing {expected}")
    if "$write-plan" not in openai_yaml:
        ERRORS.append("skills/write-plan/agents/openai.yaml should expose a $write-plan default prompt")


def check_docs() -> None:
    english_docs = [
        path
        for path in (ROOT / "docs").glob("*.md")
        if not path.name.endswith(".zh-CN.md")
    ]
    for path in english_docs:
        zh = path.with_name(f"{path.stem}.zh-CN.md")
        if not zh.is_file():
            ERRORS.append(f"missing Chinese doc pair for {rel(path)}")

    readme = read_text("README.md")
    readme_zh = read_text("README.zh-CN.md")
    for text, path in ((readme, "README.md"), (readme_zh, "README.zh-CN.md")):
        for token in ("$write-plan", "docs/write-plan", "docs/design-principles", "CONTRIBUTING.md", "LICENSE"):
            if token not in text:
                ERRORS.append(f"{path} missing expected reference: {token}")
        if "--ref v0.1.0" in text:
            ERRORS.append(f"{path} should not recommend an unreleased v0.1.0 tag")

    stale_patterns = (
        "$ralplan",
        "RalPlan",
        "ralplan",
        "--low",
        "--medium",
        "--high",
        "--max",
        "$plan",
        "skills/plan",
        "docs/plan",
        "agent-forge:plan",
        ".agent-work/plans/<slug>/plan.md",
        "Status: Draft",
        "Status: Execution Plan",
        "status: \"draft\"",
        "status: \"final\"",
    )
    docs_to_check = [
        "README.md",
        "README.zh-CN.md",
        "CONTRIBUTING.md",
        "TODO.md",
        "TODO.zh-CN.md",
        "AGENTS.md",
        "docs/write-plan.md",
        "docs/write-plan.zh-CN.md",
        "docs/design-principles.md",
        "docs/design-principles.zh-CN.md",
        "docs/local-plugin-development.md",
        "docs/local-plugin-development.zh-CN.md",
        ".codex-plugin/plugin.json",
    ]
    for path in docs_to_check:
        text = read_text(path)
        for pattern in stale_patterns:
            if pattern in text:
                ERRORS.append(f"{path} contains stale Plan reference: {pattern}")



def check_issue_templates() -> None:
    required_templates = [
        ".github/ISSUE_TEMPLATE/bug_report.yml",
        ".github/ISSUE_TEMPLATE/feature_request.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
    ]
    for path in required_templates:
        require_file(path)


def check_trailing_whitespace() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_TEXT_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            if re.search(r"[ \t]+$", line):
                ERRORS.append(f"trailing whitespace: {rel(path)}:{index}")


def check_portable_text() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_TEXT_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        for index, line in enumerate(lines, start=1):
            for pattern in MACHINE_PATH_PATTERNS:
                if pattern.search(line):
                    ERRORS.append(f"machine-specific path: {rel(path)}:{index}")


def main() -> int:
    check_required_files()
    check_manifests()
    check_skill_contract()
    check_docs()
    check_issue_templates()
    check_trailing_whitespace()
    check_portable_text()

    if ERRORS:
        print("Agent Forge validation failed:")
        for error in ERRORS:
            print(f"- {error}")
        return 1

    print("Agent Forge validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

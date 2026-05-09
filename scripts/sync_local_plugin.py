#!/usr/bin/env python3
"""Prepare and refresh a local Codex plugin development install."""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MARKETPLACE = "agent-forge-local"
EXCLUDED_DIRS = {
    ".agent-work",
    ".codex",
    ".git",
    ".local-marketplace",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
}
EXCLUDED_FILES = {".DS_Store", "*.pyc", "*.pyo"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync this repository into a local Codex plugin marketplace and cache."
    )
    parser.add_argument(
        "--repo-root",
        default=str(ROOT),
        help="Repository root to sync. Defaults to this script's repository.",
    )
    parser.add_argument(
        "--codex-home",
        default=os.environ.get("CODEX_HOME") or str(Path.home() / ".codex"),
        help="Codex home directory. Defaults to CODEX_HOME or ~/.codex.",
    )
    parser.add_argument(
        "--marketplace-name",
        default=DEFAULT_MARKETPLACE,
        help=f"Local marketplace name. Defaults to {DEFAULT_MARKETPLACE}.",
    )
    return parser.parse_args()


def load_plugin(repo_root: Path) -> dict:
    manifest_path = repo_root / ".codex-plugin" / "plugin.json"
    with manifest_path.open("r", encoding="utf-8") as handle:
        plugin = json.load(handle)
    for key in ("name", "version"):
        if not plugin.get(key):
            raise SystemExit(f"Missing {key!r} in {manifest_path}")
    return plugin


def ensure_inside(path: Path, root: Path) -> None:
    path_abs = path.absolute()
    root_abs = root.absolute()
    try:
        path_abs.relative_to(root_abs)
    except ValueError as exc:
        raise SystemExit(f"Refusing to write outside {root_abs}: {path_abs}") from exc


def is_link_or_junction(path: Path) -> bool:
    is_junction = getattr(os.path, "isjunction", lambda value: False)
    return path.is_symlink() or bool(is_junction(path))


def remove_existing(path: Path, allowed_root: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    ensure_inside(path, allowed_root)
    if is_link_or_junction(path):
        if path.is_dir():
            path.rmdir()
        else:
            path.unlink()
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def ignore_names(_directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    for name in names:
        if name in EXCLUDED_DIRS:
            ignored.add(name)
            continue
        if any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDED_FILES):
            ignored.add(name)
    return ignored


def mirror_repo(repo_root: Path, destination: Path, allowed_root: Path) -> None:
    remove_existing(destination, allowed_root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(repo_root, destination, ignore=ignore_names)


def write_marketplace_manifest(
    marketplace_root: Path, marketplace_name: str, plugin_name: str
) -> None:
    manifest = {
        "name": marketplace_name,
        "interface": {"displayName": "Agent Forge Local"},
        "plugins": [
            {
                "name": plugin_name,
                "source": {
                    "source": "local",
                    "path": f"./plugins/{plugin_name}",
                },
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Productivity",
            }
        ],
    }
    target = marketplace_root / ".agents" / "plugins" / "marketplace.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    codex_home = Path(args.codex_home).expanduser().resolve()
    plugin = load_plugin(repo_root)
    plugin_name = plugin["name"]
    version = plugin["version"]

    marketplace_root = codex_home / "local-marketplaces" / args.marketplace_name
    marketplace_plugin = marketplace_root / "plugins" / plugin_name
    cache_plugin = codex_home / "plugins" / "cache" / args.marketplace_name / plugin_name / version

    codex_home.mkdir(parents=True, exist_ok=True)
    write_marketplace_manifest(marketplace_root, args.marketplace_name, plugin_name)
    mirror_repo(repo_root, marketplace_plugin, codex_home)
    mirror_repo(repo_root, cache_plugin, codex_home)

    print("Local Agent Forge plugin synced.")
    print(f"Marketplace root: {marketplace_root}")
    print(f"Marketplace plugin source: {marketplace_plugin}")
    print(f"Plugin cache: {cache_plugin}")
    print("")
    print("Register once if needed:")
    print(f"  codex plugin marketplace add {marketplace_root}")
    print("")
    print("Then enable the plugin in Codex:")
    print(f"  {plugin_name}@{args.marketplace_name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

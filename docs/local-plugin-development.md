# Local Plugin Development

This guide describes a repeatable local workflow for developing Agent Forge without changing the public marketplace manifest. It works on Windows, Linux, and macOS with Python 3 and the Codex CLI.

## What This Is

The public marketplace file at `.agents/plugins/marketplace.json` must keep pointing at the GitHub repository. Do not rewrite it for local testing.

For local development, use a separate marketplace under the Codex home directory:

```text
~/.codex/local-marketplaces/agent-forge-local/
```

The helper script creates that local marketplace and syncs this repository into the Codex plugin cache:

```text
~/.codex/plugins/cache/agent-forge-local/agent-forge/<version>/
```

Codex loads skills from the cache path, so changes in the repository are not visible until you sync and start a fresh session.

## One-Time Setup

From the repository root, sync the local plugin files:

```bash
python3 scripts/sync_local_plugin.py
```

On Windows, `python` may be the command instead:

```powershell
python scripts\sync_local_plugin.py
```

Register the generated local marketplace once.

Windows PowerShell:

```powershell
codex plugin marketplace add "$env:USERPROFILE\.codex\local-marketplaces\agent-forge-local"
```

Linux or macOS:

```bash
codex plugin marketplace add "$HOME/.codex/local-marketplaces/agent-forge-local"
```

Then open Codex, go to `/plugins`, select the `Agent Forge Local` marketplace, and enable `agent-forge`.

## Iteration Loop

After editing source files in this repository:

```bash
python3 scripts/validate.py
git diff --check
python3 scripts/sync_local_plugin.py
```

Windows equivalent:

```powershell
python scripts\validate.py
git diff --check
python scripts\sync_local_plugin.py
```

Open a new Codex session or restart Codex, then test the local skill:

```text
$plan "Test the local Plan skill"
```

Current sessions usually do not reload the available skill list or skill file contents.

## How It Works

The sync script reads `.codex-plugin/plugin.json` to get the plugin name and version. It then writes a local marketplace manifest with this source:

```json
{
  "source": "local",
  "path": "./plugins/agent-forge"
}
```

The script copies this repository to two local Codex-controlled locations:

```text
~/.codex/local-marketplaces/agent-forge-local/plugins/agent-forge/
~/.codex/plugins/cache/agent-forge-local/agent-forge/<version>/
```

The first path lets the local marketplace resolve a valid plugin source. The second path is where Codex reads the installed plugin. The cache copy is intentional because current Codex builds load plugin skills from cache and do not hot-reload files from the repository checkout.

When the plugin loads, `skills/plan/SKILL.md` becomes available as:

```text
agent-forge:plan
```

You can inspect the model-visible skill list with:

```bash
codex debug prompt-input '$plan "test"'
```

## Updating Versions

The cache path includes the version from `.codex-plugin/plugin.json`. After changing the plugin version, run the sync script again. If Codex still shows an older plugin version, remove and re-add the local marketplace, then enable the plugin again.

## Cleanup

To remove the local development marketplace:

```bash
codex plugin marketplace remove agent-forge-local
```

Then delete these local Codex directories if you no longer need the cached files:

```text
~/.codex/local-marketplaces/agent-forge-local/
~/.codex/plugins/cache/agent-forge-local/
```

## Official Status

Local marketplaces and plugin cache loading are Codex plugin mechanisms; see the OpenAI Codex plugin documentation at `https://developers.openai.com/codex/plugins/build`. The `scripts/sync_local_plugin.py` helper is repository tooling for fast local development and is not part of the public installation flow.

Public installation should continue to use:

```bash
codex plugin marketplace add li959598874/agent-forge --ref main
```

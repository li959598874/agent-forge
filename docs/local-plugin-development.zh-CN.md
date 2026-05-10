# 本地插件开发

本文说明如何在不修改公开 marketplace manifest 的前提下本地开发和调试 Agent Forge。流程适用于 Windows、Linux 和 macOS，需要 Python 3 与 Codex CLI。

## 这套流程是什么

公开发布文件 `.agents/plugins/marketplace.json` 必须继续指向 GitHub 仓库。不要为了本地测试把它改成本地路径。

本地开发使用 Codex home 目录下的独立 marketplace：

```text
~/.codex/local-marketplaces/agent-forge-local/
```

辅助脚本会创建这个本地 marketplace，并把当前仓库同步到 Codex 插件缓存：

```text
~/.codex/plugins/cache/agent-forge-local/agent-forge/<version>/
```

Codex 从缓存路径加载 skill，所以修改仓库源码后，需要先同步，再打开新会话或重启 Codex。

## 一次性设置

在仓库根目录同步本地插件文件：

```bash
python3 scripts/sync_local_plugin.py
```

Windows 上命令可能是 `python`：

```powershell
python scripts\sync_local_plugin.py
```

然后注册生成的本地 marketplace。这个步骤只需要做一次。

Windows PowerShell：

```powershell
codex plugin marketplace add "$env:USERPROFILE\.codex\local-marketplaces\agent-forge-local"
```

Linux 或 macOS：

```bash
codex plugin marketplace add "$HOME/.codex/local-marketplaces/agent-forge-local"
```

接着打开 Codex，进入 `/plugins`，选择 `Agent Forge Local` marketplace，并启用 `agent-forge` 插件。

## 迭代流程

每次修改仓库源码后执行：

```bash
python3 scripts/validate.py
git diff --check
python3 scripts/sync_local_plugin.py
```

Windows 对应命令：

```powershell
python scripts\validate.py
git diff --check
python scripts\sync_local_plugin.py
```

然后打开新的 Codex 会话或重启 Codex，再测试本地 skill：

```text
$write-plan "Test the local Write Plan skill"
```

当前已打开的会话通常不会重新加载可用 skill 列表或 skill 文件内容。

## 实现原理

同步脚本读取 `.codex-plugin/plugin.json`，获取插件名称和版本。然后写入一个本地 marketplace manifest，其中插件来源是：

```json
{
  "source": "local",
  "path": "./plugins/agent-forge"
}
```

脚本会把当前仓库复制到两个由 Codex 使用的本地位置：

```text
~/.codex/local-marketplaces/agent-forge-local/plugins/agent-forge/
~/.codex/plugins/cache/agent-forge-local/agent-forge/<version>/
```

第一个路径让本地 marketplace 能解析出合法插件来源。第二个路径是 Codex 实际读取已安装插件的位置。复制到缓存是有意为之，因为当前 Codex 构建会从插件缓存加载 skill，不会直接热加载仓库工作区里的文件。

插件加载后，`skills/write-plan/SKILL.md` 会作为下面的 skill 出现：

```text
agent-forge:write-plan
```

可以用下面的命令查看模型可见的 skill 列表：

```bash
codex debug prompt-input '$write-plan "test"'
```

## 更新版本

缓存路径包含 `.codex-plugin/plugin.json` 中的版本号。修改插件版本后，重新运行同步脚本。如果 Codex 仍显示旧版本，移除并重新添加本地 marketplace，然后再次启用插件。

## 清理

移除本地开发 marketplace：

```bash
codex plugin marketplace remove agent-forge-local
```

如果不再需要缓存文件，可以删除这些本地 Codex 目录：

```text
~/.codex/local-marketplaces/agent-forge-local/
~/.codex/plugins/cache/agent-forge-local/
```

## 官方性

本地 marketplace 和插件缓存加载属于 Codex 插件机制；官方文档见 `https://developers.openai.com/codex/plugins/build`。`scripts/sync_local_plugin.py` 是本仓库为了本地快速开发提供的辅助工具，不属于公开安装流程。

公开安装仍应使用：

```bash
codex plugin marketplace add li959598874/agent-forge --ref main
```

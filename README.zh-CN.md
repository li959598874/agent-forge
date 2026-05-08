# Agent Forge

[English](README.md)

Agent Forge 探索一种更轻量的智能体编排方式。它不把所有请求都塞进重度规划或多代理流程，而是把“需要多少流程”这件事交给用户显式控制，同时保留智能体根据任务复杂度自主判断的能力。

目标很直接：小任务保持小，大任务在确实需要时再进入更深入的澄清、研究和只读探索。

## 安装

将这个 GitHub 仓库添加为 Codex 插件 marketplace：

```bash
codex plugin marketplace add li959598874/agent-forge --ref main
```

然后打开 Codex，并从插件目录安装 Agent Forge：

```text
/plugins
```

选择 `Agent Forge` marketplace，打开 `agent-forge` 插件详情，然后选择 `Install plugin`。

发布 release tag 之后，正式公开安装建议使用 tag，而不是直接安装 `main`：

```bash
codex plugin marketplace add li959598874/agent-forge --ref v0.1.0
```

## 快速上手

在本地仓库中查看当前可用资产：

```bash
cd agent-forge
find .agents .codex-plugin skills -maxdepth 4 -type f
```

当前资产：

| 资产 | 类型 | 说明 |
| --- | --- | --- |
| [.agents/plugins/marketplace.json](.agents/plugins/marketplace.json) | Marketplace manifest | 让 Codex 可以把这个 GitHub 仓库作为插件 marketplace 加载。 |
| [.codex-plugin/plugin.json](.codex-plugin/plugin.json) | Plugin manifest | 声明 Agent Forge 是 Codex 插件，并指向仓库内置 skills。 |
| [ralplan](skills/ralplan/SKILL.md) | Skill | 澄清模糊任务，并通过显式复杂度控制，在用户确认后产出 Markdown 执行计划。 |

## 使用 RalPlan

在兼容 Codex skill 的环境中显式调用：

```text
$ralplan --scale medium --depth standard --name auth-refactor "Plan the authentication refactor"
```

RalPlan 固定遵循同一条流程：

1. 归一化结构化参数、自然语言偏好和隐含意图。
2. 收集最小必要项目上下文。
3. 只询问仍然缺失的澄清问题。
4. 在会话中给出计划草案。
5. 用户确认后写入最终 Markdown 计划。

它的控制面刻意保持很小：

- `--scale auto|tiny|small|medium|large`：控制智能体假定的规划规模。
- `--depth auto|lite|standard|deep`：控制澄清访谈的深度。
- `--agents off|auto|on`：控制是否允许只读子代理探索。
- `--research off|auto|on`：控制是否允许外部研究。

这样可以避免轻量任务被迫进入重流程，同时在任务确实需要时仍能启用更深入的编排。

完整说明见 [docs/ralplan.zh-CN.md](docs/ralplan.zh-CN.md)。

## 仓库结构

```text
.agents/
  plugins/
    marketplace.json # Agent Forge 的 GitHub marketplace 入口
.codex-plugin/
  plugin.json      # Codex 插件 manifest
skills/
  ralplan/          # RalPlan 工作流 skill
docs/
  ralplan.md        # RalPlan 英文说明
  ralplan.zh-CN.md  # RalPlan 中文说明
```

## 扩展方向

本仓库会以增量方式扩展。预留类别：

- `skills/`：可复用 Codex skills，包含 `SKILL.md`、可选 references、模板和 UI 元数据。
- `hooks/`：后续生命周期 hook 或自动化入口。
- `agents/`：后续可复用 agent 角色提示词和协作模式。
- `docs/`：面向人类用户的使用说明和设计说明。

新增内容应保持职责收敛、说明明确、行为可验证。优先增加一个聚焦资产，而不是引入宽泛框架。

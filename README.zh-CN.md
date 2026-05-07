# Agent Forge

[English](README.md)

Agent Forge 是一个用于打造可复用智能体工作流资产的项目，包括 skills、hooks、agent roles、模板和工作流文档。

本项目强调小而清晰的能力模块。每个工作流资产都应该有明确入口、清晰职责边界，并提供足够文档，让人类用户和后续智能体都能在没有隐藏上下文的情况下使用。

## 快速上手

在本地仓库中查看当前可用资产：

```bash
cd agent-forge
find skills -maxdepth 2 -type f
```

当前资产：

| 资产 | 类型 | 说明 |
| --- | --- | --- |
| [ralplan](skills/ralplan/SKILL.md) | Skill | 澄清模糊任务，并在用户确认后产出 Markdown 执行计划。 |

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

完整说明见 [docs/ralplan.zh-CN.md](docs/ralplan.zh-CN.md)。

## 仓库结构

```text
skills/
  ralplan/          # 当前仓库的第一个工作流 skill
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

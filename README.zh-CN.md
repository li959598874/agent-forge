# Agent Forge

[English](README.md)

Agent Forge 是一个面向 Codex 的插件，用 skills 提供一套用户可控、低侵入、可自由组合使用的多智能体工作流编排能力。用户可以按需调用、组合或忽略每个 workflow 原语，而不是把所有请求都塞进同一套固定流程。

核心规则很简单：流程由用户控制，skill 保持可组合，智能体编排只有在能提升结果时才增加结构。

## 项目初衷

现有智能体编排工作流有价值，但常见问题是把所有请求都放进固定流程。这样会带来不必要的 token 消耗，让小任务变得笨重，也可能干扰用户已有的 skills 或本地工作流。

Agent Forge 围绕四个约束构建：

- **用户可控流程**：workflow 是显式调用的 skills，而不是隐藏拦截规则。
- **低侵入性**：插件只提供 skills 和文档，不改 hook、全局配置或无关工具。
- **Skill 自由组合**：每个 skill 只解决一个 workflow 问题，并能和用户自己的 skills 并行使用。
- **多智能体编排**：当任务受益于并行上下文时，子代理可作为探索、风险复核、测试、文档研究或未来 workflow 角色的可选通道。

## 当前状态

本仓库当前发布一个插件和一个 skill：

| 资产 | 作用 |
| --- | --- |
| `agent-forge` plugin | Agent Forge 工作流资产的 Codex 插件封装。 |
| `$write-plan` skill | 在开始实现之前创建决策完整的 Markdown 计划。 |

Write Plan 是当前工作流原语。后续新增资产应遵循同一合同：显式调用、默认低仪式感、能和其他 skills 清晰组合，并且不在请求范围外制造惊喜变更。

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

发布稳定 release tag 之后，公开安装建议使用固定 release ref，而不是直接使用 `main`：

```bash
codex plugin marketplace add li959598874/agent-forge --ref <release-tag>
```

## 快速上手

在兼容 Codex skill 的环境中显式调用 Write Plan：

```text
$write-plan "Plan the authentication refactor before editing files"
```

自然语言约束是请求的一部分：

```text
$write-plan "Plan the logging cleanup. Keep compatibility risks visible."
```

范围较宽的工作可以直接在任务文本中说明需要的规划深度：

```text
$write-plan "Create a decision-complete plan for the plugin release process. Inspect local docs and manifests first."
```

Write Plan 会保存一份本地 Markdown 产物：

```text
.agent-work/plan-<short-slug>.md
```

## 工作流

Write Plan 将规划和实现分开：

1. 以非变更方式探索本地环境。
2. 只询问会改变计划、确认重要假设，或在真实取舍之间做选择的问题。
3. 把实现形态说明到另一个工程师或 agent 可以执行的程度。
4. 保存决策完整的 Markdown 计划。
5. 简短回复计划路径和必要注意事项。

完整 Write Plan 说明见 [docs/write-plan.zh-CN.md](docs/write-plan.zh-CN.md)。设计原则见 [docs/design-principles.zh-CN.md](docs/design-principles.zh-CN.md)。

## 仓库结构

```text
.agents/
  plugins/
    marketplace.json        # Agent Forge 的 GitHub marketplace 入口
.codex-plugin/
  plugin.json               # Codex 插件 manifest
.github/
  ISSUE_TEMPLATE/           # GitHub issue 表单
  workflows/validate.yml    # 仓库校验工作流
docs/
  design-principles.md      # 工作流理念和防漂移约束
  design-principles.zh-CN.md
  write-plan.md             # Write Plan 英文说明
  write-plan.zh-CN.md       # Write Plan 中文说明
scripts/
  validate.py               # 仓库本地校验
skills/
  write-plan/               # Write Plan 工作流 skill
```

## 开发

当前没有编译型构建步骤。使用以下命令校验仓库结构、manifest、文档和 skill 合同：

```bash
python3 scripts/validate.py
```

仓库自带校验器已经包含 skill 包装检查。如果你使用外部 Codex skill 校验器，请按该校验器自己的安装路径运行。

同时运行：

```bash
git diff --check
```

本地插件开发和调试流程见 [docs/local-plugin-development.zh-CN.md](docs/local-plugin-development.zh-CN.md)。

## 贡献

提交 issue 或 pull request 前，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。影响公开行为的变更应同步更新英文和中文文档。

## 许可证

Agent Forge 使用 [MIT License](LICENSE) 发布。

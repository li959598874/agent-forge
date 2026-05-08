# Agent Forge

[English](README.md)

Agent Forge 是一个面向 Codex 的轻量智能体工作流编排插件。它把“任务需要多少流程”的控制权交给用户显式配置，同时在用户使用 `auto` 时，允许 Codex 根据任务证据做保守的默认判断。

核心规则很简单：小任务保持小；复杂工作在确实需要时，再进入更深入的澄清、带研究支撑的只读探索和可持久保存的本地计划。

## 项目初衷

现有智能体编排工作流有价值，但常见问题是把所有请求都放进重流程。这样会带来不必要的 token 消耗，让小任务变得笨重，也可能干扰用户已有的 skills 或本地工作流。Codex plan 模式足够轻量，但默认不会把计划产物写入仓库。

Agent Forge 围绕三个约束构建：

- **显式流程预算**：用户可以控制任务规模、澄清深度、子代理使用和带研究支撑的探索。
- **自适应默认值**：当控制项为 `auto` 时，只有任务证据确实需要，agent 才升级流程。
- **低侵入性**：插件只提供 skills 和文档，不改用户 hook、全局配置或无关工具。

## 当前状态

本仓库当前发布一个插件和一个 skill：

| 资产 | 作用 |
| --- | --- |
| `agent-forge` plugin | Agent Forge 工作流资产的 Codex 插件封装。 |
| `$ralplan` skill | 澄清模糊任务，并写入经过用户确认的 Markdown 执行计划。 |

RalPlan 是第一个工作流原语。后续新增资产应遵循同一合同：显式控制、默认低仪式感、需要持久化时写入本地产物，并且不在请求范围外制造惊喜变更。

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

在兼容 Codex skill 的环境中显式调用 RalPlan：

```text
$ralplan --scale medium --depth standard --agents auto --name auth-refactor "Plan the authentication refactor"
```

轻量任务可以降低流程预算：

```text
$ralplan --scale small --depth lite --agents off "Plan the logging cleanup"
```

或：

```text
$ralplan 保持 logging cleanup 轻量，不使用子代理。
```

架构或迁移类任务可以启用更深澄清和官方来源研究：

```text
$ralplan --scale large --depth deep --agents on "Plan the plugin release process"
```

或：

```text
$ralplan 为 plugin release process 制定一份深入计划，并使用子代理做宽范围探索。
```

RalPlan 只会在用户确认后写入最终计划：

```text
.agent-work/plans/<slug>/plan.md
```

## 控制项

| 参数 | 取值 | 作用 |
| --- | --- | --- |
| `--scale` | `auto`, `tiny`, `small`, `medium`, `large` | 设置预期规划面和产物完整度。 |
| `--depth` | `auto`, `lite`, `standard`, `deep` | 设置澄清访谈深度。 |
| `--agents` | `off`, `auto`, `on` | 控制是否允许只读子代理探索。 |
| `--research` | `off`, `auto`, `on` | 控制带研究支撑的证据链路。默认值：`auto`。 |
| `--dir` | 路径 | 设置计划输出根目录。默认值：`.agent-work`。 |
| `--name` | slug | 设置计划目录名。 |

完整 RalPlan 说明见 [docs/ralplan.zh-CN.md](docs/ralplan.zh-CN.md)。设计原则见 [docs/design-principles.zh-CN.md](docs/design-principles.zh-CN.md)。

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
  ralplan.md                # RalPlan 英文说明
  ralplan.zh-CN.md          # RalPlan 中文说明
scripts/
  validate.py               # 仓库本地校验
skills/
  ralplan/                  # RalPlan 工作流 skill
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

## 贡献

提交 issue 或 pull request 前，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。影响公开行为的变更应同步更新英文和中文文档。

## 许可证

Agent Forge 使用 [MIT License](LICENSE) 发布。

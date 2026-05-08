# Plan

[English](plan.md)

Plan 是一个规划类 skill，用于把模糊的软件或工作流请求转化为经过用户确认的 Markdown 执行计划。它的职责刻意保持狭窄：澄清需求、生成草案、等待确认，然后把同一份本地 Markdown 文件升级为执行计划。它不实现代码、不做最终 review、不提交 git，也不创建并行的 JSON handoff 文件。

Plan 是 Agent Forge 的第一个工作流原语。它落实 [design-principles.zh-CN.md](design-principles.zh-CN.md) 中的项目原则：只使用任务真正需要的流程。

## Skill 位置

```text
skills/plan/
  SKILL.md
  agents/openai.yaml
```

## 适用场景

只有用户明确要求规划时，才使用 Plan：

- 用户显式调用 `$plan`。
- 用户明确要求在实现前制定计划。
- 用户明确要求生成可持久保存、后续可执行的计划文件。

当用户只是要求一般澄清、立即实现、最终代码 review、提交 commit 或只询问信息时，不应使用 Plan。

## 调用方式

Plan 支持预设参数，同时也接受自然语言指令和隐含意图。

```text
$plan [--low|-l|--medium|-m|--high|-h|--max|-x] "<task>"
```

示例：

```text
$plan --low "Plan a logging cleanup"
```

```text
$plan -m "Plan the authentication refactor"
```

```text
$plan --high "Plan the plugin release process"
```

```text
$plan -x "Plan this architecture migration"
```

自然语言控制也有效：

```text
$plan 保持轻量，不要使用子代理。规划一下如何清理 logging 模块。
```

```text
$plan 为 plugin release process 制定一份深入计划，并使用子代理做宽范围探索。
```

## 预设归一化

工作流第一步是从以下来源归一化预设：

1. 结构化预设参数。
2. 明确的自然语言偏好。
3. 从任务中推断出的隐含意图。
4. agent 的智能默认判断。

skill 必须在继续后续流程前，在会话中显式回显解析结果：

```text
Normalized Plan preset:
- preset: medium (inferred from cross-module scope)
```

如果用户没有提供预设，则完全由 agent 判断。如果某个推断选择会实质影响流程且不确定，agent 应先询问用户。

## 预设

| 预设 | 缩写 | 作用 |
| --- | --- | --- |
| `--low` | `-l` | 最少本地 grounding，只问阻塞问题。 |
| `--medium` | `-m` | 面向普通 feature、cleanup 或跨文件工作的标准规划。 |
| `--high` | `-h` | 更深探索、分阶段澄清，并在可用时使用只读子代理。 |
| `--max` | `-x` | 宽范围探索，可用时使用只读多智能体 research/critic lanes，并进行深度确认。 |

预设是流程上限，不是配额。需求已经很详细的高风险任务可以快速推进；描述很粗的小任务也仍然可能需要一两个边界问题。

## 工作流

Plan 固定遵循带确认门的草案到计划流程：

1. 归一化预设，并在会话中回显。
2. 读取项目说明、顶层结构、manifest、测试入口和直接相关文件进行 grounding。
3. 只询问尚未解决的澄清问题。
4. 写入带 `Status: Draft` 的草案文件。
5. 汇报草案摘要、路径和需要确认的决策。
6. 等待用户确认或修订。
7. 把同一份 Markdown 文件升级为 `Status: Execution Plan`。
8. 汇报计划路径和剩余假设或验证缺口。

如果用户说“只要草案”或“先别写文件”，Plan 应在当前轮停在升级步骤之前。

## 澄清问题

问题必须足够清楚，避免用户在不理解取舍的情况下被迫选择。每个问题都需要：

- 清晰的问题文本。
- 有意义的选项标签。
- 一句选项说明。
- 允许用户自己输入答案的方式。

当宿主提供 `request_user_input` 时，使用该工具并依赖其自由输入选项。纯文本场景下，应显式加入 `用户自己输入答案` 选项。

## 计划产物

Plan 写入一份产物：

```text
.agent-work/plans/<slug>/plan.md
```

slug 根据任务自动生成。如果路径已存在，除非用户明确要求继续该草案，否则 Plan 会选择安全后缀。

每份产物使用稳定外壳：

- `Status: Draft` 或 `Status: Execution Plan`

Plan 不创建：

- `draft.md`
- `plan.json`
- handoff JSON
- state JSON
- `.gitignore`

人类用户和后续智能体都应阅读同一份 Markdown 文件。

## 自适应正文

Plan 不要求固定正文标题。agent 应根据任务和预设选择易读的 Markdown 结构。

草案内容必须覆盖需求描述、关键决策、建议或取舍、开放问题和确认门。

执行计划内容必须覆盖目标和非目标、已确认决策和假设、执行方案、验证方式、相关风险和回滚、开放问题或 `None`，以及意图漂移检查。

## 开发说明

使用以下命令校验仓库和 skill 包装：

```bash
python3 scripts/validate.py
```

如果你使用外部 Codex skill 校验器，请按该校验器自己的安装路径运行。

修改 Plan 时，将核心提示词保留在 `SKILL.md`。除非提示词大到难以安全维护，否则不要把工作流规则或产物规则拆到额外文件中。

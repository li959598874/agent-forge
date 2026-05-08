# RalPlan

[English](ralplan.md)

RalPlan 是一个规划类 skill，用于把模糊的软件或工作流请求转化为经过用户确认的 Markdown 执行计划。它的职责刻意保持狭窄：澄清需求、制定计划、在确认后写入一份计划文件。它不实现代码、不做最终 review、不提交 git，也不创建并行的 JSON handoff 文件。

RalPlan 是 Agent Forge 的第一个工作流原语。它落实 [design-principles.zh-CN.md](design-principles.zh-CN.md) 中的项目原则：只使用任务真正需要的流程。

## Skill 位置

```text
skills/ralplan/
  SKILL.md
  agents/openai.yaml
  references/workflow.md
  references/plan-markdown.md
  assets/plan-template.md
```

## 适用场景

只有用户明确要求规划时，才使用 RalPlan：

- 用户显式调用 `$ralplan`。
- 用户明确要求在实现前制定计划。
- 用户明确要求生成可持久保存、后续可执行的计划文件。

当用户只是要求一般澄清、立即实现、最终代码 review、提交 commit 或只询问信息时，不应使用 RalPlan。

## 调用方式

RalPlan 支持 CLI 风格参数，同时也接受自然语言指令和隐含意图。

```text
$ralplan [--scale auto|tiny|small|medium|large]
         [--depth auto|lite|standard|deep]
         [--agents off|auto|on]
         [--research off|auto|on]
         [--dir .agent-work]
         [--name <slug>]
         "<task>"
```

示例：

```text
$ralplan --scale small --depth lite --agents off "Plan a logging cleanup"
```

```text
$ralplan --scale medium --depth standard --agents auto --name auth-refactor "Plan the authentication refactor"
```

```text
$ralplan --scale large --depth deep --agents on "Plan the plugin release process"
```

自然语言控制也有效：

```text
$ralplan 保持轻量，不要使用子代理。规划一下如何清理 logging 模块。
```

```text
$ralplan 做一份深入架构计划，草案前先检查最新官方文档。
```

## 参数归一化

工作流第一步是从三类来源归一化参数：

1. 结构化 CLI 风格参数。
2. 明确的自然语言偏好。
3. 从任务中推断出的隐含意图。

skill 必须在继续后续流程前，在会话中显式回显解析结果：

```text
Normalized RalPlan options:
- scale: medium (inferred from cross-module scope)
- depth: standard (natural language requested a normal plan)
- agents: auto (default)
- research: on (default)
- dir: .agent-work (default)
- name: auth-refactor (derived)
```

优先级为：结构化参数最高，其次是明确自然语言，再其次是隐含意图，最后是默认值。如果某个推断值会实质影响流程且不确定，agent 应先询问用户。

## 参数说明

### `--scale`

控制规划规模和产物丰富度。

- `auto`：从任务自动推断。
- `tiny`：局部、低风险、容易回滚的任务。
- `small`：范围较窄、不确定性有限的任务。
- `medium`：跨文件或跨模块，且存在实质歧义的规划。
- `large`：架构、迁移、多阶段或高风险规划。

### `--depth`

控制访谈细致程度。

- `auto`：根据任务复杂度和需求描述细致程度自动推断。
- `lite`：只问阻塞问题。
- `standard`：问到足以冻结范围和验收标准。
- `deep`：深入追问目标、非目标、备选方案、风险、发布和验证。

### `--agents`

控制是否允许只读子代理探索。

- `off`：不使用子代理。
- `auto`：由 agent 根据任务事实自主判断；本地 grounding 足够时保持本地处理。
- `on`：对宽范围或读密集工作，优先使用子代理探索。

启用后，RalPlan 围绕独立证据链路组织只读探索，例如模块、仓库、架构层、来源类型、风险或 critic pass。使用 `on` 时，主代理应在草案前展开有价值的探索链路，并保留自身上下文用于综合。RalPlan 不把写入任务委派给子代理。

### `--research`

控制带研究支撑的证据链路。默认值：`on`。

- `off`：不浏览、不使用外部来源。
- `auto`：由 agent 判断是否需要来源核验。
- `on`：保持来源核验可用，优先官方文档和一手来源。

Research 通常在子代理探索中执行。如果当前环境无法使用子代理，主代理可以执行最小必要来源核验，并在 Evidence 中记录来源。

### `--dir`

设置最终计划的工作目录。默认值：

```text
.agent-work
```

### `--name`

设置计划 slug。如果省略，RalPlan 会根据任务生成小写连字符 slug。

## 工作流

RalPlan 固定遵循带确认门的写入流程：

1. 归一化参数，并在会话中回显。
2. 最小 grounding：读取项目说明、顶层结构、manifest、测试入口和直接相关文件。
3. 根据变更面、歧义度、失败代价和验证宽度判断任务复杂度。
4. 判断用户需求描述已经有多细致。
5. 只询问尚未解决的澄清问题。
6. 在会话中给出计划草案。
7. 等待用户确认。
8. 写入最终 Markdown 计划。
9. 汇报计划路径和剩余假设或验证缺口。

如果用户说“只要草案”或“先别写文件”，RalPlan 应在当前轮停在 approval/write 步骤之前。这不是一个独立模式参数。

## 访谈深度

访谈深度同时取决于任务复杂度和需求描述细致程度。

需求描述细致程度：

- `high detail`：用户已经提供目标、非目标、约束、验收标准、相关文件和偏好取舍。
- `medium detail`：用户提供了清晰目标和部分约束，但验收、风险或边界仍不完整。
- `low detail`：用户只提供意图，没有提供范围、成功标准、约束或授权边界。

问题数量应按比例控制：

| 规模 | 典型问题数 |
| --- | --- |
| `tiny` | 0-2 |
| `small` | 1-3 |
| `medium` | 2-5 |
| `large` | 分阶段访谈 |

这是上限，不是配额。大任务如果需求已经非常清楚，不应进行形式化的冗长访谈。小任务如果需求描述很粗，也仍然需要先澄清边界和验收标准。

## 子代理策略

只有当前环境允许，且子代理能明显保护主上下文质量时，才使用子代理。

默认行为：

- `off`：不使用子代理。
- `auto`：由 agent 根据任务证据判断；`tiny` 和 `small` 通常保持本地处理，更宽的工作可拆分为证据链路。
- `on`：宽范围或读密集发现任务优先使用子代理，并按模块、子系统、来源类型、风险区域、官方文档研究或 critic pass 拆分。

子代理应返回简洁事实、证据、文件路径、来源链接、风险和置信度。主代理保护上下文质量，负责综合计划和所有用户沟通。

## 计划产物

RalPlan 只写入一个最终产物：

```text
.agent-work/plans/<slug>/plan.md
```

使用 `--dir` 修改 `.agent-work`。使用 `--name` 修改 `<slug>`。

RalPlan 不创建：

- `plan.json`
- handoff JSON
- state JSON
- `.gitignore`

人类用户和后续智能体都应阅读同一份 Markdown 文件。

如果目标 `plan.md` 已存在，agent 不得静默覆盖。应询问用户是替换文件，还是选择新的 slug。

## 计划章节

最终计划应遵循 `skills/ralplan/assets/plan-template.md`，并包含：

1. Task
2. Process Budget
3. Goals
4. Non-Goals
5. Evidence
6. Decisions
7. Assumptions
8. Execution Slices
9. Validation
10. Risks And Rollback
11. Open Questions
12. Intent Drift Check

Evidence 章节很重要。它记录本轮读取过的本地文件、用于发现的命令、使用过的官方文档或一手来源，以及某条判断是观察事实还是推断。它替代任何单独的机器可读 handoff。

## 开发说明

使用以下命令校验仓库和 skill 包装：

```bash
python3 scripts/validate.py
```

如果你使用外部 Codex skill 校验器，请按该校验器自己的安装路径运行。

修改 RalPlan 时，保持 `SKILL.md` 简洁。详细流程规则放到 `references/`，面向用户的说明放在本文档中。

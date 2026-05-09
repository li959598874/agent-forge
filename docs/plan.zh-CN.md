# Plan

[English](plan.md)

Plan 是一个 Codex skill，用于在执行前产出本地实施计划。它先探索当前环境，只澄清会实质影响计划的决策，写入草案，等待用户确认，然后把同一份 Markdown 文件升级为最终 checklist。

Plan 默认只做规划。除非用户明确要求实现，否则它只修改计划文件，不修改源码。

## Skill 包

```text
skills/plan/
  SKILL.md
  agents/openai.yaml
  assets/
    draft-plan-template.md
    final-plan-template.md
```

## 调用方式

当用户显式调用 `$plan`、要求先规划再实现，或需要一份后续可执行的本地 checklist 时，使用 Plan。

```text
$plan "Plan the authentication refactor"
```

自然语言约束是请求的一部分：

```text
$plan "Plan the release process. Use read-only subagents if the repository scope is broad."
```

```text
$plan "Plan the logging cleanup and write the plan under .agent-work/planning."
```

## 文件规则

除非用户指定其他目录，Plan 将文件写入 `.agent-work/`。默认文件名是：

```text
<yyyyMMdd-HHmm>-<task-slug>.plan.md
```

如果存在匹配草案，Plan 会更新该草案，而不是创建重复文件。每个计划始终保留在一个 Markdown 文件中。草案使用 `status: "draft"`；确认后的版本会在同一文件中替换为 `status: "final"`。

草案使用 `skills/plan/assets/draft-plan-template.md`。最终计划使用 `skills/plan/assets/final-plan-template.md`。

## 工作流

1. 先基于本地事实做 grounding，再提问。
2. 检查相关说明、目录结构、manifest、schema、类型、测试、fixture、文档、生成源码边界和现有模式。
3. 只有当前或版本敏感事实、平台规则、API、官方文档、标准，或不能依赖记忆的行为会影响计划时，才使用外部研究。
4. 只询问无法通过探索回答、且影响较高的问题。
5. 写入或更新草案计划，包含 Approach Overview、Key Decisions、Open Questions and Optimization Ideas。
6. 要求用户确认或修订草案方向。
7. 用户明确确认后，将同一份文件重写为最终计划，包含 summary、assumptions、execution checklist、validation checklist、risks、safeguards 和 completion criteria。
8. 汇报计划路径和状态；除非用户要求，不在对话中重复完整本地计划。

## 澄清问题

问题应锁定有意义的决策、确认重要假设，或在真实取舍之间做选择。当 `request_user_input` 可用时，用它处理会改变计划的决策。在纯文本场景中，只有当合理的多选形式会误导用户时，才直接提出自由文本问题。

不要询问本地检查可以回答的问题。不要用“是否继续”替代草案确认。

## Subagent Rules

当宽范围探索会稀释主 agent 上下文时，将子代理用作窄范围、只读的规划通道。常见通道包括代码地图、测试地图、风险复核和官方文档研究。

探索子代理应优先使用当前环境可用的最新版、快速、便宜的模型。要求每个子代理返回简洁发现、相关路径或 URL、置信度和未解决问题。

主 agent 始终负责用户沟通、产品决策、综合和计划文件。子代理不应决定产品意图、最终确定取舍、写计划、实现代码或修改仓库文件。

## 质量标准

草案应说明方案方向，列出支撑性的仓库事实，区分已确认决策和建议默认值，将开放问题限制在阻塞项，并把可选优化标记为非阻塞。

最终计划应达到决策完备，另一个工程师或 agent 不依赖隐藏对话上下文也能执行。Checklist 条目应以命令式动词开头，并包含具体的验证命令、测试、人工检查或 review 标准。

## 校验

使用以下命令校验仓库和 skill 包装：

```bash
python3 scripts/validate.py
```

同时运行：

```bash
git diff --check
```

如果你使用外部 Codex skill 校验器，请按该校验器自己的安装路径运行。

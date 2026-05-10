# Write Plan

Write Plan 用于在开始实现之前创建一份决策完整的 Markdown 计划。它是显式规划 workflow：用户要求先写计划，agent 先基于可用环境建立事实基础，补齐意图和实现决策，然后写入一份本地计划产物，使另一个工程师或 agent 不依赖隐藏对话上下文也能执行。

当任务范围较宽、存在歧义、风险较高、跨多个模块，或需要先达成共识再修改源码时使用它。对于很小的直接修改、快速问答，或用户已经明确要求立即实现的工作，不需要先进入 Write Plan。

## 调用方式

在兼容 Codex skill 的环境中显式调用：

```text
$write-plan "Plan the authentication refactor before editing files"
```

自然语言约束是请求的一部分：

```text
$write-plan "Plan the billing export change. Keep compatibility risks visible."
```

范围更大的工作，可以直接在任务文本中说明需要的深度：

```text
$write-plan "Create a decision-complete plan for the plugin release process. Inspect local docs and manifests first."
```

## 行为合同

Write Plan 将规划和执行分开：

1. 用非变更动作探索相关本地上下文。
2. 从文件、配置、schema、测试、日志和当前实现中解析可发现事实。
3. 只询问会实质改变计划、确认重要假设，或在真实取舍之间做选择的问题。
4. 把实现形态定义到可以执行的程度：范围、成功标准、关键变更、接口、数据流、边界情况、测试、发布和兼容约束等。
5. 写入一份本地 Markdown 计划产物。
6. 简短回复计划路径和必要注意事项。

除了创建或更新计划产物之外，这个 workflow 不编辑 repo-tracked 文件、不应用 patch、不运行会重写文件的 formatter、不执行迁移，也不开始实现计划。

## 探索规则

除非没有本地环境，或请求本身互相矛盾，否则先进行有目标的检查。能从仓库里回答的事实，不应转问用户。

可发现事实包括路径、现有 API、schema、配置值、测试布局、依赖选择和当前行为。检查后如果仍有多个合理答案，再带着具体候选项和推荐默认值询问用户。

偏好和取舍不同。涉及用户意图时应尽早询问，例如兼容策略、可接受迁移成本、发布风险、UX 优先级，或哪个约束更重要。

## 计划产物

使用用户当前对话语言写计划。写入前先检查是否已经存在相关本地计划；如果存在，询问用户是继续细化原计划，还是新建计划。

默认路径：

```text
.agent-work/plan-<short-slug>.md
```

slug 使用简短的小写连字符命名，例如 `auth-timeout`、`checkout-copy` 或 `dash-counter`。

除非任务需要额外章节，使用下面的基础结构：

```markdown
# <清晰标题>

## Summary
- <目标、成功标准、当前状态和预期结果>

## Key Changes
- <按子系统或行为分组的实现变更>
- <重要 API、接口、类型、数据结构或 I/O 变更>

## Test Plan
- <测试、手动验收场景和校验命令>

## Assumptions
- <假设、默认值，以及已接受但未完全解决的约束>
```

当额外章节能避免执行错误时，可以加入 `Risks`、`Edge Cases`、`API / Data Shape` 或 `Migration / Compatibility`。计划应紧凑并可直接执行：按行为分组，只在能减少歧义时写具体路径或符号，不要发明用户没有要求的策略。

## 组合方式

Write Plan 是上游 workflow 原语。它产出一份持久的本地计划，供人类、基础 agent 或其他 workflow skill 后续执行。其他 skill 可以把这份计划作为上下文，但不能把它当作越过用户请求范围修改文件的授权。


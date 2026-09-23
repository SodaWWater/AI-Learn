# 02｜工程案例 1：自动恢复为什么会把 Agent 变成“无限烧钱机器”

> 本章只解决一个问题：
>
> **Agent 为了自动恢复错误而 continue，但如果它忘了自己已经恢复过，就可能永远转不出来。**
>
> 这一章学透以后，再看到 State、Retry、Guard、transition、Circuit Breaker 这些词就不会觉得抽象。

---

# 1. 先从一个真实开发事故开始

假设我们自己写了一个 Agent：

~~~ts
while (true) {
  const response = await callModel(messages)

  if (response.error === "prompt_too_long") {
    messages = await compact(messages)
    continue
  }

  ...
}
~~~

第一眼看非常合理：

> Context 太长 → 压缩 → 再试一次。

问题在于：

> 压缩以后如果还是太长呢？

执行会变成：

~~~text
模型请求
↓
prompt_too_long
↓
compact
↓
continue

模型请求
↓
还是 prompt_too_long
↓
又 compact
↓
continue

模型请求
↓
还是 prompt_too_long
↓
又 compact
↓
...
~~~

程序没有 Crash。

日志里甚至会不断出现“正在恢复”。

但实际上：

> Agent 已经进入无限恢复循环，并持续消耗 API、Token、时间和钱。

这类问题比直接 throw Error 更危险，因为它表面上“还活着”。

---

# 2. 为什么 Demo 很容易写出这个 Bug

因为写 Demo 时，我们往往只关心：

~~~text
当前发生了什么？
~~~

例如：

~~~text
现在 Context 太长。
~~~

然后立即做：

~~~text
那我 Compact。
~~~

但生产 Runtime 还必须知道：

~~~text
我之前已经做过什么？
这次继续是因为什么？
这个恢复动作已经尝试过几次？
~~~

也就是说：

> 循环里的“下一步决策”，不仅依赖当前输入，还依赖前几轮留下的执行状态。

---

# 3. 什么叫 State

现在再引入第一个专业词。

**State（状态）**：

> Runtime 为了让下一轮知道“前面发生过什么”，显式保存的一组数据。

当前源码里 queryLoop 有一个集中 State，大致包含：

~~~ts
type State = {
  messages
  toolUseContext
  autoCompactTracking
  maxOutputTokensRecoveryCount
  hasAttemptedReactiveCompact
  maxOutputTokensOverride
  pendingToolUseSummary
  stopHookActive
  turnCount
  transition
}
~~~

这不是说你现在要背九个字段。

我们先只挑四个：

~~~text
turnCount
hasAttemptedReactiveCompact
maxOutputTokensRecoveryCount
transition
~~~

它们分别回答四种问题：

| 字段 | 人话 |
|---|---|
| turnCount | Agent 已经跑到第几轮？ |
| hasAttemptedReactiveCompact | 这条恢复路径是不是已经试过？ |
| maxOutputTokensRecoveryCount | 输出截断已经恢复几次？ |
| transition | 上一次为什么选择继续循环？ |

---

# 4. 先解决最简单的：同一个恢复动作只能做一次

刚才的 Bug：

~~~text
prompt_too_long
→ compact
→ retry
→ prompt_too_long
→ compact
→ retry
→ ...
~~~

可以增加：

~~~text
hasAttemptedReactiveCompact
~~~

这个名字看起来长，拆开就是：

~~~text
has Attempted
= 是否已经尝试过

Reactive Compact
= 收到真实“上下文太长”错误以后临时触发的压缩
~~~

所以整句话就是：

> “是否已经尝试过一次错误后的临时压缩。”

---

## 4.1 修复前

~~~ts
if (promptTooLong) {
  compact()
  continue
}
~~~

无记忆。

---

## 4.2 修复后

~~~ts
if (promptTooLong && !state.hasAttemptedReactiveCompact) {
  const compacted = await compact()

  state = {
    ...state,
    messages: compacted,
    hasAttemptedReactiveCompact: true
  }

  continue
}

if (promptTooLong && state.hasAttemptedReactiveCompact) {
  return "prompt_too_long"
}
~~~

第一次：

~~~text
hasAttemptedReactiveCompact = false

↓ 压缩

hasAttemptedReactiveCompact = true

↓ retry
~~~

第二次还失败：

~~~text
看到 true
↓
不再重复 Compact
↓
承认恢复失败
↓
退出
~~~

这就是一个 **Guard**。

---

# 5. 什么叫 Guard

Guard 可以翻成：

> **保护条件 / 闸门条件。**

作用是：

> 在执行一个危险或不可重复的动作前，先检查“现在还允许不允许做”。

例如：

~~~text
if 还没恢复过
    → 允许恢复

if 已经恢复过
    → 禁止再次恢复
~~~

所以不要把 Guard 当成某个 Claude Code 专属技术。

本质就是一个：

~~~text
防止同一动作无限重复的条件判断。
~~~

---

# 6. 为什么只用一个 Boolean 还不够

有些恢复允许：

~~~text
最多一次
~~~

Boolean 很合适。

但有些恢复允许：

~~~text
最多三次
~~~

例如模型输出因为 max_output_tokens 被截断。

这时需要：

~~~text
maxOutputTokensRecoveryCount
~~~

即：

> 已经尝试恢复几次。

假设：

~~~text
RecoveryCount = 0
~~~

第一次截断：

~~~text
RecoveryCount = 1
continue
~~~

第二次：

~~~text
RecoveryCount = 2
continue
~~~

第三次：

~~~text
RecoveryCount = 3
continue
~~~

再失败：

~~~text
达到 MAX_OUTPUT_TOKENS_RECOVERY_LIMIT
↓
停止自动恢复
↓
把错误真正暴露出去
~~~

当前源码中这个上限是：

~~~text
MAX_OUTPUT_TOKENS_RECOVERY_LIMIT = 3
~~~

---

# 7. Retry 到底是什么

现在再给一个常见词命名。

**Retry（重试）**：

> 某次操作失败后，再尝试执行一次。

例如：

~~~text
API 请求失败
↓
Retry API
~~~

或者：

~~~text
调整输出上限
↓
Retry 同一个模型请求
~~~

问题是：

> Retry 不能等于 while(true)。

生产级 Retry 至少需要回答：

1. 什么错误可以重试？
2. 重试前要不要修改状态？
3. 最多几次？
4. 每次失败后怎么记录？
5. 最终失败返回什么？

这就是为什么简单一句：

~~~text
失败就重试
~~~

远远不够。

---

# 8. 为什么 State 要集中放，而不是到处写变量

假设我们自己写：

~~~ts
let compacted = false
let retryCount = 0
let stopHookActive = false
let turn = 1
let someOtherFlag = false
...
~~~

然后 1000 行 queryLoop 到处：

~~~text
if (...)
  retryCount++

if (...)
  compacted = false

if (...)
  stopHookActive = true
~~~

运行十几轮后，如果它又 continue 了：

> 你很难回答“到底是谁让它继续的？”

所以当前 queryLoop 使用集中 State，并且每个继续分支构造一个新的 next State。

学习上可以理解为：

~~~ts
const next = {
  messages: ...,
  turnCount: ...,
  hasAttemptedReactiveCompact: ...,
  transition: {
    reason: "reactive_compact_retry"
  }
}

state = next
continue
~~~

重点不是“不可变编程”这些词。

重点是：

> 每次继续循环时，都把“下一轮现场”完整写出来。

---

# 9. transition 是什么，为什么非常值得学

transition 直译是：

> 状态转换。

但这里你只需要理解成：

> “上一轮到底为什么又 continue 了？”

例如当前源码里可能记录：

~~~text
next_turn
reactive_compact_retry
collapse_drain_retry
max_output_tokens_recovery
max_output_tokens_escalate
stop_hook_blocking
token_budget_continuation
~~~

不要背。

看它解决什么。

假设：

~~~text
上一轮因为 Context Collapse 已经恢复过一次
↓
这一轮还是 413
~~~

Runtime 需要知道：

> “我刚才已经走过 collapse recovery 了，这次不能再走同一条路。”

于是可以判断：

~~~text
state.transition.reason === "collapse_drain_retry"
~~~

从而跳过重复动作。

---

# 10. 一个真实的死循环：Stop Hook + Compact

当前源码注释里记录了一个非常典型的问题。

假设流程：

~~~text
Context 太长
↓
Reactive Compact
↓
Retry
↓
仍然太长
↓
Stop Hook 又塞入 blocking message
↓
Runtime 决定继续
↓
如果这时错误地把
hasAttemptedReactiveCompact
重置为 false
↓
下一轮又 Compact
↓
仍然太长
↓
Stop Hook 再继续
↓
Compact
↓
...
~~~

这不是理论问题。

源码注释明确说明，这种错误会形成：

~~~text
compact
→ still too long
→ error
→ stop hook blocking
→ compact
→ ...
~~~

并持续浪费 API 调用。

所以当前代码在 Stop Hook blocking 的 continue 分支里，**故意保留**：

~~~text
hasAttemptedReactiveCompact
~~~

而不是重置。

这就是 State 最有价值的地方：

> 某个字段什么时候重置，什么时候不能重置，直接决定 Runtime 会不会走进死循环。

---

# 11. 为什么“新一轮正常 Tool 调用”又可以重置 Guard

注意：

> Guard 不是永远 true。

假设这一轮：

~~~text
Context 太长
↓
Compact 成功
↓
模型正常工作
↓
Tool 执行成功
↓
进入一个全新的正常 Agent Iteration
~~~

下一轮如果未来又出现新的上下文问题，可能应该允许新的恢复。

所以在真正的：

~~~text
next_turn
~~~

分支中，一些恢复状态会重新初始化。

这说明：

> State 字段的作用域必须想清楚。

例如：

~~~text
整个 Conversation 有效？
整个 User Turn 有效？
只对当前 Recovery Attempt 有效？
~~~

如果作用域设计错，就会：

- 该重试时不重试；
- 不该重试时无限重试。

---

# 12. Circuit Breaker 是什么

现在再引入另一个经常被滥用的词。

**Circuit Breaker（熔断）**：

> 同一种操作连续失败到一定程度后，暂时停止继续尝试，避免系统一直浪费资源。

生活里可以理解成：

> 电路异常太多，保险丝先断开，而不是继续通电烧设备。

当前 AutoCompact 里有：

~~~text
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3
~~~

即：

~~~text
AutoCompact 连续失败
1 次
2 次
3 次
↓
停止自动 Compact
~~~

源码注释还记录过真实生产现象：

> 曾经出现大量 Session 连续失败几十次甚至上千次，造成大量无意义 API 调用。

所以“3 次后停止”不是为了代码漂亮。

它来自真实生产成本问题。

---

# 13. Retry、Guard、Circuit Breaker 到底什么区别

这三个词以后会经常遇到。

## Retry

~~~text
失败后再试一次。
~~~

例：

~~~text
max_output_tokens
→ 再请求
~~~

## Guard

~~~text
执行动作前检查现在允不允许做。
~~~

例：

~~~text
如果已经 Reactive Compact 过
→ 不准再 Compact
~~~

## Circuit Breaker

~~~text
连续失败达到阈值后
→ 暂停整个自动尝试机制
~~~

例：

~~~text
AutoCompact 连续失败 3 次
→ 不再自动 Compact
~~~

关系可以画成：

~~~text
Retry
= 我要再试

Guard
= 我现在还允许再试吗？

Circuit Breaker
= 失败太多，整个自动重试通道先关闭
~~~

---

# 14. 事故现场：State 在恢复前后怎么变化

假设：

~~~text
messages = M0
hasAttemptedReactiveCompact = false
turnCount = 4
transition = next_turn
~~~

API 返回 prompt_too_long。

### 第一次恢复

~~~text
compact(M0)
↓
messages = M1

hasAttemptedReactiveCompact:
false → true

transition:
next_turn → reactive_compact_retry
~~~

然后：

~~~text
continue
~~~

### 第二次还是 prompt_too_long

此时 Runtime 看到：

~~~text
hasAttemptedReactiveCompact = true
~~~

所以：

~~~text
不再 Compact
↓
return prompt_too_long
~~~

这就是：

> 一个很小的 Boolean，控制一条非常昂贵的恢复路径只能执行一次。

---

# 15. 为什么 transition 比只看 Boolean 更有价值

Boolean 只告诉你：

~~~text
发生过 / 没发生过
~~~

transition 还能告诉你：

~~~text
为什么发生
~~~

调试时如果发现 Runtime 连续进行了 8 次 iteration：

只看：

~~~text
turnCount = 8
~~~

你只知道它跑了八轮。

如果有：

~~~text
transition.reason
~~~

可能看到：

~~~text
1 next_turn
2 next_turn
3 reactive_compact_retry
4 stop_hook_blocking
5 max_output_tokens_recovery
...
~~~

这相当于给 Runtime 留下了执行轨迹。

所以它既服务控制逻辑，也服务测试和 Debug。

---

# 16. 这套思想如何迁移到自己的 Agent

以后你自己写 Agent Loop，不要只写：

~~~ts
while (true) {
  ...
}
~~~

至少先问：

## 16.1 哪些动作可能自动 Retry

例如：

- Model API；
- Tool；
- Compact；
- 外部检索；
- SubAgent。

## 16.2 每种 Retry 最多几次

不要所有东西统一：

~~~text
retry = 3
~~~

要按风险和成本设计。

## 16.3 哪些动作同一轮只能发生一次

例如：

~~~text
Reactive Compact
Fallback
某些补偿操作
~~~

## 16.4 continue 前是否能说明“为什么继续”

最好建立：

~~~text
transition.reason
~~~

而不是让 continue 散落在代码里却没人知道来源。

## 16.5 最终失败必须是什么状态

例如：

~~~text
prompt_too_long
model_error
max_turns
...
~~~

而不是：

~~~text
return false
~~~

---

# 17. 和 LangGraph 的关系

你之前学 LangGraph 时接触过：

~~~text
State
Node
Conditional Edge
~~~

Claude Code 没有把主循环显式画成 Graph。

但思想很像：

~~~text
当前 State
↓
执行当前逻辑
↓
产生新 State
↓
根据结果决定下一 Transition
~~~

区别是：

> Claude Code 把这个状态机手写在 queryLoop 的 while(true) 里。

所以你现在看到：

~~~text
state = next
continue
~~~

可以把它理解成：

> 手写状态机的一次状态转移。

---

# 18. 和 Hermes 的关系

Hermes 里的 Runtime / TurnContext 同样需要回答：

~~~text
这轮执行到哪了？
已经用过哪些资源？
哪些操作允许继续？
~~~

Claude Code 的 State 更突出：

> Agent Loop 内部的恢复与迭代控制。

所以：

~~~text
ToolUseContext
≈ 运行环境和能力

State
≈ 当前 Agent Loop 的执行现场
~~~

不要把两者混成一个 Context。

---

# 19. 本章源码定位

重点只看：

~~~text
src/query.ts

type State
query()
queryLoop()
~~~

重点字段：

~~~text
maxOutputTokensRecoveryCount
hasAttemptedReactiveCompact
turnCount
transition
~~~

Context 恢复相关：

~~~text
src/services/compact/autoCompact.ts
~~~

可关注：

~~~text
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3
~~~

---

# 20. 本章最终心智模型

Agent Loop 真正危险的不是：

~~~text
while(true)
~~~

而是：

~~~text
发生错误
↓
Runtime 自动恢复
↓
continue
~~~

因为每一个 continue 都必须回答：

~~~text
为什么继续？
之前尝试过没有？
还允许再试几次？
失败到什么程度必须停止？
下一轮需要带哪些状态？
~~~

所以 Claude Code 使用显式 State 的核心价值不是“代码风格好看”。

而是：

> **把每次 continue 背后的控制条件摊在明面上，避免恢复逻辑自己变成新的故障源。**

下一章进入第二个更具体的问题：

> 模型已经发出了 tool_use，但 Tool 没有成功返回时，为什么一个小中断可能把整个 Conversation 的消息协议弄坏？

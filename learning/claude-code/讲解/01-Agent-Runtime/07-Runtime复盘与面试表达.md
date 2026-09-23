# 07｜Runtime 复盘：把四层调用、Agent Loop 和生产级保护重新拼成一张图

> 这一篇不再引入新的复杂机制。
>
> 目标是把前面六篇重新压成一个完整、能复述、能面试、能继续读源码的心智模型。

---

# 1. 先用一句话定义 Claude Code Runtime

如果现在有人问：

> Claude Code Runtime 是什么？

不要回答：

~~~text
就是 queryLoop。
~~~

也不要回答：

~~~text
就是 ask → submitMessage → query → queryLoop。
~~~

更完整的是：

> **Claude Code Runtime 是一套以 queryLoop 为执行心脏、由 QueryEngine 管理 Conversation / Turn、由 query 包裹一次执行生命周期，并通过状态、协议修复、有限恢复和并发调度保证 Agent 可以持续运行的控制系统。**

这句话现在应该能拆开理解。

---

# 2. 总体架构重新画一次

~~~mermaid
flowchart TB
    OUT["CLI / SDK / REPL 等外部入口"]

    A["ask()<br/>方便启动一次调用"]
    B["QueryEngine.submitMessage()<br/>准备一次 User Turn"]
    C["query()<br/>包住本次执行生命周期"]
    D["queryLoop()<br/>Agent Loop 心脏"]

    OUT --> A --> B --> C --> D

    subgraph LOOP["正常循环"]
      direction LR
      L1["准备 messagesForQuery"]
      L2["Streaming Model"]
      L3{"有 tool_use?"}
      L4["Tool Execution"]
      L5["tool_result"]
      L6["更新 State"]
      L7["完成判断"]
      L1 --> L2 --> L3
      L3 -->|Yes| L4 --> L5 --> L6 --> L1
      L3 -->|No| L7
    end

    D --> LOOP

    S["Case 1<br/>State / Guard / 有限恢复"] -.保护循环.-> D
    P["Case 2<br/>tool_use / tool_result 协议修复"] -.保护消息链.-> D
    R["Case 3<br/>输出截断 Recovery"] -.保护模型输出.-> D
    X["Case 4<br/>StreamingToolExecutor"] -.提升性能并控制并发.-> D
    CTX["Context Management"] -.控制 messagesForQuery.-> D
~~~

---

# 3. 四层调用链现在应该怎么记

## ask()

问：

> 外部怎么方便地启动一次 Claude Code 执行？

核心：

~~~text
创建 QueryEngine
↓
把 prompt 交给 submitMessage
~~~

---

## QueryEngine.submitMessage()

问：

> 用户这句话进入当前会话后，怎样准备成一次完整任务？

核心：

~~~text
处理输入
↓
加入 Conversation messages
↓
准备 Prompt / Model / Tools / Permission 等运行材料
↓
先保存关键 Transcript
↓
进入 query()
~~~

---

## query()

问：

> 一整次 Agent 执行的开始和结束由谁包住？

核心：

~~~text
开始外围记录
↓
try
  yield* queryLoop()
finally
  无论成功失败都做收尾
~~~

它不是主要数据加工层。

它是：

> Lifecycle Wrapper，也就是执行生命周期外壳。

---

## queryLoop()

问：

> Agent 到底怎么一圈圈工作？

核心：

~~~text
Context
↓
Model
↓
tool_use?
↓
Tool
↓
tool_result
↓
下一轮
~~~

异常恢复、状态转移、并发 Tool 等主要集中在这里。

---

# 4. 一个 User Turn 的正常数据轨迹

用户：

~~~text
帮我查登录为什么 401
~~~

进入 Conversation：

~~~text
User(question)
~~~

模型第一轮：

~~~text
Assistant(
  text="我先搜索",
  tool_use id=A Grep(...)
)
~~~

Tool：

~~~text
User(
  tool_result id=A
  "auth.ts ..."
)
~~~

模型第二轮：

~~~text
Assistant(
  tool_use id=B Read(auth.ts)
)
~~~

Tool：

~~~text
User(
  tool_result id=B
  "const token = ..."
)
~~~

模型最终：

~~~text
Assistant(
  final answer
)
~~~

Agent Loop 的“记忆”不是神秘东西。

最基础的一层就是：

> 每一轮 Action 和 Observation 继续进入 messages。

---

# 5. 为什么简单 while(true) 不够

Demo：

~~~ts
while (true) {
  const response = await model()

  if (response.toolUse) {
    const result = await tool()
    messages.push(result)
  } else {
    break
  }
}
~~~

它能跑 Happy Path。

生产环境马上出现：

1. Recovery 自己进入死循环；
2. Tool 中断后消息协议坏掉；
3. 模型输出写一半被截断；
4. Tool 全串行太慢，全并行又可能冲突；
5. messages 越来越大最终塞不进模型。

所以真正工程量在：

> **如何让循环出错后仍然保持可控。**

---

# 6. Case 1 最终记什么：State 是“下一轮的执行现场”

不要把 State 记成一个 TypeScript 类型。

它的本质：

> 把下一轮必须知道的执行现场显式保存下来。

例如：

~~~text
已经重试几次？
已经 Compact 过没有？
现在第几轮？
上一轮为什么 continue？
~~~

关键思想：

~~~text
Retry 必须有限
恢复必须有 Guard
连续失败要有熔断
continue 最好能说明原因
~~~

---

# 7. Case 2 最终记什么：停止程序不等于修复状态

Tool Calling 有协议：

~~~text
tool_use id=A
↓
tool_result id=A
~~~

中途中断时：

~~~text
只有 tool_use
没有 result
~~~

会让下一轮消息链不完整。

所以 Runtime 不只是：

~~~text
Abort Tool
~~~

还要：

~~~text
补 synthetic tool_result
~~~

关键思想：

> **异常退出以后，系统状态仍然必须满足下一次执行所需的协议规则。**

---

# 8. Case 3 最终记什么：一次 API 失败不等于用户任务失败

max_output_tokens 时：

~~~text
模型回答被截断
~~~

Runtime 可以：

~~~text
暂扣中间 Error
↓
先尝试输出额度升档
↓
仍失败则加入内部 nudge
↓
让模型续写
↓
RecoveryCount 限制次数
↓
最终才承认失败
~~~

关键思想：

> **在 API 层失败和用户任务失败之间建立有限恢复层。**

---

# 9. Case 4 最终记什么：性能优化必须带安全边界

StreamingToolExecutor：

~~~text
模型还在 Streaming
↓
完整 tool_use 一出现
↓
并发条件允许
↓
Tool 提前开跑
~~~

但：

~~~text
只有明确 concurrency-safe
才允许和其他 safe Tool 重叠执行
~~~

判断不清：

~~~text
false
↓
按不安全处理
~~~

关键思想：

> **生产并发不是越多越好，而是在可证明安全的边界内尽量重叠等待时间。**

---

# 10. Context Too Long 最终记什么

不要现在背所有压缩算法。

Runtime 视角只记：

~~~text
messages
↓
Context Management Pipeline
↓
messagesForQuery
↓
callModel()
~~~

当前固定源码的方向：

~~~text
先控制 Tool Result
↓
局部清理
↓
旧历史折叠
↓
主动 Compact
↓
预测下一轮增长
↓
真实 413 后 Reactive Recovery
↓
有限恢复
~~~

关键思想：

> **不要把所有希望寄托在最后一次错误恢复；生产系统需要多层防线。**

---

# 11. 本专题出现过的专业词，一次说清

| 词 | 直接理解 |
|---|---|
| Runtime | 让 Agent 真正运行起来并控制执行过程的程序层 |
| Conversation | 整个持续会话 |
| User Turn | 用户一次新输入到这次任务结束 |
| Loop Iteration | Turn 内一次 Model / Tool 往返 |
| State | 下一轮必须知道的执行现场 |
| Transition | 上一轮为什么进入下一轮 |
| Retry | 失败后重新尝试 |
| Guard | 执行动作前检查现在还允不允许做 |
| Circuit Breaker | 连续失败达到阈值后停止继续自动尝试 |
| tool_use | 模型提出的结构化 Tool 调用请求 |
| tool_result | Runtime 执行 Tool 后返回给模型的结果 |
| Synthetic Result | Tool 没正常完成时 Runtime 人工构造的错误结果 |
| Abort | 主动取消正在进行的异步工作 |
| Fallback | 当前执行路径失败后切到备用路径，例如备用模型 |
| Streaming | 结果不是最后一次性返回，而是边生成边收到 |
| Async Generator | 可以持续 yield 多个异步事件的函数 |
| yield* | 把内部 Generator 产生的事件继续向外转发 |
| Recovery | 出错后尝试把任务恢复到可继续状态 |
| Nudge | Runtime 加入内部提示，轻推模型下一轮继续正确行为 |
| Concurrency Safe | 和其他安全 Tool 同时执行不会互相破坏 |
| Fail-Closed | 判断不清时默认采用更保守、不放行的策略 |
| Context Window | 单次模型请求最多能处理的上下文容量 |
| Proactive | 问题发生前主动预防 |
| Reactive | 问题已经发生后再响应处理 |
| Terminal Reason | Runtime 最终为什么停止 |

---

# 12. 有哪些 Runtime 机制这次没有深挖，但不是遗漏

为了保持主线，本专题没有逐一深挖所有 query.ts 分支。

下面这些你应该知道存在，但目前不需要单独开课：

## Permission

> 模型提出 Tool Call 不代表它有权执行。Runtime 还要根据权限规则、Hook、用户确认等决定 Allow / Deny / Ask。

为什么没单独作为四大 Case：

> 后面 Tool System / Security 专题更适合完整展开。

---

## Transcript / Session Persistence

> 关键 Conversation 数据持久化，让进程退出后可以 resume。

本专题已经讲了：

> 用户消息为什么要在进入模型前先落 Transcript。

更完整的 parentUuid chain、Compact Boundary、Resume 留到 Session / Memory 相关学习。

---

## Max Turns / Budget

> 限制 Agent 运行轮次、Token、费用等资源，防止任务跑飞。

本专题没有展开具体 Budget 算法，因为 State 案例已经建立：

> 自治循环必须有 Runtime 硬边界。

---

## Stop Hook

> 模型看起来想结束后，外部规则还可以检查是否允许真正停止。

本专题只在死循环案例里用到。

Hook 体系后面可以和 Permission / Plugin 一起学。

---

## Model Fallback

> 主模型路径失败后切到备用模型。

本专题在 Tool 协议案例中只学习：

> Fallback 时旧 Assistant / Tool 半成品为什么必须清理。

模型路由策略本身不是当前重点。

---

## Terminal Reasons

当前源码有多种：

~~~text
completed
model_error
prompt_too_long
blocking_limit
aborted_streaming
aborted_tools
max_turns
hook_stopped
...
~~~

你现在不用背全。

只需要理解：

> 生产 Runtime 应该告诉外层“为什么停”，而不是只返回 true / false。

---

# 13. 小林文章与本专题的最终关系

小林文章最值得保留的四个设计哲学：

## 边干边吐

Async Generator + Streaming。

## 状态显式管理

State 不藏在不可见角落。

## 引擎不掺具体 Tool 业务

Runtime 调度 Tool，但不需要知道每个 Tool 的内部业务。

## 错误恢复优先

能修复的失败先修复，而不是一出错就崩。

本专题在此基础上补充：

> 每种哲学在当前固定源码里到底如何落到 messages、State、Executor 和 Recovery Path 上。

---

# 14. 2 分钟面试回答模板

如果被问：

> “Claude Code 的 Agent Runtime / Query Loop 怎么设计？”

可以这样回答：

> Claude Code 的 Runtime 外部是一条 ask → QueryEngine.submitMessage → query → queryLoop 的调用链。ask 更像 one-shot 入口，QueryEngine 维护 Conversation 级状态并把用户输入准备成一个 Turn，query 用 try/finally 包住一次执行生命周期，真正的 Agent Loop 在 queryLoop 里。
>
> queryLoop 每轮先整理 messagesForQuery，然后流式调用模型。如果流里出现 tool_use，就执行对应 Tool，把 tool_result 加回历史，再进入下一轮；没有 tool_use 才进入结束判断。
>
> 真正体现生产级的不是 while(true) 本身，而是异常和性能路径。第一，所有跨轮恢复状态显式放在 State 里，用计数器和 Guard 防止 Retry / Compact 无限循环。第二，如果 Tool 中途中断，会补 synthetic tool_result 保证 tool_use/tool_result 协议闭合。第三，模型输出撞 max_output_tokens 时会先尝试恢复，例如升输出额度或加入内部续写提示，同时限制恢复次数。第四，StreamingToolExecutor 会在模型仍在流式输出时提前执行确认并发安全的 Tool，但不安全 Tool 独占，判断不清则 fail-closed。Context 方面还会在每轮模型调用前做多层大小控制和 Compact，真实 413 后再 Reactive Recovery。
>
> 所以我会把 Claude Code Runtime 理解成“LLM ↔ Tool 循环发动机 + 状态、协议、恢复、并发和 Context 的生产保护层”。

---

# 15. 如果面试官追问，按什么顺序展开

不要一口气讲十个点。

推荐：

~~~text
第一问：
正常 Loop 怎么转？
→ tool_use / tool_result

第二问：
为什么要 State？
→ Retry / Recovery 防死循环

第三问：
Tool 中断呢？
→ synthetic tool_result 修协议

第四问：
性能呢？
→ StreamingToolExecutor

第五问：
Context 越滚越大呢？
→ Context Pipeline + Compact
~~~

这样有一条很清楚的因果链。

---

# 16. 和 Hermes 怎么对应

只做思想对照，不强行一一映射。

| Claude Code | Hermes / 通用 Agent 可类比 |
|---|---|
| QueryEngine | Conversation / Session Runtime |
| submitMessage | 一次 Turn 入口 |
| queryLoop | Agent Loop |
| ToolUseContext | Turn / Runtime Context |
| State | Loop 内部执行状态 |
| tool_use | Tool Call / Action |
| tool_result | Observation |
| Transcript | Conversation Persistence |
| Compact | History / Context Compression |

最重要的是：

> Hermes 和 Claude Code 都不是“LLM 自己在运行”，而是 Runtime 在组织 LLM、Tool、State 和 Context。

---

# 17. 和 LangGraph 怎么对应

LangGraph：

~~~text
State
↓
Node
↓
Conditional Edge
↓
Next Node
~~~

Claude Code：

~~~text
State
↓
queryLoop 当前逻辑
↓
Model / Tool / Recovery 判断
↓
state = next
continue / return
~~~

可以把 Claude Code 看成：

> 手写在 while(true) 中的动态状态机。

而 LangGraph：

> 把很多状态转换显式建模成 Graph。

---

# 18. 后续学习路线

Runtime 到这里先停。

下一专题建议：

## Context

重点回答：

- System Prompt、User Context、Messages、Tool Result 到底怎么组装；
- messages 和 messagesForQuery 的完整差异；
- Tool Result Budget；
- Snip；
- MicroCompact；
- Context Collapse；
- AutoCompact；
- Compact Summary；
- Context 和 Memory 的边界。

再之后：

## Memory

## Retrieval

## Skill

## Tool / Permission / Security

这样就不会再次把所有机制混在 Runtime 一章里。

---

# 19. 源码阅读导航

第一轮只看：

~~~text
src/QueryEngine.ts
  ask()
  submitMessage()

src/query.ts
  State
  query()
  queryLoop()
~~~

第二轮按案例搜索：

~~~text
hasAttemptedReactiveCompact
maxOutputTokensRecoveryCount
transition

yieldMissingToolResultBlocks

isWithheldMaxOutputTokens
MAX_OUTPUT_TOKENS_RECOVERY_LIMIT

StreamingToolExecutor
isConcurrencySafe
~~~

第三轮再进入：

~~~text
src/services/compact/
src/services/contextCollapse/
src/utils/toolResultStorage.ts
~~~

不要第一次读源码就顺序滚完整个 query.ts。

---

# 20. Runtime 专题验收

如果下面十题能不用文档回答，就可以进入 Context：

1. 四层调用链为什么不是四个独立模块？
2. query() 为什么存在？
3. Conversation / User Turn / Loop Iteration 有什么区别？
4. 模型怎么告诉 Runtime“我要调用 Tool”？
5. Tool Result 为什么要重新进入 messages？
6. State 为什么能防 Recovery 死循环？
7. tool_use 没有对应 tool_result 为什么危险？
8. max_output_tokens 为什么不一定意味着任务失败？
9. StreamingToolExecutor 为什么更快？
10. 为什么并发判断不清时应该默认串行？

如果某一题答不出来，回到对应案例，而不是重新从第一篇开始。

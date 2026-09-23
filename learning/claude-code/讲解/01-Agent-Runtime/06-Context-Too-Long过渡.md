# 06｜Context Too Long：从 Runtime 过渡到 Context 专题

> 这篇不是 Context 专题本身。
>
> 它只回答一个 Runtime 问题：
>
> **queryLoop 每轮都把 Assistant Message 和 Tool Result 继续带到下一轮，消息一定会越来越长。生产 Runtime 怎么避免 Context 最终把模型请求撑爆？**
>
> 这也是小林文章和当前固定源码差异最明显的地方之一。

---

# 1. 先从最真实的增长过程看问题

假设用户让 Agent：

> “排查整个登录模块。”

第一轮：

~~~text
User 问题
↓
Model
↓
Grep
↓
Grep Result
~~~

第二轮：

~~~text
之前全部 History
+
Model
+
Read auth.ts
+
Read Result
~~~

第三轮：

~~~text
之前全部 History
+
Model
+
Bash 测试
+
Bash Result
~~~

继续十几轮：

~~~text
User
Assistant
Tool Result
Assistant
Tool Result
Assistant
Tool Result
...
~~~

每次 Loop 都把新 Observation 带给下一轮。

这正是 Agent 能持续工作的原因。

同时也是：

> Context 会不断膨胀的根源。

---

# 2. Context Window 是什么

先解释词。

**Context Window（上下文窗口）**：

> 一次模型请求最多能够接收和处理的上下文容量。

你可以把它想成：

> 模型当前桌面一次最多能摊开的材料。

材料包括：

- System Prompt；
- 历史 Messages；
- Tool Result；
- 项目规则；
- Memory；
- Skill；
- 当前用户输入；
- 其他注入信息。

桌面再大也有限。

一旦塞不下：

~~~text
prompt_too_long
~~~

模型请求会失败。

---

# 3. 小林文章里的教学模型

小林“主循环 Query”文章为了突出 Runtime 主干，把这一段压得很简单：

~~~text
先正常请求模型
↓
如果 API 返回 prompt_too_long / 413
↓
Reactive Compact
↓
压缩后重试
↓
如果还失败
↓
退出
~~~

这个模型非常适合第一次理解：

> Context 超限不是普通 Tool Error，而是 Runtime 自己必须做 Recovery。

文章还重点解释：

~~~text
hasAttemptedReactiveCompact
~~~

防止：

~~~text
Compact
→ 还是太长
→ 再 Compact
→ 还是太长
→ 无限循环
~~~

这部分思想仍然成立。

---

# 4. 但当前固定源码已经不只是“出错后再 Compact”

当前源码基线：

~~~text
claude-code-best/claude-code
77a7934e15d69da13879112ed7db695c9ee7a52a
~~~

queryLoop 在真正请求模型前，已经有一条 Context 预处理管道。

概念上：

~~~text
历史 messages
↓
释放不再需要的原始 Tool Payload
↓
Tool Result Budget
↓
Snip
↓
MicroCompact
↓
Context Collapse
↓
AutoCompact
↓
Hard Limit / Predictive Check
↓
模型请求
↓
如果真实 413
↓
Collapse Recovery / Reactive Compact
~~~

注意：

> Snip、Context Collapse 等部分受 Feature Flag 或配置控制，不代表每个运行环境永远全部同时开启。

但架构方向已经很明确：

> 当前 Runtime 不只是“出事后救火”，而是“平时就控制增长 + 快溢出时主动处理 + 真溢出后再恢复”。

---

# 5. 为什么会演化成这么多层

因为所有 Context 问题都直接用“全量摘要 Compact”解决，代价很大。

假设：

~~~text
只是某个 Bash Tool 打了 10000 行日志
~~~

如果立刻：

~~~text
把整段 Conversation 全部总结一次
~~~

太重。

更好的思路是：

> 什么地方胖，就先处理什么地方；只有局部手段不够，再做更大范围压缩。

所以不同机制解决的是不同粒度的问题。

---

# 6. 第一层：先释放 Runtime 自己不再需要的原始 Tool Payload

当前源码会区分：

~~~text
message.message.content
~~~

和一些 Runtime / UI 侧保留的：

~~~text
toolUseResult raw payload
~~~

模型下一轮真正需要的是：

> API Message 里的 tool_result 内容。

不一定需要 Runtime 为 UI 保存的整个原始对象。

如果每次 Read 400KB 文件，原始对象永远挂在长期 messages 引用上：

> 长 Session 内存会持续涨。

所以 queryLoop 在构造 messagesForQuery 时，会复制 Message，并去掉下一次 API 不需要的原始 payload。

这里解决的首先是：

> Runtime 内存增长。

它还不是模型 Context 压缩。

---

# 7. 第二层：Tool Result Budget

假设 Bash 输出：

~~~text
200,000 个字符
~~~

如果全部塞进下一轮模型：

- Token 成本暴涨；
- Context 被迅速占满；
- 大量日志可能根本不重要。

所以有：

~~~text
applyToolResultBudget()
~~~

Budget 在这里可以翻成：

> 给 Tool Result 规定可进入模型 Context 的容量预算。

过大的结果可以：

~~~text
完整内容持久化到其他位置
↓
模型 Context 只保留 preview / stub
↓
告诉模型完整结果在哪里
~~~

preview：

> 预览。

stub：

> 占位信息，告诉模型“这里原来有一大段内容，但为了容量被替换了”。

这属于：

> 从源头控制最容易爆炸的数据。

---

# 8. 第三层：Snip

Snip 原意：

> 剪掉一段。

这里可以先理解为：

> 从很长的历史中，剪掉某些中间部分，保留更需要的上下文结构。

它不是一定把整个 Conversation 重新总结。

所以比“全量 Compact”更轻。

当前源码中：

~~~text
snipCompactIfNeeded()
~~~

运行在 MicroCompact 之前。

还会计算：

~~~text
snipTokensFreed
~~~

即：

> 这次 Snip 大概释放了多少 Token。

后面的 AutoCompact 判断会参考这个结果，避免已经 Snip 过了还因为旧估算误判。

---

# 9. 第四层：MicroCompact

Micro：

> 小型、局部。

所以 MicroCompact 可以先理解为：

> 不做一次“大总结”，只清理某些已经没有必要完整保留的局部内容。

它的价值：

> 比全局 Compact 成本低，而且尽量保留更多细节。

当前 queryLoop 里顺序是：

~~~text
Tool Result Budget
↓
Snip
↓
MicroCompact
~~~

说明这些机制可以叠加。

不是只能三选一。

---

# 10. 第五层：Context Collapse

Collapse 可以理解成：

> 把一段已经完成的历史折叠成更小的表示。

它和传统“整个会话只剩一份摘要”又不完全一样。

当前源码注释强调：

> Collapse 可以作为 full history 上的 read-time projection。

先不要钻内部实现。

你现在只需要理解目标：

> 尽量把旧的、已经稳定完成的部分压缩，而保留当前需要的细粒度 Context。

这是一种：

> 更细粒度的历史折叠。

后面 Context 专题再深入。

---

# 11. 第六层：AutoCompact

AutoCompact：

> Runtime 发现 Context 已经接近危险区，自动执行更大的压缩。

当前源码会计算：

~~~text
当前 Token 使用
AutoCompact Threshold
有效 Context Window
~~~

达到阈值时，可以主动 Compact。

这里和小林文章里的“先请求，等 413 再压缩”不同。

当前实现已经存在：

> Proactive Compaction。

Proactive：

> 问题真正发生前主动处理。

---

# 12. 为什么 AutoCompact 还需要 Circuit Breaker

Compact 本身也可能失败。

例如：

~~~text
Context 已经过于异常
↓
AutoCompact 请求失败
↓
下一轮又 AutoCompact
↓
又失败
↓
...
~~~

所以：

~~~text
consecutiveFailures
~~~

记录连续失败次数。

当前源码：

~~~text
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3
~~~

连续失败达到阈值：

> 停止继续自动尝试。

这正是上一章 Case 1 的思想在 Context 系统里的真实应用。

---

# 13. 第七层：Predictive AutoCompact

这是当前源码很值得学的演化。

假设：

~~~text
Context Window = 200K
当前已经用了 180K
~~~

现在还没超。

如果只看：

~~~text
180K < 200K
~~~

似乎可以继续。

但下一轮可能：

~~~text
模型输出 10K
+
Tool Result 15K
~~~

最后：

~~~text
205K
~~~

就爆了。

所以源码有：

~~~text
estimateMaxTurnGrowth(model)
~~~

它估算：

> 下一轮最大可能增长多少。

大致考虑：

~~~text
模型最大输出
+
Tool Result 增长预估
~~~

然后：

~~~text
当前 Context
+
预计下一轮增长
~~~

如果会进入危险区：

> API 请求之前就主动 Compact。

这叫：

> Predictive AutoCompact。

Predictive：

> 预测式。

---

# 14. 为什么“预测”比等 413 更好

等真实 413：

~~~text
已经发了一次必然失败的 API
↓
浪费时间
↓
然后再 Compact
↓
再请求
~~~

预测式：

~~~text
请求前发现：
这一轮大概率会把窗口撑爆
↓
先 Compact
↓
再请求
~~~

减少一次无意义失败。

但预测也不可能 100% 准确。

所以真实 413 Recovery 仍然需要保留。

---

# 15. Hard Blocking Limit 是什么

如果自动压缩被关闭，或者当前环境不允许自动 Recovery：

Runtime 还需要：

> 在明显已经没有空间时，禁止继续发一个注定失败的模型请求。

这就是 Blocking Limit。

Blocking：

> 阻止继续。

它还会预留一点空间，让用户可以执行：

~~~text
/compact
~~~

之类的恢复动作。

这是：

> 最后一道请求前保护。

---

# 16. 真正 API 还是返回 413 怎么办

即使做了：

- Budget；
- Snip；
- MicroCompact；
- AutoCompact；
- Predictive Check；

真实世界还是可能：

~~~text
API: prompt_too_long
~~~

这时进入 Reactive Recovery。

Reactive：

> 问题已经发生以后才响应。

当前源码的顺序里，会根据启用能力先尝试：

~~~text
Context Collapse Recover / Drain
~~~

如果仍不能恢复：

~~~text
Reactive Compact
~~~

然后：

~~~text
Retry
~~~

如果再失败：

~~~text
hasAttemptedReactiveCompact
~~~

等 Guard 阻止无限循环。

最后返回：

~~~text
prompt_too_long
~~~

---

# 17. Proactive 和 Reactive 到底什么区别

这个词以后会经常遇到。

## Proactive

~~~text
问题还没真正发生
↓
提前预防
~~~

例如：

~~~text
Predictive AutoCompact
~~~

## Reactive

~~~text
问题已经发生
↓
再处理
~~~

例如：

~~~text
API 真返回 413
↓
Reactive Compact
~~~

生产系统一般不是二选一。

而是：

> Proactive 降低事故概率，Reactive 兜住预测失败。

---

# 18. 把整个 Context 防线压成“由轻到重”

为了学习，不要先背函数顺序。

先记处理思想：

~~~text
第一步：
别让 Tool Result 无限大
↓
局部裁剪 / 局部压缩
↓
折叠旧历史
↓
接近上限时主动 Compact
↓
预测下一轮会爆时提前 Compact
↓
真实 413 后再 Recovery
↓
Recovery 也有限次
↓
最终承认失败
~~~

这就很像医学：

~~~text
日常控制
↓
早期干预
↓
重症处理
↓
抢救失败才宣布无法继续
~~~

---

# 19. 小林文章和当前源码到底怎么合并

小林文章的模型：

~~~text
413
↓
Reactive Compact
↓
Retry
↓
Guard 防无限 Compact
~~~

非常适合讲：

> “Runtime 出错后如何恢复。”

当前源码补充：

~~~text
错误前已经有大量 Context Management
~~~

所以最终学习模型应该是：

~~~text
文章：
先学最小闭环

当前源码：
再看这个闭环如何被生产需求逐步扩展
~~~

不是：

> 小林文章错了。

而是：

> 教学模型为了突出主循环，省略了当前源码里已经出现的多层 Context 控制。

---

# 20. 为什么 Context 不应该全部塞进 Runtime 章节

现在你已经看到：

~~~text
Tool Result Budget
Snip
MicroCompact
Context Collapse
AutoCompact
Predictive Compact
Reactive Compact
~~~

如果继续展开每个机制：

> Runtime 主线马上会被 Context 细节淹没。

所以 Runtime 学到这里就够。

这里真正需要带走的是：

> queryLoop 每轮都负责调用 Context Management Pipeline，确保“这一轮发给模型的 messagesForQuery”处于可执行范围。

至于：

~~~text
每种压缩到底删什么
Summary 怎么生成
Compact Boundary 怎么保存
Session Memory 怎么参与
Collapse Store 怎么工作
~~~

属于下一专题 Context。

---

# 21. 从 Runtime 视角看 messages 和 messagesForQuery

这时你应该能更清楚理解之前那个区别。

## messages

~~~text
Runtime 当前执行链持有的历史
~~~

## messagesForQuery

~~~text
经过 Context Management 后
这一轮真正准备给模型看的版本
~~~

所以：

~~~text
messages
↓
各种 Context 处理
↓
messagesForQuery
↓
callModel()
~~~

这就是 Context 机制真正嵌入 Runtime 的位置。

---

# 22. 这套思想怎么迁移到自己的 Agent

如果以后自己写 Agent，不要只设置：

~~~text
context_window = 200k
~~~

然后不管了。

应该分层考虑：

## 数据源控制

~~~text
Tool Result 最大多大？
日志是否全塞？
大文件如何处理？
~~~

## 局部清理

~~~text
哪些旧 Observation 可以删？
哪些可以只留摘要？
~~~

## 主动阈值

~~~text
多少 Token 开始处理？
是否要为下一轮输出预留空间？
~~~

## 真实 Overflow Recovery

~~~text
API 还是拒绝怎么办？
最多恢复几次？
~~~

---

# 23. 本章源码定位

Runtime 入口：

~~~text
src/query.ts
~~~

可以按顺序搜索：

~~~text
applyToolResultBudget
snipCompactIfNeeded
microcompact
applyCollapsesIfNeeded
autocompact
estimateMaxTurnGrowth
calculateTokenWarningState
tryReactiveCompact
~~~

AutoCompact：

~~~text
src/services/compact/autoCompact.ts
~~~

重点：

~~~text
getEffectiveContextWindowSize
getAutoCompactThreshold
estimateMaxTurnGrowth
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES
~~~

Tool Result：

~~~text
src/utils/toolResultStorage.ts
~~~

---

# 24. 本章最终心智模型

小林文章让我们先理解：

~~~text
Context 超了
↓
Compact
↓
Retry
~~~

当前生产源码进一步告诉我们：

> 真正稳定的 Runtime 不应该把所有希望都寄托在最后一次抢救上。

更完整的是：

~~~text
控制数据源增长
↓
局部清理
↓
逐步压缩
↓
主动预警
↓
预测未来增长
↓
真实失败后恢复
↓
恢复有限次
↓
最终明确退出
~~~

到这里 Runtime 专题的主干已经闭环。

下一篇做一次完整复盘：

> 如果面试官问“Claude Code Runtime 为什么不是一个简单 while(true)”，怎么从总体架构一路讲到这四个生产级案例，而不是背一堆术语。

# 02｜Context 治理总图：Claude Code 不是“快满了就 Compact”

> 这篇不是重新教一遍小林文章，而是把你已经看过的内容重新拼成一张**完整处理流程图**，并把当前固定源码里比文章更多的分支补上。

---

## 1. 先看最终主线

在 `queryLoop()` 每次真正调用模型之前，Claude Code 不是直接拿历史消息去请求 API。

当前固定源码的正常路径可以压成：

```text
messages
  ↓
getMessagesAfterCompactBoundary()
  ↓
去掉旧 toolUseResult 原始 payload
  ↓
Tool Result Budget
  ↓
Snip                         [HISTORY_SNIP feature]
  ↓
Micro-Compact
  ↓
Context Collapse             [CONTEXT_COLLAPSE feature；当前固定源码为 stub]
  ↓
Auto-Compact
  ↓
Hard Blocking Check
  ↓
Predictive Check
  ↓
prependUserContext()
  ↓
callModel()
```

如果 API 仍然真实返回 Prompt Too Long：

```text
真实 413 / prompt_too_long
  ↓
Context Collapse Drain       [若该内部能力可用]
  ↓
Reactive Compact
  ↓
Retry 一次
  ↓
仍失败
  ↓
明确返回 prompt_too_long
```

所以最重要的修正是：

> **Claude Code 的 Context 管理不是一条“5 层压缩流水线”那么简单，而是“调用前治理 + 调用后恢复”两套机制。**

---

# 2. 两大阶段比“几层压缩”更好记

## 阶段 A：模型调用前的 Proactive Management

目标：

> 尽量不要让本轮请求真的撞上 Context Window。

它又分成三种力度。

### A1. 先控制最肥的数据源

```text
Tool Result Budget
```

不是摘要整个对话，而是先解决：

> “一个 Tool Result 为什么要塞几十万字符进去？”

---

### A2. 局部清理旧历史

```text
Snip
Micro-Compact
```

它们都比全量摘要轻。

目的不是“重写整个 Conversation”，而是：

> 能删旧的就删旧的，能清理可重新获取结果就先清掉。

---

### A3. 接近 Context 极限后做大动作

```text
Context Collapse
或
Auto-Compact
```

这时候才进入真正重型 Context 重组。

但这里有个非常重要的源码边界：

> 在你固定的 `77a7934...` 源码里，Context Collapse 调用位存在，但 `src/services/contextCollapse/index.ts` 是明确的 auto-generated stub。

也就是说：

```text
文章/内部设计：
Context Collapse = 真正的读时投影系统

当前固定源码：
接口和 queryLoop 接线存在
但 applyCollapsesIfNeeded() 实际不做折叠
```

所以这份学习文档会把它作为“架构能力”讲，但不会假装我们已经从当前源码验证了内部算法。

---

# 3. 阶段 B：真实 Overflow 后的 Reactive Recovery

即使调用前已经做很多治理，真实 API 仍然可能拒绝：

```text
prompt_too_long
```

原因可能包括：

- Token 估算不是完全精确；
- Tool Result / Attachment 比预期更大；
- Provider 的真实计数与本地估算有差异；
- Media / PDF / Image 也可能造成大小限制；
- 当前 Context 已经处于极端边界。

因此 Runtime 还保留：

```text
Reactive Compact
```

Reactive 的意思就是：

> **不是提前预防，而是在错误真的发生后再抢救。**

并且它有 Guard：

```text
hasAttemptedReactiveCompact
```

保证同一条错误恢复路径不会无限循环。

---

# 4. 为什么“小林五层金字塔”仍然值得保留

小林文章的五层心智图：

```text
1. 大结果落盘
2. Snip
3. Micro-Compact
4. Context Collapse
5. Auto-Compact
```

最大的价值是：

> **从轻到重。**

这个思想完全正确。

真正需要补的是：

### 补充 1：Tool Result Budget 已经不只是“单结果超过 50KB”

当前源码还有：

```text
Per-message aggregate tool-result budget
```

即：

> 同一 API-level User Message 里，如果多个并行 Tool Result 合并后总量过大，也会重新预算并选择替换。

---

### 补充 2：Snip 不是一个自己按 Token 阈值决定“删谁”的函数

当前 `snipCompactIfNeeded()` 的主要职责是：

> 发现已经存在的 `snip_boundary`，根据其中的 `removedUuids` 把对应历史从模型视图移除。

所以：

```text
决定删哪些消息
和
真正执行删除
```

是两步。

---

### 补充 3：Micro-Compact 当前实现已经分支化

当前源码不是单一一套 Micro-Compact。

至少有：

```text
Time-based Microcompact
Cached Microcompact          [feature / provider 条件]
```

而旧的 legacy microcompact 路径在当前源码里已经移除。

---

### 补充 4：Context Collapse 在固定源码里无法完整验证

这是文章与当前学习树最重要的证据边界之一。

---

### 补充 5：Auto-Compact Buffer 已经不是永远固定 13K

当前源码：

```text
普通窗口        → 13K
>= 400K window  → 30K
>= 800K window  → 50K
```

也就是说：

> 小林文章里“始终固定减 13K”的讲法，适合解释基础公式，但当前源码已经做了窗口自适应。

---

### 补充 6：还有 Predictive Check

当前 `query.ts` 会估算：

```text
本轮最大模型输出
+
Tool Result 预计增长
```

用来判断：

> “虽然现在没溢出，但这一轮跑完可能会不会直接撞墙？”

这是文章主线里没有充分展开的部分。

---

### 补充 7：真实 413 后还有 Reactive Compact

也就是说：

```text
Auto-Compact
≠ 最后一道防线
```

真实 Overflow 后还有恢复路径。

---

# 5. 当前源码真正值得记的处理顺序

建议不要背“5 层”。

你复习时背这条更准确：

```text
【A. 先做模型输入视图】

取 Compact Boundary 之后的 active history
↓
释放 Runtime 不再需要的 raw toolUseResult
↓
限制 Tool Result 大小
↓
应用 Snip 投影
↓
做 Micro-Compact
↓
如果有真实 Collapse 实现则做 read-time collapse
↓
必要时 Auto-Compact 全量重写

【B. 发请求前最后保护】

如果 Auto-Compact 关闭：
    Hard Blocking Limit
↓
估计下一轮最大增长：
    Predictive Check
↓
callModel()

【C. API 仍然失败】

真实 413
↓
Collapse Drain（若可用）
↓
Reactive Compact
↓
Retry
↓
仍失败则终止
```

---

# 6. 为什么这些机制不能简单合并

因为它们处理的信息对象不一样。

| 机制 | 主要处理对象 | 是否重写整个对话 | 代价 |
|---|---|---:|---:|
| Tool Result Budget | 超大 Tool Result | 否 | 很低 |
| Snip | 已标记不再需要的历史 | 否 | 很低 |
| Micro-Compact | 可重新获取的旧 Tool Result | 否 | 低 |
| Context Collapse | 旧历史的模型可见投影 | 否（设计目标） | 中 |
| Auto-Compact | 整个有效 Conversation | 是 | 高 |
| Reactive Compact | 已经失败的完整 Context | 是 | 高 |

这正是 Claude Code 的核心思路：

> **先压最便宜、最局部、最可恢复的信息；最后才压语义主干。**

---

# 7. 用一个长任务重新走一遍

用户让 Agent：

> 重构整个鉴权模块，跑测试，修所有失败。

执行过程中：

### 第 1 阶段：Tool Result 很肥

Bash 测试输出 15000 行。

```text
优先处理 Tool Result
而不是立刻总结整段 Conversation
```

---

### 第 2 阶段：历史越来越长

很多早期探索已经失去价值。

```text
Snip
Micro-Compact
```

先减少旧 Action / Observation。

---

### 第 3 阶段：语义历史本身也太长

即使 Tool Result 都清理过，Conversation 仍接近窗口。

才需要：

```text
Auto-Compact
```

把“任务目标、关键决策、错误、当前进度、待办”等重新组织成 Summary。

---

### 第 4 阶段：本地估算没拦住

API 还是返回：

```text
prompt_too_long
```

于是：

```text
Reactive Compact
```

作为 emergency recovery。

---

# 8. 复习时真正要形成的框架

不是：

> Claude Code 有五种压缩算法。

而是：

> **Claude Code 把 Context 问题拆成“数据源控制、局部回收、历史结构重组、调用前预测、真实错误恢复”五类问题。**

这是比函数名更重要的设计框架。

下一篇只看第一类：Tool Result Budget。它看起来最简单，但当前源码里为了 Prompt Cache 和 Resume 一致性做了不少文章里没展开的工程处理。

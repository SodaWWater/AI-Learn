# 08｜小林文章 vs 当前固定源码：哪些已经讲到，哪些需要补，最终怎么记

> 这篇是整个 Context 专题的复习页。
>
> 目标不是继续增加新机制，而是帮你快速判断：
>
> **小林文章哪里已经足够，哪里当前源码有变化，哪里属于无法从固定源码验证的内部实现。**

---

# 1. 总体评价

小林文章最核心的设计思想没有问题：

> **Context 管理不是简单省 Token，而是不同类型信息分通道、分成本、分生命周期管理。**

它尤其讲清了：

- 大结果外置；
- Snip；
- Micro-Compact；
- Context Collapse；
- Auto-Compact；
- Summary Prompt；
- 文件/任务/CLAUDE.md 恢复；
- 熔断；
- Compact 后如何继续。

所以这次 Context 复习不是“推翻重学”。

而是：

> **把文章心智模型校准到当前固定源码，并补生产边角。**

---

# 2. 一张最终流程图

```text
                     Context Sources
 ┌────────────┬──────────────┬──────────────┐
 │SystemPrompt│ userContext  │ Conversation │
 │SystemCtx   │ reminders    │ tool results │
 └─────┬──────┴──────┬───────┴──────┬───────┘
       │             │              │
       └─────────────┴──────────────┘
                     ↓
                  messages
                     ↓
       getMessagesAfterCompactBoundary
                     ↓
       去除旧 raw toolUseResult payload
                     ↓
          Tool Result Budget
                     ↓
          Snip [feature gated]
                     ↓
             Micro-Compact
                     ↓
   Context Collapse [接口存在；固定源码 stub]
                     ↓
              Auto-Compact
                     ↓
       Hard Blocking / Predictive Check
                     ↓
                 callModel
                     ↓
           ┌─────────┴─────────┐
           │                   │
         正常                真实 PTL
           │                   │
     Agent Loop              Collapse Drain
                               ↓
                          Reactive Compact
                               ↓
                              Retry
```

---

# 3. 小林讲法与当前源码对照表

| 主题 | 小林文章 | 当前固定源码补充 |
|---|---|---|
| 大结果落盘 | 单大结果外置 | 还有 API-level User Message 聚合预算；替换决策会持久化 |
| Snip | 模型标记旧消息再删除 | `snipCompactIfNeeded()` 本身只执行 Boundary/removedUuids 投影；30 Message Nudge |
| Micro-Compact | 时间衰减清旧 Tool Result | 当前分 Time-based + Cached Microcompact；legacy 路径已移除 |
| Context Collapse | 90%/95%、读时投影 | query 接线存在，但固定源码核心实现是 stub，无法验证内部算法 |
| Auto-Compact Threshold | Effective Window - 13K | 当前 Buffer 动态：13K / 30K / 50K |
| Summary Reserve | 20K，p99.99=17,387 | 当前源码仍保留 |
| Auto-Compact | 全量摘要 | 现在先尝试 Session Memory Compaction |
| Post Compact | Boundary + Summary + Attachments + Hooks | 当前实际还有 `messagesToKeep` preserved segment |
| File Recovery | 5 files / 5K each / 50K total | 当前源码仍保留 |
| Skill Recovery | 文章较少展开 | 5K per skill / 25K total budget |
| Compact Input | 全历史 | 还会 strip images/documents、strip reinjected attachments、Microcompact |
| Summary Prompt | 9 sections | 现在额外明确保留安全约束 |
| Predictive | 非文章重点 | `estimateMaxTurnGrowth()` + query-level predictive check |
| Reactive | 非文章重点 | 真实 413 后 `tryReactiveCompact()`，单次 Guard |
| Compact 自己 PTL | 很少展开 | `truncateHeadForPTLRetry()` 丢最旧 API-round group 作为最后逃生 |

---

# 4. 文章里最容易让你形成的三个错误印象

## 错误印象 1：Context 就是一条五层压缩流水线

更准确：

```text
调用前治理
+
调用前保护
+
调用后恢复
```

五层只是“调用前治理”最直观的教学视角。

---

## 错误印象 2：Context Collapse 当前源码已经完整实现

不对。

固定学习树：

```text
src/services/contextCollapse/index.ts
= stub
```

我们只能确认：

- 接口；
- 调用位；
- 互斥设计；
- Recovery contract。

核心算法不在这份源码里。

---

## 错误印象 3：Auto-Compact 永远就是 Window - 33K

以前可以这样解释：

```text
20K summary reserve
+
13K buffer
```

当前源码已经变成：

```text
summary reserve
+
context-aware buffer
```

大 Context Window 会使用 30K / 50K Buffer。

---

# 5. 当前版本最值得你额外记住的 8 个补漏点

### ① Tool Result Budget 会按最终 API Message 结构聚合

避免并行 Tool Result 分开看都不过大，但合并后爆炸。

### ② Content Replacement State 用于保持 Prompt Cache 稳定

Context 优化不仅看 Token，也要避免前缀每轮变化。

### ③ Snip 和 Micro-Compact 可以同时发生

不是互斥。

### ④ Micro-Compact 当前不是固定 legacy 算法

Time-based / Cached 分支才是当前重点。

### ⑤ Context Collapse 固定源码是 stub

这是最重要的证据边界。

### ⑥ Auto-Compact 先尝试 Session Memory Compaction

说明 Memory 已开始参与 Context 压缩路径。

### ⑦ Post Compact 可以保留 messagesToKeep

不是所有 Compact 都绝对“一刀切”。

### ⑧ 真实 413 后还有 Reactive Compact

Auto-Compact 不是终点。

---

# 6. 最终只需要记住的五类问题

如果以后忘记所有函数，至少能还原：

## 问题 1：输入数据本身太肥

```text
Tool Result Budget
```

---

## 问题 2：历史里有很多已经没价值的内容

```text
Snip
Micro-Compact
```

---

## 问题 3：语义历史整体太长

```text
Context Collapse（设计）
Auto-Compact（当前可完整验证）
```

---

## 问题 4：这一轮可能突然增长很多

```text
Predictive Check
Hard Limit
```

---

## 问题 5：预测失败，Provider 真的拒绝

```text
Reactive Recovery
```

这五类问题就是 Context 工程的骨架。

---

# 7. Context 和 Memory 的最终边界再确认一次

```text
Memory
= 长期或阶段性保存的信息源

Context
= 当前这一次模型调用真正看到的信息
```

Memory 进入 Context 的方式很多：

```text
CLAUDE.md
→ project-instructions

relevant memory
→ system-reminder

nested memory
→ system-reminder

session memory
→ 既可能作为 reminder / attachment
  也可能参与 compaction
```

因此：

> Context 是“消费层”，Memory 是“信息供给层”。

后面进入 Memory 专题时，就不会把两者重新混起来。

---

# 8. 面试/复述时推荐的 90 秒结构

> Claude Code 的 Context 管理不是只有 Auto-Compact。每轮模型调用前，它先从 Compact Boundary 后取 active history，释放 Runtime 不再需要的 raw tool payload，然后做 Tool Result Budget，避免 Observation 一次性撑爆窗口；如果开启 Snip，会把已经标记为不再需要的历史移出模型视图，随后 Micro-Compact 会回收旧的、可重新获取的 Tool Result。再往上才是重型治理：内部设计里有 Context Collapse 做细粒度读时投影，但我当前对齐的固定源码这里是 stub，因此可以完整验证的主力仍然是 Auto-Compact。
>
> Auto-Compact 会先预留 Summary 输出空间，再用随窗口大小变化的 Buffer 判断阈值；当前源码达到阈值后还会先尝试 Session Memory Compaction，再回退到传统结构化 Summary。Compact 后 Context 不只是 Boundary + Summary，还可以保留 messagesToKeep，并有限恢复文件、Skill、任务和 Hook 信息。
>
> 最后，Runtime 还有调用前的 growth estimation 和真实 prompt-too-long 后的 Reactive Compact，所以整体上是“数据源控制 → 局部回收 → 语义重组 → 调用前保护 → 调用后恢复”，而不是单一的摘要算法。

---

# 9. 本专题到这里的验收标准

你不需要重新背文章。

只要现在能回答：

1. 为什么 Tool Result 要先于 Auto-Compact 治理？
2. Snip 和 Micro-Compact 到底差在哪？
3. Context Collapse 在固定源码里能确认到什么程度？
4. 当前 Auto-Compact 阈值和文章里的固定 13K 有什么变化？
5. `messagesToKeep` 为什么说明 Compact 不是绝对全量一刀切？
6. Predictive 和 Reactive 分别在什么时候工作？
7. 为什么 Context Management 还要考虑 Prompt Cache 稳定？
8. Memory 被召回以后和 Context 是什么关系？

如果这些都有大致答案，就可以阶段性结束 Context，进入 Memory 专题。

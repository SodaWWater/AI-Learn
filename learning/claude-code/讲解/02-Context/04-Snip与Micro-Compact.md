# 04｜Snip 与 Micro-Compact：两个“局部回收”机制不要混在一起

> 小林文章已经解释过它们都比 Auto-Compact 轻。
>
> 复习时最需要补的是：**Snip 处理“哪些历史消息应该从视图里消失”，Micro-Compact 处理“旧 Tool Result 的内容是否还值得原样保留”。它们不是同一种压缩。**

---

# 1. 先用一句话区分

```text
Snip
= 删除被明确标记为可以移除的历史 Message

Micro-Compact
= 保留消息结构，但清掉某些旧 Tool Result 的正文
```

所以：

```text
Snip 更像删记录
Micro-Compact 更像瘦身记录
```

---

# 2. Snip 当前源码到底做什么

当前：

```text
snipCompactIfNeeded(messages)
```

本身并不会：

> “检测 Token 太长，然后自己决定删最旧 20 条。”

它真正做的是：

1. 找最后一个 `snip_boundary`；
2. 从 boundary metadata 取出 `removedUuids`；
3. 过滤掉这些 UUID 对应的消息；
4. 保留 boundary 和其他消息；
5. 粗略计算释放 Token 数。

即：

```text
snip_boundary
    │
    └── removedUuids = [A,B,C]
              ↓
        Snip Projection
              ↓
消息 A/B/C 不再进入模型视图
```

---

# 3. 那“谁决定删哪些”？

当前源码把“决策”和“执行”分开。

`snipCompactIfNeeded()`：

> 只负责执行已有 Snip Boundary。

至于 Boundary 可以来自：

- Snip Tool；
- force-snip；
- 其他启用 HISTORY_SNIP 的控制路径。

当前源码还有：

```text
SNIP_NUDGE_THRESHOLD = 30 messages
```

当历史足够长，会提醒模型：

> 可以考虑使用 snip / force-snip 来释放上下文。

所以更准确的模型：

```text
历史变长
↓
Runtime / Prompt 提醒
↓
产生 Snip 决策
↓
写 snip_boundary + removedUuids
↓
下一次 query
↓
snipCompactIfNeeded() 真正过滤
```

---

# 4. 一个很容易遗漏的细节：Snip 不只改“这一轮视图”

当前源码里 Snip 还服务两个位置：

### query.ts

> 从模型本轮看到的 `messagesForQuery` 中移除。

### QueryEngine replay

> 进一步修剪 `mutableMessages`，避免长 SDK Session 的内存状态无限增长。

所以 Snip 同时解决：

```text
模型 Context
+
Runtime 自身内存增长
```

---

# 5. 为什么 Snip 释放 Token 数还要传给 Auto-Compact

源码：

```text
snipTokensFreed
```

会继续交给 Auto-Compact 判断。

原因是：

> API usage 里记录的历史 Token 统计可能仍反映 Snip 前的旧值。

如果不扣掉：

```text
Snip 明明已经把 Context 拉下来
↓
Auto-Compact 仍认为快超限
↓
又做一次重型摘要
```

所以：

```text
AutoCompact tokenCount
=
estimated tokens
-
snipTokensFreed
```

这就是不同 Context 层之间的联动。

---

# 6. Micro-Compact 的对象完全不同

Micro-Compact 关注的是：

> 某些 Tool Result 内容是不是已经老到没必要继续原样保留。

当前可 compact 的工具包括：

- Read；
- Shell / Bash；
- Grep；
- Glob；
- Web Search；
- Web Fetch；
- Edit；
- Write。

这些有共同特征：

> 大部分结果可以通过再次调用 Tool 重新获取。

所以旧内容被清理后，模型真需要时还能重新查。

---

# 7. Time-based Micro-Compact

当前有一条明确的时间触发路径。

默认配置：

```text
gapThresholdMinutes = 60
keepRecent = 5
enabled = false（默认配置；实际可由远端配置开启）
```

思想：

```text
距离上次主循环 Assistant Message 已经 > 60 分钟
↓
Prompt Cache 1h TTL 基本已经失效
↓
这一轮本来就要重写整个 Prefix
↓
不如趁机清掉旧 Tool Result
```

保留：

```text
最近 5 个 compactable Tool Result
```

更老的替换成：

```text
[Old tool result content cleared]
```

---

# 8. 为什么 60 分钟不是随便拍脑袋

源码注释给出的理由：

> Server-side Prompt Cache 1h TTL 已确定过期。

这意味着：

如果在 Cache 仍热的时候贸然改旧 Prompt：

```text
旧 Tool Result 内容改变
↓
Prompt Prefix 改变
↓
Cache Miss
```

反而会损失性能。

所以 Time-based Micro-Compact 选择：

> Cache 已经冷了的时候再清。

这是 Context 管理和 Prompt Cache 的联动设计。

---

# 9. Cached Micro-Compact：当前源码比文章更复杂的一层

固定源码还存在：

```text
CACHED_MICROCOMPACT
```

这条路径不直接改本地 Message Content。

而是利用：

```text
cache_edits / cache_reference
```

在 API Cache 层删除旧 Tool Results。

关键点：

- feature-gated；
- 只在支持的模型/主线程路径使用；
- 有自己的 tool registration state；
- 不把 forked agent 的 Tool Result 混入主线程状态；
- 本地 Conversation History 可以继续保留。

所以文章里“Micro-Compact = 把旧 Tool Result 替换成本地占位符”是理解基础，但当前源码还有更先进的 Cache Editing 分支。

---

# 10. 当前源码一个很重要的变化：Legacy Microcompact 已移除

源码直接写着：

> Legacy microcompact path removed.

也就是说：

如果：

- Time-based 没触发；
- Cached Microcompact 不可用；

当前函数可以直接：

```text
return { messages }
```

然后把 Context 压力交给：

```text
Auto-Compact
```

因此不要把“小林文章里的 Micro-Compact”理解成所有环境下必然发生的固定第三层。

它是：

> 一个可能启用的轻量 Context 回收策略。

---

# 11. Snip 和 Micro-Compact 可以同时发生

queryLoop 注释明确：

```text
Apply snip before microcompact
(both may run — they are not mutually exclusive)
```

所以：

```text
Snip
先把明确无用消息移出历史

Micro-Compact
再清掉剩余历史里过时的 Tool Result
```

它们是可叠加的。

---

# 12. 最终对比

| | Snip | Micro-Compact |
|---|---|---|
| 处理对象 | Message | Tool Result 内容 |
| 结构是否保留 | 被 Snip 的 Message 不再进入视图 | Message 保留 |
| 谁决定清理对象 | Snip Boundary / removedUuids | Tool 类型 + 时间/Cache 策略 |
| 是否需要 LLM 摘要 | 否 | 否 |
| 是否可和另一层同时发生 | 是 | 是 |
| 核心目的 | 删无用历史 | 清旧 Observation |

复习时把它们放在一起，是因为它们都属于：

> **全量摘要之前的局部 Context 回收。**

下一篇看 Context Collapse。重点不是重新背 90%/95%，而是搞清楚：哪些内容是当前固定源码可验证的，哪些只能视为内部架构接口。

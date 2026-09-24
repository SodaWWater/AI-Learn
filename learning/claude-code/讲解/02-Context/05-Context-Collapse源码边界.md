# 05｜Context Collapse：架构思想成立，但当前固定源码必须标明“实现不可见”

> 这是本专题最需要做证据校准的一节。
>
> 小林文章把 Context Collapse 描述成很完整的第 4 层机制；而当前固定学习树里，**调用位和接口是真的，但核心实现是 stub**。

---

# 1. 小林文章给出的设计思想

核心可以压成：

> **原始历史不破坏，只在模型调用时生成一个折叠后的可见视图。**

即：

```text
Full Conversation History
        │
        │ 本地继续保留
        ▼
   projectView()
        │
        ▼
Collapsed Model View
        │
        ▼
       LLM
```

这叫：

> Read-time Projection（读时投影）。

和 Auto-Compact 最大区别：

```text
Context Collapse
→ 原历史仍在

Auto-Compact
→ 旧历史被 Summary 主动替换
```

---

# 2. queryLoop 确实为它留了位置

当前 `query.ts` 有：

```text
if feature('CONTEXT_COLLAPSE')
    applyCollapsesIfNeeded(messagesForQuery)
```

并且放在：

```text
Micro-Compact
↓
Context Collapse
↓
Auto-Compact
```

注释还明确表达了设计意图：

> 如果 Collapse 已经把 Context 降到 Auto-Compact 阈值以下，就不要再做重型全量摘要。

所以架构上：

> Collapse 是更细粒度治理，Auto-Compact 是更粗粒度兜底。

---

# 3. 但是：当前固定源码的实现是 Stub

`src/services/contextCollapse/index.ts` 第一行就是：

```text
Auto-generated stub — replace with real implementation
```

并且：

```text
isContextCollapseEnabled()
→ 默认 false

applyCollapsesIfNeeded(...)
→ identity / 透传

recoverFromOverflow(...)
→ committed = 0
```

因此在这份固定源码上，我们能验证的是：

### 可以验证

- queryLoop 有调用位置；
- Auto-Compact 有互斥判断接口；
- Prompt Too Long recovery 有 collapse drain 的入口；
- Runtime 设计上预留了这一整套系统。

### 不能验证

- 90% 怎么挑 Span；
- 95% blocking spawn 的真实算法；
- Summary Store / Commit Log 的内部格式；
- 真正的 projectView 如何回放；
- 哪些消息被归档、哪些保留；
- 内部 ctx-agent 的实际行为。

这些不能拿 stub 代码硬推成事实。

---

# 4. 为什么小林文章会有更多细节

固定学习树本身已经在其他文档中说明：

> Context Collapse 是 internal / ant-only 能力，对外构建会被裁掉或替换为 stub。

所以更合理的理解是：

```text
小林文章 / 其他逆向资料
→ 描述完整内部设计

当前固定公开学习树
→ 只保留接口和接线
→ 核心实现不可验证
```

这不是“文章错了”。

而是：

> 我们必须把“设计信息”和“当前源码可验证事实”分开。

---

# 5. Context Collapse 和 Auto-Compact 为什么理论上互斥

当前 `shouldAutoCompact()` 里写得很清楚：

如果：

```text
isContextCollapseEnabled() == true
```

那么：

```text
shouldAutoCompact()
→ false
```

源码注释给的原因：

```text
Collapse commit-start ≈ 90%
Auto-Compact ≈ 93%
Collapse blocking ≈ 95%
```

如果两套系统同时启用：

```text
90% Collapse 开始准备
↓
93% Auto-Compact 把整个 History 重写
↓
Collapse 原本准备保存的 granular context 被一锅端
```

所以：

> 两者都处理“高压 Context”，但策略冲突。

---

# 6. 为什么当前固定源码实际不会发生这种互斥

因为 Stub：

```text
isContextCollapseEnabled() = false
```

所以在当前可执行路径里：

```text
Auto-Compact 不会因为 Collapse 被关闭
```

换句话说：

> **“两者互斥”是 Runtime 接口契约；“当前固定源码运行时互斥”并不是实际发生的事实，因为 Collapse 本身没启用。**

这是复习时很值得说清楚的一个点。

---

# 7. Prompt Too Long Recovery 里也预留了 Collapse Drain

真实 413 后：

```text
如果 Context Collapse 可用
并且上一轮不是 collapse_drain_retry
↓
recoverFromOverflow()
↓
如果 committed > 0
↓
带着更小 Context retry
```

如果还是 413：

```text
fall through
↓
Reactive Compact
```

因此完整内部设计意图应该是：

```text
细粒度 Collapse Recovery
优先
↓
Full Summary Reactive Compact
兜底
```

仍然体现：

> 先轻后重。

---

# 8. 这部分面试/复习怎么讲最稳

可以这样说：

> Claude Code 的 queryLoop 预留了 Context Collapse，设计上是读时投影，优先于 Auto-Compact 保留更细粒度历史；Auto-Compact 在 Collapse 真正启用时会被抑制，真实 413 也会先尝试 drain staged collapses。但我当前对齐的固定源码里 `contextCollapse/index.ts` 是 external stub，所以接口和控制流可以确认，内部 collapse 算法不能从这份源码直接验证。

这比直接背：

> 90% / 95% / read-time projection

更严谨。

---

# 9. 这一节最后只记一个框架

```text
Context Collapse
= 理想目标：
  尽量不破坏原历史
  只改变模型当前看到的 View

Auto-Compact
= 真的重写 Conversation

当前固定源码
= Collapse 接口存在
  实现 stub
  Auto-Compact 才是可完整验证的主力路径
```

下一篇进入 Auto-Compact：这是当前固定源码里真正可以完整追到底的重型机制。

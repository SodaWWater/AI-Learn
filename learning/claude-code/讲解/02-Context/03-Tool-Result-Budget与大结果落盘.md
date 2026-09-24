# 03｜Tool Result Budget：为什么先处理“大结果”，而不是先 Compact 整个对话

> 小林文章把这一层概括成“大结果存磁盘”。这个直觉是对的。
>
> 当前固定源码值得补的细节是：**Claude Code 同时处理“单个 Tool Result 太大”和“同一 API User Message 内多个 Tool Result 聚合后太大”两类问题，而且会保存替换决策，保证 Resume 和 Prompt Cache 一致。**

---

# 1. 真实问题

假设：

```text
Bash
→ 输出 300KB 日志

Grep
→ 输出 80KB

MCP Tool
→ 输出 500KB JSON
```

如果全部原样进入下一轮：

```text
Tool Result
→ Messages
→ 下一轮 Model Input
```

Context 很快被 Tool Output 吃掉。

而这些内容很多是：

- 日志；
- 原始 JSON；
- 大段文件内容；
- 可以再次读取的数据。

所以最优先应该做：

> **控制数据源，而不是立刻总结 Conversation。**

---

# 2. 第一种控制：单 Tool Result 大小

源码里的基本逻辑：

```text
Tool Result
↓
检查 Tool 自己的 maxResultSizeChars / 默认阈值
↓
没超
    → 原样保留
超了
    → 完整内容持久化
    → Context 只放 preview + 文件位置
```

如果持久化失败：

> 回退为原内容，不为了 Context 优化把真实结果弄丢。

另外 Image Block 不走这套文本持久化替换，因为图片必须按原 API 结构发送。

---

# 3. 文章里容易忽略的一点：FileRead 不是所有情况都按同一个阈值

Tool 可以自己声明：

```text
maxResultSizeChars
```

所以 Runtime 不是简单：

> 所有 Tool 超过 50KB 就落盘。

更准确是：

> **优先用 Tool 自己的限制，没有时才使用全局限制。**

因此这一层实际上是：

```text
Tool-level policy
+
Runtime fallback policy
```

---

# 4. 第二种控制：Aggregate Budget

当前源码里更值得注意的是：

```text
applyToolResultBudget()
```

它不是只看一条 Tool Result。

它会模拟最终 API 消息结构，把：

> **连续 User Messages 中属于同一 API-level User Message 的 Tool Result 聚合起来计算。**

为什么？

因为并行 Tool 可能在 Runtime 状态里是：

```text
User(tool_result A)
User(tool_result B)
User(tool_result C)
```

但 API normalization 最终可能把它们合并成一个 User Message。

如果 Runtime 分开算：

```text
A = 80K
B = 80K
C = 80K

每条都没超
```

但上线：

```text
A+B+C = 240K
```

就超了。

当前默认 aggregate budget：

```text
MAX_TOOL_RESULTS_PER_MESSAGE_CHARS = 200_000
```

并且可以通过远端配置覆盖。

---

# 5. 为什么要保存“替换决策”

这是小林文章里不太会重点讲，但很生产级的一点。

假设第一次请求：

```text
Tool Result A
→ 被替换成 preview P1
```

下一轮又重新跑预算算法。

如果这次：

```text
因为消息顺序或算法变化
→ A 不再被替换
```

那么 Prompt 前缀从：

```text
P1
```

变成：

```text
完整 A
```

Prompt Cache 会直接失效。

所以源码有：

```text
ContentReplacementState
```

包含：

```text
seenIds
replacements
```

含义：

### seenIds

> 这条 Tool Result 的命运已经决定过。

### replacements

> 如果当时替换过，精确保存模型看到的 replacement 字符串。

后续再处理时直接复用。

---

# 6. 为什么 Resume 后也必须保持一致

假设：

```text
Session 1:
A 被替换成 preview

退出 Claude Code

Resume

如果重新跑算法后：
A 变成完整内容
```

模型看到的历史前缀就变了。

所以源码还会把：

```text
ContentReplacementRecord
```

写入 Transcript。

Resume 时重建 replacement state。

这意味着：

> Context 管理决策本身也是 Conversation State 的一部分。

这比单纯“把大文件存磁盘”更完整。

---

# 7. 为什么它必须在 Snip / Micro-Compact 前执行

queryLoop 顺序：

```text
Tool Result Budget
↓
Snip
↓
Micro-Compact
```

原因很自然：

### Tool Result Budget

处理的是：

> “现在这个结果本身太大。”

### Snip / Micro-Compact

处理的是：

> “历史里哪些东西已经不值得保留。”

所以先做源头限流，再做历史回收。

---

# 8. Tool Result Budget 和 Compact 本质区别

Tool Result Budget：

```text
不改变 Conversation 语义
不重新总结任务
不要求 LLM 重新理解历史
```

它只是把：

```text
巨大原始数据
```

换成：

```text
较小 preview
+
可重新访问路径
```

因此代价远小于 Auto-Compact。

---

# 9. 这一层真正值得记的设计思想

小林文章可以记成：

> 大结果存磁盘。

源码层面更完整的说法应该是：

> **Tool Result 采用“按 Tool 限额 + API Message 聚合预算 + 内容外置 + 稳定替换决策”四层控制，在尽量不损失可恢复性的前提下，防止 Observation 把 Context 吃光。**

这已经足够作为复习结论。

下一篇看 Snip 和 Micro-Compact：它们不再处理“单次结果太大”，而是处理“这些旧结果现在还有没有必要继续留着”。

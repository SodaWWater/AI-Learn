# 07｜Predictive / Reactive：文章主线之外，Runtime 怎么防“这一轮直接撞墙”

> 这一篇专门补小林文章没有充分展开的两条保护：
>
> **Predictive Check：调用前预测下一轮增长。**
>
> **Reactive Compact：真实 API 拒绝后做一次紧急 Compact。**

---

# 1. 为什么只看当前 Token 数不够

假设：

```text
Effective Window = 180K
当前 Context = 155K
```

看起来还有：

```text
25K
```

但这一轮可能：

```text
模型输出 = 20K
Tool Result = 15K
```

总增长：

```text
35K
```

结果：

```text
155K + 35K = 190K
```

直接越界。

所以 Runtime 不应该只问：

> “现在超没超？”

还应该问：

> “这一轮结束以后会不会超？”

---

# 2. estimateMaxTurnGrowth()

当前源码：

```text
maxOutput
+
TOOL_RESULT_GROWTH_ESTIMATE
```

其中：

```text
TOOL_RESULT_GROWTH_ESTIMATE = 15K
```

模型最大输出会取：

```text
min(model max output, 20K)
```

所以典型最大估计：

```text
约 35K
```

---

# 3. Predictive Threshold

queryLoop 计算：

```text
predictiveThreshold
=
effectiveContextWindow
-
estimatedGrowth
```

如果：

```text
currentTokens > predictiveThreshold
```

就进入：

```text
predictive autocompact check
```

---

# 4. 一个很重要的源码细节：Predictive Check 不是独立的“强制 Compact 算法”

当前 `query.ts` 虽然检测了 predictive threshold，但实际仍然调用：

```text
deps.autocompact()
```

也就是同一个：

```text
autoCompactIfNeeded()
```

而这个函数内部仍会走：

```text
shouldAutoCompact()
```

正常阈值判断。

所以最严谨的理解不是：

> “一旦预测下一轮会溢出，就强制在更早阈值 Compact。”

而是：

> **queryLoop 增加了一次“预测风险时的 Auto-Compact 机会”，但是否真的 Compact 仍服从 Auto-Compact 本身的启用条件和阈值。**

这点比把 Predictive 当成独立第 6 层更准确。

---

# 5. Hard Blocking Limit

如果 Auto-Compact 被关闭：

Runtime 不能一直把明显会失败的请求送给 API。

因此有：

```text
blocking limit
=
effective context window
-
3K manual compact reserve
```

达到后：

```text
return blocking_limit
```

目的：

> 仍然给用户留一点空间执行手动 `/compact`。

---

# 6. 为什么启用了 Reactive Compact 时反而跳过某些 Blocking Preempt

这是一个非常工程化的细节。

如果 Runtime 在 API 调用前就：

```text
synthetic prompt-too-long
→ return
```

那么：

> Reactive Compact 永远收不到真实 413。

因此当自动恢复能力开启时，部分 preempt 会被跳过，让真实 API 错误发生，再进入恢复链。

这是：

> **错误检测机制不能把自己的恢复机制饿死。**

---

# 7. 真实 413 后的第一层恢复：Collapse Drain

在内部 Context Collapse 真正可用的设计里：

```text
prompt_too_long
↓
recoverFromOverflow()
↓
把 staged collapses 全部 commit
↓
retry
```

为什么先做这个？

> 因为比 Full Summary 更轻，尽量保留 granular context。

但再次强调：

> 当前固定源码 Collapse 是 stub，所以这条路径接口存在，实际 committed=0。

---

# 8. 第二层恢复：Reactive Compact

如果：

```text
isWithheld413
或
recoverable media-size error
```

Runtime 调：

```text
tryReactiveCompact()
```

条件：

```text
hasAttempted == false
aborted == false
```

成功：

```text
buildPostCompactMessages()
↓
hasAttemptedReactiveCompact = true
↓
transition = reactive_compact_retry
↓
continue
```

也就是：

> Full Summary 后再给原任务一次机会。

---

# 9. 为什么错误要先 Withhold

如果 API 一返回 413 就立刻向 SDK / UI 发：

```text
Error
```

外层可能认为 Turn 已结束。

但 Runtime 其实还想自动恢复。

所以：

```text
413
↓
先不向外暴露
↓
内部 Recovery
↓
成功：
  用户无感继续
失败：
  再真正 Surface Error
```

这和 Runtime 里 max_output_tokens 的恢复思想一致。

---

# 10. 为什么 Reactive Compact 只能尝试一次

如果：

```text
413
→ Reactive Compact
→ Retry
→ 413
→ Reactive Compact
→ ...
```

就是 Recovery Death Spiral。

所以：

```text
hasAttemptedReactiveCompact
```

作为 Guard。

第二次还失败：

> 直接让真实 prompt_too_long 暴露并终止。

---

# 11. 为什么失败后不能继续跑普通 Stop Hook

源码注释非常明确。

如果：

```text
Prompt Too Long
↓
Stop Hook 认为任务未完成
↓
塞一条 blocking message
↓
Retry
↓
Context 更大
↓
Prompt Too Long
↓
...
```

就会形成：

> Error → Hook Blocking → Retry → Error

所以 Recovery 耗尽后：

```text
直接 executeStopFailureHooks
return prompt_too_long
```

不进入普通 Stop Hook 继续链。

---

# 12. Media Error 为什么也能走 Reactive Compact

Current source 不只考虑文字 Token。

Image / PDF / many-image 也可能造成请求大小问题。

Reactive Compact 能：

- Strip / summarize history；
- 去掉部分 Media burden；
- 重建 Context 后 Retry。

但如果 oversized media 位于必须保留 Tail：

> Retry 可能仍失败。

此时同样靠：

```text
hasAttemptedReactiveCompact
```

阻止死循环。

---

# 13. 最终应该把 Predictive 和 Reactive 放在什么位置

不要把它们理解成“第 6、7 层压缩”。

更准确：

```text
正常 Context 治理层：
Budget / Snip / Micro / Auto

调用前风险控制：
Predictive Check / Blocking Limit

调用后错误恢复：
Collapse Drain / Reactive Compact
```

这是完整 Runtime 框架。

---

# 14. 复习结论

小林文章重点在：

> “平时怎么逐层把 Context 压下来。”

当前源码还值得补一句：

> **生产级 Context 管理必须同时覆盖：调用前主动治理、调用前增长预测、真实 Provider 拒绝后的恢复，以及恢复失败后的硬退出。**

到这里 Context Runtime 路径基本闭环。

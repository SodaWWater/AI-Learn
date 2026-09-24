# 06｜Auto-Compact：当前固定源码里真正完整可验证的重型 Context 机制

> 小林文章这一部分已经讲得比较完整。
>
> 本篇重点不是重复，而是补上当前源码相比文章更值得注意的几个变化：**动态 Buffer、Session Memory Compaction 优先、messagesToKeep、Skill 恢复预算、Media Strip、Compact 自己的 PTL Recovery。**

---

# 1. Auto-Compact 在整个体系里的位置

前面轻量机制处理不了时：

```text
Tool Result Budget
↓
Snip
↓
Micro-Compact
↓
仍然接近 Context 上限
↓
Auto-Compact
```

它与前面最大的区别：

> **真的重新组织 Conversation。**

---

# 2. 有效 Context Window 先预留 Summary 输出空间

源码：

```text
MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000
```

原因注释：

> Summary output 的 p99.99 是 17,387 tokens，因此向上留到 20K。

所以：

```text
effectiveContextWindow
=
rawContextWindow
-
reservedSummaryOutput
```

这里小林文章的解释仍然成立。

---

# 3. 文章需要补一个重要更新：Buffer 不再永远固定 13K

基础常量仍然是：

```text
AUTOCOMPACT_BUFFER_TOKENS = 13_000
```

但当前源码新增：

```text
getAutocompactBufferTokens(model)
```

规则：

```text
effective window < 400K
→ 13K

>= 400K
→ 30K

>= 800K
→ 50K
```

所以当前更准确公式：

```text
AutoCompact Threshold
=
Effective Context Window
-
Dynamic Buffer
```

而不是永远：

```text
Window - 20K - 13K
```

---

# 4. 为什么大窗口反而需要更大 Buffer

因为单 Turn 也会变大：

- 模型能输出更多；
- Tool Result 可能更大；
- 一轮增长不再是固定规模。

所以窗口越大：

> 给“下一轮突然膨胀”留的 Headroom 也增加。

这是当前源码比文章“绝对固定 13K”模型更生产化的一点。

---

# 5. Auto-Compact 前还有 Circuit Breaker

如果前几轮 Compact 连续失败：

```text
MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3
```

达到 3：

> 本 Session 不再继续无意义地每轮尝试。

源码注释记录过非常具体的生产事故：

```text
1,279 sessions
出现 50+ 连续失败
最高 3,272 次
约浪费 250K API calls/day
```

这就是 Runtime 章节已经学过的：

> Recovery 自己也必须被限制。

---

# 6. 递归守卫仍然非常重要

如果当前 Query Source 是：

```text
session_memory
compact
```

Auto-Compact 直接：

```text
return false
```

原因：

> Compact Agent 自己如果再 Compact，会形成递归甚至死锁。

这个点和小林文章一致。

---

# 7. 当前源码一个很重要的新分支：先尝试 Session Memory Compaction

当前：

```text
autoCompactIfNeeded()
```

达到阈值以后，并不是直接：

```text
compactConversation()
```

而是先：

```text
trySessionMemoryCompaction()
```

如果成功：

> 直接使用 Session Memory 生成的 CompactionResult。

失败/不可用才进入传统：

```text
compactConversation()
```

这体现一个新的方向：

> 已经有结构化 Session Memory 时，优先复用，而不是每次重新让模型全量总结。

这是小林文章当前版本里没有作为主线展开的一个补充。

---

# 8. Full Compact 之前会做预处理

当前传统 Compact 不是生吞所有原历史。

至少还有：

### Strip Images / Documents

图片和文档会替换成：

```text
[image]
[document]
```

原因：

> Summary 任务没必要重新吞完整媒体，而且媒体本身可能让 Compact 请求先爆掉。

---

### Strip Reinjected Attachments

某些 Skill Discovery 等下一轮本来就会重新注入。

如果摘要器再看一遍：

> 浪费 Token，还可能把“过期 Skill 推荐”写进 Summary。

所以先去掉。

---

### Micro-Compact

手动/传统 Compact 路径也会先做 Micro-Compact，尽量减少摘要输入。

---

# 9. Compact Prompt：文章讲的 9 段结构仍然成立

当前源码仍要求：

1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections
4. Errors and fixes
5. Problem Solving
6. All user messages
7. Pending Tasks
8. Current Work
9. Optional Next Step

其中当前版本还明确增加：

> **用户提出的安全相关约束必须逐字保留。**

例如：

- 某文件不能访问；
- 不允许上传某类数据；
- Secret 处理规则；
- 某操作禁止执行。

这说明 Compact 不只是保“任务语义”，还要保：

> **安全约束。**

---

# 10. 为什么仍然禁止 Summary Agent 调 Tool

Prompt 前面非常强地强调：

```text
TEXT ONLY
DO NOT CALL TOOLS
```

原因和文章讲的一样：

> Summary Agent 的职责只是重建 Context，不应该在这个特殊 Turn 里产生新 Action。

否则：

```text
总结任务
→ 模型想 Read 文件
→ Tool Call 被拒绝
→ 这唯一一轮摘要失败
```

---

# 11. Compact 后不再是简单“四段式”

文章常用：

```text
boundary
summary
attachments
hook results
```

当前源码的真实顺序是：

```text
boundaryMarker
↓
summaryMessages
↓
messagesToKeep
↓
attachments
↓
hookResults
```

也就是说：

> **多了一个 messagesToKeep。**

这很重要。

---

# 12. messagesToKeep 是什么

并不是所有 Compact 都必须“历史一刀切全没”。

当前 CompactionResult 允许：

```text
messagesToKeep?: Message[]
```

它用于：

- Session Memory Compact；
- Reactive Compact；
- Partial Compact；
- 某些需要保留最近/特定 Segment 的路径。

因此当前更准确说法：

> Auto-Compact 的主干仍是 Summary 重写，但 Compaction Framework 已支持“Summary + preserved segment”混合形式。

这是文章“所有 200 轮全部一刀切”的一个重要补全。

---

# 13. preservedSegment 甚至写入 Boundary Metadata

源码有：

```text
annotateBoundaryWithPreservedSegment()
```

记录：

```text
headUuid
anchorUuid
tailUuid
```

用于 Resume / Loader 重新把保留 Segment 接回正确 Message Chain。

所以：

> 保留最近消息不是临时拼接，而是持久化模型的一部分。

---

# 14. Compact 后恢复文件：文章数字仍然成立

当前常量：

```text
POST_COMPACT_MAX_FILES_TO_RESTORE = 5
POST_COMPACT_MAX_TOKENS_PER_FILE = 5_000
POST_COMPACT_TOKEN_BUDGET = 50_000
```

也就是：

> 最近/最重要文件有限恢复，而不是全量恢复。

---

# 15. 当前还增加了 Skill 恢复预算

源码：

```text
POST_COMPACT_MAX_TOKENS_PER_SKILL = 5_000
POST_COMPACT_SKILLS_TOKEN_BUDGET = 25_000
```

原因：

> Skill 本身也可能非常长，Compact 后如果无上限重新注入，会再次快速吃掉 Context。

这属于文章“附件恢复”机制的进一步工程化。

---

# 16. CLAUDE.md 为什么不需要塞进 Summary

这一点文章讲法基本正确。

`CLAUDE.md` 属于长期指令来源。

Compact 后：

> Context Cache / User Context 会重新构建，使它再次进入下一轮。

因此没必要要求 Summary Agent：

> 把 CLAUDE.md 原文再总结一遍。

这是：

```text
语义进度
→ Summary

长期规则
→ Context Rebuild
```

两条通道。

---

# 17. Compact 自己如果 Prompt Too Long 怎么办

这是很容易遗漏的极端情况：

> 我就是因为 Context 太长才要 Compact，但“做 Summary 的那个请求”自己也可能太长。

当前源码准备了：

```text
truncateHeadForPTLRetry()
```

如果 Compact Request 本身 PTL：

1. 按 API Round 分组；
2. 从最老的 Group 开始丢；
3. 丢到覆盖 Token Gap；
4. 至少保留一组可总结内容；
5. 必要时补 synthetic User marker；
6. 再尝试 Summary。

最多有受限 Retry。

这是一种：

> **损失性但能解锁 Session 的最后逃生通道。**

文章主线里通常不会把这个 corner case 展开。

---

# 18. Manual / Auto Compact 的主要差异

### Auto

```text
suppressFollowUpQuestions = true
customInstructions = undefined
```

目的：

> 不要因为压缩突然打断正在自动工作的 Agent。

### Manual /compact

允许：

```text
customInstructions
```

例如：

> 这次特别保留数据库迁移相关上下文。

---

# 19. Auto-Compact 复习结论

不要只记：

> “把全部历史总结成 9 段 Summary。”

当前源码更准确是：

> **当轻量治理不够时，Claude Code 先尝试 Session Memory Compaction；否则对有效历史做预处理后生成结构化 Summary，再用 Boundary + Summary + 可选保留 Segment + Attachments + Hook Results 重建新的 Context，并通过多类预算控制恢复内容。**

这才是当前版本完整的 Auto-Compact 心智模型。

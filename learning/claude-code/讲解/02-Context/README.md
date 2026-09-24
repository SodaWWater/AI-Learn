# Claude Code Context 学习专题

> 本专题建立在 Agent Runtime 之后。
>
> 目标不是把所有带 Context 的变量都背一遍，而是理解：**Claude Code 如何把多种信息组装成一次模型输入，以及当 Context 不断膨胀时，为什么需要多层、从轻到重的治理机制。**
>
> 源码基线：`claude-code-best/claude-code@77a7934e15d69da13879112ed7db695c9ee7a52a`
>
> 原文参考：`text/03-源码解析/03-上下文管理-Compact.md`

## 为什么这样组织

原文对 Auto-Compact 的讲解很有价值，也已经给出“大结果落盘 → Snip → Micro-Compact → Context Collapse / Auto-Compact”的金字塔视角。

但正式学习还需要补足三件事：

1. **先知道 Context 到底由什么组成。** 如果不知道 System Prompt、User Context、System Context、Messages、Memory Reminder、Tool Schema 分别从哪来，后面所有“压缩”都会失去对象。
2. **把文章教学模型与当前固定源码区分开。** 当前实现已经包含 Predictive AutoCompact、真实 413 后的 Reactive Recovery、Tool Result Budget、Context Collapse 与 AutoCompact 的互斥等更完整的生产逻辑。
3. **把 Memory / Skill 作为 Context 来源看待，但不提前进入 Memory / Skill 专题。** 这里只讲它们“怎样进入当前模型输入、怎样占 Context”，内部选择和存储机制留给后续专题。

## 学习主线

### 01. Context 总体架构与信息注入

文件：`01-Context总体架构与信息注入.md`

重点回答：

- Claude 一次模型调用到底看到什么？
- System Prompt / System Context / User Context / Messages / Tools 分别是什么？
- `CLAUDE.md` 为什么主要走 `<project-instructions>`？
- `<system-reminder>` 为什么不只是日期，而是一个通用“系统附加信息”载体？
- relevant memories、nested memory、Skill、IDE、Hook 等信息如何以 Meta User Message / reminder 进入 Context？
- Memory 为什么是 Context 的来源，不等于 Context 本身？

### 02. Context 治理总图：为什么不是一个 Compact 就够

重点回答：

- Context 为什么会持续增长？
- 哪些增长来自 Tool Result、哪些来自历史、哪些来自动态 Reminder？
- Claude Code 为什么采用“从轻到重”的分层治理，而不是每次都做全量摘要？
- `messagesForQuery` 在这里扮演什么角色？

这里会把消息生命周期只作为必要背景，不单独展开成一整课。

### 03. 第 1 层：Tool Result Budget / 大结果落盘

真实问题：

> Bash / Read / MCP 一次返回几十 KB 到几 MB，为什么不能全部塞进下一轮？

重点：

- Tool Result Budget；
- 持久化完整结果，只给模型 preview / stub；
- 这一步为什么是最轻、最值得优先做的治理；
- 与小林“大结果存磁盘”说法如何对应当前源码。

### 04. 第 2～3 层：Snip 与 Micro-Compact

重点：

- Snip 到底删什么，为什么不是简单“删最老 N 条”；
- Micro-Compact 为什么针对可重新获取的 Tool Result；
- 为什么局部治理比全量摘要便宜；
- 两者和 Auto-Compact 的关系。

### 05. 第 4 层：Context Collapse

重点：

- 什么叫“写时保留，读时投影”；
- 为什么原始历史可以保留，但模型只看到折叠视图；
- 90% / 95% 一类触发思想；
- 为什么启用 Context Collapse 时会抑制 Auto-Compact；
- 当前源码中这一机制的 Feature Gate / 实验边界。

### 06. 第 5 层：Auto-Compact 全量重写

重点：

- 为什么不是只压旧消息，而是重写整个有效历史；
- Summary Prompt；
- Boundary Marker；
- Summary Messages；
- Attachments；
- Hook Results；
- 文件、任务、CLAUDE.md、Memory 分别如何恢复；
- Manual Compact 与 Auto Compact 的差异；
- 熔断和递归守卫。

### 07. Predictive / Reactive：当前源码对原文的重要补全

重点：

- Predictive AutoCompact：为什么“现在没超”也要提前处理；
- `estimateMaxTurnGrowth()` 如何给下一轮增长预留空间；
- Reactive Compact：真实 413 以后如何恢复；
- Context Collapse Drain → Reactive Compact → 最终失败；
- Guard 如何防恢复死循环。

### 08. 小林文章 vs 当前源码：差异、补全与最终心智模型

把整套方案压成：

```text
信息注入
↓
控制大结果
↓
局部清理
↓
历史折叠
↓
重型摘要
↓
预测式保护
↓
真实 Overflow 后恢复
```

并明确：

- 哪些是文章为了教学做的简化；
- 哪些是当前源码新增或更复杂的实现；
- 哪些特性互斥；
- 哪些机制受 Feature Flag 控制；
- 面试时如何讲，不把术语堆在一起。

## 一个特别重要的边界：system-reminder 不等于“日期提醒”

当前源码里 `<system-reminder>` 是一个通用包装机制。它可以承载：

- currentDate 等 User Context；
- relevant memories；
- nested `CLAUDE.md` / conditional memory；
- auto-loaded Skill / Skill reminder；
- IDE 当前打开或选择内容；
- Plan / Auto Mode 提示；
- Hook additional context；
- deferred tools / MCP 等运行提示；
- 其他 Runtime 自动附加信息。

因此后续统一把它理解为：

> **Runtime 放进 User-role Messages 中、只给模型看的系统附加上下文载体。**

其中很多消息带 `isMeta: true`，并不等于用户真的输入。

## 学习原则

这个专题不追求函数覆盖率。

每个机制都固定回答四个问题：

1. **真实问题是什么？**
2. **为什么上一层不够？**
3. **这一层具体改了哪部分 Context？**
4. **代价是什么，什么时候才值得用？**

这样才能真正理解为什么 Claude Code 不是“Context 快满了就总结一下”这么简单。

# 01｜Context 总体架构与信息注入：Claude 一次调用模型到底看到了什么

> 本章先不讲 Compact。
>
> 目标只有一个：先把“Claude 这一轮到底看到了哪些信息、这些信息分别从哪条通道进入”讲清楚。
>
> 后续所有 Tool Result Budget、Snip、Micro-Compact、Context Collapse、Auto-Compact，本质都在管理这里的某一部分。

---

# 1. 先把 Context 这个词限定清楚

Claude Code 源码里有很多带 Context 的名字：

- `ToolUseContext`
- `userContext`
- `systemContext`
- Context Window
- Context Collapse

它们不是同一个东西。

本专题核心讨论的是：

> **某一次 Model Call 时，真正提供给模型的信息集合。**

也就是模型为什么会知道：

```text
这是一个 Node 项目
项目要求用 pnpm
当前 Git 分支是 feature/login
用户之前已经让我读过 auth.ts
刚才 Grep 找到了 3 个文件
之前保存的某条相关 Memory 提醒我一个已知坑
当前启用了某个 Skill
```

而 `ToolUseContext` 更接近 Runtime 自己运行 Tool 时使用的程序环境，例如 Abort、Permission、Tools、AppState、File State。它不是整包发送给模型。

---

# 2. 当前源码里，模型输入先看成三大块

真正调用模型时，可以先建立这个最简单的结构：

```text
Model Input
│
├─ ① System Prompt
│
├─ ② Messages
│
└─ ③ Tool Schemas
```

然后再看两条附加注入：

```text
systemContext
→ 追加进 System Prompt

userContext / attachments / reminders
→ 转成 User-role Meta Messages
→ 加进 Messages
```

所以源码思路可以简化成：

```text
systemPrompt + systemContext
            ↓
      fullSystemPrompt

userContext + messagesForQuery + dynamic attachments/reminders
            ↓
        modelMessages

fullSystemPrompt + modelMessages + tools
            ↓
           LLM
```

---

# 3. System Prompt：工作手册

System Prompt 主要回答：

> “你是什么 Agent，你应该如何工作？”

里面会包含：

- Claude Code 的身份和基本行为；
- Coding Task 的处理原则；
- Tool 使用原则；
- 输出风格；
- 一些安全和运行模式约束；
- 某些 Memory / Session Guidance / MCP 等动态 Section。

它不是单一写死字符串，而是动态组装的 `string[]` / `SystemPrompt`。

学习上先把它理解为：

> **长期、全局、Agent 级的工作规则。**

---

# 4. System Context：当前环境快照

当前 `getSystemContext()` 主要会提供 Git 相关现场，例如：

```text
Current branch: feature/login
Main branch: main

Status:
 M src/auth.ts

Recent commits:
...
```

最后通过：

```ts
appendSystemContext(systemPrompt, systemContext)
```

追加到 System Prompt。

所以：

```text
System Prompt
= 工作规则

System Context
= 当前运行环境的一些事实
```

一个重要细节：

> Git 状态是 Conversation 级快照，不保证随着后续 Tool 修改文件实时刷新。

模型后面如果需要实时状态，应该再次使用 Tool 获取。

---

# 5. User Context：不是“用户刚输入的那句话”

`getUserContext()` 当前主要会准备：

```text
CLAUDE.md / memory-file-derived project instructions
currentDate
```

但它们进入模型的方式并不一样。

---

# 6. CLAUDE.md：主要走 project-instructions

`prependUserContext()` 会把 `claudeMd` 从普通 User Context 中单独拿出来：

```text
<project-instructions>
...CLAUDE.md 内容...
</project-instructions>
```

然后构造一条 User-role Meta Message。

为什么不和普通 reminder 混在一起？

因为普通 reminder 有类似：

> “这些信息可能相关，也可能不相关。”

如果把项目规则埋进去，会削弱它的指令权重。

所以可以记：

```text
CLAUDE.md
→ userContext
→ <project-instructions>
→ Meta User Message
```

这是一条高权重的项目指令通道。

---

# 7. currentDate：走 system-reminder

`currentDate` 等普通 User Context 会被包装成：

```text
<system-reminder>
As you answer the user's questions, you can use the following context:

# currentDate
Today's date is ...

IMPORTANT:
this context may or may not be relevant...
</system-reminder>
```

再作为 User-role Meta Message 放进模型消息。

这就是我们上一轮提到的 reminder。

但这里必须纠正一个容易形成的误解：

> **system-reminder 绝不只是“日期提醒”。**

---

# 8. system-reminder 实际上是通用 Context 注入载体

当前 System Prompt 自己就明确告诉模型：

> Tool results and user messages may include `<system-reminder>` tags. These tags contain useful information and reminders and are automatically added by the system.

也就是说：

> `<system-reminder>` 是 Runtime 给模型附加系统背景信息的一种通用包装格式。

它可以出现在：

- User Message；
- Tool Result 附近；
- Attachment 转换后的 Message；
- Runtime 自动插入的 Meta Message。

这些内容通常不是用户本人输入的。

---

# 9. 你记得没错：Reminder 里确实包含 Memory

当前源码至少能看到几类 Memory 注入。

## 9.1 Relevant Memories

Runtime 可以先通过 `findRelevantMemories()` 选择与当前任务最相关的记忆文件。

选中后形成：

```text
attachment.type = relevant_memories
```

进入 API 前，`normalizeAttachmentForAPI()` / message normalization 会把这些记忆转换成 User Messages，并使用：

```text
wrapMessagesInSystemReminder(...)
```

也就是：

```text
Relevant Memory
↓
Attachment
↓
Meta User Message
↓
<system-reminder>
  memory content
</system-reminder>
↓
LLM Context
```

当前源码还专门限制：

- 每次最多若干相关 Memory；
- 单文件行数和字节数；
- Session 累计注入量；

原因很直接：

> Memory 本身也会吃 Context。

所以 Memory 召回不能无限塞。

---

## 9.2 Nested Memory / Nested CLAUDE.md

当 Claude 访问某个更深层目录时，可能发现该目录下还有更局部的 `CLAUDE.md` 或条件规则。

它们不是一开始全部加载。

而是当路径触发时形成：

```text
nested_memory attachment
```

然后被转换成类似：

```text
<system-reminder>
Contents of path/to/CLAUDE.md:

...
</system-reminder>
```

这可以理解成：

> **按访问路径懒加载的项目局部指令。**

所以：

```text
根级 CLAUDE.md
→ 主要进入 project-instructions

深层 / 后续触发的 CLAUDE.md
→ nested_memory attachment
→ system-reminder
```

两条通道不要混在一起。

---

## 9.3 Session Memory / Auto Memory

当前 Attachment 类型中还能看到：

```text
current_session_memory
relevant_memories
nested_memory
```

这说明 Memory 并不是只有“启动时加载 CLAUDE.md”这一种形式。

在不同机制下：

- 当前 Session 的工作记忆；
- 长期 memdir 中召回的相关记忆；
- 目录级项目规则；

都可能在不同时间进入当前模型 Context。

Memory 专题会讲它们分别怎么产生和选择。

Context 专题只需要记：

> **一旦被选中，它们最终都必须变成当前 Model Call 能看到的信息，因此会占用 Context。**

---

# 10. Reminder 还不只装 Memory

当前源码还会用 `<system-reminder>` 包装很多东西，例如：

- Skill auto-load / Skill reminder；
- IDE 当前选中的代码；
- IDE 当前打开的文件；
- Plan Mode / Auto Mode 状态；
- Hook additional context；
- Deferred Tools；
- MCP 资源或提示；
- Tool 文件读取提醒；
- Edited file reminder；
- Diagnostics；
- Task / Todo 提醒。

所以最好的理解不是：

```text
system-reminder
= Memory
```

而是：

```text
system-reminder
= Runtime 给模型附加“这轮需要知道但不是用户原始输入”的上下文载体
```

Memory 只是其中非常重要的一类。

---

# 11. Messages：动态增长的主体

假设用户说：

> 帮我查登录为什么 401。

最初 Conversation Messages：

```text
User:
帮我查登录为什么 401
```

模型第一轮：

```text
Assistant:
tool_use A = Grep(...)
```

Tool 返回：

```text
User:
tool_result A = auth.ts, login.ts
```

第二轮又会带上这些历史。

所以 Messages 是：

> **Agent Loop 每一轮不断累积 Action / Observation 的动态主体。**

这也是 Context 最容易越滚越大的地方。

---

# 12. messagesForQuery：治理后的模型可见历史

Runtime 手里有 `messages`，但不会保证原样全部发送。

进入 Model Call 前会得到：

```text
messagesForQuery
```

它可以理解为：

> **经过 Context 治理之后，这一轮真正准备发送的 Conversation History 版本。**

后面的专题重点就是：

```text
messages
↓
Tool Result Budget
↓
Snip
↓
Micro-Compact
↓
Context Collapse / Auto-Compact
↓
messagesForQuery
```

所以消息生命周期不是我们下一课的主角。

它只需要提供这个关键背景：

> 多层治理最终都在影响“这一轮模型到底看到哪一版历史”。

---

# 13. Tools：又是一条独立输入通道

`callModel()` 还会单独收到：

```text
tools
```

也就是 Tool Schema：

```text
Grep:
  description
  input schema

Read:
  description
  input schema
...
```

它们不是 Conversation Message，也不是 System Prompt。

但从广义 Context 角度，它们当然属于模型当前掌握的信息。

所以可以区分：

```text
狭义 Model Context
= System Prompt + Messages

广义 Model Input
= System Prompt + Messages + Tool Schemas + 其他请求配置
```

---

# 14. 用一个完整例子拼起来

用户：

> 帮我看看登录为什么一直返回 401。

项目根 `CLAUDE.md`：

```text
这是 Node.js 项目
使用 pnpm
auth 在 src/auth
修改后运行 pnpm test
```

相关长期 Memory 被召回：

```text
过去处理过这个项目：
JWT 中间件曾经因为 Bearer 前缀空格出过问题
```

当前 Git：

```text
branch = feature/login
M src/auth.ts
```

那么模型这一轮可能看到：

## System Prompt

```text
Claude Code 基础规则
Tool 使用规则
Coding 行为规则
...
gitStatus:
Current branch: feature/login
M src/auth.ts
```

## Messages 前缀

```text
Meta User:

<project-instructions>
这是 Node.js 项目
使用 pnpm
...
</project-instructions>
```

然后可能还有：

```text
Meta User:

<system-reminder>
Relevant memory:
JWT 中间件曾经因为 Bearer 前缀空格出过问题
</system-reminder>
```

以及：

```text
Meta User:

<system-reminder>
Today's date is ...
</system-reminder>
```

最后才是：

```text
User:
帮我看看登录为什么一直返回401
```

## Tools

```text
Grep
Read
Edit
Bash
...
```

所以模型真正做决策时，看到的从来不是孤零零一句用户问题。

---

# 15. 为什么这个架构对后面压缩特别重要

现在可以看到，Context 增长来源至少有：

```text
Conversation History
Tool Results
Memory Reminders
Skill Reminders
Attachments
Project Instructions
Tool Schemas
System Prompt
```

但这些信息性质完全不同。

例如：

```text
巨大的 Bash 日志
→ 可以裁

旧 Tool Result
→ 可能可重新获取

长期项目规则
→ 不能随便摘要掉

相关 Memory
→ 可能按需重注入

Conversation 语义进度
→ 适合摘要

当前任务状态
→ 可能要原样恢复
```

这正是 Claude Code 需要“多层 Context 管理”，而不是简单：

```text
超过 80%
→ 全部做摘要
```

的根本原因。

---

# 16. 本章最终心智模型

先记模型输入：

```text
System Prompt
  ↑
systemContext

Messages
  ↑
userContext
  ↑
project-instructions
  ↑
system-reminder attachments
  ↑
Conversation / Tool Results

Tools
  ↑
Tool Schemas

        ↓
       LLM
```

再记三条边界：

### CLAUDE.md 不等于普通 Reminder

根级项目指令主要走：

```text
<project-instructions>
```

### Reminder 不等于日期

它是通用 Runtime Context 注入载体，Memory / Skill / IDE / Hook / Mode 等都可能通过它进入。

### Memory 不等于 Context

```text
Memory
= 可保存 / 可召回的信息来源

Context
= 本轮模型真正看到的信息集合
```

Memory 被召回以后，才成为 Context 的一部分。

---

# 17. 下一课不讲“消息生命周期”，直接进入 Context 治理总图

下一步我们直接回答：

> **既然 Context 有这么多来源，而且 Tool Loop 每一轮都会继续增长，Claude Code 到底用哪几层机制控制它？为什么要从轻到重，而不是直接 Auto-Compact？**

主线会是：

```text
Tool Result Budget / 大结果落盘
↓
Snip
↓
Micro-Compact
↓
Context Collapse 或 Auto-Compact
↓
Predictive Protection
↓
真实 413 后 Reactive Recovery
```

然后再逐层拆真实问题、数据变化、代价与源码实现。

这也是本专题真正的重点。

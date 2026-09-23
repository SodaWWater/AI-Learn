# Claude Code Agent Runtime 学习专题

> 本目录是源码校准后的学习讲义，不修改小林原文。
>
> 学习源码基线：claude-code-best/claude-code @ 77a7934e15d69da13879112ed7db695c9ee7a52a
>
> 来源边界：该仓库是逆向学习树，不是 Anthropic 官方源码。版本说明见 ../../来源与版本.md。

## 为什么单独做这一套讲义

小林的“主循环 Query”文章非常适合建立直觉：Claude Code 不是一次模型调用，而是模型、工具、结果不断往返的 Agent Loop。真正进入源码后，query.ts 又包含大量恢复、状态、并发和清理逻辑。如果直接把所有机制一次性列出来，很容易只记住一堆名词，却不知道它们为什么存在。

这套讲义采用另一种顺序：

1. 先把整个 Runtime 的总体架构和正常路径讲清楚。
2. 再只挑 4 个最有工程价值的问题，用真实故障场景学习。
3. 每个专业词都先出现问题，再解释这个词是给什么机制起的名字。
4. 最后用 Context Too Long 把 Runtime 自然过渡到下一专题 Context。

目标不是背 query.ts，而是理解：

> 一个几十行就能写出的 Agent Demo，为什么到了生产环境会演化成上千行 Runtime。

## 学习顺序

### 01. 总体架构与正常主循环

文件：01-总体架构与正常主循环.md

回答：

- ask → QueryEngine.submitMessage → query → queryLoop 到底是不是四个独立模块？
- 为什么 query() 看起来薄，却不能简单删掉？
- Conversation、User Turn、Loop Iteration 分别是什么？
- 用户一句“帮我修登录 401”进入后，数据如何逐步变化？
- queryLoop 正常一圈如何完成 Model → tool_use → Tool → tool_result → Model？

先把这篇学透，再看工程异常。

### 02. Case 1：State 与防无限循环

文件：02-案例1-State与防无限循环.md

核心事故：

> 自动恢复本来是为了救任务，却因为没有记录“已经恢复过几次”，变成无限 Retry，持续烧 API。

重点理解：

- 为什么 while(true) 里的状态不能散落在隐式变量里；
- State 里哪些字段实际上是“防重复”和“计数器”；
- transition 为什么要记录“上一轮为什么继续”；
- Guard、Retry、Circuit Breaker 分别是什么。

### 03. Case 2：Tool 中断与消息协议修复

文件：03-案例2-工具中断与协议修复.md

核心事故：

> 模型已经发出 tool_use，工具却因为 Ctrl+C、网络错误、Fallback 等没有产生 tool_result。下一次请求可能因为消息协议不完整被 API 拒绝。

重点理解：

- tool_use 和 tool_result 为什么必须配对；
- 什么叫“孤儿 tool_use”；
- yieldMissingToolResultBlocks() 为什么要制造 synthetic tool_result；
- Abort、Streaming Failure、Fallback 为什么都会遇到同一类协议问题；
- “程序停止”与“消息状态修复”为什么是两件事。

### 04. Case 3：模型输出截断后的自动恢复

文件：04-案例3-输出截断与自动恢复.md

核心事故：

> 模型正在完成长任务，输出撞上 max_output_tokens，中途被切断。

重点理解：

- 为什么不能直接把错误显示给用户；
- 第一次为什么可以提高输出上限后重试同一请求；
- 仍然截断时，为什么把一条内部恢复消息加入下一轮；
- nudge 到底是什么；
- 为什么恢复最多只能有限次。

### 05. Case 4：Streaming Tool Execution 与并发边界

文件：05-案例4-流式工具执行与并发边界.md

核心问题：

> 如果等模型完整输出后才开始工具，模型生成时间和工具执行时间完全串行；但如果所有 Tool 都并发，又可能互相覆盖状态。

重点理解：

- StreamingToolExecutor 如何在模型还在流式输出时就开始 Tool；
- concurrent-safe 是什么意思；
- 为什么并发安全的 Tool 可以重叠执行；
- 为什么不安全 Tool 需要独占执行；
- fail-closed 为什么是“判断不清时按不安全处理”。

### 06. Context Too Long：从 Runtime 过渡到 Context

文件：06-Context-Too-Long过渡.md

这里会专门对齐：

- 小林文章里的教学模型；
- 当前固定源码里的实际实现。

你会看到当前源码已经不只是“API 413 后 Compact 一次”，而是存在一个逐层控制 Context 增长的管道，包括：

Tool Result Budget → Snip → MicroCompact → Context Collapse → AutoCompact → Predictive AutoCompact → 真实 413 后 Reactive Recovery。

这篇只解释“为什么 Runtime 需要这些保护”，具体每种 Context 技术的内部实现留给 Context 专题。

### 07. Runtime 复盘与面试表达

文件：07-Runtime复盘与面试表达.md

把前面内容重新压缩成：

- 一张总体心智模型；
- 一套 2 分钟回答；
- 一套被追问时的展开顺序；
- 与 Hermes / LangGraph 的对应关系；
- 专业词中文解释表；
- 源码阅读导航。

## 每个工程案例统一怎么学

为了避免再次变成术语清单，四个案例统一使用九步：

1. 真实开发事故：先看到用户或系统会遇到什么问题。
2. 最简单实现：如果我们自己写 Demo，最自然会怎么写。
3. Bug 为什么出现：明确哪条假设在生产环境失效。
4. 事故现场数据：直接看 messages / state 在出错瞬间长什么样。
5. Claude Code 修复：说明 Runtime 实际做了什么。
6. 修复后数据：对比修复前后的变化。
7. 专业词解释：只解释本案例真正用到的词。
8. 通用迁移：说明自己以后写 Agent 时怎么复用这个思想。
9. 源码定位：最后才进入关键函数和文件。

## 这套讲义和小林文章是什么关系

不是替代，而是合并。

小林文章负责：

- 把复杂源码压成可理解的主线；
- 选择最有代表性的机制；
- 给出为什么值得学的直觉。

本讲义负责：

- 对齐当前固定源码；
- 补充文章之后源码已经出现的实现演化；
- 把“名词”还原成“真实开发问题”；
- 展示 messages / State 如何实际变化；
- 区分教学简化和当前源码事实。

如果文章与固定源码不一致，以固定源码为准，并在讲义中明确标注“文章教学模型”和“当前源码实现”。

## 建议学习节奏

不要一口气读完七篇。

推荐：

第一天：01  
第二天：02  
第三天：03  
第四天：04  
第五天：05  
第六天：06 + 07

每学一个案例，至少能自己回答三句话再进入下一篇：

- 真实问题是什么？
- Runtime 为什么不能用最简单写法？
- Claude Code 的修复核心改变了哪一份数据或哪一个状态？

如果这三句答不出来，继续看案例，不急着背源码函数名。

# Claude Code 学习讲义

这里放“基于专栏教学思路、再用固定源码校准”的正式学习内容。

与 ../text/ 的区别：

- ../text/：来源文章正文，尽量保持原始学习资料边界；
- 本目录：重新组织后的学习教材，可以补充源码事实、工程案例、跨框架比较和学习图。

## 当前专题

### 01. Agent Runtime

入口：01-Agent-Runtime/README.md

学习顺序：

1. 总体架构与正常主循环；
2. State 与防无限循环；
3. Tool 中断与消息协议修复；
4. 输出截断与自动恢复；
5. Streaming Tool Execution 与并发边界；
6. Context Too Long 过渡；
7. Runtime 复盘与面试表达。

源码基线统一遵循 ../来源与版本.md。

### 02. Context

入口：02-Context/README.md

当前专题已补齐，建议已读过小林文章时优先按 **02 → 05 → 06 → 07 → 08** 复习：先看总图，再看源码差异与补漏。

专题主线：

~~~text
Context Assembly
→ Tool Result Budget
→ Snip
→ Micro-Compact
→ Context Collapse / Auto-Compact
→ Predictive AutoCompact
→ Reactive Recovery
→ 小林文章 vs 当前源码补全
~~~

## 后续规划

~~~text
03-Memory
04-Retrieval
05-Skill
06-Tool-Permission-Security
~~~

每个专题都坚持：

> 先总体视角 → 再正常路径 → 再少数高价值生产案例 → 最后源码定位。

避免把源码函数清单直接当成教学内容。

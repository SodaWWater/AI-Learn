---
id: LANGGRAPH-VAULT-README
title: LangGraph Interview Vault
status: teaching_draft
updated: 2026-09-15
---

# LangGraph Interview Vault

这是面向 **AI Agent 开发岗位** 的 LangGraph 学习 Vault。目标不是先背零散题目，而是先建立完整框架心智模型，再进入核心机制和生产级开发场景。

## 本地打开

1. 在本地 `AI-Learn` 仓库执行 `git pull`。
2. 打开 Obsidian，选择 **Open folder as vault**。
3. 选择目录：`AI-Learn/learning/langgraph-vault`。
4. 首先打开 [[00-开始这里]]。

## 当前进度

- Part 1：LangGraph 全景地图 —— **已完成第一版**。
- Part 2：一次数据分析 Agent 的完整运行旅程 —— **已完成第一版**。
- Part 3：从零编排同一个 Agent —— 待生成。
- Part 4：核心机制面试题 —— 待生成。
- Part 5：生产级 Agent 场景题 —— 待生成。

## Part 2 相比 Part 1 的讲解升级

Part 1 主要负责“知道有什么”。Part 2 开始要求每个机制都同时回答：

1. 它在完整运行流程里的位置；
2. 为什么这里需要它；
3. 不使用它会怎样；
4. 用真实业务数据时状态如何变化；
5. 关键代码与运行时行为怎样对应。

因此 Part 2 会大量使用整体流程图、时序图、状态快照、真实的教学数据和通俗类比。

## 教学原则

- 贯穿案例统一使用“集团采购经营数据分析 Agent”。
- 不采用“先造简单问题、再逐步发现问题”的慢节奏；直接解释是什么、为什么使用、用于什么场景以及和其他机制如何协作。
- 图用于表达结构、运行、状态变化和调用关系，不只是装饰。
- 专业术语使用中文工程语境 + 英文原名；代码标识符保持原样。
- LangGraph 技术行为优先依据官方文档；业务案例只是教学载体，不反向证明框架行为。

> [!warning] 状态说明
> 本 Vault 当前是 `teaching_draft`，不是仓库已经完成来源覆盖审计的正式 LangGraph 知识库。Part 1 与 Part 2 的框架行为按 2026-09-15 的 LangGraph 官方文档核对；后续可运行代码章节仍需锁定具体依赖版本并实际执行验证。

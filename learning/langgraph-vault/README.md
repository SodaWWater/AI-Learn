---
id: LANGGRAPH-VAULT-README
title: LangGraph Interview Vault
status: teaching_draft
updated: 2026-09-16
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
- Part 3：从零编排同一个 Agent —— **已完成第一版**。
- Part 4：核心机制面试题 —— 待生成。
- Part 5：生产级 Agent 场景题 —— 待生成。

## Part 3 的定位

Part 1 解决“有什么”，Part 2 解决“怎么跑”，Part 3 解决“怎么写”。

Part 3 会固定同一个采购经营数据分析 Agent，从业务需求开始依次完成：

```text
业务需求
→ Graph 蓝图
→ State Schema
→ Node 设计
→ Edge / Conditional Edge / Command
→ Parallel / Send / Reducer
→ LLM / Tool 接入
→ compile
→ invoke / stream
→ Checkpointer / Thread
```

这部分不要求你先背 API，而是让每一行代码都能重新映射回 Part 1 和 Part 2 的整体图。

## 教学原则

- 贯穿案例统一使用“集团采购经营数据分析 Agent”。
- 不采用“先造简单问题、再逐步发现问题”的慢节奏；直接解释是什么、为什么使用、用于什么场景以及和其他机制如何协作。
- 图用于表达结构、运行、状态变化和调用关系，不只是装饰。
- 专业术语使用中文工程语境 + 英文原名；代码标识符保持原样。
- LangGraph 技术行为优先依据官方文档；业务案例只是教学载体，不反向证明框架行为。
- 示例代码分清“教学可执行骨架”和“真实 LLM / 数据平台集成”，不把 mock 结果伪装成真实模型调用。

> [!warning] 状态说明
> 本 Vault 当前是 `teaching_draft`，不是仓库已经完成来源覆盖审计的正式 LangGraph 知识库。Part 1～3 的 API 与运行行为按 2026-09-16 的 LangGraph 官方文档核对；配套 Part 3 代码用于学习结构，未在本仓库的锁定依赖环境中执行验证。
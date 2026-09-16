---
id: LANGGRAPH-VAULT-README
title: LangGraph Interview Vault
status: teaching_draft
updated: 2026-09-16
---

# LangGraph Interview Vault

这是面向 **AI Agent 开发岗位** 的 LangGraph 学习 Vault。前三部分建立框架全貌、运行模型和开发编排；之后通过公开面经题池与深度追问链，把框架机制放入真实工程问题中学习。

## 本地打开

1. 在本地 `AI-Learn` 仓库执行 `git pull`。
2. 打开 Obsidian，选择 **Open folder as vault**。
3. 选择目录：`AI-Learn/learning/langgraph-vault`。
4. 首先打开 [[00-开始这里]]。

## 当前进度

- Part 1：LangGraph 全景地图 —— **已完成第一版**。
- Part 2：一次数据分析 Agent 的完整运行旅程 —— **已完成第一版**。
- Part 3：从零编排同一个 Agent —— **已完成第一版**。
- 面试题池研究 —— **已完成第一版（69 道候选题）**。
- 20 条深度主链 —— **已完成路线设计**。
- Part 4：核心/综合机制面试题 —— **M01～M03 已完成第一版**。
- Part 5：生产级 Agent Engineering —— 待后续主链逐步进入。

## 当前学习入口

优先从 [[讲解/04-深度面试主链/00-Part4导航|Part 4 深度面试主链]] 开始。

第一批：

- [[讲解/04-深度面试主链/01-M01-为什么是LangGraph|M01 为什么是 LangGraph]]
- [[讲解/04-深度面试主链/02-M02-一次真实请求完整调用链|M02 一次真实请求完整调用链]]
- [[讲解/04-深度面试主链/03-M03-Graph拆分与多Agent边界|M03 Graph 拆分与 Multi-Agent 边界]]

## 面试题研究方法

题池明确区分：

- 真实/verified 面试证据；
- 二次面经整理；
- 专项题库补漏；
- 官方文档只做版本核验。

69 道原题没有因为“压缩”为 20 条主链而删除。主链只是把相互依赖的问题串成真实面试中的连续追问。

## Part 4 的教学原则

- 先给可以直接用于面试表达的回答，再做深讲。
- 不重新平铺 State / Node / Checkpoint 定义，而是在综合问题里反复使用并深入。
- 每条主链同时包含架构图、真实采购数据分析案例、关键代码、追问题、错误回答和生产边界。
- 面经决定“值得学什么”，官方文档决定“当前版本应该怎么答”。
- 权限、幂等、安全、失败恢复等能力不会包装成 LangGraph 自动提供的功能。
- 专业术语使用中文工程语境 + 英文原名；代码标识符保持原样。

> [!warning] 状态说明
> 本 Vault 当前仍是 `teaching_draft`。面试题池是 2026-09-16 的公开检索快照，不表示互联网永久绝对完整。Part 4 每篇正式答案都应继续用 LangGraph / LangChain 当前官方文档核验版本相关事实。

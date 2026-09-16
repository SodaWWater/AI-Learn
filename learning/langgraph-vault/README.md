---
id: LANGGRAPH-VAULT-README
title: LangGraph Interview Vault
status: teaching_draft
updated: 2026-09-16
---

# LangGraph Interview Vault

这是面向 **AI Agent 开发岗位** 的 LangGraph 学习 Vault。前三部分先建立框架全貌、运行模型和开发编排；之后不直接凭空生成面试题，而是先研究公开面经和专项题库，再决定正式学习路线。

## 本地打开

1. 在本地 `AI-Learn` 仓库执行 `git pull`。
2. 打开 Obsidian，选择 **Open folder as vault**。
3. 选择目录：`AI-Learn/learning/langgraph-vault`。
4. 首先打开 [[00-开始这里]]。

## 当前进度

- Part 1：LangGraph 全景地图 —— **已完成第一版**。
- Part 2：一次数据分析 Agent 的完整运行旅程 —— **已完成第一版**。
- Part 3：从零编排同一个 Agent —— **已完成第一版**。
- 面试题池研究 —— **已完成第一版（2026-09-16 快照）**。
- Part 4：核心/综合机制面试题 —— 尚未开始写答案，等待从题池选主线。
- Part 5：生产级 Agent 场景题 —— 尚未开始写答案。

## 面试题池

当前已经从第一人称面经、带岗位/日期的面经整理、LangGraph 专项题库以及当前官方文档中整理出 **69 道高价值候选题**。

入口：[[面试题池/00-题目池说明]] → [[面试题池/01-高价值题目池]]。

题池明确区分：

- 真实/verified 面试证据；
- 二次面经整理；
- 专项题库补漏；
- 官方文档只做版本核验。

因此不会把“某 SEO 题库写了 250 道”误当成“市场高频 250 道”。

## 教学原则

- 贯穿案例统一使用“集团采购经营数据分析 Agent”。
- 基础知识不再反复扩写；后续通过综合面试题把 State、Reducer、Checkpoint、Retry、Security 等机制放进真实工程问题里深入。
- 面经决定“值得学什么”，官方文档决定“当前版本应该怎么答”。
- 图用于表达结构、运行、状态变化和调用关系，不只是装饰。
- 专业术语使用中文工程语境 + 英文原名；代码标识符保持原样。
- 不把二次题库包装成公司真题，不虚构面试频率。

> [!warning] 状态说明
> 本 Vault 当前仍是 `teaching_draft`。面试题池是 2026-09-16 的公开检索快照，不表示互联网永久绝对完整。后续正式答案必须继续以 LangGraph / LangChain 当前官方文档做版本核验。

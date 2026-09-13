---
vault: Hermes 独立学习 Vault
status: active_draft
updated_at: 2026-09-12
---

# Hermes 独立学习 Vault

这是一个可以直接用 Obsidian 打开的独立 Vault。它与 AI-Learn 的 RAG 知识库分开，Hermes 的课程参考仓库和官方源码只作为外部证据，不直接混入正式章节正文。

## 阅读顺序

1. [[00-开始这里]]：章节状态、资料边界和阅读规则。
2. [[章节总览]]：第 1–12 章的最新规划和完成状态。
3. [[chapters/01-系统全貌-对象关系与运行边界-正式占位]]、[[chapters/02-Turn生命周期-租约与并发隔离-正式占位]]、[[chapters/03-AgentLoop与Iteration-正式占位]]：前三章正式占位，等待后续回顾时按新规划重编。
4. [[chapters/04-context-engineering-request-assembly]]：当前正式学习入口，解释 Context 的真实对象、文件装载和请求组装。
5. [[chapters/05-context-compression-session-rotation-recovery]]：完整解释压缩算法、原地压实、会话轮换、持久化、回滚和恢复。
6. [[chapters/06-memory-history-external-provider]]：先讲 Memory 整体架构，再讲 History、本地文件、外部 Provider 和 review 生命周期。
7. [[附录/术语与源码索引]]：固定源码提交和专有名词索引。
8. [[来源与版本]]：官方源码、课程仓库和本地参考包的证据边界。

## 来源边界

- 官方 Hermes 源码固定提交：`f97a4102dd3864eed0c85132850ce7e06f13e09a`。
- 课程仓库固定提交：`d9e02cbed9dbeb2ad30f7a63905a831ca30cdba6`。
- 课程仓库只用于发现概念和文件名；与官方源码冲突时以官方源码为准。
- 本 Vault 不复制许可不明确的外部全文，只保留自己的解释、短引文、定位和关系。

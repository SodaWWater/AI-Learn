---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-REWRITE
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 查询改写（Query Rewrite）第三轮独立补漏

## 1. 本轮目标与边界

本轮固定 LangChain MultiQueryRetriever（LangChain 多查询检索器）和 LlamaIndex QueryFusionRetriever（LlamaIndex 查询融合检索器）的当前 Source Commit（源码提交），核对 Original-query Branch（原查询分支）、Generated-query Count（生成查询数量）、Sync / Async Execution（同步/异步执行）、Deduplication（去重）和 Fusion Mode（融合模式）。同时补 Rewrite Branch（改写分支）的权限重绑定、安全边界和 Counterfactual Ablation（反事实消融）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | LangChain 实现（LangChain Implementation） | `repo:langchain-ai/langchain class MultiQueryRetriever include_original agenerate_queries unique_union` | GitHub 官方仓库（Official Repository） |
| Q-302 | LlamaIndex 实现（LlamaIndex Implementation） | `repo:run-llama/llama_index class QueryFusionRetriever num_queries fusion mode use_async` | GitHub 官方仓库（Official Repository） |
| Q-303 | 安全（Security） | `query rewrite prompt injection authorization filter derived query RAG` | OWASP 官方安全指南（Official Security Guidance）与既有 Azure 权限过滤文档 |
| Q-304 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG Query Rewrite MultiQuery 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `langchain-multi-query-retriever-2026` | 官方仓库（Official Repository） | `included` | 固定 Commit（提交），核对默认生成三个改写、默认不含原查询、异步并发和 Unique Union（唯一并集） |
| `llamaindex-query-fusion-retriever-2026` | 官方仓库（Official Repository） | `included` | 固定 Commit（提交），核对默认总查询数四、始终包含原查询、默认 Simple Fusion（简单融合）和多种 Fusion Mode（融合模式） |
| `owasp-llm-top10-2025` | 官方安全指南（Official Security Guidance） | `included_existing` | 将 Prompt Injection（提示注入）风险映射到改写器输入和派生查询，不重复登记来源 |
| `azure-search-security-filter-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 证明 Authorization Principal（授权主体）必须由可信会话注入并用于每次查询 |

## 4. 当前实现差异

| 契约 | LangChain MultiQueryRetriever（LangChain 多查询检索器） | LlamaIndex QueryFusionRetriever（LlamaIndex 查询融合检索器） | 工程影响 |
|---|---|---|---|
| 默认生成数量（Default Generated Count） | Prompt（提示词）要求 3 个生成查询 | `num_queries=4` 表示 1 个原查询加最多 3 个生成查询 | “默认四个改写”或“默认三个总查询”都不是跨框架事实 |
| 原查询（Original Query） | `include_original=False` | 查询列表起始即包含 Original Query（原查询） | Control Branch（控制分支）必须显式验证 |
| 聚合（Aggregation） | Document Unique Union（文档唯一并集） | Simple / RRF / Relative-score / Distance-based Fusion（简单/倒数排名/相对分数/距离融合） | 同名 Multi-query（多查询）并不代表同一 Ranking Semantics（排序语义） |
| 执行（Execution） | 同步循环；异步使用 `asyncio.gather` | `use_async=True` 默认异步；每个 Query × Retriever 执行 | Timeout（超时）、Cancellation（取消）和并发预算需在应用层补齐 |

## 5. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `QRW-K-301` | `knowledge` | Multi-query（多查询）的“是否保留 Original Query（原查询）”“总分支数”“去重方式”和“融合算法”都是版本化实现契约，不能由框架名称推断 | 两个当前源码来源 | `new` |
| `QRW-K-302` | `knowledge` | Rewrite Branch（改写分支）是派生的检索请求，而不是新的 Authorization Principal（授权主体）；业务 Filter（过滤器）可以来自理解结果，权限 Filter（过滤器）必须从可信会话重新绑定到每个分支 | `azure-search-security-filter-docs-2026`; `owasp-llm-top10-2025` | `new` |
| `QRW-P-301` | `problem_question` | 从 LangChain 切换到 LlamaIndex 或升级版本后仍沿用“默认包含原查询、默认 RRF、默认查询数”的假设，导致 Recall（召回率）、Latency（延迟）和排序静默变化 | 两个当前源码来源 | `new` |
| `QRW-P-302` | `problem_question` | Multi-query（多查询）异步并发没有 Per-branch Timeout（分支超时）、Cancellation（取消）、Global Deadline（全局截止时间）和 Partial-result Policy（部分结果策略）时，一个慢分支会耗尽整体预算 | 两个当前源码来源 | `new` |
| `QRW-P-303` | `problem_question` | Rewrite Prompt（改写提示词）吸收用户指令后生成扩大范围、移除租户条件或暴露敏感实体的查询；若只在原查询绑定权限，派生分支可能越权 | `owasp-llm-top10-2025`; `azure-search-security-filter-docs-2026` | `new` |
| `QRW-E-301` | `evaluation` | Counterfactual Branch Ablation（反事实分支消融）至少比较 Original-only（仅原查询）、Each-branch-only（仅单分支）、All-minus-one（全部减一分支）、Fusion-only Change（仅更换融合）和 Rewrite-off（关闭改写） | 两个当前源码来源与 `rag-fusion-2024` | `new` |
| `QRW-S-301` | `solution` | 每个分支保存 `rewrite_id`、Parent Query ID（父查询标识符）、Exact-token Preservation（精确词元保留）、Trusted Filter Hash（可信过滤器哈希）、Retriever（检索器）、Deadline（截止时间）和 Returned Document IDs（返回文档标识符），形成可归因 Trace（追踪） | 本轮来源与既有可观测性来源 | `new` |

## 6. 公开面试题来源核验

本轮公开页面仍归入 `RAG-SCENE-015` 的 Multi-Query（多查询）、HyDE（假设文档嵌入）、Query Expansion（查询扩展）和语义漂移问题；其他页面为公开题库的重复表达，没有独立的新工程条件，故不新增题目。

## 7. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 词项扩展、多查询、HyDE、分解、Step-back Prompting（后退式提示）和会话改写已覆盖 |
| 实现（Implementation） | `covered` | 两个框架的当前 Source Commit（源码提交）和默认行为已固定 |
| 工程问题（Engineering Problem） | `covered` | 保真、偏题、重复放大、版本漂移、并发预算与越权已登记 |
| 解决方案（Solution） | `covered` | Original-query Control Branch（原查询控制分支）、Gate（闸门）、Timeout（超时）、可信 Filter（过滤器）与 Fallback（回退）已覆盖 |
| 评估（Evaluation） | `covered` | Token 保留、分支召回、融合、端到端和 Counterfactual Ablation（反事实消融）已覆盖 |
| 公开面试题（Public Interview Question） | `covered` | 公开题库可回链，未复制重复题 |
| 时效（Freshness） | `covered` | 源码 URL 固定 Commit（提交），产品 Preview（预览）边界仍保留 |
| 安全或治理（Security or Governance） | `covered` | Prompt Injection（提示注入）、敏感实体和逐分支授权重绑定已补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接 Understanding（理解）、Routing（路由）、Retrieval（检索）、Fusion（融合）、Evaluation（评估）和 Production Governance（生产治理） |

## 8. 冲突、版本与未验证假设

- LangChain 当前实现返回 Unique Union（唯一并集）而不是 RRF（倒数排名融合）；LlamaIndex 当前默认 Fusion Mode（融合模式）是 Simple（简单），不是 RRF。教程示例不能覆盖这些版本化默认值。
- `asyncio.gather` 或框架 `use_async` 只表示并发执行路径，不自动提供 Production Timeout（生产超时）、Bulkhead（舱壁隔离）、Cancellation（取消）和预算分配。
- Prompt Injection（提示注入）安全指南给出威胁类别，不证明某个 Guardrail（防护措施）可以彻底阻断攻击；授权过滤必须独立于改写模型。
- Counterfactual Ablation（反事实消融）是仓库要求建立的评估协议，本轮只完成证据和设计登记，尚未生成业务数据集。

## 9. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 10. 下一轮动作

建立 Rewrite Fidelity Dataset（改写保真数据集）与 Branch Trace Schema（分支追踪模式），覆盖产品号、错误码、日期、地域、否定、范围、权限和多轮指代；对两个固定框架版本执行相同数据集的行为差异测试。

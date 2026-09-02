---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-REWRITE
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 查询改写（Query Rewrite）第二轮独立补漏

## 1. 本轮目标与边界

专项补查多查询扩展（Multi-query Expansion）与结果融合（Result Fusion）的联合实现、改写保真度（Rewrite Fidelity）、精确 Token 保留、反事实评估（Counterfactual Evaluation）和失败回退（Failure Fallback）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 多查询与融合（Multi-query and Fusion） | `site:arxiv.org RAG-Fusion multiple queries reciprocal rank fusion` | arXiv 原始论文（Original Paper） |
| Q-202 | 实现（Implementation） | `site:docs.llamaindex.ai query fusion retriever multi query` | LlamaIndex 官方文档（Official Documentation） |
| Q-203 | 实现（Implementation） | `site:python.langchain.com MultiQueryRetriever source` | LangChain 官方参考（Official Reference） |
| Q-204 | 保真与回退（Fidelity and Fallback） | `site:learn.microsoft.com semantic query rewrite exact identifier fallback original query` | Azure AI Search 官方文档（Official Documentation） |
| Q-205 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG Query Rewrite Multi Query 改写 面经` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `rag-fusion-2024` | 原始论文（Original Paper） | `included` | 补多查询生成（Multi-query Generation）与倒数排名融合（Reciprocal Rank Fusion，RRF）的联合流程、偏题与延迟实验 |
| `azure-semantic-query-rewrite-2026` | 官方文档（Official Documentation） | `included_existing` | 既有来源已经覆盖精确标识符风险、超时和原查询回退，不重复登记 |
| `cohere-parallel-query-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 既有来源覆盖复合问题拆分与并行执行，不重复登记 |
| `llamaindex-query-fusion-docs` | 官方文档（Official Documentation） | `lead_only` | 搜索结果指向旧版或非稳定文档路径，暂不作为当前接口证据 |
| `langchain-multi-query-reference` | 官方参考（Official Reference） | `lead_only` | 当前搜索命中统一参考入口，缺少稳定版本页；待固定包版本后登记 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `QRW-K-201` | `knowledge` | 多查询扩展（Multi-query Expansion）和结果融合（Result Fusion）是耦合策略：生成数量、重复度和相关性会改变同一文档在 RRF 中的累计排名贡献 | `rag-fusion-2024` | `new` |
| `QRW-P-201` | `problem_question` | 多个语义近似改写重复命中同一错误主题时，融合分数可能放大偏题而不是提供独立证据 | `rag-fusion-2024` | `new` |
| `QRW-P-202` | `problem_question` | 只比较“开启改写”和“关闭改写”的最终答案，无法区分改写保真、分支召回、融合和生成阶段的贡献 | `rag-fusion-2024`; 既有评估来源 | `new` |
| `QRW-E-201` | `evaluation` | 改写评估（Rewrite Evaluation）需同时记录精确 Token / 条件保留率、分支 Recall、候选重合与多样性、融合后 NDCG、延迟和端到端答案质量 | `rag-fusion-2024`; 既有 RRF 与评估来源 | `new` |
| `QRW-S-201` | `solution` | 原查询作为固定 Control Branch，与改写分支并行；按保真校验、预算和检索增益 Gate，失败时退回原查询结果 | `azure-semantic-query-rewrite-2026`; `rag-fusion-2024` | `extends` |

## 5. 公开面试题来源核验

未发现独立于 `RAG-SCENE-015` 的新单节点公开题目类型。现有题目已覆盖 Multi-Query、HyDE、子问题分解、语义漂移和成本；本轮把其答案证据补成“生成—检索—融合—评估”完整链路。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 词项扩展、Multi-Query、HyDE、Decomposition、Step-back、Conversational Rewrite 与 Fusion 已覆盖 |
| 实现（Implementation） | `covered` | Azure、Cohere 和 RAG-Fusion 流程已登记；框架包版本仍待固定 |
| 工程问题（Engineering Problem） | `covered` | 精确 Token 丢失、语义漂移、重复放大、延迟和降级已登记 |
| 解决方案（Solution） | `covered` | Control Branch、Token 保护、Gate、Fusion 与 Fallback 已登记 |
| 评估（Evaluation） | `covered` | 已拆分保真、分支召回、融合、延迟与端到端结果 |
| 公开面试题（Public Interview Question） | `covered` | 公开题库问题可回链，未虚构新题 |
| 时效（Freshness） | `covered` | 论文版本及 2026 Preview / GA 边界已保留 |
| 安全或治理（Security or Governance） | `partial` | 改写器 Prompt Injection、敏感实体扩展和外部模型数据边界仍需专项来源 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接理解、路由、检索、融合、重排、评估和生产预算 |

## 7. 冲突、版本与未验证假设

- RAG-Fusion 的人工评估和单一企业产品语料不能证明该方法对所有任务优于单查询检索（Single-query Retrieval）。
- 改写数量提高既可能增加覆盖，也可能增加重复、偏题、延迟和生成上下文；必须与融合和候选预算联合调优。
- Azure Semantic Query Rewrite 的产品稳定性和精确 Token 行为属于易变能力；正式正文必须使用登记的审核日期。
- 框架级 MultiQueryRetriever / QueryFusionRetriever 需在后续固定具体包版本与源代码提交后再作为实现证据。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 2 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

固定 LangChain / LlamaIndex 当前包版本和实现提交；建立含产品号、错误码、日期、地域、权限和多轮指代的改写保真度（Rewrite Fidelity）数据集，并加入反事实分支消融（Counterfactual Branch Ablation）与安全测试。

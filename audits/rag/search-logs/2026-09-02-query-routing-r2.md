---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-ROUTING
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 查询路由（Query Routing）第二轮独立补漏

## 1. 本轮目标与边界

专项补查路由置信度校准（Routing Confidence Calibration）、查询—语料兼容性（Query–Corpus Compatibility）、成本敏感路由（Cost-sensitive Routing）、下游失败传播（Downstream Failure Propagation）和多路扇出（Fan-out）的权限边界。路由器（Router）决定执行链路，不把意图识别（Intent Detection）、检索器（Retriever）或生成器（Generator）的能力混算为路由能力。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 自适应路由（Adaptive Routing） | `RAGRouter-Bench adaptive RAG routing query corpus compatibility` | arXiv 原始论文（Original Paper） |
| Q-202 | 成本路由（Cost-aware Routing） | `cost effective LLM routing reasoning knowledge official paper` | ACL Anthology 原始论文（Original Paper） |
| Q-203 | 知识源路由（Knowledge-source Routing） | `site:docs.aws.amazon.com Bedrock Knowledge Bases routing data source` | AWS 官方文档（Official Documentation） |
| Q-204 | 本地知识源（Local Knowledge Source） | `site:learn.microsoft.com Foundry Local knowledge source routing` | Microsoft 官方文档（Official Documentation） |
| Q-205 | 公开题目（Public Question） | `site:nowcoder.com RAG 查询路由 多路检索 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `ragrouter-bench-2026` | 原始论文（Original Paper） | `included` | 补齐查询和语料双侧特征、范式选择及效果—成本联合评估 |
| `adaptive-rag-2024` | 原始论文（Original Paper） | `included_existing` | 已覆盖按问题复杂度选择无检索、单步或迭代检索（Iterative Retrieval） |
| `azure-agentic-retrieval-overview-2026` | 官方文档（Official Documentation） | `included_existing` | 已覆盖知识源选择、并行查询和当前接口边界 |
| `x-router-2026` | 原始论文（Original Paper） | `lead_only` | 主要解决大语言模型路由（LLM Routing），不能直接替代检索增强生成路由（RAG Routing）证据 |
| AWS / Microsoft Local 页面 | 官方文档（Official Documentation） | `not_added_duplicate` | 未形成独立于既有知识源路由来源的新类型，避免重复登记 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `ROUTE-K-201` | `knowledge` | 最优检索增强生成范式（RAG Paradigm）不仅取决于查询复杂度，还取决于语料的语义和结构属性及二者兼容性 | `ragrouter-bench-2026` | `new` |
| `ROUTE-P-201` | `problem_question` | 只用查询分类准确率（Query Classification Accuracy）评估路由，会掩盖同一标签下不同语料、成本和最终答案质量的差异 | `ragrouter-bench-2026` | `new` |
| `ROUTE-P-202` | `problem_question` | 低置信多路扇出（Low-confidence Fan-out）能减少漏路由，但会扩大延迟、费用、噪声和越权检索面 | 既有官方路由与权限来源 | `new` |
| `ROUTE-E-201` | `evaluation` | 路由评估应记录查询—语料组合、最终任务成功、资源消耗、拒识、回退、错误类型和权限违规，而非只报宏平均准确率 | `ragrouter-bench-2026`; 既有评估来源 | `new` |
| `ROUTE-S-201` | `solution` | 将路由策略实现为带预算和权限约束的策略层（Policy Layer）：候选链路先做授权裁剪，再按校准置信度执行单路、多路或回退 | 既有路由与安全来源 | `extends` |

## 5. 公开面试题来源核验

未发现独立于 `RAG-SCENE-014` 和 `RAG-SCENE-016` 的新路由题型。搜索命中的公开题库仍围绕意图路由（Intent Routing）、无需检索（No Retrieval）、单次检索（Single Retrieval）、多次检索（Multiple Retrieval）和工具调用（Tool Calling）；本轮新增的是这些题目的查询—语料与成本评估维度。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 查询复杂度、查询—语料兼容性和多目标路由已覆盖 |
| 实现（Implementation） | `covered` | Azure、Cohere、LlamaIndex 和 Elasticsearch 已有实现入口 |
| 工程问题（Engineering Problem） | `covered` | 误路由、广播成本、描述漂移、权限扩大和失败传播已登记 |
| 解决方案（Solution） | `covered` | 置信度、预算、授权裁剪、回退和降级状态机均有位置 |
| 评估（Evaluation） | `covered` | 增加查询—语料分层和效果—效率联合指标 |
| 公开面试题（Public Interview Question） | `covered` | 第一人称帖子与公开题库均可回链，未虚构新题 |
| 时效（Freshness） | `covered` | 2024 基础论文、2026 基准和当前官方实现均已登记 |
| 安全或治理（Security or Governance） | `partial` | 外部工具的数据驻留、提示注入（Prompt Injection）和凭据代理仍需生产治理轮次补证 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接理解、改写、检索、权限、评估和智能体检索增强生成（Agentic RAG） |

## 7. 冲突、版本与未验证假设

- `ragrouter-bench-2026` 是研究基准（Research Benchmark），不能证明其路由器直接适用于企业私域流量；正式章节需保留数据集和模型边界。
- “复杂问题用更复杂检索增强生成范式（RAG Paradigm）”不是单调规律；更复杂方法可能增加成本而没有质量收益。
- 语义阈值（Semantic Threshold）只有在目标流量上完成校准后才可解释，不能把余弦相似度（Cosine Similarity）直接当概率。
- 路由缓存（Routing Cache）必须把身份、权限、知识源版本和策略版本纳入缓存键或禁用跨安全域复用。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 2 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立带误路由成本矩阵（Misrouting Cost Matrix）、权限约束和故障注入（Fault Injection）的回放集；专项核查外部工具路由（External Tool Routing）的身份传播、数据出域与回退状态机。

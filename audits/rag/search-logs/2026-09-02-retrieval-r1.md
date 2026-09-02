---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RETRIEVAL
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：检索（Retrieval）第一轮

## 1. 本轮目标与边界

核查稠密检索（Dense Retrieval）、稀疏检索（Sparse Retrieval）、BM25、学习型稀疏检索（Learned Sparse Retrieval）、后期交互（Late Interaction）和混合检索（Hybrid Search）的原理、实现、失败模式和评估。本节点负责产生候选集，不把融合或重排收益算作召回器自身能力。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 稀疏检索（Sparse Retrieval） | `Robertson Zaragoza probabilistic relevance framework BM25 2009 PDF original` | BM25 综述论文 |
| Q-002 | 稠密检索（Dense Retrieval） | `site:arxiv.org dense passage retrieval original paper` | DPR 原始论文 |
| Q-003 | 新方法（New Method） | `site:arxiv.org SPLADE sparse lexical expansion model information retrieval` | SPLADE 原始论文 |
| Q-004 | 新方法（New Method） | `site:arxiv.org ColBERT late interaction passage search` | ColBERT 原始论文 |
| Q-005 | 实现（Implementation） | `site:learn.microsoft.com azure ai search hybrid search official 2026` | Azure 官方文档 |
| Q-006 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG 混合检索 BM25 面试` | 牛客公开页面 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `bm25-foundations-2009` | 原始论文（Original Paper） | `included` | 用于 BM25 公式和参数，不用博客简化公式替代 |
| `dense-passage-retrieval-2020` | 原始论文（Original Paper） | `included` | 用于 Dual-encoder Dense Retrieval 与训练方法 |
| `splade-2021` | 原始论文（Original Paper） | `included` | 用于可进入倒排索引的学习型稀疏表示 |
| `colbert-2020` | 原始论文（Original Paper） | `included` | 用于 Token-level Late Interaction 及质量成本权衡 |
| `azure-hybrid-search-overview-2026` | 官方文档（Official Documentation） | `included` | 当前全文、向量、过滤和 Semantic Ranker 链路 |
| `nowcoder-rag-retrieval-evolution-2026` | 工程实践（Engineering Practice） | `included` | 项目演进和失败场景线索；指标不推广 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `RET-K-001` | `knowledge` | Dense、Sparse 和 Late Interaction 的匹配粒度、索引结构和成本不同 | `new` |
| `RET-K-002` | `knowledge` | Hybrid Search 的价值来自词法精确匹配与语义泛化互补，不保证无条件提升 | `extends` |
| `RET-P-001` | `problem_question` | 产品号、人名和错误码可能在纯 Dense Retrieval 中被语义近邻淹没 | `new` |
| `RET-P-002` | `problem_question` | 口语同义表达可能在纯 BM25 中因词项不重叠而零召回 | `new` |
| `RET-P-003` | `problem_question` | 过滤、权限和 Top-K 顺序可能让相关文档在融合前已经丢失 | `extends` |
| `RET-C-001` | `conflict` | “Hybrid Search 必然优于单路”与数据集、过滤和候选预算依赖冲突 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-017` | 精确词项和语义需求并存时怎样设计多路召回 | 公开题库（Public Question Bank） | 牛客 Q5 | 否 | BM25、DPR、SPLADE、ColBERT 论文与 Azure 官方文档 |
| `RAG-SCENE-019` | Reranker 前的候选集怎样决定效果上限 | 工程实践（Engineering Practice） | 公开项目复盘 | 否 | Sentence Transformers 官方文档与检索论文 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | BM25、DPR、SPLADE、ColBERT 和 Hybrid Search 已覆盖 |
| 实现（Implementation） | `covered` | Azure、Elasticsearch、FAISS/数据库入口已有登记 |
| 工程问题（Engineering Problem） | `covered` | 零召回、噪声、词法语义错配、过滤和权限已登记 |
| 解决方案（Solution） | `partial` | 多跳、迭代、时间衰减和动态 Top-K 待补 |
| 评估（Evaluation） | `covered` | Recall、Precision、MRR、NDCG 和 Exact Ground Truth 已有来源 |
| 公开面试题（Public Interview Question） | `covered` | 公开题库和项目场景有入口 |
| 时效（Freshness） | `covered` | 经典论文与 2026 官方 Hybrid API 兼顾 |
| 安全或治理（Security or Governance） | `partial` | 权限裁剪、可信源白名单和攻击检索待补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接索引、改写、融合、重排和评估 |

## 7. 冲突、版本与未验证假设

- 不接受“Dense 替代 Sparse”或“Hybrid 一定更好”的无条件结论；
- 过滤必须区分 Pre-filter、Post-filter 和 Strict Post-filter，不能只写“支持 Metadata”；
- ColBERT 是多向量 Late Interaction 路线，不能简化为普通 Single-vector Embedding；
- 下一轮需补 Multi-hop Retrieval、Iterative Retrieval、Freshness Signal 和 Permission-aware Retrieval。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 一手资料缺口检查是否完成 | 否 |
| 公开面试题专项搜索是否完成 | 第一轮完成 |
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补多跳、迭代、时间/新鲜度、权限感知和动态候选集检索；建立按 Query 类型分层的 Dense/Sparse/Hybrid 对照表。

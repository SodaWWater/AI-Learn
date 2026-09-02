---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-STORAGE-INDEXING
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：存储与索引（Storage and Indexing）第一轮

## 1. 本轮目标与边界

核查向量数据库（Vector Database）的系统职责、精确最近邻（Exact Nearest Neighbor）与近似最近邻（Approximate Nearest Neighbor，ANN）、HNSW、IVF、量化、元数据过滤和索引维护。明确向量数据库（Vector Database）是系统能力集合，而 HNSW 只是其中一种索引能力。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 原理（Principle） | `site:arxiv.org HNSW approximate nearest neighbor original paper` | HNSW 原始论文 |
| Q-002 | 实现（Implementation） | `site:github.com/pgvector/pgvector README HNSW IVFFlat iterative scans filtering official` | pgvector 官方仓库固定提交 |
| Q-003 | 实现（Implementation） | `site:qdrant.tech documentation filtering HNSW payload index multitenancy official` | Qdrant 官方文档 |
| Q-004 | 实现（Implementation） | `site:milvus.io/docs hnsw M efConstruction ef official` | Milvus 3.0.x 官方文档 |
| Q-005 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG 向量数据库 HNSW 索引 面试` | 牛客公开页面 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `hnsw-paper-2018` | 原始论文（Original Paper） | `included` | 用于分层小世界图原理，不把论文实验直接当作当前数据库默认性能 |
| `pgvector-official-repository-2026` | 官方仓库（Official Repository） | `included` | 固定提交，覆盖 HNSW、IVFFlat、过滤和 Iterative Scan |
| `qdrant-indexing-docs-2026` | 官方文档（Official Documentation） | `included` | 用于 Vector Index 和 Payload Index 的职责分离及 Query Planning |
| `milvus-hnsw-docs-2026` | 官方文档（Official Documentation） | `included` | 用于 M、efConstruction 和 ef 参数的工程权衡 |
| `faiss-official-repository-2026` | 官方仓库（Official Repository） | `included` | 固定提交，作为 Exact、IVF、PQ、HNSW 实现与实验工具入口 |
| `nowcoder-agent-rag-question-bank-2026` | 公开题库（Public Question Bank） | `included` | 提取选型和部署问题，经验答案不直接采信 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `IDX-K-001` | `knowledge` | 向量数据库（Vector Database）除 ANN 外还承担 Schema、元数据、过滤、持久化、更新、分片和运维 | `extends` |
| `IDX-K-002` | `knowledge` | Vector Index 加速向量搜索，Payload Index 加速过滤并辅助过滤基数估计 | `new` |
| `IDX-P-001` | `problem_question` | 后过滤（Post-filtering）可能让 Top-K 候选被过滤后不足，造成召回下降 | `new` |
| `IDX-P-002` | `problem_question` | HNSW 参数提高召回时会同时增加内存、构建时间或查询延迟 | `extends` |
| `IDX-P-003` | `problem_question` | 删除、更新和 Embedding 模型升级会引出墓碑、压缩、双索引和一致性问题 | `extends` |
| `IDX-C-001` | `conflict` | “有向量索引即可高效过滤”与官方 Payload Index / Iterative Scan 设计冲突 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-009` | 文档更新删除时怎样维护索引一致性 | 公开题库（Public Question Bank） | 固定 GitHub 题库 Naive RAG Q8 | 否 | pgvector、Qdrant 和数据库官方文档 |
| `RAG-SCENE-013` | 规模、过滤、更新和模型升级下怎样选择与迁移索引 | 公开题库（Public Question Bank） | 牛客 Q10 部署挑战 | 否 | HNSW 原始论文及 pgvector、Qdrant、Milvus、FAISS 官方资料 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Exact、ANN、HNSW 及数据库职责边界已覆盖 |
| 实现（Implementation） | `covered` | PostgreSQL 扩展、专用向量库和 FAISS 三类实现入口已登记 |
| 工程问题（Engineering Problem） | `covered` | 过滤、内存、索引构建、更新删除、迁移已登记 |
| 解决方案（Solution） | `partial` | IVF/PQ 深入参数、分片热点和多租户隔离需下一轮补 |
| 评估（Evaluation） | `partial` | 已有 Recall—Latency 权衡；统一硬件、数据规模和过滤选择率基准待补 |
| 公开面试题（Public Interview Question） | `covered` | 更新删除及生产选型问题有公开来源 |
| 时效（Freshness） | `covered` | 官方仓库固定到 2026-08/09 提交，产品文档按 2026-09-02 审核 |
| 安全或治理（Security or Governance） | `partial` | 多租户隔离、权限过滤和备份恢复需单独来源 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接 Embedding、检索、数据治理和生产运维 |

## 7. 冲突、版本与未验证假设

- 不把向量数据库（Vector Database）与 HNSW 或 FAISS 画等号；
- HNSW 原始论文解释算法，数据库中的参数默认值、磁盘布局和过滤策略必须使用当前官方实现；
- pgvector 与专用向量数据库在事务、过滤、分布式能力和运维边界上不同，不能仅按“支持 HNSW”比较；
- 下一轮需按过滤选择率区分前过滤（Pre-filtering）、后过滤（Post-filtering）和过滤感知搜索（Filter-aware Search）；
- 需要补多租户、分片、副本、压缩和恢复点目标（Recovery Point Objective，RPO）证据。

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

补充 IVF、PQ、DiskANN、过滤选择率、多租户、分片副本、Compaction 和备份恢复的一手资料；建立同一数据集上的 Exact Ground Truth 与 ANN Recall 基准方法。

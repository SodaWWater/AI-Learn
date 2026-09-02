---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-STORAGE-INDEXING
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 存储与索引（Storage and Indexing）第二轮独立补漏

## 1. 本轮目标与边界

专项补查倒排文件索引（Inverted File Index，IVF）、乘积量化（Product Quantization，PQ）、磁盘近似最近邻检索（Disk-based Approximate Nearest Neighbor Search，DiskANN）、过滤选择率（Filter Selectivity）、多租户（Multitenancy）、副本一致性（Replica Consistency）、压缩整理（Compaction）和备份恢复（Backup and Restore）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 算法（Algorithm） | `DiskANN fast accurate billion point nearest neighbor NeurIPS 2019` | NeurIPS 原始论文（Original Paper） |
| Q-202 | 实现（Implementation） | `site:faiss.ai IndexIVFPQ nlist nprobe product quantizer` | FAISS 官方文档（Official Documentation） |
| Q-203 | 多租户（Multitenancy） | `site:qdrant.tech multitenancy tenant index collection payload` | Qdrant 官方文档（Official Documentation） |
| Q-204 | 一致性（Consistency） | `site:qdrant.tech consistency guarantees replication write ordering read consistency` | Qdrant 官方文档（Official Documentation） |
| Q-205 | 运维（Operations） | `site:milvus.io compaction backup restore clustering key segment pruning` | Milvus 官方文档（Official Documentation） |
| Q-206 | 公开题目（Public Question） | `site:nowcoder.com/discuss 企业级 RAG 多租户 增量更新 P99 面试` | 牛客第一人称帖子（First-person Post） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `diskann-paper-2019` | 原始论文（Original Paper） | `included` | 补磁盘索引（Disk-backed Index）和 Vamana 的算法、硬件与实验边界 |
| `faiss-official-repository-2026` | 官方仓库（Official Repository） | `included_existing` | 既有固定提交已覆盖 IVF、PQ 和 Exact 基准，不为同一实现重复登记来源 |
| `qdrant-multitenancy-docs-2026` | 官方文档（Official Documentation） | `included` | 补共享 Collection、Tenant Payload 和 Tenant Index 的边界 |
| `qdrant-consistency-docs-2026` | 官方文档（Official Documentation） | `included` | 补副本（Replica）、写入顺序（Write Ordering）与读取一致性（Read Consistency） |
| `milvus-clustering-compaction-docs-2026` | 官方文档（Official Documentation） | `included` | 补 Segment 重分布、PartitionStats、Segment Pruning 和过滤选择率实验 |
| `milvus-backup-docs-2026` | 官方文档（Official Documentation） | `included` | 补备份恢复命令与恢复验证入口 |
| `nowcoder-enterprise-rag-system-interview-2026` | 第一人称面经（First-person Interview Report） | `included` | 只登记多租户、增量索引、P99 和质量目标的问题条件；文章指标不作事实依据 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `IDX-K-201` | `knowledge` | HNSW、IVF-PQ 与 DiskANN 的资源假设不同：内存图、聚类倒排与压缩码、固态硬盘（Solid-state Drive，SSD）图索引不能只按算法名横向比较 | `diskann-paper-2019`; `faiss-official-repository-2026` | `new` |
| `IDX-K-202` | `knowledge` | 多租户（Multitenancy）至少包含 Collection 隔离、Shard / Partition 隔离和共享 Collection + Tenant Payload 三类路线，隔离强度与运维成本不同 | `qdrant-multitenancy-docs-2026`; `milvus-clustering-compaction-docs-2026` | `new` |
| `IDX-K-203` | `knowledge` | 副本一致性（Replica Consistency）、压缩整理（Compaction）和备份恢复（Backup and Restore）解决的是不同故障面，不能互相替代 | `qdrant-consistency-docs-2026`; `milvus-clustering-compaction-docs-2026`; `milvus-backup-docs-2026` | `new` |
| `IDX-P-201` | `problem_question` | 过滤选择率（Filter Selectivity）变化会改变需要扫描的 Segment、Posting List 或 Graph 路径，统一 Top-K 与单一延迟基准会掩盖租户长尾 | `milvus-clustering-compaction-docs-2026`; `qdrant-multitenancy-docs-2026` | `new` |
| `IDX-P-202` | `problem_question` | 热租户集中到少数 Shard 或 Segment 时，平均查询每秒（Queries Per Second，QPS）正常但 P99 延迟和副本积压恶化 | `qdrant-multitenancy-docs-2026`; `qdrant-consistency-docs-2026` | `new` |
| `IDX-P-203` | `problem_question` | 已成功写入主副本不等于所有读取一致；写入顺序、读取一致性和故障转移配置不匹配会短暂返回旧向量 | `qdrant-consistency-docs-2026` | `new` |
| `IDX-P-204` | `problem_question` | 有副本（Replica）但没有独立备份、恢复演练和恢复点目标（Recovery Point Objective，RPO）时，误删与逻辑损坏仍会复制到全部副本 | `milvus-backup-docs-2026`; `qdrant-consistency-docs-2026` | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-022` | 多企业租户、增量更新、检索质量和 P99 约束下设计企业级 RAG 系统 | 第一人称面经（First-person Interview Report） | 牛客第三轮系统设计题及三项追问 | 发布者自述，可称“帖子记录出现”，不可称企业官方题 | DiskANN 论文、FAISS / Qdrant / Milvus 官方资料及自有基准 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Exact、HNSW、IVF-PQ、DiskANN 的主要资源路线已覆盖 |
| 实现（Implementation） | `covered` | FAISS、Qdrant、Milvus 和 pgvector 的互补实现入口已登记 |
| 工程问题（Engineering Problem） | `covered` | 过滤、热点、一致性、压缩、备份与迁移已登记 |
| 解决方案（Solution） | `covered` | Tenant Index、Clustering Key、Compaction、Consistency 与 Backup 路线已有官方来源 |
| 评估（Evaluation） | `partial` | 需要统一数据、硬件、过滤选择率和更新率的 Exact Ground Truth 对照脚本 |
| 公开面试题（Public Interview Question） | `covered` | 新增企业级系统设计第一人称记录 |
| 时效（Freshness） | `covered` | 经典算法论文与 2026 产品文档分别标记 |
| 安全或治理（Security or Governance） | `covered` | 租户隔离、权限过滤、备份恢复和一致性已有入口 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接 Embedding、Retrieval、Data Governance、Evaluation 和 Production Governance |

## 7. 冲突、版本与未验证假设

- DiskANN 论文的十亿规模结果绑定论文硬件、数据集和指标定义，不能当作当前云服务的服务级别目标（Service Level Objective，SLO）。
- “每租户一个 Collection 隔离最强”不等于在大量小租户下运维最优；共享 Collection 也不等于自动满足授权隔离。
- Clustering Compaction 的官方实验只证明其给定数据、过滤和硬件条件，不构成通用倍数承诺。
- Exact Ground Truth、过滤选择率分桶、更新混合负载和灾难恢复演练仍需在仓库中建立可复现实验。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 3 |
| 本轮新增问题类型数 | 4 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立 Exact Ground Truth 与 ANN Recall 基准协议，覆盖过滤选择率、热租户、混合读写、故障转移、备份恢复和成本；补不同数据库的分片再平衡（Shard Rebalancing）与在线重建边界。

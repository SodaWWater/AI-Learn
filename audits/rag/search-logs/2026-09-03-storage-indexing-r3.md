---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-STORAGE-INDEXING
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 存储与索引（Storage and Indexing）第三轮独立补漏

## 1. 本轮目标与边界

本轮专查 Exact k-nearest Neighbor Search（精确 K 近邻搜索）对照、Approximate Nearest Neighbor Recall（近似最近邻召回率）、现代 Embedding Dataset（嵌入数据集）、Out-of-distribution Query（分布外查询）、硬件可复现性、Online Reconfiguration（在线重配置）和 Rollback（回滚）。算法排行榜只作为实验框架，不能替代业务负载验收。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 正确性（Correctness） | `site:qdrant.tech measuring ANN recall exact search recall@k CI hnsw_ef` | Qdrant 官方文档（Official Documentation） |
| Q-302 | 基准（Benchmark） | `VIBE vector index benchmark embeddings in-distribution out-of-distribution hardware 2026` | VIBE 官方仓库（Official Repository）与论文入口 |
| Q-303 | 在线迁移（Online Migration） | `site:qdrant.tech blue green cluster deployment reshard quantization snapshot rollback` | Qdrant 官方文档（Official Documentation） |
| Q-304 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG 向量数据库 索引 召回率 P99 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `qdrant-ann-recall-docs-2026` | 官方文档（Official Documentation） | `included` | 给出 Approximate Search（近似搜索）与 Exact Search（精确搜索）对照、Recall@K（K 位召回率）和 CI Regression（持续集成回归）入口 |
| `vibe-vector-index-benchmark-2026` | 官方仓库（Official Repository） | `included` | 固定当前 Commit（提交）、算法版本、硬件、精度类型和 In-distribution / Out-of-distribution（分布内/分布外）数据 |
| `qdrant-blue-green-deployment-2026` | 官方文档（Official Documentation） | `included` | 给出流式迁移、Snapshot Restore（快照恢复）、索引完成检查、端点切换和回滚边界 |
| `ann-benchmarks` | 社区仓库（Community Repository） | `excluded_superseded` | 项目声明不再积极维护；只保留为历史线索，不作为当前选型基准 |
| `big-ann-benchmarks` | 竞赛仓库（Benchmark Repository） | `lead_only` | VIBE 指向其 Billion-scale ANN（十亿规模近似最近邻）和 Constrained ANN（受约束近似最近邻）负载；待固定任务版本后再登记 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `IDX-K-301` | `knowledge` | ANN Recall（近似最近邻召回率）只回答 Approximate Index（近似索引）与 Exact kNN（精确 K 近邻）的结果重合度；它不等于 Retrieval Relevance（检索相关性）、Pipeline Quality（流水线质量）或 Business Impact（业务影响） | `qdrant-ann-recall-docs-2026` | `new` |
| `IDX-K-302` | `knowledge` | Search-time Parameter（查询时参数）和 Build-time Parameter（构建时参数）影响不同：例如提高 `hnsw_ef` 可交换延迟与召回，而 `m` 或 `ef_construct` 变化需要重建索引 | `qdrant-ann-recall-docs-2026` | `new` |
| `IDX-P-301` | `problem_question` | 用旧式随机向量、单一 In-distribution Query（分布内查询）或未固定硬件的排行榜选索引，无法预测现代文本 Embedding（嵌入）、量化精度和 Out-of-distribution Query（分布外查询）的表现 | `vibe-vector-index-benchmark-2026` | `new` |
| `IDX-P-302` | `problem_question` | 平均 ANN Recall（近似最近邻召回率）正常，但高选择性 Filter（过滤器）、热租户、混合读写或故障转移后的 P99 Latency（P99 延迟）和 Recall（召回率）回归被平均值掩盖 | `qdrant-ann-recall-docs-2026`; 既有多租户与一致性来源 | `extends` |
| `IDX-P-303` | `problem_question` | Online Resharding（在线重分片）或 Quantization Change（量化变更）完成数据复制后立即切流，没有确认点数、索引状态、质量、版本行为和回滚点 | `qdrant-blue-green-deployment-2026` | `new` |
| `IDX-E-301` | `evaluation` | 索引基准必须固定 Dataset Revision（数据集修订）、Embedding Model（嵌入模型）、Distance Metric（距离度量）、Ground Truth（真实对照）、Algorithm Version（算法版本）、硬件、线程、并发、精度和查询分布 | `vibe-vector-index-benchmark-2026`; `qdrant-ann-recall-docs-2026` | `new` |
| `IDX-S-301` | `solution` | 建立分层 Workload Matrix（负载矩阵）：无过滤、不同 Filter Selectivity（过滤选择率）、不同租户规模、读写混合、索引构建、故障转移和恢复；每层同时报告 Recall、P50/P95/P99、吞吐、内存、磁盘和成本 | 本轮来源与既有数据库来源 | `extends` |

## 5. 公开面试题来源核验

本轮命中内容仍属于 `RAG-SCENE-013`、`RAG-SCENE-017`、`RAG-SCENE-018` 和 `RAG-SCENE-022` 的索引选型、Hybrid Retrieval（混合检索）、P99 Latency（P99 延迟）与多租户系统设计。没有发现独立问题条件，因此公开题目计数不变。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Exact、HNSW、IVF-PQ、DiskANN 与 ANN Recall（近似最近邻召回率）层级已覆盖 |
| 实现（Implementation） | `covered` | Exact Mode（精确模式）、CI Gate（持续集成闸门）和 Blue-green Deployment（蓝绿部署）已有入口 |
| 工程问题（Engineering Problem） | `covered` | 过滤、热点、混合负载、重配置、备份和回滚已登记 |
| 解决方案（Solution） | `covered` | 分层基准、流式迁移、Snapshot（快照）和旧集群保留已登记 |
| 评估（Evaluation） | `covered` | Ground Truth（真实对照）、硬件、版本和分布契约已补 |
| 公开面试题（Public Interview Question） | `covered` | 现有公开题可回链，未复制重复题 |
| 时效（Freshness） | `covered` | VIBE 固定当前 Commit（提交），产品教程按审核日期登记 |
| 安全或治理（Security or Governance） | `covered` | 租户隔离、权限过滤、快照与恢复已有来源 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接 Embedding（嵌入）、Retrieval（检索）、Evaluation（评估）和 Production Governance（生产治理） |

## 7. 冲突、版本与未验证假设

- Qdrant 页面给出的示例 Query Sample Size（查询样本量）不是通用统计保证；正式阈值必须按目标置信区间、分层数量和最小可检测差异确定。
- VIBE 的公开结果绑定其数据、算法版本和硬件；不覆盖当前项目的 Metadata Filter（元数据过滤）、热租户、网络、托管服务和读写混合成本。
- 高 ANN Recall（近似最近邻召回率）只说明索引逼近 Exact kNN（精确 K 近邻）；若 Embedding（嵌入）本身错误，相关性仍可能很差。
- Blue-green Deployment（蓝绿部署）的回滚在旧集群仍可用或 Snapshot（快照）可恢复时才成立；切换后的新写入如何回灌仍需业务级协议。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立仓库内可执行 Benchmark Protocol（基准协议），补 Filtered ANN（过滤近似最近邻）、Mixed Read/Write（混合读写）、Failover（故障转移）和 Cutover Write Reconciliation（切换写入对账）；固定 Big-ANN Benchmark（大规模近似最近邻基准）的具体任务版本后再决定是否纳入。

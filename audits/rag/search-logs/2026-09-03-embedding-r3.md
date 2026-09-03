---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-EMBEDDING
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 向量嵌入（Embedding）第三轮独立补漏

## 1. 本轮目标与边界

本轮专查生产级 Embedding Model Migration（嵌入模型迁移）、Dual Write（双写）、Traffic Cutover（流量切换）、Rollback（回滚）、Incremental Re-embedding（增量重嵌入）和第三方 Embedding API（嵌入应用程序编程接口）的 Data Residency（数据驻留）与 Logging（日志记录）边界。产品教程只证明相应产品的当前实现，不推导为所有 Vector Database（向量数据库）的统一保证。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 模型迁移（Model Migration） | `site:qdrant.tech embedding model migration dual write named vectors zero downtime delete partial update` | Qdrant 官方文档（Official Documentation） |
| Q-302 | 增量更新（Incremental Update） | `site:qdrant.tech incremental embedding updates deterministic id content hash delete moved content` | Qdrant 官方文档（Official Documentation） |
| Q-303 | 数据治理（Data Governance） | `site:learn.microsoft.com Foundry embeddings data privacy processing geography content logging` | Microsoft 官方文档（Official Documentation） |
| Q-304 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG embedding 模型升级 双索引 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `qdrant-embedding-model-migration-2026` | 官方文档（Official Documentation） | `included` | 给出 Blue-green Collection（蓝绿集合）和 Named Vector（命名向量）两条零停机迁移路线，并明确 Delete（删除）和 Partial Update（部分更新）边界 |
| `qdrant-incremental-embedding-updates-2026` | 官方文档（Official Documentation） | `included` | 给出 Deterministic Point ID（确定性点标识符）、Content Fingerprint（内容指纹）、五类同步状态和全量扫描成本边界 |
| `azure-foundry-data-privacy-2026` | 官方文档（Official Documentation） | `included` | 明确 Embedding（嵌入）输入、区域处理、Stateful Feature（有状态功能）存储和 Abuse Monitoring（滥用监控）边界 |
| `qdrant-blue-green-deployment-2026` | 官方文档（Official Documentation） | `included_cross_stage` | 用于集群级 Traffic Cutover（流量切换）与 Rollback（回滚），不与模型级迁移重复计数 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `EMB-K-301` | `knowledge` | Embedding Model Migration（嵌入模型迁移）至少有“两套 Collection（集合）”和“同一 Collection（集合）内多 Named Vector（命名向量）”两种物理布局；资源占用、删除安全性和回滚方式不同 | `qdrant-embedding-model-migration-2026` | `new` |
| `EMB-K-302` | `knowledge` | Vector（向量）是 Raw Data（原始数据）的派生表示；稳定地址标识回答“位置是否相同”，Content Fingerprint（内容指纹）回答“内容是否相同”，两者不能互相替代 | `qdrant-incremental-embedding-updates-2026` | `new` |
| `EMB-P-301` | `problem_question` | 迁移期间只对 Upsert（插入或更新）做 Dual Write（双写），却允许 Delete（删除）、Payload Update（载荷更新）或 Vector Update（向量更新）单边发生，会使旧索引与新索引静默分叉 | `qdrant-embedding-model-migration-2026` | `new` |
| `EMB-P-302` | `problem_question` | 只保存 Vector（向量）而没有可重建的原始文本、Parser Version（解析器版本）和 Chunker Version（切分器版本）时，模型升级无法证明新旧表示来自同一内容 | `qdrant-embedding-model-migration-2026`; `qdrant-incremental-embedding-updates-2026` | `new` |
| `EMB-P-303` | `problem_question` | 选择第三方 Embedding API（嵌入应用程序编程接口）时只核对“不会训练模型”，但没有区分 Processing Location（处理位置）、At-rest Storage（静态存储）、Stateful Feature（有状态功能）和 Abuse-monitoring Log（滥用监控日志） | `azure-foundry-data-privacy-2026`; `azure-foundry-deployment-types-2026` | `new` |
| `EMB-S-301` | `solution` | 发布清单同时固定 Model Revision（模型修订）、Tokenizer（分词器）、Prompt（提示词）、Pooling（池化）、Normalization（归一化）、Dimension（维度）、Precision（精度）、Chunk Version（切分版本）、Cache Namespace（缓存命名空间）和 Index Alias（索引别名） | 本轮来源与既有模型卡（Model Card） | `extends` |
| `EMB-S-302` | `solution` | Cutover Gate（切换闸门）至少核对点数、派生版本、迁移失败队列、分层 Recall（召回率）、Latency（延迟）、删除一致性和回滚可用性；旧索引在观察窗结束前保持可读 | `qdrant-embedding-model-migration-2026`; `qdrant-blue-green-deployment-2026` | `new` |

## 5. 公开面试题来源核验

公开搜索命中仍落入 `RAG-SCENE-012`、`RAG-SCENE-013` 和 `RAG-SCENE-022`：Embedding Model Selection（嵌入模型选型）、Embedding Model Upgrade（嵌入模型升级）、Index Rebuild（索引重建）和企业级无停机迁移。没有发现带独立问题条件且可追溯的新类型，因此不复制题目。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 派生表示、模型契约（Model Contract）和迁移布局已覆盖 |
| 实现（Implementation） | `covered` | Blue-green Collection（蓝绿集合）、Named Vector（命名向量）、Content Fingerprint（内容指纹）和同步状态已有实现入口 |
| 工程问题（Engineering Problem） | `covered` | 单边写、删除回放、源数据缺失、缓存污染和数据治理已登记 |
| 解决方案（Solution） | `covered` | Dual Write（双写）、Background Re-embedding（后台重嵌入）、Cutover Gate（切换闸门）和 Rollback（回滚）已登记 |
| 评估（Evaluation） | `covered` | 质量、延迟、删除一致性和版本一致性联合验收 |
| 公开面试题（Public Interview Question） | `covered` | 既有公开问题已覆盖，未虚构新增题 |
| 时效（Freshness） | `covered` | 产品行为按 2026-09-03 审核日期登记 |
| 安全或治理（Security or Governance） | `covered` | Embedding API（嵌入应用程序编程接口）的处理、存储和日志边界已补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接摄取、切分、存储、评估与生产治理 |

## 7. 冲突、版本与未验证假设

- Named Vector（命名向量）路线在该教程中要求相应产品版本和原始 Collection（集合）配置；不能假设其他数据库存在相同操作。
- Blue-green Collection（蓝绿集合）的示例只天然覆盖 Upsert（插入或更新）；Delete（删除）和 Partial Update（部分更新）需要暂停、事件日志或额外冲突消解。
- Incremental Re-embedding（增量重嵌入）示例依赖 Deterministic Chunking（确定性切分）且每轮枚举全部源内容；大规模或高频更新应改用变更流、桶级摘要或分区清单。
- Azure 文档说明的是该服务与部署类型；每个供应商、区域、Preview Feature（预览功能）和合同仍需独立核验。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立可执行的 Embedding Release Manifest（嵌入发布清单）和 Dual-index Fault Injection（双索引故障注入）测试；分别模拟新模型超时、单边写失败、删除迟到、缓存污染和切换后回滚。

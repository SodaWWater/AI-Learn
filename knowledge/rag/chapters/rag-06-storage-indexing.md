---
id: RAG-06
title: 存储与索引（Storage and Indexing）
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: active
chapter_path: knowledge/rag/chapters/rag-06-storage-indexing.md
atoms: [RAG-06-001, RAG-06-002, RAG-06-003, RAG-06-004, RAG-06-005, RAG-06-006, RAG-06-007, RAG-06-008, RAG-06-009, RAG-06-010, RAG-06-011, RAG-06-012, RAG-06-013, RAG-06-014, RAG-06-015]
related_problem_ids: [PQ-RAG-0004, PQ-RAG-0012, PQ-RAG-0017, PQ-RAG-0022]
---

# 存储与索引（Storage and Indexing）

> 本章为 `formal_bounded`（范围受限正式），覆盖图谱中 15 个原子，不将具体产品默认成普适结论。

## 一、知识点概要

向量数据库（Vector Database）负责向量、元数据和近似最近邻检索（Approximate Nearest Neighbor，ANN），与事务数据库的精确过滤和连接职责不同（`RAG-06-001`）。精确检索与 ANN 是召回质量和性能的基本取舍（`RAG-06-002`）。Schema 应同时保存向量、原文定位、元数据和稳定主键（`RAG-06-003`、`RAG-06-004`）。

HNSW（Hierarchical Navigable Small World，`RAG-06-005`）、IVF（Inverted File Index，`RAG-06-006`）和 PQ（Product Quantization，`RAG-06-007`）分别以图、聚类分桶和压缩降低搜索代价。倒排/稀疏/全文索引（`RAG-06-008`）与向量索引共存形成混合检索基础（`RAG-06-009`）。元数据过滤的执行位置影响召回和延迟（`RAG-06-010`）。FAISS、Milvus、Qdrant、Chroma、Pinecone 和 pgvector 选型应基于数据规模、QPS、延迟、召回率和成本（`RAG-06-011`、`RAG-06-012`）。分区、分片、副本和冷热策略（`RAG-06-013`）、增删改与 Compaction（`RAG-06-014`）、构建加载预热持久化（`RAG-06-015`）决定生产可用性。

## 二、技术原理

给定查询向量 `q` 和集合 `V`，精确检索遍历全部向量；ANN 只访问候选子集，以可控召回损失换取低延迟。HNSW 用多层小世界图逐层导航，`M` 影响连接度和内存，`efConstruction` 影响建图质量，`efSearch` 影响查询召回与延迟。IVF 先以 `nlist` 聚类，再访问 `nprobe` 个桶；桶数和探测数决定扫描范围。PQ 将向量子空间量化为码字，降低内存但引入距离误差。

倒排索引按词项组织文档，稀疏向量以非零维保存权重；它对编号、专名和精确词形敏感。向量索引与关键词索引可并行召回，再由结果融合（Result Fusion）合并。过滤可以在 ANN 前、ANN 中或召回后执行：前置过滤节省无权数据访问但可能造成候选不足，后置过滤实现简单但可能返回空集，必须按引擎能力和租户隔离要求验证。

主键关系应满足 `document_id → parent_id → chunk_id → vector_id`，并携带模型、索引和文档版本。更新通常是追加新版本、标记旧版本删除，再由 Compaction 回收空间。构建、加载、预热和持久化是不同状态：未加载索引不能接受流量，未预热可能出现首请求长尾，未持久化则故障后无法快速恢复。

## 三、实际开发中的位置和使用方式

索引服务接收 RAG-05 的 `EmbeddingRecord`，写入：

```text
VectorPoint { id, vector, text_ref, document_id, parent_id, chunk_id,
              tenant_id, acl, document_version, model_version,
              index_version, valid_time, deleted }
```

先依据规模和隔离要求选择单机库、分布式库或关系库扩展；再固定距离度量、索引参数和过滤策略。生产查询记录候选数、过滤前后数量、索引版本、分片、副本和 P99 延迟。模型或 Chunking 变化生成新索引版本，使用别名或原子切换，避免同一查询混用不兼容向量。

基准至少包含数据规模梯度、并发梯度、ANN 参数网格和真实过滤分布，联合观察 Recall@K、MRR、P99、内存、构建时间、写入吞吐和成本。增删改测试要检查版本一致性、删除传播、Compaction 后可见性和恢复时间。

## 四、具体技术或框架实现

- FAISS 提供 Flat、HNSW、IVF、PQ 等索引，适合本地基线和离线实验；生产持久化、权限和多租户需由外围服务补齐。
- Milvus、Qdrant、Pinecone、Chroma 与 pgvector 的部署、过滤、分片和持久化能力不同；使用前按登记版本核对 API 与限制。
- HNSW 调优先固定 `M`、`efConstruction`，再用 `efSearch` 换取查询召回；IVF 调优联合 `nlist` 与 `nprobe`，PQ 调优记录码本和量化误差。
- 关键词索引可由 Elasticsearch 或数据库全文能力提供，向量和关键词通道统一 `document_id/chunk_id`，再交给 RRF（Reciprocal Rank Fusion，倒数排名融合）或加权融合。
- 增量写入用幂等键，删除使用 tombstone（删除标记）并定期 Compaction；模型迁移采用双集合、回归、灰度、别名切换和回滚。

### 完整性检查：对比、关系、错误与评估

Flat、HNSW、IVF 和 PQ 按召回、内存、构建时间、过滤能力与更新成本比较；数据沿 `document → chunk → embedding → index → retrieval` 关系链流转。常见错误包括维度不匹配、过滤顺序错误、删除未传播、分片不均和索引未预热；以分层 Recall@K、P99 延迟、吞吐、内存、恢复时间和成本评估发布。

## 相关工程问题/面试题

- [`PQ-RAG-0004`](../../../interview/rag/stages/storage-indexing.md#pq-rag-0004)
- [`PQ-RAG-0012`](../../../interview/rag/stages/storage-indexing.md#pq-rag-0012)
- [`PQ-RAG-0017`](../../../interview/rag/stages/storage-indexing.md#pq-rag-0017)
- [`PQ-RAG-0022`](../../../interview/rag/stages/storage-indexing.md#pq-rag-0022)

## 图谱与来源边界

覆盖 `RAG-06-001` 至 `RAG-06-015`（15/15），图谱原子均已完成来源映射，章节审核状态为 `formal_bounded`。来源包括 FAISS、HNSW、DiskANN、Milvus、Qdrant、pgvector、Azure、BM25/SPLADE 和登记的基准资料。产品的复制、过滤、Compaction、成本和性能属于版本相关行为；本章未新增来源、节点或关系，所有选型结论仍需用业务数据复核。

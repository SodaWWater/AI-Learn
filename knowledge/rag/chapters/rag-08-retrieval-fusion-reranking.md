---
id: RAG-08
title: 检索（Retrieval）、融合（Fusion）与重排（Reranking）
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: active
chapter_path: knowledge/rag/chapters/rag-08-retrieval-fusion-reranking.md
atoms: [RAG-08-001, RAG-08-002, RAG-08-003, RAG-08-004, RAG-08-005, RAG-08-006, RAG-08-007, RAG-08-008, RAG-08-009, RAG-08-010, RAG-08-011, RAG-08-012, RAG-08-013, RAG-08-014, RAG-08-015, RAG-08-016]
related_problem_ids: [PQ-RAG-0002, PQ-RAG-0004, PQ-RAG-0005, PQ-RAG-0015, PQ-RAG-0016, PQ-RAG-0017, PQ-RAG-0018, PQ-RAG-0022]
---

# 检索（Retrieval）、融合（Fusion）与重排（Reranking）

> 本章是 `formal_bounded`（范围受限正式），只使用图谱已有原子和登记来源。

## 一、知识点概要

稠密检索（Dense Retrieval，`RAG-08-001`）用向量相似度捕获语义近似；稀疏检索（Sparse Retrieval，`RAG-08-002`）和 BM25（Best Matching 25，`RAG-08-003`）擅长精确词项、编号和专名。混合检索（Hybrid Search，`RAG-08-004`）把多路召回（`RAG-08-005`）合并，RRF（Reciprocal Rank Fusion，`RAG-08-006`）按名次融合，加权分数融合需先归一化（`RAG-08-007`）。Top-K、相似度阈值和动态候选集（`RAG-08-008`）控制召回与成本。

双编码器（Bi-encoder）负责大规模初召回，交叉编码器（Cross-encoder）负责精排（`RAG-08-009`、`RAG-08-010`）。MMR（Maximal Marginal Relevance，最大边际相关性）和去重提高结果多样性（`RAG-08-011`）；时间衰减、新鲜度和热度可作为业务信号（`RAG-08-012`）。多跳和迭代检索（`RAG-08-013`）依赖前序证据；过滤可信来源（`RAG-08-014`）和零召回恢复（`RAG-08-015`）是可靠性边界。并发、缓存和批处理决定在线延迟（`RAG-08-016`）。

## 二、技术原理

稠密检索计算查询向量与文档向量的相似度；稀疏检索按词项权重匹配。BM25 结合词频、逆文档频率和文档长度归一化，`k1` 与 `b` 影响词频饱和和长度惩罚，但对同义改写和跨语言表达不敏感。混合检索通过并行通道覆盖两类需求，不能直接比较未经校准的分数。

RRF 对每个结果在各通道中的名次计算 `1/(k+rank)` 并求和，避免分数尺度差异；加权融合需对各通道分数做可解释归一化。候选数过小会漏召回，过大增加重排和上下文成本；阈值应在业务验证集上校准，动态策略可按查询难度或置信度调整。

Bi-encoder 将查询和文档独立编码，适合 ANN 大规模搜索；Cross-encoder 联合输入查询和文档，精度通常更高但计算昂贵。Reranker 可批处理候选并设置最低分数。MMR 在相关性和新颖性之间折中，时间信号应有明确时钟、衰减函数和业务优先级。多跳检索通过实体、关系或前一轮答案生成下一查询，必须设置步数、去环和证据门槛。

过滤应在召回前、中或后执行，并保证租户、ACL、来源可信度和有效期；零召回或低相关时可回退关键词、放宽非安全过滤、触发查询改写或拒答，但不能绕过权限。检索服务通过并行通道、连接池、批量重排、结果缓存和超时取消控制 P99。

## 三、实际开发中的位置和使用方式

检索服务接收 `QueryPlan` 和索引版本，输出候选证据：

```text
Candidate { chunk_id, document_id, channel, raw_score, rank,
            filter_status, source_trust, valid_time }
Evidence { chunk_id, fused_score, rerank_score, dedupe_key,
           citation_locator, trace_id }
```

先并行执行稠密、稀疏或结构化通道，再做权限和有效期过滤、去重与融合；只有候选规模允许时才调用 Cross-encoder。记录每通道召回数、融合排名、重排耗时、过滤丢弃数和最终证据。多跳请求使用有界状态机，保存每轮查询和证据链。

评估按通道和阶段拆分：Recall@K、Hit Rate、MRR、nDCG、重排增益、可信来源命中、零召回率、P50/P99 延迟、QPS、缓存命中率和成本。对 `Top-K`、阈值、RRF 参数、MMR、时间权重和重排模型做消融，确保端到端收益可归因。

## 四、具体技术或框架实现

- FAISS/Qdrant/Milvus 等提供稠密 ANN；Elasticsearch 或数据库全文索引提供 BM25/稀疏通道。
- Azure Hybrid Search、Elasticsearch RRF、LlamaIndex Query Fusion 和 LangChain MultiQuery 可实现多通道融合；参数按登记版本核对。
- Sentence Transformers `CrossEncoder`、Cohere Rerank 等实现批量重排；候选上限和超时应由服务预算控制。
- MMR、去重和时间衰减在融合层实现，记录 `dedupe_key`、权重、时间戳和最终排序理由。
- 低相关恢复采用原查询回退、稀疏通道兜底、受控改写、扩大候选或拒答；不得因召回为空而跳过 ACL。
- 并行查询、批量重排、短 TTL（Time To Live，生存时间）缓存、请求取消和熔断降低延迟；缓存键必须包含租户、过滤条件、模型和索引版本。

### 完整性检查：对比、关系、错误与评估

稠密（Dense）、稀疏（Sparse）、混合（Hybrid）和多跳（Multi-hop）检索按语料、查询复杂度、权限和延迟预算组合；它们保持 `QueryPlan → candidates → fusion → rerank → evidence` 关系链。常见错误包括过滤顺序错误、分数未归一化、候选窗口过小、重复证据和重排超时；评估分别报告各通道 Recall@K、融合/重排增益、零召回率、可信来源命中率、P50/P99、QPS、缓存命中率和成本。

## 相关工程问题/面试题

- [`PQ-RAG-0002`](../../../interview/rag/stages/retrieval.md#pq-rag-0002)
- [`PQ-RAG-0004`](../../../interview/rag/stages/retrieval.md#pq-rag-0004)
- [`PQ-RAG-0005`](../../../interview/rag/stages/retrieval.md#pq-rag-0005)
- [`PQ-RAG-0015`](../../../interview/rag/stages/retrieval.md#pq-rag-0015)
- [`PQ-RAG-0016`](../../../interview/rag/stages/retrieval.md#pq-rag-0016)
- [`PQ-RAG-0017`](../../../interview/rag/stages/retrieval.md#pq-rag-0017)
- [`PQ-RAG-0018`](../../../interview/rag/stages/retrieval.md#pq-rag-0018)
- [`PQ-RAG-0022`](../../../interview/rag/stages/storage-indexing.md#pq-rag-0022)

## 图谱与来源边界

覆盖 `RAG-08-001` 至 `RAG-08-016`（16/16），图谱原子均已完成来源映射，章节审核状态为 `formal_bounded`。来源包括 DPR、BGE-M3、ColBERT、ColPali、BM25、SPLADE、RRF、MMR、RankGPT、Azure/Elasticsearch/Cohere/LangChain/LlamaIndex 文档及登记问题材料。产品 API、阈值、模型性能、缓存和成本随版本变化；本章未新增来源、节点或关系。

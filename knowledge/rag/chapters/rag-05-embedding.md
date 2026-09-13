---
id: RAG-05
title: 向量嵌入（Embedding）与表示学习
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: active
chapter_path: knowledge/rag/chapters/rag-05-embedding.md
atoms: [RAG-05-001, RAG-05-002, RAG-05-003, RAG-05-004, RAG-05-005, RAG-05-006, RAG-05-007, RAG-05-008, RAG-05-009, RAG-05-010, RAG-05-011, RAG-05-012, RAG-05-013, RAG-05-014, RAG-05-015, RAG-05-016]
related_problem_ids: [PQ-RAG-0004, PQ-RAG-0012, PQ-RAG-0022]
---

# 向量嵌入（Embedding）与表示学习

> 本章是 `formal_bounded`（范围受限正式），覆盖图谱原子，不将模型卡或问题库存扩展为未登记结论。

## 一、知识点概要

向量嵌入（Embedding）把查询（Query）、文本片段或多模态对象映射到向量空间，使相似性可以被计算并交给向量索引（`RAG-05-001`）。Word2Vec、BERT、SBERT 到现代检索嵌入体现了从词级共现、上下文表示到句段级对比学习的演进（`RAG-05-002`、`RAG-05-003`）。查询和文档可能使用非对称编码与任务前缀（`RAG-05-004`、`RAG-05-015`）。

模型选择需同时考虑通用、领域和多语言能力（`RAG-05-005`）、维度/精度/速度/存储（`RAG-05-006`）、距离度量与归一化（`RAG-05-007`、`RAG-05-008`）。Matryoshka 表示学习（Matryoshka Representation Learning）允许截断向量（`RAG-05-009`）；MTEB 等公开基准只能做初筛，最终要用业务数据（`RAG-05-010`）。批量推理和缓存（`RAG-05-011`）降低构建成本；模型升级必须重建或迁移向量（`RAG-05-012`）。领域微调、检索器与生成器偏好对齐（`RAG-05-013`、`RAG-05-014`）以及多模态嵌入（`RAG-05-016`）属于需额外数据和验证的扩展。

## 二、技术原理

给定编码器 `f`，文本 `x` 映射为 $v=f(x)\in R^d$。余弦相似度为 $v_q\cdot v_d/(||v_q||||v_d||)$；归一化后内积（Inner Product）与余弦排序等价。L2 距离强调几何半径，不能与余弦分数混用而不校准。双编码器（Bi-encoder）分别编码查询和文档、适合大规模召回；交叉编码器（Cross-encoder）联合编码、适合小候选精排。

对比学习使用正样本和硬负样本优化相似度间隔；负样本分布决定模型会区分哪些错误。非对称编码允许查询前缀和文档前缀不同，适合“短问题—长文档”检索。Matryoshka 训练让前缀维度保留主要语义，截断后仍需重新校准索引和阈值。多模态模型在共享空间对齐文本、图像或页面，跨模态质量依赖任务数据，不能从单模态基准推断。

向量维度越高通常存储和计算越大；量化和低精度可降成本但可能损失边界样本。模型、分词器、归一化方式和距离度量必须作为同一版本契约。领域适配可用对比微调、适配器或线性变换；只在业务标注足够且基线失败明确时启用。

## 三、实际开发中的位置和使用方式

Embedding 位于文本切分（Chunking）之后、向量数据库（Vector Database）写入之前，在线也对 Query 使用同一兼容模型。每个向量记录应携带：

```text
EmbeddingRecord { chunk_id, model_id, model_version, dimension,
                  dtype, normalized, metric, vector, created_at }
```

离线先固定业务查询集和目标证据，比较模型召回、MRR、nDCG、内存、吞吐、延迟与成本。批量任务采用有界并发、重试和内容哈希缓存；失败项可重放，不重复计费。升级时双写新旧集合，完成离线回归和影子流量后原子切换，保留旧向量用于回滚。

## 四、具体技术或框架实现

- Sentence Transformers 的 `encode`、`normalize_embeddings` 和 `util.semantic_search` 可构建基线；`CrossEncoder` 仅对候选精排。
- E5、BGE-M3、Cohere Embed 等模型的查询/文档前缀、维度、语言和最大长度按登记模型卡配置，不跨模型复用分数阈值。
- Matryoshka 或向量量化需在同一业务集比较完整维度与截断维度，重新建立索引并记录 `dimension` 与 `dtype`。
- 批量 Embedding 使用内容哈希缓存和幂等任务键；模型迁移采用新集合、回归、灰度和别名切换。
- 领域微调和偏好对齐只使用有来源的训练对，报告训练集、负样本、版本与离线收益；多模态检索保存模态类型和原始对象定位。

### 完整性检查：对比、关系、错误与评估

通用（General）、领域（Domain-specific）和多语言（Multilingual）模型应在同一业务集上比较；Embedding 与索引、距离度量和 Reranker 共同构成 `query → vector → candidate → evidence` 关系链。常见错误包括查询/文档前缀不一致、归一化与距离度量不匹配、模型升级后混用旧向量和缓存污染；验收同时报告 Recall@K、MRR、nDCG、吞吐、P95/P99 延迟、内存和单位查询成本。

## 相关工程问题/面试题

- [`PQ-RAG-0004`](../../../interview/rag/stages/embedding.md#pq-rag-0004)
- [`PQ-RAG-0012`](../../../interview/rag/stages/embedding.md#pq-rag-0012)
- [`PQ-RAG-0022`](../../../interview/rag/stages/embedding.md#pq-rag-0022)

## 图谱与来源边界

覆盖 `RAG-05-001` 至 `RAG-05-016`（16/16），图谱原子均已完成来源映射，章节审核状态为 `formal_bounded`。来源包括 E5、BGE-M3、DPR、SPLADE、ColBERT、ColPali、MTEB、Matryoshka、Sentence Transformers 和已登记模型文档。`RAG-05-013`、`RAG-05-014` 主要由用户资料映射，结论边界较窄；本章不把其扩展为已验证通用方法。模型版本、维度、阈值、成本和性能需按登记版本复核。

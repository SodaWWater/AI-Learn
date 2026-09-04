# 跨节点工程问题与系统设计问题库存（Cross-stage Problem and System Design Inventory）

> 状态：`candidate / WP-P6-001 / graph-backed / inventory-only`
>
> 本页只投影已有问题节点及 `problem_at`、`supported_by`、`solved_by`、`evaluated_by` 关系；不新增综合题、系统设计题、来源或正式答案。

## 生成审计（Generation Audit）

图谱版本：`2026-09-04`；跨节点问题：22；问题节点总数：26。

跨节点定义为同一问题通过 `problem_at` 映射到两个及以上流程节点。未达到该条件的问题保留在节点页面，不在此重复展开。

## 问题库存（Problem Inventory）

<a id="pq-rag-0002"></a>
### PQ-RAG-0002：法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子 文本片段（Chunk）、元数据（Metadata）、混合检索（Hybrid Retrieval）、重排（Rerank）、引用和质检？（RAG engineering problem RAG-SCENE-002）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 4 节：法律文本 Chunking |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG`: https://www.nowcoder.com/discuss/882634966025175040；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0003"></a>
### PQ-RAG-0003：面对给定文档量、文本片段（Chunk） 数和固定 词元（Token） 长度，如何验证切分参数自洽，并用数据而不是经验值证明选择？（RAG engineering problem RAG-SCENE-003）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 附录：500 份 PDF、5 万 Chunk 与 512 Token |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG`: https://www.nowcoder.com/discuss/882634966025175040；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 文本切分（Chunking） [`PS-CHUNKING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0004` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION`, `EVAL-RAG-RETRIEVAL` |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0004"></a>
### PQ-RAG-0004：补全 查询（Query）/Document 向量嵌入（Embedding）、批量建库、FAISS Top-K 检索、ID 映射、上下文生成和准确率记录的完整 向量检索增强生成（VectorRAG） 链路。（RAG engineering problem RAG-SCENE-004）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 1 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] |
| 图谱解决方案边（Solved By） | 未登记 |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0005"></a>
### PQ-RAG-0005：实现实体召回、多跳子图抽取、路径去重、语义剪枝、生产者消费者队列、提前停止，并分析路径爆炸和图算法选型。（RAG engineering problem RAG-SCENE-005）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 2 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 图谱解决方案边（Solved By） | 未登记 |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0007"></a>
### PQ-RAG-0007：如何按文档结构、模型长度和业务查询选择文本切分大小、重叠与高级切分方案，并用检索和端到端实验验证参数？（RAG engineering problem RAG-SCENE-007）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：文本切块策略、大小和重叠长度 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 文本切分（Chunking） [`PS-CHUNKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0008"></a>
### PQ-RAG-0008：生产 RAG 面对复杂文档解析、增量索引、多语言检索、延迟、模型升级、缓存、监控和敏感信息权限时，应如何分层定位与治理？（RAG engineering problem RAG-SCENE-008）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：实际部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 评估（Evaluation） [`PS-EVALUATION`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0009"></a>
### PQ-RAG-0009：向量索引中的文档发生新增、修改和删除时，如何在全量重建、软删除、版本化标识和延迟压缩之间选择，并保证在线一致性与回滚能力？（RAG engineering problem RAG-SCENE-009）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：document updates and deletions |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 来源定位与审核（Locator and Review） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026`: https://github.com/ImranMatin/rag-interview-questions；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0010"></a>
### PQ-RAG-0010：固定长度、滑动窗口、语义切分和分层切分分别怎样影响召回、精度、索引规模和上下文完整性，应该如何设计对照实验？（RAG engineering problem RAG-SCENE-010）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q6：chunking strategies and retrieval quality |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 来源定位与审核（Locator and Review） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026`: https://github.com/ImranMatin/rag-interview-questions；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 文本切分（Chunking） [`PS-CHUNKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0011"></a>
### PQ-RAG-0011：如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？（RAG engineering problem RAG-SCENE-011）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：mixed text, tables, and images in PDF |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 来源定位与审核（Locator and Review） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026`: https://github.com/ImranMatin/rag-interview-questions；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0012"></a>
### PQ-RAG-0012：面对中文、多语言、领域术语和短 查询（Query）—长 Document 的非对称检索，如何选择 向量嵌入（Embedding） 模型，并共同评估效果、维度、吞吐、存储、成本及模型升级重建风险？（RAG engineering problem RAG-SCENE-012）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q4：Embedding 模型选择与评估 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] |
| 图谱解决方案边（Solved By） | 未登记 |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0013"></a>
### PQ-RAG-0013：向量数据库在数据增长、高并发、元数据（Metadata） 过滤、删除更新和 向量嵌入（Embedding） 模型升级时，如何选择 Exact、HNSW 或 IVF，定位过滤后召回下降，并完成无停机索引迁移？（RAG engineering problem RAG-SCENE-013）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：向量数据库、检索延迟和模型升级等部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0014"></a>
### PQ-RAG-0014：线上存在复合意图、表达省略、地域歧义和新业务类型时，如何证明规则与模型的意图识别覆盖真实流量，并用影子对比、拒识和错误路由样本发现盲区？（RAG engineering problem RAG-SCENE-014）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | Q3：使用规则做意图路由时，如何证明规则能够覆盖线上流量 |
| 来源引用（Source References） | `SRC-NOWCODER-XUNLEI-AI-INTENT-ROUTING-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-XUNLEI-AI-INTENT-ROUTING-2026`: https://www.nowcoder.com/discuss/918809114392657920；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | 未登记 |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0015"></a>
### PQ-RAG-0015：长尾 查询（Query） 召回低时，如何在 Multi-查询（Query）、HyDE、子问题分解、会话改写和 Step-back Prompting 之间选择，并防止专有名词丢失、语义漂移、噪声放大及延迟失控？（RAG engineering problem RAG-SCENE-015）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q5：Query 改写、HyDE、Query Expansion 与 Multi-Query |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0016"></a>
### PQ-RAG-0016：一个请求什么时候无需检索、只需单次检索、需要多次检索或应路由到外部工具，如何设计置信度、成本预算、降级和错误路由评估？（RAG engineering problem RAG-SCENE-016）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q9：Adaptive RAG、Iterative RAG、Self-RAG、CRAG 与 Agentic RAG |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0017"></a>
### PQ-RAG-0017：产品编号和专业术语依赖精确匹配、口语问题又依赖语义检索时，如何设计 稠密检索（Dense Retrieval）、稀疏检索（Sparse Retrieval） 与 混合检索（Hybrid Search） 多路召回，并诊断零召回、噪声召回和权限过滤问题？（RAG engineering problem RAG-SCENE-017）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q5：向量、BM25、Hybrid Search、RRF 与 Rerank |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0018"></a>
### PQ-RAG-0018：BM25 与向量检索的原始分数尺度不可直接比较且会返回重复 文本片段（Chunk） 时，如何用 RRF 或分数归一化融合、去重，并验证某个通道没有被系统性淹没？（RAG engineering problem RAG-SCENE-018）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | BM25 + 向量召回、RRF 融合和去重候选链路 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026`: https://www.nowcoder.com/discuss/906597462301818880；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-RETRIEVAL` |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0019"></a>
### PQ-RAG-0019：重排（Rerank）er 不新增候选却增加明显延迟时，怎样选择进入重排的候选数、最终 Top-N、跳过重排条件和降级链路，并分别解释 召回率（Recall）、NDCG 与 MRR 的变化？（RAG engineering problem RAG-SCENE-019）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | RRF 候选集后接 Reranker 的场景闸门、Top-N 和评测结果 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026`: https://www.nowcoder.com/discuss/906597462301818880；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-RETRIEVAL` |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0020"></a>
### PQ-RAG-0020：相关证据已经召回但位于长上下文中间、被重复片段或冲突证据淹没时，如何分配 词元（Token） 预算、排序、去重、压缩并验证没有丢失关键依据？（RAG engineering problem RAG-SCENE-020）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q6：Lost in the Middle |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | 未登记 |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0022"></a>
### PQ-RAG-0022：为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？（RAG engineering problem RAG-SCENE-022）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第三轮系统设计题及多租户、增量更新、检索评估追问 |
| 来源引用（Source References） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026`: https://www.nowcoder.com/discuss/904058990026420224；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0023"></a>
### PQ-RAG-0023：当检索结果质量不足但生成器仍会强制作答时，如何识别 Retrieval Bias（检索偏置），区分零召回、低相关和证据不足，并在过滤、拒答、回退及迭代检索之间选择？（RAG engineering problem RAG-SCENE-023）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q4：如何解决 Retrieval Bias（检索偏置） |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025`: https://www.nowcoder.com/feed/main/detail/d15b819dd04c4fdda9c2cc82d8fadbbc；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0024"></a>
### PQ-RAG-0024：多个已召回文档在事实、时间或观点上互相冲突时，如何保留来源与时间 元数据（Metadata）（元数据），进行可信度排序和交叉验证，并在答案中显式呈现共识、分歧与不确定性？（RAG engineering problem RAG-SCENE-024）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：RAG 如何处理多文档冲突信息 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025`: https://www.nowcoder.com/feed/main/detail/d15b819dd04c4fdda9c2cc82d8fadbbc；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | 未登记 |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

<a id="pq-rag-0026"></a>
### PQ-RAG-0026：智能体检索增强生成（Agentic RAG）（智能体检索增强生成）中的工具怎样注册并描述参数、权限和作用范围，如何把请求用户身份与最小权限传播到每次工具调用，并防止工具描述投毒、跨服务越权和高风险调用绕过人工确认？（RAG engineering problem RAG-SCENE-026）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | Agent 架构与记忆追问 4 |
| 来源引用（Source References） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026`: https://www.nowcoder.com/feed/main/detail/76f5be8b8bd5420b94d32a66e26a7ad9；审核日期 2026-09-04 |
| 跨节点映射（Cross-stage Mapping） | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记 |

该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。

## 来源与限制（Sources and Limits）

- 所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)。
- 面经和公开题库只证明题目出处或工程场景，不升级为企业官方面试结论。
- 当前状态为 inventory-only；本页不替代正式问题答案或知识章节。

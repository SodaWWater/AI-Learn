# RAG 主干节点工程问题与公开面试题索引（RAG Stage Problem and Public Interview Question Index）

> 状态：`candidate / WP-P5-001 / graph-backed / inventory-only`
>
> 图谱输入：[`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)；生成器：[`scripts/generate_rag_stage_problem_index.py`](../../scripts/generate_rag_stage_problem_index.py)。

本索引只投影已有工程问题/面试题（Engineering Problem / Interview Question）节点和图谱关系，不生成答案、不新增题目，也不把公开题库或第一人称面经升级为企业官方面试结论。一个问题可以出现在多个流程节点（Pipeline Stage），这是图谱中的多对多映射。

## 生成审计（Generation Audit）

- 图谱版本：`2026-09-04`；节点：437；边：1930。
- 流程节点：18；问题节点：26；已映射问题：26。
- 未映射问题节点：0；未映射项必须在正式页面生产前处理。
- 来源定位、来源类型和技术证据边界沿用图谱字段；本索引不把题目来源当作技术结论证据。

## 18 节点索引（18-stage Index）

| 顺序 | 流程节点（Pipeline Stage） | 问题数 | 问题 ID |
|---:|---|---:|---|
| 1 | 数据摄取（Data Ingestion） [`PS-DATA-INGESTION`] | 0 | 无 |
| 2 | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 4 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0008`](#pq-rag-0008), [`PQ-RAG-0011`](#pq-rag-0011), [`PQ-RAG-0022`](#pq-rag-0022) |
| 3 | 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 4 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0008`](#pq-rag-0008), [`PQ-RAG-0011`](#pq-rag-0011), [`PQ-RAG-0022`](#pq-rag-0022) |
| 4 | 文本切分（Chunking） [`PS-CHUNKING`] | 6 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0003`](#pq-rag-0003), [`PQ-RAG-0007`](#pq-rag-0007), [`PQ-RAG-0010`](#pq-rag-0010), [`PQ-RAG-0011`](#pq-rag-0011), [`PQ-RAG-0022`](#pq-rag-0022) |
| 5 | 向量嵌入（Embedding） [`PS-EMBEDDING`] | 4 | [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0012`](#pq-rag-0012), [`PQ-RAG-0013`](#pq-rag-0013), [`PQ-RAG-0022`](#pq-rag-0022) |
| 6 | 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 7 | [`PQ-RAG-0003`](#pq-rag-0003), [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0008`](#pq-rag-0008), [`PQ-RAG-0009`](#pq-rag-0009), [`PQ-RAG-0012`](#pq-rag-0012), [`PQ-RAG-0013`](#pq-rag-0013), [`PQ-RAG-0022`](#pq-rag-0022) |
| 7 | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`] | 3 | [`PQ-RAG-0014`](#pq-rag-0014), [`PQ-RAG-0015`](#pq-rag-0015), [`PQ-RAG-0016`](#pq-rag-0016) |
| 8 | 查询改写（Query Rewrite） [`PS-QUERY-REWRITE`] | 0 | 无 |
| 9 | 查询路由（Query Routing） [`PS-QUERY-ROUTING`] | 0 | 无 |
| 10 | 检索（Retrieval） [`PS-RETRIEVAL`] | 10 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0005`](#pq-rag-0005), [`PQ-RAG-0015`](#pq-rag-0015), [`PQ-RAG-0016`](#pq-rag-0016), [`PQ-RAG-0017`](#pq-rag-0017), [`PQ-RAG-0018`](#pq-rag-0018), [`PQ-RAG-0019`](#pq-rag-0019), [`PQ-RAG-0023`](#pq-rag-0023), [`PQ-RAG-0024`](#pq-rag-0024) |
| 11 | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 10 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0005`](#pq-rag-0005), [`PQ-RAG-0015`](#pq-rag-0015), [`PQ-RAG-0016`](#pq-rag-0016), [`PQ-RAG-0017`](#pq-rag-0017), [`PQ-RAG-0018`](#pq-rag-0018), [`PQ-RAG-0019`](#pq-rag-0019), [`PQ-RAG-0023`](#pq-rag-0023), [`PQ-RAG-0024`](#pq-rag-0024) |
| 12 | 重排（Reranking） [`PS-RERANKING`] | 10 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0005`](#pq-rag-0005), [`PQ-RAG-0015`](#pq-rag-0015), [`PQ-RAG-0016`](#pq-rag-0016), [`PQ-RAG-0017`](#pq-rag-0017), [`PQ-RAG-0018`](#pq-rag-0018), [`PQ-RAG-0019`](#pq-rag-0019), [`PQ-RAG-0023`](#pq-rag-0023), [`PQ-RAG-0024`](#pq-rag-0024) |
| 13 | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 5 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0020`](#pq-rag-0020), [`PQ-RAG-0023`](#pq-rag-0023), [`PQ-RAG-0024`](#pq-rag-0024) |
| 14 | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 5 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0020`](#pq-rag-0020), [`PQ-RAG-0023`](#pq-rag-0023), [`PQ-RAG-0024`](#pq-rag-0024) |
| 15 | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 5 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0004`](#pq-rag-0004), [`PQ-RAG-0020`](#pq-rag-0020), [`PQ-RAG-0023`](#pq-rag-0023), [`PQ-RAG-0024`](#pq-rag-0024) |
| 16 | 评估（Evaluation） [`PS-EVALUATION`] | 14 | [`PQ-RAG-0001`](#pq-rag-0001), [`PQ-RAG-0003`](#pq-rag-0003), [`PQ-RAG-0006`](#pq-rag-0006), [`PQ-RAG-0007`](#pq-rag-0007), [`PQ-RAG-0008`](#pq-rag-0008), [`PQ-RAG-0010`](#pq-rag-0010), [`PQ-RAG-0014`](#pq-rag-0014), [`PQ-RAG-0018`](#pq-rag-0018), [`PQ-RAG-0019`](#pq-rag-0019), [`PQ-RAG-0020`](#pq-rag-0020), [`PQ-RAG-0021`](#pq-rag-0021), [`PQ-RAG-0023`](#pq-rag-0023), [`PQ-RAG-0024`](#pq-rag-0024), [`PQ-RAG-0025`](#pq-rag-0025) |
| 17 | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 7 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0005`](#pq-rag-0005), [`PQ-RAG-0008`](#pq-rag-0008), [`PQ-RAG-0009`](#pq-rag-0009), [`PQ-RAG-0013`](#pq-rag-0013), [`PQ-RAG-0022`](#pq-rag-0022), [`PQ-RAG-0026`](#pq-rag-0026) |
| 18 | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 4 | [`PQ-RAG-0005`](#pq-rag-0005), [`PQ-RAG-0011`](#pq-rag-0011), [`PQ-RAG-0016`](#pq-rag-0016), [`PQ-RAG-0026`](#pq-rag-0026) |

## 问题明细（Problem Details）

<a id="pq-rag-0001"></a>
### PQ-RAG-0001：已有 Recall@5 指标时，如何证明结果足够好，评测集规模和分布如何设计，怎样建立公平基线并区分检索错误与生成错误？（RAG engineering problem RAG-SCENE-001）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 2 节：Recall@5 与评测集；附录现场碎片 |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 关联流程节点（Pipeline Stages） | 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-10-001`, `RAG-10-002`, `RAG-10-003`, `RAG-10-004`, `RAG-10-009`, `RAG-10-011`, `RAG-10-013` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0002"></a>
### PQ-RAG-0002：法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子 Chunk、Metadata、Hybrid Retrieval、Rerank、引用和质检？（RAG engineering problem RAG-SCENE-002）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 4 节：法律文本 Chunking |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 关联流程节点（Pipeline Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 知识节点（Knowledge Nodes） | `RAG-03-003`, `RAG-03-004`, `RAG-03-014`, `RAG-04-004`, `RAG-04-007`, `RAG-04-014`, `RAG-08-004`, `RAG-08-010`, `RAG-09-007`, `RAG-11-005` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0003"></a>
### PQ-RAG-0003：面对给定文档量、Chunk 数和固定 Token 长度，如何验证切分参数自洽，并用数据而不是经验值证明选择？（RAG engineering problem RAG-SCENE-003）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 附录：500 份 PDF、5 万 Chunk 与 512 Token |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 关联流程节点（Pipeline Stages） | 文本切分（Chunking） [`PS-CHUNKING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-04-012`, `RAG-04-013`, `RAG-04-015`, `RAG-06-012`, `RAG-10-009` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0004"></a>
### PQ-RAG-0004：补全 Query/Document Embedding、批量建库、FAISS Top-K 检索、ID 映射、上下文生成和准确率记录的完整 VectorRAG 链路。（RAG engineering problem RAG-SCENE-004）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 1 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 关联流程节点（Pipeline Stages） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] |
| 知识节点（Knowledge Nodes） | `RAG-05-004`, `RAG-05-008`, `RAG-05-011`, `RAG-06-003`, `RAG-06-015`, `RAG-08-008`, `RAG-09-006`, `RAG-13-007` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0005"></a>
### PQ-RAG-0005：实现实体召回、多跳子图抽取、路径去重、语义剪枝、生产者消费者队列、提前停止，并分析路径爆炸和图算法选型。（RAG engineering problem RAG-SCENE-005）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 2 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 关联流程节点（Pipeline Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 知识节点（Knowledge Nodes） | `RAG-08-013`, `RAG-11-007`, `RAG-12-009`, `RAG-12-010`, `RAG-12-020`, `RAG-13-007` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0006"></a>
### PQ-RAG-0006：把 VectorRAG 和 GraphRAG 日志转换为评测数据，计算 Faithfulness、Context Precision 和 Context Recall，并输出可比较的明细结果。（RAG engineering problem RAG-SCENE-006）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 3 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 关联流程节点（Pipeline Stages） | 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-10-003`, `RAG-10-004`, `RAG-10-006`, `RAG-10-008`, `RAG-10-013`, `RAG-13-009` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0007"></a>
### PQ-RAG-0007：如何按文档结构、模型长度和业务查询选择文本切分大小、重叠与高级切分方案，并用检索和端到端实验验证参数？（RAG engineering problem RAG-SCENE-007）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：文本切块策略、大小和重叠长度 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 文本切分（Chunking） [`PS-CHUNKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-04-002`, `RAG-04-003`, `RAG-04-004`, `RAG-04-005`, `RAG-04-007`, `RAG-04-012`, `RAG-04-013`, `RAG-10-009` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0008"></a>
### PQ-RAG-0008：生产 RAG 面对复杂文档解析、增量索引、多语言检索、延迟、模型升级、缓存、监控和敏感信息权限时，应如何分层定位与治理？（RAG engineering problem RAG-SCENE-008）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：实际部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 评估（Evaluation） [`PS-EVALUATION`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 知识节点（Knowledge Nodes） | `RAG-02-008`, `RAG-03-003`, `RAG-03-012`, `RAG-06-014`, `RAG-10-001`, `RAG-11-002`, `RAG-11-013` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0009"></a>
### PQ-RAG-0009：向量索引中的文档发生新增、修改和删除时，如何在全量重建、软删除、版本化标识和延迟压缩之间选择，并保证在线一致性与回滚能力？（RAG engineering problem RAG-SCENE-009）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：document updates and deletions |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 关联流程节点（Pipeline Stages） | 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 知识节点（Knowledge Nodes） | `RAG-02-008`, `RAG-06-014`, `RAG-11-002`, `RAG-11-003`, `RAG-11-004` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0010"></a>
### PQ-RAG-0010：固定长度、滑动窗口、语义切分和分层切分分别怎样影响召回、精度、索引规模和上下文完整性，应该如何设计对照实验？（RAG engineering problem RAG-SCENE-010）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q6：chunking strategies and retrieval quality |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 关联流程节点（Pipeline Stages） | 文本切分（Chunking） [`PS-CHUNKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-04-002`, `RAG-04-005`, `RAG-04-007`, `RAG-04-012`, `RAG-04-013`, `RAG-10-009` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0011"></a>
### PQ-RAG-0011：如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？（RAG engineering problem RAG-SCENE-011）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：mixed text, tables, and images in PDF |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 关联流程节点（Pipeline Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 知识节点（Knowledge Nodes） | `RAG-03-003`, `RAG-03-004`, `RAG-03-006`, `RAG-03-014`, `RAG-04-011`, `RAG-12-011` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0012"></a>
### PQ-RAG-0012：面对中文、多语言、领域术语和短 Query—长 Document 的非对称检索，如何选择 Embedding 模型，并共同评估效果、维度、吞吐、存储、成本及模型升级重建风险？（RAG engineering problem RAG-SCENE-012）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q4：Embedding 模型选择与评估 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] |
| 知识节点（Knowledge Nodes） | `RAG-05-004`, `RAG-05-005`, `RAG-05-006`, `RAG-05-009`, `RAG-05-010`, `RAG-05-011`, `RAG-05-012`, `RAG-06-012` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0013"></a>
### PQ-RAG-0013：向量数据库在数据增长、高并发、Metadata 过滤、删除更新和 Embedding 模型升级时，如何选择 Exact、HNSW 或 IVF，定位过滤后召回下降，并完成无停机索引迁移？（RAG engineering problem RAG-SCENE-013）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：向量数据库、检索延迟和模型升级等部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 知识节点（Knowledge Nodes） | `RAG-05-012`, `RAG-06-001`, `RAG-06-002`, `RAG-06-005`, `RAG-06-006`, `RAG-06-010`, `RAG-06-012`, `RAG-06-014`, `RAG-11-004` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0014"></a>
### PQ-RAG-0014：线上存在复合意图、表达省略、地域歧义和新业务类型时，如何证明规则与模型的意图识别覆盖真实流量，并用影子对比、拒识和错误路由样本发现盲区？（RAG engineering problem RAG-SCENE-014）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | Q3：使用规则做意图路由时，如何证明规则能够覆盖线上流量 |
| 来源引用（Source References） | `SRC-NOWCODER-XUNLEI-AI-INTENT-ROUTING-2026` |
| 关联流程节点（Pipeline Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-07-001`, `RAG-07-002`, `RAG-07-008`, `RAG-07-010`, `RAG-07-011`, `RAG-07-012`, `RAG-10-009`, `RAG-10-011` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0015"></a>
### PQ-RAG-0015：长尾 Query 召回低时，如何在 Multi-Query、HyDE、子问题分解、会话改写和 Step-back Prompting 之间选择，并防止专有名词丢失、语义漂移、噪声放大及延迟失控？（RAG engineering problem RAG-SCENE-015）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q5：Query 改写、HyDE、Query Expansion 与 Multi-Query |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`] |
| 知识节点（Knowledge Nodes） | `RAG-07-003`, `RAG-07-004`, `RAG-07-005`, `RAG-07-006`, `RAG-07-007`, `RAG-07-009`, `RAG-07-011`, `RAG-07-012`, `RAG-08-011` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0016"></a>
### PQ-RAG-0016：一个请求什么时候无需检索、只需单次检索、需要多次检索或应路由到外部工具，如何设计置信度、成本预算、降级和错误路由评估？（RAG engineering problem RAG-SCENE-016）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q9：Adaptive RAG、Iterative RAG、Self-RAG、CRAG 与 Agentic RAG |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 知识节点（Knowledge Nodes） | `RAG-07-002`, `RAG-07-010`, `RAG-07-012`, `RAG-08-013`, `RAG-12-004`, `RAG-12-005`, `RAG-12-006`, `RAG-12-007` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0017"></a>
### PQ-RAG-0017：产品编号和专业术语依赖精确匹配、口语问题又依赖语义检索时，如何设计 Dense、Sparse 与 Hybrid Search 多路召回，并诊断零召回、噪声召回和权限过滤问题？（RAG engineering problem RAG-SCENE-017）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q5：向量、BM25、Hybrid Search、RRF 与 Rerank |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`] |
| 知识节点（Knowledge Nodes） | `RAG-08-001`, `RAG-08-002`, `RAG-08-003`, `RAG-08-004`, `RAG-08-005`, `RAG-08-008`, `RAG-08-014`, `RAG-08-015` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0018"></a>
### PQ-RAG-0018：BM25 与向量检索的原始分数尺度不可直接比较且会返回重复 Chunk 时，如何用 RRF 或分数归一化融合、去重，并验证某个通道没有被系统性淹没？（RAG engineering problem RAG-SCENE-018）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | BM25 + 向量召回、RRF 融合和去重候选链路 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 关联流程节点（Pipeline Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-08-004`, `RAG-08-005`, `RAG-08-006`, `RAG-08-007`, `RAG-08-008`, `RAG-08-011`, `RAG-10-009` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0019"></a>
### PQ-RAG-0019：Reranker 不新增候选却增加明显延迟时，怎样选择进入重排的候选数、最终 Top-N、跳过重排条件和降级链路，并分别解释 Recall、NDCG 与 MRR 的变化？（RAG engineering problem RAG-SCENE-019）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | RRF 候选集后接 Reranker 的场景闸门、Top-N 和评测结果 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 关联流程节点（Pipeline Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-08-008`, `RAG-08-009`, `RAG-08-010`, `RAG-08-011`, `RAG-08-016`, `RAG-10-002`, `RAG-10-003`, `RAG-10-004` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0020"></a>
### PQ-RAG-0020：相关证据已经召回但位于长上下文中间、被重复片段或冲突证据淹没时，如何分配 Token 预算、排序、去重、压缩并验证没有丢失关键依据？（RAG engineering problem RAG-SCENE-020）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q6：Lost in the Middle |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-09-002`, `RAG-09-003`, `RAG-09-004`, `RAG-09-005`, `RAG-09-011`, `RAG-09-013`, `RAG-10-014` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0021"></a>
### PQ-RAG-0021：一次回答失败时，如何区分解析、召回、排序、上下文、生成和引用错误，并联合设计 Golden Dataset、分层指标、LLM-as-a-Judge 校准、人工抽检及线上 A/B 实验？（RAG engineering problem RAG-SCENE-021）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：如何全面评估 RAG 系统 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点（Pipeline Stages） | 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-10-001`, `RAG-10-002`, `RAG-10-004`, `RAG-10-005`, `RAG-10-007`, `RAG-10-008`, `RAG-10-009`, `RAG-10-011`, `RAG-10-013`, `RAG-10-014` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0022"></a>
### PQ-RAG-0022：为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？（RAG engineering problem RAG-SCENE-022）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第三轮系统设计题及多租户、增量更新、检索评估追问 |
| 来源引用（Source References） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 关联流程节点（Pipeline Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 知识节点（Knowledge Nodes） | `RAG-03-003`, `RAG-04-007`, `RAG-05-012`, `RAG-06-010`, `RAG-06-012`, `RAG-06-013`, `RAG-06-014`, `RAG-11-002`, `RAG-11-004`, `RAG-11-008`, `RAG-11-012`, `RAG-11-013`, `RAG-11-019` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0023"></a>
### PQ-RAG-0023：当检索结果质量不足但生成器仍会强制作答时，如何识别 Retrieval Bias（检索偏置），区分零召回、低相关和证据不足，并在过滤、拒答、回退及迭代检索之间选择？（RAG engineering problem RAG-SCENE-023）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q4：如何解决 Retrieval Bias（检索偏置） |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 关联流程节点（Pipeline Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-08-008`, `RAG-08-013`, `RAG-08-015`, `RAG-09-006`, `RAG-09-008`, `RAG-09-009`, `RAG-10-014` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0024"></a>
### PQ-RAG-0024：多个已召回文档在事实、时间或观点上互相冲突时，如何保留来源与时间 Metadata（元数据），进行可信度排序和交叉验证，并在答案中显式呈现共识、分歧与不确定性？（RAG engineering problem RAG-SCENE-024）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：RAG 如何处理多文档冲突信息 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 关联流程节点（Pipeline Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-08-014`, `RAG-09-007`, `RAG-09-011`, `RAG-09-012`, `RAG-09-013`, `RAG-10-008`, `RAG-10-009` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0025"></a>
### PQ-RAG-0025：RAG 评测命中率接近 100% 时，如何排查样本过小、针对性调参、训练或提示泄漏、公开文档进入模型预训练数据等污染，并用私有未见数据、冻结快照和分层置信区间证明结果可信？（RAG engineering problem RAG-SCENE-025）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | RAG 评测追问 1—6 |
| 来源引用（Source References） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026` |
| 关联流程节点（Pipeline Stages） | 评估（Evaluation） [`PS-EVALUATION`] |
| 知识节点（Knowledge Nodes） | `RAG-10-001`, `RAG-10-002`, `RAG-10-003`, `RAG-10-004`, `RAG-10-011`, `RAG-10-012`, `RAG-10-014` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

<a id="pq-rag-0026"></a>
### PQ-RAG-0026：Agentic RAG（智能体检索增强生成）中的工具怎样注册并描述参数、权限和作用范围，如何把请求用户身份与最小权限传播到每次工具调用，并防止工具描述投毒、跨服务越权和高风险调用绕过人工确认？（RAG engineering problem RAG-SCENE-026）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | Agent 架构与记忆追问 4 |
| 来源引用（Source References） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026` |
| 关联流程节点（Pipeline Stages） | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 知识节点（Knowledge Nodes） | `RAG-11-012`, `RAG-11-013`, `RAG-11-015`, `RAG-11-016`, `RAG-11-017`, `RAG-12-004`, `RAG-12-018` |

该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。

## 生产边界（Production Boundary）

- `first_person_interview` 只证明发布者自述的面试经历；`public_question_bank` 和 `project_interview_exercise` 不证明企业真实面试。
- `engineering_case` 明确标记为工程问题（Engineering Case），不得补写为真实面试题。
- 技术结论必须回到已登记的官方文档（Official Documentation）、官方代码仓库（Official Repository）或原始论文（Original Paper）；本索引不替代证据核验。
- `RAG-07-001` 与 `RAG-13-011` 仍是无来源库存草稿（Inventory Draft），不能在正式页面中作为已核验结论。

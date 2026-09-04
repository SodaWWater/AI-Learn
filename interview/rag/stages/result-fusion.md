# 结果融合（Result Fusion）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`
>
> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

结果融合（Result Fusion）合并稠密、稀疏或多路检索结果，处理分数尺度、重复和通道偏置。当前图谱包含 16 个知识原子，并映射 10 道问题。题目来源只证明出处或工程场景，技术结论仍需回到已登记的一手证据。

## 通用诊断路径

1. 先固定查询、数据快照、过滤条件、候选数和模型版本，再区分召回缺失、融合偏置与重排误差。
2. 同时记录命中率、召回率、排序质量、延迟、吞吐、成本和权限过滤后的有效候选数。
3. 用离线基线、影子流量和失败样本验证通道贡献，不把单一数据集或固定参数当作普遍最优。
4. 图谱未登记的根因或评估关系保持为待验证缺口，不以推断替代证据。

## 问题明细

<a id="pq-rag-0002"></a>
### PQ-RAG-0002：法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子 文本片段（Chunk）、元数据（Metadata）、Hybrid Retrieval、Rerank、引用和质检？（RAG engineering problem RAG-SCENE-002）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 4 节：法律文本 Chunking |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG`: https://www.nowcoder.com/discuss/882634966025175040；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-004`, `RAG-08-010` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0004"></a>
### PQ-RAG-0004：补全 查询/文档向量嵌入（Query/Document Embedding）、批量建库、FAISS 前 K 个结果（Top-K Results） 检索、ID 映射、上下文生成和准确率记录的完整 向量检索增强生成（VectorRAG） 链路。（RAG engineering problem RAG-SCENE-004）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 1 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-008` |
| 本问题全部流程节点（All Mapped Stages） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0005"></a>
### PQ-RAG-0005：实现实体召回、多跳子图抽取、路径去重、语义剪枝、生产者消费者队列、提前停止，并分析路径爆炸和图算法选型。（RAG engineering problem RAG-SCENE-005）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 2 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-013` |
| 本问题全部流程节点（All Mapped Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0015"></a>
### PQ-RAG-0015：长尾查询（Long-tail Query） 召回低时，如何在 多查询扩展（Multi-Query Expansion）、假设文档嵌入（Hypothetical Document Embeddings，HyDE）、子问题分解、会话改写和 退步提示（Step-back Prompting） 之间选择，并防止专有名词丢失、语义漂移、噪声放大及延迟失控？（RAG engineering problem RAG-SCENE-015）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q5：Query 改写、HyDE、Query Expansion 与 Multi-Query |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-011` |
| 本问题全部流程节点（All Mapped Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0016"></a>
### PQ-RAG-0016：一个请求什么时候无需检索、只需单次检索、需要多次检索或应路由到外部工具，如何设计置信度、成本预算、降级和错误路由评估？（RAG engineering problem RAG-SCENE-016）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q9：Adaptive RAG、Iterative RAG、Self-RAG、CRAG 与 Agentic RAG |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-013` |
| 本问题全部流程节点（All Mapped Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0017"></a>
### PQ-RAG-0017：产品编号和专业术语依赖精确匹配、口语问题又依赖语义检索时，如何设计 稠密检索（Dense Retrieval）、稀疏检索（Sparse Retrieval） 与 混合检索（Hybrid Search） 多路召回，并诊断零召回、噪声召回和权限过滤问题？（RAG engineering problem RAG-SCENE-017）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q5：向量、BM25、Hybrid Search、RRF 与 Rerank |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-001`, `RAG-08-002`, `RAG-08-003`, `RAG-08-004`, `RAG-08-005`, `RAG-08-008`, `RAG-08-014`, `RAG-08-015` |
| 本问题全部流程节点（All Mapped Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0018"></a>
### PQ-RAG-0018：BM25 与向量检索的原始分数尺度不可直接比较且会返回重复 文本片段（Chunk） 时，如何用 RRF 或分数归一化融合、去重，并验证某个通道没有被系统性淹没？（RAG engineering problem RAG-SCENE-018）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | BM25 + 向量召回、RRF 融合和去重候选链路 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026`: https://www.nowcoder.com/discuss/906597462301818880；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-004`, `RAG-08-005`, `RAG-08-006`, `RAG-08-007`, `RAG-08-008`, `RAG-08-011` |
| 本问题全部流程节点（All Mapped Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-RETRIEVAL` |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0019"></a>
### PQ-RAG-0019：重排模型（Reranker） 不新增候选却增加明显延迟时，怎样选择进入重排的候选数、最终 Top-N、跳过重排条件和降级链路，并分别解释 召回率（Recall）、归一化折损累计增益（NDCG） 与 平均倒数排名（MRR） 的变化？（RAG engineering problem RAG-SCENE-019）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | RRF 候选集后接 Reranker 的场景闸门、Top-N 和评测结果 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026`: https://www.nowcoder.com/discuss/906597462301818880；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-008`, `RAG-08-009`, `RAG-08-010`, `RAG-08-011`, `RAG-08-016` |
| 本问题全部流程节点（All Mapped Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-RETRIEVAL` |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0023"></a>
### PQ-RAG-0023：当检索结果质量不足但生成器仍会强制作答时，如何识别 检索偏置（Retrieval Bias）（检索偏置），区分零召回、低相关和证据不足，并在过滤、拒答、回退及迭代检索之间选择？（RAG engineering problem RAG-SCENE-023）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q4：如何解决 Retrieval Bias（检索偏置） |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025`: https://www.nowcoder.com/feed/main/detail/d15b819dd04c4fdda9c2cc82d8fadbbc；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-008`, `RAG-08-013`, `RAG-08-015` |
| 本问题全部流程节点（All Mapped Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0024"></a>
### PQ-RAG-0024：多个已召回文档在事实、时间或观点上互相冲突时，如何保留来源与时间 元数据（Metadata）（元数据），进行可信度排序和交叉验证，并在答案中显式呈现共识、分歧与不确定性？（RAG engineering problem RAG-SCENE-024）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：RAG 如何处理多文档冲突信息 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025`: https://www.nowcoder.com/feed/main/detail/d15b819dd04c4fdda9c2cc82d8fadbbc；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-08-014` |
| 本问题全部流程节点（All Mapped Stages） | 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 第一人称面经（First-person Interview Report）、公开题库（Public Question Bank）和项目型考题（Project Interview Exercise）只证明题目出处或场景，不证明企业官方面试事实。
- 当前状态为 inventory-only；正式页面仍需按模板补充完整现象、根因分支、方案权衡、实现细节和验证证据。

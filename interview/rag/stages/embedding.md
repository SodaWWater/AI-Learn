# 向量嵌入（Embedding）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`
>
> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

向量嵌入（Embedding）向量表示和模型选择、批处理、维度、成本与迁移约束。当前图谱包含 16 个知识原子，并映射 4 道问题。题目来源只证明出处或工程场景，技术结论仍需回到已登记的一手证据。

## 通用诊断路径

1. 先固定文档快照、模型版本、数据模式和服务目标，再区分表示质量、索引质量与在线一致性问题。
2. 将向量维度、相似度度量、索引参数、过滤条件和版本标识作为同一条可追踪链路记录。
3. 用离线检索指标、资源成本、延迟和失败样本做对照实验，不把题目中的参数当作通用最佳值。
4. 图谱未登记的根因或评估关系保持为待验证缺口，不以推断替代证据。

## 问题明细

<a id="pq-rag-0004"></a>
### PQ-RAG-0004：补全 查询/文档向量嵌入（Query/Document Embedding）、批量建库、FAISS 前 K 个结果（Top-K Results） 检索、ID 映射、上下文生成和准确率记录的完整 VectorRAG 链路。（RAG engineering problem RAG-SCENE-004）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 1 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-05-004`, `RAG-05-008`, `RAG-05-011` |
| 本问题全部流程节点（All Mapped Stages） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`], 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`], 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] |
| 图谱解决方案边（Solved By） | `未登记（图谱无 solved_by 边）` |
| 图谱评估边（Evaluated By） | `未登记（图谱无 evaluated_by 边）` |

**工程现象与候选诊断点**：该题涉及的现象、约束和候选知识原子以 `problem_at` 映射为边界；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和相关知识原子展开，比较质量、延迟、吞吐、存储、成本、权限和迁移风险；本页不补写图谱之外的框架结论。

**验证与追问**：固定数据快照和版本，分别做召回/排序回归、资源压测、更新删除一致性和失败样本复查；缺少 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0012"></a>
### PQ-RAG-0012：面对中文、多语言、领域术语和短 Query—长 Document 的非对称检索，如何选择 向量嵌入模型（Embedding Model），并共同评估效果、维度、吞吐、存储、成本及模型升级重建风险？（RAG engineering problem RAG-SCENE-012）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q4：Embedding 模型选择与评估 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-05-004`, `RAG-05-005`, `RAG-05-006`, `RAG-05-009`, `RAG-05-010`, `RAG-05-011`, `RAG-05-012` |
| 本问题全部流程节点（All Mapped Stages） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] |
| 图谱解决方案边（Solved By） | `未登记（图谱无 solved_by 边）` |
| 图谱评估边（Evaluated By） | `未登记（图谱无 evaluated_by 边）` |

**工程现象与候选诊断点**：该题涉及的现象、约束和候选知识原子以 `problem_at` 映射为边界；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和相关知识原子展开，比较质量、延迟、吞吐、存储、成本、权限和迁移风险；本页不补写图谱之外的框架结论。

**验证与追问**：固定数据快照和版本，分别做召回/排序回归、资源压测、更新删除一致性和失败样本复查；缺少 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0013"></a>
### PQ-RAG-0013：向量数据库在数据增长、高并发、元数据（Metadata） 过滤、删除更新和 向量嵌入模型（Embedding Model）升级时，如何选择 精确最近邻（Exact）、分层可导航小世界图（HNSW）或倒排文件索引（IVF），定位过滤后召回下降，并完成无停机索引迁移？（RAG engineering problem RAG-SCENE-013）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：向量数据库、检索延迟和模型升级等部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-05-012` |
| 本问题全部流程节点（All Mapped Stages） | 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001` |
| 图谱评估边（Evaluated By） | `未登记（图谱无 evaluated_by 边）` |

**工程现象与候选诊断点**：该题涉及的现象、约束和候选知识原子以 `problem_at` 映射为边界；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和相关知识原子展开，比较质量、延迟、吞吐、存储、成本、权限和迁移风险；本页不补写图谱之外的框架结论。

**验证与追问**：固定数据快照和版本，分别做召回/排序回归、资源压测、更新删除一致性和失败样本复查；缺少 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0022"></a>
### PQ-RAG-0022：为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 尾延迟（P99 Tail Latency）目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？（RAG engineering problem RAG-SCENE-022）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第三轮系统设计题及多租户、增量更新、检索评估追问 |
| 来源引用（Source References） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026`: https://www.nowcoder.com/discuss/904058990026420224；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-05-012` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`], 向量嵌入（Embedding） [`PS-EMBEDDING`], 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`], 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | `未登记（图谱无 evaluated_by 边）` |

**工程现象与候选诊断点**：该题涉及的现象、约束和候选知识原子以 `problem_at` 映射为边界；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和相关知识原子展开，比较质量、延迟、吞吐、存储、成本、权限和迁移风险；本页不补写图谱之外的框架结论。

**验证与追问**：固定数据快照和版本，分别做召回/排序回归、资源压测、更新删除一致性和失败样本复查；缺少 `evaluated_by` 时保留为待验证项。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 第一人称面经（First-person Interview Report）、公开题库（Public Question Bank）和项目型考题（Project Interview Exercise）只证明题目出处或场景，不证明企业官方面试事实。
- 当前状态为 inventory-only；正式问题页面仍需按模板补充完整现象、根因分支、方案权衡、实现细节和验证证据。

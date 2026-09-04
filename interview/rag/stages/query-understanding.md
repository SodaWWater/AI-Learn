# 查询理解（Query Understanding）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`
>
> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

查询理解（Query Understanding）识别意图、实体、上下文、歧义和拒识条件。当前图谱包含 12 个知识原子，并映射 3 道问题。题目来源只证明出处或工程场景，技术结论仍需回到已登记的一手证据。

## 通用诊断路径

1. 先固定原始查询、上下文、模型版本、路由策略和服务目标，再区分理解错误、改写漂移与路由错误。
2. 记录拒识、歧义、长尾表达和新业务类型，使用影子流量与错误样本评估覆盖，而不是只看平均准确率。
3. 将质量收益与额外调用、延迟、成本、隐私和可回滚性一起比较。
4. 图谱未登记的根因或评估关系保持为待验证缺口，不以推断替代证据。

## 问题明细

<a id="pq-rag-0014"></a>
### PQ-RAG-0014：线上存在复合意图、表达省略、地域歧义和新业务类型时，如何证明规则与模型的意图识别覆盖真实流量，并用影子对比、拒识（Abstention）和错误路由（Misrouting）样本发现盲区？（RAG engineering problem RAG-SCENE-014）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | Q3：使用规则做意图路由时，如何证明规则能够覆盖线上流量 |
| 来源引用（Source References） | `SRC-NOWCODER-XUNLEI-AI-INTENT-ROUTING-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-XUNLEI-AI-INTENT-ROUTING-2026`: https://www.nowcoder.com/discuss/918809114392657920；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-07-001`, `RAG-07-002`, `RAG-07-008`, `RAG-07-010`, `RAG-07-011`, `RAG-07-012` |
| 本问题全部流程节点（All Mapped Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 评估（Evaluation） [`PS-EVALUATION`] |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做离线分类/改写/路由评估、影子流量对比、延迟成本压测和失败样本复查；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0015"></a>
### PQ-RAG-0015：长尾查询（Long-tail Query） 召回率（Recall）低时，如何在 多查询扩展（Multi-Query Expansion）、假设文档嵌入（Hypothetical Document Embeddings，HyDE）、查询分解（Query Decomposition）、会话查询改写（Conversational Query Rewrite）和 退步提示（Step-back Prompting） 之间选择，并防止专有名词丢失、语义漂移、噪声放大及延迟失控？（RAG engineering problem RAG-SCENE-015）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q5：Query 改写、HyDE、Query Expansion 与 Multi-Query |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-07-003`, `RAG-07-004`, `RAG-07-005`, `RAG-07-006`, `RAG-07-007`, `RAG-07-009`, `RAG-07-011`, `RAG-07-012` |
| 本问题全部流程节点（All Mapped Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做离线分类/改写/路由评估、影子流量对比、延迟成本压测和失败样本复查；没有 `evaluated_by` 时保留为待验证项。

<a id="pq-rag-0016"></a>
### PQ-RAG-0016：一个请求什么时候无需检索、只需单次检索、需要多次检索或应路由到外部工具（External Tool），如何设计置信度（Confidence）、成本预算、降级（Graceful Degradation）和错误路由（Misrouting）评估？（RAG engineering problem RAG-SCENE-016）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q9：Adaptive RAG、Iterative RAG、Self-RAG、CRAG 与 Agentic RAG |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-07-002`, `RAG-07-010`, `RAG-07-012` |
| 本问题全部流程节点（All Mapped Stages） | 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`], 检索（Retrieval） [`PS-RETRIEVAL`], 结果融合（Result Fusion） [`PS-RESULT-FUSION`], 重排（Reranking） [`PS-RERANKING`], 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。

**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。

**验证与追问**：固定数据和版本，做离线分类/改写/路由评估、影子流量对比、延迟成本压测和失败样本复查；没有 `evaluated_by` 时保留为待验证项。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 第一人称面经（First-person Interview Report）、公开题库（Public Question Bank）和项目型考题（Project Interview Exercise）只证明题目出处或场景，不证明企业官方面试事实。
- 当前状态为 inventory-only；正式页面仍需按模板补充完整现象、根因分支、方案权衡、实现细节和验证证据。

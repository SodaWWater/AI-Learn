# 答案生成（Answer Generation）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`

> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

答案生成（Answer Generation）基于查询和受控上下文生成答案，并处理忠实性、拒答、格式和输出边界。当前图谱包含 16 个知识原子，并映射 5 道问题。

## 通用诊断路径

1. 固定查询、证据集合、模型版本、提示模板和发布策略，区分上下文缺失、生成偏差与引用失配。
2. 记录窗口截断、权限过滤、拒答、未支撑主张和格式错误，按失败样本而非平均指标复查。
3. 同时比较质量、延迟、成本、隐私、可回滚性与审计可追溯性。
4. 图谱未登记的根因、方案或评估关系保持为待验证缺口。

## 问题明细

<a id="pq-rag-0002"></a>
### PQ-RAG-0002：法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子 Chunk、Metadata、Hybrid Retrieval、Rerank、引用和质检？（RAG engineering problem RAG-SCENE-002）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 4 节：法律文本 Chunking |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG`: https://www.nowcoder.com/discuss/882634966025175040；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-09-007` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0004"></a>
### PQ-RAG-0004：补全 Query/Document Embedding、批量建库、FAISS Top-K 检索、ID 映射、上下文生成和准确率记录的完整 VectorRAG 链路。（RAG engineering problem RAG-SCENE-004）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 1 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-09-006` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0020"></a>
### PQ-RAG-0020：相关证据已经召回但位于长上下文中间、被重复片段或冲突证据淹没时，如何分配 词元（Token） 预算、排序、去重、压缩并验证没有丢失关键依据？（RAG engineering problem RAG-SCENE-020）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q6：Lost in the Middle |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-09-002`, `RAG-09-003`, `RAG-09-004`, `RAG-09-005`, `RAG-09-011`, `RAG-09-013` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0023"></a>
### PQ-RAG-0023：当检索结果质量不足但生成器仍会强制作答时，如何识别 Retrieval Bias（检索偏置），区分零召回、低相关和证据不足，并在过滤、拒答、回退及迭代检索之间选择？（RAG engineering problem RAG-SCENE-023）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q4：如何解决 Retrieval Bias（检索偏置） |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025`: https://www.nowcoder.com/feed/main/detail/d15b819dd04c4fdda9c2cc82d8fadbbc；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-09-006`, `RAG-09-008`, `RAG-09-009` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0024"></a>
### PQ-RAG-0024：多个已召回文档在事实、时间或观点上互相冲突时，如何保留来源与时间 Metadata（元数据），进行可信度排序和交叉验证，并在答案中显式呈现共识、分歧与不确定性？（RAG engineering problem RAG-SCENE-024）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：RAG 如何处理多文档冲突信息 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-TEN-QUESTIONS-2025`: https://www.nowcoder.com/feed/main/detail/d15b819dd04c4fdda9c2cc82d8fadbbc；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-09-007`, `RAG-09-011`, `RAG-09-012`, `RAG-09-013` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 当前状态为 inventory-only；正式页面仍需按模板补充完整证据。

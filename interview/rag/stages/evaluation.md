# 评估（Evaluation）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`

> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

评估（Evaluation）用离线数据、在线流量和端到端指标验证检索增强生成质量、成本与稳定性。当前图谱包含 14 个知识原子，并映射 14 道问题。

## 通用诊断路径

1. 固定查询、证据集合、模型版本、提示模板和发布策略，区分上下文缺失、生成偏差与引用失配。
2. 记录窗口截断、权限过滤、拒答、未支撑主张和格式错误，按失败样本而非平均指标复查。
3. 同时比较质量、延迟、成本、隐私、可回滚性与审计可追溯性。
4. 图谱未登记的根因、方案或评估关系保持为待验证缺口。

## 问题明细

<a id="pq-rag-0001"></a>
### PQ-RAG-0001：已有 召回率（Recall）@5 指标时，如何证明结果足够好，评测集规模和分布如何设计，怎样建立公平基线并区分检索错误与生成错误？（RAG engineering problem RAG-SCENE-001）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 2 节：Recall@5 与评测集；附录现场碎片 |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG`: https://www.nowcoder.com/discuss/882634966025175040；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-001`, `RAG-10-002`, `RAG-10-003`, `RAG-10-004`, `RAG-10-009`, `RAG-10-011`, `RAG-10-013` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0004` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION`, `EVAL-RAG-LAYERED` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0003"></a>
### PQ-RAG-0003：面对给定文档量、Chunk 数和固定 词元（Token） 长度，如何验证切分参数自洽，并用数据而不是经验值证明选择？（RAG engineering problem RAG-SCENE-003）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 附录：500 份 PDF、5 万 Chunk 与 512 Token |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG`: https://www.nowcoder.com/discuss/882634966025175040；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-009` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0004` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION`, `EVAL-RAG-RETRIEVAL` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0006"></a>
### PQ-RAG-0006：把 VectorRAG 和 GraphRAG 日志转换为评测数据，计算 忠实性（Faithfulness）、上下文（Context） Precision 和 上下文（Context） 召回率（Recall），并输出可比较的明细结果。（RAG engineering problem RAG-SCENE-006）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 3 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-003`, `RAG-10-004`, `RAG-10-006`, `RAG-10-008`, `RAG-10-013` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0004` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-LAYERED` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0007"></a>
### PQ-RAG-0007：如何按文档结构、模型长度和业务查询选择文本切分大小、重叠与高级切分方案，并用检索和端到端实验验证参数？（RAG engineering problem RAG-SCENE-007）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：文本切块策略、大小和重叠长度 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-009` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0008"></a>
### PQ-RAG-0008：生产 RAG 面对复杂文档解析、增量索引、多语言检索、延迟、模型升级、缓存、监控和敏感信息权限时，应如何分层定位与治理？（RAG engineering problem RAG-SCENE-008）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：实际部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-001` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0010"></a>
### PQ-RAG-0010：固定长度、滑动窗口、语义切分和分层切分分别怎样影响召回、精度、索引规模和上下文完整性，应该如何设计对照实验？（RAG engineering problem RAG-SCENE-010）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q6：chunking strategies and retrieval quality |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 来源定位与审核（Locator and Review） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026`: https://github.com/ImranMatin/rag-interview-questions；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-009` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0014"></a>
### PQ-RAG-0014：线上存在复合意图、表达省略、地域歧义和新业务类型时，如何证明规则与模型的意图识别覆盖真实流量，并用影子对比、拒识和错误路由样本发现盲区？（RAG engineering problem RAG-SCENE-014）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | Q3：使用规则做意图路由时，如何证明规则能够覆盖线上流量 |
| 来源引用（Source References） | `SRC-NOWCODER-XUNLEI-AI-INTENT-ROUTING-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-XUNLEI-AI-INTENT-ROUTING-2026`: https://www.nowcoder.com/discuss/918809114392657920；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-009`, `RAG-10-011` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0018"></a>
### PQ-RAG-0018：BM25 与向量检索的原始分数尺度不可直接比较且会返回重复 Chunk 时，如何用 RRF 或分数归一化融合、去重，并验证某个通道没有被系统性淹没？（RAG engineering problem RAG-SCENE-018）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | BM25 + 向量召回、RRF 融合和去重候选链路 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026`: https://www.nowcoder.com/discuss/906597462301818880；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-009` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-RETRIEVAL` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0019"></a>
### PQ-RAG-0019：Reranker 不新增候选却增加明显延迟时，怎样选择进入重排的候选数、最终 Top-N、跳过重排条件和降级链路，并分别解释 召回率（Recall）、NDCG 与 MRR 的变化？（RAG engineering problem RAG-SCENE-019）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `engineering_case` |
| 原始定位（Source Locator） | RRF 候选集后接 Reranker 的场景闸门、Top-N 和评测结果 |
| 来源引用（Source References） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026`: https://www.nowcoder.com/discuss/906597462301818880；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-002`, `RAG-10-003`, `RAG-10-004` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0002` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-RETRIEVAL` |

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
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-014` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0021"></a>
### PQ-RAG-0021：一次回答失败时，如何区分解析、召回、排序、上下文、生成和引用错误，并联合设计 Golden Dataset、分层指标、LLM-as-a-Judge 校准、人工抽检及线上 A/B 实验？（RAG engineering problem RAG-SCENE-021）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：如何全面评估 RAG 系统 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-001`, `RAG-10-002`, `RAG-10-004`, `RAG-10-005`, `RAG-10-007`, `RAG-10-008`, `RAG-10-009`, `RAG-10-011`, `RAG-10-013`, `RAG-10-014` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0004` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-LAYERED` |

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
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-014` |
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
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-008`, `RAG-10-009` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0025"></a>
### PQ-RAG-0025：RAG 评测命中率接近 100% 时，如何排查样本过小、针对性调参、训练或提示泄漏、公开文档进入模型预训练数据等污染，并用私有未见数据、冻结快照和分层置信区间证明结果可信？（RAG engineering problem RAG-SCENE-025）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | RAG 评测追问 1—6 |
| 来源引用（Source References） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026`: https://www.nowcoder.com/feed/main/detail/76f5be8b8bd5420b94d32a66e26a7ad9；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-10-001`, `RAG-10-002`, `RAG-10-003`, `RAG-10-004`, `RAG-10-011`, `RAG-10-012`, `RAG-10-014` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0004` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-LAYERED` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 当前状态为 inventory-only；正式页面仍需按模板补充完整证据。

# 生产治理（Production Governance）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`

> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

生产治理（Production Governance）管理权限、安全、可观测性、性能、成本、版本发布与故障恢复。当前图谱包含 19 个知识原子，并映射 7 道问题。

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
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-11-005` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | `EVAL-RAG-CITATION` |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0005"></a>
### PQ-RAG-0005：实现实体召回、多跳子图抽取、路径去重、语义剪枝、生产者消费者队列、提前停止，并分析路径爆炸和图算法选型。（RAG engineering problem RAG-SCENE-005）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 2 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-11-007` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
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
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-11-002`, `RAG-11-013` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0009"></a>
### PQ-RAG-0009：向量索引中的文档发生新增、修改和删除时，如何在全量重建、软删除、版本化标识和延迟压缩之间选择，并保证在线一致性与回滚能力？（RAG engineering problem RAG-SCENE-009）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：document updates and deletions |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 来源定位与审核（Locator and Review） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026`: https://github.com/ImranMatin/rag-interview-questions；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-11-002`, `RAG-11-003`, `RAG-11-004` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0013"></a>
### PQ-RAG-0013：向量数据库在数据增长、高并发、Metadata 过滤、删除更新和 Embedding 模型升级时，如何选择 Exact、HNSW 或 IVF，定位过滤后召回下降，并完成无停机索引迁移？（RAG engineering problem RAG-SCENE-013）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：向量数据库、检索延迟和模型升级等部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-11-004` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0022"></a>
### PQ-RAG-0022：为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？（RAG engineering problem RAG-SCENE-022）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第三轮系统设计题及多租户、增量更新、检索评估追问 |
| 来源引用（Source References） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026`: https://www.nowcoder.com/discuss/904058990026420224；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-11-002`, `RAG-11-004`, `RAG-11-008`, `RAG-11-012`, `RAG-11-013`, `RAG-11-019` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0001`, `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0026"></a>
### PQ-RAG-0026：Agentic RAG（智能体检索增强生成）中的工具怎样注册并描述参数、权限和作用范围，如何把请求用户身份与最小权限传播到每次工具调用，并防止工具描述投毒、跨服务越权和高风险调用绕过人工确认？（RAG engineering problem RAG-SCENE-026）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | Agent 架构与记忆追问 4 |
| 来源引用（Source References） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AI-APP-INTERN-RAG-EVAL-2026`: https://www.nowcoder.com/feed/main/detail/76f5be8b8bd5420b94d32a66e26a7ad9；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-11-012`, `RAG-11-013`, `RAG-11-015`, `RAG-11-016`, `RAG-11-017` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 当前状态为 inventory-only；正式页面仍需按模板补充完整证据。

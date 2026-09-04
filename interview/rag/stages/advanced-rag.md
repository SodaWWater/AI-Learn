# 高级检索增强生成（Advanced RAG）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`

> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

高级检索增强生成（Advanced RAG）组合迭代检索、智能体、自反思和图谱等能力，并明确适用边界与验证要求。当前图谱包含 20 个知识原子，并映射 4 道问题。

## 通用诊断路径

1. 固定查询、证据集合、模型版本、提示模板和发布策略，区分上下文缺失、生成偏差与引用失配。
2. 记录窗口截断、权限过滤、拒答、未支撑主张和格式错误，按失败样本而非平均指标复查。
3. 同时比较质量、延迟、成本、隐私、可回滚性与审计可追溯性。
4. 图谱未登记的根因、方案或评估关系保持为待验证缺口。

## 问题明细

<a id="pq-rag-0005"></a>
### PQ-RAG-0005：实现实体召回、多跳子图抽取、路径去重、语义剪枝、生产者消费者队列、提前停止，并分析路径爆炸和图算法选型。（RAG engineering problem RAG-SCENE-005）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `project_interview_exercise` |
| 原始定位（Source Locator） | README 考题 2 |
| 来源引用（Source References） | `SRC-HEBUTBRYANT-RAG-INTERVIEW` |
| 来源定位与审核（Locator and Review） | `SRC-HEBUTBRYANT-RAG-INTERVIEW`: https://github.com/hebutBryant/rag_interview；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-12-009`, `RAG-12-010`, `RAG-12-020` |
| 图谱解决方案边（Solved By） | 未登记（图谱无 solved_by 边） |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0011"></a>
### PQ-RAG-0011：如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？（RAG engineering problem RAG-SCENE-011）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：mixed text, tables, and images in PDF |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 来源定位与审核（Locator and Review） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026`: https://github.com/ImranMatin/rag-interview-questions；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-12-011` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0003` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

<a id="pq-rag-0016"></a>
### PQ-RAG-0016：一个请求什么时候无需检索、只需单次检索、需要多次检索或应路由到外部工具，如何设计置信度、成本预算、降级和错误路由评估？（RAG engineering problem RAG-SCENE-016）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q9：Adaptive RAG、Iterative RAG、Self-RAG、CRAG 与 Agentic RAG |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 来源定位与审核（Locator and Review） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026`: https://www.nowcoder.com/discuss/878352209799364608；审核日期 2026-09-04 |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-12-004`, `RAG-12-005`, `RAG-12-006`, `RAG-12-007` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0006` |
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
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-12-004`, `RAG-12-018` |
| 图谱解决方案边（Solved By） | `SOL-RAG-0005` |
| 图谱评估边（Evaluated By） | 未登记（图谱无 evaluated_by 边） |

**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。

**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。

**限制**：当前为 inventory-only，缺失关系保留为待验证项。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 当前状态为 inventory-only；正式页面仍需按模板补充完整证据。

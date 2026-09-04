# 文档解析（Document Parsing）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-02`
>
> 本页只投影图谱中已登记并通过 `problem_at` 关联到文档解析（Document Parsing）流程节点（Pipeline Stage）的工程问题/面试题（Engineering Problem / Interview Question）。来源只证明题目出处，不把题库答案当作技术证据。

## 节点边界

文档解析（Document Parsing）将 PDF、扫描件、网页、表格和图片转换为保留结构与定位信息的中间表示，供数据治理（Data Governance）和文本切分（Chunking）继续处理。当前映射 4 道问题：`PQ-RAG-0002`、`PQ-RAG-0008`、`PQ-RAG-0011`、`PQ-RAG-0022`。

## 通用诊断路径

1. 先按文档类型记录解析器、版本、页码、元素类型和失败率，再区分 OCR（Optical Character Recognition）、版面顺序、表格结构或编码问题。
2. 原始文件、解析中间表示和最终 Chunk 保留稳定文档 ID、页码、坐标、版本和父子关系，保证可重放与引用回溯。
3. 解析质量门通过后才进入数据治理（Data Governance）；无法解析的页应进入隔离队列或降级路径，不静默写入空索引。
4. 图谱当前未登记 `caused_by` 根因边；下文候选诊断点仅来自 `problem_at` 关系。

## 问题明细

### PQ-RAG-0002：法律条文结构与扫描件噪声

| 字段 | 内容 |
|---|---|
| 问题 | 法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子文本切分（Parent-child Chunking）、元数据（Metadata）、混合检索（Hybrid Retrieval）、重排（Reranking）、引用（Citation）和质检？ |
| 来源类型 | `first_person_interview`（第一人称面经，First-person Interview Report） |
| 原始定位 | `第 4 节：法律文本 Chunking`；`SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 关联流程节点 | `PS-DOCUMENT-PARSING`、`PS-DATA-GOVERNANCE`、`PS-CHUNKING`、`PS-RETRIEVAL`、`PS-RESULT-FUSION`、`PS-RERANKING`、`PS-CONTEXT-ASSEMBLY`、`PS-ANSWER-GENERATION`、`PS-CITATION-VERIFICATION`、`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-03-003`、`RAG-03-004`、`RAG-03-014` 及其跨节点关联原子 |
| 图谱方案与实现 | `SOL-RAG-0003` → `IMP-RAG-0004`；权限边界另见 `SOL-RAG-0005` |
| 图谱评估 | `EVAL-RAG-CITATION` |

**工程现象和候选根因**：OCR（Optical Character Recognition）误识别、双栏顺序错乱、条款层级丢失或页码映射不稳定，使召回证据无法定位；候选点为 `RAG-03-003`、`RAG-03-004`、`RAG-03-014`。

**方案、选择依据与实现**：保存原始页码、元素坐标、条款层级和父子 ID；对低质量页面隔离并人工抽检，再让小片段负责召回、父片段负责上下文组装和引用。实现沿图谱登记的 `IMP-RAG-0004`，按引用完整性、解析延迟和存储成本选择。

**验证与追问**：建立页级金标准，检查 OCR 字段、层级、引用和回溯成功率；追问扫描质量下降时如何降级，跨租户文档如何证明权限过滤在检索前生效。

### PQ-RAG-0008：生产 RAG 的解析质量与更新边界

| 字段 | 内容 |
|---|---|
| 问题 | 生产检索增强生成（Retrieval-Augmented Generation，RAG）面对复杂文档解析、增量索引、多语言检索、延迟、模型升级、缓存、监控和敏感信息权限时，应如何分层定位与治理？ |
| 来源类型 | `public_question_bank`（公开题库，Public Question Bank） |
| 原始定位 | `Q10：实际部署挑战`；`SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点 | `PS-DOCUMENT-PARSING`、`PS-DATA-GOVERNANCE`、`PS-STORAGE-INDEXING`、`PS-EVALUATION`、`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-03-003`、`RAG-03-012` 及其跨节点关联原子 |
| 图谱方案与实现 | `SOL-RAG-0001` → `IMP-RAG-0005`；权限过滤使用 `SOL-RAG-0005` |
| 图谱评估 | 图谱未登记该问题的 `evaluated_by` 边，不能补写为已验证结论。 |

**工程现象和候选根因**：解析失败形成索引空洞，旧版本仍可召回，或模型升级造成表示不兼容；候选点为 `RAG-03-003`、`RAG-03-012`、`RAG-06-014`。

**方案、选择依据与实现**：为每份文档记录解析版本、内容哈希和处理批次；失败进入重试/隔离队列，成功结果以版本化索引和原子别名发布。按 P99 延迟、回滚窗口和重建成本选择，具体实现只引用 `IMP-RAG-0005`。

**验证与追问**：对新增、修改、删除、解析失败和模型升级执行幂等性（Idempotency）、回滚和索引滞后回归；追问缓存如何避免绕过权限，部分租户失败时如何恢复。

### PQ-RAG-0011：混合模态 PDF 的结构保真

| 字段 | 内容 |
|---|---|
| 问题 | 如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？ |
| 来源类型 | `public_question_bank`（公开题库，Public Question Bank） |
| 原始定位 | `Q8：mixed text, tables, and images in PDF`；`SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 关联流程节点 | `PS-DOCUMENT-PARSING`、`PS-DATA-GOVERNANCE`、`PS-CHUNKING`、`PS-ADVANCED-RAG` |
| 知识节点 | `RAG-03-003`、`RAG-03-004`、`RAG-03-006`、`RAG-03-014`、`RAG-12-011` |
| 图谱方案与实现 | `SOL-RAG-0003` → `IMP-RAG-0004` |
| 图谱评估 | 图谱未登记该问题的 `evaluated_by` 边；应回查解析质量和引用指标，而不是推断通过。 |

**工程现象和候选根因**：表格被展平、图片与 Caption（图注）脱离、页码丢失或 OCR 文本混入正文，导致命中后无法恢复证据；候选点为 `RAG-03-004`、`RAG-03-006`、`RAG-03-014`。

**方案、选择依据与实现**：保留元素类型、页码、坐标、父文档 ID 和模态关系；文本、表格和图片使用匹配的表示，再在上下文组装（Context Assembly）阶段恢复页级引用。按模态覆盖、可解释性和成本选择，沿用 `IMP-RAG-0004`。

**验证与追问**：用页级人工金标准分别统计表格单元格、图片 Caption 和页码引用错误率；追问图片无法解析时是否降级为 OCR，以及多模态表示如何避免重复计权。

### PQ-RAG-0022：多租户文档解析与版本一致性

| 字段 | 内容 |
|---|---|
| 问题 | 为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？ |
| 来源类型 | `first_person_interview`（第一人称面经，First-person Interview Report） |
| 原始定位 | `第三轮系统设计题及多租户、增量更新、检索评估追问`；`SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 关联流程节点 | `PS-DOCUMENT-PARSING`、`PS-DATA-GOVERNANCE`、`PS-CHUNKING`、`PS-EMBEDDING`、`PS-STORAGE-INDEXING`、`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-03-003` 及其跨节点关联原子 |
| 图谱方案与实现 | `SOL-RAG-0001` → `IMP-RAG-0005`；权限与租户隔离另见 `SOL-RAG-0005` |
| 图谱评估 | 图谱未登记该问题的 `evaluated_by` 边；需按 `RAG-06-012` 的规模和延迟指标补做验证。 |

**工程现象和候选根因**：租户分片热点、解析/向量版本混用、删除延迟和权限传播错误会造成陈旧结果或越权；候选点为 `RAG-03-003`、`RAG-06-010`、`RAG-06-014`。

**方案、选择依据与实现**：解析输出携带租户、文档和版本前缀；使用版本化索引、双写（Dual Write）和原子别名切换完成迁移，检索前传播租户身份做过滤。按隔离强度、P99、成本和恢复时间目标选择，引用 `IMP-RAG-0005`。

**验证与追问**：压测租户倾斜、迁移回滚、删除传播、备份恢复和越权样本；分层记录解析失败率、索引滞后、召回率和 P99。追问：单租户热点如何迁移，旧解析版本何时可下线。

## 来源与限制

- 本页题目、知识、方案、实现和评估 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 题目来源只证明出处；技术结论仍需由图谱登记的一手证据（First-party Evidence）核验。
- 图谱未登记的 `caused_by` 或 `evaluated_by` 关系在本页明确标注，不能用推断替代证据。

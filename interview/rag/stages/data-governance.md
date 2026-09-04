# 数据治理（Data Governance）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-03`
>
> 本页只投影有向知识图谱（Directed Knowledge Graph）中已登记、通过 `problem_at` 关联到数据治理（Data Governance）流程节点（Pipeline Stage）的工程问题/面试题（Engineering Problem / Interview Question）。题目来源只证明问题出处，不单独证明技术结论。

## 节点边界

数据治理（Data Governance）负责解析后数据进入文本切分（Chunking）和索引前的质量、权限、隐私、来源与版本约束。图谱当前将 4 道问题映射到本节点：`PQ-RAG-0002`、`PQ-RAG-0008`、`PQ-RAG-0011`、`PQ-RAG-0022`。

## 通用诊断路径

1. 先核对文档类型、解析结果、来源与时间元数据（Metadata），再判断问题是否来自解析、治理或后续文本切分（Chunking）。
2. 对权限和个人可识别信息（Personally Identifiable Information，PII）先做入库前拒绝、脱敏和租户隔离，不能依赖生成阶段补救。
3. 记录文档版本、处理批次、解析质量和删除状态，保证增量更新（Incremental Update）可重放、可回滚。
4. 图谱当前未登记 `caused_by` 根因边，因此下表的“根因分支”严格以该问题的 `problem_at` 知识节点作为候选诊断点，不把候选点宣称为已证实根因。

## 问题明细

### PQ-RAG-0002：法律条文和扫描件的治理链路

| 字段 | 内容 |
|---|---|
| 问题 | 法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子文本切分（Parent-child Chunking）、元数据（Metadata）、混合检索（Hybrid Retrieval）、重排（Reranking）、引用（Citation）和质检？ |
| 来源类型 | `first_person_interview`（第一人称面经，First-person Interview Report） |
| 原始定位 | `第 4 节：法律文本 Chunking`；来源节点：`SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 关联流程节点 | 文档解析（Document Parsing）`PS-DOCUMENT-PARSING`；数据治理（Data Governance）`PS-DATA-GOVERNANCE`；文本切分（Chunking）`PS-CHUNKING`；检索（Retrieval）`PS-RETRIEVAL`；结果融合（Result Fusion）`PS-RESULT-FUSION`；重排（Reranking）`PS-RERANKING`；上下文组装（Context Assembly）`PS-CONTEXT-ASSEMBLY`；答案生成（Answer Generation）`PS-ANSWER-GENERATION`；引用与验证（Citation and Verification）`PS-CITATION-VERIFICATION`；生产治理（Production Governance）`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-03-003`、`RAG-03-004`、`RAG-03-014`、`RAG-04-004`、`RAG-04-007`、`RAG-04-014`、`RAG-08-004`、`RAG-08-010`、`RAG-09-007`、`RAG-11-005` |
| 图谱方案与实现 | `SOL-RAG-0003` 结构感知与父子上下文切分（Structure-aware and Parent-child Chunking）→ `IMP-RAG-0004`；`SOL-RAG-0005` 权限过滤与多租户隔离（Access Filtering and Tenant Isolation）→ `IMP-RAG-0004`、`IMP-RAG-0005` |
| 图谱评估 | `EVAL-RAG-CITATION` 引用准确性与完整性评估（Citation Accuracy and Completeness） |

**工程现象和候选根因**：扫描件 OCR（Optical Character Recognition）误识别、栏序错乱、条款层级丢失或父子 ID 不一致，会导致召回证据不可定位。对应候选诊断点是 `RAG-03-003`、`RAG-03-004`、`RAG-03-014`、`RAG-04-014`。

**方案、选择依据与实现**：保留原始页码和元素坐标，按条/款/项建立父子关系；敏感文档在入库前做权限过滤和 PII 脱敏；以业务的引用可追溯性、权限风险和解析延迟选择是否启用多模态解析。实现沿图谱登记的 `IMP-RAG-0004`、`IMP-RAG-0005`，不在此页新增框架结论。

**验证与追问**：抽样检查 OCR 字段、层级关系、引用页码和权限越权样本；使用 `EVAL-RAG-CITATION` 检查引用准确性（Citation Accuracy）与完整性（Citation Completeness）。追问：扫描质量下降时如何回退？跨租户文档如何证明过滤在召回前生效？

### PQ-RAG-0008：生产 RAG 的数据治理边界

| 字段 | 内容 |
|---|---|
| 问题 | 生产检索增强生成（Retrieval-Augmented Generation，RAG）面对复杂文档解析、增量索引、多语言检索、延迟、模型升级、缓存、监控和敏感信息权限时，应如何分层定位与治理？ |
| 来源类型 | `public_question_bank`（公开题库，Public Question Bank） |
| 原始定位 | `Q10：实际部署挑战`；来源节点：`SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点 | 数据治理（Data Governance）`PS-DATA-GOVERNANCE`；文档解析（Document Parsing）`PS-DOCUMENT-PARSING`；存储与索引（Storage and Indexing）`PS-STORAGE-INDEXING`；评估（Evaluation）`PS-EVALUATION`；生产治理（Production Governance）`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-02-008`、`RAG-03-003`、`RAG-03-012`、`RAG-06-014`、`RAG-10-001`、`RAG-11-002`、`RAG-11-013` |
| 图谱方案与实现 | `SOL-RAG-0001` 增量与版本化索引更新（Incremental and Versioned Index Updates）→ `IMP-RAG-0005`；`SOL-RAG-0005` 权限过滤与多租户隔离（Access Filtering and Tenant Isolation）→ `IMP-RAG-0004`、`IMP-RAG-0005` |
| 图谱评估 | 图谱未为该问题登记 `evaluated_by`；应回查 `RAG-10-001` 的评估覆盖（Evaluation Coverage）和 `RAG-06-014` 的更新一致性。 |

**工程现象和候选根因**：增量更新后旧版本仍可召回、权限过滤遗漏、解析失败导致索引空洞、模型升级造成向量空间不兼容。候选诊断点为 `RAG-03-003`、`RAG-03-012`、`RAG-06-014`。

**方案、选择依据与实现**：以文档版本和删除标记驱动增量流水线；用蓝绿索引（Blue-green Index）或版本别名完成原子切换；在检索前执行租户和文档级权限过滤。选择取决于 P99 延迟、回滚窗口、租户隔离强度和重建成本；实现仅引用 `IMP-RAG-0005`。

**验证与追问**：对新增、修改、删除和模型升级分别做幂等性（Idempotency）、回滚和权限回归；记录解析失败率、索引滞后、过滤后召回和 P99 延迟。追问：如何证明缓存没有绕过权限？如何在部分租户失败时恢复？

### PQ-RAG-0011：混合模态文档的数据保真

| 字段 | 内容 |
|---|---|
| 问题 | 如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？ |
| 来源类型 | `public_question_bank`（公开题库，Public Question Bank） |
| 原始定位 | `Q8：mixed text, tables, and images in PDF`；来源节点：`SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 关联流程节点 | 文档解析（Document Parsing）`PS-DOCUMENT-PARSING`；数据治理（Data Governance）`PS-DATA-GOVERNANCE`；文本切分（Chunking）`PS-CHUNKING`；高级检索增强生成（Advanced RAG）`PS-ADVANCED-RAG` |
| 知识节点 | `RAG-03-003`、`RAG-03-004`、`RAG-03-006`、`RAG-03-014`、`RAG-04-011`、`RAG-12-011` |
| 图谱方案与实现 | `SOL-RAG-0003` 结构感知与父子上下文切分（Structure-aware and Parent-child Chunking）→ `IMP-RAG-0004` |
| 图谱评估 | 图谱未为该问题登记 `evaluated_by`；验证应覆盖 `RAG-03-014` 的解析质量抽检和 `RAG-10-009` 的引用准确性。 |

**工程现象和候选根因**：表格被展平、图片与 Caption（图注）脱离、页码丢失或 OCR 结果混入正文，导致检索命中但无法还原证据。候选诊断点为 `RAG-03-004`、`RAG-03-006`、`RAG-03-014`、`RAG-04-011`。

**方案、选择依据与实现**：保存元素类型、页码、坐标、父文档 ID 和模态关系；文本、表格和图片使用与其表示匹配的检索通道，再在上下文组装（Context Assembly）阶段恢复页级引用。按可解释性、存储成本和目标文档模态分布选择方案；实现沿用 `IMP-RAG-0004`。

**验证与追问**：建立页级人工金标准，分别统计表格单元格、图片 Caption 和页码引用的错误率；追问：图片无法解析时是否降级为 OCR？多模态表示如何避免重复计权？

### PQ-RAG-0022：多租户企业知识库治理

| 字段 | 内容 |
|---|---|
| 问题 | 为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？ |
| 来源类型 | `first_person_interview`（第一人称面经，First-person Interview Report） |
| 原始定位 | `第三轮系统设计题及多租户、增量更新、检索评估追问`；来源节点：`SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 关联流程节点 | 文档解析（Document Parsing）`PS-DOCUMENT-PARSING`；数据治理（Data Governance）`PS-DATA-GOVERNANCE`；文本切分（Chunking）`PS-CHUNKING`；向量嵌入（Embedding）`PS-EMBEDDING`；存储与索引（Storage and Indexing）`PS-STORAGE-INDEXING`；生产治理（Production Governance）`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-03-003`、`RAG-04-007`、`RAG-05-012`、`RAG-06-010`、`RAG-06-012`、`RAG-06-013`、`RAG-06-014`、`RAG-11-002`、`RAG-11-004`、`RAG-11-008`、`RAG-11-012`、`RAG-11-013`、`RAG-11-019` |
| 图谱方案与实现 | `SOL-RAG-0001` 增量与版本化索引更新（Incremental and Versioned Index Updates）→ `IMP-RAG-0005`；`SOL-RAG-0005` 权限过滤与多租户隔离（Access Filtering and Tenant Isolation）→ `IMP-RAG-0004`、`IMP-RAG-0005` |
| 图谱评估 | 图谱未为该问题登记 `evaluated_by`；应按 `RAG-06-012` 的规模、QPS、延迟、召回率和成本基准验证。 |

**工程现象和候选根因**：租户增长造成分片热点，模型升级期间新旧向量混查，权限传播和删除延迟造成跨租户暴露或陈旧结果。候选诊断点为 `RAG-03-003`、`RAG-06-010`、`RAG-06-014`、`RAG-11-012`、`RAG-11-013`。

**方案、选择依据与实现**：按租户规模和风险选择物理隔离、逻辑隔离或混合分片；通过版本化索引、双写（Dual Write）和原子别名切换完成无停机迁移；权限过滤字段随请求身份传播到每次检索。选择依据是隔离强度、P99、成本、恢复时间目标和运维复杂度；实现引用 `IMP-RAG-0005`。

**验证与追问**：压测租户倾斜、迁移回滚、备份恢复、删除传播和越权样本；分层报告检索召回、P99、成本和权限错误率。追问：单租户热点如何迁移？旧模型索引何时安全下线？

## 来源与限制

- 本页所有题目、节点和方案 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 题目来源定位沿用图谱字段；技术实现和评估只沿已有关系引用，不复制来源正文。
- 当前图谱没有为上述所有问题登记根因（`caused_by`）和评估（`evaluated_by`）边；缺口已在各题标明，不以推断替代证据。

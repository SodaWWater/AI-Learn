# 文本切分（Chunking）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-04`
>
> 本页只投影图谱中已登记、通过 `problem_at` 关联到文本切分（Chunking）流程节点（Pipeline Stage）的工程问题/面试题（Engineering Problem / Interview Question）。它们是问题入口，不是背诵式答案，也不把公开题库升级为企业官方结论。

## 节点边界

文本切分（Chunking）把解析后的文档组织为可检索、可回溯、可装配的片段，同时受检索（Retrieval）和生成（Generation）的上下文预算约束。当前 6 道问题映射到本节点：`PQ-RAG-0002`、`PQ-RAG-0003`、`PQ-RAG-0007`、`PQ-RAG-0010`、`PQ-RAG-0011`、`PQ-RAG-0022`。

## 通用诊断路径

1. 先明确文档结构、查询类型、上下文预算和引用粒度，再选择固定长度、递归、结构感知或父子切分。
2. 分块大小（Chunk Size）、分块重叠（Chunk Overlap）和父子映射必须与召回、上下文完整性、索引规模和延迟一起评估，不能使用脱离数据的固定经验值。
3. 对表格、代码和多模态内容保留元素边界与来源定位，必要时让小片段负责召回、大片段负责回溯。
4. 图谱当前未登记 `caused_by` 根因边；“候选根因”仅表示该题关联的知识节点，不表示因果关系已被证明。

## 问题明细

### PQ-RAG-0002：结构感知切分与父子回溯

| 字段 | 内容 |
|---|---|
| 问题 | 法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子文本切分（Parent-child Chunking）、元数据（Metadata）、混合检索（Hybrid Retrieval）、重排（Reranking）、引用（Citation）和质检？ |
| 来源类型 | `first_person_interview`（第一人称面经，First-person Interview Report） |
| 原始定位 | `第 4 节：法律文本 Chunking`；`SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 关联流程节点 | 文档解析（Document Parsing）`PS-DOCUMENT-PARSING`；数据治理（Data Governance）`PS-DATA-GOVERNANCE`；文本切分（Chunking）`PS-CHUNKING`；检索（Retrieval）`PS-RETRIEVAL`；结果融合（Result Fusion）`PS-RESULT-FUSION`；重排（Reranking）`PS-RERANKING`；上下文组装（Context Assembly）`PS-CONTEXT-ASSEMBLY`；答案生成（Answer Generation）`PS-ANSWER-GENERATION`；引用与验证（Citation and Verification）`PS-CITATION-VERIFICATION`；生产治理（Production Governance）`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-04-004`、`RAG-04-007`、`RAG-04-014`，并与 `RAG-03-003`、`RAG-03-004`、`RAG-03-014` 等解析节点相连 |
| 图谱方案与实现 | `SOL-RAG-0003` 结构感知与父子上下文切分（Structure-aware and Parent-child Chunking）→ `IMP-RAG-0004` |
| 图谱评估 | `EVAL-RAG-CITATION` 引用准确性与完整性评估（Citation Accuracy and Completeness） |

**工程现象和候选根因**：条款边界被截断、父子 ID 丢失或扫描噪声进入片段，导致命中片段无法回溯完整条文。候选诊断点为 `RAG-04-004`、`RAG-04-007`、`RAG-04-014`。

**方案、选择依据与实现**：按标题、条款层级切分；小子片段用于召回，父片段用于上下文组装和引用；保留 `Chunk ID`、`Parent ID` 和版本字段。方案选择看引用粒度、索引规模和上下文预算；实现引用 `IMP-RAG-0004`。

**验证与追问**：对条款边界、父子回溯、引用页码和重复片段做回归测试（Regression Test）；追问：父片段过大导致上下文超限时如何压缩？

### PQ-RAG-0003：切分参数自洽与实验验证

| 字段 | 内容 |
|---|---|
| 问题 | 面对给定文档量、Chunk 数和固定 Token 长度，如何验证切分参数自洽，并用数据而不是经验值证明选择？ |
| 来源类型 | `first_person_interview`（第一人称面经，First-person Interview Report） |
| 原始定位 | `附录：500 份 PDF、5 万 Chunk 与 512 Token`；`SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 关联流程节点 | 文本切分（Chunking）`PS-CHUNKING`；存储与索引（Storage and Indexing）`PS-STORAGE-INDEXING`；评估（Evaluation）`PS-EVALUATION` |
| 知识节点 | `RAG-04-012`、`RAG-04-013`、`RAG-04-015`、`RAG-06-012`、`RAG-10-009` |
| 图谱方案与实现 | `SOL-RAG-0004` 分层评估与回归诊断（Layered Evaluation and Regression Diagnosis）；图谱未登记该问题的 `implemented_by` 边 |
| 图谱评估 | `EVAL-RAG-CITATION`、`EVAL-RAG-RETRIEVAL` |

**工程现象和候选根因**：文档数、片段数、平均长度和 Token 上限相互矛盾，或 Overlap（重叠）放大索引规模。候选诊断点为 `RAG-04-012`、`RAG-04-013`、`RAG-06-012`。

**方案、选择依据与实现**：先用计数、长度分布和 Token 预算校验参数，再以检索召回、引用完整性、索引大小、吞吐和成本做对照实验；按数据和 SLO（Service Level Objective，服务等级目标）选择，而不是给出通用最佳值。验证沿 `SOL-RAG-0004` 和两个图谱评估节点。

**验证与追问**：固定数据快照，比较不同分块大小（Chunk Size）、分块重叠（Chunk Overlap）和策略的召回率（Recall）、平均倒数排名（Mean Reciprocal Rank，MRR）、引用完整性和 P99 延迟（P99 Latency）；追问：平均长度满足约束但长尾超限时如何处理？

### PQ-RAG-0007：按结构和查询选择切分策略

| 字段 | 内容 |
|---|---|
| 问题 | 如何按文档结构、模型长度和业务查询选择文本切分大小、重叠与高级切分方案，并用检索和端到端实验验证参数？ |
| 来源类型 | `public_question_bank`（公开题库，Public Question Bank） |
| 原始定位 | `Q3：文本切块策略、大小和重叠长度`；`SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 关联流程节点 | 文本切分（Chunking）`PS-CHUNKING`；评估（Evaluation）`PS-EVALUATION` |
| 知识节点 | `RAG-04-002`、`RAG-04-003`、`RAG-04-004`、`RAG-04-005`、`RAG-04-007`、`RAG-04-012`、`RAG-04-013`、`RAG-10-009` |
| 图谱方案与实现 | `SOL-RAG-0003` 结构感知与父子上下文切分（Structure-aware and Parent-child Chunking）→ `IMP-RAG-0004` |
| 图谱评估 | 图谱未登记 `evaluated_by`；应使用 `RAG-10-009` 与检索指标回归。 |

**工程现象和候选根因**：固定长度切断语义单元，语义切分成本过高，Overlap 造成重复召回。候选诊断点为 `RAG-04-002`、`RAG-04-003`、`RAG-04-005`、`RAG-04-012`、`RAG-04-013`。

**方案、选择依据与实现**：从递归字符切分（Recursive Character Splitting）起步，对标题和段落明确的文档使用结构切分；需要跨段回溯时使用父子切分。实现引用 `IMP-RAG-0004`，选择依据为查询分布、上下文预算、延迟和存储。

**验证与追问**：对切分策略做离线消融实验（Ablation Study）和端到端回归；追问：不同文档类型是否应使用不同策略？

### PQ-RAG-0010：切分方法对召回和索引成本的影响

| 字段 | 内容 |
|---|---|
| 问题 | 固定长度、滑动窗口、语义切分和分层切分分别怎样影响召回、精度、索引规模和上下文完整性，应该如何设计对照实验？ |
| 来源类型 | `public_question_bank`（公开题库，Public Question Bank） |
| 原始定位 | `Q6：chunking strategies and retrieval quality`；`SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 关联流程节点 | 文本切分（Chunking）`PS-CHUNKING`；评估（Evaluation）`PS-EVALUATION` |
| 知识节点 | `RAG-04-002`、`RAG-04-005`、`RAG-04-007`、`RAG-04-012`、`RAG-04-013`、`RAG-10-009` |
| 图谱方案与实现 | `SOL-RAG-0003` 结构感知与父子上下文切分（Structure-aware and Parent-child Chunking）→ `IMP-RAG-0004` |
| 图谱评估 | 图谱未登记 `evaluated_by`；关联 `RAG-10-009` 做引用与端到端检查。 |

**工程现象和候选根因**：召回率提升但重复片段、索引体积和上下文噪声同时增加，或语义边界导致片段长度长尾。候选诊断点为 `RAG-04-005`、`RAG-04-012`、`RAG-04-013`。

**方案、选择依据与实现**：保持数据、Embedding（向量嵌入）模型和检索器不变，仅切换切分策略；将召回、排序、引用完整性、索引规模和延迟作为联合目标。实现使用 `IMP-RAG-0004` 的结构与父子策略。

**验证与追问**：对每种方法运行相同查询集和显著性比较，记录召回率（Recall）、归一化折损累计增益（Normalized Discounted Cumulative Gain，nDCG）、平均倒数排名（Mean Reciprocal Rank，MRR）、词元（Token）消耗和 P99 延迟（P99 Latency）；追问：如何区分切分收益与嵌入模型（Embedding Model）变化？

### PQ-RAG-0011：表格、代码和多模态内容专项切分

| 字段 | 内容 |
|---|---|
| 问题 | 如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？ |
| 来源类型 | `public_question_bank`（公开题库，Public Question Bank） |
| 原始定位 | `Q8：mixed text, tables, and images in PDF`；`SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 关联流程节点 | 文档解析（Document Parsing）`PS-DOCUMENT-PARSING`；数据治理（Data Governance）`PS-DATA-GOVERNANCE`；文本切分（Chunking）`PS-CHUNKING`；高级检索增强生成（Advanced RAG）`PS-ADVANCED-RAG` |
| 知识节点 | `RAG-04-011`、以及 `RAG-03-003`、`RAG-03-004`、`RAG-03-006`、`RAG-03-014`、`RAG-12-011` |
| 图谱方案与实现 | `SOL-RAG-0003` 结构感知与父子上下文切分（Structure-aware and Parent-child Chunking）→ `IMP-RAG-0004` |
| 图谱评估 | 图谱未登记 `evaluated_by`；回查 `RAG-03-014` 和 `RAG-10-009`。 |

**工程现象和候选根因**：表格行列被打散、代码缩进丢失、图片与 Caption 分离或页码无法回溯。候选诊断点为 `RAG-04-011` 及其关联解析节点。

**方案、选择依据与实现**：按元素类型使用专项切分，保留页码、坐标、父文档和模态关联；小粒度元素负责召回，父片段负责上下文。实现引用 `IMP-RAG-0004`，依据可引用性、模态覆盖和存储成本选择。

**验证与追问**：建立表格、代码和图片混合金标准，分别评估元素召回、结构完整性和页级引用；追问：表格序列化和原图并存时如何去重？

### PQ-RAG-0022：多租户场景的父子切分与版本一致性

| 字段 | 内容 |
|---|---|
| 问题 | 为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？ |
| 来源类型 | `first_person_interview`（第一人称面经，First-person Interview Report） |
| 原始定位 | `第三轮系统设计题及多租户、增量更新、检索评估追问`；`SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 关联流程节点 | 文档解析（Document Parsing）`PS-DOCUMENT-PARSING`；数据治理（Data Governance）`PS-DATA-GOVERNANCE`；文本切分（Chunking）`PS-CHUNKING`；向量嵌入（Embedding）`PS-EMBEDDING`；存储与索引（Storage and Indexing）`PS-STORAGE-INDEXING`；生产治理（Production Governance）`PS-PRODUCTION-GOVERNANCE` |
| 知识节点 | `RAG-04-007`，以及 `RAG-03-003`、`RAG-05-012`、`RAG-06-010`、`RAG-06-012`、`RAG-06-013`、`RAG-06-014`、`RAG-11-002`、`RAG-11-004`、`RAG-11-008`、`RAG-11-012`、`RAG-11-013`、`RAG-11-019` |
| 图谱方案与实现 | `SOL-RAG-0001` 增量与版本化索引更新（Incremental and Versioned Index Updates）→ `IMP-RAG-0005` |
| 图谱评估 | 图谱未登记 `evaluated_by`；按 `RAG-06-012` 验证规模、QPS、延迟、召回率和成本。 |

**工程现象和候选根因**：父片段跨租户复用、Chunk 版本与向量版本不一致、增量删除未传播到父子映射。候选诊断点为 `RAG-04-007`、`RAG-06-014` 和权限相关节点。

**方案、选择依据与实现**：父子 ID 带租户和版本前缀；增量更新采用版本化索引和原子别名切换，检索时先做租户过滤再回溯父片段。实现引用 `IMP-RAG-0005`，选择依据为隔离强度、回滚能力、P99 延迟（P99 Latency）和维护成本。

**验证与追问**：压测租户隔离、版本迁移、删除传播和回滚；检查父子命中不会跨租户，比较更新前后召回率（Recall）、引用完整性和 P99 延迟（P99 Latency）。追问：共享父片段如何证明不存在隐式数据泄露？

## 来源与限制

- 本页所有问题、知识、方案、实现和评估 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 来源定位沿用图谱字段；公开题目只作为问题线索，技术结论仍需由图谱登记的一手证据核验。
- 当前部分问题没有 `evaluated_by` 或 `implemented_by` 边，页面已显式标注，不能以推断替代图谱关系。

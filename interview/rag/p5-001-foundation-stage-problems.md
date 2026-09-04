# P5-001 基础流程节点问题索引增量（Foundation Stage Problem Batch）

> 状态：`candidate / WP-P5-001 / graph-backed / inventory-only`
>
> 范围：数据摄取（Data Ingestion）、文档解析（Document Parsing）、数据治理（Data Governance）、文本切分（Chunking）。
>
> 图谱输入：[`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)；生成器：[`scripts/generate_rag_stage_problem_batch.py`](../../scripts/generate_rag_stage_problem_batch.py)。

本批只投影已有问题节点（Problem Question Nodes）以及图谱中的 `contains`、`problem_at` 和 `supported_by` 关系；不新增题目、不生成正式答案、不把来源登记中的阶段提示替换为图谱关系。

## 生成审计（Generation Audit）

- 图谱版本：`2026-09-04`；节点：437；边：1930。
- 批次流程节点：4；图谱问题节点：26；本批已投影问题：7。
- 题目来源只证明题目出处或工程场景；技术结论仍需回到图谱已登记的一手证据（First-party Evidence）。

## 节点覆盖（Stage Coverage）

| 流程节点（Pipeline Stage） | 图谱包含原子数 | 已映射问题数 | 问题 ID | 覆盖结论 |
|---|---:|---:|---|---|
| 数据摄取（Data Ingestion） [`PS-DATA-INGESTION`] | 0 | 0 | 无 | 当前图谱没有该阶段的 `contains` 原子，不能从来源元数据推断题目映射；保留为覆盖缺口。 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 15 | 4 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0008`](#pq-rag-0008), [`PQ-RAG-0011`](#pq-rag-0011), [`PQ-RAG-0022`](#pq-rag-0022) | 可由现有 `contains` 与 `problem_at` 边投影；仅作为问题入口。 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 15 | 4 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0008`](#pq-rag-0008), [`PQ-RAG-0011`](#pq-rag-0011), [`PQ-RAG-0022`](#pq-rag-0022) | 可由现有 `contains` 与 `problem_at` 边投影；仅作为问题入口。 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 17 | 6 | [`PQ-RAG-0002`](#pq-rag-0002), [`PQ-RAG-0003`](#pq-rag-0003), [`PQ-RAG-0007`](#pq-rag-0007), [`PQ-RAG-0010`](#pq-rag-0010), [`PQ-RAG-0011`](#pq-rag-0011), [`PQ-RAG-0022`](#pq-rag-0022) | 可由现有 `contains` 与 `problem_at` 边投影；仅作为问题入口。 |

## 问题映射（Problem Mappings）

### 数据摄取（Data Ingestion） [`PS-DATA-INGESTION`]

当前图谱没有可投影的问题节点。数据摄取（Data Ingestion）来源检索和来源登记仍存在候选证据，但本批不新增 `problem_at` 或 `contains` 边；待图谱映射审计后再进入正式问题生产。

### 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`]

<a id="pq-rag-0002"></a>
#### PQ-RAG-0002：法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子 Chunk、Metadata、Hybrid Retrieval、Rerank、引用和质检？（RAG engineering problem RAG-SCENE-002）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 4 节：法律文本 Chunking |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003`, `RAG-03-004`, `RAG-03-014` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0008"></a>
#### PQ-RAG-0008：生产 RAG 面对复杂文档解析、增量索引、多语言检索、延迟、模型升级、缓存、监控和敏感信息权限时，应如何分层定位与治理？（RAG engineering problem RAG-SCENE-008）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：实际部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003`, `RAG-03-012` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0011"></a>
#### PQ-RAG-0011：如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？（RAG engineering problem RAG-SCENE-011）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：mixed text, tables, and images in PDF |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003`, `RAG-03-004`, `RAG-03-006`, `RAG-03-014` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0022"></a>
#### PQ-RAG-0022：为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？（RAG engineering problem RAG-SCENE-022）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第三轮系统设计题及多租户、增量更新、检索评估追问 |
| 来源引用（Source References） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

### 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`]

<a id="pq-rag-0002"></a>
#### PQ-RAG-0002：法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子 Chunk、Metadata、Hybrid Retrieval、Rerank、引用和质检？（RAG engineering problem RAG-SCENE-002）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 4 节：法律文本 Chunking |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003`, `RAG-03-004`, `RAG-03-014` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0008"></a>
#### PQ-RAG-0008：生产 RAG 面对复杂文档解析、增量索引、多语言检索、延迟、模型升级、缓存、监控和敏感信息权限时，应如何分层定位与治理？（RAG engineering problem RAG-SCENE-008）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q10：实际部署挑战 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003`, `RAG-03-012` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0011"></a>
#### PQ-RAG-0011：如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？（RAG engineering problem RAG-SCENE-011）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：mixed text, tables, and images in PDF |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003`, `RAG-03-004`, `RAG-03-006`, `RAG-03-014` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0022"></a>
#### PQ-RAG-0022：为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？（RAG engineering problem RAG-SCENE-022）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第三轮系统设计题及多租户、增量更新、检索评估追问 |
| 来源引用（Source References） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-03-003` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

### 文本切分（Chunking） [`PS-CHUNKING`]

<a id="pq-rag-0002"></a>
#### PQ-RAG-0002：法律条文包含条、款、项、引用关系和扫描件噪声时，如何设计结构解析、父子 Chunk、Metadata、Hybrid Retrieval、Rerank、引用和质检？（RAG engineering problem RAG-SCENE-002）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第 4 节：法律文本 Chunking |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-04-004`, `RAG-04-007`, `RAG-04-014` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0003"></a>
#### PQ-RAG-0003：面对给定文档量、Chunk 数和固定 Token 长度，如何验证切分参数自洽，并用数据而不是经验值证明选择？（RAG engineering problem RAG-SCENE-003）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 附录：500 份 PDF、5 万 Chunk 与 512 Token |
| 来源引用（Source References） | `SRC-NOWCODER-BYTEDANCE-AI-APPLICATION-RAG` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-04-012`, `RAG-04-013`, `RAG-04-015` |
| 本问题全部流程节点（All Mapped Stages） | 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0007"></a>
#### PQ-RAG-0007：如何按文档结构、模型长度和业务查询选择文本切分大小、重叠与高级切分方案，并用检索和端到端实验验证参数？（RAG engineering problem RAG-SCENE-007）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q3：文本切块策略、大小和重叠长度 |
| 来源引用（Source References） | `SRC-NOWCODER-AGENT-RAG-QUESTION-BANK-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-04-002`, `RAG-04-003`, `RAG-04-004`, `RAG-04-005`, `RAG-04-007`, `RAG-04-012`, `RAG-04-013` |
| 本问题全部流程节点（All Mapped Stages） | 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0010"></a>
#### PQ-RAG-0010：固定长度、滑动窗口、语义切分和分层切分分别怎样影响召回、精度、索引规模和上下文完整性，应该如何设计对照实验？（RAG engineering problem RAG-SCENE-010）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q6：chunking strategies and retrieval quality |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-04-002`, `RAG-04-005`, `RAG-04-007`, `RAG-04-012`, `RAG-04-013` |
| 本问题全部流程节点（All Mapped Stages） | 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0011"></a>
#### PQ-RAG-0011：如何从混合文本、表格和图片的 PDF 中保留版面、页码和模态关系，分别建立检索表示，并在答案中恢复可靠引用？（RAG engineering problem RAG-SCENE-011）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `public_question_bank` |
| 原始定位（Source Locator） | Q8：mixed text, tables, and images in PDF |
| 来源引用（Source References） | `SRC-IMRANMATIN-RAG-INTERVIEW-QUESTIONS-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-04-011` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

<a id="pq-rag-0022"></a>
#### PQ-RAG-0022：为大量企业租户设计支持复杂文档、增量更新、文档级权限、检索质量目标和 P99 延迟目标的 RAG 系统时，如何选择索引与隔离方式，规划分片副本、无停机模型迁移、备份恢复和分层评测？（RAG engineering problem RAG-SCENE-022）

| 字段 | 内容 |
|---|---|
| 来源类型（Provenance Type） | `first_person_interview` |
| 原始定位（Source Locator） | 第三轮系统设计题及多租户、增量更新、检索评估追问 |
| 来源引用（Source References） | `SRC-NOWCODER-ENTERPRISE-RAG-SYSTEM-INTERVIEW-2026` |
| 当前节点关联原子（Stage Knowledge Atoms） | `RAG-04-007` |
| 本问题全部流程节点（All Mapped Stages） | 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`], 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`], 文本切分（Chunking） [`PS-CHUNKING`] |

该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。

## 关系与边界（Relations and Boundaries）

- 节点映射仅使用图谱已有 `contains`（Contains）和问题到知识原子的 `problem_at`（Problem At）边；没有因题目语义相近而合并问题。
- `supported_by`（Supported By）沿用图谱的来源引用；公开题目来源支持题目出处，不直接支持技术结论。
- 数据摄取（Data Ingestion）目前为零映射是结构性缺口，不代表该流程没有工程问题；补映射前不得生成无来源问题节点。
- 文档解析（Document Parsing）、数据治理（Data Governance）和文本切分（Chunking）的跨节点问题必须保留其全部流程节点，不强制拆成单节点题目。

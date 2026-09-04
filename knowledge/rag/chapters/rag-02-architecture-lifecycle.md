---
id: RAG-02
title: RAG 系统架构与生命周期
status: formal_candidate
reviewed_at: 2026-09-04
freshness_class: active
atoms:
  - RAG-02-001
  - RAG-02-002
  - RAG-02-003
  - RAG-02-004
  - RAG-02-005
  - RAG-02-006
  - RAG-02-007
  - RAG-02-008
  - RAG-02-009
  - RAG-02-010
related_problem_ids:
  - PQ-RAG-0008
  - PQ-RAG-0009
  - PQ-RAG-0013
  - PQ-RAG-0022
source_refs:
  - rag-original-2020
  - nvidia-rag-blueprint
  - azure-ai-search-rag-overview-2026
  - azure-indexer-change-delete-detection-2026
  - azure-document-access-control-2026
  - debezium-architecture-docs-2026
  - aws-genai-data-lifecycle-guidance-2026
  - langchain-parent-document-retriever-2026
  - langchain-multi-query-retriever-2026
  - llamaindex-router-docs-2026
related_problem_ids:
  - PQ-RAG-0008
  - PQ-RAG-0009
  - PQ-RAG-0013
  - PQ-RAG-0022
related_node_ids:
  - RAG-01
  - RAG-03
  - RAG-04
  - RAG-05
  - RAG-06
  - RAG-07
  - RAG-08
  - RAG-09
  - RAG-10
  - RAG-11
  - RAG-12
---

# RAG 系统架构与生命周期（RAG System Architecture and Lifecycle）

## 1. 知识点概要

检索增强生成（Retrieval-Augmented Generation，RAG）系统由离线知识构建（Offline Knowledge Construction）和在线问答（Online Question Answering）两条主链组成。离线链把来源对象（Source Object）变成带版本、权限和元数据（Metadata）的索引；在线链把用户问题（User Query）变成候选（Candidate）、证据（Evidence）和可追溯答案（Traceable Answer）。评估（Evaluation）、生产治理（Production Governance）和反馈把两条链闭合为可持续生命周期。

本章保留 `RAG-02` 的 10 个知识原子（Knowledge Atom），它们描述系统级边界而不是某个产品的固定架构：

| 原子 | 覆盖内容 |
|---|---|
| `RAG-02-001` | 离线知识库构建全流程（Offline Knowledge-base Build） |
| `RAG-02-002` | 在线问答全流程（Online Question-answering Flow） |
| `RAG-02-003` | 召回、过滤、生成三段式链路（Recall, Filtering and Generation Chain） |
| `RAG-02-004` | 解析器、切分器、嵌入器、索引和检索器边界（Component Boundaries） |
| `RAG-02-005` | 检索器、重排器、生成器边界（Retriever, Reranker and Generator） |
| `RAG-02-006` | 数据流、控制流和错误流（Data, Control and Error Flows） |
| `RAG-02-007` | 来源到答案的可追溯链路（Source-to-answer Traceability） |
| `RAG-02-008` | 批处理、流式摄取和事件驱动更新（Batch, Streaming and Event-driven Updates） |
| `RAG-02-009` | 模块化接口和组件可替换性（Modular Interfaces and Replaceability） |
| `RAG-02-010` | 任务状态、幂等性和失败恢复（Task State, Idempotency and Recovery） |

该架构不等同于“向量数据库（Vector Database）加大语言模型（Large Language Model，LLM）”。可检索证据的生产、权限裁剪、版本发布、失败恢复和分层评估同样属于系统职责。原始 RAG 论文只规定了检索器与生成器的基本关系；下文的生产边界是工程化扩展，不能反推为论文中的固定实现。

## 2. 技术原理

### 2.1 离线知识库构建全流程（`RAG-02-001`）

离线流程的输入是文件、网页、数据库记录或对象存储事件，输出是一个可验证的索引版本（Index Version）。典型变换为：

```text
Source Object
 -> Parsed Document
 -> Normalized Elements
 -> Chunk[]
 -> Dense/Sparse Representation
 -> Candidate Index
 -> Validated Index Release
```

每个中间对象都应保存输入哈希（Hash）、处理器版本（Processor Version）、配置哈希、输出定位和状态。内容哈希用于判断是否需要重算；文档标识（Document ID）表示逻辑身份，文档版本（Document Version）表示内容状态。索引写入（Index Write）和索引发布（Index Release）必须分离，只有通过模式（Schema）、权限、数量、抽样检索和回归测试（Regression Test）的候选版本才能切换为在线版本。

### 2.2 在线问答全流程（`RAG-02-002`）

在线请求先完成认证、租户识别、限流（Rate Limiting）和追踪标识（Trace ID）生成，再依次或并行经过查询理解（Query Understanding）、查询改写（Query Rewrite）、查询路由（Query Routing）、多路检索（Multi-channel Retrieval）、过滤、结果融合（Result Fusion）、重排（Reranking）、上下文组装（Context Assembly）、答案生成（Answer Generation）和引用验证（Citation Verification）。推荐把状态建模为对象而非字符串：

```text
QueryRequest -> Candidate[] -> Evidence[] -> GenerationContext -> Answer
```

`Candidate` 仍可能无权限、重复或低相关，不能直接作为答案依据；`Evidence` 已经过权限和质量门禁；`Answer` 还应带引用、拒答（Abstention）状态、模型版本、索引版本和追踪标识。这样可以分别计算检索覆盖率（Recall）、排序质量和生成忠实度（Faithfulness）。

### 2.3 召回、过滤、生成三段式链路（`RAG-02-003`）

三段式是故障归因和指标设计的逻辑边界，不要求拆成三个网络服务。

1. **召回（Recall）**：用稠密检索（Dense Retrieval）、稀疏检索（Sparse Retrieval）、结构化查询或知识图谱（Knowledge Graph）取得高覆盖候选。关注 `Recall@K`、命中率（Hit Rate）、候选数量和延迟。
2. **过滤与排序（Filtering and Ranking）**：按访问控制列表（Access Control List，ACL）、有效时间、来源可信度、去重、融合和重排保留可用证据。关注归一化折损累计增益（Normalized Discounted Cumulative Gain，nDCG）、平均倒数排名（Mean Reciprocal Rank，MRR）和权限过滤后的证据保留率。
3. **上下文与生成（Context and Generation）**：在词元（Token）预算内排序、压缩和标注证据，要求模型进行基于检索证据的生成（Grounded Generation）；证据不足时走拒答或澄清。关注答案正确性（Answer Correctness）、事实依据性（Groundedness）、引用准确率和端到端成功率。

用最终答案指标直接调 `Top-K` 会混淆知识缺失、召回失败、排序错误、上下文截断和生成偏离；必须保留分段日志。

### 2.4 离线组件职责边界（`RAG-02-004`）

| 组件 | 输入与职责 | 明确不负责 |
|---|---|---|
| Loader/Connector | 发现来源、读取内容、记录版本 | 猜测阅读顺序或生成答案 |
| Parser | 恢复文本、版面、表格和图片元素 | 擅自固定长度切分并丢弃结构 |
| Normalizer/Governor | 清洗、去重、脱敏、元数据和权限 | 修改事实以迎合模型 |
| Splitter | 按结构和检索目标生成文本片段（Chunk）及父子关系 | 选择在线候选或生成答案 |
| Embedder | 按固定嵌入模型（Embedding Model）生成向量 | 混写不同维度或归一化规则 |
| Index Writer | 校验模式、幂等写入、构建索引 | 未过质量门禁就发布 |
| Retriever | 按查询和过滤条件获得候选 | 将候选宣称为最终证据 |

稳定的 `document_id` 和 `chunk_id` 让解析器或嵌入模型可以单独升级；下游只依赖领域数据契约，不依赖某个框架的私有对象。

### 2.5 检索器、重排器和生成器边界（`RAG-02-005`）

检索器（Retriever）面向全库，优先吞吐和覆盖，输出通道、原始分数、名次、索引版本和过滤结果。重排器（Reranker）只处理较小候选集，用查询与文档联合编码或业务规则提升精度；它不能补回检索器从未找到的文档。生成器（Generator）消费已编号证据，负责综合、抽取或结构化输出，并遵守证据范围、无证据行为和引用映射。

并行检索的延迟预算可写为：

$$T_{total}=T_{route}+\max(T_{retrieve,1},...,T_{retrieve,n})+T_{rerank}+T_{context}+T_{generate}+T_{post}$$

各阶段应有独立超时和降级路径；把所有调用串行化，或把过大的候选集送入重排，通常比生成模型本身更容易造成尾延迟（Tail Latency）。

### 2.6 数据流、控制流和错误流（`RAG-02-006`）

数据流（Data Flow）携带文档、文本片段、向量、查询、候选、证据、上下文和答案；控制流（Control Flow）决定是否检索、并行通道、重试、停止条件、降级或人工审批；错误流（Error Flow）携带技术错误、数据错误、质量错误和业务状态。网络超时、解析空白、向量维度不兼容、零召回、无权限和证据不足必须使用不同错误码和恢复策略，不能统一变成 `HTTP 500`，也不能在检索失败时静默让模型自由作答。

### 2.7 来源到答案的可追溯链路（`RAG-02-007`）

可审计链路至少包含：

```text
source_id -> document_id/document_version -> chunk_id/chunk_version
 -> representation_version -> index_version -> request_id/trace_id
 -> citation_id/answer_id
```

引用记录应保存来源标识、固定版本或时间、页码/段落等定位、内容哈希和答案中的支持范围，而不只是可变的 URL。删除传播要覆盖向量、倒排项、图节点、缓存、评估副本和日志副本；只删除向量库不构成完整删除。

### 2.8 批处理、流式摄取和事件驱动更新（`RAG-02-008`）

批处理（Batch Processing）适合高吞吐和全局去重；流式摄取（Streaming Ingestion）适合持续记录和低新鲜度延迟；事件驱动更新（Event-driven Update）适合文件新增、修改和删除的增量触发。事件只是“可能变化”的通知，消费者仍需读取当前来源、比较哈希和版本。周期性全量对账可发现丢事件、乱序、权限变化和长期漂移。混合方案通常是事件增量加周期对账，但会增加背压（Backpressure）、重复消费和小批效率的治理成本。

### 2.9 模块化接口和组件可替换性（`RAG-02-009`）

可替换性来自稳定接口而不是类名。最低契约应明确字段语义、分数方向、版本、超时、错误类型、最大批量和幂等性：

```text
Retriever.search(QueryRequest) -> Candidate[]
Reranker.rank(QueryRequest, Candidate[]) -> Evidence[]
ContextBuilder.build(QueryRequest, Evidence[], Budget) -> GenerationContext
Generator.generate(GenerationContext) -> AnswerDraft
Verifier.verify(AnswerDraft, Evidence[]) -> Answer
```

切换嵌入模型、检索器、重排器或生成器时，先做离线回放或影子流量（Shadow Traffic），再做灰度发布（Canary Release）；比较质量、延迟、成本和失败分布。向量维度、查询/文档前缀、文本片段格式和上下文窗口等兼容条件应封装为经过验证的 `pipeline_profile`。

### 2.10 任务状态、幂等性和失败恢复（`RAG-02-010`）

摄取任务可按以下状态推进：

```text
DISCOVERED -> FETCHED -> PARSED -> NORMALIZED -> CHUNKED
           -> EMBEDDED -> INDEXED -> VALIDATED -> PUBLISHED
```

状态记录完成时间、处理器版本、输入输出引用、尝试次数和最后错误；`PUBLISHED` 应是索引版本状态，而不是单个文档直接设置。幂等键可由租户、来源、文档版本、处理器版本和配置哈希组成。短暂网络错误使用带抖动的指数退避；权限、损坏文件和模式不兼容进入死信（Dead Letter）或人工队列。索引发布使用不可变版本和可切换别名，质量回归时回滚到上一个已验证版本。

## 3. 实际开发中的位置和使用方式

### 3.1 服务和数据边界

小规模系统可以同进程部署，但仍按职责划分模块：摄取调度器（Ingestion Scheduler）写入状态存储（State Store），解析和表示工作进程生成中间产物，索引写入器和发布管理器维护候选索引；查询应用程序编程接口（Application Programming Interface，API）负责认证和策略，查询编排器调用检索适配器、重排器、上下文构建器、生成器和验证器。只有吞吐、资源隔离或团队边界需要时才拆为独立服务。

### 3.2 一个请求的运行位置

请求进入 `Query API` 后生成 `request_id` 和 `trace_id`，查询理解与路由决定知识源和检索预算；检索适配器并行访问稠密、稀疏或结构化后端；策略层执行租户和文档级 ACL；重排与上下文构建把候选收敛成证据；生成器和验证器返回答案、引用、拒答原因和版本。在线服务不得读取候选中未通过权限检查的文本。

### 3.3 更新、删除和发布位置

来源连接器在摄取阶段记录内容哈希和有效时间；事件消费者只负责触发，实际内容由读取器确认。删除事件应沿 `document_id` 找到所有文本片段、向量、索引项、缓存和评估样本。新索引在隔离环境完成数量、模式、权限和黄金数据集（Golden Dataset）回归后，以原子切换（Atomic Switch）更新别名；旧版本保留到回滚窗口结束。

### 3.4 可观测性和评估位置

每个阶段至少记录耗时、输入输出数量、版本、失败原因和过滤数量。摄取关注解析空白率和更新延迟，索引关注构建耗时和删除滞留，检索关注零召回与通道延迟，重排关注批大小和截断率，生成关注首词元延迟、拒答和引用，端到端关注答案质量、成本和用户反馈。评估集同时标注问题、可接受答案和直接证据，并用分层指标定位首次失败阶段。

### 3.5 何时选择不同生命周期模式

数据小时级更新且允许重建时选择批处理；订单、工单等持续变化数据选择流式或事件增量；高合规场景必须把 ACL、保留期和删除验证放进状态机；多租户场景把租户标识、索引隔离和资源配额放进每个接口契约。没有可靠评测集时，不应仅凭单次示例扩大路由、重排或生成模型。

## 4. 具体技术或框架实现

### 4.1 自研最小实现（伪代码）

以下伪代码展示状态、幂等和证据边界，具体存储和模型由适配器提供：

```python
def ingest(event, state, parser, embedder, index):
    doc = source.read(event.source_id)
    version = sha256(doc.bytes)
    key = (event.tenant_id, event.source_id, version,
           parser.version, config.hash)
    if state.done(key):
        return state.result(key)

    elements = parser.parse(doc)
    chunks = splitter.make(elements, parent_id=doc.document_id)
    vectors = embedder.encode(chunks, model_version=embedder.version)
    candidate = index.upsert(chunks, vectors, acl=doc.acl,
                             document_version=version)
    state.mark(key, "INDEXED", candidate.index_version)
    return candidate

def answer(request):
    route = router.choose(request.query, request.tenant_id)
    candidates = parallel_search(route, request.query, request.filters)
    allowed = [c for c in candidates if policy.allows(request.user, c.acl)]
    evidence = reranker.rank(request.query, deduplicate(allowed))[:8]
    if not evidence:
        return Answer.abstain("NO_EVIDENCE", trace_id=request.trace_id)
    context = context_builder.build(evidence, token_budget=3000)
    draft = generator.generate(request.query, context)
    return verifier.attach_citations(draft, evidence,
                                     trace_id=request.trace_id)
```

这里的 `state.done`、`upsert` 和 `attach_citations` 是自研领域接口：它们分别对应幂等性、索引写入和可追溯引用，不代表某个框架的现成 API。生产实现还需持久化重试次数、删除状态、版本清单和审计日志。

### 4.2 LangChain 组件组合

已登记的 LangChain 官方来源（`langchain-parent-document-retriever-2026`、`langchain-multi-query-retriever-2026`）可用于验证组件组合方式。下面示例保留领域对象边界，框架对象只出现在适配器内；API 以 2026-09-04 审核版本为准，部署前应锁定实际包版本：

```python
from langchain.retrievers import MultiQueryRetriever
from langchain.retrievers import ParentDocumentRetriever

child_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
multi_query = MultiQueryRetriever.from_llm(
    retriever=child_retriever, llm=query_llm
)
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=docstore,
    child_splitter=child_splitter,
)

def retrieve(query):
    candidates = multi_query.invoke(query)
    return normalize_candidates(candidates, index_version=INDEX_VERSION)
```

`MultiQueryRetriever` 对应查询改写和多路召回，`ParentDocumentRetriever` 对应子片段检索后恢复父文档上下文；权限过滤、版本记录、去重和引用映射仍由应用适配器负责，不能假定框架默认行为已经满足生产治理。

### 4.3 LlamaIndex 查询路由

已登记的 `llamaindex-router-docs-2026` 用于查询路由（Query Routing）接口核验。可将向量检索、关键词检索和结构化查询包装成带描述的工具，再由路由器根据查询选择一个或多个工具。路由结果必须记录工具标识、查询、租户策略、超时和失败原因；模型生成的路由不能绕过 ACL 或人工审批。

### 4.4 生产平台和增量事件实现边界

`nvidia-rag-blueprint` 提供生产检索增强生成（Production RAG）的摄取、检索、评估和部署参考；`azure-ai-search-rag-overview-2026` 与 `azure-document-access-control-2026` 用于多源摄取、增量索引和文档级权限边界；`debezium-architecture-docs-2026` 用于变更数据捕获（Change Data Capture，CDC）事件传播的架构参考；`aws-genai-data-lifecycle-guidance-2026` 用于数据生命周期和反馈更新的治理参考。这些资料证明可采用相应模式，不证明任何云服务在当前项目中的默认配置或性能。

## 相关工程问题/面试题

- [PQ-RAG-0008：生产 RAG 分层治理](../../../interview/rag/stages/production-governance.md#pq-rag-0008)
- [PQ-RAG-0009：索引新增、修改和删除的一致性](../../../interview/rag/stages/storage-indexing.md#pq-rag-0009)
- [PQ-RAG-0013：索引类型、过滤和无停机迁移](../../../interview/rag/stages/storage-indexing.md#pq-rag-0013)
- [PQ-RAG-0022：多租户企业 RAG 系统设计](../../../interview/rag/stages/storage-indexing.md#pq-rag-0022)

这些页面包含工程现象、根因、方案比较和验证路径；本章只保留架构原理与实现入口。

## 相关知识节点

| 关系 | 节点 ID | 说明 |
|---|---|---|
| `depends_on` | `RAG-03`、`RAG-04`、`RAG-05`、`RAG-06` | 解析、治理、切分、嵌入和索引实现离线链 |
| `depends_on` | `RAG-07`、`RAG-08`、`RAG-09` | 查询、检索、融合、重排、上下文和生成实现在线链 |
| `evaluated_by` | `RAG-10` | 对召回、排序、生成和端到端链路分层评估 |
| `governed_by` | `RAG-11` | 权限、版本、成本、可观测性和灾难恢复（Disaster Recovery，DR） |
| `extended_by` | `RAG-12` | 模块化、智能体和图增强范式在稳定接口上重组流程 |

## 来源、版本与审核状态

- `rag-original-2020`：RAG 原始论文，NeurIPS 2020，固定 arXiv v4；用于检索器与生成器关系，不作为生产流水线的唯一证据。
- `nvidia-rag-blueprint`：NVIDIA 官方文档，审核日期 2026-09-02；用于生产摄取、检索、评估和部署边界。
- `azure-ai-search-rag-overview-2026`、`azure-indexer-change-delete-detection-2026`、`azure-document-access-control-2026`：Microsoft 官方文档，页面版本和审核日期记录在来源登记；用于增量更新、删除传播和文档级权限。
- `debezium-architecture-docs-2026`：Debezium 官方架构文档，固定登记版本；用于变更事件传播模式。
- `aws-genai-data-lifecycle-guidance-2026`：AWS 官方指导，审核日期 2026-09-02；用于数据生命周期和反馈更新治理。
- `langchain-parent-document-retriever-2026`、`langchain-multi-query-retriever-2026`、`llamaindex-router-docs-2026`：已登记框架官方资料；接口属于高变化内容，示例仅在锁定审核版本后使用。
- `xiaolin-ai-learning`、`ai-agent-interview-guide`、`agent-guide` 和用户 PDF 的相关语义单元已映射到本章原子；题库或用户材料只提供题目线索和场景，不作为技术结论唯一证据。

本章状态为 `formal_candidate`：四段式正文、10 个原子、工程链接和来源边界已完成；框架 API、云产品行为、成本与性能仍需按登记版本周期复核。`RAG-07-001` 与 `RAG-13-011` 的无来源 `inventory_draft` 不被本章引用为已验证事实。

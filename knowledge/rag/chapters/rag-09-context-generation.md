---
id: RAG-09
title: 上下文组装与答案生成
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: mixed
chapter_path: knowledge/rag/chapters/rag-09-context-generation.md
atoms: [RAG-09-001, RAG-09-002, RAG-09-003, RAG-09-004, RAG-09-005, RAG-09-006, RAG-09-007, RAG-09-008, RAG-09-009, RAG-09-010, RAG-09-011, RAG-09-012, RAG-09-013, RAG-09-014, RAG-09-015, RAG-09-016]
related_problem_ids: [PQ-RAG-0002, PQ-RAG-0004, PQ-RAG-0020, PQ-RAG-0023, PQ-RAG-0024]
---

# 上下文组装与答案生成

> 本章状态：`formal_bounded`（范围受限正式，已通过当前登记范围严格验收）。只使用图谱中已登记的来源与原子；问题页面保留工程条件，不把库存题目改写成标准答案。

## 一、知识点概要

上下文组装（Context Assembly）把用户问题（User Query）、检索证据（Retrieved Evidence）、系统提示词（System Prompt）和输出约束合成为生成上下文。答案生成（Answer Generation）必须在证据范围内完成综合、抽取或结构化输出，并返回引用（Citation）、版本和拒答（Abstention）状态。`RAG-09-001`、`RAG-09-006`、`RAG-09-007` 是这条边界的核心。

组装不是把 Top-K 文本简单拼接。系统需要按词元（Token）预算分配空间，去重和压缩证据，排序并处理长上下文的位置效应（`RAG-09-002` 至 `RAG-09-005`）。证据可信度、事实/观点/推断区分和来源冲突处理（`RAG-09-011` 至 `RAG-09-013`）决定答案能否审计；结构化输出（Structured Output）和生成器适配（`RAG-09-014`、`RAG-09-016`）决定结果能否被下游系统消费。

## 二、技术原理

### 2.1 证据包与提示词边界

将输入建模为不可变证据包：

```text
Query -> Policy -> Evidence[] -> Context -> AnswerDraft -> VerifiedAnswer
```

每个 `Evidence` 至少包含 `document_id`、`chunk_id`、来源版本、定位、权限结果和检索/重排分数。系统提示词（System Prompt）规定角色、证据优先级、无证据行为和输出模式；用户问题与证据分区标记，避免把文档中的指令误当成控制指令。生成器只消费通过访问控制列表（Access Control List，ACL）和质量门禁的证据（`RAG-09-001`、`RAG-09-006`）。

### 2.2 预算、排序与压缩

上下文预算应显式扣除系统提示词、用户问题、历史会话、证据、输出预留和安全缓冲。候选按相关性、覆盖、来源可信度、时效和多样性排序，并用文档/段落标识去重。中间信息丢失（Lost in the Middle）说明长上下文中段证据可能被模型利用不足；可通过首尾放置高价值证据、分段摘要、上下文压缩（Contextual Compression）或分批回答缓解，但必须用业务集验证而非假设位置策略必然有效（`RAG-09-002` 至 `RAG-09-005`、`RAG-09-015`）。

压缩只能删除与问题无关的内容或保留支持断言的片段，不能把派生摘要当作原始证据。父子检索（Parent-Document Retrieval）、句子窗口和抽取式压缩可组合；每次压缩保存原始证据 ID，确保引用仍能回链。

### 2.3 基于证据的生成、拒答与核查

基于检索证据的生成（Grounded Generation）要求每个可验证断言由一个或多个证据支持。证据为空、相关性低、权限过滤后不足或来源冲突未解决时，系统应澄清、拒答或说明不确定性，而不是让模型自由补全（`RAG-09-006`、`RAG-09-008`）。常见幻觉链路包括：知识源缺失、解析/切分损坏、召回偏置、排序噪声、上下文截断、模型把证据外知识当事实，以及引用与断言错配（`RAG-09-009`）。

生成后事实核查（Post-generation Fact Checking）可按断言切分答案，逐条寻找支持证据，检查数值、时间、实体和否定关系；未支持断言应删除、改为不确定表述或触发二次检索（`RAG-09-010`）。引用编号应稳定映射到来源固定版本和页/段定位，不以可变 URL 作为唯一凭据（`RAG-09-007`）。

### 2.4 来源、冲突和输出模式

来源可信度（Source Credibility）是策略输入，不是单一全局排名。官方资料、固定版本和直接记录通常优先于二次摘要，但业务时效、权限和适用范围仍需共同判断。事实（Fact）、观点（Opinion）和推断（Inference）在答案中分别标注；多源冲突保留各来源及生效时间，输出共识、分歧和待验证项，不静默合并（`RAG-09-011` 至 `RAG-09-013`）。

结构化输出（Structured Output）以 JSON Schema 或等价模式约束字段、枚举、数组和引用对象；解析失败进入重试或人工队列，不能把半结构化文本当作成功结果（`RAG-09-014`）。长上下文（Long Context）和提示词缓存（Prompt Caching）可降低重复前缀成本，但缓存不应越过租户/权限边界，且不能替代检索、压缩和引用验证（`RAG-09-015`）。生成器适配与微调（Fine-tuning）应优化证据格式遵循、引用行为或领域表达；它不能弥补知识库缺失，也不能绕过在线证据门禁（`RAG-09-016`）。

## 三、实际开发中的位置和使用方式

本模块位于重排（Reranking）之后、引用与验证（Citation and Verification）之后的答案出口之前。在线编排器先完成权限过滤和证据去重，再调用 `ContextBuilder` 生成带预算的上下文，`Generator` 产生答案草稿，`Verifier` 添加引用并记录断言级结果。日志至少包含证据 ID、压缩前后长度、提示词/模型版本、拒答原因和引用覆盖。

典型策略是：简单事实问题使用一次检索和短上下文；多文档综合问题使用分组压缩与冲突检测；证据不足时请求澄清或迭代检索。生产系统应对 `NO_EVIDENCE`、`LOW_RELEVANCE`、`CONFLICT_UNRESOLVED`、`SCHEMA_INVALID` 使用不同错误状态，以便与检索和生成故障分开评估。

## 四、具体技术或框架实现

自研接口可保持如下领域契约：

```python
context = context_builder.build(query, evidence, token_budget=3000)
draft = generator.generate(context, output_schema=AnswerSchema)
answer = verifier.attach_citations(draft, evidence)
```

LangChain 的 `ContextualCompressionRetriever`、`LLMChainExtractor`、`ParentDocumentRetriever` 可作为压缩、抽取和父子上下文适配器；LlamaIndex 的 Sentence Window 思路可恢复命中句的邻近语境。OpenAI Structured Outputs 或同类能力可约束模式，Google Check Grounding、Anthropic Citations 等官方能力可用于核查和引用适配。所有框架 API 以登记审核版本为准，权限过滤、版本追踪、断言级引用和拒答策略仍由应用层负责。

### 完整性检查：对比、关系、错误与评估

短上下文（Short Context）、上下文压缩（Contextual Compression）和长上下文（Long Context）按证据覆盖、成本和延迟对比；它们共同维护 `evidence → context → draft → verified answer → citation` 关系链。常见错误包括 Token 超预算、证据被中间位置淹没、引用与断言错配和结构化解析失败；验收按断言支持率、Citation Accuracy/Completeness、Groundedness、答案正确性、拒答率、P95/P99 和 Token 成本分层。

## 相关工程问题/面试题

- [PQ-RAG-0002：法律文本解析到引用](../../../interview/rag/stages/document-parsing.md#pq-rag-0002)
- [PQ-RAG-0004：VectorRAG 完整链路](../../../interview/rag/stages/storage-indexing.md#pq-rag-0004)
- [PQ-RAG-0020：长上下文证据被淹没](../../../interview/rag/stages/answer-generation.md#pq-rag-0020)
- [PQ-RAG-0023：检索不足时的拒答与回退](../../../interview/rag/stages/answer-generation.md#pq-rag-0023)
- [PQ-RAG-0024：多源冲突答案合并](../../../interview/rag/stages/citation-verification.md#pq-rag-0024)

## 相关知识节点

`RAG-08` 提供候选证据，`RAG-10` 评估答案、忠实度和引用，`RAG-11` 提供权限、安全、成本和可观测性治理，`RAG-12` 提供自适应检索与高级生成范式。

## 来源、版本与审核状态

原始论文和官方资料包括 `SRC-RAG-ORIGINAL-2020`、`SRC-SELF-RAG-2023`、`SRC-LOST-IN-THE-MIDDLE-2023`、`SRC-RECOMP-CONTEXT-COMPRESSION-2023`、`SRC-ALCE-CITATION-EVALUATION-2023`、`SRC-GOOGLE-CHECK-GROUNDING-DOCS-2026`、`SRC-ANTHROPIC-CITATIONS-DOCS-2026`、`SRC-OPENAI-STRUCTURED-OUTPUTS-DOCS-2026` 及已登记框架文档。`SRC-AGENT-GUIDE`、`SRC-AI-AGENT-INTERVIEW-GUIDE`、`SRC-XIAOLIN-AI-LEARNING` 和用户 PDF 只作已纳管补充来源，不能替代原始技术证据。框架接口、模型上下文窗口、缓存和引用能力属于高变化内容，需按登记版本复核。本章覆盖 16 个原子；不引用无来源的 `RAG-13-011`。

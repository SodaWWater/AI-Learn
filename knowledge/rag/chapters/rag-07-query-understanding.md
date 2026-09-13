---
id: RAG-07
title: 查询理解（Query Understanding）与路由
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: active
chapter_path: knowledge/rag/chapters/rag-07-query-understanding.md
atoms: [RAG-07-001, RAG-07-002, RAG-07-003, RAG-07-004, RAG-07-005, RAG-07-006, RAG-07-007, RAG-07-008, RAG-07-009, RAG-07-010, RAG-07-011, RAG-07-012]
related_problem_ids: [PQ-RAG-0014, PQ-RAG-0015, PQ-RAG-0016]
---

# 查询理解（Query Understanding）与路由

> 本章为 `formal_bounded`（范围受限正式）。`RAG-07-001` 在图谱中没有来源引用，本文仅登记其待验证边界，不将其作为已证实结论。

## 一、知识点概要

查询理解把用户原始输入转换为可检索、可路由和可审计的请求。清洗、规范化与语言检测属于 `RAG-07-001`（无来源待验证）；意图识别和是否检索判断（`RAG-07-002`）决定直接回答、单次检索、多次检索或外部工具。查询改写（Query Rewrite，`RAG-07-003`）补全省略并对齐语料；多查询扩展（Multi-Query Expansion，`RAG-07-004`）、HyDE（Hypothetical Document Embeddings，`RAG-07-005`）、子问题分解（`RAG-07-006`）和 Step-back Prompting（`RAG-07-007`）用于长尾或复杂问题。

系统还应抽取实体、时间、地域和权限过滤（`RAG-07-008`），把多轮问题改写成独立查询（`RAG-07-009`），并按意图选择知识源和检索器（`RAG-07-010`）。增强可能造成语义漂移、专名丢失和噪声放大（`RAG-07-011`），需要离线评估（`RAG-07-012`）。

## 二、技术原理

查询处理可表示为 `raw_query → normalized_query → intent/filters → rewrite_set → route`。规范化应保持原始语义、专名、数字和时间；意图分类输出置信度与拒识（Abstention）状态，而不是强制落入已知类别。是否检索判断应考虑知识新鲜度、权限、证据要求和问题类型。

改写目标是提高查询与索引表达的匹配，不是生成答案。多查询产生多个互补表达，再由结果融合去重；HyDE 先生成假设文档并嵌入，可能改善语义匹配，也可能引入幻觉词；子问题分解把复合问题拆成可独立检索的步骤；Step-back 先生成更抽象的问题，适合概念缺失但会损失实体细节。多轮改写需把会话上下文解析为独立、可复现的查询，同时保留原始问题用于审计。

过滤条件应输出结构化字段，如 `entity`, `time_range`, `region`, `tenant_id`, `acl`，并区分硬约束与软偏好。路由器依据意图、数据源能力、延迟预算和权限选择向量、关键词、结构化数据库或外部工具。增强失败时保留原查询并降级到基线检索；语义漂移、实体丢失和错误路由必须可检测。

## 三、实际开发中的位置和使用方式

在线入口接收：

```text
QueryRequest { request_id, user_query, history, tenant_id,
               locale, current_time, user_acl, latency_budget }
QueryPlan { normalized_query, intent, confidence, filters,
            rewrite_queries[], route, fallback, trace_id }
```

先记录原始查询和模型版本，再按低成本规则做安全规范化；需要时调用分类或改写模型。改写结果必须通过实体/数字/时间校验和长度上限，低置信度保留原查询。多查询、HyDE、分解和 Step-back 采用可配置预算，超过延迟或调用次数自动回退。路由在执行前注入租户和权限过滤，禁止由模型自行提升访问范围。

评估使用标注意图、独立查询、过滤字段和目标知识源的数据集，比较分类准确率、拒识率、改写后 Recall@K、实体保真率、路由准确率、延迟和成本。影子流量可检验线上分布，失败样本按“理解、改写、过滤、路由”首个错误阶段归因。

## 四、具体技术或框架实现

- LangChain `MultiQueryRetriever`、LlamaIndex Router/Query Fusion 可实现多查询和路由组合；每个子查询保留父请求和 trace ID。
- Azure semantic query rewrite、Cohere parallel query 等登记能力可用于改写或并行扩展，版本和配额需复核。
- HyDE、Step-back、ReAct/IRCOT 等方法通过提示模板产生中间查询；必须限制中间文本只用于检索，不直接作为事实答案。
- 结构化过滤可由 Pydantic/JSON Schema 校验；实体和时间字段在进入检索器前做类型、范围和租户权限验证。
- 对 `RAG-07-011` 设计漂移检测：比较原始/改写的关键实体、数值、时间和语言，失败时回退原查询并记录样本。

### 完整性检查：对比、关系、错误与评估

规则规范化（Rule-based Normalization）、模型改写（Model Rewrite）和多查询扩展（Multi-query Expansion）分别在成本、覆盖和漂移风险上取舍；它们通过 `raw_query → intent/filters → rewrite_set → route → retrieval` 关系链衔接，不把改写文本当作答案证据。典型错误是实体或数字丢失、语言识别错误、过滤条件越权和改写循环；评估按意图准确率、拒识率、实体保真率、改写后 Recall@K、路由准确率、延迟和成本分层验证。

## 相关工程问题/面试题

- [`PQ-RAG-0014`](../../../interview/rag/stages/query-understanding.md#pq-rag-0014)
- [`PQ-RAG-0015`](../../../interview/rag/stages/query-understanding.md#pq-rag-0015)
- [`PQ-RAG-0016`](../../../interview/rag/stages/query-understanding.md#pq-rag-0016)

## 图谱与来源边界

覆盖 `RAG-07-001` 至 `RAG-07-012`（12/12）。除 `RAG-07-001` 外，其余原子均有图谱来源支持；`RAG-07-011` 虽有来源但仍需按失败样本验证具体约束。来源包括 HyDE、QReCC、Rewrite-Retrieve-Read、Step-back、Self-RAG、Adaptive/Modular RAG、Azure/Cohere/LlamaIndex 文档和已登记问题材料。本章不把无来源原子升级为正式事实。

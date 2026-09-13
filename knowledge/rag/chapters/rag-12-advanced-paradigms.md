---
id: RAG-12
title: 高级检索增强生成范式
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: mixed
chapter_path: knowledge/rag/chapters/rag-12-advanced-paradigms.md
atoms: [RAG-12-001, RAG-12-002, RAG-12-003, RAG-12-004, RAG-12-005, RAG-12-006, RAG-12-007, RAG-12-008, RAG-12-009, RAG-12-010, RAG-12-011, RAG-12-012, RAG-12-013, RAG-12-014, RAG-12-015, RAG-12-016, RAG-12-017, RAG-12-018, RAG-12-019, RAG-12-020]
related_problem_ids: [PQ-RAG-0005, PQ-RAG-0011, PQ-RAG-0016, PQ-RAG-0026]
---

# 高级检索增强生成范式

> 本章状态：`formal_bounded`（范围受限正式，已通过当前登记范围严格验收）。高级范式是对基线检索增强生成（Retrieval-Augmented Generation，RAG）链路的重组或控制策略；其适用性必须由业务评估和安全约束证明。

## 一、知识点概要

朴素检索增强生成（Naive RAG）是“切分、嵌入、检索、拼接、生成”的基线，易实现但对复杂问题、长文档、冲突和多跳关系支持有限（`RAG-12-001`）。高级检索增强生成（Advanced RAG）通过查询改写、混合检索、重排、压缩和验证改进质量；模块化检索增强生成（Modular RAG）把这些能力组合为可替换组件（`RAG-12-002`、`RAG-12-003`）。

智能体检索增强生成（Agentic RAG）、自适应检索（Adaptive Retrieval）、自反思检索增强生成（Self-RAG）、纠错检索增强生成（Corrective RAG，CRAG）和迭代检索（Iterative Retrieval）增加动态决策与反馈（`RAG-12-004` 至 `RAG-12-008`）。图检索增强生成（GraphRAG）、多模态检索增强生成（Multimodal RAG）、Agentic Search 和 Deep Research 扩展知识结构、模态和任务规划（`RAG-12-009` 至 `RAG-12-017`）。

## 二、技术原理

### 2.1 从基线到动态控制

高级范式不改变证据边界：每次动态检索仍须遵守权限、版本、引用和拒答策略。模块化架构将 `router`、`retriever`、`reranker`、`context_builder`、`verifier` 暴露为稳定接口，路由可按问题类型、置信度、成本和时延选择一个或多个模块（`RAG-12-002`、`RAG-12-003`）。

智能体检索增强生成把检索、工具调用、规划和观察结果放入循环。自适应检索先判断是否需要外部证据；Self-RAG 通过检索/批评标记控制是否取证和是否继续；CRAG 对检索质量评分，低质量时重写查询、补充来源或回退。多步和迭代检索将复杂问题分解为子问题，设置最大步数、预算和提前停止条件，避免循环和成本失控（`RAG-12-004` 至 `RAG-12-008`）。

### 2.2 图、向量和多模态

GraphRAG 先抽取实体、关系和社区摘要，再按局部实体问题或全局主题问题检索；图索引与向量检索可组合，图用于关系和跨文档路径，向量用于语义相似度（`RAG-12-009`、`RAG-12-010`）。Local、Global、DRIFT 等搜索模式是不同的查询粒度和迭代策略，不应混为单一“图检索”指标（`RAG-12-020`）。

多模态 RAG 同时处理文本、表格、图像、版面和视觉表示。解析阶段保留元素关系，索引阶段按模态路由，检索阶段融合不同分数，生成阶段回传原始视觉证据。视觉文档检索（Visual Document Retrieval）和 Late Interaction 允许细粒度匹配，但成本、坐标引用和跨模态校准需要专项评估（`RAG-12-011`、`RAG-12-012`）。

### 2.3 搜索规划与停止

Agentic Search 相比传统搜索或一次性 RAG，具有工具选择、查询重写、结果观察和多步停止；它不应在无必要时取代低成本直接检索（`RAG-12-013`）。Deep Research 将任务分解、搜索规划、来源交叉验证和中间证据组织为可审计轨迹（`RAG-12-014`、`RAG-12-015`、`RAG-12-017`）。

信息饱和（Information Saturation）不是“搜得越多越好”。按新增证据率、来源多样性、冲突未决数、时间预算和边际质量设停止条件；达到预算或证据充分后停止，保留未验证假设（`RAG-12-016`）。高级 RAG 的成本、风险和适用边界包括额外模型调用、提示注入面、工具权限、循环延迟、复杂评估和难以重放（`RAG-12-018`）。

### 2.4 范式分类维度

RAG 范式可按检索时机（静态/自适应）、控制者（固定流水线/模块路由/智能体）、知识结构（向量/倒排/图/多模态）、步骤数（单步/多步）和验证方式（无验证/自反思/外部核查）分类（`RAG-12-019`）。分类用于选择与评估，不代表复杂范式必然优于基线。

### 2.5 方案对比与关系（Comparison and Relations）

下表把原子知识点放在同一决策坐标中；它是选择依据，不是“高级”标签的排序：

| 路线 | 控制方式 | 主要证据结构 | 适合的任务形态 | 与其他路线的关系 |
|---|---|---|---|---|
| Naive RAG（`RAG-12-001`） | 固定单步 | 向量或稀疏候选 | 简单、低延迟事实问答 | 作为所有改进的基线 |
| Advanced/Modular RAG（`RAG-12-002`、`RAG-12-003`） | 规则或路由组合 | 多通道候选与重排 | 明确的召回、排序或上下文失败 | 可组合 Adaptive、CRAG 和多模态模块 |
| Agentic/Self/Corrective RAG（`RAG-12-004` 至 `RAG-12-008`） | 动态循环与反思 | 步骤级证据和状态 | 多跳、低置信度或需要工具的请求 | 共享同一检索器，但增加预算和停止门 |
| GraphRAG/知识图谱组合（`RAG-12-009`、`RAG-12-010`、`RAG-12-020`） | 图结构查询与向量召回 | 实体、关系、社区摘要 | 关系、多跳或全局主题问题 | 图检索与向量检索互补，不互相替代 |
| Multimodal/视觉检索（`RAG-12-011`、`RAG-12-012`） | 按模态路由和融合 | 文本、版面、图像表示 | 表格、图表、扫描件和视觉文档 | 依赖解析、坐标和跨模态校准 |
| Agentic Search/Deep Research（`RAG-12-013` 至 `RAG-12-017`） | 任务规划、工具和交叉验证 | 可回放的中间证据 | 长任务、多源和需要研究轨迹的请求 | 可把任意 RAG 检索器作为工具 |

因此，`RAG-12-019` 的分类维度与 `RAG-12-018` 的成本/风险边界共同决定路由；`RAG-12-020` 的 Local、Global、DRIFT 和基础模式是 GraphRAG 内的查询模式，而不是四套互斥产品。

### 2.6 错误模式与恢复（Failure Modes and Recovery）

| 现象 | 首要检查 | 保守恢复动作 | 不能直接推断 |
|---|---|---|---|
| 路由反复循环或步数爆炸 | `trace_id`、步数、预算和停止原因 | 限制最大步数，保留中间证据并回退到单步检索 | 不能仅凭“模型很强”扩大预算 |
| Adaptive/Self-RAG 跳过必要检索 | 置信度校准、拒答样本和权限过滤 | 对高风险领域强制检索，低置信度转 CRAG 或人工队列 | “无需检索”不是默认正确 |
| CRAG 评分高但答案错误 | 评分器与黄金样本的一致性、候选集覆盖 | 重写查询、增加独立通道并触发端到端验证 | 评分器分数不等于答案正确 |
| GraphRAG 路径爆炸或社区摘要失真 | 实体链接、关系去重、社区版本和剪枝 | 限制 hop/分支、语义剪枝并回退向量检索 | 图规模增加不必然提高召回 |
| 多模态引用错位 | 页码、坐标、元素 ID 和模态分数校准 | 保留原始元素，降低融合权重或转人工核验 | OCR 文本不能替代视觉证据 |
| Deep Research 证据冲突或未饱和 | 来源版本、冲突数、边际新增率和预算 | 显示分歧与未验证假设，达到停止条件后结束 | 搜索次数不是证据质量 |

### 2.7 评估方法（Evaluation）

高级范式必须与 `RAG-10` 的基线在同一问题分层、索引快照和权限策略下比较。离线至少记录：检索召回率（Recall@K）、首个相关结果排名（MRR）、答案正确性（Answer Correctness）、事实依据性（Groundedness）、引用准确率（Citation Accuracy）、P95/P99 延迟、每请求 Token 成本和拒答率。多步路线额外记录平均步数、提前停止率、工具调用成功率、证据新增率和循环率（`RAG-12-004` 至 `RAG-12-018`）。

评估应按范式做消融（Ablation）：固定生成器只替换路由，固定候选集只替换重排或图扩展，固定预算再比较质量；对 GraphRAG 分开报告 Local、Global、DRIFT 和基础搜索模式，对多模态分开报告文本、版面和图像命中。线上采用影子流量（Shadow Traffic）和灰度发布（Canary Release），以成本、延迟和安全事件作为护栏，避免把单一离线分数当作升级依据。

## 三、实际开发中的位置和使用方式

先以朴素 RAG 建立可测基线，再针对明确失败类型引入一个高级能力。低风险事实问答优先单步检索；需要多跳关系时增加图检索或迭代；复杂研究任务才启用规划和工具。每个动态步骤携带 `trace_id`、证据 ID、预算、工具权限和停止原因，结果写入可回放轨迹。

路由门禁应同时检查置信度、用户权限、数据新鲜度和成本；工具调用使用最小权限并对高风险动作人工确认。高级模式的离线评估必须与 Naive RAG 使用相同数据集、索引快照和端到端指标，线上以影子流量和灰度发布验证收益。

## 四、具体技术或框架实现

可用统一控制接口承载多种范式：

```python
plan = router.plan(query, budget=budget, policy=policy)
for step in plan.steps:
    evidence = retrieve(step.query, mode=step.mode)
    if verifier.sufficient(evidence, step.goal):
        break
answer = generator.generate(context_builder.build(evidence))
```

LlamaIndex Router、LangChain 检索器组合、Microsoft GraphRAG 等官方组件可作为适配器；ColPali 等视觉模型用于视觉文档检索；OpenAI Deep Research 系统卡和 Agentic RAG 研究用于规划边界参考。组件版本、工具权限、图构建成本和多模态模型能力必须以登记来源和本地回归为准，不把示例代码当成生产默认配置。

实现边界可按以下接口审计：`router.plan` 只产生带预算的计划，`retrieve` 返回带来源版本和权限结果的证据，`verifier.sufficient` 只能依据已登记证据判断是否停止，`context_builder.build` 不得丢失原始证据 ID。每个模块都应能单独重放和替换；否则无法把质量变化归因到某一高级能力（`RAG-12-003`、`RAG-12-016`、`RAG-12-017`）。

## 相关工程问题/面试题

- [PQ-RAG-0005：多跳子图与路径剪枝](../../../interview/rag/stages/advanced-rag.md#pq-rag-0005)
- [PQ-RAG-0011：多模态文档检索与引用](../../../interview/rag/stages/advanced-rag.md#pq-rag-0011)
- [PQ-RAG-0016：检索、工具和多步路由](../../../interview/rag/stages/query-routing.md#pq-rag-0016)
- [PQ-RAG-0026：Agentic RAG 工具安全](../../../interview/rag/stages/production-governance.md#pq-rag-0026)

## 相关知识节点

`RAG-07` 和 `RAG-08` 提供查询与检索基线，`RAG-09` 提供上下文和验证，`RAG-10` 负责公平比较，`RAG-11` 约束权限、安全、成本和可观测性。

## 来源、版本与审核状态

主要来源包括 `SRC-ADAPTIVE-RAG-2024`、`SRC-SELF-RAG-2023`、`SRC-CORRECTIVE-RAG-2024`、`SRC-IRCOT-2023`、`SRC-MODULAR-RAG-2024`、`SRC-GRAPHRAG-LOCAL-GLOBAL-2024`、`SRC-MICROSOFT-GRAPHRAG-DOCS`、`SRC-COLPALI-2024`、`SRC-OPENAI-DEEP-RESEARCH-SYSTEM-CARD-2025`、`SRC-AGENTIC-RAG-SURVEY-2025` 和已登记官方框架文档。研究论文证明方法和实验边界，面经与题库只提供问题场景。高级范式、云组件和模型接口属于高变化内容，需按登记版本复核。

原子—来源覆盖抽查（Atom-to-Source Coverage）：`RAG-12-001`→`SRC-AGENT-GUIDE`；`RAG-12-002`→`SRC-AGENT-GUIDE`；`RAG-12-003`→`SRC-MODULAR-RAG-2024`；`RAG-12-004`→`SRC-AGENTIC-RAG-SURVEY-2025`；`RAG-12-005`→`SRC-ADAPTIVE-RAG-2024`；`RAG-12-006`→`SRC-SELF-RAG-2023`；`RAG-12-007`→`SRC-CORRECTIVE-RAG-2024`；`RAG-12-008`→`SRC-IRCOT-2023`；`RAG-12-009`→`SRC-GRAPHRAG-LOCAL-GLOBAL-2024`；`RAG-12-010`→`SRC-GRAPHRAG-LOCAL-GLOBAL-2024`；`RAG-12-011`→`SRC-COLPALI-2024`；`RAG-12-012`→`SRC-COLPALI-2024`；`RAG-12-013`→`SRC-OPENAI-DEEP-RESEARCH-SYSTEM-CARD-2025`；`RAG-12-014`→`SRC-OPENAI-DEEP-RESEARCH-SYSTEM-CARD-2025`；`RAG-12-015`→`SRC-AGENT-GUIDE`；`RAG-12-016`→`SRC-ENTERPRISE-DEEP-RESEARCH-TERMINATION-2026`；`RAG-12-017`→`SRC-ATBENCH-AGENT-TRAJECTORY-SAFETY-2026`；`RAG-12-018`→`SRC-ADAPTIVE-RAG-2024`；`RAG-12-019`→`SRC-REALM-2020`；`RAG-12-020`→`SRC-MICROSOFT-GRAPHRAG-DOCS`。该抽查只证明图谱已有来源映射，不扩大单个来源的结论边界。本章覆盖 20 个原子。

---
id: RAG-01
title: RAG 基础、价值与能力边界
status: formal_candidate
reviewed_at: 2026-09-04
freshness_class: stable
chapter_path: knowledge/rag/chapters/rag-01-foundations.md
atoms:
  - RAG-01-001
  - RAG-01-002
  - RAG-01-003
  - RAG-01-004
  - RAG-01-005
  - RAG-01-006
  - RAG-01-007
  - RAG-01-008
  - RAG-01-009
  - RAG-01-010
related_problem_ids:
  - PQ-RAG-0008
  - PQ-RAG-0016
  - PQ-RAG-0020
  - PQ-RAG-0021
  - PQ-RAG-0023
  - PQ-RAG-0024
---

# RAG 基础、价值与能力边界

> 章节状态：`formal_candidate`（正式候选，待全库验收）。本章只整理已登记来源和图谱原子，不把问题库存当作答案，也不宣称检索增强生成（Retrieval-Augmented Generation，RAG）全库完成。

## 一、知识点概要

检索增强生成（Retrieval-Augmented Generation，RAG）是在生成阶段读取模型参数之外的外部知识，并让生成模型依据检索证据回答问题。它把参数记忆（Parametric Memory）与非参数记忆（Non-parametric Memory）连接起来：前者提供语言和推理能力，后者提供可更新、可撤回、可定位的文档、记录、知识图谱或工具结果。

一个最小的检索增强生成（RAG）闭环包括知识源、知识处理、检索器（Retriever）、上下文组装（Context Assembly）、生成器（Generator）和来源标识。生产系统通常还需要查询理解（Query Understanding）、查询改写（Query Rewrite）、权限过滤、重排（Reranking）、拒答（Abstention）、引用（Citation）、评估（Evaluation）和索引版本管理；这些能力不是定义的必要条件，却决定了系统是否可审计、可排障和可持续更新。

本章覆盖图谱中的 10 个知识原子：定义与目标（`RAG-01-001`）、知识截止与更新（`RAG-01-002`）、企业私域知识与审计（`RAG-01-003`）、幻觉缓解边界（`RAG-01-004`）、与微调（Fine-tuning）的选型（`RAG-01-005`）、与长上下文（Long Context）的选型（`RAG-01-006`）、与传统搜索（Traditional Search）的关系（`RAG-01-007`）、与模型记忆和上下文工程（Context Engineering）的关系（`RAG-01-008`）、适用条件（`RAG-01-009`）以及收益有限场景（`RAG-01-010`）。完整关系图见 [`RAG-01 基础与边界`](../../../learning/rag/maps/rag-01.md)。

## 二、技术原理

### 2.1 参数记忆（Parametric Memory）与外部证据（`RAG-01-001`）

Lewis 等人的原始检索增强生成（RAG）模型将预训练序列到序列模型作为参数记忆（Parametric Memory），将可访问的 Wikipedia 稠密向量索引作为非参数记忆（Non-parametric Memory）。给定问题 $x$、检索文档 $z$ 和答案 $y$，论文形式可表示为：

$$p(y\mid x)=\sum_{z\in\operatorname{TopK}(x)}p_{\eta}(z\mid x)\,p_{\theta}(y\mid x,z)$$

其中 $p_{\eta}(z\mid x)$ 表示检索器相关性分布，$p_{\theta}(y\mid x,z)$ 表示生成器在证据条件下的输出分布。工程中的广义检索增强生成（RAG）不要求检索器和生成器联合训练，也不要求显式计算边缘概率；只要推理时选取外部证据并用它约束答案，通常都属于检索增强生成（RAG）系统。

系统质量至少包含四个相互牵制的目标：可获得性（能否找到所需事实）、可利用性（模型是否正确使用证据）、可更新性（变更能否按约定生效）和可追溯性（答案能否回到来源和版本）。最终文字流畅不等于四项目标都达成。

### 2.2 为什么需要外部知识（`RAG-01-002`）

模型训练存在知识截止（Knowledge Cutoff），部署后发生的政策、价格、库存、组织文档和研究进展不会自动写入参数。企业手册、工单、合同和个人资料等私域知识（Private Knowledge）通常不在通用训练集内，不能因模型具有领域语言能力就推断其知道具体内容。

外部知识可按文档或记录更新、撤回、设置有效期并重新索引，比定向修改模型参数更容易隔离影响和证明变更。但“索引可更新”不等于答案立即新鲜：变更检测、重新解析、向量嵌入（Embedding）、索引发布、缓存失效或在线路由的任一步延迟，都会使旧内容继续被返回。

### 2.3 私域、安全与可审计性（`RAG-01-003`）

私域接入必须把权限控制（Access Control）放在检索链路内，而不是只在提示词（Prompt）中要求模型保密。摄取时记录租户、所有者、访问控制列表（Access Control List，ACL）、敏感等级、有效期和删除状态；检索前由已验证身份生成过滤条件；检索后再次校验每个证据的权限。答案至少保留 `source_id`、`document_id`、`chunk_id`、文档版本、索引版本和追踪标识（Trace ID），以便复现。

数据不写入模型参数并不代表零泄露。解析服务、向量嵌入（Embedding）服务、向量数据库（Vector Database）、模型应用程序编程接口（Application Programming Interface，API）、缓存和日志都可能接触内容；托管与自部署方案应按传输、留存、训练使用和删除能力逐项核验。日志和评估样本还要遵守脱敏（Redaction）与留存期限。

### 2.4 幻觉缓解而非消除（`RAG-01-004`）

检索证据、来源引用和证据不足时拒答可以减少模型仅凭参数记忆（Parametric Memory）补全事实的机会，但端到端正确性仍受知识存在、解析正确、召回相关、排序保留和模型忠实使用共同影响。可用下式作为故障归因框架，而不是统计独立性的真实概率：

$$P(\text{正确且有依据})\approx P(\text{知识存在})\times P(\text{解析正确})\times P(\text{召回相关})\times P(\text{排序保留})\times P(\text{模型忠实使用})$$

典型失败包括知识缺失或过期、光学字符识别（Optical Character Recognition，OCR）和表格解析破坏语义、查询（Query）与文档表达不一致、正确证据被重排或上下文预算截断、来源互相冲突或含间接提示注入（Indirect Prompt Injection），以及模型生成未被证据支持的细节。因此检索增强生成（RAG）提高的是可干预性和可观测性，不是事实保证；仍需分层评估、拒答、引用验证和生成后核查。

### 2.5 与相邻方案的边界（`RAG-01-005` 至 `RAG-01-008`）

| 方案 | 主要改变 | 更适合解决 | 与 RAG 的关系 |
|---|---|---|---|
| 检索增强生成（RAG） | 推理时选择外部证据 | 可变、私域、需引用的事实 | 可与其他方案组合 |
| 微调（Fine-tuning） | 更新模型参数或行为 | 稳定的风格、格式和任务能力 | 可改变生成行为，不能替代可追溯知识通道 |
| 长上下文（Long Context） | 一次接收更多词元（Token） | 文档量可控、需要整体阅读 | 可先检索候选，再将少量原文放入长上下文 |
| 传统搜索（Traditional Search） | 返回文档或排序列表 | 精确术语、编号和导航 | 与稠密检索（Dense Retrieval）共用索引、排序和相关性评估基础 |
| 模型记忆与上下文工程（Context Engineering） | 管理短期、长期、工具和状态信息 | 决定模型每一步看到什么 | RAG 是外部记忆读取和上下文工程的一种实现 |

微调（Fine-tuning）与检索增强生成（RAG）的“怎么说/说什么”比喻仅是入门近似；两者都可能影响事实和表达，应按目标变量、更新频率、追溯要求和维护成本选型。长上下文（Long Context）也没有跨模型、跨任务的统一优胜方案；LaRA 基准（Benchmark）和中间信息丢失（Lost in the Middle）研究都支持在自有任务集上比较，而不能只看标称上下文窗口。传统搜索（Traditional Search）擅长精确匹配，稠密检索（Dense Retrieval）擅长语义近似，混合检索（Hybrid Search）常用于同时覆盖两类需求，但生成层还会引入断言级引用和忠实度（Faithfulness）问题。

### 2.6 适用性边界（`RAG-01-009`、`RAG-01-010`）

当答案依赖训练后或频繁变化的信息、企业或个人私域资料、来源与版本、按用户隔离的知识子集，且证据可被定位和评估时，检索增强生成（RAG）的预期价值较高。内部制度问答、技术文档辅助、客服知识辅助和带来源研究分析属于这类任务。

当任务主要是稳定通用能力或创意闲聊、语料极少且可稳定放入提示、无法提供可靠证据、要求极低延迟、授权和数据驻留无法满足，或问题需要对全体材料做精确计算而前 K 个结果（Top-K Results）会丢失长尾信息时，纯检索增强生成（RAG）收益可能有限。可考虑结构化查询、规则引擎、数据库计算、直接长上下文（Long Context）、微调（Fine-tuning）或组合方案；“不适合纯 RAG”不等于禁止所有检索。

## 三、实际开发位置和使用方式

### 3.1 在系统链路中的位置

离线知识构建通常依次经过数据摄取（Data Ingestion）、文档解析（Document Parsing）、数据治理（Data Governance）、文本切分（Chunking）、向量嵌入（Embedding）和存储与索引（Storage and Indexing）；在线请求经过查询理解（Query Understanding）、查询改写（Query Rewrite）、查询路由（Query Routing）、检索（Retrieval）、结果融合（Result Fusion）、重排（Reranking）、上下文组装（Context Assembly）、答案生成（Answer Generation）以及引用与验证（Citation and Verification）。本章定义和边界决定这些阶段何时值得引入、应保留哪些审计字段以及如何解释失败。

### 3.2 输入、证据和答案契约

```text
QueryRequest
  request_id, tenant_id, user_id, query, conversation_context,
  filters, locale, current_time

Evidence
  chunk_id, document_id, source_id, document_version, index_version,
  text_or_payload, retrieval_score, rerank_score, acl, valid_time

Answer
  request_id, text, citations[], confidence_or_abstention,
  model_version, prompt_version, index_version, trace_id
```

上述字段把“能回答”变成“能排障”：出现错误答案时，可以重放查询、索引、证据排序、提示版本和模型版本。敏感文本不应无条件写入日志，可按权限保存标识、哈希、脱敏片段或受控采样。

### 3.3 最小可验证闭环

先从真实任务抽取有代表性问题，标注可接受答案及直接证据；再分别评估知识覆盖、解析、检索、重排、生成忠实度和引用。每次调整文本切分（Chunking）、向量嵌入（Embedding）、前 K 个结果（Top-K Results）参数、重排器（Reranker）或提示词（Prompt）后运行回归测试（Regression Test），并记录首次失败阶段。只有端到端收益超过延迟、词元（Token）成本和维护代价，才扩大使用范围。

## 四、具体技术或框架实现

### 4.1 原始模型与研究实现

- `SRC-RAG-ORIGINAL-2020`：Lewis 等人的 RAG 原始论文，支持参数记忆（Parametric Memory）、非参数记忆（Non-parametric Memory）和论文模型形式。
- `SRC-REALM-2020`：REALM 论文，支持检索增强语言模型和外部非参数记忆（Non-parametric Memory）的历史背景。

这些论文定义的是研究模型，不等同于生产组件清单；生产实现仍需把解析、索引、权限、引用和评估拆成可替换模块。

### 4.2 检索、上下文和评估组件的实现边界

实现可以使用稀疏检索（Sparse Retrieval）、稠密检索（Dense Retrieval）、混合检索（Hybrid Search）、结构化查询或知识图谱（Knowledge Graph），再按候选规模接入重排器（Reranker）。向量数据库（Vector Database）只是存储和索引能力，不能代替查询路由（Query Routing）、上下文组装（Context Assembly）或引用验证（Citation Verification）。具体框架、模型和接口必须在对应流程节点按固定版本登记；本章不把未登记产品能力写成稳定事实。

### 4.3 与长上下文的实验实现

使用 `SRC-LARA-RAG-LONG-CONTEXT-2025` 和 `SRC-LOST-IN-THE-MIDDLE-2023` 作为研究证据，构造同一问题集的 RAG、直接长上下文（Long Context）和混合路由对照。固定答案标注、证据标注、模型版本、上下文长度和成本口径，分别记录召回、答案正确性、忠实度、引用和延迟；不以单个模型或公开基准推导所有业务的统一结论。

### 4.4 已登记来源的工程化使用边界

`SRC-AI-AGENT-INTERVIEW-GUIDE`、`SRC-AGENT-GUIDE` 和 `SRC-XIAOLIN-AI-LEARNING` 用于定义、流程、业务动机和相邻方案导航；用户 PDF `SRC-USER-RAG-EXPERIENCE-PDF` 仅保留页级定位和本项目自己的归纳，不能当作公开许可全文或唯一技术主证据。所有实现参数、产品行为和性能结论应回到对应官方文档、官方仓库或原始论文。

## 相关工程问题/面试题

以下链接指向当前 `inventory-only`（仅库存）问题页。它们通过跨节点场景帮助定位本章边界，不表示图谱已经为 `RAG-01` 原子建立 `problem_at` 边，也不提供正式答案：

- [`PQ-RAG-0008`：生产部署的分层定位与治理](../../../interview/rag/cross-stage-problem-inventory.md#pq-rag-0008)
- [`PQ-RAG-0016`：无需检索、单次检索、多次检索与外部工具路由](../../../interview/rag/cross-stage-problem-inventory.md#pq-rag-0016)
- [`PQ-RAG-0020`：长上下文位置、Token 预算与证据保留](../../../interview/rag/cross-stage-problem-inventory.md#pq-rag-0020)
- [`PQ-RAG-0021`：解析、召回、生成和引用的分层评估](../../../interview/rag/stages/evaluation.md#pq-rag-0021)
- [`PQ-RAG-0023`：零召回、低相关、证据不足与拒答](../../../interview/rag/cross-stage-problem-inventory.md#pq-rag-0023)
- [`PQ-RAG-0024`：多来源事实、时间和观点冲突](../../../interview/rag/cross-stage-problem-inventory.md#pq-rag-0024)

## 图谱与来源记录

### 图谱节点

本章原子和状态以 [`knowledge/rag/graph.json`](../graph.json) 为准：`RAG-01-001` 至 `RAG-01-010` 均为 `knowledge` 节点，当前状态为 `source_mapped`，审核日期为 2026-09-04。章节关系图见 [`learning/rag/maps/rag-01.md`](../../../learning/rag/maps/rag-01.md)。

### 来源登记

| 来源 ID | 类型与定位 | 本章用途 |
|---|---|---|
| `SRC-RAG-ORIGINAL-2020` | 原始论文（Primary Paper），[arXiv:2005.11401](https://arxiv.org/abs/2005.11401)，2020 | 狭义 RAG 定义、记忆划分和模型形式 |
| `SRC-REALM-2020` | 原始论文（Primary Paper），[arXiv:2002.08909](https://arxiv.org/abs/2002.08909)，2020 | 外部非参数记忆（Non-parametric Memory）历史背景 |
| `SRC-LARA-RAG-LONG-CONTEXT-2025` | 原始论文（Primary Paper），[arXiv:2502.09977](https://arxiv.org/abs/2502.09977) v2，2025-03-05 | RAG 与长上下文比较边界 |
| `SRC-LOST-IN-THE-MIDDLE-2023` | 原始论文（Primary Paper），[arXiv:2307.03172](https://arxiv.org/abs/2307.03172) v3，2023-11-20 | 长上下文位置效应 |
| `SRC-AGENT-GUIDE` | 已纳管学习来源（Curated Learning Source），[AgentGuide](https://github.com/adongwanai/AgentGuide)，审核日期以来源登记为准 | 流程、搜索和上下文工程导航 |
| `SRC-AI-AGENT-INTERVIEW-GUIDE` | 已纳管学习来源（Curated Learning Source），[AI Agent Interview Guide](https://github.com/bcefghj/ai-agent-interview-guide)，审核日期以来源登记为准 | 定义、业务动机和选型导航 |
| `SRC-XIAOLIN-AI-LEARNING` | 已纳管学习来源（Curated Learning Source），[xiaolin-ai-learning](https://github.com/SodaWWater/xiaolin-ai-learning)，审核日期以来源登记为准 | 知识截止、私域和幻觉边界导航 |
| `SRC-USER-RAG-EXPERIENCE-PDF` | 用户资料（User Material），《大模型 RAG 经验面》，页级定位已登记，公开许可未知 | 仅作补充归纳，不作唯一主证据 |

## 审核边界

- 本章覆盖 `RAG-01` 的 10 个目录原子，但节点仍为 `source_mapped`，章节仍为 `content_draft`，需统一人工验收后才能提升状态。
- 本章未添加新的来源、图谱节点或关系；未把 `RAG-07-011`、`RAG-13-011` 等 `inventory_draft` 节点当作已验证事实。
- 研究结论、框架接口、模型能力、成本和性能随版本变化；使用前应按来源登记的固定版本复核。

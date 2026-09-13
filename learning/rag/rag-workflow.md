# 完整检索增强生成（Retrieval-Augmented Generation，RAG）流程

> 状态：`accepted_bounded / WP-P4-001 / graph-first`
>
> 图谱基线：[`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)
>
> 边界：这是完整检索增强生成（Retrieval-Augmented Generation，RAG）流程的前置学习视图，不是知识章节（Knowledge Chapter）、工程问题/面试题（Engineering Problem / Interview Question）页面，也不替代来源覆盖审计（Source Coverage Audit）。

## 阅读目标

本页先给出一个检索增强生成（Retrieval-Augmented Generation，RAG）系统的端到端工作模型：离线知识构建（Offline Knowledge Construction）准备可检索的已发布索引；在线查询与回答（Online Query and Answering）处理一次用户问题；评估反馈（Evaluation and Feedback）把结果返回改进环；生产治理（Production Governance）为全生命周期提供运行边界。每个流程节点（Pipeline Stage）均以有向知识图谱（Directed Knowledge Graph）中的 ID 标识，可以回查到底层节点和受控关系。

本页只陈述当前图谱已登记的基线路径。技术细节、框架实现（Framework Implementation）、故障诊断和方案比较分别留给后续知识章节（Knowledge Chapter）与工程问题/面试题（Engineering Problem / Interview Question）产物。

## 全局运行模型

```text
离线知识构建（Offline Knowledge Construction）
数据摄取（Data Ingestion）
  -> 文档解析（Document Parsing）
  -> 数据治理（Data Governance）
  -> 文本切分（Chunking）
  -> 向量嵌入（Embedding）
  -> 存储与索引（Storage and Indexing）

在线查询与回答（Online Query and Answering）
用户问题（User Query）
  -> 查询理解（Query Understanding）
  -> 查询改写（Query Rewrite）
  -> 查询路由（Query Routing）
  -> 检索（Retrieval）
  -> 结果融合（Result Fusion）
  -> 重排（Reranking）
  -> 上下文组装（Context Assembly）
  -> 答案生成（Answer Generation）
  -> 引用与验证（Citation and Verification）

评估反馈（Evaluation and Feedback）
引用与验证（Citation and Verification） -> 评估（Evaluation）

生产治理（Production Governance）
评估（Evaluation） -> 生产治理（Production Governance） -> 高级检索增强生成（Advanced RAG）
```

以上箭头对应当前有向知识图谱（Directed Knowledge Graph）中的 `next_stage` 基线关系。它说明学习和默认处理顺序；它不把所有运行时条件压缩为单一路径。当前图谱尚未登记 `branches_to` 或 `merges_into` 关系，因此查询改写（Query Rewrite）、查询路由（Query Routing）、结果融合（Result Fusion）和高级检索增强生成（Advanced RAG）的条件分支只能在关系被明确建模后，才能由后续局部图（Local Node Map）展示。

## 离线知识构建（Offline Knowledge Construction）

离线知识构建（Offline Knowledge Construction）的目标是把可纳管的数据转换为可供在线检索（Retrieval）使用的索引版本。该主干在一次用户问题到来之前运行，其当前流程节点（Pipeline Stage）顺序如下。

| 顺序 | 流程节点（Pipeline Stage） | 图谱 ID | 基线衔接 |
|---:|---|---|---|
| 1 | 数据摄取（Data Ingestion） | `PS-DATA-INGESTION` | 进入文档解析（Document Parsing） |
| 2 | 文档解析（Document Parsing） | `PS-DOCUMENT-PARSING` | 进入数据治理（Data Governance） |
| 3 | 数据治理（Data Governance） | `PS-DATA-GOVERNANCE` | 进入文本切分（Chunking） |
| 4 | 文本切分（Chunking） | `PS-CHUNKING` | 进入向量嵌入（Embedding） |
| 5 | 向量嵌入（Embedding） | `PS-EMBEDDING` | 进入存储与索引（Storage and Indexing） |
| 6 | 存储与索引（Storage and Indexing） | `PS-STORAGE-INDEXING` | 为在线查询与回答（Online Query and Answering）提供已发布索引 |

离线知识构建（Offline Knowledge Construction）不是在线查询与回答（Online Query and Answering）的附属步骤：没有可用的存储与索引（Storage and Indexing），后续检索（Retrieval）没有可消费的索引对象。图谱中的 `NEXT-STAGE-PS-STORAGE-INDEXING-PS-QUERY-UNDERSTANDING` 记录了这一完整学习链路的衔接，不应理解为每次用户问题都会重新执行离线知识构建（Offline Knowledge Construction）。

## 在线查询与回答（Online Query and Answering）

在线查询与回答（Online Query and Answering）以用户问题（User Query）为输入，并消费离线知识构建（Offline Knowledge Construction）已发布的索引。当前基线先处理问题，再取得和整理证据，最后生成并核验答案。

| 顺序 | 流程节点（Pipeline Stage） | 图谱 ID | 在基线路径中的职责边界 |
|---:|---|---|---|
| 1 | 查询理解（Query Understanding） | `PS-QUERY-UNDERSTANDING` | 接收用户问题（User Query）并进入查询改写（Query Rewrite） |
| 2 | 查询改写（Query Rewrite） | `PS-QUERY-REWRITE` | 形成进入查询路由（Query Routing）的查询表达 |
| 3 | 查询路由（Query Routing） | `PS-QUERY-ROUTING` | 将查询交给检索（Retrieval）路径 |
| 4 | 检索（Retrieval） | `PS-RETRIEVAL` | 取得候选结果并进入结果融合（Result Fusion） |
| 5 | 结果融合（Result Fusion） | `PS-RESULT-FUSION` | 将候选结果交给重排（Reranking） |
| 6 | 重排（Reranking） | `PS-RERANKING` | 将有序候选交给上下文组装（Context Assembly） |
| 7 | 上下文组装（Context Assembly） | `PS-CONTEXT-ASSEMBLY` | 形成答案生成（Answer Generation）的上下文 |
| 8 | 答案生成（Answer Generation） | `PS-ANSWER-GENERATION` | 形成待核验答案并进入引用与验证（Citation and Verification） |
| 9 | 引用与验证（Citation and Verification） | `PS-CITATION-VERIFICATION` | 连接评估（Evaluation）反馈环 |

一次用户问题（User Query）的动态执行路径应以此基线开始阅读：先沿顺序追踪输入和下游输出。当前图谱只记录该顺序，并未把查询改写（Query Rewrite）、查询路由（Query Routing）与结果融合（Result Fusion）的条件分支登记为图边；在这些关系被建模前，本页不预设某个用户问题必然使用某项可选策略，也不将任一公开问题来源升级为技术结论。

## 评估反馈（Evaluation and Feedback）

评估反馈（Evaluation and Feedback）不等同于一次答案的末尾检查。它以引用与验证（Citation and Verification）的结果和运行反馈为入口，形成评估（Evaluation）后回到数据、策略或模型更新的闭环。当前有向知识图谱（Directed Knowledge Graph）把该闭环的评估位置聚合为以下流程节点（Pipeline Stage）。

| 流程节点（Pipeline Stage） | 图谱 ID | 当前图谱表达的边界 |
|---|---|---|
| 评估（Evaluation） | `PS-EVALUATION` | 接在引用与验证（Citation and Verification）之后，并进入生产治理（Production Governance） |

项目路线图（Project Roadmap）列出的用户反馈（User Feedback）、失败归因（Failure Attribution）、检索评估（Retrieval Evaluation）、生成评估（Generation Evaluation）、端到端评估（End-to-end Evaluation）以及数据、策略或模型更新（Data, Strategy or Model Update）是此反馈环的操作层次。它们尚未在当前图谱中分别登记为独立流程节点（Pipeline Stage），所以本页不为它们虚构节点 ID 或边。后续图视图只可使用图谱已存在的关系表达其落点。

## 生产治理（Production Governance）

生产治理（Production Governance）约束离线知识构建（Offline Knowledge Construction）、在线查询与回答（Online Query and Answering）和评估反馈（Evaluation and Feedback）的整个生命周期。当前基线的流程节点（Pipeline Stage）如下。

| 流程节点（Pipeline Stage） | 图谱 ID | 基线衔接 |
|---|---|---|
| 生产治理（Production Governance） | `PS-PRODUCTION-GOVERNANCE` | 承接评估（Evaluation），并进入高级检索增强生成（Advanced RAG） |
| 高级检索增强生成（Advanced RAG） | `PS-ADVANCED-RAG` | 表示在已知基线之上组织优化或可选处理路径 |

生产治理（Production Governance）在项目路线图（Project Roadmap）中覆盖权限控制（Access Control）、安全治理（Security Governance）、可观测性（Observability）、性能和成本（Performance and Cost）、版本发布（Version Release）与故障恢复（Failure Recovery）。这些治理维度属于跨主干约束；本页不把它们误写成当前图谱中的独立流程节点（Pipeline Stage）。

高级检索增强生成（Advanced RAG）也不是替代离线知识构建（Offline Knowledge Construction）或在线查询与回答（Online Query and Answering）的另一套无关流程。学习时应先掌握基线路径，再通过 `PS-ADVANCED-RAG` 回查图谱中的相关知识节点（Knowledge Node）和受控关系。

## 图谱回查与学习顺序

1. 先沿离线知识构建（Offline Knowledge Construction）的六个流程节点（Pipeline Stage）理解“索引为何存在”。
2. 再沿在线查询与回答（Online Query and Answering）的九个流程节点（Pipeline Stage）追踪一次用户问题（User Query）如何取得、整理和核验检索证据。
3. 返回评估反馈（Evaluation and Feedback），区分一次引用与验证（Citation and Verification）和跨周期的评估（Evaluation）改进闭环。
4. 最后把生产治理（Production Governance）作为所有主干的运行约束，并在已有基线明确后学习高级检索增强生成（Advanced RAG）。

图谱节点（Graph Node）回查入口：[`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)。本页涉及的 18 个流程节点（Pipeline Stage）为：`PS-DATA-INGESTION`、`PS-DOCUMENT-PARSING`、`PS-DATA-GOVERNANCE`、`PS-CHUNKING`、`PS-EMBEDDING`、`PS-STORAGE-INDEXING`、`PS-QUERY-UNDERSTANDING`、`PS-QUERY-REWRITE`、`PS-QUERY-ROUTING`、`PS-RETRIEVAL`、`PS-RESULT-FUSION`、`PS-RERANKING`、`PS-CONTEXT-ASSEMBLY`、`PS-ANSWER-GENERATION`、`PS-CITATION-VERIFICATION`、`PS-EVALUATION`、`PS-PRODUCTION-GOVERNANCE`、`PS-ADVANCED-RAG`。

## 当前范围与未决项

- 本前置学习产物只使用现有有向知识图谱（Directed Knowledge Graph）、术语表（Terminology Glossary）和项目路线图（Project Roadmap）；没有新增外部来源（External Source）。
- `RAG-07-001` 与 `RAG-13-011` 仍是没有来源引用的库存草稿知识节点（Inventory-draft Knowledge Node）。本页不把它们作为正式知识结论，也不视为已解决。
- 用户批准的不可访问 EUR-Lex 来源例外保持非证据性（Non-evidentiary）；本页不以其支持技术或法律结论。
- 图谱中尚未把评估反馈（Evaluation and Feedback）的每一个操作活动拆为独立流程节点（Pipeline Stage）。后续全局图（Global Metro Map）、主干图（Backbone Map）、重叠图（Overlap Map）、执行路径图（Execution Path Map）和局部图（Local Node Map）必须继续以当前图谱为唯一节点和关系来源。

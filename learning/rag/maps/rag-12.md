# RAG-12 高级范式：关系图

> 本图是由 `knowledge/rag/graph.json` 投影的学习视图。叶子节点只对应标准知识原子；图中不新增脱离图谱来源的技术结论。

## 图 1：范式原子覆盖

```mermaid
mindmap
  root(("RAG-12 高级范式"))
    基线与模块化
      RAG_12_001["RAG-12-001 Naive RAG 的流程和局限"]
      RAG_12_002["RAG-12-002 Advanced RAG 的查询、检索和生成优化"]
      RAG_12_003["RAG-12-003 Modular RAG 的组件化和路由"]
    动态检索与控制
      RAG_12_004["RAG-12-004 Agentic RAG 的动态决策闭环"]
      RAG_12_005["RAG-12-005 Adaptive Retrieval 与是否检索判断"]
      RAG_12_006["RAG-12-006 Self-RAG 的检索和反思控制"]
      RAG_12_007["RAG-12-007 CRAG 的检索评估和纠错"]
      RAG_12_008["RAG-12-008 Multi-Step 与 Iterative Retrieval"]
    图与多模态
      RAG_12_009["RAG-12-009 GraphRAG 的图构建、社区和全局检索"]
      RAG_12_010["RAG-12-010 知识图谱与向量检索的组合"]
      RAG_12_011["RAG-12-011 多模态 RAG 的解析、索引、路由和生成"]
      RAG_12_012["RAG-12-012 视觉文档检索与 Late Interaction"]
      RAG_12_020["RAG-12-020 GraphRAG 的 Local、Global、DRIFT 与基础搜索模式"]
    搜索规划与边界
      RAG_12_013["RAG-12-013 Agentic Search 与传统搜索、传统 RAG"]
      RAG_12_014["RAG-12-014 Deep Research 的任务分解和搜索规划"]
      RAG_12_015["RAG-12-015 Deep Research 的多源交叉验证"]
      RAG_12_016["RAG-12-016 信息饱和、搜索预算和停止条件"]
      RAG_12_017["RAG-12-017 长研究任务的中间证据和上下文组织"]
      RAG_12_018["RAG-12-018 高级 RAG 的成本、风险和适用边界"]
      RAG_12_019["RAG-12-019 RAG 范式的概念与分类维度"]
```

## 图 2：图谱中已登记的实现与问题关系

```mermaid
flowchart LR
  I1["IMP-RAG-0001 VectorRAG 与 FAISS 链路"] -->|implements| K9["RAG-12-009"]
  I1 -->|implements| K10["RAG-12-010"]
  I1 -->|implements| K20["RAG-12-020"]
  I4["IMP-RAG-0004 Unstructured 解析与切分策略"] -->|implements| K11["RAG-12-011"]
  P5["PQ-RAG-0005 多跳子图与路径剪枝"] -->|problem_at| K9
  P5 -->|problem_at| K10
  P5 -->|problem_at| K20
  P11["PQ-RAG-0011 多模态文档检索与引用"] -->|problem_at| K11
  P16["PQ-RAG-0016 检索、工具和多步路由"] -->|problem_at| K4["RAG-12-004"]
  P16 -->|problem_at| K5["RAG-12-005"]
  P16 -->|problem_at| K6["RAG-12-006"]
  P16 -->|problem_at| K7["RAG-12-007"]
  P26["PQ-RAG-0026 Agentic RAG 工具安全"] -->|problem_at| K4
  P26 -->|problem_at| K18["RAG-12-018"]
```

## 原子知识覆盖

| 原子 ID | 图中分组 | 图谱关系 |
|---|---|---|
| `RAG-12-001` 至 `RAG-12-003` | 基线与模块化 | `contains`（`PS-ADVANCED-RAG`） |
| `RAG-12-004` 至 `RAG-12-008` | 动态检索与控制 | `contains`；`problem_at`（`PQ-RAG-0016` 部分） |
| `RAG-12-009`、`RAG-12-010`、`RAG-12-020` | 图与多模态 | `implements`（`IMP-RAG-0001`）；`problem_at`（`PQ-RAG-0005`） |
| `RAG-12-011`、`RAG-12-012` | 图与多模态 | `implements`（`IMP-RAG-0004`）及 `problem_at`（`PQ-RAG-0011`） |
| `RAG-12-013` 至 `RAG-12-019` | 搜索规划与边界 | `contains`（`PS-ADVANCED-RAG`） |
| `RAG-12-020` | 图与多模态 | `implements`（`IMP-RAG-0001`）；`problem_at`（`PQ-RAG-0005`） |

覆盖：**20 / 20**。标准正文见 [`rag-12-advanced-paradigms.md`](../../../knowledge/rag/chapters/rag-12-advanced-paradigms.md)。


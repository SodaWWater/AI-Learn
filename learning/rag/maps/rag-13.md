# RAG-13 项目与面试应用：关系图

> 本图是由 `knowledge/rag/graph.json` 投影的学习视图。`RAG-13-011` 是无来源的 `inventory_draft` 原子，仅为覆盖登记，不构成正式结论。

## 图 1：项目与面试原子覆盖

```mermaid
mindmap
  root(("RAG-13 项目与面试应用"))
    方案表达与系统设计
      RAG_13_002["RAG-13-002 RAG 完整流程口述"]
      RAG_13_003["RAG-13-003 从零设计企业 RAG 系统"]
      RAG_13_004["RAG-13-004 Chunk、Embedding、向量库和 Reranker 选型表达"]
      RAG_13_006["RAG-13-006 RAG 框架、平台和开源项目选型"]
    实现、优化与排障
      RAG_13_005["RAG-13-005 检索优化方案和实验依据"]
      RAG_13_007["RAG-13-007 最小 RAG 与生产级代码结构"]
      RAG_13_008["RAG-13-008 无召回、噪声、幻觉和高延迟排障"]
      RAG_13_009["RAG-13-009 用指标证明 RAG 优化效果"]
    项目叙事与题目映射
      RAG_13_010["RAG-13-010 RAG 项目 STAR 叙事"]
      RAG_13_011["RAG-13-011 不同岗位的 RAG 回答深度（inventory_draft）"]
      RAG_13_012["RAG-13-012 原始面试题、追问与标准知识双向映射"]
```

## 图 2：图谱中已登记的实现与问题关系

```mermaid
flowchart LR
  I1["IMP-RAG-0001 VectorRAG 与 FAISS 链路"] -->|implements| K7["RAG-13-007"]
  P4["PQ-RAG-0004 VectorRAG 完整实现"] -->|problem_at| K7
  P5["PQ-RAG-0005 GraphRAG 多跳实现"] -->|problem_at| K7
  P6["PQ-RAG-0006 VectorRAG/GraphRAG 评估"] -->|problem_at| K9["RAG-13-009"]
```

## 原子知识覆盖

| 原子 ID | 图中分组 | 图谱关系与状态 |
|---|---|---|
| `RAG-13-002`、`RAG-13-003`、`RAG-13-004`、`RAG-13-006` | 方案表达与系统设计 | `contains`（`BB-RAG`） |
| `RAG-13-005`、`RAG-13-007`、`RAG-13-008`、`RAG-13-009` | 实现、优化与排障 | `contains`（`BB-RAG`）；`RAG-13-007` 有 `implements`/`problem_at`，`RAG-13-009` 有 `problem_at` |
| `RAG-13-010`、`RAG-13-012` | 项目叙事与题目映射 | `contains`（`BB-RAG`） |
| `RAG-13-011` | 项目叙事与题目映射 | `contains`（`BB-RAG`），状态 `inventory_draft`，无来源且未作为正文结论 |

覆盖：**11 / 11**（其中 1 个为待处置库存原子）。标准正文见 [`rag-13-project-interview.md`](../../../knowledge/rag/chapters/rag-13-project-interview.md)。


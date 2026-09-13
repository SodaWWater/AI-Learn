# RAG-08 检索、融合与重排（Retrieval, Fusion and Reranking）：关系图

```mermaid
flowchart TD
  Q["RAG-07 Query Plan"] --> D["RAG-08-001 Dense"]
  Q --> S["RAG-08-002 Sparse / RAG-08-003 BM25"]
  D --> H["RAG-08-004 Hybrid / RAG-08-005 多路"]
  S --> H
  H --> R["RAG-08-006 RRF / RAG-08-007 加权归一化"]
  R --> K["RAG-08-008 Top-K 与阈值"]
  K --> X["RAG-08-009 Bi-Encoder / Cross-Encoder"]
  X --> Y["RAG-08-010 Reranker"]
  Y --> Z["RAG-08-011 MMR / RAG-08-012 新鲜度"]
  Z --> M["RAG-08-013 多跳迭代"]
  M --> F["RAG-08-014 过滤可信来源"]
  F --> E["RAG-08-015 低相关恢复"]
  E --> L["RAG-08-016 延迟并发缓存"]
  L --> G["RAG-09 Context Assembly"]
```

## 原子覆盖

`RAG-08-001` 至 `RAG-08-016`，共 16/16；详细正文见 [`rag-08-retrieval-fusion-reranking.md`](../../../knowledge/rag/chapters/rag-08-retrieval-fusion-reranking.md)。各通道指标、过滤数量、重排耗时和索引版本需进入追踪。

逐项引用：`RAG-08-001`、`RAG-08-002`、`RAG-08-003`、`RAG-08-004`、`RAG-08-005`、`RAG-08-006`、`RAG-08-007`、`RAG-08-008`、`RAG-08-009`、`RAG-08-010`、`RAG-08-011`、`RAG-08-012`、`RAG-08-013`、`RAG-08-014`、`RAG-08-015`、`RAG-08-016`。

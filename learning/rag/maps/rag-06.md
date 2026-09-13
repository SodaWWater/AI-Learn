# RAG-06 存储与索引（Storage and Indexing）：关系图

```mermaid
flowchart TD
  E["RAG-05 Embedding"] --> A["RAG-06-001 向量库职责"]
  A --> B["RAG-06-002 精确 / ANN"]
  B --> C["RAG-06-003 / RAG-06-004 Schema 与 ID"]
  C --> D["RAG-06-005 HNSW / RAG-06-006 IVF / RAG-06-007 PQ"]
  C --> F["RAG-06-008 倒排 / RAG-06-009 共存"]
  D --> G["RAG-06-010 过滤顺序"]
  F --> G
  G --> H["06-011 选型"]
  H --> I["RAG-06-012 基准"]
  I --> J["RAG-06-013 分区分片副本"]
  J --> K["RAG-06-014 增删改与 Compaction"]
  K --> L["RAG-06-015 构建加载预热持久化"]
  L --> N["RAG-08 Retrieval"]
```

## 原子覆盖

`RAG-06-001` 至 `RAG-06-015`，共 15/15；详细正文见 [`rag-06-storage-indexing.md`](../../../knowledge/rag/chapters/rag-06-storage-indexing.md)。索引参数、过滤语义和产品能力需按固定版本复核。

逐项引用：`RAG-06-001`、`RAG-06-002`、`RAG-06-003`、`RAG-06-004`、`RAG-06-005`、`RAG-06-006`、`RAG-06-007`、`RAG-06-008`、`RAG-06-009`、`RAG-06-010`、`RAG-06-011`、`RAG-06-012`、`RAG-06-013`、`RAG-06-014`、`RAG-06-015`。

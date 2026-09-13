# RAG-07 查询理解（Query Understanding）：关系图

```mermaid
flowchart TD
  Q["原始 User Query"] --> A["RAG-07-001 清洗规范化（待来源验证）"]
  A --> B["RAG-07-002 意图与是否检索"]
  B --> C["RAG-07-003 Rewrite"]
  C --> D["RAG-07-004 Multi-Query / RAG-07-005 HyDE"]
  C --> E["RAG-07-006 分解 / RAG-07-007 Step-back"]
  B --> F["RAG-07-008 实体时间地域权限"]
  Q --> G["RAG-07-009 多轮独立问题"]
  B --> H["RAG-07-010 路由与知识源"]
  D --> I["RAG-07-011 漂移与失败约束"]
  E --> I
  F --> I
  H --> I
  I --> J["RAG-07-012 离线评估"]
  J --> R["RAG-08 Retrieval"]
```

## 原子覆盖

`RAG-07-001` 至 `RAG-07-012`，共 12/12；详细正文见 [`rag-07-query-understanding.md`](../../../knowledge/rag/chapters/rag-07-query-understanding.md)。`RAG-07-001` 无来源，图中明确标为待验证。

逐项引用：`RAG-07-001`、`RAG-07-002`、`RAG-07-003`、`RAG-07-004`、`RAG-07-005`、`RAG-07-006`、`RAG-07-007`、`RAG-07-008`、`RAG-07-009`、`RAG-07-010`、`RAG-07-011`、`RAG-07-012`。

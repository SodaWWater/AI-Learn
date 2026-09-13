# RAG-09 上下文与生成：关系图

```mermaid
flowchart TD
  Q["RAG-09-001 问题、证据与输出约束"] --> B["RAG-09-002 Token 预算"]
  B --> O["RAG-09-003 排序与位置"] --> L["RAG-09-004 Lost in the Middle"]
  O --> C["RAG-09-005 Contextual Compression"] --> G["RAG-09-006 Grounded Generation"]
  G --> V["RAG-09-010 事实核查"] --> CI["RAG-09-007 引用与追溯"]
  G --> A["RAG-09-008 拒答与不确定性"]
  G --> H["RAG-09-009 忠实度与事实依据性"]
  CI --> S["RAG-09-011 来源可信度"] --> X["RAG-09-013 冲突合并"]
  S --> F["RAG-09-012 事实/观点/推断"]
  G --> J["RAG-09-014 结构化输出"]
  B --> P["RAG-09-015 长上下文与缓存"]
  J --> T["RAG-09-016 生成器适配"]
```

所有 16 个原子均由 [标准学习正文](../../../knowledge/rag/chapters/rag-09-context-generation.md) 覆盖。逐项引用：`RAG-09-001`、`RAG-09-002`、`RAG-09-003`、`RAG-09-004`、`RAG-09-005`、`RAG-09-006`、`RAG-09-007`、`RAG-09-008`、`RAG-09-009`、`RAG-09-010`、`RAG-09-011`、`RAG-09-012`、`RAG-09-013`、`RAG-09-014`、`RAG-09-015`、`RAG-09-016`。关系图只表达数据流和约束，不新增独立技术结论。

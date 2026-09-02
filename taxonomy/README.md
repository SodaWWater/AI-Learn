# AI 知识分类规范

检索增强生成（Retrieval-Augmented Generation，RAG）的节点类型、关系类型和图约束见 [`rag-graph-model.json`](rag-graph-model.json)，机器可读双语术语见 [`rag-terminology.json`](rag-terminology.json)。两者分别由项目规划和 [`knowledge/rag/TERMINOLOGY.md`](../knowledge/rag/TERMINOLOGY.md) 约束。

## 分类原则

- 一级领域回答“主要属于哪一类知识”。
- 标签表达跨领域关系，一个知识点可以拥有多个标签。
- 文件目录只放主领域，跨领域内容通过 `related` 和 `topics` 连接。
- ID 一经发布不得因标题调整而改变。

## 知识关系

| 关系 | 含义 | 能否删除原信息 |
|---|---|---:|
| `duplicate` | 语义和适用条件完全等价 | 可以合并，但保留全部来源 |
| `contains` | 一个知识点包含另一个 | 否 |
| `extends` | 增加条件、细节或边界 | 否 |
| `implements` | 概念的代码或工程实现 | 否 |
| `compares` | 对比、选型或权衡 | 否 |
| `conflicts` | 来源结论不一致 | 否，必须核验 |
| `versioned` | 不同版本下的不同结论 | 否 |
| `related` | 有关但不存在包含关系 | 否 |

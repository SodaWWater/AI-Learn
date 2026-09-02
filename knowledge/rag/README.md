# RAG 标准知识库

当前状态：`restructuring`。来源盘点已经完成，来源单元正在逐条人工复核。`RAG-01` 至 `RAG-03` 的第一版正文早于最新双语、图优先和问题驱动标准，现统一标记为待重写草稿，不视为正式正文。

详细原子知识目录见 [`catalog.md`](catalog.md)，机器可读版本见 [`catalog.json`](catalog.json)。当前目录用于防止不同角度的细节在去重时被错误删除；其中条目尚未全部完成来源映射和事实核验。

待重写草稿：

- [`RAG-01` 基础、价值与能力边界](chapters/rag-01-foundations.md)
- [`RAG-02` 系统架构与生命周期](chapters/rag-02-architecture-lifecycle.md)
- [`RAG-03` 文档解析与数据治理](chapters/rag-03-document-parsing-governance.md)

学习总览和多图导航见 [`learning/rag/overview.md`](../../learning/rag/overview.md)。

正式内容必须遵守 [`CONTENT_STANDARD.md`](CONTENT_STANDARD.md) 和 [`TERMINOLOGY.md`](TERMINOLOGY.md)。整体执行顺序见 [`docs/PROJECT_PLAN.md`](../../docs/PROJECT_PLAN.md)。

## 预定知识主干

| ID | 模块 | 必须覆盖的核心内容 |
|---|---|---|
| `RAG-01` | 基础与边界 | 定义、目标、知识截止、私域知识、幻觉、RAG 与微调/长上下文/搜索的关系 |
| `RAG-02` | 系统架构与生命周期 | 离线建库、在线问答、数据流、控制流、组件边界 |
| `RAG-03` | 文档解析与数据治理 | PDF、Word、HTML、OCR、表格、图片、清洗、去重、元数据、权限 |
| `RAG-04` | Chunking | 固定、递归、结构、语义、滑窗、父子、命题、上下文化、参数与评估 |
| `RAG-05` | Embedding | 原理、训练范式、模型选择、维度、归一化、距离度量、领域与多语言评估 |
| `RAG-06` | 存储与索引 | 向量库、倒排索引、HNSW、IVF、PQ、过滤、ID、版本与选型 |
| `RAG-07` | Query 理解 | 意图、改写、扩展、分解、HyDE、Step-back、路由与时间约束 |
| `RAG-08` | 检索、融合与重排 | Dense、Sparse、BM25、Hybrid、多路召回、RRF、Rerank、MMR、阈值与失败恢复 |
| `RAG-09` | 上下文与生成 | Prompt 拼装、上下文压缩、Lost in the Middle、引用、拒答、Grounding 与核查 |
| `RAG-10` | 评估 | 数据集、检索指标、生成指标、端到端指标、人工评估、线上实验与失败归因 |
| `RAG-11` | 生产工程与治理 | 增量更新、缓存、延迟、吞吐、多租户、ACL、PII、安全、可观测性与成本 |
| `RAG-12` | 高级范式 | Advanced/Modular/Agentic RAG、Self-RAG、CRAG、Adaptive、GraphRAG、多模态与 Deep Research |
| `RAG-13` | 项目与面试应用 | 系统设计、选型、排障、项目指标、代码实践及有公开出处的题目关联 |

以上只是分类骨架，不代表最终知识点清单。最终清单必须由来源覆盖矩阵和权威资料补漏共同确定。

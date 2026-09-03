# 从一个问题到可核验答案：检索增强生成（Retrieval-Augmented Generation，RAG）首次构建走读

> 状态：`draft / backbone-v0.1 / 非正式`

这一页不要求先选定某个框架或某个向量数据库（Vector Database）。目标是把检索增强生成（Retrieval-Augmented Generation，RAG）看成一组可以逐段检查的输入、输出与失败边界。

## 先定义要解决的问题

假设用户问："某项内部制度现在是否仍适用？"

一个合格的检索增强生成（Retrieval-Augmented Generation，RAG）系统不应只追求流畅回答，而应能说明：用了哪一版制度、哪些证据支持结论、用户是否有权读取这些证据，以及证据不足时为什么拒答。

这让目标从"让模型回答"变成"让答案可追溯、可更新、可拒答"。

## 离线链路：先让知识值得被检索

| 步骤 | 输入 | 必须保留的输出 | 常见失败 |
|---|---|---|---|
| 数据摄取（Data Ingestion） | 原始文件与变更事件 | 来源 ID、文档 ID、版本、采集时间 | 新版本覆盖旧版本但没有版本记录 |
| 文档解析（Document Parsing） | PDF、网页、表格或 Markdown | 正确的阅读顺序、标题层级、表格与代码边界 | 多栏内容错序，表格字段丢失 |
| 数据治理（Data Governance） | 解析结果与访问规则 | 权限、有效期、敏感级别、删除状态 | 只在生成提示中要求保密，检索时已越权 |
| 文本切分（Chunking） | 可读内容与结构 | 可引用片段、父文档关系、片段版本 | 把条件与结论切开，导致片段看似相关却无法支持答案 |
| 向量嵌入（Embedding）与存储索引（Storage and Indexing） | 片段与元数据 | 可检索表示、过滤字段、索引版本 | 向量更新了但索引或缓存仍返回旧内容 |

第一轮构建的关键不是追求最多组件，而是让每个片段都能回答四个问题：它来自哪里、何时有效、谁可以读取、能否回到完整上下文。

## 在线链路：把问题变成受约束的证据选择

用户问题进入在线查询与回答（Online Query and Answering）后，系统依次做五件事：

1. 查询理解（Query Understanding）：识别问题中的主体、时间、权限和是否真的需要检索。
2. 查询改写（Query Rewrite）与查询路由（Query Routing）：必要时生成更适合召回的表达，并选择正确知识源；改写不能改变用户原意。
3. 检索（Retrieval）：从已授权的候选空间召回证据。高相似度不等于证据支持结论。
4. 结果融合（Result Fusion）与重排（Reranking）：合并多种召回信号，并让更能直接回答问题的证据靠前。
5. 上下文组装（Context Assembly）与答案生成（Answer Generation）：在有限上下文预算中放入问题、规则和有序证据，要求答案只陈述证据可以支撑的内容。

如果没有足够证据，答案应该执行拒答（Abstention）或追问，而不是用模型参数记忆补齐细节。

## 答案不是终点

回答输出至少应包含答案文本、引用与验证（Citation and Verification）信息、索引版本、模型版本和追踪 ID。这样，用户或工程人员才可以区分三类问题：

- 没有找到证据：可能是知识缺失、解析失败、权限过滤或召回失败；
- 找到证据但回答错误：可能是排序、上下文组装或证据约束生成（Grounded Generation）失败；
- 回答当时正确、后来失效：可能是文档更新、索引发布或缓存失效链路出了问题。

评估反馈（Evaluation and Feedback）应把这些失败样本送回对应阶段，而不是只用一次端到端得分判断整个检索增强生成（Retrieval-Augmented Generation，RAG）系统好坏。

## 第一版工程边界

第一版检索增强生成（Retrieval-Augmented Generation，RAG）系统可以很小，但不能省略以下边界：

- 检索前执行权限过滤；
- 检索后保留来源、版本和片段 ID；
- 证据不足时拒答或明确不确定性；
- 每次发布记录索引版本；
- 为查询、候选、最终证据和答案保留可排障追踪。

有了这些边界后，再逐步比较文本切分（Chunking）、向量嵌入（Embedding）、混合检索（Hybrid Search）、重排（Reranking）或高级检索增强生成（Advanced RAG）策略，才知道一次优化实际改变了哪一段链路。

继续阅读：[18 节点概要学习卡](03-stage-cards.md) | [基础、价值与能力边界](../../../knowledge/rag/chapters/rag-01-foundations.md) | [系统架构与生命周期](../../../knowledge/rag/chapters/rag-02-architecture-lifecycle.md)

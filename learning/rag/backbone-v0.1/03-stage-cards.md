# 18 个节点概要学习卡：检索增强生成（Retrieval-Augmented Generation，RAG）

> 状态：`draft / backbone-v0.1 / 非正式`
>
> 使用方式：按编号从上游读到下游；遇到工程现象时，先沿“工程问题”定位，再回到“上下游”和“跨主干关系”。这里的技术框架（Framework）仅作定位示例，具体版本、接口和适用条件须在正式章节阶段重新核验。

## 1. 数据摄取（Data Ingestion）

- **节点目标**：把数据源（Data Source）稳定接入知识流水线（Knowledge Pipeline），保留来源标识、版本和变更事件。
- **输入**：文件、网页、数据库记录、事件消息和来源登记（Source Registry）。
- **输出**：原始文档（Raw Document）、来源元数据（Source Metadata）、摄取状态（Ingestion Status）。
- **核心原理**：以可重复、可追踪和幂等性（Idempotency）为约束，区分首次全量和增量更新（Incremental Update）。
- **实际开发位置**：连接对象存储（Object Storage）、消息队列（Message Queue）、定时任务（Scheduled Job）与解析队列的入口。
- **常用技术或框架**：Airflow、Dagster、Kafka、S3-compatible Storage、Webhook。
- **常见工程问题**：重复摄取、漏事件、来源版本漂移、失败重试造成重复写入。
- **上下游关系**：上游是数据源（Data Source）；下游是文档解析（Document Parsing）和数据治理（Data Governance）。
- **跨主干关系**：连接生产治理（Production Governance）的权限、审计、限流（Rate Limiting）与灾难恢复（Disaster Recovery）。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 2. 文档解析（Document Parsing）

- **节点目标**：从 PDF、Word、HTML、Markdown、表格或图像中恢复文本、版面和结构。
- **输入**：原始文档（Raw Document）及文件格式、编码和版本信息。
- **输出**：结构化文档（Structured Document）、页码、标题、表格、图片和定位信息。
- **核心原理**：解析质量决定后续文本切分（Chunking）边界和引用（Citation）定位；阅读顺序错误会制造语义噪声。
- **实际开发位置**：离线知识构建（Offline Knowledge Construction）中，通常位于清洗和切分之前。
- **常用技术或框架**：PyMuPDF、Apache Tika、Unstructured、OCR（Optical Character Recognition）。
- **常见工程问题**：多栏错序、扫描件无文本层、表格扁平化、页眉页脚污染、代码和公式损坏。
- **上下游关系**：上游是数据摄取（Data Ingestion）；下游是数据治理（Data Governance）。
- **跨主干关系**：与多模态检索增强生成（Multimodal RAG）、文档理解（Document Understanding）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 3. 数据治理（Data Governance）

- **节点目标**：在进入索引前确认质量、来源、时间、权限、隐私和合规边界。
- **输入**：结构化文档（Structured Document）、来源元数据（Source Metadata）、访问控制列表（Access Control List，ACL）。
- **输出**：清洗文档（Clean Document）、治理标签（Governance Tag）、权限和保留策略（Retention Policy）。
- **核心原理**：治理是检索可信度和访问安全的前置条件；质量规则必须可审计并支持回退。
- **实际开发位置**：解析后、文本切分（Chunking）前；也参与索引发布（Index Release）审批。
- **常用技术或框架**：数据质量规则（Data Quality Rules）、DLP（Data Loss Prevention）、Schema Registry。
- **常见工程问题**：PII（Personally Identifiable Information）泄露、权限标签丢失、旧版本未下线、重复文档未识别。
- **上下游关系**：上游是文档解析（Document Parsing）；下游是文本切分（Chunking）和存储与索引（Storage and Indexing）。
- **跨主干关系**：与安全治理（Security Governance）、多租户（Multi-tenancy）和合规审计（Compliance Audit）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 4. 文本切分（Chunking）

- **节点目标**：形成既能被检索命中又能支持答案生成（Answer Generation）的内容片段。
- **输入**：清洗文档（Clean Document）、标题层级、段落、表格和代码结构。
- **输出**：Chunk、Chunk ID、Parent ID、重叠范围（Overlap）和来源定位。
- **核心原理**：切分粒度同时受召回率（Recall）、上下文预算（Context Budget）和引用完整性约束。
- **实际开发位置**：离线知识构建（Offline Knowledge Construction）的核心变换阶段。
- **常用技术或框架**：Recursive Character Splitter、Sentence Window Retrieval、Parent-Child Retrieval、Late Chunking。
- **常见工程问题**：片段过大或过小、语义边界断裂、重复过多、表格和代码不可检索。
- **上下游关系**：上游是数据治理（Data Governance）；下游是向量嵌入（Embedding）和存储与索引（Storage and Indexing）。
- **跨主干关系**：与长上下文（Long Context）、知识图谱（Knowledge Graph）实体片段和多模态内容切分重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 5. 向量嵌入（Embedding）

- **节点目标**：把 Chunk 和用户问题（User Query）编码为可比较的语义向量（Semantic Vector）。
- **输入**：文本片段（Chunk）、查询表达（Query Expression）、嵌入模型（Embedding Model）。
- **输出**：向量、模型版本、维度、归一化状态和批处理结果。
- **核心原理**：相似度函数（Similarity Function）把语义接近度转化为检索排序信号；查询和文档可能需要非对称编码。
- **实际开发位置**：离线为文档建立向量；在线为查询生成向量，并参与模型升级重建。
- **常用技术或框架**：Sentence Transformers、BGE、E5、OpenAI Embeddings、Cosine Similarity。
- **常见工程问题**：领域语义不匹配、维度或距离配置错误、模型升级导致向量空间不兼容、吞吐不足。
- **上下游关系**：上游是文本切分（Chunking）或查询改写（Query Rewrite）；下游是存储与索引（Storage and Indexing）或检索（Retrieval）。
- **跨主干关系**：与向量数据库（Vector Database）、多模态嵌入（Multimodal Embedding）和模型适配（Model Adaptation）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 6. 存储与索引（Storage and Indexing）

- **节点目标**：持久化向量、文本、元数据和主键，并提供可扩展检索索引。
- **输入**：向量、Chunk、Document ID、Parent ID、权限标签和索引参数。
- **输出**：可查询索引（Queryable Index）、版本、分区（Partition）和副本（Replica）。
- **核心原理**：精确检索（Exact Search）与近似最近邻检索（Approximate Nearest Neighbor Search，ANN）在延迟、召回率和成本之间权衡。
- **实际开发位置**：离线索引构建（Index Construction）与在线检索服务（Retrieval Service）的交界。
- **常用技术或框架**：FAISS、Milvus、Qdrant、pgvector、HNSW（Hierarchical Navigable Small World）。
- **常见工程问题**：索引未加载、过滤顺序错误、分片倾斜、更新与删除不一致、热数据预热不足。
- **上下游关系**：上游是向量嵌入（Embedding）和数据治理（Data Governance）；下游是检索（Retrieval）。
- **跨主干关系**：与向量数据库（Vector Database）、全文索引（Full-text Index）和分布式存储（Distributed Storage）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 7. 查询理解（Query Understanding）

- **节点目标**：识别用户意图、实体、时间、地域、权限和是否需要检索。
- **输入**：用户问题（User Query）、会话历史（Conversation History）和用户上下文。
- **输出**：规范化查询（Normalized Query）、意图标签（Intent Label）和约束条件。
- **核心原理**：先决定“问的是什么”和“应走哪条路径”，再进行查询改写（Query Rewrite）或路由。
- **实际开发位置**：在线查询（Online Query）入口，可由规则、分类器或大语言模型（Large Language Model，LLM）实现。
- **常用技术或框架**：规则引擎（Rule Engine）、Structured Output、LLM Router。
- **常见工程问题**：多轮指代丢失、是否检索判断错误、权限条件遗漏、语言检测错误。
- **上下游关系**：上游是用户问题（User Query）；下游是查询改写（Query Rewrite）和查询路由（Query Routing）。
- **跨主干关系**：与搜索（Search）、智能体（Agent）规划和提示工程（Prompt Engineering）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 8. 查询改写（Query Rewrite）

- **节点目标**：生成更适合召回的一个或多个查询，同时避免语义漂移。
- **输入**：规范化查询（Normalized Query）、会话历史（Conversation History）和意图约束。
- **输出**：改写查询、Multi-Query、HyDE（Hypothetical Document Embeddings）或子问题。
- **核心原理**：扩展召回表达可以提高覆盖，但生成内容不能被误当作事实证据。
- **实际开发位置**：查询理解（Query Understanding）之后、检索（Retrieval）之前。
- **常用技术或框架**：Multi-Query Expansion、HyDE、Query Decomposition、Step-back Prompting。
- **常见工程问题**：语义漂移、改写延迟、查询爆炸、原始约束被删除。
- **上下游关系**：上游是查询理解（Query Understanding）；下游是查询路由（Query Routing）和多路检索（Multi-channel Retrieval）。
- **跨主干关系**：与提示工程（Prompt Engineering）、智能体（Agent）规划和深度研究（Deep Research）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 9. 查询路由（Query Routing）

- **节点目标**：根据问题类型选择知识源、检索通道、工具或不检索路径。
- **输入**：改写查询、意图标签、权限条件和系统能力目录。
- **输出**：路由决策（Routing Decision）、目标索引和执行计划。
- **核心原理**：路由把单一链路变成有条件分支，必须有默认路径和失败回退。
- **实际开发位置**：在线查询（Online Query）控制流中，连接查询增强和检索执行。
- **常用技术或框架**：规则路由（Rule-based Routing）、语义路由（Semantic Routing）、LangGraph。
- **常见工程问题**：路由误判、权限绕过、工具不可用、分支结果难以评估。
- **上下游关系**：上游是查询改写（Query Rewrite）；下游是检索（Retrieval）、工具调用（Tool Calling）或不检索路径。
- **跨主干关系**：与智能体（Agent）、GraphRAG、SQL 检索（SQL Retrieval）和搜索系统重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 10. 检索（Retrieval）

- **节点目标**：从候选空间召回与查询相关、可用且允许访问的证据。
- **输入**：查询向量、关键词查询、过滤条件、索引和 Top-K 参数。
- **输出**：检索候选（Retrieval Candidate）、相关性分数和来源定位。
- **核心原理**：稠密检索（Dense Retrieval）、稀疏检索（Sparse Retrieval）和元数据过滤（Metadata Filtering）各有覆盖边界。
- **实际开发位置**：在线链路的候选生成阶段，直接依赖存储与索引（Storage and Indexing）。
- **常用技术或框架**：BM25、Hybrid Search、FAISS、Milvus、Qdrant。
- **常见工程问题**：零召回、噪声召回、过滤后为空、延迟过高、召回结果版本过旧。
- **上下游关系**：上游是查询路由（Query Routing）；下游是结果融合（Result Fusion）和重排（Reranking）。
- **跨主干关系**：与向量数据库（Vector Database）、传统搜索（Traditional Search）和 GraphRAG 重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 11. 结果融合（Result Fusion）

- **节点目标**：合并多个检索通道、查询变体或知识源的候选。
- **输入**：多路候选、名次、相似度分数、来源可信度和新鲜度信号。
- **输出**：统一候选集（Unified Candidate Set）和融合分数。
- **核心原理**：不同通道分数不可直接比较时，应使用排名或归一化策略并保留来源多样性。
- **实际开发位置**：检索（Retrieval）之后、重排（Reranking）之前。
- **常用技术或框架**：RRF（Reciprocal Rank Fusion）、Weighted Fusion、Score Normalization。
- **常见工程问题**：分数尺度不一致、某一路径垄断、重复候选过多、来源冲突未显露。
- **上下游关系**：上游是稠密检索（Dense Retrieval）、稀疏检索（Sparse Retrieval）和过滤；下游是重排（Reranking）。
- **跨主干关系**：与联邦搜索（Federated Search）、多路召回（Multi-channel Retrieval）和 GraphRAG 融合重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 12. 重排（Reranking）

- **节点目标**：对有限候选执行更精细的查询-文档相关性判断。
- **输入**：统一候选集（Unified Candidate Set）、原始查询和重排模型（Reranker）。
- **输出**：重排候选、精排分数、截断后的 Top-K Results。
- **核心原理**：Cross-encoder（交叉编码器）通常更精确但更昂贵；重排只应处理受控候选规模。
- **实际开发位置**：结果融合（Result Fusion）之后、上下文组装（Context Assembly）之前。
- **常用技术或框架**：Cross-encoder、Bi-encoder、Cohere Rerank、bge-reranker。
- **常见工程问题**：批处理不足、长文档截断、重排模型过拟合、延迟挤占生成预算。
- **上下游关系**：上游是结果融合（Result Fusion）；下游是上下文组装（Context Assembly）。
- **跨主干关系**：与学习排序（Learning to Rank）、搜索排序（Search Ranking）和成本优化重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 13. 上下文组装（Context Assembly）

- **节点目标**：在上下文预算（Context Budget）内选择、排序、压缩并标注证据。
- **输入**：重排候选、查询、System Prompt、权限和输出 Schema。
- **输出**：结构化上下文（Structured Context）、证据编号和可引用片段。
- **核心原理**：相关性、覆盖、多样性、位置效应和 Token 预算共同决定入模内容。
- **实际开发位置**：重排（Reranking）和答案生成（Answer Generation）之间。
- **常用技术或框架**：Contextual Compression、MMR（Maximal Marginal Relevance）、Prompt Template。
- **常见工程问题**：Lost in the Middle、上下文超限、重复证据、权限标签丢失。
- **上下游关系**：上游是重排（Reranking）；下游是答案生成（Answer Generation）和引用与验证（Citation and Verification）。
- **跨主干关系**：与长上下文（Long Context）、提示工程（Prompt Engineering）和多模态上下文重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 14. 答案生成（Answer Generation）

- **节点目标**：基于检索证据生成满足任务、格式和安全约束的回答。
- **输入**：结构化上下文（Structured Context）、用户问题（User Query）、System Prompt 和输出 Schema。
- **输出**：答案草稿、断言（Claim）、引用标记和不确定性表达。
- **核心原理**：Grounded Generation（基于检索证据的生成）要求断言受上下文支持，而不是把模型记忆当作证据。
- **实际开发位置**：在线回答（Online Answering）末端，紧接引用与验证（Citation and Verification）。
- **常用技术或框架**：LLM API、Structured Output、Prompt Caching、温度和停止条件配置。
- **常见工程问题**：幻觉（Hallucination）、证据遗漏、格式失控、长上下文位置偏差。
- **上下游关系**：上游是上下文组装（Context Assembly）；下游是引用与验证（Citation and Verification）。
- **跨主干关系**：与大语言模型（Large Language Model，LLM）、提示工程（Prompt Engineering）和智能体（Agent）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 15. 引用与验证（Citation and Verification）

- **节点目标**：检查答案断言是否由允许的证据支持，并在不足或冲突时拒答或降级。
- **输入**：答案草稿、证据片段、来源可信度、版本和验证规则。
- **输出**：带引用答案、验证报告（Verification Report）、拒答（Abstention）或冲突标记。
- **核心原理**：引用完整性（Citation Completeness）和引用准确率（Citation Accuracy）需要分别检查；事实、观点和推断需区分。
- **实际开发位置**：答案生成（Answer Generation）之后，可同步或异步执行。
- **常用技术或框架**：规则核验（Rule-based Verification）、NLI（Natural Language Inference）、LLM-as-a-Judge。
- **常见工程问题**：引用与断言错配、来源过期、多源冲突、证据不足仍强答。
- **上下游关系**：上游是答案生成（Answer Generation）和上下文组装（Context Assembly）；下游是用户输出（User Output）和评估（Evaluation）。
- **跨主干关系**：与事实核查（Fact Checking）、安全治理（Security Governance）和可信人工智能（Trustworthy AI）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 16. 评估（Evaluation）

- **节点目标**：分层测量解析、检索、生成和端到端任务质量，定位改动收益与回归。
- **输入**：Golden Dataset、日志、人工标注、检索候选和模型输出。
- **输出**：Precision、Recall、Hit Rate、MRR、nDCG、Faithfulness、Groundedness、延迟和成本指标。
- **核心原理**：单一总分不能解释失败；必须把检索质量、答案质量和系统体验拆开，并通过消融实验验证因果。
- **实际开发位置**：离线评估（Offline Evaluation）、线上监控（Online Monitoring）和发布门禁（Release Gate）。
- **常用技术或框架**：RAGAS、LLM-as-a-Judge、A/B Test、Regression Test、Ablation Study。
- **常见工程问题**：数据集偏差、裁判模型偏差、指标与业务目标脱节、线上线下分布漂移。
- **上下游关系**：上游是引用与验证（Citation and Verification）和运行日志（Runtime Log）；下游是失败归因（Failure Attribution）与更新。
- **跨主干关系**：与机器学习评估（Machine Learning Evaluation）、可观测性（Observability）和实验平台重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 17. 生产治理（Production Governance）

- **节点目标**：横切管理权限、安全、可靠性、性能、成本、版本和恢复。
- **输入**：服务配置、数据版本、访问策略、运行指标、审计日志和故障事件。
- **输出**：受控版本、告警、审计记录、降级路径和恢复结果。
- **核心原理**：治理把离线和在线链路置于可观察、可回滚、可恢复的运行边界内。
- **实际开发位置**：覆盖数据摄取（Data Ingestion）至用户输出（User Output）的所有节点。
- **常用技术或框架**：OpenTelemetry、Prometheus、Kubernetes、Canary Release、Circuit Breaker。
- **常见工程问题**：间接提示注入（Indirect Prompt Injection）、数据投毒（Data Poisoning）、高延迟、租户越权、索引版本错配。
- **上下游关系**：横切所有 1 至 16 节点；接收评估（Evaluation）反馈并驱动版本发布（Version Release）。
- **跨主干关系**：与平台工程（Platform Engineering）、安全工程（Security Engineering）和数据治理（Data Governance）重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 18. 高级检索增强生成（Advanced RAG）

- **节点目标**：在基础链路上引入动态路由、多步检索、反思、图结构和多模态能力。
- **输入**：复杂任务、基础 RAG 失败信号、知识图谱（Knowledge Graph）、工具和检索策略。
- **输出**：多步执行轨迹、综合证据、动态答案和停止原因。
- **核心原理**：高级范式通过额外控制环提高复杂任务能力，同时增加延迟、成本、状态管理和评估难度。
- **实际开发位置**：跨越查询理解（Query Understanding）、查询路由（Query Routing）、检索（Retrieval）、生成和评估反馈。
- **常用技术或框架**：Self-RAG、CRAG（Corrective RAG）、GraphRAG、Agentic RAG、LangGraph。
- **常见工程问题**：循环检索、停止条件不明、工具失败传播、证据轨迹不可审计、成本失控。
- **上下游关系**：依赖基础 1 至 17 节点的稳定接口和评估闭环；可回退到传统 RAG（Traditional RAG）。
- **跨主干关系**：与智能体（Agent）、GraphRAG、深度研究（Deep Research）、知识图谱（Knowledge Graph）和多模态 RAG 重叠。
- **后续占位**：[正式知识章节](../../../knowledge/rag/chapters/)；[工程问题/面试题](../../../interview/)。

## 草稿边界

这些学习卡是结构化导航，不是完整知识章节。正式阶段必须从审核后的来源证据（Source Evidence）和有向知识图谱（Directed Knowledge Graph）生成，并补充版本、来源、实现细节、问题双向链接和冲突说明。

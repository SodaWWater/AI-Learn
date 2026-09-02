# 检索增强生成术语规范

> 状态：`v1-initial`  
> 更新日期：2026-09-02  
> 作用：统一正文、图、表格、问题页和索引中的中英文技术术语。

## 1. 强制表达规则

每次出现专业技术术语，都必须使用本表规定的双语表达，不只在第一次出现时说明。

示例：

- 文档解析（Document Parsing）负责把原始文档转成结构化元素；
- 文档解析（Document Parsing）的输出进入文本切分（Chunking）；
- 文本切分（Chunking）的结果用于向量嵌入（Embedding）。

不要写成：

```text
文档解析负责处理原文，之后 Chunking，再做嵌入。
```

代码中的类名、函数名、参数、应用程序编程接口（Application Programming Interface，API）、命令和配置项保持原样，不翻译代码标识符。

## 2. 规范原则

1. 中文使用国内工程领域常见表达，不机械直译。
2. 括号中使用专业英文全称或通用英文名称。
3. 缩写与英文全称同时存在时，格式为“中文（English Full Name，ABBR）”。
4. 原本以英文为主的术语，也提供中文解释，例如“文本切分（Chunking）”。
5. 同一英文术语不能按上下文随意改变中文主名称；确有多义时在备注中区分。
6. 算法名称已有通行缩写时保留缩写，不自行创造中文缩写。
7. 产品、项目和框架使用官方名称，并在需要时补充中文类别。
8. 标题、图节点、表格和正文采用同一规范名称。

## 3. 基础与架构

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 检索增强生成（Retrieval-Augmented Generation，RAG） | RAG | 不写“检索增强式生成”等自创名称 |
| 大语言模型（Large Language Model，LLM） | LLM | 复数仍使用同一形式 |
| 参数记忆（Parametric Memory） | 参数知识 | 讨论模型参数中知识时使用 |
| 非参数记忆（Non-parametric Memory） | 外部知识 | 不使用生硬的“非参数化知识” |
| 检索增强生成流程（RAG Workflow） | RAG 流程 | 表示完整学习主干 |
| 检索增强生成流水线（RAG Pipeline） | RAG Pipeline | 偏工程执行链路 |
| 离线知识构建（Offline Knowledge Construction） | 离线建库 | 包含摄取、解析、切分和索引 |
| 在线问答（Online Query and Answering） | 在线链路 | 用户请求执行链路 |
| 数据流（Data Flow） |  | 业务对象流动 |
| 控制流（Control Flow） |  | 路由、编排和停止条件 |
| 错误流（Error Flow） |  | 错误和低质量状态传播 |
| 有向知识图谱（Directed Knowledge Graph） | 知识图谱 | 本项目底层关系模型 |
| 主干（Backbone） | 技术主线 | 独立技术体系的主路径 |
| 流程节点（Pipeline Stage） | 节点 | 主干中的处理阶段 |
| 跨主干重叠（Cross-backbone Overlap） | 重叠 | 两个技术体系共享节点或能力 |

## 4. 数据摄取、解析与治理

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 数据源（Data Source） | 知识源 | 原始数据入口 |
| 数据摄取（Data Ingestion） | Ingestion | 不写“数据吸入” |
| 文档加载器（Document Loader） | Loader | 读取外部来源 |
| 文档解析（Document Parsing） | Parsing | 恢复文本和结构 |
| 光学字符识别（Optical Character Recognition，OCR） | OCR | 扫描件和图像文字识别 |
| 版面分析（Layout Analysis） | 版面识别 | 恢复区域和阅读顺序 |
| 阅读顺序（Reading Order） |  | 多栏和复杂版面重点 |
| 文档元素（Document Element） | Element | 标题、段落、表格、图片等 |
| 数据清洗（Data Cleaning） | 清洗 | 不等于语义改写 |
| 数据规范化（Data Normalization） | 规范化 | 编码、空白和格式统一 |
| 近似重复检测（Near-duplicate Detection） | 近重复检测 | 区别于精确哈希去重 |
| 元数据（Metadata） |  | 来源、时间、层级和权限等字段 |
| 个人身份信息（Personally Identifiable Information，PII） | PII | 隐私和脱敏治理 |
| 访问控制列表（Access Control List，ACL） | ACL | 文档或片段权限 |
| 数据治理（Data Governance） |  | 权限、合规、时效和删除 |

## 5. 文本切分与表示

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 文本切分（Chunking） | Chunking | 不单独翻译为“分块技术” |
| 文本片段（Chunk） | Chunk | 可带结构和元数据 |
| 分块大小（Chunk Size） | Chunk Size | 字符数或词元数需说明 |
| 分块重叠（Chunk Overlap） | Overlap | 相邻文本片段重叠 |
| 递归字符切分（Recursive Character Splitting） | 递归切分 | 常见结构保持方法 |
| 结构化切分（Structure-aware Chunking） | 结构切分 | 按标题、段落或元素切分 |
| 语义切分（Semantic Chunking） | 语义分块 | 根据语义边界切分 |
| 父子文档检索（Parent-Child Retrieval） | Parent-Child | 小片段召回、父上下文返回 |
| 句子窗口检索（Sentence Window Retrieval） | Sentence Window | 命中句子并扩展窗口 |
| 命题化切分（Proposition-based Chunking） | 命题切分 | 拆成原子事实 |
| 上下文化切分（Contextual Chunking） | Contextual Chunking | 为片段补充局部上下文 |
| 词元（Token） | Token | 不使用“标记”替代模型词元 |
| 上下文窗口（Context Window） | Context Window | 模型可接受输入范围 |
| 向量嵌入（Embedding） | Embedding | 表示模型或向量结果按语境说明 |
| 嵌入模型（Embedding Model） | Embedding Model | 生成向量表示的模型 |
| 对比学习（Contrastive Learning） |  | Embedding 常见训练范式 |
| 向量归一化（Vector Normalization） | Normalization | 与数据规范化区分 |
| 余弦相似度（Cosine Similarity） | Cosine | 向量相似度度量 |
| 内积（Inner Product） | IP | 向量相似度度量 |
| 欧氏距离（Euclidean Distance） | L2 Distance | 距离越小通常越相近 |

## 6. 存储、索引与向量数据库

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 向量数据库（Vector Database） | Vector DB | 不等同于近似最近邻检索 |
| 向量存储（Vector Storage） |  | 向量数据库的一项能力 |
| 数据模式（Data Schema） | Schema | 主键、正文、向量和元数据 |
| 向量索引（Vector Index） |  | 用于近邻查询 |
| 倒排索引（Inverted Index） |  | 关键词和稀疏检索基础 |
| 精确最近邻检索（Exact Nearest Neighbor Search） | Exact KNN | 全量精确比较 |
| 近似最近邻检索（Approximate Nearest Neighbor Search，ANN） | ANN | 向量数据库的一项检索能力 |
| 分层可导航小世界图（Hierarchical Navigable Small World，HNSW） | HNSW | 图结构近似最近邻索引 |
| 倒排文件索引（Inverted File Index，IVF） | IVF | 向量空间聚类分桶 |
| 乘积量化（Product Quantization，PQ） | PQ | 向量压缩方法 |
| 元数据过滤（Metadata Filtering） | Filter | 精确条件过滤 |
| 索引构建（Index Construction） | Indexing | 与数据摄取阶段关联 |
| 索引发布（Index Release） |  | 候选版本切换为在线版本 |
| 索引合并（Index Compaction） | Compaction | 合并段和回收删除空间 |
| 分区（Partitioning） | Partition | 逻辑或物理数据划分 |
| 分片（Sharding） | Shard | 水平扩展数据 |
| 副本（Replication） | Replica | 高可用和读扩展 |
| 多租户（Multi-tenancy） | Multi-tenant | 租户数据和资源隔离 |

## 7. 查询、检索、融合与重排

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 用户问题（User Query） | Query | 用户原始输入 |
| 查询理解（Query Understanding） |  | 意图、实体、时间和路由 |
| 查询改写（Query Rewrite） | Rewrite | 生成更适合检索的查询 |
| 多查询扩展（Multi-Query Expansion） | Multi-Query | 生成多个检索表达 |
| 假设文档嵌入（Hypothetical Document Embeddings，HyDE） | HyDE | 先生成假设文档再嵌入 |
| 查询分解（Query Decomposition） | Decomposition | 将复杂问题拆成子问题 |
| 退步提示（Step-back Prompting） | Step-back | 先提出更抽象问题 |
| 查询路由（Query Routing） | Routing | 选择知识源、方法或工具 |
| 检索（Retrieval） | Retrieval | 泛指候选查找过程 |
| 检索器（Retriever） | Retriever | 执行检索的组件 |
| 稠密检索（Dense Retrieval） | Dense Search | 基于稠密向量 |
| 稀疏检索（Sparse Retrieval） | Sparse Search | 基于词项或稀疏表示 |
| 最佳匹配算法（Best Matching 25，BM25） | BM25 | 常用稀疏排序函数 |
| 混合检索（Hybrid Search） | Hybrid Search | 组合稠密和稀疏检索 |
| 多路召回（Multi-channel Retrieval） | 多路检索 | 多种通道并行产生候选 |
| 结果融合（Result Fusion） | Fusion | 合并不同通道结果 |
| 倒数排名融合（Reciprocal Rank Fusion，RRF） | RRF | 基于名次的融合方法 |
| 召回候选（Retrieval Candidate） | Candidate | 尚未完成重排和上下文选择 |
| 重排（Reranking） | Rerank | 对候选进行更精细排序 |
| 重排模型（Reranker） | Reranker | 执行重排的模型或组件 |
| 双编码器（Bi-encoder） | Bi-encoder | 查询和文档分别编码 |
| 交叉编码器（Cross-encoder） | Cross-encoder | 查询和文档联合编码 |
| 最大边际相关性（Maximal Marginal Relevance，MMR） | MMR | 平衡相关性和多样性 |
| 前 K 个结果（Top-K Results） | Top-K | 需要明确所在阶段 |

## 8. 上下文、生成与验证

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 上下文组装（Context Assembly） | Context Building | 选择、排序和格式化入模内容 |
| 上下文压缩（Contextual Compression） | Compression | 压缩检索内容 |
| 中间信息丢失（Lost in the Middle） | Lost in the Middle | 长上下文位置效应 |
| 提示词（Prompt） | Prompt | 国内常用“提示词” |
| 系统提示词（System Prompt） | System Prompt | 高优先级指令 |
| 基于检索证据的生成（Grounded Generation） | Grounded Generation | 不译成生硬的“接地生成” |
| 事实依据性（Groundedness） | Groundedness | 输出是否有证据支持 |
| 忠实度（Faithfulness） | Faithfulness | 输出是否忠于上下文 |
| 引用（Citation） | Citation | 答案与来源映射 |
| 拒答（Abstention） | Abstention | 证据不足时不回答 |
| 结构化输出（Structured Output） |  | 按数据模式输出 |
| 提示词缓存（Prompt Caching） | Prompt Cache | 缓存可复用前缀 |

## 9. 评估、生产与安全

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 黄金数据集（Golden Dataset） | Golden Set | 标注问题、答案和证据 |
| 准确率（Precision） | Precision | 相关结果占返回结果比例 |
| 召回率（Recall） | Recall | 找到目标证据的能力 |
| 命中率（Hit Rate） | Hit Rate | Top-K 是否包含目标 |
| 平均倒数排名（Mean Reciprocal Rank，MRR） | MRR | 首个正确结果的位置 |
| 归一化折损累计增益（Normalized Discounted Cumulative Gain，nDCG） | nDCG | 有等级相关性的排序质量 |
| 答案正确性（Answer Correctness） | Correctness | 答案与参考事实一致性 |
| 引用准确率（Citation Accuracy） |  | 引用是否真正支持断言 |
| 大语言模型裁判（LLM-as-a-Judge） | LLM Judge | 使用模型评分 |
| 消融实验（Ablation Study） | Ablation | 移除模块判断贡献 |
| 回归测试（Regression Test） | Regression | 防止更新破坏历史表现 |
| 增量更新（Incremental Update） | Incremental Update | 只处理变化数据 |
| 幂等性（Idempotency） | Idempotency | 重复执行结果一致 |
| 灰度发布（Canary Release） | Canary | 不使用 Gray Release |
| 双写（Dual Write） | Dual Write | 新旧版本并行写入 |
| 原子切换（Atomic Switch） |  | 在线版本一次切换 |
| 缓存（Caching） | Cache | 检索、重排或答案缓存 |
| 限流（Rate Limiting） | Rate Limit | 控制请求速率 |
| 背压（Backpressure） | Backpressure | 下游过载时抑制上游 |
| 熔断（Circuit Breaking） | Circuit Breaker | 故障时停止调用 |
| 可观测性（Observability） |  | 指标、日志和追踪 |
| 分布式追踪（Distributed Tracing） | Tracing | 串联调用链 |
| 间接提示注入（Indirect Prompt Injection） | Indirect Injection | 恶意指令来自检索文档 |
| 数据投毒（Data Poisoning） | Poisoning | 恶意内容污染知识库 |
| 灾难恢复（Disaster Recovery） | DR | 备份、恢复和重建 |

## 10. 高级范式与交叉领域

| 规范表达 | 缩写/别名 | 备注 |
|---|---|---|
| 基础检索增强生成（Naive RAG） | Naive RAG | 基线流程 |
| 高级检索增强生成（Advanced RAG） | Advanced RAG | 查询、检索和生成优化 |
| 模块化检索增强生成（Modular RAG） | Modular RAG | 组件化和路由组合 |
| 智能体检索增强生成（Agentic RAG） | Agentic RAG | 动态决策闭环 |
| 自适应检索（Adaptive Retrieval） | Adaptive Retrieval | 动态决定是否和如何检索 |
| 自反思检索增强生成（Self-RAG） | Self-RAG | 检索与反思控制 |
| 纠错检索增强生成（Corrective RAG，CRAG） | CRAG | 检索质量评估和纠错 |
| 图检索增强生成（GraphRAG） | GraphRAG | 图结构和社区摘要检索 |
| 多模态检索增强生成（Multimodal RAG） | Multimodal RAG | 文本、图像、表格等共同检索 |
| 深度研究（Deep Research） | Deep Research | 多步搜索、验证和综合 |
| 智能体（Agent） | Agent | 具备状态、工具和动态决策 |
| 工具调用（Tool Calling） | Tool Calling | 调用外部能力 |
| 提示工程（Prompt Engineering） | Prompt Engineering | 提示设计与上下文组织 |

## 11. 维护方法

- 新术语先加入本表，再进入正式内容。
- 修改规范名称时，必须全库替换并更新图节点标签。
- 存在翻译争议时，记录候选表达、国内使用证据和最终决定。
- 产品、框架和模型名称使用官方拼写，不纳入普通术语翻译。
- 术语表后续应生成机器可读版本，用于自动检查裸露术语和不一致翻译。


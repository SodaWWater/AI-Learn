# RAG 原子知识目录

当前版本共 **191** 个原子知识点，状态为 `inventory_draft`。

> 原子目录用于防止去重时丢失不同角度的信息；它不是已完成的标准答案。

## RAG-01 基础与边界

- `RAG-01-001` RAG 的定义、核心组件与工作目标
- `RAG-01-002` 知识截止、知识空白与知识更新问题
- `RAG-01-003` 企业私域知识接入与可审计性
- `RAG-01-004` RAG 对幻觉的缓解能力与边界
- `RAG-01-005` RAG 与微调的区别、组合和选型
- `RAG-01-006` RAG 与长上下文的区别、组合和选型
- `RAG-01-007` RAG 与传统搜索系统的区别和联系
- `RAG-01-008` RAG 与模型记忆、上下文工程的关系
- `RAG-01-009` 适合使用 RAG 的任务与业务条件
- `RAG-01-010` 不适合使用 RAG 或收益有限的场景

## RAG-02 系统架构与生命周期

- `RAG-02-001` 离线知识库构建全流程
- `RAG-02-002` 在线问答全流程
- `RAG-02-003` 召回、过滤、生成三段式链路
- `RAG-02-004` 解析器、切分器、嵌入器、索引和检索器的边界
- `RAG-02-005` Retriever、Reranker 与 Generator 的边界
- `RAG-02-006` RAG 数据流、控制流和错误流
- `RAG-02-007` 来源、文档、Chunk 与答案的可追溯链路
- `RAG-02-008` 批处理、流式摄取与事件驱动更新
- `RAG-02-009` 模块化接口与组件可替换性
- `RAG-02-010` 任务状态、幂等与失败恢复边界

## RAG-03 文档解析与数据治理

- `RAG-03-001` PDF、Word、HTML、Markdown 等来源类型
- `RAG-03-002` 文本型 PDF 的解析问题
- `RAG-03-003` 扫描文档与 OCR 流程
- `RAG-03-004` 版面分析、多栏与阅读顺序恢复
- `RAG-03-005` 页眉、页脚、脚注和目录噪声处理
- `RAG-03-006` 表格结构保留、序列化与结构化检索
- `RAG-03-007` 图片、图表、流程图和 Caption 处理
- `RAG-03-008` 公式、代码与特殊内容解析
- `RAG-03-009` 文本清洗、编码和格式标准化
- `RAG-03-010` 文档级、段落级和近似重复检测
- `RAG-03-011` 文档元数据、来源和时间字段设计
- `RAG-03-012` 入库前权限、PII 脱敏与合规检查
- `RAG-03-013` 解析工具与 Pipeline 方案选型
- `RAG-03-014` 解析质量抽检、错误率和回退策略
- `RAG-03-015` 多模态文档的元素关联与阅读顺序

## RAG-04 Chunking

- `RAG-04-001` Chunking 的目标与检索、生成双重约束
- `RAG-04-002` 固定字符或 Token 长度切分
- `RAG-04-003` 递归字符切分
- `RAG-04-004` 按标题、段落和文档结构切分
- `RAG-04-005` 语义切分与边界阈值
- `RAG-04-006` 滑动窗口与 Chunk Overlap
- `RAG-04-007` 父子文档切分和命中回溯
- `RAG-04-008` Sentence Window Retrieval
- `RAG-04-009` 命题化切分与原子事实
- `RAG-04-010` Contextual Chunking 与上下文补充
- `RAG-04-011` 表格、代码和多模态内容的专项切分
- `RAG-04-012` Chunk Size 的选择与过大、过小问题
- `RAG-04-013` Overlap 的收益、冗余和存储代价
- `RAG-04-014` Chunk ID、Parent ID 和版本设计
- `RAG-04-015` Chunking 策略的离线评估和消融实验
- `RAG-04-016` 延迟切分（Late Chunking）的先编码后池化与全文上下文保留
- `RAG-04-017` 假设问题索引（Hypothetical Question Indexing）与文档侧问题增强

## RAG-05 Embedding

- `RAG-05-001` Embedding 的语义空间与检索作用
- `RAG-05-002` Word2Vec、BERT、SBERT 与现代 Embedding 演进
- `RAG-05-003` 对比学习、正负样本和训练目标
- `RAG-05-004` Query 与 Document 的非对称编码
- `RAG-05-005` 通用、领域、多语言 Embedding 选择
- `RAG-05-006` 向量维度、精度、速度和存储权衡
- `RAG-05-007` Cosine、Inner Product 与 L2 距离
- `RAG-05-008` 向量归一化与相似度实现细节
- `RAG-05-009` Matryoshka 与可截断向量
- `RAG-05-010` Embedding Benchmark 与业务数据集评估
- `RAG-05-011` 批量 Embedding、缓存与吞吐优化
- `RAG-05-012` Embedding 模型升级与向量重建
- `RAG-05-013` 领域检索器微调、适配器与 Embedding 变换
- `RAG-05-014` 检索器与生成器偏好对齐及 LLM 监督信号
- `RAG-05-015` 指令感知嵌入（Instruction-aware Embedding）与任务条件编码
- `RAG-05-016` 多模态嵌入（Multimodal Embedding）与跨模态检索

## RAG-06 存储与索引

- `RAG-06-001` 向量数据库的职责与普通数据库的差异
- `RAG-06-002` 精确检索与近似最近邻 ANN
- `RAG-06-003` 向量、文本、元数据和主键 Schema
- `RAG-06-004` Document ID、Chunk ID 与 Parent ID
- `RAG-06-005` HNSW 原理、参数与权衡
- `RAG-06-006` IVF 原理、nlist、nprobe 与权衡
- `RAG-06-007` PQ、量化和压缩索引
- `RAG-06-008` 倒排索引、稀疏向量和全文索引
- `RAG-06-009` 向量索引与关键词索引的共存
- `RAG-06-010` 元数据过滤与过滤前后执行顺序
- `RAG-06-011` FAISS、Milvus、Qdrant、Chroma、Pinecone 与 pgvector 选型
- `RAG-06-012` 数据规模、QPS、延迟、召回率和成本基准
- `RAG-06-013` 分区、分片、副本与冷热数据
- `RAG-06-014` 新增、删除、更新和索引 Compaction
- `RAG-06-015` 索引构建、加载、预热和持久化

## RAG-07 Query 理解

- `RAG-07-001` Query 清洗、规范化与语言检测
- `RAG-07-002` 意图识别和是否检索判断
- `RAG-07-003` Query Rewrite 的目标和约束
- `RAG-07-004` Multi-Query 查询扩展
- `RAG-07-005` HyDE 假设文档嵌入
- `RAG-07-006` 复杂问题的子问题分解
- `RAG-07-007` Step-back Prompting
- `RAG-07-008` 实体、时间、地域和权限过滤条件抽取
- `RAG-07-009` 多轮会话中的独立问题改写
- `RAG-07-010` 查询路由与知识源选择
- `RAG-07-011` Query 增强失败、语义漂移与约束
- `RAG-07-012` Query 增强策略的离线评估

## RAG-08 检索、融合与重排

- `RAG-08-001` Dense Retrieval 语义检索
- `RAG-08-002` Sparse Retrieval 与关键词检索
- `RAG-08-003` BM25 原理、参数和局限
- `RAG-08-004` Hybrid Search 混合检索
- `RAG-08-005` 多路召回的通道设计
- `RAG-08-006` RRF 排名融合
- `RAG-08-007` 加权分数融合与分数归一化
- `RAG-08-008` Top-K、相似度阈值与动态候选集
- `RAG-08-009` Bi-Encoder 与 Cross-Encoder
- `RAG-08-010` Reranker 模型选择、批处理和阈值
- `RAG-08-011` MMR、去重和结果多样性
- `RAG-08-012` 时间衰减、新鲜度和热度信号
- `RAG-08-013` 多跳、迭代和依赖前序结果的检索
- `RAG-08-014` 检索结果过滤与可信来源控制
- `RAG-08-015` 低相关、零召回和噪声召回的恢复策略
- `RAG-08-016` 检索阶段延迟、并发和缓存优化

## RAG-09 上下文与生成

- `RAG-09-001` System Prompt、问题、证据和输出约束的组装
- `RAG-09-002` 上下文预算与 Token 分配
- `RAG-09-003` 检索结果排序和上下文位置
- `RAG-09-004` Lost in the Middle 问题与缓解
- `RAG-09-005` Contextual Compression 与证据压缩
- `RAG-09-006` 基于证据的 Grounded Generation
- `RAG-09-007` 引用编号、出处和可追溯答案
- `RAG-09-008` 证据不足时的拒答与不确定性表达
- `RAG-09-009` RAG 幻觉类型和产生链路
- `RAG-09-010` 生成后事实核查与证据对齐
- `RAG-09-011` 来源可信度与多源交叉验证
- `RAG-09-012` 事实、观点和推断的区分
- `RAG-09-013` 来源冲突、时效冲突和答案合并
- `RAG-09-014` 结构化输出与答案 Schema
- `RAG-09-015` 长上下文与 Prompt Caching 的边界
- `RAG-09-016` 面向检索证据输入的生成器适配与微调

## RAG-10 评估

- `RAG-10-001` 解析、检索、生成和端到端分层评估
- `RAG-10-002` Golden Dataset 与问题、答案、证据标注
- `RAG-10-003` 人工数据、日志数据和合成数据构建
- `RAG-10-004` Precision、Recall、Hit Rate 与 Coverage
- `RAG-10-005` MRR、MAP 与 nDCG 排序指标
- `RAG-10-006` Reranker 评估和候选集条件
- `RAG-10-007` Answer Correctness、Relevancy 与 Completeness
- `RAG-10-008` Faithfulness、Groundedness 与幻觉评估
- `RAG-10-009` Citation Accuracy 与 Citation Completeness
- `RAG-10-010` RAGAS 等自动评测框架
- `RAG-10-011` LLM-as-a-Judge 的偏差和校准
- `RAG-10-012` 人工抽检、评分标准和一致性
- `RAG-10-013` 线上任务成功、满意度和 A/B 实验
- `RAG-10-014` 失败归因、消融实验与回归测试

## RAG-11 生产工程与治理

- `RAG-11-001` 文档变更检测、哈希和事件来源
- `RAG-11-002` 新增、修改、删除的增量更新
- `RAG-11-003` 新旧数据和模型分布不一致
- `RAG-11-004` 索引版本、双写、灰度和原子切换
- `RAG-11-005` 知识新鲜度、时间衰减和过期策略
- `RAG-11-006` Embedding、检索、Rerank 和答案缓存
- `RAG-11-007` 批处理、异步和并行流水线
- `RAG-11-008` 在线延迟预算与阶段耗时拆解
- `RAG-11-009` 高并发、限流、背压和资源隔离
- `RAG-11-010` 超时、重试、熔断和故障转移
- `RAG-11-011` 检索和生成降级策略
- `RAG-11-012` 多租户数据隔离
- `RAG-11-013` 文档级、Chunk 级 ACL 权限过滤
- `RAG-11-014` PII、数据保留和删除合规
- `RAG-11-015` 间接 Prompt Injection 与恶意文档
- `RAG-11-016` 数据投毒、来源伪造和信息泄露
- `RAG-11-017` Tracing、日志、反馈和可观测性
- `RAG-11-018` Token、模型、存储和检索成本优化
- `RAG-11-019` 备份、恢复、重建和灾难恢复

## RAG-12 高级范式

- `RAG-12-001` Naive RAG 的流程和局限
- `RAG-12-002` Advanced RAG 的查询、检索和生成优化
- `RAG-12-003` Modular RAG 的组件化和路由
- `RAG-12-004` Agentic RAG 的动态决策闭环
- `RAG-12-005` Adaptive Retrieval 与是否检索判断
- `RAG-12-006` Self-RAG 的检索和反思控制
- `RAG-12-007` CRAG 的检索评估和纠错
- `RAG-12-008` Multi-Step 与 Iterative Retrieval
- `RAG-12-009` GraphRAG 的图构建、社区和全局检索
- `RAG-12-010` 知识图谱与向量检索的组合
- `RAG-12-011` 多模态 RAG 的解析、索引、路由和生成
- `RAG-12-012` 视觉文档检索与 Late Interaction
- `RAG-12-013` Agentic Search 与传统搜索、传统 RAG
- `RAG-12-014` Deep Research 的任务分解和搜索规划
- `RAG-12-015` Deep Research 的多源交叉验证
- `RAG-12-016` 信息饱和、搜索预算和停止条件
- `RAG-12-017` 长研究任务的中间证据和上下文组织
- `RAG-12-018` 高级 RAG 的成本、风险和适用边界
- `RAG-12-019` RAG 范式的概念与分类维度
- `RAG-12-020` GraphRAG 的 Local、Global、DRIFT 与基础搜索模式

## RAG-13 项目与面试应用

- `RAG-13-002` RAG 完整流程口述
- `RAG-13-003` 从零设计企业 RAG 系统
- `RAG-13-004` Chunk、Embedding、向量库和 Reranker 选型表达
- `RAG-13-005` 检索优化方案和实验依据
- `RAG-13-006` RAG 框架、平台和开源项目选型
- `RAG-13-007` 最小 RAG 与生产级代码结构
- `RAG-13-008` 无召回、噪声、幻觉和高延迟排障
- `RAG-13-009` 用指标证明 RAG 优化效果
- `RAG-13-010` RAG 项目 STAR 叙事
- `RAG-13-011` 不同岗位的 RAG 回答深度
- `RAG-13-012` 原始面试题、追问与标准知识双向映射

---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-CONTEXT-ASSEMBLY
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 上下文组装（Context Assembly）第三轮独立补漏

## 1. 本轮目标与边界

本轮固定当前框架源码，区分文档过滤（Document Filtering）、内容抽取（Content Extraction）、摘要改写（Summarization Rewrite）和令牌预算管理（Token-budget Management）。上下文压缩检索器（Contextual Compression Retriever）只是“先检索、后压缩”的包装器；具体压缩器是否删除整篇文档、改写正文、保留元数据和引用跨度，必须逐实现核验。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 当前实现（Current Implementation） | `repo:langchain-ai/langchain ContextualCompressionRetriever BaseDocumentCompressor` | LangChain 官方仓库（Official Repository） |
| Q-302 | 抽取压缩（Extractive Compression） | `repo:langchain-ai/langchain LLMChainExtractor NO_OUTPUT metadata` | LangChain 官方仓库（Official Repository） |
| Q-303 | 嵌入过滤（Embedding Filter） | `repo:langchain-ai/langchain EmbeddingsFilter similarity_threshold k` | LangChain 官方仓库（Official Repository） |
| Q-304 | 冲突上下文（Conflicting Context） | `ConflictRAG inter-document factual temporal opinion conflict detect resolve generate` | arXiv 原始论文（Original Paper） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com RAG 上下文压缩 Lost in the Middle 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `langchain-contextual-compression-retriever-2026` | 官方仓库源码（Official Repository Source） | `included` | 固定提交，证明基础检索器（Base Retriever）先执行，存在候选后才调用基础压缩器（Base Compressor） |
| `langchain-llm-chain-extractor-2026` | 官方仓库源码（Official Repository Source） | `included` | 补逐文档大语言模型抽取（LLM Extraction）、`NO_OUTPUT` 整篇删除和原元数据复制行为 |
| `langchain-embeddings-filter-2026` | 官方仓库源码（Official Repository Source） | `included` | 补 Top-K（前 K 项）与相似度阈值（Similarity Threshold）过滤，它选择文档而不改写正文 |
| `conflictrag-2026` | 预印本（Preprint） | `included` | 补文档间冲突（Inter-document Conflict）的事实、时间和观点类型化处理路线 |
| `nowcoder-agent-rag-question-bank-2-2026` | 公开题库（Public Question Bank） | `included_duplicate_type` | 新增题目出处，但其上下文压缩与 Lost in the Middle（中间信息丢失）仍映射既有题型，不复制问题 |

## 4. 当前实现边界

| 组件 | 实际行为 | 不是它保证的内容 |
|---|---|---|
| ContextualCompressionRetriever（上下文压缩检索器） | 调用基础检索器（Base Retriever），再把候选和查询交给基础压缩器（Base Compressor）；同步和异步路径均存在 | 不自动执行全局令牌预算（Global Token Budget）、去重、引用跨度校验或事实保真校验 |
| EmbeddingsFilter（嵌入过滤器） | 按查询—文档嵌入相似度选择 Top-K（前 K 项）和/或超过阈值的完整文档 | 不做句子抽取、内容改写或事实级压缩 |
| LLMChainExtractor（大语言模型链式抽取器） | 对每篇文档单独生成相关内容；空输出时删除该文档；新正文沿用原文档元数据 | 元数据被复制不等于新正文仍能映射到原始字符、页码或单元格跨度 |

## 5. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `CTX-K-301` | `knowledge` | “上下文压缩（Context Compression）”是策略族：文档选择、片段抽取、摘要改写和表示压缩会丢失不同信息，不能共用一个无条件的保真结论 | 三项 LangChain 固定源码；`sara-context-compression-2026` | `new` |
| `CTX-P-301` | `problem_question` | 逐文档压缩（Per-document Compression）各自看似合理，但没有全局预算和跨文档去重时，总上下文仍可能超限或被同源证据占满 | `langchain-contextual-compression-retriever-2026` | `new` |
| `CTX-P-302` | `problem_question` | LLMChainExtractor（大语言模型链式抽取器）把改写后的正文与原元数据直接组合；若调用方把旧页码或字符范围当作新文本的精确引用锚点，会产生来源错位 | `langchain-llm-chain-extractor-2026` | `new` |
| `CTX-P-303` | `problem_question` | `NO_OUTPUT` 或相似度阈值会整篇删除候选；当关键限定词分散在另一文档时，压缩阶段会制造下游不可恢复的证据缺口 | 两项压缩器源码 | `new` |
| `CTX-P-304` | `problem_question` | 事实冲突、时间演化和观点差异若统一压成一个摘要，会把“存在分歧”误写成单一确定事实 | `conflictrag-2026` | `new` |
| `CTX-S-301` | `solution` | 先建立不可变证据包（Immutable Evidence Package），再产生带派生关系和跨度映射的压缩表示；最终按查询子目标、来源多样性、冲突组、信任域和令牌预算联合装箱 | 新增与既有来源 | `extends` |
| `CTX-E-301` | `evaluation` | 对选择式、抽取式和改写式压缩分别记录原子事实保留、数字/否定/日期保留、原始跨度可逆性、整篇删除率、跨文档覆盖、重复率、冲突保留和实际 Token（词元）用量 | 新增与既有来源 | `new` |

## 6. 公开面试题来源核验

新增登记一个公开题库来源，但没有新增题目编号。其上下文压缩（Context Compression）、Lost in the Middle（中间信息丢失）、完整流程和评估问题均与 `RAG-SCENE-020`、`RAG-SCENE-021`、`RAG-SCENE-024` 重合；保留来源多样性，不复制同型问题。

## 7. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 预算、位置、过滤、抽取、改写、冲突和保真已覆盖 |
| 实现（Implementation） | `covered` | 固定 LangChain 源码（LangChain Source）已补，不再只依赖旧模块页 |
| 工程问题（Engineering Problem） | `covered` | 全局超限、锚点错位、整篇误删、重复、冲突压平和注入已登记 |
| 解决方案（Solution） | `covered` | 不可变证据包、派生边、跨度映射、冲突分组和全局预算已覆盖 |
| 评估（Evaluation） | `covered` | 按压缩机制分层的质量、成本和可逆性指标已定义 |
| 公开面试题（Public Interview Question） | `covered` | 新来源映射既有题型，未虚构题目 |
| 时效（Freshness） | `covered` | 固定当前源码提交并登记 2026 研究 |
| 安全或治理（Security or Governance） | `covered` | 信任分区、权限、派生来源和间接提示注入（Indirect Prompt Injection）已覆盖 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接检索、融合、重排、生成、引用和评估 |

## 8. 冲突、版本与未验证假设

- LangChain Classic（LangChain 经典模块）当前源码是产品实现，不是上下文压缩（Context Compression）的统一标准；版本升级必须重新检查导入路径与行为。
- LLMChainExtractor（大语言模型链式抽取器）名称含“Extractor（抽取器）”，但输出来自生成模型；没有对齐测试时不能假设逐字抽取或无幻觉。
- ConflictRAG（冲突感知检索增强生成）的阈值、分类器和收益来自预印本实验；本项目只采用“先检测、分类、再决策”的结构，不照搬数值。
- 上下文分隔符（Context Delimiter）是软防线；不能代替权限、输出验证和工具授权。

## 9. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 4 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 10. 下一轮动作

基于固定源码建立三类压缩器回放：文档过滤（Document Filtering）、内容抽取（Content Extraction）和摘要改写（Summarization Rewrite）；加入中文 UTF-8（八位统一码转换格式）跨度、表格单元格、父子块、冲突组和恶意指令样本。

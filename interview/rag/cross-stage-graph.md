# 跨节点问题关系视图（Cross-stage Problem Graph View）

> 状态：`candidate / WP-P6-001 / graph-backed / inventory-only`
>
> 本视图由 `problem_at` 经知识原子反向连接到流程节点，并统计共享问题数量；不新增关系。

## 节点对重叠（Stage-pair Overlap）

| 节点 A | 节点 B | 共享问题数 |
|---|---|---:|
| 检索（Retrieval） [`PS-RETRIEVAL`] | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 10 |
| 检索（Retrieval） [`PS-RETRIEVAL`] | 重排（Reranking） [`PS-RERANKING`] | 10 |
| 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 重排（Reranking） [`PS-RERANKING`] | 10 |
| 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 5 |
| 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 5 |
| 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 5 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 4 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 4 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 4 |
| 检索（Retrieval） [`PS-RETRIEVAL`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 4 |
| 检索（Retrieval） [`PS-RETRIEVAL`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 4 |
| 检索（Retrieval） [`PS-RETRIEVAL`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 4 |
| 检索（Retrieval） [`PS-RETRIEVAL`] | 评估（Evaluation） [`PS-EVALUATION`] | 4 |
| 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 4 |
| 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 4 |
| 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 4 |
| 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 评估（Evaluation） [`PS-EVALUATION`] | 4 |
| 重排（Reranking） [`PS-RERANKING`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 4 |
| 重排（Reranking） [`PS-RERANKING`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 4 |
| 重排（Reranking） [`PS-RERANKING`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 4 |
| 重排（Reranking） [`PS-RERANKING`] | 评估（Evaluation） [`PS-EVALUATION`] | 4 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 文本切分（Chunking） [`PS-CHUNKING`] | 3 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 3 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 文本切分（Chunking） [`PS-CHUNKING`] | 3 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 3 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 评估（Evaluation） [`PS-EVALUATION`] | 3 |
| 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 评估（Evaluation） [`PS-EVALUATION`] | 3 |
| 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 评估（Evaluation） [`PS-EVALUATION`] | 3 |
| 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 评估（Evaluation） [`PS-EVALUATION`] | 3 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 2 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 2 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 2 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 2 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 2 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 评估（Evaluation） [`PS-EVALUATION`] | 2 |
| 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`] | 检索（Retrieval） [`PS-RETRIEVAL`] | 2 |
| 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`] | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 2 |
| 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`] | 重排（Reranking） [`PS-RERANKING`] | 2 |
| 检索（Retrieval） [`PS-RETRIEVAL`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 2 |
| 检索（Retrieval） [`PS-RETRIEVAL`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 2 |
| 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 2 |
| 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 2 |
| 重排（Reranking） [`PS-RERANKING`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 2 |
| 重排（Reranking） [`PS-RERANKING`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 2 |
| 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 2 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 向量嵌入（Embedding） [`PS-EMBEDDING`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 检索（Retrieval） [`PS-RETRIEVAL`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 重排（Reranking） [`PS-RERANKING`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 评估（Evaluation） [`PS-EVALUATION`] | 1 |
| 文档解析（Document Parsing） [`PS-DOCUMENT-PARSING`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 向量嵌入（Embedding） [`PS-EMBEDDING`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 检索（Retrieval） [`PS-RETRIEVAL`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 重排（Reranking） [`PS-RERANKING`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 评估（Evaluation） [`PS-EVALUATION`] | 1 |
| 数据治理（Data Governance） [`PS-DATA-GOVERNANCE`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 向量嵌入（Embedding） [`PS-EMBEDDING`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 检索（Retrieval） [`PS-RETRIEVAL`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 重排（Reranking） [`PS-RERANKING`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 1 |
| 文本切分（Chunking） [`PS-CHUNKING`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 1 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 检索（Retrieval） [`PS-RETRIEVAL`] | 1 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 1 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 重排（Reranking） [`PS-RERANKING`] | 1 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 1 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 1 |
| 向量嵌入（Embedding） [`PS-EMBEDDING`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 1 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 检索（Retrieval） [`PS-RETRIEVAL`] | 1 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 结果融合（Result Fusion） [`PS-RESULT-FUSION`] | 1 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 重排（Reranking） [`PS-RERANKING`] | 1 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 1 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 1 |
| 存储与索引（Storage and Indexing） [`PS-STORAGE-INDEXING`] | 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 1 |
| 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`] | 评估（Evaluation） [`PS-EVALUATION`] | 1 |
| 查询理解（Query Understanding） [`PS-QUERY-UNDERSTANDING`] | 高级检索增强生成（Advanced RAG） [`PS-ADVANCED-RAG`] | 1 |
| 上下文组装（Context Assembly） [`PS-CONTEXT-ASSEMBLY`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 1 |
| 答案生成（Answer Generation） [`PS-ANSWER-GENERATION`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 1 |
| 引用与验证（Citation and Verification） [`PS-CITATION-VERIFICATION`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 1 |
| 评估（Evaluation） [`PS-EVALUATION`] | 生产治理（Production Governance） [`PS-PRODUCTION-GOVERNANCE`] | 1 |

## 生成限制（Limits）

- 共享问题数来自现有问题节点的 `problem_at` 与知识原子的 `contains` 关系。
- 该视图用于定位跨节点复习路径，不等同于正式系统设计方案或因果证明。
- 来源、解决方案和评估证据仍需回到问题库存及图谱原始关系。

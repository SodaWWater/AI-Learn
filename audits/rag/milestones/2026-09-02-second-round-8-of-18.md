# 检索增强生成（Retrieval-Augmented Generation，RAG）第二轮 8/18 检查点

日期：2026-09-02  
工作项：`WP-P2-002`  
状态：`in_progress`

## 本检查点结果

- 第一轮节点检索：18/18；
- 第二轮节点检索：8/18；
- 已登记来源：98；
- 已登记公开工程问题/面试题线索：22；
- 当前覆盖饱和（coverage_saturated）节点：0/18。

本批完成：

1. 向量嵌入（Embedding）；
2. 存储与索引（Storage and Indexing）；
3. 查询理解（Query Understanding）；
4. 查询改写（Query Rewrite）。

## 本批新增的重要边界

- 向量模型（Embedding Model）的 Prompt、输入类型、Pooling、Normalization、Dimension、Precision 和模型修订共同构成索引兼容契约；
- 困难负样本（Hard Negative）挖掘必须控制假负例（False Negative），量化（Quantization）必须使用代表性校准集并做分层回归；
- HNSW、IVF-PQ 和 DiskANN 的内存、磁盘、训练、更新和过滤假设不同；
- 多租户（Multitenancy）、副本一致性（Replica Consistency）、压缩整理（Compaction）和备份恢复（Backup and Restore）是不同能力面；
- 查询理解（Query Understanding）可以抽取业务 Metadata Filter，但授权主体（Authorization Principal）必须来自可信身份上下文；
- 多查询扩展（Multi-query Expansion）必须与结果融合（Result Fusion）联合设计和评估，并保留原查询 Control Branch。

## 为什么仍未标记覆盖饱和

四个节点的第二轮均发现了新的知识类型或问题类型，连续无新增类型轮数仍为 0。根据项目规则，节点至少还需要连续两轮独立补漏没有新增知识或问题类型，并完成其余来源、冲突和九类覆盖前置项，才能标记为当前版本的 `coverage_saturated`。

## 下一步

继续第二轮：查询路由（Query Routing）、检索（Retrieval）、结果融合（Result Fusion）和重排（Reranking）；随后处理上下文组装（Context Assembly）至高级检索增强生成（Advanced RAG）。

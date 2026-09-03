# 检索增强生成（Retrieval-Augmented Generation，RAG）第三轮 8/18 检查点

日期：2026-09-03

工作项：`WP-P2-002`

状态：`in_progress`

## 本检查点结果

- 第一轮节点检索：18/18；
- 第二轮节点检索：18/18；
- 第三轮节点检索：8/18；
- 已登记来源：141；
- 已登记公开工程问题/面试题线索：24；
- 当前覆盖饱和（Coverage Saturated）节点：0/18。

本批完成 Embedding（嵌入）、Storage and Indexing（存储与索引）、Query Understanding（查询理解）和 Query Rewrite（查询改写）的第三轮独立补漏。

## 本批新增的重要边界

- Embedding Model Migration（嵌入模型迁移）存在 Blue-green Collection（蓝绿集合）与 Named Vector（命名向量）两种物理路线；Dual Write（双写）不能天然覆盖 Delete（删除）和 Partial Update（部分更新）；
- Vector（向量）是可重建的派生数据，Deterministic Point ID（确定性点标识符）与 Content Fingerprint（内容指纹）分别表达位置和内容，必须与模型、切分、缓存和索引版本共同登记；
- 第三方 Embedding API（嵌入应用程序编程接口）的“不会训练”不等于没有跨区处理、状态存储或滥用监控日志，供应商与部署类型必须逐项审核；
- ANN Recall（近似最近邻召回率）只评价近似索引对 Exact kNN（精确 K 近邻）的逼近，不等于 Retrieval Relevance（检索相关性）或 Business Impact（业务影响）；
- Vector Index Benchmark（向量索引基准）必须固定数据集、Embedding Model（嵌入模型）、算法版本、硬件、线程、精度和查询分布，并额外补业务过滤、热租户和混合读写负载；
- 查询理解各组件的 Confidence（置信度）不能压成一个标量；下游 Verbal Confidence（口头置信度）会被检索噪声污染，不能反推上游解析正确；
- 中文 Named Entity Recognition（命名实体识别）、Entity Linking（实体链接）、Geocoding（地理编码）与 Temporal Expression Normalization（时间表达归一化）是相邻但不同的处理节点；
- LangChain MultiQueryRetriever（LangChain 多查询检索器）和 LlamaIndex QueryFusionRetriever（LlamaIndex 查询融合检索器）的默认原查询、分支数、并发与融合语义不同，必须固定 Source Commit（源码提交）；
- 每个 Rewrite Branch（改写分支）都必须重新绑定可信 Authorization Filter（授权过滤器），并记录分支级 Trace（追踪）和 Counterfactual Ablation（反事实消融）。

## 公开面试题处理

本轮公开搜索命中已登记的 `RAG-SCENE-012/013/014/015/017/018/022` 问题类型。新增内容扩展其生产迁移、索引基准、查询理解和改写实现分支；没有发现独立问题条件，因此不复制题目，公开题目计数保持 24。

## 为什么仍未标记覆盖饱和

本批四个节点仍发现新的知识或工程问题类型，连续无新增类型轮数全部重置为 0。第三轮仍有 10 个节点未处理；已完成节点也必须再经历连续两轮独立无新增类型并满足所有前置项，才允许标记覆盖饱和（Coverage Saturated）。

## 下一步

继续第三轮剩余 10 个节点。下一批优先处理 Query Routing（查询路由）、Retrieval（检索）、Result Fusion（结果融合）和 Reranking（重排序）；同时保留本批未完成的可执行评测协议作为后续知识图谱与实践资产，不提前把审计日志包装成正式学习正文。

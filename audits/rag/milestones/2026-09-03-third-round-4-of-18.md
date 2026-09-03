# 检索增强生成（Retrieval-Augmented Generation，RAG）第三轮 4/18 检查点

日期：2026-09-03

工作项：`WP-P2-002`

状态：`in_progress`

## 本检查点结果

- 第一轮节点检索：18/18；
- 第二轮节点检索：18/18；
- 第三轮节点检索：4/18；
- 已登记来源：130；
- 已登记公开工程问题/面试题线索：24；
- 当前覆盖饱和（Coverage Saturated）节点：0/18。

本批完成数据摄取（Data Ingestion）、文档解析（Document Parsing）、数据治理（Data Governance）和文本切分（Chunking）的第三轮独立补漏。

## 本批新增的重要边界

- Incremental Snapshot（增量快照）需要水位窗口与并发 CDC（变更数据捕获）事件冲突消解；连接器参与 Exactly-once（精确一次）不代表 RAG 派生链路端到端精确一次；
- Schema Evolution（模式演进）的兼容模式决定生产者与消费者升级顺序，历史回放还需要传递兼容性；
- Page-level Evaluation（页面级评测）无法覆盖跨页文本/表格合并和文档级标题树，解析验收必须扩展到 Document-level Evaluation（文档级评测）；
- Lineage（数据血缘）应建模为 Entity/Activity/Agent（实体/活动/主体）的派生与失效图，不能退化为一个来源链接；
- Erasure（删除）、Access Revocation（访问撤销）、Cryptographic Erasure（密码学擦除）和 Backup Expiration（备份过期）是不同状态；
- Sentence-window/Parent-child Retrieval（句子窗口/父子检索）形成“小粒度索引—大粒度返回”的双表示契约，必须原子维护版本、权限和删除映射；
- Chunking Evaluation（文本切分评估）要同时衡量质量、计算、Embedding（嵌入）、索引、存储、在线 Token 和更新成本。

## 公开面试题处理

本轮公开题目搜索命中 `RAG-SCENE-007/008/009/010/011/022` 已登记类型。新增知识作为这些题目的工程追问分支，不为凑数量复制题目，也不把技术文章伪装成真实面经。

## 为什么仍未标记覆盖饱和

四个节点都发现了新的知识或问题类型，因此连续无新增类型轮数仍为 0。其余 14 个节点尚未执行第三轮。只有某节点连续两轮独立补漏均无新增类型，并满足来源、冲突、九类覆盖、公开题目和图谱前置项，才允许标记覆盖饱和（Coverage Saturated）。

## 下一步

继续第三轮剩余 14 个节点，下一批优先处理 Embedding（嵌入）、Storage and Indexing（存储与索引）、Query Understanding（查询理解）和 Query Rewrite（查询改写）；若仍发现新类型，继续重置对应节点的无新增计数。

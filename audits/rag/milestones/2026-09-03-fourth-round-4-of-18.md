# 检索增强生成（Retrieval-Augmented Generation，RAG）第四轮 4/18 检查点

日期：2026-09-03

工作项：`WP-P2-002`

状态：`in_progress`

## 当前进度

- 第一、第二、第三轮：各 18/18；
- 第四轮：4/18；
- 已登记来源：170；
- 已登记公开工程问题/面试题线索：26；
- 覆盖饱和（Coverage Saturated）节点：0/18。

## 本批完成节点

- Data Ingestion（数据摄取）：补 Connector Capability Negotiation（连接器能力协商）、配置相关 Exactly-once（精确一次）声明、位点修改幂等和端到端对账边界；
- Document Parsing（文档解析）：补类型化中间表示、Body/Furniture（正文/版面附属物）、可见与不可见 PDF 文本、能力未知与空结果的三态，以及结构引用锚点；
- Data Governance（数据治理）：用 OpenLineage（开放数据血缘）区分设计时与运行时事件，建立 RAG 派生资产的 Job/Run/Dataset（作业/运行/数据集）映射边界；
- Chunking（文本切分）：补 Proposition Chunking（命题切分）的原始论文定义、生成误差、来源跨度、离线成本和统一预算评测。

## 饱和判断

四个节点均发现新知识或问题类型，连续无新增类型计数保持 0。第四轮继续处理 Embedding（嵌入）到 Advanced RAG（高级检索增强生成）的剩余 14 个节点。

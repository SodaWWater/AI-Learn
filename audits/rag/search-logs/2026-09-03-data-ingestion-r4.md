---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DATA-INGESTION
round: 4
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 数据摄取（Data Ingestion）第四轮独立补漏

## 1. 独立检索设计

本轮不复用增量快照查询，改从 Connector Capability Negotiation（连接器能力协商）、Offset Mutation（位点修改）、事务边界与派生数据血缘反查端到端 Reconciliation（对账）。来源族改为 Apache Kafka API（Apache Kafka 应用程序接口）和 OpenLineage Specification（OpenLineage 规范）。

| 检索族 | 查询或入口 | 独立性 |
|---|---|---|
| 能力协商（Capability Negotiation） | `Kafka SourceConnector exactlyOnceSupport proposed configuration transaction boundary` | 从运行时接口而非 CDC（变更数据捕获）文章核验 |
| 恢复控制（Recovery Control） | `Kafka SourceConnector alterOffsets idempotent reset retry` | 从人工位点操作反查重放风险 |
| 派生血缘（Derived Lineage） | `OpenLineage Job Run Dataset lifecycle version source code location` | 跨治理、解析、切分和索引节点 |
| 冲突查询（Conflict Search） | `exactly once connector unsupported configuration worker guarantee boundary` | 主动验证“启用平台配置即可精确一次”的反例 |

## 2. 来源处理

| 来源 ID | 状态 | 用途 |
|---|---|---|
| `kafka-source-connector-api-4-3-1` | `included` | Exact-once（精确一次）能力依赖连接器实现和拟议配置；事务边界能力也需连接器声明 |
| `openlineage-object-model-1-53-0` | `included_cross_stage` | 用 Job/Run/Dataset（作业/运行/数据集）记录源数据到派生资产的运行与设计血缘 |
| `debezium-incremental-snapshots-2021` | `included_existing` | 与第四轮接口证据交叉核验 At-least-once（至少一次）边界 |

## 3. 新增类型与工程链路

| 类型 ID | 类别 | 内容 | 关系 |
|---|---|---|---|
| `ING-K-401` | `knowledge` | Exactly-once Support（精确一次支持）是连接器在给定配置下声明的能力，不是 Kafka Connect（Kafka 连接框架）全局开关自动赋予的属性；未覆写能力接口时应视为不支持 | `new` |
| `ING-P-401` | `problem_question` | 灾难恢复时人工 Reset/Alter Offset（重置/修改位点）可能被重试；若连接器、索引写入和对账任务不具幂等性，会重复回放或跳过变更 | `new` |
| `ING-P-402` | `problem_question` | 只记录消息位点不能证明文档、解析结果、Chunk（文本块）、Embedding（嵌入）和索引属于同一次成功 Run（运行）；中间节点失败会留下部分派生状态 | `new` |
| `ING-S-401` | `solution` | 启动前检查连接器对当前配置的能力声明；恢复操作保存旧新位点、操作者、原因和幂等请求 ID（标识），随后按源主键与版本对账派生对象 | `extends` |
| `ING-E-401` | `evaluation` | 故障注入覆盖提交前崩溃、提交后确认丢失、位点修改重试、乱序更新、删除 Tombstone（墓碑）和派生节点部分成功；比较源端真值与最终索引版本集合 | `extends` |

工程链路为：Source Snapshot/Log（源快照/日志）→ Connector Transaction（连接器事务）→ Durable Offset（持久位点）→ Parse Run（解析运行）→ Chunk/Embedding Run（切分/嵌入运行）→ Index Commit（索引提交）→ Reconciliation（对账）。每段都记录输入输出 Dataset Version（数据集版本）和 Run ID（运行标识），但仍需目标技术栈故障注入证明。

## 4. 公开题与覆盖检查

没有检索到条件独立的新公开面试问题；现有 `RAG-SCENE-008/009/013/022` 已覆盖增量、删除、迁移和恢复，但第四轮新增的是连接器能力协商与位点管理接口证据。九类覆盖中公开题仍为 `covered`，可执行跨系统对账仍为 `partial`。

## 5. 冲突与边界

- Source Connector（源连接器）声明支持 Exactly-once（精确一次），不推出解析器、向量数据库和引用缓存端到端精确一次。
- OpenLineage（开放数据血缘）定义通用 Job/Run/Dataset（作业/运行/数据集）；把单文档或单 Chunk（文本块）建模为 Dataset（数据集）可能造成高基数，粒度需实验决定。
- 位点重置的幂等性只说明相同控制操作可重复调用，不说明其触发的所有下游副作用自动幂等。

## 6. 饱和判定与下一步

本轮新增知识类型 1、问题类型 2；连续无新增类型轮数重置并保持 0，状态为 `round_complete`。下一轮需执行一套具体 Source Connector（源连接器）—解析器—向量库故障矩阵并生成差异报告。

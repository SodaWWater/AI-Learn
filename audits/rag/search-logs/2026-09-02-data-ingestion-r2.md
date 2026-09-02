---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DATA-INGESTION
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 数据摄取（Data Ingestion）第二轮独立补漏

## 1. 本轮目标与边界

补查数据库变更捕获（Change Data Capture，CDC）、事件顺序、删除传播和数据生命周期，独立于第一轮的 Azure Indexer 路线。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 实现 | `site:debezium.io/documentation/reference/stable incremental snapshots official` | Debezium 官方文档 |
| Q-202 | 架构 | `site:debezium.io/documentation/reference/stable architecture change data capture official` | Debezium 官方文档 |
| Q-203 | 治理 | `site:docs.aws.amazon.com prescriptive guidance data lifecycle generative AI RAG` | AWS 官方文档 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `debezium-features-docs-2026` | 官方文档 | `included` | 新增 Log-based CDC 路线 |
| `debezium-architecture-docs-2026` | 官方文档 | `included` | 新增 Source/Sink 事件传播架构 |
| `aws-genai-data-lifecycle-guidance-2026` | 官方文档 | `included` | 补数据生命周期和云上治理 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关系 |
|---|---|---|---|
| `ING-K-201` | `implementation` | 用 Log-based CDC 连接源数据库变更和索引更新 | `new` |
| `ING-P-201` | `problem_question` | 变更事件重复、乱序或删除事件遗漏造成索引漂移 | `new` |

## 5. 公开面试题来源核验

本轮未发现新的高可信公开题目类型；继续沿 `RAG-SCENE-009` 的更新删除问题补技术证据。

## 6. 九类覆盖检查

原理、实现、工程问题和跨节点关系新增 CDC 覆盖；Schema Evolution、Snapshot/Streaming 切换和 Exactly-once 边界仍为缺口。

## 7. 冲突、版本与未验证假设

Log-based CDC 的“捕获全部变更”不等于下游索引 Exactly-once；仍需幂等键、顺序和重放策略。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 1 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

补 Incremental Snapshot、Schema Evolution、Outbox/CDC 选择、重放和幂等。

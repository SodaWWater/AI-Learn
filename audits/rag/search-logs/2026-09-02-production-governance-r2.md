---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-PRODUCTION-GOVERNANCE
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 生产治理（Production Governance）第二轮独立补漏

## 1. 本轮目标与边界

专项补查多租户隔离（Multitenancy Isolation）、缓存污染（Cache Poisoning）、服务级目标（Service Level Objective，SLO）、恢复点目标（Recovery Point Objective，RPO）、恢复时间目标（Recovery Time Objective，RTO）、人工智能事件响应（AI Incident Response）、红队（Red Teaming）和容量成本模型（Capacity and Cost Model）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 事件响应（Incident Response） | `site:nist.gov incident response preparation AI systems` | NIST 官方指导（Official Guidance） |
| Q-202 | 风险清单（Risk Inventory） | `site:owasp.org Top 10 LLM applications 2025 RAG poisoning` | OWASP 官方项目（Official Project） |
| Q-203 | 数据库恢复（Database Recovery） | `Milvus backup restore Qdrant consistency multitenancy official` | 数据库官方文档（Official Documentation） |
| Q-204 | 公开题目（Public Question） | `site:nowcoder.com RAG multitenant disaster recovery prompt injection interview` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `nist-ai-incident-response-2026` | 官方指导（Official Guidance） | `included` | 补准备、职责、证据保全、演练和恢复闭环 |
| `owasp-llm-top10-2025` | 官方项目（Official Project） | `included_existing` | 已覆盖提示注入、敏感信息泄露、供应链和向量/嵌入弱点 |
| `qdrant-multitenancy-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 已覆盖基于 Payload（载荷）的租户隔离边界 |
| `milvus-backup-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 已覆盖备份恢复入口，必须用演练验证 RPO/RTO |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `PROD-K-201` | `knowledge` | AI Incident Response（人工智能事件响应）除基础设施故障外还需处理模型、数据、提示、检索轨迹和第三方服务证据 | `nist-ai-incident-response-2026` | `new` |
| `PROD-P-201` | `problem_question` | 缓存键未包含租户、权限、索引版本、模型版本和策略版本时，可能跨租户泄露或复用过期答案 | 既有缓存、权限和多租户来源 | `new` |
| `PROD-P-202` | `problem_question` | 有备份文件不等于满足 RPO/RTO；未演练恢复可能在索引、Metadata（元数据）或模型版本不兼容时失败 | `milvus-backup-docs-2026`; `nist-ai-incident-response-2026` | `new` |
| `PROD-P-203` | `problem_question` | 平均延迟符合目标仍可能掩盖重排、迭代检索和大租户导致的 P99 尾延迟及容量争抢 | 既有性能与路由来源 | `new` |
| `PROD-S-201` | `solution` | 事件 Runbook（运行手册）明确检测、隔离、证据保全、撤销凭据、回滚索引/模型、通知、恢复验证和复盘责任 | `nist-ai-incident-response-2026` | `extends` |
| `PROD-E-201` | `evaluation` | 定期执行租户越权、缓存污染、提示注入、索引投毒、依赖故障、备份恢复和流量突增演练并记录恢复结果 | 新增与既有来源 | `new` |

## 5. 公开面试题来源核验

`RAG-SCENE-008`、`RAG-SCENE-013` 和 `RAG-SCENE-022` 已覆盖敏感信息权限、无停机迁移、多租户、P99、备份和恢复；本轮不重复拆题。

## 6. 九类覆盖检查

原理、实现入口、工程问题、解决方案、评估、公开题目、时效、安全治理和跨节点关系均已覆盖。具体 SLO、RPO 和 RTO 数值必须由业务影响分析和演练决定，不在通用知识库中杜撰固定目标。

## 7. 冲突与边界

- 数据库支持租户过滤不等于已实现端到端租户隔离；身份传播、缓存、日志和引用同样需要隔离。
- 高可用（High Availability）与灾难恢复（Disaster Recovery）不是同一能力。
- 安全红队发现率不能证明“系统安全”，只能说明在给定威胁模型和测试集下的表现。

## 8. 饱和判定

本轮新增知识类型 1、问题类型 3；连续无新增类型轮数为 0，结论为 `round_complete`，不得标记饱和。

## 9. 下一轮动作

建立可执行演练矩阵与证据模板；把身份、租户、权限、缓存、索引、模型、提示、第三方服务和引用日志接入统一 Trace（链路追踪）与事件时间线。

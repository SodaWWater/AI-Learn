---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DATA-GOVERNANCE
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 数据治理（Data Governance）第二轮独立补漏

## 1. 本轮目标与边界

补查隐私风险管理、数据生命周期、保留删除与云上生成式 AI 数据策略，不重复第一轮 ACL 和 PII 检索。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 隐私 | `site:nist.gov privacy framework data retention AI official` | NIST |
| Q-202 | 生命周期 | `site:docs.aws.amazon.com data security lifecycle generative AI applications` | AWS |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `nist-privacy-framework-2020` | 官方文档 | `included` | 补隐私风险治理框架 |
| `aws-genai-data-lifecycle-guidance-2026` | 官方文档 | `included` | 补来源到消费的数据生命周期 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关系 |
|---|---|---|---|
| `GOV-K-201` | `knowledge` | 数据治理需覆盖识别、控制、沟通、保护和持续管理 | `new` |
| `GOV-P-201` | `problem_question` | 源数据删除后，Chunk、Embedding、缓存和日志仍残留 | `new` |

## 5. 公开面试题来源核验

未新增题目；`RAG-SCENE-008/009` 已覆盖权限和删除传播问题。

## 6. 九类覆盖检查

隐私和生命周期新增覆盖；许可证、数据驻留、审计证据和删除证明仍缺。

## 7. 冲突、版本与未验证假设

框架级风险管理不等于满足某一法域合规；正式内容需按场景标注法律边界。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 1 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

补许可证、数据驻留、删除证明、Lineage、审计和不同法域适用边界。

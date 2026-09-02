---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RESULT-FUSION
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 结果融合（Result Fusion）第二轮独立补漏

## 1. 本轮目标与边界

专项补查分数归一化（Score Normalization）、CombSUM、CombMNZ、线性融合（Linear Fusion）、加权倒数排名融合（Weighted Reciprocal Rank Fusion）、父子分块去重（Parent-child Chunk Deduplication）和跨权限源合并。融合器（Fusion Layer）合并多个候选列表，不重新编码查询—文档对，也不等同于重排序器（Reranker）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 归一化（Normalization） | `Evaluating Score Normalization Methods in Data Fusion AIRS 2006` | Springer 论文（Paper） |
| Q-202 | 当前实现（Current Implementation） | `site:elastic.co linear retriever weighted normalized scores` | Elasticsearch 官方文档（Official Documentation） |
| Q-203 | 加权融合（Weighted Fusion） | `weighted reciprocal rank fusion retrieval paper` | 论文检索（Paper Search） |
| Q-204 | 混合搜索（Hybrid Search） | `site:learn.microsoft.com hybrid search RRF official` | Microsoft 官方文档（Official Documentation） |
| Q-205 | 公开题目（Public Question） | `site:nowcoder.com RAG RRF 分数融合 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `score-normalization-data-fusion-2006` | 论文（Paper） | `included` | 补齐分数归一化是 CombSUM / CombMNZ 等分数融合的前置契约 |
| `elasticsearch-retrievers-docs-2026` | 官方文档（Official Documentation） | `included_existing_extended` | 既有来源已登记 Linear Retriever（线性检索器）和归一化权重，不创建重复来源 |
| `reciprocal-rank-fusion-2009` | 原始论文（Original Paper） | `included_existing` | 已覆盖 RRF（倒数排名融合）的原始定义 |
| `azure-hybrid-rrf-ranking-2026` | 官方文档（Official Documentation） | `included_existing` | 已覆盖当前 RRF 分数与查询数边界 |
| `weighted-rrf-cybersecurity-2026` | 论文（Paper） | `lead_only` | 领域单一，且用查询内 Min-max Normalization（最小—最大归一化）近似置信度；不足以支持通用校准结论 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `FUS-K-201` | `knowledge` | 排名融合（Rank Fusion）只使用顺序，分数融合（Score Fusion）依赖跨通道分数的可比较契约；二者不可只按公式名字互换 | `score-normalization-data-fusion-2006`; 既有 RRF 来源 | `new` |
| `FUS-P-201` | `problem_question` | Min-max Normalization（最小—最大归一化）对每次返回集合的极值敏感，候选截断或离群值会改变同一文档的归一化分数 | `score-normalization-data-fusion-2006` | `new` |
| `FUS-P-202` | `problem_question` | 父分块和子分块从多路重复返回时，只按文本哈希去重会丢失层级、页码、权限或证据跨度 | 既有分块与融合来源 | `new` |
| `FUS-P-203` | `problem_question` | 来自不同访问控制列表（Access Control List，ACL）的候选不能先无条件融合再过滤，否则排名统计和日志可能泄露无权结果 | 既有安全过滤与融合来源 | `new` |
| `FUS-E-201` | `evaluation` | 融合实验应固定各路候选预算，报告通道独占命中、重合率、贡献消融、分层 NDCG、最终 Recall、延迟和权限违规数 | 新增与既有来源 | `new` |
| `FUS-S-201` | `solution` | 去重键应区分内容身份、文档身份、父子关系、版本和权限域，并在融合前后分别记录候选去向 | 既有元数据、权限和融合来源 | `extends` |

## 5. 公开面试题来源核验

未发现独立于 `RAG-SCENE-018` 的新融合题型。第一人称面经检索仍不足；现有公开工程问题已经覆盖分数不可比、候选重复、RRF（倒数排名融合）、归一化和通道淹没，本轮补全归一化稳定性、层级去重和权限域边界。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | RRF、线性分数融合、CombSUM、CombMNZ 和归一化前提已覆盖 |
| 实现（Implementation） | `covered` | Azure 与 Elasticsearch 当前接口已登记 |
| 工程问题（Engineering Problem） | `covered` | 尺度、极值、通道预算、重复层级、截断和权限域已登记 |
| 解决方案（Solution） | `covered` | 排名融合、归一化、结构化去重、授权前置和通道消融均有位置 |
| 评估（Evaluation） | `covered` | 通道贡献、重合、分层排序、召回、延迟和安全指标已覆盖 |
| 公开面试题（Public Interview Question） | `partial` | 有公开工程场景，尚缺可读取的第一人称融合面经 |
| 时效（Freshness） | `covered` | 经典融合论文与当前产品接口兼顾 |
| 安全或治理（Security or Governance） | `covered` | 已明确授权裁剪不得晚于会暴露候选身份的融合步骤 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接改写、检索、重排、上下文和权限治理 |

## 7. 冲突、版本与未验证假设

- RRF 分数（RRF Score）不是概率；线性融合分数（Linear Fusion Score）也只有在明确归一化契约下才可比较。
- Weighted RRF（加权倒数排名融合）的权重可能把训练流量偏差固化到少数通道，必须按查询类型做消融。
- CombMNZ 会奖励多通道共同命中，但通道高度相关时，“多次命中”不等于多份独立证据。
- Elasticsearch 当前接口属于易变能力；正式章节必须保留审核日期和目标版本。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

补可审计的第一人称面经来源；在统一候选集上复现实验 RRF、Weighted RRF、CombSUM、CombMNZ 和 Linear Retriever，并加入父子分块、版本冲突和多权限域样本。

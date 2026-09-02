---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RESULT-FUSION
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：结果融合（Result Fusion）第一轮

## 1. 本轮目标与边界

核查多路召回后的排名融合、分数融合、去重、通道权重和候选截断。结果融合（Result Fusion）负责把多个检索列表合成候选列表，不与后续基于 Query—Document 联合建模的重排序（Reranking）混淆。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 原理（Principle） | `reciprocal rank fusion original paper SIGIR 2009 PDF` | RRF 原始论文 |
| Q-002 | 实现（Implementation） | `site:learn.microsoft.com azure hybrid search reciprocal rank fusion ranking official` | Azure 官方文档 |
| Q-003 | 实现（Implementation） | `site:elastic.co retrievers reciprocal rank fusion linear retriever official` | Elasticsearch 官方文档 |
| Q-004 | 公开场景（Public Scenario） | `site:nowcoder.com/discuss RRF RAG BM25 向量 融合` | 牛客公开项目复盘 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `reciprocal-rank-fusion-2009` | 原始论文（Original Paper） | `included` | RRF 原始定义与实验 |
| `azure-hybrid-rrf-ranking-2026` | 官方文档（Official Documentation） | `included` | 当前 RRF 分数、查询数和 Semantic Reranker Score 边界 |
| `azure-hybrid-search-overview-2026` | 官方文档（Official Documentation） | `included` | 全文与多向量查询并行融合的实现 |
| `elasticsearch-retrievers-docs-2026` | 官方文档（Official Documentation） | `included` | RRF 与 Linear Retriever 的当前接口 |
| `nowcoder-rag-retrieval-evolution-2026` | 工程实践（Engineering Practice） | `included` | 去重、候选截断和项目指标场景；不采信为通用参数 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `FUS-K-001` | `knowledge` | RRF 使用各通道的排名位置，规避原始分数尺度不可比 | `new` |
| `FUS-K-002` | `knowledge` | 加权分数融合需要归一化、校准或可比较分数契约 | `new` |
| `FUS-P-001` | `problem_question` | 同一 Chunk 从多通道返回时，错误去重会丢 Metadata 或父子关系 | `new` |
| `FUS-P-002` | `problem_question` | 通道候选数和权重不平衡会压制长尾通道 | `new` |
| `FUS-P-003` | `problem_question` | 融合后过早截断会降低 Reranker 的候选上限 | `extends` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-018` | 分数不可比和候选重复时怎样融合 | 工程实践（Engineering Practice） | 公开项目 RRF 链路 | 否 | RRF 原始论文与 Azure/Elastic 官方文档 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | RRF 和加权分数融合边界已覆盖 |
| 实现（Implementation） | `covered` | Azure 与 Elasticsearch 当前接口已登记 |
| 工程问题（Engineering Problem） | `covered` | 分数尺度、重复候选、通道权重和截断已登记 |
| 解决方案（Solution） | `partial` | 学习融合权重、校准和父子去重待补 |
| 评估（Evaluation） | `partial` | 需按通道贡献、覆盖率和消融实验评估 |
| 公开面试题（Public Interview Question） | `partial` | 有公开工程场景，第一人称面经仍缺 |
| 时效（Freshness） | `covered` | 原始算法和 2026 API 均有来源 |
| 安全或治理（Security or Governance） | `partial` | 不同权限源融合后的 ACL 合并规则待补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接改写、检索、重排和评估 |

## 7. 冲突、版本与未验证假设

- 不把 RRF Score 当作相关性概率；
- RRF 的排名常数和每路候选数需要在业务数据上评估；
- 分数融合前若未校准，权重可能只反映分数量纲；
- 下一轮补 Weighted RRF、CombSUM/CombMNZ、学习融合和去重实体键策略。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 一手资料缺口检查是否完成 | 否 |
| 公开面试题专项搜索是否完成 | 第一轮完成但仅找到工程实践 |
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补加权 RRF、CombSUM、CombMNZ、分数校准、父子 Chunk 去重和多权限源融合；专项搜索第一人称面经。

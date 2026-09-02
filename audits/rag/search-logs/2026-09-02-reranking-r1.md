---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RERANKING
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：重排序（Reranking）第一轮

## 1. 本轮目标与边界

核查交叉编码器（Cross-Encoder）、序列到序列重排（Sequence-to-sequence Reranking）、LLM 重排（LLM Reranking）和多样性重排的原理、候选上限、延迟、领域迁移和评估。重排只能改变已有候选顺序，不能恢复未被召回的文档。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 原理（Principle） | `site:sbert.net cross encoder retrieve rerank official documentation` | Sentence Transformers 官方文档 |
| Q-002 | 原始研究（Original Research） | `site:arxiv.org monoT5 reranking sequence-to-sequence document ranking` | monoT5 原始论文 |
| Q-003 | 新方法（New Method） | `site:arxiv.org Is ChatGPT Good at Search reranking agents RankGPT` | RankGPT 原始论文 |
| Q-004 | 实现（Implementation） | `site:docs.cohere.com rerank official docs cross encoder reranking` | Cohere 官方文档 |
| Q-005 | 公开场景（Public Scenario） | `site:nowcoder.com/discuss Reranker RAG 面试` | 牛客公开项目复盘 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `sentence-transformers-retrieve-rerank-2026` | 官方文档（Official Documentation） | `included` | Bi-encoder 候选与 Cross-encoder 精排的两阶段边界 |
| `cohere-rerank-docs-2026` | 官方文档（Official Documentation） | `included` | 当前 API、Top-N 和半结构化输入实现 |
| `monot5-2020` | 原始论文（Original Paper） | `included` | Sequence-to-sequence 点式重排与迁移实验 |
| `rankgpt-2024` | 原始论文（Original Paper） | `included` | LLM Listwise Reranking、滑动窗口和蒸馏 |
| `colbert-2020` | 原始论文（Original Paper） | `included` | Late Interaction 作为检索与重排之间的路线 |
| `nowcoder-rag-retrieval-evolution-2026` | 工程实践（Engineering Practice） | `included` | 候选不变时 NDCG/MRR 变化和场景闸门线索 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `RRK-K-001` | `knowledge` | Cross-Encoder 联合编码 Query 与 Document，计算更贵但交互更充分 | `extends` |
| `RRK-K-002` | `knowledge` | Pointwise、Pairwise 和 Listwise Reranking 的输入与目标不同 | `new` |
| `RRK-P-001` | `problem_question` | 候选召回缺失时，Reranker 无法提高候选 Recall 上限 | `new` |
| `RRK-P-002` | `problem_question` | 候选数过大造成延迟和成本，过小又提前丢失相关文档 | `new` |
| `RRK-P-003` | `problem_question` | 相关性高不等于能够支持答案，需要区分 Relevance 与 Answer Support | `new` |
| `RRK-C-001` | `conflict` | “接入 Reranker 即全面提升”与领域迁移、延迟及候选上限冲突 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-019` | 候选数、Top-N、跳过条件和指标变化怎样选择 | 工程实践（Engineering Practice） | 公开项目 Reranker 链路 | 否 | Sentence Transformers、Cohere、monoT5、RankGPT |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Cross-encoder、Sequence-to-sequence 和 LLM Reranking 已覆盖 |
| 实现（Implementation） | `covered` | Sentence Transformers 和 Cohere 当前接口已登记 |
| 工程问题（Engineering Problem） | `covered` | 候选上限、延迟、领域迁移和答案支持已登记 |
| 解决方案（Solution） | `partial` | 动态闸门、批处理、蒸馏、量化和缓存待补 |
| 评估（Evaluation） | `covered` | NDCG、MRR、Recall 边界和分阶段评估已登记 |
| 公开面试题（Public Interview Question） | `partial` | 有公开工程场景，需补第一人称面经 |
| 时效（Freshness） | `covered` | 经典模型、2024 LLM Reranking 与 2026 API 已覆盖 |
| 安全或治理（Security or Governance） | `partial` | 外部 Rerank API 数据边界与 Prompt Injection 待补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接召回、融合、上下文组装和评估 |

## 7. 冲突、版本与未验证假设

- 不将重排后的 NDCG/MRR 改善写成 Recall 必然改善；
- Reranker Score 通常不是跨模型可比概率；
- Listwise LLM Reranking 受候选顺序、窗口和模型版本影响；
- 下一轮补 MMR 原始资料、领域 Reranker、蒸馏、量化、批处理和动态跳过策略。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 一手资料缺口检查是否完成 | 否 |
| 公开面试题专项搜索是否完成 | 第一轮完成但第一人称面经不足 |
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补 MMR、领域 Reranker、蒸馏、量化、Batching、动态 Gate 和 Answer-support Reranking；继续搜第一人称面经。

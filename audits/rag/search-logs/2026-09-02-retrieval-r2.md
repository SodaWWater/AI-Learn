---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RETRIEVAL
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 检索（Retrieval）第二轮独立补漏

## 1. 本轮目标与边界

专项补查多跳检索（Multi-hop Retrieval）、迭代检索（Iterative Retrieval）、中间推理状态（Intermediate Reasoning State）、动态停止（Dynamic Stopping）、权限感知检索（Permission-aware Retrieval）和新鲜度信号（Freshness Signal）。本节点只评价候选证据是否被取回，不把结果融合（Result Fusion）、重排序（Reranking）或生成（Generation）的改善归因给检索器（Retriever）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 多步检索（Multi-step Retrieval） | `IRCoT interleaving retrieval chain of thought multi-step questions` | ACL Anthology 原始论文（Original Paper） |
| Q-202 | 迭代诊断（Iterative Diagnostic） | `iterative RAG diagnostic multi-hop evidence failure early stop` | arXiv / TMLR 论文（Paper） |
| Q-203 | 时间检索（Temporal Retrieval） | `temporal RAG freshness time-aware retrieval official paper` | 原始论文（Original Paper） |
| Q-204 | 权限检索（Permission-aware Retrieval） | `site:learn.microsoft.com Azure AI Search document level access control` | Microsoft 官方文档（Official Documentation） |
| Q-205 | 公开题目（Public Question） | `site:nowcoder.com RAG 迭代检索 多跳检索 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `ircot-2023` | 原始论文（Original Paper） | `included` | 补齐推理和检索交替、后续查询依赖中间状态的机制 |
| `iterative-rag-diagnostic-2026` | 论文（Paper） | `included` | 补齐跳数覆盖、干扰锁定（Distractor Latch）、过早停止校准和组合失败诊断 |
| `ia-rag-temporal-2026` | 原始论文（Original Paper） | `included_existing` | 已覆盖时间约束理解与不完整时间边界，不重复登记 |
| `azure-search-security-filter-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 已覆盖可信身份注入和文档级安全过滤，不重复登记 |
| `chronofy-2026` | 预印本（Preprint） | `lead_only` | 证据规模和成熟度不足，未形成必须新增的独立结论 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `RET-K-201` | `knowledge` | 多跳问题的后续检索查询依赖已获得的中间证据，不能预先一次性固定全部查询 | `ircot-2023` | `new` |
| `RET-P-201` | `problem_question` | 首跳证据相关但不完整时，系统可能围绕错误实体持续检索并形成干扰锁定（Distractor Latch） | `iterative-rag-diagnostic-2026` | `new` |
| `RET-P-202` | `problem_question` | 停止条件只看相似度或生成器自信度时，可能在关键跳尚未覆盖前提前停止（Early Stop） | `iterative-rag-diagnostic-2026` | `new` |
| `RET-P-203` | `problem_question` | 检索到每一跳的理想证据仍不保证最终答案正确，组合推理（Compositional Reasoning）必须单独归因 | `iterative-rag-diagnostic-2026` | `new` |
| `RET-E-201` | `evaluation` | 多跳检索评估应拆分每跳覆盖、路径完成率、错误实体转移、停止校准、总调用数、延迟及最终组合正确率 | `ircot-2023`; `iterative-rag-diagnostic-2026` | `new` |
| `RET-S-201` | `solution` | 迭代控制器（Iterative Controller）保留证据状态、未满足子目标和预算，在每跳后决定继续、改写、回退或停止 | 两项新增论文；既有路由来源 | `extends` |

## 5. 公开面试题来源核验

新增 `RAG-SCENE-023`：公开题库明确提出检索偏置（Retrieval Bias）及过滤、拒答、回退和迭代检索（Iterative Retrieval）的选择问题。该页面只作为题目出处，不采用其简略答案替代本轮论文证据。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Dense、Sparse、Hybrid、Late Interaction、多跳和迭代检索已覆盖 |
| 实现（Implementation） | `covered` | 数据库、搜索引擎、两阶段和迭代控制器均有实现入口或论文算法 |
| 工程问题（Engineering Problem） | `covered` | 零召回、权限、时效、干扰锁定、过早停止和组合失败已登记 |
| 解决方案（Solution） | `covered` | 混合召回、权限前置、状态化迭代、预算和回退链路已覆盖 |
| 评估（Evaluation） | `covered` | 增加每跳、路径、停止、成本和组合分层指标 |
| 公开面试题（Public Interview Question） | `covered` | 公开题库、工程实践及项目考题均可回链 |
| 时效（Freshness） | `covered` | 经典检索论文、2026 迭代诊断和当前产品能力兼顾 |
| 安全或治理（Security or Governance） | `partial` | 间接提示注入（Indirect Prompt Injection）和恶意语料检索仍待生产治理轮次补证 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接路由、改写、融合、重排、推理和评估 |

## 7. 冲突、版本与未验证假设

- 迭代检索（Iterative Retrieval）不是复杂问题的默认最优策略；它增加调用次数，并可能累积错误和噪声。
- 链式思维（Chain-of-Thought）属于推理机制，不应把不可观测的内部推理文字当作可靠证据状态。
- 新鲜度（Freshness）和相关性（Relevance）是不同维度；时间衰减不能无条件压过权威旧资料。
- 权限过滤（Permission Filtering）必须在候选泄露之前执行；生成后再隐藏来源不能修复越权检索。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立按事实型、精确词项型、多跳型、时间型、权限型和长文档型查询分层的 Dense / Sparse / Hybrid / Iterative 对照；补间接提示注入（Indirect Prompt Injection）和可信来源传播（Trusted-source Propagation）的原始安全证据。

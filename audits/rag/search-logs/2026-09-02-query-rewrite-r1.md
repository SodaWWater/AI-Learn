---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-REWRITE
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：查询改写（Query Rewrite）第一轮

## 1. 本轮目标与边界

核查查询改写（Query Rewrite）、多查询扩展（Multi-Query Expansion）、假设文档嵌入（Hypothetical Document Embeddings，HyDE）、子问题分解（Sub-question Decomposition）、退步提示（Step-back Prompting）和会话查询改写（Conversational Query Rewriting）。重点登记语义漂移、精确标识符丢失、噪声放大与延迟成本。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 原理（Principle） | `site:arxiv.org HyDE Precise Zero-Shot Dense Retrieval hypothetical document embeddings` | HyDE 原始论文 |
| Q-002 | 新方法（New Method） | `site:aclanthology.org 2023 emnlp query rewriting retrieval augmented language models` | Rewrite-Retrieve-Read 原始论文 |
| Q-003 | 新方法（New Method） | `site:arxiv.org step-back prompting abstraction retrieval` | Step-back Prompting 原始论文 |
| Q-004 | 会话（Conversation） | `site:aclanthology.org conversational question rewriting QReCC` | QReCC 原始论文 |
| Q-005 | 实现（Implementation） | `site:learn.microsoft.com semantic query rewrite generative count preview exact identifier` | Azure AI Search 官方文档 |
| Q-006 | 实现（Implementation） | `site:docs.cohere.com generating parallel queries better RAG retrieval` | Cohere 官方文档 |
| Q-007 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG Query Rewrite 查询改写 HyDE 面试` | 牛客公开页面 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `hyde-2022` | 原始论文（Original Paper） | `included` | 用于假设文档生成、编码和语料检索的原始流程 |
| `rewrite-retrieve-read-emnlp-2023` | 原始论文（Original Paper） | `included` | 用于可训练重写器与 Black-box LLM 组合 |
| `step-back-prompting-2024` | 原始论文（Original Paper） | `included` | 用于从实例问题生成抽象问题并联合推理 |
| `qrecc-naacl-2021` | 原始论文（Original Paper） | `included` | 用于会话独立问题改写和指代/省略 |
| `azure-semantic-query-rewrite-2026` | 官方文档（Official Documentation） | `included` | 用于当前生成式改写 API、降级和精确标识符风险；明确 Preview |
| `cohere-parallel-query-docs-2026` | 官方文档（Official Documentation） | `included` | 用于复合查询分解和并行查询的当前实现 |
| `nowcoder-agent-rag-question-bank-2026` | 公开题库（Public Question Bank） | `included` | 提取 HyDE、Query Expansion 和 Multi-Query 选型问题 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `QRW-K-001` | `knowledge` | 不同改写方法改变的对象不同：词项、多个查询、假设文档、子问题或抽象问题 | `new` |
| `QRW-K-002` | `knowledge` | 会话改写（Conversational Query Rewriting）目标是生成可独立检索的问题，不等同于通用同义改写 | `new` |
| `QRW-P-001` | `problem_question` | 生成式改写可能删除产品号、错误码、人名和日期等精确约束 | `new` |
| `QRW-P-002` | `problem_question` | 多查询扩展提高召回同时扩大噪声、融合成本和延迟 | `extends` |
| `QRW-P-003` | `problem_question` | HyDE 生成的假设内容偏离领域事实时可能改变检索方向 | `new` |
| `QRW-S-001` | `solution` | 保留原查询并与改写并行检索，显式保护精确 Token，再进行结果融合 | `new` |
| `QRW-C-001` | `conflict` | “改写后的自然语言更流畅即更适合检索”与精确标识符丢失风险冲突 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-015` | 召回低时怎样选择改写方法并控制语义漂移和成本 | 公开题库（Public Question Bank） | 牛客 Q5 | 否 | HyDE、Rewrite-Retrieve-Read、Step-back、QReCC 原始论文与 Azure/Cohere 官方文档 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 五类主要改写/分解路线及其不同输出对象已覆盖 |
| 实现（Implementation） | `covered` | 生成式 Rewrite 和 Parallel Query 当前接口已登记 |
| 工程问题（Engineering Problem） | `covered` | 语义漂移、精确 Token 丢失、噪声、失败降级和延迟已登记 |
| 解决方案（Solution） | `partial` | Token 保护、候选融合和策略门控需更多官方/可复现实验 |
| 评估（Evaluation） | `partial` | 需拆分 Rewrite Fidelity、Retrieval Recall、Noise 和端到端答案质量 |
| 公开面试题（Public Interview Question） | `covered` | 公开题库已覆盖 HyDE、Multi-Query 和扩展问题 |
| 时效（Freshness） | `covered` | 经典论文与 2026 Preview API 均有明确版本 |
| 安全或治理（Security or Governance） | `partial` | Prompt Injection 经改写传播、敏感实体扩展和外部模型调用待补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接理解、路由、检索、融合和生成 |

## 7. 冲突、版本与未验证假设

- 不把 Query Rewrite 视为必经步骤；应由问题类型、历史、检索失败信号和成本预算决定；
- Azure Semantic Query Rewrite 在 2026-09-02 仍是 Preview，无服务级别协议（Service Level Agreement，SLA），不能按稳定生产能力描述；
- 改写数量不是越多越好，必须与融合方法、候选预算和延迟目标联合评估；
- HyDE 论文的向量瓶颈假设需要在目标 Embedding 模型与领域语料上复验；
- 下一轮需补查询改写忠实度（Rewrite Fidelity）、精确 Token 保留率和离线/在线反事实评估。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 一手资料缺口检查是否完成 | 否 |
| 公开面试题专项搜索是否完成 | 第一轮完成，需补第一人称面经 |
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补充 Multi-Query、子问题分解和查询融合的原始实验；建立含错误码、产品号、时间和权限条件的 Rewrite Fidelity 测试集，并记录原查询保留与失败降级策略。

---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-ROUTING
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：查询路由（Query Routing）第一轮

## 1. 本轮目标与边界

核查查询路由（Query Routing）在无需检索、单一知识源、多知识源、外部工具和多步检索之间的选择机制。路由接收查询理解（Query Understanding）的结构化结果，但本身负责“走哪条执行链路”，不与意图识别合并。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 原理（Principle） | `site:arxiv.org Adaptive-RAG question complexity retrieval` | Adaptive-RAG 原始论文 |
| Q-002 | 实现（Implementation） | `site:learn.microsoft.com query routing knowledge source selection agentic retrieval official` | Azure AI Search 官方文档 |
| Q-003 | 实现（Implementation） | `site:developers.llamaindex.ai query router selector query engine` | LlamaIndex 当前官方文档 |
| Q-004 | 实现（Implementation） | `site:docs.cohere.com routing queries data sources official` | Cohere 官方文档 |
| Q-005 | 公开题目（Public Question） | `site:nowcoder.com/discuss 意图路由 自适应检索 RAG 面试` | 牛客公开题库与第一人称帖子 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `adaptive-rag-2024` | 原始论文（Original Paper） | `included` | 按问题复杂度选择无检索、单步和迭代检索 |
| `azure-agentic-retrieval-overview-2026` | 官方文档（Official Documentation） | `included` | 当前知识源选择、查询规划、并行执行和成本边界 |
| `cohere-query-routing-docs-2026` | 官方文档（Official Documentation） | `included` | 查询分类到不同数据源的实现 |
| `llamaindex-router-docs-2026` | 官方文档（Official Documentation） | `included` | Selector、Router Query Engine 与单路/多路选择 |
| `elasticsearch-retrievers-docs-2026` | 官方文档（Official Documentation） | `included` | Retriever Tree 作为检索执行计划的实现入口 |
| `nowcoder-xunlei-ai-intent-routing-2026` | 第一人称面经（First-person Interview Report） | `included` | 仅确认线上路由覆盖问题曾在帖子中出现 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `ROUTE-K-001` | `knowledge` | 路由输出可以是零个、一个或多个知识源/检索器，而非只能单标签分类 | `new` |
| `ROUTE-K-002` | `knowledge` | 无需检索判断、检索器选择和工具选择是相邻但不同的决策层 | `new` |
| `ROUTE-P-001` | `problem_question` | 单路路由误判会直接造成零召回，多路广播又增加成本和噪声 | `new` |
| `ROUTE-P-002` | `problem_question` | 知识源描述不清或版本落后导致 LLM 路由不稳定 | `new` |
| `ROUTE-S-001` | `solution` | 高置信单路、低置信多路、失败回退和预算上限形成分层策略 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-014` | 怎样证明意图路由覆盖线上流量 | 第一人称面经（First-person Interview Report） | 迅雷 AI 一面 Q3 | 发布者自述，非企业官方题 | Adaptive-RAG 与当前官方路由文档 |
| `RAG-SCENE-016` | 什么时候无需检索、单次检索、多次检索或调用工具 | 公开题库（Public Question Bank） | 牛客 Q9 | 否 | Adaptive-RAG、Azure Agentic Retrieval |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 复杂度路由、知识源路由和多路路由已覆盖 |
| 实现（Implementation） | `covered` | Azure、Cohere、LlamaIndex 和 Elasticsearch 有入口 |
| 工程问题（Engineering Problem） | `covered` | 误判、广播成本、描述漂移和降级已登记 |
| 解决方案（Solution） | `partial` | 校准、路由缓存和回退状态机需补充 |
| 评估（Evaluation） | `partial` | 需建立成本敏感混淆矩阵和端到端路由成功率 |
| 公开面试题（Public Interview Question） | `covered` | 第一人称帖子和公开题库均有入口 |
| 时效（Freshness） | `covered` | 2026 官方实现已审核 |
| 安全或治理（Security or Governance） | `partial` | 路由到外部源的数据边界和最小权限待补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接理解、改写、检索和 Agentic RAG |

## 7. 冲突、版本与未验证假设

- 不把路由准确率等同于最终回答成功率；不同错误的成本不相同；
- 多路广播可降低漏路由但可能扩大越权面、延迟和融合噪声；
- Azure 2026-04-01 GA 与 2026-08-01-preview 的能力必须分开描述；
- 下一轮补语义路由（Semantic Routing）阈值校准、工具路由和故障回退实验。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 一手资料缺口检查是否完成 | 否 |
| 公开面试题专项搜索是否完成 | 第一轮完成 |
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 2 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补路由置信度校准、语义阈值、路由缓存、外部工具选择和成本敏感评测；建立错误路由到下游失败的传播表。

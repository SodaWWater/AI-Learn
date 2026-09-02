---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-UNDERSTANDING
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：查询理解（Query Understanding）第一轮

## 1. 本轮目标与边界

核查用户输入进入 RAG 后的规范化、意图识别、是否检索判断、实体与约束抽取、歧义澄清、会话历史理解和复杂度判断。查询理解（Query Understanding）负责判断“用户在问什么和需要什么”，不与后续查询改写（Query Rewrite）合并。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 新方法（New Method） | `site:arxiv.org Adaptive-RAG question complexity retrieval` | Adaptive-RAG 原始论文 |
| Q-002 | 实现（Implementation） | `site:learn.microsoft.com azure AI search agentic retrieval query planning official 2026` | Azure AI Search 官方文档 |
| Q-003 | 实现（Implementation） | `site:docs.cohere.com routing queries data sources official` | Cohere 官方文档 |
| Q-004 | 评估（Evaluation） | `site:aclanthology.org intent understanding classification clarification lightweight LLM EACL 2026` | ACL Anthology 原始论文 |
| Q-005 | 公开题目（Public Question） | `site:nowcoder.com/discuss 意图路由 复合意图 歧义 AI 一面` | 牛客第一人称帖子 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `azure-agentic-retrieval-overview-2026` | 官方文档（Official Documentation） | `included` | 用于当前复杂查询规划、会话历史、子查询和成本延迟边界 |
| `adaptive-rag-2024` | 原始论文（Original Paper） | `included` | 用于按问题复杂度在不同检索策略间选择 |
| `cohere-query-routing-docs-2026` | 官方文档（Official Documentation） | `included` | 用于查询分类和数据源路由实现 |
| `intent-understanding-clarification-eacl-2026` | 原始论文（Original Paper） | `included` | 用于意图分类与澄清的组合框架 |
| `qrecc-naacl-2021` | 原始论文（Original Paper） | `included` | 用于会话省略与指代问题和独立查询目标 |
| `nowcoder-xunlei-ai-intent-routing-2026` | 第一人称面经（First-person Interview Report） | `included` | 只确认意图路由覆盖问题线索；整理答案另行核验 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `QUD-K-001` | `knowledge` | 查询理解（Query Understanding）可产出意图、实体、时间、地域、权限、复杂度和歧义状态，而不只是一条重写文本 | `new` |
| `QUD-K-002` | `knowledge` | 是否检索和检索深度可根据问题复杂度进行自适应选择 | `extends` |
| `QUD-P-001` | `problem_question` | 规则在离线样本上覆盖高，但对复合意图、表达省略和新意图错误吞并 | `new` |
| `QUD-P-002` | `problem_question` | 低置信意图继续强制路由会把错误传播到数据源选择和检索 | `new` |
| `QUD-P-003` | `problem_question` | 多轮指代和时间条件未解析，后续检索即使正确执行也会查询错范围 | `extends` |
| `QUD-S-001` | `solution` | 在拒识、澄清、规则、分类器和规划模型之间建立分层决策 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-014` | 怎样证明意图规则覆盖线上复合和歧义请求 | 第一人称面经（First-person Interview Report） | 迅雷服务端开发（AI）一面 Q3 | 发布者自述，可称“帖子记录出现”，不可称企业官方题 | Adaptive-RAG、EACL 2026 论文和 Cohere/Azure 官方文档 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 意图、实体约束、复杂度、会话历史和澄清已建立边界 |
| 实现（Implementation） | `covered` | 规则/分类器/LLM 路由、结构化输出和官方 Query Planning 有入口 |
| 工程问题（Engineering Problem） | `covered` | 复合意图、歧义、长尾、低置信和多轮指代已登记 |
| 解决方案（Solution） | `partial` | 实体抽取、时间解析和权限条件抽取的当前框架实现待补 |
| 评估（Evaluation） | `partial` | 分类准确率、拒识和错误路由已有方向；线上分布漂移与校准待补 |
| 公开面试题（Public Interview Question） | `covered` | 已有 2026 第一人称帖子问题 |
| 时效（Freshness） | `covered` | 2026 论文和官方 Agentic Retrieval 文档已登记 |
| 安全或治理（Security or Governance） | `partial` | 权限条件抽取失败的越权风险和 Prompt Injection 检测待补 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接改写、路由、检索、生成和评估 |

## 7. 冲突、版本与未验证假设

- 不把意图分类（Intent Classification）的准确率等同于端到端路由正确率；
- 规则命中率升高可能来自宽泛规则错误吞并，必须同时看拒识率和错误路由率；
- Azure Agentic Retrieval 的通用可用（General Availability，GA）API 与 2026-08-01-preview 完整功能集不同，正式内容必须分别标记；
- EACL 2026 结果需进一步提取数据集、标签体系和澄清成本，不能直接推广到任意业务；
- 下一轮补命名实体识别（Named Entity Recognition，NER）、时间解析（Temporal Parsing）、置信度校准（Confidence Calibration）与分布漂移（Distribution Drift）。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 一手资料缺口检查是否完成 | 否 |
| 公开面试题专项搜索是否完成 | 第一轮完成 |
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补充实体、时间、地域、权限约束抽取和置信度校准的一手资料；建立“理解错误—路由错误—检索错误”的错误传播矩阵及线上影子评估方法。

---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-UNDERSTANDING
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 查询理解（Query Understanding）第二轮独立补漏

## 1. 本轮目标与边界

专项补查结构化约束抽取（Structured Constraint Extraction）、时间约束（Temporal Constraint）、分布外意图（Out-of-distribution Intent，OOD Intent）、置信拒识（Confidence-based Rejection）和权限边界（Authorization Boundary）。本轮明确区分“从用户问题抽取业务过滤条件”和“由可信身份上下文注入访问控制条件”。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 结构化查询（Structured Query） | `site:docs.langchain.com self query retriever metadata filter attribute schema` | LangChain 官方文档（Official Documentation） |
| Q-202 | 权限（Authorization） | `site:learn.microsoft.com azure ai search security trimming principal filter search.in` | Azure AI Search 官方文档（Official Documentation） |
| Q-203 | 拒识（Rejection） | `site:aclanthology.org 2025 intent classification out-of-distribution detection LLM` | ACL Anthology 原始论文（Original Paper） |
| Q-204 | 时间（Temporal） | `site:arxiv.org 2026 temporal RAG interval algebra query constraint` | arXiv 原始论文（Original Paper） |
| Q-205 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG 查询理解 权限 过滤 面经` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `langchain-self-query-hana-docs-2026` | 官方文档（Official Documentation） | `included` | 展示 Attribute Schema、Self-query Retriever 和自然语言到 Metadata Filter 的当前实现 |
| `azure-search-security-filter-docs-2026` | 官方文档（Official Documentation） | `included` | 明确文档级权限过滤（Document-level Authorization Filter）必须使用请求者身份 Principal，并应用于每次 Query |
| `ood-intent-detection-emnlp-2025` | 原始论文（Original Paper） | `included` | 补 Near-OOD、Semantic Shift、Covariate Shift、ID/OOD 指标和拒识路线 |
| `ia-rag-temporal-2026` | 原始论文（Original Paper） | `included` | 补时间区间、重叠、包含和不完整时间边界，不把时间条件缩减为单一 Timestamp |
| `deepcontext-intent-drift-2026` | 原始论文（Original Paper） | `lead_only` | 多轮攻击意图漂移（Adversarial Intent Drift）作为安全线索，待下一轮与 Prompt Injection 威胁模型统一审计 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `QUD-K-201` | `knowledge` | 查询理解（Query Understanding）的结构化输出可包含语义 Query 与类型化 Metadata Filter，但字段、运算符和值必须受 Schema 白名单约束 | `langchain-self-query-hana-docs-2026` | `new` |
| `QUD-K-202` | `knowledge` | 用户文本中的“我属于某组”不是授权事实；访问控制主体（Authorization Principal）必须来自已认证会话或网关，并与业务条件合并而非由模型生成 | `azure-search-security-filter-docs-2026` | `new` |
| `QUD-K-203` | `knowledge` | 分布外意图（Out-of-distribution Intent，OOD Intent）包含同域未见意图的 Near-OOD；高分类准确率不能替代 OOD Recall 和拒识后人工成本 | `ood-intent-detection-emnlp-2025` | `new` |
| `QUD-K-204` | `knowledge` | 时间约束（Temporal Constraint）可能是 Point、Interval、Overlap、Containment 或模糊边界，不能只抽取一个日期字符串 | `ia-rag-temporal-2026` | `new` |
| `QUD-P-201` | `problem_question` | 大语言模型（Large Language Model，LLM）把用户自述角色直接翻译成权限过滤条件，导致越权检索 | `azure-search-security-filter-docs-2026` | `new` |
| `QUD-P-202` | `problem_question` | 新业务意图与已知意图语义相近时被强制归类，离线 Accuracy 正常但 OOD Recall 与错误路由率恶化 | `ood-intent-detection-emnlp-2025` | `new` |
| `QUD-P-203` | `problem_question` | “上季度仍有效”“A 任职期间”等区间关系被降级为关键词或单日期后，检索执行正确但范围错误 | `ia-rag-temporal-2026` | `new` |

## 5. 公开面试题来源核验

本轮没有发现比 `RAG-SCENE-014` 更独立的查询理解（Query Understanding）单节点第一人称题。`RAG-SCENE-022` 的多租户与文档级权限追问作为跨节点问题保留，连接查询理解（Query Understanding）、检索（Retrieval）和生产治理（Production Governance）。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 意图、实体、结构化约束、时间关系、会话和复杂度已覆盖 |
| 实现（Implementation） | `covered` | Self-query、Attribute Schema、Security Filter 和 OOD 路线已有入口 |
| 工程问题（Engineering Problem） | `covered` | 低置信、Near-OOD、权限伪造和时间范围错误已登记 |
| 解决方案（Solution） | `covered` | Schema 白名单、可信 Principal 注入、拒识/澄清和区间建模已登记 |
| 评估（Evaluation） | `partial` | 仍需线上分布漂移（Distribution Drift）、校准误差（Calibration Error）与下游错误传播的统一数据集 |
| 公开面试题（Public Interview Question） | `covered` | 节点题与企业级综合题均有公开出处 |
| 时效（Freshness） | `covered` | 2025/2026 论文和 2026 官方接口已核对 |
| 安全或治理（Security or Governance） | `covered` | 权限来源、每次 Query 强制过滤和 Prompt Injection 线索已登记 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接改写、路由、存储过滤、检索、评估和生产治理 |

## 7. 冲突、版本与未验证假设

- Self-query Retriever 只说明如何生成业务 Metadata Filter，不证明生成结果可作为授权决策。
- Azure Security Filter Pattern 中 Principal 只是过滤字段值，真正认证授权仍由应用层负责；`retrievable=false` 也不是字段级安全机制。
- OOD 论文的阈值和结果依赖标签集、数据集与成本函数，不能复制为生产固定阈值。
- IA-RAG 是 2026 研究路线，正式学习内容需把其作为时间检索（Temporal Retrieval）专项方法，不描述为默认工业标准。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 4 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立“理解输出—路由—过滤—召回”错误传播矩阵，加入置信度校准（Confidence Calibration）、线上漂移（Online Drift）、Prompt Injection 和多轮权限上下文测试；补中文实体、时间和地域解析的可复现实验。

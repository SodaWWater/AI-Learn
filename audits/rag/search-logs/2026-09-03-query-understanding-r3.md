---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-UNDERSTANDING
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 查询理解（Query Understanding）第三轮独立补漏

## 1. 本轮目标与边界

本轮专查查询理解输出的 Error Propagation（错误传播）、Confidence Calibration（置信度校准）、中文 Named Entity Recognition（命名实体识别）、Temporal Expression Normalization（时间表达归一化）、Prompt Injection（提示注入）和 Multi-turn Intent Drift（多轮意图漂移）。查询理解置信度、检索置信度和回答置信度分属不同随机变量，不合并为一个“系统置信度”。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 置信度（Confidence） | `RAG verbal confidence calibration retrieval noise ECE AUROC 2026` | arXiv 原始论文（Original Paper） |
| Q-302 | 中文实体（Chinese Entity） | `CLUENER2020 Chinese fine grained named entity recognition address organization F1` | CLUE 官方仓库（Official Repository） |
| Q-303 | 时间归一化（Temporal Normalization） | `cross-language domain temporal expression normalization Computational Linguistics 2025` | ACL Anthology 原始论文（Original Paper） |
| Q-304 | 多轮安全（Multi-turn Safety） | `multi-turn adversarial intent drift stateful detection LLM 2026` | arXiv 研究线索（Research Lead） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com/discuss RAG 查询理解 意图识别 权限 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `nova-rag-confidence-calibration-2026` | 原始论文（Original Paper） | `included` | 用 Gold / Relevant / Irrelevant / Counterfactual Passage（正确/相关/无关/反事实段落）分层证明下游 Verbal Confidence（口头置信度）受检索噪声影响 |
| `cluener2020-benchmark` | 官方仓库（Official Repository） | `included` | 提供中文 Address（地址）、Organization（组织）、Position（职位）等 Span-level Label（跨度级标签）和分类型 F1 |
| `cross-language-temporal-normalization-2025` | 原始论文（Original Paper） | `included` | 补 Temporal Expression（时间表达）数值化、Cross-language Adaptation（跨语言适配）和 Cross-domain Adaptation（跨领域适配） |
| `deepcontext-intent-drift-2026` | 预印本（Preprint） | `lead_only` | 研究 Session-level State（会话级状态）检测，但当前为特定攻击检测预印本，且报告复杂 Function Calling（函数调用）中的 False Positive（误报）风险，不升级为通用实现证据 |
| `owasp-llm-top10-2025` | 官方安全指南（Official Security Guidance） | `included_existing` | 将 Prompt Injection（提示注入）映射到查询理解和查询改写节点，不重复登记来源 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `QUD-K-301` | `knowledge` | Query-understanding Confidence（查询理解置信度）、Authorization Confidence（授权置信度）、Routing Confidence（路由置信度）、Retrieval Confidence（检索置信度）和 Answer Confidence（回答置信度）语义不同，不能压成一个无来源标量 | `nova-rag-confidence-calibration-2026`; 既有 OOD Intent（分布外意图）来源 | `new` |
| `QUD-K-302` | `knowledge` | Named Entity Recognition（命名实体识别）负责 Span（跨度）和类型，Entity Linking（实体链接）负责映射到业务标识符，Geocoding（地理编码）负责地点标准化；三者是相邻但不同节点 | `cluener2020-benchmark` | `new` |
| `QUD-P-301` | `problem_question` | 下游大语言模型（Large Language Model，LLM）在存在 Irrelevant Passage（无关段落）或 Counterfactual Passage（反事实段落）时仍可能高置信，因此不能把 Verbal Confidence（口头置信度）反推为查询解析正确 | `nova-rag-confidence-calibration-2026` | `new` |
| `QUD-P-302` | `problem_question` | 中文 Query（查询）在 Address（地址）、Organization（组织）、Position（职位）和别名上整体 F1 正常，但少数类别或边界错误会生成错误 Metadata Filter（元数据过滤器） | `cluener2020-benchmark`; `langchain-self-query-hana-docs-2026` | `new` |
| `QUD-P-303` | `problem_question` | 相对时间、模糊时间或跨域表达被识别成实体但没有 Normalized Value（归一值）、Reference Time（参考时间）、Timezone（时区）和 Granularity（粒度），导致过滤语法合法但范围错误 | `cross-language-temporal-normalization-2025`; `ia-rag-temporal-2026` | `new` |
| `QUD-P-304` | `problem_question` | 单轮分类均安全或低风险，但多轮对话逐步改变目标、实体和权限请求时，Stateless Classifier（无状态分类器）无法表达 Session-level Intent（会话级意图） | `deepcontext-intent-drift-2026`; `owasp-llm-top10-2025` | `research_lead` |
| `QUD-E-301` | `evaluation` | Error Propagation Matrix（错误传播矩阵）分别记录 Parse（解析）、Intent（意图）、Entity（实体）、Time（时间）、Business Filter（业务过滤）、Authorization Filter（授权过滤）、Route（路由）、Retrieval（检索）和 Answer（回答）的标签、置信度、最终影响与可恢复性 | 本轮来源与既有结构化查询来源 | `new` |

## 5. 公开面试题来源核验

公开搜索命中 `RAG-SCENE-014`、`RAG-SCENE-015` 和 `RAG-SCENE-022` 已包含 Query Understanding（查询理解）、Query Rewrite（查询改写）、Metadata Filter（元数据过滤）与文档级权限问题。未发现更独立且出处更强的新题目类型，计数不变。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 意图、实体、时间、结构化约束、会话和 OOD Intent（分布外意图）已覆盖 |
| 实现（Implementation） | `covered` | Attribute Schema（属性模式）、可信 Principal（主体）、中文实体基准和时间归一化路线已登记 |
| 工程问题（Engineering Problem） | `covered` | 错误传播、类别长尾、时间范围、权限伪造与多轮漂移已登记 |
| 解决方案（Solution） | `covered` | Schema Allowlist（模式白名单）、分量置信度、澄清、拒识和可信授权注入已覆盖 |
| 评估（Evaluation） | `covered` | Span F1（跨度 F1）、Per-class F1（分类别 F1）、OOD Recall（分布外召回率）、ECE 和传播矩阵已覆盖 |
| 公开面试题（Public Interview Question） | `covered` | 既有公开题可连接，未虚构新增题 |
| 时效（Freshness） | `covered` | 稳定基准、2025 期刊论文和 2026 预印本边界分别标注 |
| 安全或治理（Security or Governance） | `covered` | Prompt Injection（提示注入）、可信授权来源和多轮状态线索已覆盖 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接 Rewrite（改写）、Routing（路由）、Storage Filter（存储过滤）、Retrieval（检索）、Evaluation（评估）和 Generation（生成） |

## 7. 冲突、版本与未验证假设

- CLUENER2020 来自新闻文本；它不代表业务搜索、口语、多轮、省略表达和企业内部实体分布，必须加业务 Gold Set（黄金测试集）。
- Temporal Normalization（时间归一化）论文的跨语言与跨领域结果不能证明对中文业务表达直接有效；需保存 Reference Time（参考时间）和 Locale（区域设置）后复验。
- NOVA 研究的是回答阶段 Verbal Confidence Calibration（口头置信度校准），其价值在于证明“下游置信度不可替代上游诊断”，不是查询理解分类器实现。
- DeepContext 为特定 Multi-turn Adversarial Intent Drift（多轮对抗意图漂移）预印本，只保留研究线索；不能声称已形成行业标准。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3；另有 1 个研究线索 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立中文业务 Query Understanding Test Set（查询理解测试集），覆盖别名、型号、错误码、地址、跨地域、相对时间、否定、范围、多轮指代和可信 Principal（主体）；用组件级标签生成 Error Propagation Matrix（错误传播矩阵）。

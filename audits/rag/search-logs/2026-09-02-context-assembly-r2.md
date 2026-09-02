---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-CONTEXT-ASSEMBLY
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 上下文组装（Context Assembly）第二轮独立补漏

## 1. 本轮目标与边界

专项补查上下文压缩（Context Compression）、固定 Token 预算（Fixed Token Budget）、细粒度事实保真（Fine-grained Fact Fidelity）、父子展开（Parent-child Expansion）、冲突证据分组（Conflicting-evidence Grouping）和信任分区（Trust Partition）。本节点决定模型看见哪些证据及其结构，不把生成器（Generator）的遵循能力算作组装能力。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 压缩研究（Compression Research） | `context compression RAG fine grained facts token budget ACL` | ACL Anthology 原始论文（Original Paper） |
| Q-202 | 框架实现（Framework Implementation） | `site:python.langchain.com contextual compression retriever` | LangChain 官方参考（Official Reference） |
| Q-203 | 证据结构（Evidence Structure） | `evidence based generation citation granularity ACL 2026` | ACL Anthology 综述（Survey） |
| Q-204 | 公开题目（Public Question） | `site:nowcoder.com RAG context compression Lost in the Middle interview` | 牛客公开题库（Public Question Bank） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `sara-context-compression-2026` | 原始论文（Original Paper） | `included` | 补纯压缩丢实体和数值的边界，以及文本片段和语义压缩向量的混合预算 |
| `evidence-based-generation-survey-2026` | 综述（Survey） | `included` | 补文本、表格、图和视觉证据的不同粒度 |
| LangChain Contextual Compression | 官方参考（Official Reference） | `lead_only` | 搜索入口指向旧版模块页；需固定当前包版本后再作为实现契约 |
| `lost-in-the-middle-2024` | 原始论文（Original Paper） | `included_existing` | 已覆盖上下文位置效应，不重复登记 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `CTX-K-201` | `knowledge` | 压缩覆盖率（Compression Coverage）与细粒度事实保真（Fine-grained Fact Fidelity）存在独立权衡，摘要语义相近也可能丢实体、数值和限定词 | `sara-context-compression-2026` | `new` |
| `CTX-P-201` | `problem_question` | 只用语义相似度评估压缩结果，会漏掉数字、否定、日期和引用锚点被改写或删除的错误 | `sara-context-compression-2026` | `new` |
| `CTX-P-202` | `problem_question` | 父子分块展开后若不重新计算 Token 预算和去重，可能把同一证据重复塞入并挤掉互补证据 | 既有父子分块、去重和预算来源 | `new` |
| `CTX-P-203` | `problem_question` | 把可信规则和不可信检索文本拼入同一指令区，会让间接提示注入（Indirect Prompt Injection）获得指令优先级 | 既有 OWASP 与提示注入来源 | `new` |
| `CTX-E-201` | `evaluation` | 上下文组装回归应同时测原子事实保留、证据覆盖、重复率、冲突保留、引用锚点存活、Token 成本及注入越权率 | 新增与既有来源 | `new` |
| `CTX-S-201` | `solution` | 使用结构化证据包（Structured Evidence Package）保留来源 ID、原文跨度、权限、时间和信任级别；摘要或向量压缩仅作为附加表示 | 新增与既有来源 | `extends` |

## 5. 公开面试题来源核验

未发现独立于 `RAG-SCENE-020` 和 `RAG-SCENE-024` 的新题型。现有题目已覆盖长上下文位置、重复片段和冲突证据；本轮补充压缩保真、父子展开和信任分区的答案证据。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 预算、位置、压缩、细粒度保真和冲突结构已覆盖 |
| 实现（Implementation） | `partial` | LangChain 当前包版本和 Token Counter（词元计数器）实现仍需固定 |
| 工程问题（Engineering Problem） | `covered` | 超长、重复、父子扩张、压缩丢失、冲突和注入已登记 |
| 解决方案（Solution） | `covered` | 结构化证据包、原文跨度、信任分区和预算重算已覆盖 |
| 评估（Evaluation） | `covered` | 原子事实、覆盖、重复、锚点、成本和安全指标已覆盖 |
| 公开面试题（Public Interview Question） | `covered` | 公开题库可回链，未虚构新题 |
| 时效（Freshness） | `covered` | 2023—2026 原始研究兼顾 |
| 安全或治理（Security or Governance） | `covered` | 不可信内容与指令分区、权限和来源身份均已进入结构 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接切分、融合、重排、生成、引用和安全 |

## 7. 冲突与边界

- 更高压缩率（Compression Ratio）不等于更高有效上下文利用率；必须保留任务所需的原子事实。
- 语义压缩向量（Semantic Compression Vector）是研究路线，不代表任意生成 API（生成接口）都可直接消费。
- 原文片段保留可以提高可核验性，但会增加 Token 成本；应按事实敏感度和引用要求分配预算。

## 8. 饱和判定

本轮新增知识类型 1、问题类型 3；连续无新增类型轮数为 0，结论为 `round_complete`，不得标记饱和。

## 9. 下一轮动作

固定框架包版本；建立包含数值、否定、时间、表格单元格、父子分块、冲突来源和恶意指令的压缩保真回放集。

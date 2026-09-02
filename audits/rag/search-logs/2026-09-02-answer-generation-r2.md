---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-ANSWER-GENERATION
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 答案生成（Answer Generation）第二轮独立补漏

## 1. 本轮目标与边界

专项补查提示契约（Prompt Contract）、结构化输出（Structured Output）、拒答分支（Refusal Branch）、声明优先生成（Claim-first Generation）、多源冲突表达和面向证据的生成器适配（Evidence-aware Generator Adaptation）。生成节点只负责根据给定证据产出，不修复上游未召回或已丢失的证据。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 结构化输出（Structured Output） | `site:developers.openai.com structured outputs JSON Schema official` | OpenAI 官方文档（Official Documentation） |
| Q-202 | 框架实现（Framework Implementation） | `site:docs.langchain.com structured output schema official` | LangChain 官方文档（Official Documentation） |
| Q-203 | 证据生成（Evidence-based Generation） | `attribution citation quotation evidence based generation ACL 2026` | ACL Anthology 综述（Survey） |
| Q-204 | 冲突证据（Conflicting Evidence） | `cross modal evidence conflict multimodal RAG ACL 2026` | ACL Anthology 原始论文（Original Paper） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `openai-structured-outputs-docs-2026` | 官方文档（Official Documentation） | `included` | 补严格 JSON Schema（JSON 模式）和拒答处理，但不把格式保证扩张为事实保证 |
| `evidence-based-generation-survey-2026` | 综述（Survey） | `included` | 补生成前、生成中和生成后归因路线及证据粒度 |
| LangChain Structured Output | 官方文档（Official Documentation） | `not_added_duplicate` | 提供 Provider / Tool Strategy（提供方/工具策略），未形成独立于结构契约的新知识类型 |
| Multimodal Conflict Paper | 原始论文（Original Paper） | `lead_only` | 留给多模态专项轮次，不用单篇实验支持通用冲突策略 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `GEN-K-201` | `knowledge` | Schema Adherence（模式遵循）、Instruction Following（指令遵循）和 Factual Grounding（事实基于证据）是三种不同保证 | `openai-structured-outputs-docs-2026`; 既有生成来源 | `new` |
| `GEN-P-201` | `problem_question` | 输出完全符合 JSON Schema（JSON 模式）仍可能包含无依据事实、错误引用或冲突合并 | 新增与既有来源 | `new` |
| `GEN-P-202` | `problem_question` | 把拒答仅编码成自然语言字符串会与正常答案 Schema（模式）混淆，导致调用方误处理 | `openai-structured-outputs-docs-2026` | `new` |
| `GEN-P-203` | `problem_question` | 先写完整答案再补引用可能产生找不到支持的声明；先列声明和证据又可能牺牲流畅性 | `evidence-based-generation-survey-2026` | `new` |
| `GEN-S-201` | `solution` | 输出契约显式区分 `answer`、`abstain`、`conflict` 和 `error`，并让每个原子声明携带证据 ID 与支持状态 | 新增与既有来源 | `extends` |
| `GEN-E-201` | `evaluation` | 分别测 Schema 有效率、拒答精确率/召回率、声明支持率、冲突呈现完整性和最终答案正确性 | 新增与既有评估来源 | `new` |

## 5. 公开面试题来源核验

`RAG-SCENE-023` 与 `RAG-SCENE-024` 分别覆盖证据不足时的拒答/回退和多源冲突表达；未把本轮技术扩展虚构成新的面试题。

## 6. 九类覆盖检查

原理、实现、工程问题、解决方案、评估、公开题目、时效、安全治理和跨节点关系均已形成证据入口。仍需在正式章节中按具体模型/接口版本注明 Structured Output（结构化输出）的受支持 Schema 子集和拒答字段行为。

## 7. 冲突与边界

- Strict Schema（严格模式）只约束结构，不证明答案正确或安全。
- 提示词中的“仅依据上下文”是软约束，不是访问控制或事实验证器。
- Claim-first Generation（声明优先生成）是管线设计选项，不应在缺少业务实验时写成通用最优解。

## 8. 饱和判定

本轮新增知识类型 1、问题类型 3；连续无新增类型轮数为 0，结论为 `round_complete`，不得标记饱和。

## 9. 下一轮动作

固定模型与接口版本；用无答案、部分答案、冲突答案、恶意上下文和 Schema 变更样本验证结构、事实、拒答和引用四类独立门禁。

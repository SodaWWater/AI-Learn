---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-ADVANCED-RAG
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 高级检索增强生成（Advanced RAG）第二轮独立补漏

## 1. 本轮目标与边界

专项补查模块化检索增强生成（Modular RAG）、深度研究（Deep Research）、证据感知停止（Evidence-aware Termination）、搜索预算（Search Budget）、轨迹评估（Trajectory Evaluation）、外部搜索风险和跨范式选型。高级路线作为可组合结构，不定义成固定产品清单。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 模块化架构（Modular Architecture） | `Modular RAG LEGO reconfigurable framework original paper` | arXiv 原始论文（Original Paper） |
| Q-202 | 深度研究（Deep Research） | `evidence aware termination enterprise deep research ACL 2026` | ACL Anthology 原始论文（Original Paper） |
| Q-203 | 轨迹基准（Trajectory Benchmark） | `AgenticRAGTracer hop aware benchmark ACL 2026` | ACL Anthology 原始论文（Original Paper） |
| Q-204 | 系统风险（System Risk） | `site:openai.com deep research system card official` | OpenAI 官方系统卡（Official System Card） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `modular-rag-2024` | 原始论文（Original Paper） | `included` | 补模块、操作符、路由、调度和可重构管线 |
| `enterprise-deep-research-termination-2026` | 原始论文（Original Paper） | `included` | 补受控信息流和证据充分性停止，不依赖固定轮数 |
| `agentic-rag-tracer-2026` | 原始论文（Original Paper） | `included` | 补逐跳轨迹和错误传播基准 |
| `openai-deep-research-system-card-2025` | 官方系统卡（Official System Card） | `included` | 补公开深度研究系统的能力、安全评测和风险边界 |
| `deep-researcher-agent-2026` | 预印本（Preprint） | `excluded_irrelevant` | 面向自动化深度学习实验，不是通用研究型检索增强生成证据 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `ADV-K-201` | `knowledge` | Modular RAG（模块化检索增强生成）把检索增强生成拆为可重构模块和操作符，并通过路由与调度形成不同流程 | `modular-rag-2024` | `new` |
| `ADV-K-202` | `knowledge` | Deep Research（深度研究）的停止条件应结合证据覆盖、未解决声明、边际信息增益、冲突和预算，而非只用最大轮数 | `enterprise-deep-research-termination-2026` | `new` |
| `ADV-P-201` | `problem_question` | Agentic RAG（智能体检索增强生成）最终答案正确时，中间仍可能走过越权、无效或不可复现路径，端点指标会漏报 | `agentic-rag-tracer-2026` | `new` |
| `ADV-P-202` | `problem_question` | 外部网页中的间接提示注入、动态内容和失效链接会沿研究轨迹污染规划、证据和引用 | `openai-deep-research-system-card-2025`; 既有安全来源 | `new` |
| `ADV-P-203` | `problem_question` | 模块数量增加会扩大配置空间和错误传播面，若没有统一契约与可观测性，模块化反而降低可维护性 | `modular-rag-2024` | `new` |
| `ADV-S-201` | `solution` | 统一模块输入/输出、权限、预算、证据和错误契约；把每跳动作、来源、状态和停止理由写入可回放轨迹 | 新增来源 | `extends` |
| `ADV-E-201` | `evaluation` | 跨范式比较需固定查询、语料、模型、预算和工具权限，并报告答案、证据、轨迹、成本、停止和安全指标 | 三项新增论文 | `new` |

## 5. 公开面试题来源核验

现有 `RAG-SCENE-005`、`RAG-SCENE-016`、`RAG-SCENE-021` 和 `RAG-SCENE-022` 已覆盖多跳图检索、路由、全链路评估和企业系统设计。未检索到可独立核验的新 Deep Research（深度研究）第一人称面试题，因此不虚构题目。

## 6. 九类覆盖检查

原理、实现、工程问题、解决方案、评估、公开题目、时效、安全治理和跨节点关系均有证据入口。高级路线仍需在图谱阶段拆成能力节点，避免把 GraphRAG（图检索增强生成）、Agentic RAG（智能体检索增强生成）、Multimodal RAG（多模态检索增强生成）、Long-context RAG（长上下文检索增强生成）和 Deep Research（深度研究）混成单一层级。

## 7. 冲突与边界

- “Advanced RAG（高级检索增强生成）”不是统一成熟度等级；不同路线解决不同问题。
- 更长轨迹可能提高覆盖，也会增加错误、成本和攻击面。
- 系统卡（System Card）描述特定产品与评测，不证明所有 Deep Research（深度研究）实现具有同等能力或风险控制。

## 8. 饱和判定

本轮新增知识类型 2、问题类型 3；连续无新增类型轮数为 0，结论为 `round_complete`，不得标记饱和。

## 9. 下一轮动作

构建统一跨范式选型矩阵和逐跳轨迹 Schema（模式）；专项补查多模态间接提示注入、工具权限传播和证据饱和判定的可复现实验。

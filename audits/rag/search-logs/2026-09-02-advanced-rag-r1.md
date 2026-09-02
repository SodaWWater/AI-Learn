---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-ADVANCED-RAG
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：高级检索增强生成（Advanced RAG）第一轮

## 1. 本轮目标与边界

核查 Self-RAG、Corrective RAG、Adaptive RAG、Agentic RAG、GraphRAG、多模态 RAG 及 RAG 与长上下文的边界。高级范式按控制机制、数据结构和检索循环分类，不按名称堆砌。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 自反思 | `site:arxiv.org Self-RAG retrieve generate critique` | 原始论文 |
| Q-002 | 纠错 | `site:arxiv.org Corrective RAG 2401.15884` | 原始论文 |
| Q-003 | 图检索 | `site:arxiv.org From Local to Global GraphRAG 2404.16130` | 原始论文 |
| Q-004 | 多模态 | `site:arxiv.org ColPali visual document retrieval late interaction` | 原始论文 |
| Q-005 | Agentic | `site:learn.microsoft.com agentic retrieval overview 2026` | 官方文档 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `self-rag-2023` | 原始论文 | `included` | Adaptive Retrieve/Generate/Critique |
| `corrective-rag-2024` | 原始论文 | `included` | 检索评估与纠错分支 |
| `adaptive-rag-2024` | 原始论文 | `included` | 问题复杂度路由 |
| `graphrag-local-global-2024` | 原始论文 | `included` | Community Hierarchy 与全局问题 |
| `colpali-2024` | 原始论文 | `included` | 视觉文档多向量检索 |
| `agentic-rag-survey-2025` | 综述论文 | `included` | 分类线索，结论回到原始论文 |
| `azure-agentic-retrieval-overview-2026` | 官方文档 | `included` | 当前工程实现和 GA/Preview 边界 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `ADV-K-001` | `knowledge` | 高级 RAG 可按是否检索、如何纠错、循环控制、数据结构和模态分类 | `new` |
| `ADV-P-001` | `problem_question` | Agentic Retrieval 多轮搜索没有停止条件导致成本失控 | `new` |
| `ADV-P-002` | `problem_question` | GraphRAG 用于局部事实问题可能增加无必要的建图成本 | `new` |
| `ADV-P-003` | `problem_question` | 多模态检索直接索引页面图像会增加存储、延迟和解释难度 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 短转述 | 来源类型 | 是否真实面试 | 技术核验 |
|---|---|---|---|---|
| `RAG-SCENE-005` | GraphRAG 多跳与路径爆炸怎样处理 | 项目型考题 | 否 | GraphRAG 论文和官方文档 |
| `RAG-SCENE-011` | 混合模态 PDF 怎样检索和引用 | 公开题库 | 否 | ColPali、解析官方文档 |
| `RAG-SCENE-016` | 何时选择 Adaptive/Self/Corrective/Agentic RAG | 公开题库 | 否 | 各原始论文 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理 | `covered` | 五类高级路线 |
| 实现 | `covered` | GraphRAG 与 Agentic Retrieval 当前入口 |
| 工程问题 | `covered` | 成本、停止、建图、模态 |
| 解决方案 | `partial` | Deep Research 和 Modular RAG 待补 |
| 评估 | `partial` | 跨范式统一基准待补 |
| 公开面试题 | `covered` | 项目考题与题库 |
| 时效 | `covered` | 2023–2026 |
| 安全或治理 | `partial` | Agent 外部搜索和多模态注入待补 |
| 跨节点关系 | `covered` | 路由、检索、生成、评估、生产 |

## 7. 冲突、版本与未验证假设

- Advanced RAG 不是固定产品清单；
- GraphRAG、Agentic RAG 和 Long Context 需按问题类型、语料、成本选择；
- 下一轮补 Modular RAG、Deep Research、停止条件和统一选型矩阵。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补 Modular RAG、Deep Research、信息饱和、搜索预算、停止条件及跨范式评估。

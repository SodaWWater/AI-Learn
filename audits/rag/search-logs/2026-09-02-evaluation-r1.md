---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-EVALUATION
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：评估（Evaluation）第一轮

## 1. 本轮目标与边界

核查解析、检索、重排、生成、引用和端到端分层评估，Golden Dataset、自动评估、LLM-as-a-Judge、失败归因及线上指标。单一 Recall@K 或 Faithfulness 不能证明系统整体可用。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 框架 | `site:aclanthology.org RAGAS automated evaluation RAG` | RAGAS 论文 |
| Q-002 | 少标注评估 | `site:arxiv.org ARES automated evaluation RAG` | ARES 论文 |
| Q-003 | 诊断 | `site:arxiv.org RAGChecker fine-grained diagnosis` | RAGChecker 论文 |
| Q-004 | Judge 偏差 | `site:arxiv.org MT-Bench LLM-as-a-Judge bias` | 原始论文 |
| Q-005 | 公开题目 | `site:nowcoder.com/discuss RAG 评估 面试 Recall Faithfulness` | 公开题库与面经 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `ragas-eacl-2024` | 原始论文 | `included` | Reference-free 指标与框架 |
| `ares-rag-evaluation-2024` | 原始论文 | `included` | 合成训练数据、少量标注和统计估计 |
| `ragchecker-2024` | 原始论文 | `included` | Retriever/Generator 细粒度归因 |
| `llm-as-judge-mtbench-2023` | 原始论文 | `included` | Position、Verbosity 和 Self-enhancement Bias |
| `mteb-2023` | 原始论文 | `included` | Embedding 多任务评估边界 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `EVAL-K-001` | `knowledge` | 阶段指标、端到端指标和线上业务指标解决不同问题 | `new` |
| `EVAL-P-001` | `problem_question` | 自动 Judge 与人工标准不一致或受答案长度/顺序影响 | `new` |
| `EVAL-P-002` | `problem_question` | Golden Dataset 高频样本过多而漏掉长尾和负例 | `new` |
| `EVAL-P-003` | `problem_question` | 指标提升来自不同候选集、模型或成本，实验不可比 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 短转述 | 来源类型 | 是否真实面试 | 技术核验 |
|---|---|---|---|---|
| `RAG-SCENE-001` | Recall@5 好到什么程度才算足够 | 第一人称面经 | 发布者自述 | RAGAS、ARES、RAGChecker |
| `RAG-SCENE-021` | 怎样全面评估并归因 RAG 失败 | 公开题库 | 否 | RAGAS、ARES、RAGChecker、MT-Bench |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理 | `covered` | 分层、端到端、线上评估 |
| 实现 | `covered` | RAGAS、ARES、Tracing 入口 |
| 工程问题 | `covered` | 偏差、泄漏、分布和不可比实验 |
| 解决方案 | `partial` | 统计功效、Judge 校准和采样待补 |
| 评估 | `covered` | 本节点核心指标已覆盖 |
| 公开面试题 | `covered` | 第一人称和题库 |
| 时效 | `covered` | 2023–2024 框架与 2026 工程入口 |
| 安全或治理 | `partial` | 红队和安全回归集待补 |
| 跨节点关系 | `covered` | 覆盖全部链路阶段 |

## 7. 冲突、版本与未验证假设

- 不把 LLM-as-a-Judge 当作绝对真值；
- 合成数据不能替代真实线上分布；
- 下一轮补统计显著性、Judge 校准、数据泄漏和线上代理指标。

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

补统计功效、Bootstrap、Judge 校准、泄漏防控、长尾采样、线上 A/B 与安全回归集。

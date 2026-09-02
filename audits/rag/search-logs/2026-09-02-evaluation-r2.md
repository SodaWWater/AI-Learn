---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-EVALUATION
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 评估（Evaluation）第二轮独立补漏

## 1. 本轮目标与边界

专项补查统计不确定性（Statistical Uncertainty）、配对比较（Paired Comparison）、裁判校准（Judge Calibration）、对抗裁判（Adversarial Judge）、长尾采样（Long-tail Sampling）、数据泄漏（Data Leakage）、线上代理指标（Online Proxy Metric）和安全回归集（Safety Regression Set）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 裁判脆弱性（Judge Vulnerability） | `Judging the Judges alignment vulnerabilities LLM as judge ACL` | ACL Anthology 原始论文（Original Paper） |
| Q-202 | 法律检索增强生成（Legal RAG） | `LLM as judge legal document recommendation RAG evaluation` | 原始研究（Primary Research） |
| Q-203 | 轨迹评估（Trace Evaluation） | `AgenticRAGTracer hop aware benchmark ACL 2026` | ACL Anthology 原始论文（Original Paper） |
| Q-204 | 公开题目（Public Question） | `site:nowcoder.com RAG evaluation LLM as judge monitoring interview` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `llm-judge-vulnerabilities-2025` | 原始论文（Original Paper） | `included` | 补裁判与人类偏好对齐及对抗脆弱性 |
| `agentic-rag-tracer-2026` | 原始论文（Original Paper） | `included` | 补多跳轨迹和节点级错误诊断 |
| `ragas-2023` / `ares-2024` | 论文与框架（Paper and Framework） | `included_existing` | 已覆盖自动评估入口，不重复登记 |
| `nowcoder-rag-evaluation-2026` | 工程说明（Engineering Explainer） | `not_added_duplicate` | 与 `RAG-SCENE-021` 的链路评估问题同型，未增加独立题目 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `EVAL-K-201` | `knowledge` | LLM-as-a-Judge（大语言模型裁判）是需校准的测量工具，不是无误差真值标注器 | `llm-judge-vulnerabilities-2025` | `new` |
| `EVAL-P-201` | `problem_question` | 同一裁判模型可能受答案长度、措辞、顺序、身份或对抗文本影响，造成策略对比反转 | `llm-judge-vulnerabilities-2025` | `new` |
| `EVAL-P-202` | `problem_question` | 只报告平均分会掩盖长尾查询、安全样本和多跳路径的系统性失败 | 新增与既有来源 | `new` |
| `EVAL-P-203` | `problem_question` | 评测集与训练/调参数据重合会造成泄漏，且重复运行同一测试集可能间接过拟合 | 既有评估方法来源 | `new` |
| `EVAL-S-201` | `solution` | 使用冻结版本的成对回放、分层抽样、人工锚点集、多裁判一致性、盲序交换和置信区间共同决定发布 | 新增与既有来源 | `extends` |
| `EVAL-E-201` | `evaluation` | Agentic RAG（智能体检索增强生成）除最终答案外还要评价每跳检索、状态转移、停止和错误传播 | `agentic-rag-tracer-2026` | `new` |

## 5. 公开面试题来源核验

未新增题目编号；`RAG-SCENE-001` 和 `RAG-SCENE-021` 已覆盖评测集规模/分布、基线、分层归因和 LLM-as-a-Judge（大语言模型裁判）校准。

## 6. 九类覆盖检查

九类覆盖均有入口；统计功效（Statistical Power）和置信区间的具体计算将在正式评估章节以可复现实验脚本呈现，避免在检索日志中写死样本量。

## 7. 冲突与边界

- 裁判与人类一致率高不代表对所有领域、语言和攻击样本都可靠。
- 统计显著（Statistically Significant）不等于业务收益足够大，仍需报告效应量（Effect Size）。
- 线上点击、采纳或停留时长可能受界面和用户群变化影响，不能直接等同于事实质量。

## 8. 饱和判定

本轮新增知识类型 1、问题类型 3；连续无新增类型轮数为 0，结论为 `round_complete`，不得标记饱和。

## 9. 下一轮动作

生成冻结的评测协议：数据分割、分层标签、配对 Bootstrap（自助法）、效应量、裁判盲序、人工校准、安全回归和线上 Guardrail（护栏指标）。

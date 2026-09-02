---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DOCUMENT-PARSING
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 文档解析（Document Parsing）第二轮独立补漏

## 1. 本轮目标与边界

复核 ParseBench 新版本，并专项检查公式、代码、表格、阅读顺序和 Agent 下游任务的评估边界。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 基准 | `site:arxiv.org document parsing benchmark reading order formulas tables OCR RAG 2026` | arXiv |
| Q-202 | 多模态 | `site:arxiv.org visual document retrieval parsing-free ColPali` | arXiv |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `parsebench-2026` | 原始论文 | `included_version_update` | 从 v1 更新到 v2，后续提取任务级指标 |
| `colpali-2024` | 原始论文 | `included` | 解析后文本路线之外的页面视觉检索 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关系 |
|---|---|---|---|
| `PARSE-K-201` | `knowledge` | 文档解析质量需用 Agent 下游任务而非纯字符相似度验证 | `extends` |
| `PARSE-C-201` | `conflict` | 解析为文本与直接页面视觉检索是替代/组合路线 | `new` |

## 5. 公开面试题来源核验

未新增题目来源；继续使用 `RAG-SCENE-011` 多模态 PDF 场景。

## 6. 九类覆盖检查

评估与多模态路线新增覆盖；公式、代码、中文竖排、跨页表格的专项基准仍不足。

## 7. 冲突、版本与未验证假设

不得假设视觉检索可以替代所有结构化解析；引用、表格计算和可编辑文本仍有不同需求。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题/冲突类型数 | 1 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

提取 ParseBench v2 子任务，补公式、代码、中文阅读顺序与跨页表格基准。

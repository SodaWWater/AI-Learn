# 知识原子覆盖与语义审计（Knowledge Atom Coverage and Semantic Audit）

> 审计日期：2026-09-04
> 状态：`completed_bounded_semantic_audit`。正式发布集合限定为有来源且通过语义审核的原子；无来源原子仍保留为库存占位。

## 范围与口径

本审计登记 `knowledge/rag/graph.json` 中全部 `type=knowledge` 的 191 个知识原子。每条记录的 `source_refs` 原样继承图谱节点，不新增来源。189 个有来源原子已完成逐项语义边界审核；2 个无来源原子被明确排除，不作为正式结论。

`single_conclusion_status` 记录本次有界验收结果：有来源的原子标为 `reviewed_single_conclusion`，无来源的原子标为 `excluded_inventory_no_source`。无来源原子仍保留在库存中用于追踪缺口，不进入正式结论。

## 统计

| 模块 | 原子数 |
|---|---:|
| RAG-01 | 10 |
| RAG-02 | 10 |
| RAG-03 | 15 |
| RAG-04 | 17 |
| RAG-05 | 16 |
| RAG-06 | 15 |
| RAG-07 | 12 |
| RAG-08 | 16 |
| RAG-09 | 16 |
| RAG-10 | 14 |
| RAG-11 | 19 |
| RAG-12 | 20 |
| RAG-13 | 11 |
| **合计** | **191** |

- 已登记来源覆盖：189 个
- 未登记来源：2 个（`RAG-07-001`、`RAG-13-011`）
- 单一结论人工语义审核：189 个原子已完成并标记 `reviewed_single_conclusion`；2 个无来源原子标记 `excluded_inventory_no_source`

## 无来源原子处置

- `RAG-07-001`：图谱节点无来源引用，保留在库存审计中，不作为正式知识结论。
- `RAG-13-011`：图谱节点无来源引用，保留在库存审计中，不作为正式知识结论。

## 正式集合边界

- 正式知识原子：189 个，全部具有登记来源并通过单一结论语义审核。
- 排除库存占位：2 个，仅用于记录覆盖缺口，不进入正式章节结论、来源统计或发布承诺。
- 本审计证明固定登记范围内的覆盖，不宣称互联网永久完整；动态产品/API 行为仍按审核日期周期复核。

## 机器可读明细

逐项记录见 [`atom-audit.json`](atom-audit.json)。审计消费者应至少校验：原子 ID 唯一、模块计数为 191、`source_count` 等于 `source_refs` 长度、来源引用与图谱节点一致，以及无来源原子仅为上述两个 ID。

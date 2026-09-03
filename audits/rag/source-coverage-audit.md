# 检索增强生成（Retrieval-Augmented Generation，RAG）原始来源双向覆盖与去重审计

> 状态：`completed`
> 审计日期：2026-09-04
> 范围：`sources/registry.json` 登记的四个原始来源、`audits/rag/source-units.json` 的 695 个来源单元，以及 `accepted-mappings.json` 和 `reviewed/*.json` 的人工决定。

## 结论

- 695/695 个来源单元均有明确去向：653 个语义单元有人工决定，42 个非语义单元已有结构、资源或占位分类；不存在无去向来源单元。
- 653/653 个语义单元均只出现一次于人工映射记录，且每项都有 `map`、`retain`、`exact_duplicate`、`partial_overlap`、`cross_node` 或 `non_rag` 之一。
- 641 个语义单元连接到 189 个规范知识原子；12 个 `non_rag` 单元保留明确排除理由，不作为 RAG 正式知识。
- 18 个 `exact_duplicate` 决定均指向规范知识原子；222 个 `partial_overlap` 和 94 个 `cross_node` 决定均保留原子关系，未因主题相近而删除独有信息。
- 当前 191 个知识原子中有 189 个获得至少一个原始来源单元反向支持。`RAG-07-001` 与 `RAG-13-011` 尚未有该映射，作为规范知识库阶段的待处理项登记，不能声称知识到来源映射已全量完成。

## 来源到去向

| 来源 | 语义单元 | 人工决定 | 非语义单元 | 结论 |
|---|---:|---|---:|---|
| `xiaolin-ai-learning` | 127 | map 17, retain 39, exact duplicate 17, partial overlap 27, cross node 27 | 0 | 全部有去向 |
| `ai-agent-interview-guide` | 80 | map 14, retain 45, partial overlap 14, cross node 7 | 3 structural | 全部有去向 |
| `agent-guide` | 409 | map 62, retain 93, exact duplicate 1, partial overlap 181, cross node 60, non-RAG 12 | 32 structural, 4 resource, 3 placeholder | 全部有去向 |
| `user-rag-experience-pdf` | 37 | map 37 | 0 | 全部有去向 |
| **合计** | **653** | **map 130, retain 177, exact duplicate 18, partial overlap 222, cross node 94, non-RAG 12** | **42** | **695/695** |

人工映射文件合计包含 653 个唯一来源单元引用。机械分类的 42 个非语义单元不进入人工语义审核分母，其中包括 35 个 structural、4 个 resource 与 3 个 placeholder。

## 去重与排除

`exact_duplicate` 只用于来源清单、过渡标题或相同正文的重复登记，所有 18 项均保留 `duplicate_of_atom_ids` 或 `atom_ids` 指向。它们不会抹除正文、实现条件、边界或独立来源定位。

12 个 `non_rag` 单元均来自 `agent-guide`，排除原因已经逐项写入审核批次：

- `RU-7a29f0bc8394` 为单 Agent（Agent）与多 Agent（Multi-Agent）架构，自动分类错误；
- `RU-b9d282ef59a6` 为通用 Vibe Coding 技术债务讨论；
- `RU-01177dc9a633`、`RU-5b1157083b9e`、`RU-97cbf6668da6` 为通用提示工程（Prompt Engineering）内容；
- `RU-f024fdc053b9`、`RU-705e35bac80e`、`RU-c9d4d0aeb162`、`RU-c2282224bf3c` 为求职或面试表达建议；
- `RU-08f92884a1e1`、`RU-c330aa5c86ce`、`RU-5b86f3ad8faf` 为阅读或面试索引，不提供独立 RAG 技术结论。

这些单元被排除出 RAG 正式知识，不等于删除来源记录；其来源 ID、正文审核批次和原因均可回溯。

## 知识到来源

人工映射将 641 个语义单元反向连接到 189 个原子。单个已映射原子至少有 1 个、最多有 71 个来源单元支持。下列两个现有原子尚无来源反向映射，必须在 `WP-P3-001` 规范知识库整理时补充已登记证据或降级/移除，当前不标记为已验收：

| 原子 | 标题 | 状态 |
|---|---|---|
| `RAG-07-001` | Query 清洗、规范化与语言检测 | 缺少原始来源反向映射 |
| `RAG-13-011` | 不同岗位的 RAG 回答深度 | 缺少原始来源反向映射 |

## 可复核路径

1. 用 `python scripts/review_queue.py --summary` 检查 653/653 人工审核覆盖。
2. 阅读 [`accepted-mappings.json`](accepted-mappings.json) 及 [`reviewed`](reviewed) 内的批次记录，按来源单元 ID 回溯每项判断。
3. 对照 [`source-units.json`](source-units.json) 的 695 个固定 ID 和 [`catalog.json`](../../knowledge/rag/catalog.json) 的 191 个原子。
4. 运行 `python scripts/validate_repo.py` 和 `git diff --check` 验证仓库基本一致性；`--strict-rag` 仍会因后续知识库、图谱和学习产物门禁未完成而失败，这不是来源单元遗漏。

# RAG 严格验收审计（P8 Strict Acceptance Audit）

> 审计日期：2026-09-04  
> 工作项：`WP-P8-001`  
> 范围：只使用仓库内已有来源登记、人工审核、证据核验、图谱审计和生成产物；未恢复外部搜索。

## 结论

当前验收清单的 23 项均已在当前登记范围内完成，证据均可由仓库内文件复核。正式发布集合限定为 189 个有来源知识原子；`RAG-07-001` 与 `RAG-13-011` 明确排除为无来源 `inventory_draft` 库存占位。动态产品/API 行为保留周期复核责任，因此本报告不宣称互联网永久完整。

## 已验收项目

| 验收项 | 证据 | 结论 |
|---|---|---|
| 只有适用条件和语义均等价的内容标记为 `duplicate` | `audits/rag/source-coverage-audit.md`；`audits/rag/canonical-consolidation.json` | 18 个 `exact_duplicate` 均指向规范原子，部分重叠与跨节点信息保留。 |
| 冲突内容进入冲突表并完成核验或明确标记待核验 | `audits/rag/graph-coverage-audit.json` 的 `conflict_and_version_audit` | 冲突主题均有边界、来源版本和状态。 |
| 变化内容记录版本和审核日期 | `audits/rag/evidence-verification-status.json`；同上审计的版本记录 | 已登记来源均有核验状态；版本敏感边界被保留。 |
| 每个来源单元都映射到标准知识、参考资源、占位或结构单元之一 | `audits/rag/source-coverage-audit.md`；`audits/rag/original-source-coverage.md` | 695/695 来源单元有明确去向。 |
| 总导图覆盖全部一级知识模块 | `learning/rag/overview.md`；`learning/rag/graph-views.md` | 总览列出 13 个模块，图谱投影覆盖 18 个 RAG 流程节点及已登记跨主干节点。 |
| 原始题目能够反向定位到标准知识点 | `audits/rag/graph-coverage-audit.json`；`knowledge/rag/graph.json` | 问题到节点和节点到问题的受控边通过图谱审计，未发现反向映射不一致。 |
| 场景题均有公开原始出处和来源类型，不包含自拟公司题目 | `interview/rag/public-scenarios.json`；`audits/rag/graph-coverage-audit.json` | 26 个场景均登记 URL、来源类型和非企业真题边界。 |
| 13 个一级模块均有正式有界章节，章节覆盖目录原子 | `knowledge/rag/chapters/`；`audits/rag/chapter-problem-links.json`；`audits/rag/atom-audit.json` | RAG-01 至 RAG-13 均有四段式正式有界章节；章节正文合计引用 191/191 个原子 ID。 |
| 子导图覆盖目录原子且不另造结论 | `learning/rag/maps/`；`audits/rag/atom-audit.json` | RAG-01 至 RAG-13 均有模块图；各图只引用对应目录原子，覆盖 191/191。 |
| 学习正文、概要、对比、关系图引用知识点 ID | `knowledge/rag/chapters/`；`learning/rag/maps/`；`audits/rag/chapter-problem-links.json` | 13 个正式有界章节和 13 张模块图均保留原子 ID；章节问题链接审计已覆盖全部模块。 |
| 完成来源到知识、知识到来源的双向抽查 | `audits/rag/source-coverage-audit.md`；`audits/rag/graph-coverage-audit.json` | 来源单元、规范原子和图谱证据关系可按 ID 双向回查。 |

## 完成边界

1. 知识原子单一结论检查：191 个原子逐项登记，189 个有来源原子标记为 `reviewed_single_conclusion`；2 个无来源原子标记为 `excluded_inventory_no_source`。
2. 关系保留检查：`contains` 与 `implements` 作为受控图边保留；`extends` 与 `compares` 的来源审计记录保留，当前登记中无对应记录，不新增虚假关系。
3. 正式知识来源检查：189 个正式原子全部有来源；两个库存占位不纳入正式发布集合。
4. 13 个一级模块均通过概要、原理、工程实现、权衡、对比、关系、错误和评估检查；章节和子图覆盖 191/191 原子并显式标注排除项。
5. 一手资料与经典论文缺口检查已完成登记范围内闭环；未覆盖范围、来源时效和证据边界均显式记录。
6. 变化较快内容已按来源审核日期登记当前复核结果，并保留周期复核责任，不把动态行为当作永久事实。

## 验证命令

```text
python scripts/validate_repo.py
git diff --check
python scripts/validate_repo.py --strict-rag
```

普通校验、差异检查和严格校验均应通过。后续维护工作是按审核日期复核动态产品/API 行为，并在获得明确授权后再扩展外部搜索范围。

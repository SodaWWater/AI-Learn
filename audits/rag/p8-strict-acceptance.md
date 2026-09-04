# RAG 严格验收审计（P8 Strict Acceptance Audit）

> 审计日期：2026-09-04  
> 工作项：`WP-P8-001`  
> 范围：只使用仓库内已有来源登记、人工审核、证据核验、图谱审计和生成产物；未恢复外部搜索。

## 结论

当前验收清单由 16 项未完成减少为 8 项未完成。已勾选项目均有仓库内可复核证据；剩余项目不因候选章节或库存级图谱而提前通过。`python scripts/validate_repo.py --strict-rag` 因这 8 项未完成而继续失败，因此当前版本只能发布为候选版，不能称为 RAG 全库正式版。

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
| 完成来源到知识、知识到来源的双向抽查 | `audits/rag/source-coverage-audit.md`；`audits/rag/graph-coverage-audit.json` | 来源单元、规范原子和图谱证据关系可按 ID 双向回查。 |

## 保留为未完成项目

1. 知识原子单一结论检查：当前缺少对 191 个原子逐项的独立语义审计。
2. `extends`、`contains`、`implements`、`compares` 保留检查：现有图模型已审计部分受控关系，但尚未生成与该旧清单口径完全对应的保留证明。
3. 每个标准知识点至少一个来源：`RAG-07-001` 和 `RAG-13-011` 仍无来源反向映射。
4. 每个一级模块完成概要、原理、工程实现、权衡、对比、关系、错误和评估检查：目前只有 `RAG-01` 至 `RAG-03` 为正式候选章节。
5. 使用一手资料与经典论文完成缺口检查：全库正式章节尚未完成，不能用候选章节替代全库缺口审计。
6. 变化较快内容的当前版本复核：来源证据已核验，但全库正式正文尚未完成周期复核闭环。
7. 子导图覆盖标准知识点且不另造结论：当前仅生成 `RAG-01` 至 `RAG-03` 模块图。
8. 学习正文、知识概要、概念对比和关系图均引用知识点 ID：全库仍有未生成的正式正文和视图；因此 `RAG-01` 至 `RAG-03` 之外的正式内容和对应审计仍未完成，不能将候选状态升级为正式发布。

## 验证命令

```text
python scripts/validate_repo.py
git diff --check
python scripts/validate_repo.py --strict-rag
```

普通校验和差异检查应通过；严格校验预期因剩余 8 项清单未完成而失败。下一版本应优先补齐无来源原子处置、全模块章节/子图和全库内容引用审计。

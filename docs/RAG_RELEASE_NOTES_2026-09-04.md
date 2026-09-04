# RAG 候选版本发布说明（2026-09-04）

## 版本状态

当前发布物为 `formal_candidate / strict_acceptance_pending`，不是检索增强生成（Retrieval-Augmented Generation，RAG）全库正式版。严格验收清单剩余 8 项，详见 [`audits/rag/p8-strict-acceptance.md`](../audits/rag/p8-strict-acceptance.md)。

## 本次纳入

- 653/653 个原始来源语义单元完成人工审核，695/695 个来源单元有明确去向。
- 169 个已登记外部来源完成事实、版本和时效核验；1 个用户批准的不可访问来源保持非证据豁免。
- 完成 437 节点、1930 条受控边的库存级有向图谱及结构/覆盖审计。
- 完成 18 个流程节点的问题库存和 22 个跨节点问题库存；均保持 `inventory-only`，不伪造正式答案。
- `RAG-01` 至 `RAG-03` 按四段式标准生成正式候选章节，并生成章节到问题的链接审计。
- 严格验收清单中 15 项已有证据的项目已勾选，8 项证据不足项目保持未完成。

## 已知限制

- `RAG-07-001` 与 `RAG-13-011` 尚无来源反向映射，不能作为已验证正式知识。
- `RAG-04` 至 `RAG-13` 尚未全部生成正式章节和模块图。
- `RAG-01` 至 `RAG-03` 仍为候选章节；动态产品/API 行为需要按登记版本周期复核。
- 新的外部搜索按用户决策暂停；第四轮仅保留已完成的 4/18 历史检查点。

## 复核命令

```bash
python scripts/validate_repo.py
git diff --check
python scripts/validate_repo.py --strict-rag
```

## 下一工作项

继续 `WP-P8-001`：完成剩余 8 个验收门，或明确将其拆入下一版本范围；在严格校验通过前不得宣布全库正式完成。

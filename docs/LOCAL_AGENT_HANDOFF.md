# 本地 Agent 无偏差续作手册

> 状态：`authoritative / active`  
> 更新日期：2026-09-04
> 当前任务：维护范围受限正式版本；按审核日期复核动态内容
> 本文件解决的是“新 Agent 不读取聊天记录，也能从唯一检查点继续”的问题。

## 1. 当前已经完成什么

- 4 个用户指定来源已经固定版本并登记；
- 695 个来源单元（Source Unit）已经机械盘点；
- 其中 653 个是检索增强生成（Retrieval-Augmented Generation，RAG）语义内容单元，42 个已经标为结构、资源或占位单元；
- 653 个语义单元已全部完成人工审核，所有 695 个来源单元均有显式去向；
- `xiaolin-ai-learning`、`ai-agent-interview-guide`、`agent-guide` 和用户 PDF 均已完成审核；
- 用户 PDF《大模型 RAG 经验面》37/37 已人工审核完成；
- 18 个流程节点的三轮外部检索已经完成；
- 当前登记 170 个外部时效/一手来源和 26 条公开工程问题/面试题线索；
- 第四轮只完成 4/18，结果保留为历史检查点，不继续剩余 14 个节点。

当前正式发布集合包含 189 个有来源知识原子；`RAG-07-001` 与 `RAG-13-011` 为无来源 `inventory_draft` 库存占位，不得作为已验证结论。

## 2. 已完成的执行顺序与当前维护边界

1. 已暂停继续向外搜索；
2. 已完成 4 个原始来源的逐单元人工语义审核；
3. 已完成保留、完全重复、部分重叠、跨节点或非检索增强生成内容的判断；
4. 已生成可核验的原始来源覆盖报告，证明每个单元均有去向；
5. 已使用登记来源完成事实、时效和冲突核验；
6. 已建立去重后的标准知识库和底层知识图谱；
7. 已生成完整流程前置内容、多张关系图、问题库存和正式有界知识章节；
8. 当前只按审核日期复核动态产品/API 行为；恢复外部搜索需用户明确授权。

上述质量门已全部通过；正式学习入口为 `learning/rag/overview.md`。

## 3. 当前维护队列

当前没有待审语义单元。维护顺序固定为：

1. 按 `audits/rag/dynamic-version-audit.json` 的审核日期复核动态产品/API 内容；
2. 复核 `RAG-07-001` 与 `RAG-13-011` 是否获得合规来源；
3. 只有用户明确授权后，才恢复外部搜索并建立下一版本工作包。

查看当前维护状态：

```bash
python scripts/review_queue.py --summary
```

当前队列应显示待审数量为 0；如需新增来源，先登记来源、版本和许可，再创建新的审核工作包。

## 4. 审核时必须阅读正文

`audits/rag/source-units.json` 中的标题只用于定位，不能替代正文。三个公开仓库必须按 `sources/registry.json` 中登记的固定 Commit 检出到 `AI-Learn` 仓库外的临时目录，再阅读单元所在位置及必要的上下文。

示例原则：

- 使用固定 Commit，不使用来源仓库当前 `main` 分支推断；
- 临时副本不要提交进 `AI-Learn`；
- 对无仓库许可证或许可不明确的内容，只记录定位、短转述、自己的结构化结论和来源关系，不复制整段原文；
- 无法读取正文时，将本批标为阻塞并停止，不能根据标题猜测结论；
- 用户 PDF 已完成审核，不需要本地 Agent 重新取得原文件。

## 5. 每个来源单元的判断

每个待审语义单元必须有且只有一个主判断，并可附多个关系：

| 主判断 | 使用条件 | 处理方式 |
|---|---|---|
| `retain` | 包含独立结论、条件、实现、反例、问题或验证信息 | 映射已有知识原子；不存在合适原子时新建，不得硬塞 |
| `exact_duplicate` | 语义、适用条件和结论全部等价 | 保留来源关系并指向规范知识，不复制正文；说明与谁完全重复 |
| `partial_overlap` | 主题相似，但条件、实现、边界、反例或结论至少一项不同 | 独立信息全部保留，并记录重叠与差异 |
| `cross_node` | 同时影响多个流程节点或技术主干 | 建立多个目标映射和明确的有向关系，不强行归入单一章节 |
| `non_rag` | 正文确实不属于检索增强生成（Retrieval-Augmented Generation，RAG）试点范围 | 记录排除原因和更合适的人工智能（Artificial Intelligence，AI）分类 |

“同一个主题”“标题相似”或“答案都提到同一框架”都不是完全重复。题目可以重复出现，但其中独有的工程条件、方案、代码实现、评估方法和失败边界必须保留。

## 6. 每批产出与检查点

每批新增一个 `audits/rag/reviewed/<batch-id>.json`，结构参考 `templates/source-review-batch.json`。同时更新：

- `knowledge/rag/catalog.json`：必要时新增或修正知识原子；
- `audits/rag/manual-review-status.json`：更新审核数量和当前游标；
- `audits/rag/original-source-coverage.md`：更新人类可读覆盖率；
- `audits/rag/work-status.json`：更新完成内容和下一批；
- 冲突、跨节点关系或术语表：仅在本批证据确实需要时更新。

每批结束必须运行：

```bash
python scripts/review_queue.py --summary
python scripts/validate_repo.py
git diff --check
```

普通校验通过后创建小型 Git Commit（Git 提交）检查点；拥有远端权限时推送。当前登记范围的严格校验已经通过；后续只在新增来源或版本复核时重新运行，不得为了让它变绿而伪造映射。

## 7. 明确禁止

- 不继续第四轮剩余外部搜索；
- 不重新执行已完成的前三轮搜索；
- 不把第四轮 4/18 删除或改写成 18/18；
- 不根据标题或自动分类直接批量“人工通过”；
- 不为了减少数量而合并部分重叠信息；
- 不先写正式学习正文，再倒推来源；
- 不把没有公开出处的自拟题包装成真实面试题；
- 不把旧 `RAG-01` 至 `RAG-03` 第一版当正式内容；
- 不更改“每次出现专业术语都双语说明”的规则；
- 不加入口诀、30 秒/2 分钟回答、遮挡式自测或面试话术。

## 8. 给本地 Agent 的启动提示词

将以下内容原样发送给在 `AI-Learn` 仓库根目录启动的本地 Agent：

```text
请继续本仓库的 RAG 学习资料工程，并严格以仓库文件为唯一事实来源，不依赖之前的聊天记录自行猜测。

开工前依次完整阅读：
1. AGENTS.md
2. docs/PROJECT_PLAN.md
3. audits/rag/work-status.json
4. docs/RAG_EXECUTION_ROADMAP.md
5. docs/LOCAL_AGENT_HANDOFF.md
6. audits/rag/manual-review-status.json
7. knowledge/rag/TERMINOLOGY.md
8. knowledge/rag/CONTENT_STANDARD.md
9. taxonomy/rag-graph-model.json

当前用户决策：停止新的外部搜索。前三轮 18/18 和第四轮 4/18 只作为已保存证据；不得继续第四轮剩余 14 个节点。`audits/rag/manual-review-status.json` 显示 653/653 个语义单元已审核、待审数量为 0。正式发布集合包含 189 个有来源原子，`RAG-07-001` 与 `RAG-13-011` 仅为无来源库存占位。正式学习入口为 `learning/rag/overview.md`。

先运行 `python scripts/review_queue.py --summary` 确认待审数量为 0，再按 `audits/rag/dynamic-version-audit.json` 的审核日期复核动态产品/API 内容。不得恢复外部搜索或把库存占位写成正式结论；如需新增来源或补充原子，必须先获得用户明确授权并建立下一版本工作包。

维护完成后运行 `python scripts/validate_repo.py`、`python scripts/validate_repo.py --strict-rag` 和 `git diff --check`，并更新 `audits/rag/work-status.json` 与发布说明。不要重复执行已完成的来源审核、章节生成或历史搜索轮次。
```

## 9. Agent 中断时的交接格式

```text
当前批次：
最后完成的来源单元：
本批 retain / exact_duplicate / partial_overlap / cross_node / non_rag 数量：
新增或修正的知识原子：
未解决冲突：
校验结果：
最新 Git Commit：
下一来源单元：
```

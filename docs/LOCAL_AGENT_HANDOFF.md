# 本地 Agent 无偏差续作手册

> 状态：`authoritative / active`  
> 更新日期：2026-09-03  
> 当前任务：首批原始资料人工语义审核与覆盖证明  
> 本文件解决的是“新 Agent 不读取聊天记录，也能从唯一检查点继续”的问题。

## 1. 当前已经完成什么

- 4 个用户指定来源已经固定版本并登记；
- 695 个来源单元（Source Unit）已经机械盘点；
- 其中 653 个是待语义审核的检索增强生成（Retrieval-Augmented Generation，RAG）内容单元，42 个已经标为结构、资源或占位单元；
- 653 个语义单元中，161 个已人工审核，492 个待人工审核；
- 用户 PDF《大模型 RAG 经验面》37/37 已人工审核完成；
- 18 个流程节点的三轮外部检索已经完成；
- 当前登记 170 个外部时效/一手来源和 26 条公开工程问题/面试题线索；
- 第四轮只完成 4/18，结果保留为历史检查点，不继续剩余 14 个节点。

机械盘点完成不等于语义审核完成，也不等于标准知识库完成。不得把 695 个标题已入表表述为“所有内容已经人工吸收”。

## 2. 用户已经确定的执行顺序

1. 暂停继续向外搜索；
2. 完成 4 个原始来源的逐单元人工语义审核；
3. 对每个语义单元记录保留、完全重复、部分重叠、跨节点或非检索增强生成内容的判断；
4. 生成可核验的原始来源覆盖报告，证明每个单元均有去向；
5. 使用已登记的 170 个外部来源做事实核验、时效补充和冲突校正，不再无边界扩展来源；
6. 建立去重后的标准知识库（Canonical Knowledge Base）；
7. 构建底层知识图谱（Knowledge Graph）；
8. 生成完整流程前置内容和多张关系图；
9. 按主干节点顺序生成工程问题/面试题，再生成跨节点综合问题；
10. 按统一标准完成详细知识章节。

在第 4 步达到 100% 前，不得批量进入正式正文、思维导图或面试题页面生产。

## 3. 当前唯一工作队列

执行顺序固定为：

1. `xiaolin-ai-learning`：80 个待审语义单元；这是用户当前主要学习来源；
2. `ai-agent-interview-guide`：66 个待审语义单元；
3. `agent-guide`：346 个待审语义单元；
4. `user-rag-experience-pdf`：0 个待审语义单元，37/37 已完成。

查看下一批：

```bash
python scripts/review_queue.py --limit 25
```

查看汇总：

```bash
python scripts/review_queue.py --summary
```

每批以 20～30 个单元为目标，但必须保持一个问题或连续章节的语义完整；不要为了凑数量从中间截断上下文。

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

普通校验通过后创建小型 Git Commit（Git 提交）检查点；拥有远端权限时推送。严格校验在待审单元清零前预期不会通过，不得为了让它变绿而伪造映射。

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

当前用户决策：停止新的外部搜索。前三轮 18/18 和第四轮 4/18 只作为已保存证据；不得继续第四轮剩余 14 个节点。当前唯一任务是按 audits/rag/manual-review-status.json 的实时数量完成待审原始资料语义单元的人工核验与覆盖证明；当前检查点为已审 161、待审 492。

先运行 python scripts/review_queue.py --summary 和 python scripts/review_queue.py --limit 25，按队列从 xiaolin-ai-learning 开始。必须在仓库外按 sources/registry.json 的固定 Commit 检出来源并阅读正文及上下文；不能只根据标题判断。每批审核 20～30 个单元并保持语义边界完整。每个单元必须记录 retain、exact_duplicate、partial_overlap、cross_node 或 non_rag 之一；只有语义、条件和结论都相同才可标为 exact_duplicate。部分重叠、实现差异、反例、版本差异、工程条件和评估方法全部保留。

每批按 docs/LOCAL_AGENT_HANDOFF.md 更新 reviewed 批次文件、catalog、manual-review-status、original-source-coverage 和 work-status；运行 python scripts/validate_repo.py、python scripts/review_queue.py --summary、git diff --check。通过后提交一个小型检查点，有远端权限时推送。不要提前进入正式章节、思维导图或面试题生产。完成一批后直接继续下一批，除非遇到正文无法读取、证据冲突无法判断、工作区存在不明修改或权限阻塞。
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

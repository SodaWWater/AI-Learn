# AI-Learn Agent 工作指南

本文件是所有执行 Agent 的仓库入口。开始工作前必须完整阅读 [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md)。

## 1. 项目目标

本项目把分散的人工智能（Artificial Intelligence，AI）学习资料、工程问题和公开面试题整理成可追踪、可审计、可复习的知识网络。当前试点是检索增强生成（Retrieval-Augmented Generation，RAG）。

底层维护一张有向知识图谱（Directed Knowledge Graph），上层生成完整流程、全局地铁图、节点局部图、工程问题路径、面试题索引和详细知识章节。

## 2. 开工必读顺序

1. [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md)
2. [`audits/rag/work-status.json`](audits/rag/work-status.json)
3. [`docs/LOCAL_AGENT_HANDOFF.md`](docs/LOCAL_AGENT_HANDOFF.md)
4. [`audits/rag/manual-review-status.json`](audits/rag/manual-review-status.json)
5. [`knowledge/rag/TERMINOLOGY.md`](knowledge/rag/TERMINOLOGY.md)
6. [`knowledge/rag/CONTENT_STANDARD.md`](knowledge/rag/CONTENT_STANDARD.md)
7. [`taxonomy/rag-graph-model.json`](taxonomy/rag-graph-model.json)
8. 当前任务涉及的来源登记、审计文件和模板

不要只根据 `README.md`、旧章节或聊天摘要推断当前方向。

当前用户决策优先级：暂停新的外部搜索。已完成的三轮全节点搜索和第四轮 4/18 检查点作为历史证据保留；除非用户再次明确授权，不得继续第四轮剩余搜索。当前唯一主任务是完成首批原始资料的人工语义审核、覆盖证明和保守去重。

## 3. 不可违反的内容规则

- 每次出现专业技术术语，都使用统一双语表达；代码标识符和应用程序编程接口（Application Programming Interface，API）名称保持原样。
- 知识章节只以“概要 → 原理 → 实际开发位置和使用方式 → 具体技术或框架实现”为主体。
- 故障、选型、方案比较和验证主要进入工程问题/面试题（Engineering Problem / Interview Question）页面。
- 一个问题可以关联多个流程节点，一个流程节点可以关联多道问题。
- 只有语义、条件和结论均等价的信息才能合并。
- 实现、补充、反例、冲突、版本差异和业务条件不得作为重复信息删除。
- 不复制许可不明确的外部全文；只保存定位、短转述、自己的整理和来源关系。
- 不虚构为真实公司面试题。没有原始面试来源时标记为工程问题。
- 不生成口诀、遮挡式自测、30 秒或 2 分钟背诵话术。
- 不把旧 `RAG-01` 至 `RAG-03` 第一版当作新章节模板；它们状态为待重写草稿。

## 4. 来源规则

技术结论优先使用官方文档、官方代码仓库和原始论文。公开面经只证明“有人被问过”，不能作为技术结论的唯一证据。二次题库和汇总仓库主要用于发现线索，能够回到原始页面时必须使用原始页面。

每个新来源必须登记：

- 稳定来源标识；
- 链接；
- 固定提交、版本或审核日期；
- 来源类型；
- 许可或发布策略；
- 纳管范围；
- 时效等级。

## 5. 工作包要求

开始一个工作包（Work Package）前，先在 [`audits/rag/work-status.json`](audits/rag/work-status.json) 确认状态和依赖。工作完成后更新：

- 工作项状态；
- 实际产出；
- 验证结果；
- 未解决项；
- 下一工作项。

禁止在同一工作包中无边界地混合大规模来源搜索、分类重构和正式正文批量生成。

## 6. 文件职责

| 位置 | 职责 |
|---|---|
| `sources/` | 来源、版本、许可、检索范围和时效 |
| `taxonomy/` | 主干、节点类型、关系类型和受控分类 |
| `knowledge/` | 标准知识节点及其详细正文 |
| `learning/` | 完整流程和由底层关系生成的学习视图 |
| `interview/` | 工程问题/面试题、来源和跨节点路径 |
| `audits/` | 覆盖、映射、冲突、状态和遗漏检查 |
| `templates/` | 统一内容模板 |
| `scripts/` | 收集、生成和验证脚本 |

## 7. 完成定义

不得用“文档已经写完”作为完成标准。工作项至少需要：

- 文件结构符合模板；
- 专业术语双语一致；
- 所有节点和关系 ID 有效；
- 来源可追踪；
- 独立信息没有因去重丢失；
- 本地链接有效；
- 普通校验通过；
- 工作状态已更新。

严格完成还需要：

```bash
python scripts/validate_repo.py --strict-rag
```

严格校验未通过时，不得声称检索增强生成（Retrieval-Augmented Generation，RAG）全库已经正式完成。

## 8. 常用验证

```bash
python scripts/validate_repo.py
git diff --check
```

提交前检查工作区，不提交构建缓存、下载的受限原文或无关文件。

## 9. 交接模板

Agent 结束工作时提供：

```text
工作项：
状态：
完成内容：
修改文件：
验证结果：
来源与版本：
未验证假设：
剩余风险：
下一工作项：
Git 状态：
```

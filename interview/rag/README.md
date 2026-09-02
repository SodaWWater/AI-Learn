# RAG 公开面试题关联

本目录统一管理工程问题/面试题（Engineering Problem / Interview Question）。问题既是快速学习入口，也是从实际工程现象反向连接多个流程节点、根因、方案、实现和验证方法的核心节点。

主线学习顺序为：完整检索增强生成流程（RAG Workflow）前置内容 → 各主干节点问题 → 跨节点综合问题 → 完整系统设计。这里不生产背诵式答案，也不自行模拟“某公司真实面试题”。

来源分为：

1. `first_person_interview`：发布者本人描述的公开面试经历。
2. `public_question_bank`：公开题库，不能标记为某公司真实面试。
3. `project_interview_exercise`：公开的编程、系统设计或项目型考题。
4. `secondary_index`：二次整理索引，只用于发现线索；可以回链原帖时必须使用原帖。

每条记录必须包含来源类型、原始链接、发布日期或固定 Commit、题目定位、关联知识点 ID 和核验状态。可以做简短转述，不复制整篇面经或第三方答案。

当前已核验的题目与知识映射见 [`public-scenarios.json`](public-scenarios.json)。

公开题目来源的发现范围、检索式和剩余缺口见 [`sources/rag-search-matrix.json`](../../sources/rag-search-matrix.json) 与 [`audits/rag/search-coverage.json`](../../audits/rag/search-coverage.json)。公开题目中的答案不作为技术结论证据，必须回到原始论文（Original Paper）、官方文档（Official Documentation）或官方代码仓库（Official Repository）核验。

新问题页面使用 [`templates/problem-question.md`](../../templates/problem-question.md)，整体规划见 [`docs/PROJECT_PLAN.md`](../../docs/PROJECT_PLAN.md)。

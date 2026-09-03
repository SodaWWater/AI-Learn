# 检索增强生成（Retrieval-Augmented Generation，RAG）可学习骨架版

> 状态：`draft / backbone-v0.1 / 非正式`
> 
> 边界：本目录是便于学习完整主干的前置草稿，不是正式知识章节、完整来源覆盖证明或阶段验收结果。

本骨架只整理仓库已确认的流程架构、现有 191 个规范知识原子（Canonical Knowledge Atom）目录、已审核的小林资料和用户资料。仍有原始来源语义单元（Source Unit）待人工审核，因此不得据此推断全部原始资料已经吸收或所有事实已完成核验。

## 学习入口

1. [一页式总览](01-one-page-overview.md)：先建立离线、在线、反馈和治理四条主干的边界。
2. [关系图集](02-relationship-maps.md)：再观察分支、汇合、依赖、失败传播和跨主干重叠。
3. [18 节点概要学习卡](03-stage-cards.md)：最后按完整链路定位每个节点的输入、输出与工程位置。
4. [首次构建走读](04-first-build-walkthrough.md)：把一个用户问题沿离线、在线、引用和反馈链路走完。

## 已有深读章节

完成骨架三步后，可以按系统运行顺序阅读以下已完成的第一版正文。它们是学习草稿，不代表全部来源已完成审核；阅读时应把结论理解为可根据后续来源证据修订的工程框架。

1. [基础、价值与能力边界](../../../knowledge/rag/chapters/rag-01-foundations.md)：理解检索增强生成（Retrieval-Augmented Generation，RAG）解决什么问题、何时不适合使用，以及它与微调（Fine-tuning）和长上下文（Long Context）的关系。
2. [系统架构与生命周期](../../../knowledge/rag/chapters/rag-02-architecture-lifecycle.md)：理解离线构建、在线检索、生成、评估和发布如何组成可追踪生命周期。
3. [文档解析与数据治理](../../../knowledge/rag/chapters/rag-03-document-parsing-governance.md)：理解文档质量、权限、元数据和版本边界如何决定后续检索质量。

## 非目标

- 不替代 `knowledge/rag/chapters/` 中将来按正式标准重写的知识章节（Knowledge Chapter）；
- 不新增或变更规范知识原子（Canonical Knowledge Atom）、来源映射（Source Mapping）或人工审核状态（Manual Review Status）；
- 不提供公开面试题（Public Interview Question）、自拟面试题或背诵式回答；
- 不声称通过严格检索增强生成（Retrieval-Augmented Generation，RAG）验收。

后续应在原始资料人工语义审核（Manual Semantic Review）、来源覆盖（Source Coverage）、外部证据融合（External Evidence Integration）和有向知识图谱（Directed Knowledge Graph）完成后，依据正式数据替换或吸收本目录内容。

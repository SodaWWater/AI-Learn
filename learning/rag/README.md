# 检索增强生成（Retrieval-Augmented Generation，RAG）学习入口

## 从这里开始

当前建议直接阅读 [可学习骨架版](backbone-v0.1/README.md)。它把离线建库、在线问答、评估和生产治理串成一条完整主线，适合先建立全局模型，再按节点深入。

1. [一页式总览](backbone-v0.1/01-one-page-overview.md)：理解一个检索增强生成（Retrieval-Augmented Generation，RAG）系统从知识源到反馈闭环的完整流动。
2. [关系图集](backbone-v0.1/02-relationship-maps.md)：理解组件依赖、失败传播和优化位置。
3. [18 节点概要学习卡](backbone-v0.1/03-stage-cards.md)：按工程链路逐节点学习输入、输出、决策和常见风险。

该骨架是可阅读、可迭代的学习草稿；它基于已确认的架构与规范知识原子（Canonical Knowledge Atom），但不声称已经吸收全部原始来源，也不替代后续的正式知识章节（Knowledge Chapter）。后续版本会保留清晰的 Git 检查点，因此可以根据学习反馈局部重写，不必推倒整条主线。

## 历史材料

- [审计草图](draft-overview.md)和 13 张原子清单子图：用于核对知识点是否出现，不建议作为首个学习入口。
- [旧学习总览](overview.md)和模块关系图：保留既有工作；其状态见 [`formal-status.json`](formal-status.json)，需要在正式发布前按当前标准重构。

原子目录、来源映射和人工审核状态以 `knowledge/rag/` 与 `audits/rag/` 为准。未完成的来源审核不会阻止草稿学习主线持续改善，但不会被提前表述为正式完成。

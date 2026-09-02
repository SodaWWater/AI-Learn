# 检索增强生成（Retrieval-Augmented Generation，RAG）第二轮 18/18 检查点

日期：2026-09-02

工作项：`WP-P2-002`

状态：`in_progress`

## 本检查点结果

- 第一轮节点检索：18/18；
- 第二轮节点检索：18/18；
- 已登记来源：117；
- 已登记公开工程问题/面试题线索：24；
- 当前覆盖饱和（Coverage Saturated）节点：0/18。

第二轮后半批完成：上下文组装（Context Assembly）、答案生成（Answer Generation）、引用核验（Citation Verification）、评估（Evaluation）、生产治理（Production Governance）和高级检索增强生成（Advanced RAG）。

## 本批新增的重要边界

- 上下文压缩（Context Compression）必须同时评估语义覆盖与实体、数值、否定、日期、引用锚点等细粒度事实保真；
- Structured Output（结构化输出）的 Schema Adherence（模式遵循）不等于 Factual Grounding（事实基于证据）；
- Citation（引用）、Attribution（归因）和 Quotation（引文）需要分开，生成前、生成中和生成后归因具有不同失败模式；
- LLM-as-a-Judge（大语言模型裁判）是需要人工锚点与对抗测试校准的测量工具；
- AI Incident Response（人工智能事件响应）必须覆盖模型、数据、提示、检索轨迹和第三方依赖的证据保全与恢复；
- Modular RAG（模块化检索增强生成）需要统一模块契约，Deep Research（深度研究）需要证据感知停止而非固定轮数。

## 为什么仍未标记覆盖饱和

18 个节点的第二轮都发现了新的知识或问题类型，因此每个节点的连续无新增类型轮数均为 0。下一阶段必须执行独立饱和检索轮次；只有连续两轮没有新增类型，且来源、冲突、九类覆盖和图谱前置项全部满足，才能标记当前版本的覆盖饱和（Coverage Saturated）。

## 下一步

从 18 个节点开始第三轮独立饱和检索，优先核查仍标记为 `partial` 的实现、安全、第一人称公开面经和版本固定项；发现新类型则重置该节点计数，不为追求进度伪造饱和。

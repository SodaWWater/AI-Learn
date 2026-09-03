---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DOCUMENT-PARSING
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 文档解析（Document Parsing）第三轮独立补漏

## 1. 本轮目标与边界

本轮从“单页识别分数高但 RAG 仍失败”的反例出发，专项检查跨页语义连续性、跨页表格、全局 Reading Order（阅读顺序）、Heading Hierarchy（标题层级）、公式、图像和中英文文档的文档级评测，不把 OCR（光学字符识别）字符准确率等同于可用解析质量。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 综合基准 | `site:arxiv.org OmniDocBench diverse PDF parsing comprehensive annotations` | arXiv 原始论文 |
| Q-302 | 跨页基准 | `site:arxiv.org multi-page document parsing cross-page table reading order formula Chinese 2026` | arXiv 原始论文 |
| Q-303 | 失败模式 | `document parsing benchmark cross-page table truncated text hierarchy RAG` | 原始论文与基准说明 |
| Q-304 | 公开题目 | `site:nowcoder.com 企业级 RAG 文档解析 跨页表格 面试` | 牛客公开页面 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `omnidocbench-2025` | 原始论文 | `included` | 提供九类文档来源、端到端与元素级、多属性分层评测，补“文档类型差异” |
| `mpdocbench-parse-2026` | 原始论文 | `included` | 提供中英文、多页、跨页截断文本/表格合并、图像提取和标题树评测 |
| `parsebench-2026` | 原始论文 | `existing_complement` | 第二轮已登记，继续用于 Agent 下游任务；本轮两项基准补文档级结构维度 |
| `nowcoder-enterprise-rag-system-interview-2026` | 第一人称公开面经 | `existing_duplicate_type` | 复杂 PDF、Excel、扫描件解析已登记为 `RAG-SCENE-022` |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 与现有内容关系 |
|---|---|---|---|---|
| `PARSE-K-301` | `evaluation` | Page-level Evaluation（页面级评测）会漏掉跨页文本续接、跨页表格合并和文档级标题树错误；解析验收必须同时包含 Element-level、Page-level 和 Document-level Evaluation（元素级、页面级和文档级评测） | `mpdocbench-parse-2026` | `new` |
| `PARSE-P-301` | `problem_question` | 相邻页面的表格片段若错误合并，会伪造行列；若未合并，会拆断事实和引用锚点，两种错误可能在单页 OCR（光学字符识别）分数中完全不可见 | `mpdocbench-parse-2026` | `new` |
| `PARSE-K-302` | `knowledge` | 文档解析评测应按文档来源、语言、版式属性和元素类别分层，整体平均值不能代表手写、报纸、密集表格或复杂公式子集 | `omnidocbench-2025` | `new` |
| `PARSE-I-301` | `implementation` | 解析中间表示至少应保留 page_id、bounding_box、element_type、reading_order、parent_heading、continuation_relation 和原文坐标，才能支持跨页拼接、结构切分、视觉回链与稳定引用 | 两项基准的标注对象与 RAG 派生链路推导 | `extends` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-022` | 多格式企业文档解析准确率不足时，怎样定位复杂 PDF、Excel、PPT 和扫描件问题？ | 第一人称面经（First-person Interview Report） | 牛客页面系统设计题及“文档解析的坑” | 只能声称发布者自述 | OmniDocBench、MPDocBench-Parse、ParseBench 与解析器官方文档 |
| `RAG-SCENE-011` | 混合文本、表格、图片的 PDF 如何保留版面、页码和模态关系并恢复引用？ | 公开题库（Public Question Bank） | GitHub 题库 Multi-modal RAG Q8 | 否 | 同上 |

本轮题目仍可归并到 `RAG-SCENE-011/022`，但新增“跨页合并是否正确”和“文档级结构是否恢复”两个追问分支，不重复创建 Scenario（场景题）。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Pipeline Parser（流水线解析器）误差累积与端到端 VLM Parser（视觉语言模型解析器）幻觉边界均有论文讨论 |
| 实现（Implementation） | `covered` | 现有 Unstructured、LiteParse 与结构字段要求可形成实现对照 |
| 工程问题（Engineering Problem） | `covered` | 跨页续接、表格合并、阅读顺序、标题树、图像提取、页眉页脚均已分型 |
| 解决方案（Solution） | `partial` | 基准说明了评测和部分显式拼接路线，但不同解析器的跨页实现仍需官方代码级验证 |
| 评估（Evaluation） | `covered` | 两项新基准与 ParseBench 形成元素、页面、文档和下游任务多层评测 |
| 公开面试题（Public Interview Question） | `covered` | `RAG-SCENE-011/022` 可定位；本轮无新题型 |
| 时效（Freshness） | `covered` | CVPR 2025 与 2026-05 新基准均在 2026-09-03 复核 |
| 安全或治理（Security or Governance） | `partial` | 图片 OCR、临时文件和 VLM API 的敏感数据边界需与数据治理联合验证 |
| 跨节点关系（Cross-stage Relation） | `covered` | 错误会传播到 Chunking（文本切分）、Retrieval（检索）、Citation（引用）和 Evaluation（评估） |

## 7. 冲突、版本与未验证假设

- OmniDocBench 主要补多样文档和细粒度属性，MPDocBench-Parse 主要补多页连续性；二者不是替代关系。
- MPDocBench-Parse 为 2026 年预印本 v1；其中模型排名和具体数值可能随版本变化，正式内容应优先保留任务定义和失败类型，并固定版本后再引用数值。
- “显式跨页拼接优于端到端解析”不是普遍结论；论文只显示部分当前系统在特定基准上的差异，需按目标语料复测。
- 中间表示字段是从基准标注和下游需求推导的工程契约，不表示所有框架已原生支持这些字段。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 是 |
| 九类覆盖是否全部完成 | 否；解决方案和安全仍为 `partial` |
| 一手资料缺口检查是否完成 | 是 |
| 公开面试题专项搜索是否完成 | 是 |
| 本轮新增知识/实现/评估类型数 | 3 |
| 本轮新增问题类型数 | 1 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete`，不得标记 `coverage_saturated` |

## 9. 下一轮动作

- 以解析器官方仓库和可复现实验补跨页拼接的具体实现与回退策略；
- 建立中文双栏、竖排、跨页表格、公式、代码、印章和图表的目标语料分层清单；
- 检查解析坐标怎样经过 Chunking（文本切分）仍保持 Citation Anchor（引用锚点）稳定；
- 用新的查询族继续搜索公开工程题；若下一轮无新增，连续无新增计数才变为 1。

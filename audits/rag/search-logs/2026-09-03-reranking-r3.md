---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RERANKING
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 重排序（Reranking）第三轮独立补漏

## 1. 本轮目标与边界

本轮补查外部重排序接口（External Rerank API）的真实请求数据、自动截断、过载故障和数据处理承诺，并核验过滤时机如何影响重排序候选供给。重排序器（Reranker）只能评价收到的候选；候选文本被截断、过滤后不足或调用失败都不能归因成单纯的“模型效果差”。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 请求边界（Request Boundary） | `Cohere Rerank v2 documents max_tokens_per_doc truncation priority errors` | Cohere 官方 API 文档（Official API Documentation） |
| Q-302 | 数据承诺（Data Commitment） | `Cohere enterprise data commitments SaaS private deployment ZDR retention training` | Cohere 官方政策（Official Policy） |
| Q-303 | 候选供给（Candidate Supply） | `Azure semantic ranker postFilter strictPostFilter candidate count hybrid search` | Microsoft 官方文档（Official Documentation） |
| Q-304 | 分层评测（Stratified Evaluation） | `CrossEncoder reranking query type document length candidate quality hardware benchmark` | 官方框架文档与原始论文（Official Framework Documentation and Original Papers） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com RAG Rerank API 数据 安全 截断 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `cohere-rerank-api-v2-2026` | 官方 API 文档（Official API Documentation） | `included` | 明确请求包含查询和文档文本、文档数量建议、自动截断、每文档令牌上限、优先级和错误状态 |
| `cohere-enterprise-data-commitments-2025` | 官方政策（Official Policy） | `included` | 明确 SaaS（软件即服务）、私有部署（Private Deployment）、零数据保留（Zero Data Retention，ZDR）、企业与试用范围不同 |
| `azure-hybrid-query-docs-2026` | 官方文档（Official Documentation） | `included` | 补过滤与候选窗口共同决定语义重排序器（Semantic Ranker）输入的实现证据 |
| `cohere-rerank-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 保留教程层实现入口；新 API 参考和数据政策不是它的完全重复项 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `RRK-K-301` | `knowledge` | 外部重排序接口（External Rerank API）接收的是查询与原始文档文本，而非只接收文档标识；调用本身构成新的数据处理边界（Data-processing Boundary） | `cohere-rerank-api-v2-2026` | `new` |
| `RRK-P-301` | `problem_question` | 自动文档截断（Automatic Document Truncation）可能删去位于尾部的关键证据，表面表现为重排序错误，实际是输入长度契约不匹配 | `cohere-rerank-api-v2-2026` | `new` |
| `RRK-P-302` | `problem_question` | 后过滤（Post-filtering）和小候选窗口可能使重排序器输入不足；提高重排序模型能力无法恢复未进入候选集的证据 | `azure-hybrid-query-docs-2026` | `new` |
| `RRK-P-303` | `problem_question` | 429、503、504、优先级调度和超时会造成尾延迟（Tail Latency）或部分失败；若降级策略未记录，线上排序和离线评测不可对齐 | `cohere-rerank-api-v2-2026` | `new` |
| `RRK-P-304` | `problem_question` | 把相关性分数（Relevance Score）直接当概率并设置通用阈值，会忽略模型、语料、查询类型和候选分布造成的校准差异 | API 文档；既有校准来源 | `new` |
| `RRK-S-301` | `solution` | 调用前检查文档长度和敏感级别，按需分窗或本地重排；显式设置候选上限、超时、重试、熔断与降级，并把部署模式和数据保留条款固定到服务配置 | 两项 Cohere 官方来源 | `new` |
| `RRK-E-301` | `evaluation` | 回放按查询类型、文档长度、候选质量、候选数、硬件和部署模式分层，对比 Cross-Encoder（交叉编码器）、LLM Reranker（大语言模型重排序器）、MMR（最大边际相关性）和 Dynamic Gate（动态门控），同时报告排序、答案支持、延迟、费用和数据出域量 | 新增与既有来源 | `extends` |

## 5. 公开面试题来源核验

未新增题目，继续挂接 `RAG-SCENE-019`。没有找到可读取且明确讨论外部重排序接口（External Rerank API）数据治理的第一人称面经，因此公开面试题（Public Interview Question）仍是部分覆盖（Partial Coverage）。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Cross-Encoder、Listwise、MMR、生成效用和动态门控已覆盖 |
| 实现（Implementation） | `covered` | 本地框架、ONNX（Open Neural Network Exchange）、OpenVINO（Open Visual Inference and Neural Network Optimization）、外部 API 和候选窗口均有入口 |
| 工程问题（Engineering Problem） | `covered` | 截断、输入不足、过载、领域迁移、假负例和分数误读已登记 |
| 解决方案（Solution） | `covered` | 分窗、本地或外部选择、服务保护、降级和配置固化已覆盖 |
| 评估（Evaluation） | `covered` | 质量、答案支持、性能、费用和数据出域分层已定义 |
| 公开面试题（Public Interview Question） | `partial` | 有公开工程场景，仍缺独立可读第一人称重排面经 |
| 时效（Freshness） | `covered` | 当前 API、2025 数据政策、当前产品过滤行为和既有论文兼顾 |
| 安全或治理（Security or Governance） | `covered` | 请求内容、部署方式、保留、训练选择和试用范围均已登记 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接检索候选、融合窗口、上下文长度、答案支持、评估与生产治理 |

## 7. 冲突、版本与未验证假设

- Cohere 数据承诺（Cohere Data Commitments）按 SaaS（软件即服务）、私有部署（Private Deployment）、合作方托管、企业合同、试用密钥和零数据保留（Zero Data Retention，ZDR）区分；不能写成“Cohere 一律不保存数据”。
- API 文档中的模型示例可能随版本变化；正式材料不应把示例模型名称写成全局默认值。
- 自动截断（Automatic Truncation）的影响取决于证据位置和文档序列化；结构化数据转换成 YAML（YAML Ain't Markup Language）也需要单独验证字段顺序与长度。
- 相关性分数（Relevance Score）不是跨模型可比概率；只有目标流量上的校准实验才能支持阈值策略。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 4 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

制作固定候选快照和长度分层，分别验证本地 Cross-Encoder（交叉编码器）与外部 Rerank API（重排序接口）的截断、故障、降级和数据边界；继续补第一人称公开面经，但不以产品文档冒充题目来源。

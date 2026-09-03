---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RESULT-FUSION
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 结果融合（Result Fusion）第三轮独立补漏

## 1. 本轮目标与边界

本轮验证候选窗口、分支权重、过滤域和框架具体实现如何改变融合语义。结果融合（Result Fusion）不是抽象地“把列表合在一起”：倒数排名融合（Reciprocal Rank Fusion，RRF）、相对分数融合（Relative Score Fusion）、距离分数融合（Distance-based Score Fusion）和简单融合（Simple Fusion）对重复项、分数尺度和缺失分支有不同契约。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | RRF 窗口（RRF Window） | `Elasticsearch RRF retriever rank_window_size rank_constant weights filter` | Elasticsearch 官方文档（Official Documentation） |
| Q-302 | Azure 候选集（Azure Candidate Set） | `Azure hybrid query RRF maxTextRecallSize count facets candidate window` | Microsoft 官方文档（Official Documentation） |
| Q-303 | 框架语义（Framework Semantics） | `LlamaIndex QueryFusionRetriever simple relative score distance based RRF source` | 官方仓库源码（Official Repository Source） |
| Q-304 | 权限域（Authorization Domain） | `OWASP RAG retrieval access control every chunk cross tenant test` | OWASP 官方安全指南（Official Security Guidance） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com RAG RRF 融合 候选窗口 权限 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `elasticsearch-rrf-retriever-docs-2026` | 官方文档（Official Documentation） | `included` | 补齐子检索器权重、`rank_constant`、`rank_window_size` 和全局过滤器的当前接口契约 |
| `azure-hybrid-query-docs-2026` | 官方文档（Official Documentation） | `included` | 补齐文本候选预算、向量候选预算、最终 `top` 以及计数和分面结果与实际融合窗口的差异 |
| `llamaindex-query-fusion-retriever-2026` | 官方仓库源码（Official Repository Source） | `included_existing_extended` | 固定提交中的实现显示四种融合模式、原始查询分支、异步笛卡尔执行和重复节点处理 |
| `owasp-rag-security-cheat-sheet-2026` | 官方安全指南（Official Security Guidance） | `included` | 支持融合前候选必须处于已授权域且可追溯 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `FUS-K-301` | `knowledge` | 候选窗口是融合算法输入语义的一部分；进入 RRF（倒数排名融合）前已被截断的文档不会因增大最终 `top` 而恢复 | 两项新增产品文档 | `new` |
| `FUS-K-302` | `knowledge` | 固定版本的 QueryFusionRetriever（查询融合检索器）中，简单融合（Simple Fusion）对重复节点保留较高分数，相对分数融合（Relative Score Fusion）累加归一化贡献，RRF（倒数排名融合）累加排名贡献；它们表达不同的证据聚合假设 | `llamaindex-query-fusion-retriever-2026` | `new` |
| `FUS-P-301` | `problem_question` | 加权 RRF（Weighted Reciprocal Rank Fusion）的权重只是策略系数，不是通道可信概率；错误权重会在每次查询中系统性放大某一路偏差 | `elasticsearch-rrf-retriever-docs-2026` | `new` |
| `FUS-P-302` | `problem_question` | 混合查询返回的 `count` 或分面（Facet）统计可能覆盖未进入 RRF（倒数排名融合）窗口的文本命中，若把它们当成“实际融合候选数”会误诊召回和过滤问题 | `azure-hybrid-query-docs-2026` | `new` |
| `FUS-P-303` | `problem_question` | 分支超时或返回空列表时，继续按原权重融合、重新归一化还是整体失败会得到不同排名；没有显式部分结果策略（Partial-result Policy）时，线上行为不可复现 | 新增产品文档；既有可观测性来源 | `new` |
| `FUS-S-301` | `solution` | 先按同一授权域裁剪各路候选，再固定每路窗口、算法、权重、重复键和缺失分支策略；追踪每个候选从分支排名到融合排名的贡献 | 新增与既有来源 | `extends` |
| `FUS-E-301` | `evaluation` | 在同一候选快照上复现 RRF（倒数排名融合）、加权 RRF（Weighted Reciprocal Rank Fusion）、CombSUM（分数组合求和）、CombMNZ（非零计数组合）和线性融合（Linear Fusion），并加入父子分块、版本冲突、权限域和分支失败分层 | 新增与既有来源 | `new` |

## 5. 公开面试题来源核验

未新增题目，仍挂接 `RAG-SCENE-018`。没有找到可读取且可证明题目原貌的独立第一人称融合面经，因此“公开面试题（Public Interview Question）”继续保持部分覆盖（Partial Coverage），不拿官方产品示例替代面经。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 排名融合、分数融合、归一化和候选窗口语义已覆盖 |
| 实现（Implementation） | `covered` | Azure AI Search（Azure AI Search）、Elasticsearch（Elasticsearch）和 LlamaIndex（LlamaIndex）固定接口或源码已登记 |
| 工程问题（Engineering Problem） | `covered` | 截断、权重、重复、权限域、计数错觉和分支失败已登记 |
| 解决方案（Solution） | `covered` | 授权前置、固定窗口、结构化去重、贡献追踪和部分结果策略已覆盖 |
| 评估（Evaluation） | `covered` | 五类融合复现与四类工程分层已定义 |
| 公开面试题（Public Interview Question） | `partial` | 有公开工程场景，仍缺独立可读第一人称融合面经 |
| 时效（Freshness） | `covered` | 经典原论文、当前产品接口和固定框架源码兼顾 |
| 安全或治理（Security or Governance） | `covered` | 候选在融合前必须完成授权裁剪，且日志不得泄露跨域身份 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接改写分支、检索窗口、重排输入、上下文去重和权限治理 |

## 7. 冲突、版本与未验证假设

- Elasticsearch RRF（Elasticsearch Reciprocal Rank Fusion）当前默认参数是产品版本事实，不是所有 RRF（倒数排名融合）实现的理论默认值。
- LlamaIndex QueryFusionRetriever（LlamaIndex 查询融合检索器）的行为来自固定提交；升级框架前必须做源码差异和回归检查。
- 分支权重（Branch Weight）不能直接解释为概率、置信度或证据可靠性；只有经过目标流量校准和验证后才可赋予这些含义。
- 高通道重合率（Channel Overlap）可能是稳健一致，也可能是重复语料或同源偏差；不能只凭重合率判断融合有效。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

实现统一候选快照和逐候选贡献日志，运行五类融合的可重复对照；继续补第一人称公开面经，但在找到前不新增题目。

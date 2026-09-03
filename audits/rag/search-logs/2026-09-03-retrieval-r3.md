---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-RETRIEVAL
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 检索（Retrieval）第三轮独立补漏

## 1. 本轮目标与边界

本轮聚焦混合检索（Hybrid Retrieval）的候选预算、过滤时机和不可信语料边界。检索（Retrieval）决定哪些候选能够进入后续结果融合（Result Fusion）与重排序（Reranking）；因此 `k`、文本召回窗口、过滤模式、访问控制列表（Access Control List，ACL）和来源完整性都会改变“可见候选集”，不能只看最终 `top` 数量。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 候选预算（Candidate Budget） | `Azure hybrid search k maxTextRecallSize top semantic ranker 50 candidates` | Microsoft 官方文档（Official Documentation） |
| Q-302 | 过滤时机（Filter Timing） | `Azure vector filterOverride preFilter postFilter strictPostFilter security trimming` | Microsoft 官方文档（Official Documentation） |
| Q-303 | 检索安全（Retrieval Security） | `OWASP RAG security retrieval-time access control poisoned document stale permission cache leakage` | OWASP 官方安全指南（Official Security Guidance） |
| Q-304 | 间接提示注入（Indirect Prompt Injection） | `indirect prompt injection retrieved documents real-world RAG paper` | arXiv 原始论文（Original Paper） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com RAG 混合检索 过滤 权限 召回 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `azure-hybrid-query-docs-2026` | 官方文档（Official Documentation） | `included` | 补齐向量候选数 `k`、文本候选窗口 `maxTextRecallSize`、最终数量 `top`、过滤模式和语义重排序器（Semantic Ranker）输入窗口的联动 |
| `owasp-rag-security-cheat-sheet-2026` | 官方安全指南（Official Security Guidance） | `included` | 补齐逐分块访问控制（Per-chunk Access Control）、文档哈希（Document Hash）、权限撤销、投毒文档和缓存泄露测试 |
| `indirect-prompt-injection-wild-2026` | 原始论文（Original Paper） | `included_existing_extended` | 原来源阶段映射补入检索（Retrieval），用于证明检索内容不能因查询已清洗而被视为可信 |
| `qdrant-ann-recall-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 已覆盖近似最近邻召回率（Approximate Nearest Neighbor Recall）与精确检索（Exact Search）对照 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `RET-K-301` | `knowledge` | 向量候选数 `k`、文本候选窗口 `maxTextRecallSize` 和最终返回数 `top` 是不同阶段的预算；过早截断的候选无法由后续融合或重排序恢复 | `azure-hybrid-query-docs-2026` | `new` |
| `RET-P-301` | `problem_question` | `filterOverride` 会完全覆盖目标向量查询的全局过滤条件；若没有显式重复安全裁剪（Security Trimming），语义正确的查询可能绕过访问控制列表（Access Control List，ACL） | `azure-hybrid-query-docs-2026` | `new` |
| `RET-P-302` | `problem_question` | 后过滤（Post-filtering）或严格后过滤（Strict Post-filtering）在小候选窗口下会让语义重排序器（Semantic Ranker）输入不足，表现为重排或生成退化，根因却在检索过滤顺序 | `azure-hybrid-query-docs-2026` | `new` |
| `RET-P-303` | `problem_question` | 只清洗用户查询不能消除被检索文档中的间接提示注入（Indirect Prompt Injection）；检索结果仍是外部不可信数据（Untrusted External Data） | `indirect-prompt-injection-wild-2026`; `owasp-rag-security-cheat-sheet-2026` | `new` |
| `RET-S-301` | `solution` | 检索时同时验证文档哈希（Document Hash）、来源、逐分块权限和撤销状态；权限校验失败返回空候选并失败关闭（Fail Closed），不得扩大检索域 | `owasp-rag-security-cheat-sheet-2026` | `new` |
| `RET-E-301` | `evaluation` | 检索安全回放集覆盖跨租户、已撤销权限、陈旧缓存、投毒文档、来源哈希不符和过滤覆盖；质量回放同时分层记录 `k`、文本候选窗口、过滤前后候选数和下游有效输入数 | 两项新增官方来源 | `new` |

## 5. 公开面试题来源核验

未新增题目。新增工程类型可挂接 `RAG-SCENE-017`、`RAG-SCENE-018`、`RAG-SCENE-022` 和 `RAG-SCENE-023`；本轮没有把产品文档或安全清单包装成面试题来源。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | Dense、Sparse、Hybrid、Iterative、候选预算和过滤顺序已覆盖 |
| 实现（Implementation） | `covered` | Azure AI Search（Azure AI Search）、Qdrant（Qdrant）和现有框架来源可落地 |
| 工程问题（Engineering Problem） | `covered` | 零召回、候选不足、权限绕过、陈旧缓存、投毒和间接提示注入均已登记 |
| 解决方案（Solution） | `covered` | 预算分层、权限前置、完整性校验和失败关闭（Fail Closed）已覆盖 |
| 评估（Evaluation） | `covered` | 增加候选流量计数和检索安全矩阵 |
| 公开面试题（Public Interview Question） | `covered` | 只关联已有可回链问题，不新增无来源题 |
| 时效（Freshness） | `covered` | 当前产品文档、当前安全指南和 2026 原始研究兼顾 |
| 安全或治理（Security or Governance） | `covered` | 逐分块授权、哈希、权限撤销、注入和缓存泄露已覆盖 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接过滤、融合、重排、上下文、生成和生产治理 |

## 7. 冲突、版本与未验证假设

- `maxTextRecallSize` 和部分过滤能力属于预览接口（Preview API）；正式实现必须固定 API 版本（API Version），不能把预览参数写成所有版本的稳定能力。
- 预过滤（Pre-filtering）通常更适合权限裁剪，但具体召回、延迟和分片行为依赖引擎；安全过滤不可因性能实验而后移到会泄露候选身份的阶段。
- 语义重排序器（Semantic Ranker）当前候选输入上限是产品契约，不是通用检索理论；更换产品或版本必须重新核验。
- 检索到恶意文本不等于攻击必然成功；本轮结论是“不可自动信任”，实际风险仍依赖上下文组装、提示层级、工具权限和输出处理。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

把 Dense Retrieval（稠密检索）、Sparse Retrieval（稀疏检索）、Hybrid Retrieval（混合检索）和 Iterative Retrieval（迭代检索）放入同一分层回放；除质量和延迟外，记录每一步授权域、候选预算和来源完整性结果。

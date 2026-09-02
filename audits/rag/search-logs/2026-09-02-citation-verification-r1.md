---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-CITATION-VERIFICATION
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：引用与验证（Citation and Verification）第一轮

## 1. 本轮目标与边界

核查引用存在性、声明—证据支持关系、引用完整性、粒度、冲突与拒答。引用链接存在不代表支持对应声明，必须拆开验证。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 引用基准 | `site:arxiv.org ALCE citation evaluation language models citations RAG` | ALCE 原始论文 |
| Q-002 | 细粒度诊断 | `site:arxiv.org RAGChecker claim-level evaluation` | RAGChecker 原始论文 |
| Q-003 | 幻觉标注 | `site:arxiv.org RAGTruth hallucination corpus` | RAGTruth 原始论文 |
| Q-004 | 风险 | `site:nist.gov generative AI content provenance profile` | NIST 官方资料 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `alce-citation-evaluation-2023` | 原始论文 | `included` | Citation Correctness、Completeness、Style |
| `ragchecker-2024` | 原始论文 | `included` | Claim-level 检索与生成诊断 |
| `ragtruth-2024` | 原始论文 | `included` | 细粒度无依据内容 |
| `nist-genai-profile-2024` | 官方文档 | `included` | Provenance 与风险治理，不作为自动判分算法 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `CIT-K-001` | `knowledge` | Citation Validity、Correctness 与 Completeness 是不同检查 | `new` |
| `CIT-P-001` | `problem_question` | 一个引用只支持句子中的部分声明 | `new` |
| `CIT-P-002` | `problem_question` | 多个声明共用粗粒度引用导致无法定位证据 | `new` |
| `CIT-P-003` | `problem_question` | 来源冲突和过期信息未显式表达 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 短转述 | 来源类型 | 是否真实面试 | 技术核验 |
|---|---|---|---|---|
| `RAG-SCENE-002` | 法律答案怎样保留可靠引用 | 第一人称面经 | 发布者自述 | ALCE、RAGChecker |
| `RAG-SCENE-011` | 多模态 PDF 怎样恢复页码和引用 | 公开题库 | 否 | ALCE、解析官方文档 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理 | `covered` | 声明—证据对齐与三类引用指标 |
| 实现 | `partial` | NLI/LLM Verifier 与页码锚点待补 |
| 工程问题 | `covered` | 假引用、错支持、粒度、冲突 |
| 解决方案 | `partial` | 原子声明分解和多模型验证待补 |
| 评估 | `covered` | ALCE 与 Claim-level 指标 |
| 公开面试题 | `covered` | 第一人称和题库场景 |
| 时效 | `covered` | 2023–2024 基准 |
| 安全或治理 | `partial` | 来源签名和篡改检测待补 |
| 跨节点关系 | `covered` | 上下文、生成、评估、治理 |

## 7. 冲突、版本与未验证假设

- 不把 URL 可访问性当作证据支持；
- LLM Verifier 仍可能有偏差，关键声明需确定性检查或人工抽检；
- 下一轮补引用锚点、NLI、冲突分组和来源签名。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补 Claim Segmentation、NLI/LLM Verifier、引用锚点、冲突表达和来源完整性验证。

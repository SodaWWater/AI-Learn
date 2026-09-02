---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-CITATION-VERIFICATION
round: 2
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 引用核验（Citation Verification）第二轮独立补漏

## 1. 本轮目标与边界

专项补查原子声明分解（Atomic Claim Segmentation）、自然语言推断（Natural Language Inference，NLI）、大语言模型验证器（LLM Verifier）、证据粒度（Evidence Granularity）、生成前/中/后归因（Pre/In/Post-generation Attribution）、来源完整性（Source Integrity）和冲突分组。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-201 | 归因综述（Attribution Survey） | `Attribution Citation Quotation evidence based text generation ACL 2026` | ACL Anthology 综述（Survey） |
| Q-202 | 声明核验（Claim Verification） | `claim verification LLM RAG survey ACL 2026` | ACL Anthology 综述（Survey） |
| Q-203 | 引用锚点（Citation Anchor） | `claim level citation evidence granularity RAG` | 原始研究检索（Primary Research Search） |
| Q-204 | 来源完整性（Source Integrity） | `NIST AI incident evidence preservation source integrity` | NIST 官方指导（Official Guidance） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `evidence-based-generation-survey-2026` | 综述（Survey） | `included` | 统一引用、归因和引文的术语，补归因时机、模态、粒度、风格和可见性 |
| `alce-2023` | 原始论文（Original Paper） | `included_existing` | 已覆盖引用正确性、完整性和长文本生成基准 |
| `ragtruth-2024` | 原始论文（Original Paper） | `included_existing` | 已覆盖声明级幻觉与证据核验 |
| `nist-ai-incident-response-2026` | 官方指导（Official Guidance） | `cross_stage` | 来源篡改或证据丢失时用于保全与响应，不替代语义支持判定 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `CIT-K-201` | `knowledge` | Citation（引用）、Attribution（归因）和 Quotation（引文）是不同机制；可追溯 URL 不等于声明获得语义支持 | `evidence-based-generation-survey-2026` | `new` |
| `CIT-K-202` | `knowledge` | 归因可发生在检索后、生成中、生成后或直接使用用户提供证据，不同位置的失败模式不同 | `evidence-based-generation-survey-2026` | `new` |
| `CIT-P-201` | `problem_question` | 文档级引用可能指向包含相关主题但不支持具体声明的长文档，形成粒度错配 | `evidence-based-generation-survey-2026` | `new` |
| `CIT-P-202` | `problem_question` | 生成后为已有声明搜索来源可能找到“看似相关”的事后引用，却掩盖答案最初并非由该证据支持 | 新增与既有来源 | `new` |
| `CIT-P-203` | `problem_question` | 原页面更新、删除或被篡改时，单独保存 URL 无法证明核验时看到的内容版本 | NIST 指导；既有数据治理来源 | `new` |
| `CIT-S-201` | `solution` | 引用记录至少绑定原子声明、证据跨度、文档版本/内容摘要、抓取时间、权限和支持/反驳/不足状态 | 新增与既有来源 | `extends` |
| `CIT-E-201` | `evaluation` | 分别统计引用可访问性、声明级精确度、完整性、粒度匹配、版本可复现性和验证器一致性 | 新增与既有评估来源 | `new` |

## 5. 公开面试题来源核验

现有 `RAG-SCENE-002`、`RAG-SCENE-006`、`RAG-SCENE-021` 和 `RAG-SCENE-024` 已覆盖页码恢复、引用评估、失败归因和冲突来源；本轮没有虚构额外题目。

## 6. 九类覆盖检查

原理、工程问题、解决方案、评估、公开题目、时效和跨节点关系已覆盖；实现层仍需固定 NLI Verifier（自然语言推断验证器）与 LLM Verifier（大语言模型验证器）的具体模型版本，来源签名和内容寻址需在治理轮次继续落地。

## 7. 冲突与边界

- NLI Entailment（自然语言推断蕴含）只能说明模型判定，不能作为绝对真值。
- 细粒度证据提高核验性，但切得过细可能丢失限定上下文。
- 内容哈希能检测内容变化，不能单独证明发布者身份、来源权威度或事实真实性。

## 8. 饱和判定

本轮新增知识类型 2、问题类型 3；连续无新增类型轮数为 0，结论为 `round_complete`，不得标记饱和。

## 9. 下一轮动作

固定声明分解器、NLI Verifier（自然语言推断验证器）和 LLM Verifier（大语言模型验证器）；建立支持、反驳、部分支持、粒度错配、页面版本变化和多模态锚点回归集。

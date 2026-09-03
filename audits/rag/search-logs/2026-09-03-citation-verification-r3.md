---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-CITATION-VERIFICATION
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 引用核验（Citation Verification）第三轮独立补漏

## 1. 本轮目标与边界

本轮把“引用指针可解析”“引用片段支持声明”“声明覆盖完整”“来源真实可信”拆成独立门禁，并核对中文与多字节文本的跨度协议。引用核验（Citation Verification）不能只确认 URL 或页码存在，也不能把提供商返回的支持分数（Support Score）当作事实真值概率。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 原生引用（Native Citation） | `Claude citations page character content block location exact passages official` | Anthropic 官方文档（Official Documentation） |
| Q-302 | 声明核验（Claim Grounding） | `Google check grounding claim-level score UTF-8 byte positions facts citation threshold` | Google Cloud 官方文档（Official Documentation） |
| Q-303 | 查询无关评估（Query-agnostic Evaluation） | `Q-CARE atomic claim verifiability query coverage RAG 2026` | arXiv 论文与官方仓库（Paper and Official Repository） |
| Q-304 | 来源完整性（Source Integrity） | `OWASP RAG signed source attribution document hash verification endpoint` | OWASP 官方安全指南（Official Security Guidance） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com RAG 引用 核验 页码 幻觉 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `anthropic-citations-docs-2026` | 官方文档（Official Documentation） | `included` | 补 PDF 页范围、纯文本字符范围、自定义内容块范围、流式引用和自动/自定义切分边界 |
| `google-check-grounding-docs-2026` | 官方文档（Official Documentation） | `included` | 补句子级声明、全部蕴含要求、声明级分数、引用阈值和 UTF-8 字节范围 |
| `qcare-rag-evaluation-2026` | 原始论文（Original Paper） | `included` | 补子查询覆盖和原子声明可核验性（Atomic-claim Verifiability）的统一诊断 |
| `qcare-official-repository-2026` | 官方仓库（Official Repository） | `included` | 补可执行分解、对齐判断和逐样本中间轨迹 |
| `owasp-rag-security-cheat-sheet-2026` | 官方安全指南（Official Security Guidance） | `included_existing` | 补签名归因、文档哈希和独立验证入口，不重复登记 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `CIT-K-301` | `knowledge` | 引用至少有四层正确性：指针有效（Pointer Validity）、语义支持（Semantic Support）、声明覆盖（Claim Coverage）和来源真实性/权威性（Source Authenticity or Authority）；上层通过不推出下层通过 | 新增官方文档与 OWASP 来源 | `new` |
| `CIT-K-302` | `knowledge` | 引用跨度协议随输入类型变化：PDF 文档（PDF Document）可返回页范围，纯文本（Plain Text）可返回字符范围，自定义内容（Custom Content）可返回内容块范围；系统必须保留类型和索引基准 | `anthropic-citations-docs-2026` | `new` |
| `CIT-P-301` | `problem_question` | Google Grounding（Google 依据核验）返回的声明起止位置是 UTF-8 字节偏移（UTF-8 Byte Offset），中文界面若按字符索引切片会高亮错位或截断多字节字符 | `google-check-grounding-docs-2026` | `new` |
| `CIT-P-302` | `problem_question` | 把整句视为一个声明时，只要并列事实中一个子事实错误，整句都不算完全支持；若直接展示单一结果，用户看不出哪个子声明失败 | `google-check-grounding-docs-2026` | `new` |
| `CIT-P-303` | `problem_question` | 原生引用保证指向请求中提供的文档位置，不证明该来源未被篡改、内容真实或足以回答原始查询 | `anthropic-citations-docs-2026`; `owasp-rag-security-cheat-sheet-2026` | `new` |
| `CIT-P-304` | `problem_question` | 引用阈值（Citation Threshold）提高会得到更少但更强的引用，降低会得到更多但更弱的引用；未在目标语料校准时，固定默认阈值会在完整性和精确度之间产生隐性偏置 | `google-check-grounding-docs-2026` | `new` |
| `CIT-S-301` | `solution` | 将答案分解为原子声明，为每个声明保存支持、反驳和不足证据；引用记录绑定内容哈希、来源版本、权限、输入类型、偏移单位和原始跨度，前端按协议渲染 | 新增与既有来源 | `extends` |
| `CIT-E-301` | `evaluation` | 分别测指针可解析率、跨度渲染准确率、声明支持精确度/召回率、引用完整性、来源版本复现、阈值校准和人工验证器一致性；中文、表格、PDF 和流式输出必须分层 | 新增与既有来源 | `new` |

## 5. 公开面试题来源核验

未新增题目编号。最新公开题库仍把“可追溯”和“减少幻觉”作为 RAG（检索增强生成）优势，但没有提供独立于 `RAG-SCENE-002`、`RAG-SCENE-006`、`RAG-SCENE-021`、`RAG-SCENE-024` 的引用核验场景；本轮补充实现陷阱和验证协议。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 指针、支持、覆盖、真实性和原子声明已分层 |
| 实现（Implementation） | `covered` | 两个当前产品 API、可执行 Q-CARE（查询覆盖与声明可核验）和签名归因入口已登记 |
| 工程问题（Engineering Problem） | `covered` | 多字节偏移、声明粒度、阈值、来源篡改和能力互斥已登记 |
| 解决方案（Solution） | `covered` | 原子声明、不可变证据、版本哈希、偏移协议和前端渲染已覆盖 |
| 评估（Evaluation） | `covered` | 六类独立指标与中文/多模态分层已定义 |
| 公开面试题（Public Interview Question） | `covered` | 现有题目可回链，未虚构新题 |
| 时效（Freshness） | `covered` | 当前产品接口、2026-08 最新论文与固定仓库提交均登记 |
| 安全或治理（Security or Governance） | `covered` | 签名、哈希、权限和来源验证已覆盖 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接解析、压缩、生成、评估和生产治理 |

## 7. 冲突、版本与未验证假设

- Google Grounding Support Score（Google 依据支持分数）“近似声明支持比例”是产品说明，不是跨领域校准概率；阈值必须在目标数据上验证。
- Anthropic Native Citations（Anthropic 原生引用）支持文本引用，不支持图像引用；扫描 PDF 若没有可提取文本，不能假设获得可靠页级引用。
- Q-CARE（查询覆盖与声明可核验）是无参考答案评估（Reference-free Evaluation），但依然依赖分解器和对齐判断器；“无参考”不等于“无模型误差”。
- 内容哈希（Content Hash）只能证明内容是否变化，不能独立证明发布者身份、来源权威或事实真伪。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 4 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

实现统一引用跨度（Citation Span）数据结构，编写中文 UTF-8 字节—字符映射、PDF 页码、自定义块和流式增量测试；用人工锚点集校准声明分解器与支持判断器。

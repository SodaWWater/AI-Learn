---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-ANSWER-GENERATION
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 答案生成（Answer Generation）第三轮独立补漏

## 1. 本轮目标与边界

本轮聚焦非理想检索条件下的联合指令遵循（Joint Instruction Adherence）、冲突状态、引用与结构化输出兼容性，以及生成后硬校验。答案生成器（Answer Generator）必须区分“生成了合法结构”“满足每个约束”“全部约束同时满足”“声明被证据支持”四个不同事件。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 企业鲁棒性（Enterprise Robustness） | `EnterpriseRAG instruction adherence retrieval noise knowledge gaps factual conflicts` | arXiv 原始论文（Original Paper） |
| Q-302 | 冲突生成（Conflict-aware Generation） | `ConflictRAG factual temporal opinion conflict annotation generation` | arXiv 原始论文（Original Paper） |
| Q-303 | 引用兼容性（Citation Compatibility） | `Claude citations structured outputs incompatible official documentation` | Anthropic 官方文档（Official Documentation） |
| Q-304 | 输出校验（Output Validation） | `OWASP RAG output validation structured schema policy enforcement` | OWASP 官方安全指南（Official Security Guidance） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com RAG 生成 幻觉 冲突 拒答 引用 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `enterprise-rag-benchmark-2026` | 预印本（Preprint） | `included` | 补检索噪声、知识缺口、事实冲突和多维指令共同出现时的联合遵循问题 |
| `conflictrag-2026` | 预印本（Preprint） | `included` | 补检测—分类—解决—生成的冲突感知流程和三类冲突 |
| `anthropic-citations-docs-2026` | 官方文档（Official Documentation） | `included` | 当前接口明确原生引用（Native Citations）与严格结构化输出（Structured Outputs）不兼容 |
| `owasp-rag-security-cheat-sheet-2026` | 官方安全指南（Official Security Guidance） | `included_existing` | 输出必须在返回用户或驱动工具前进行策略、敏感数据和动作模式校验 |
| `openai-structured-outputs-docs-2026` | 官方文档（Official Documentation） | `included_existing` | 继续用于结构遵循和拒答边界，不重复登记 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `GEN-K-301` | `knowledge` | 每项约束单独高通过率不代表全部约束同时满足；联合合规（Holistic Compliance）会随约束组合、检索噪声、知识缺口和冲突快速下降 | `enterprise-rag-benchmark-2026` | `new` |
| `GEN-K-302` | `knowledge` | 不同提供商能力可以存在接口级互斥：当前 Claude 原生引用（Claude Native Citations）不能与严格结构化输出（Structured Outputs）在同一请求中启用 | `anthropic-citations-docs-2026` | `new` |
| `GEN-P-301` | `problem_question` | 系统同时要求严格 JSON Schema（JSON 模式）和原生逐声明引用，但目标 API 不支持二者共存；只改提示词无法修复接口级冲突 | `anthropic-citations-docs-2026` | `new` |
| `GEN-P-302` | `problem_question` | 事实冲突、时间演化和观点差异使用同一个“选最新或选最高分”规则，会把主观分歧误判为事实错误，或把旧版本事实误判为虚假 | `conflictrag-2026` | `new` |
| `GEN-P-303` | `problem_question` | 对每个字段分别统计遵循率会掩盖整条响应是否可用；一个必填约束失败就可能使自动化调用整体失败 | `enterprise-rag-benchmark-2026` | `new` |
| `GEN-P-304` | `problem_question` | 模型生成的工具调用或敏感数据输出即使结构合法，也可能违反用户权限和业务策略；模式校验（Schema Validation）不能代替授权与策略执行 | `owasp-rag-security-cheat-sheet-2026` | `new` |
| `GEN-S-301` | `solution` | 先做能力协商（Capability Negotiation）：若引用与严格模式互斥，则选择“带原生引用的文本生成后结构化解析并再次核验”或“结构化声明先生成、再独立引用核验”的显式两阶段流程 | `anthropic-citations-docs-2026`; 既有证据生成来源 | `new` |
| `GEN-E-301` | `evaluation` | 同时报告字段级遵循、约束组合全通过率、无答案拒答、冲突分类、声明支持、输出策略违规和端到端可消费率，并按噪声、缺口和冲突分层 | `enterprise-rag-benchmark-2026`; 既有来源 | `extends` |

## 5. 公开面试题来源核验

未新增题目编号。当前公开题库中的幻觉、上下文不足、结构化输出、生产挑战和评估问题均可映射 `RAG-SCENE-021`、`RAG-SCENE-023`、`RAG-SCENE-024`；本轮新增的是接口兼容和联合合规的技术证据。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 证据条件生成、结构遵循、联合合规、拒答和冲突生成已覆盖 |
| 实现（Implementation） | `covered` | 两阶段能力协商、原生引用、结构化模式和输出校验均有接口入口 |
| 工程问题（Engineering Problem） | `covered` | 能力互斥、联合约束失败、冲突误合并和结构合法但策略非法已登记 |
| 解决方案（Solution） | `covered` | 类型化状态、两阶段流程、外部验证和策略执行已覆盖 |
| 评估（Evaluation） | `covered` | 字段级与整响应级、事实与安全级指标均定义 |
| 公开面试题（Public Interview Question） | `covered` | 既有题目可回链，没有把新论文标题变成题目 |
| 时效（Freshness） | `covered` | 当前 API 能力和 2026 企业压力测试已登记 |
| 安全或治理（Security or Governance） | `covered` | 输出被视为不可信，必须独立授权、脱敏和策略校验 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接上下文、引用、评估、工具调用和生产治理 |

## 7. 冲突、版本与未验证假设

- EnterpriseRAG（企业检索增强生成基准）目前是预印本且声明资产将在发表后发布；无法取得公开数据前不能声称已完整复现其数值。
- ConflictRAG（冲突感知检索增强生成）默认对参数知识—上下文冲突偏向检索证据；实际系统必须结合来源权威、时间、权限和业务规则，不能无条件照搬。
- Anthropic Citations（Anthropic 引用功能）的兼容性是当前产品事实；模型、平台或 API 版本变化后必须重新核验。
- 两阶段生成增加延迟和新的错误传播路径；需要追踪声明标识在两次调用间是否稳定。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 4 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

建立模型与接口能力矩阵（Capability Matrix），针对无答案、部分答案、事实冲突、时间冲突、观点冲突、恶意上下文和多约束结构分别运行单阶段与两阶段生成回放。

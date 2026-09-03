---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-PRODUCTION-GOVERNANCE
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 生产治理（Production Governance）第三轮独立补漏

## 1. 本轮目标与边界

本轮把第二轮留下的“统一 Trace（链路追踪）与事件时间线”变成可实施的数据契约，并补齐 Model Context Protocol（模型上下文协议，MCP）工具供应链、跨服务器隔离、消息重放、人工确认以及 Telemetry Data Minimization（遥测数据最小化）。目标不是把所有原文塞入日志，而是同时满足可定位、可复现、最小披露和权限审计。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 生成式链路语义（GenAI Trace Semantics） | `OpenTelemetry GenAI semantic conventions retrieval documents query text opt-in` | OpenTelemetry 官方仓库（Official Repository）固定提交 |
| Q-302 | 工具供应链安全（Tool Supply-chain Security） | `OWASP MCP tool poisoning rug pull cross server shadowing replay logging` | OWASP 官方安全清单（Official Security Guidance） |
| Q-303 | 协议授权边界（Protocol Authorization Boundary） | `MCP authorization token audience resource parameter confused deputy official` | MCP 正式规范（Official Specification） |
| Q-304 | 轨迹安全评估（Trajectory Safety Evaluation） | `agent trajectory benchmark delayed trigger heterogeneous tool pools safety 2026` | arXiv 原始论文（Original Paper） |
| Q-305 | 公开面试问题（Public Interview Question） | `site:nowcoder.com AI 应用 RAG 评测集 工具 参数 权限 作用范围 面试` | 牛客第一人称面经（First-person Interview Report） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `opentelemetry-genai-semconv-2026` | 官方仓库（Official Repository） | `included` | 固定提交给出推理、嵌入、检索和工具执行 Span（跨度）字段以及内容字段的 Opt-in（选择加入）级别 |
| `owasp-mcp-security-cheat-sheet-2026` | 官方指导（Official Guidance） | `included` | 补 Tool Poisoning（工具投毒）、Rug Pull（抽地毯攻击）、Tool Shadowing（工具遮蔽）、消息重放和人工确认控制 |
| `mcp-authorization-security-2026` | 正式规范（Official Specification） | `included_existing` | 继续约束 Token Audience Binding（令牌受众绑定）、禁止 Token Passthrough（令牌透传）和 Confused Deputy（混淆代理） |
| `atbench-agent-trajectory-safety-2026` | 原始论文（Original Paper） | `included_cross_stage` | 补多步延迟触发风险和中间动作诊断，避免只看最终答案 |
| `nowcoder-ai-app-intern-rag-eval-2026` | 第一人称面经（First-person Interview Report） | `included_question` | 明确出现工具参数、权限和作用范围，以及 RAG 评测可信度追问 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `PROD-K-301` | `knowledge` | 统一可观测性不能等于默认记录原始 Query（查询）、Prompt（提示）、Retrieved Document（检索文档）和 Tool Definition（工具定义）；OpenTelemetry GenAI Semantic Conventions（OpenTelemetry 生成式人工智能语义约定）把这些内容字段标为 Opt-in（选择加入），并警告可能包含敏感信息 | `opentelemetry-genai-semconv-2026` | `new` |
| `PROD-K-302` | `knowledge` | Tool Definition（工具定义）是运行时供应链资产：名称、描述、参数 Schema（模式）或返回结构变化都可能改变 Agent（智能体）决策，因此需要版本、哈希、审批和变更事件 | `owasp-mcp-security-cheat-sheet-2026` | `new` |
| `PROD-P-301` | `problem_question` | 只保存 Trace ID（追踪标识）却不保存索引、模型、Prompt（提示）、工具目录和策略版本，不能重放当时决策；保存全部原文又会扩大 PII（个人可识别信息）、密钥和商业数据泄漏面 | 两项新增来源 | `new` |
| `PROD-P-302` | `problem_question` | TLS（传输层安全）只保护传输段，消息在终止代理后仍可能被篡改或重放；重试、重复投递与恶意重放若没有 Nonce（一次性随机数）、Timestamp（时间戳）和 Idempotency Key（幂等键）会混在一起 | `owasp-mcp-security-cheat-sheet-2026` | `new` |
| `PROD-P-303` | `problem_question` | 用户曾批准某工具不代表批准其后续变更；Rug Pull（抽地毯攻击）和跨服务器 Tool Shadowing（工具遮蔽）会让另一安全域的描述影响可信工具调用 | `owasp-mcp-security-cheat-sheet-2026` | `new` |
| `PROD-P-304` | `problem_question` | 只在最终高风险动作前弹出摘要式确认，用户无法核对完整参数、目标资源和数据范围，且确认界面若受模型输出驱动可能被绕过 | `owasp-mcp-security-cheat-sheet-2026` | `new` |
| `PROD-S-301` | `solution` | 默认 Trace（链路追踪）保存低敏的 ID（标识）、版本、哈希、分数、计数、耗时、权限决策和错误；原始内容进入受控 Sampling（采样）通道，执行脱敏、加密、访问审计、保留期和删除策略 | OpenTelemetry 与 OWASP | `extends` |
| `PROD-S-302` | `solution` | 在工具发现时规范化并哈希 Tool Definition（工具定义），执行前重算；变更即阻断或重新审批。每个 MCP Server（模型上下文协议服务器）使用独立最小权限凭据，Tool Return（工具返回）按不可信数据校验 | OWASP 与 MCP 规范 | `extends` |
| `PROD-E-301` | `evaluation` | 演练矩阵新增工具定义突变、跨服务器遮蔽、消息重放、SSRF（服务端请求伪造）、遥测原文泄漏、确认绕过和密钥进入日志，并检查检测、阻断、证据保全与恢复 | 新增来源 | `new` |

## 5. 统一链路追踪数据契约

| 层级 | 默认记录 | 受控记录 | 关键关联 |
|---|---|---|---|
| 请求身份（Request Identity） | 请求 ID（标识）、Trace ID（追踪标识）、租户、主体、会话、策略决策 ID（标识） | 经审批的用户输入片段 | 身份 → 权限 → 检索与工具 |
| 知识版本（Knowledge Version） | 数据源、文档、Chunk（文本块）、索引、Embedding（嵌入）模型和 ACL（访问控制列表）版本或哈希 | 原文快照进入受限证据库 | 索引 → 候选 → 引用 |
| 检索生成（Retrieval and Generation） | Query（查询）哈希、Top-k（前 k 项）、候选 ID（标识）与分数、Prompt（提示）版本、模型、Token（词元）、结束原因 | 原始 Query（查询）、候选和消息按 Opt-in（选择加入）采样 | Query（查询）→ 候选 → 答案 |
| 工具执行（Tool Execution） | 服务器、工具、定义哈希、凭据受众、作用域、参数摘要、审批 ID（标识）、结果哈希、错误 | 完整参数和响应仅在加密受控审计域 | 规划 → 审批 → 执行 → 返回 |
| 产出证据（Output Evidence） | Answer（答案）版本、Claim（声明）、Citation（引用）指针、来源与权限快照、核验结果 | 必要的答案正文和证据跨度 | 答案 → 声明 → 引用 |

上述表是来源约束下的工程合成，不声称是 OpenTelemetry 的完整标准字段；落地时要固定 `opentelemetry-genai-semconv-2026` 对应提交并维护本地字段映射。

## 6. 可执行演练矩阵

| 演练 | 注入条件 | 预期控制 | 必留证据 |
|---|---|---|---|
| 跨租户缓存（Cross-tenant Cache） | 同 Query（查询）、不同租户或 ACL（访问控制列表） | 缓存键包含租户、权限、索引、模型和策略版本 | 命中键摘要、权限决策、拒绝结果 |
| 工具突变（Tool Rug Pull） | 审批后修改描述或参数 Schema（模式） | 定义哈希不一致时阻断并重新审批 | 旧新哈希、差异、审批人、阻断事件 |
| 跨服务遮蔽（Cross-server Shadowing） | 不可信服务器描述诱导调用可信工具 | 安全域隔离和跨域数据流策略 | 工具目录版本、规划轨迹、跨域告警 |
| 消息重放（Message Replay） | 重复发送有效高风险调用 | 签名、Nonce（一次性随机数）、Timestamp（时间戳）和 Idempotency Key（幂等键）拒绝重复动作 | 签名校验、Nonce（一次性随机数）状态、幂等结果 |
| 遥测泄漏（Telemetry Leakage） | Query（查询）含 PII（个人可识别信息）或密钥 | 默认不采原文，受控通道脱敏并限制访问与保留期 | 脱敏规则、访问记录、删除证明 |
| 间接注入（Indirect Prompt Injection） | 检索文档或 Tool Return（工具返回）含指令 | 数据—指令分离、输出校验、敏感动作人工确认 | 来源、净化结果、模型决定、确认参数 |

## 7. 公开面试题来源核验

新增 `RAG-SCENE-025` 与 `RAG-SCENE-026`。前者保留“近乎满分命中率是否可信、公开文档预训练污染、私有未见数据”这一不可被普通评测集设计问题完全替代的条件；后者保留“工具参数、权限和作用范围怎样描述与传播”这一 Agentic RAG（智能体检索增强生成）交叉问题。二者均为发布者自述，不标成企业官方题库。

## 8. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 可观测性、数据最小化、工具安全域和消息完整性已覆盖 |
| 实现（Implementation） | `covered` | OpenTelemetry 固定提交、MCP 正式规范和 OWASP 控制入口已登记 |
| 工程问题（Engineering Problem） | `covered` | 重放、工具突变、遮蔽、日志泄漏和确认绕过已登记 |
| 解决方案（Solution） | `covered` | 版本哈希、独立凭据、受控内容采样和演练矩阵已形成 |
| 评估（Evaluation） | `covered` | 质量、成本、尾延迟、恢复和安全演练可共同回归 |
| 公开面试题（Public Interview Question） | `covered` | 新增两项第一人称面经问题并保留来源定位 |
| 时效（Freshness） | `covered` | 2026-08 论文、当前规范与固定仓库提交已核验 |
| 安全或治理（Security or Governance） | `covered` | 身份、权限、供应链、日志、审批、恢复与证据保全已连接 |
| 跨节点关系（Cross-stage Relation） | `covered` | Trace（链路追踪）连接身份、索引、检索、生成、工具、引用与事件响应 |

## 9. 冲突、版本与未验证假设

- OpenTelemetry GenAI Semantic Conventions（OpenTelemetry 生成式人工智能语义约定）当前标为 Development（开发中），不能把字段名当永久接口；固定提交只保证本次审计可复核。
- OWASP 建议记录工具完整参数，同时要求去除密钥和 PII（个人可识别信息）；工程上必须用受控审计域、字段分级与脱敏解决张力，不能把完整参数无条件送入普通日志。
- Message Signing（消息签名）和 Replay Protection（重放防护）的具体算法与时间窗要由正式协议和威胁模型决定；本轮不把指导示例误写为唯一实现。
- 轨迹可回放不等于保存模型 Chain of Thought（思维链）；只保存可审计动作、输入输出引用、决策标签和版本。

## 10. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 4 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 11. 下一轮动作

把统一链路追踪数据契约固化为机器可读 Trace Schema（追踪模式）和 Exercise Manifest（演练清单）；在第四轮用独立来源核查日志最小化、模型与工具目录迁移、审批可用性以及多租户事件复盘，不复用本轮查询措辞。

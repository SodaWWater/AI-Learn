---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-QUERY-ROUTING
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 查询路由（Query Routing）第三轮独立补漏

## 1. 本轮目标与边界

本轮不重复查“如何分类查询”，而是验证路由目标同时作为授权资源（Authorization Resource）和数据处理边界（Data-processing Boundary）时的工程约束。查询路由器（Query Router）负责选择知识源、检索链或外部工具；它不能替代每个下游服务自己的授权校验（Authorization Validation），也不能把一个服务收到的访问令牌（Access Token）原样传给另一个资源服务器（Resource Server）。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 令牌受众（Token Audience） | `MCP authorization security token audience binding token passthrough` | MCP 官方规范（Official Specification） |
| Q-302 | 混淆代理（Confused Deputy） | `MCP intermediary upstream API separate token resource parameter` | MCP 官方规范（Official Specification） |
| Q-303 | 失败关闭（Fail Closed） | `OWASP RAG retrieval authorization failure fail closed fallback model memory` | OWASP 官方安全指南（Official Security Guidance） |
| Q-304 | 数据驻留（Data Residency） | `RAG router external tool data residency deployment official documentation` | 提供商官方文档（Provider Documentation） |
| Q-305 | 公开题目（Public Question） | `site:nowcoder.com RAG 路由 权限 回退 工具调用 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `mcp-authorization-security-2026` | 官方规范（Official Specification） | `included` | 明确令牌受众绑定（Token Audience Binding）、资源参数（Resource Parameter）、禁止令牌透传（Token Passthrough）和上游服务独立令牌 |
| `owasp-rag-security-cheat-sheet-2026` | 官方安全指南（Official Security Guidance） | `included` | 明确检索时授权（Retrieval-time Authorization）、跨租户测试（Cross-tenant Testing）、缓存泄露（Cache Leakage）和失败关闭（Fail Closed） |
| `azure-foundry-deployment-types-2026` | 官方文档（Official Documentation） | `included_existing` | 已登记全局、数据区域和区域部署（Global, Data-zone and Regional Deployment）的驻留—延迟边界 |
| 通用 OAuth 摘要文章 | 二手文章（Secondary Article） | `excluded` | 原始规范和协议安全文档已足够，二手转述不增加类型 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `ROUTE-K-301` | `knowledge` | 路由目标不仅是语义标签，还对应受众受限的授权资源（Audience-bound Authorization Resource）；语义正确但令牌受众错误仍是无效路由 | `mcp-authorization-security-2026` | `new` |
| `ROUTE-P-301` | `problem_question` | 查询路由器（Query Router）或 MCP 中间层（MCP Intermediary）把入站访问令牌（Inbound Access Token）透传给上游服务，会造成令牌受众混淆（Token Audience Confusion）和混淆代理（Confused Deputy）风险 | `mcp-authorization-security-2026` | `new` |
| `ROUTE-P-302` | `problem_question` | 路由失败若不区分空结果（Empty Result）、服务不可用（Service Unavailable）、超时（Timeout）、授权失败（Authorization Failure）和策略拒绝（Policy Denial），回退可能把安全失败错误地转换成更宽范围检索或模型记忆回答（Model-memory Answer） | `owasp-rag-security-cheat-sheet-2026` | `new` |
| `ROUTE-S-301` | `solution` | 在选择和扇出前按身份、权限、受众和数据驻留做候选裁剪；外部工具使用单独获取且受众正确的访问令牌（Access Token），授权失败执行失败关闭（Fail Closed） | 两项新增官方来源；`azure-foundry-deployment-types-2026` | `new` |
| `ROUTE-E-301` | `evaluation` | 故障注入（Fault Injection）应覆盖错误受众、过期令牌、权限撤销、跨租户路由、工具超时、区域不可用和策略拒绝，并核验没有扩大检索范围或跨安全域复用缓存 | 两项新增官方来源 | `new` |

## 5. 公开面试题来源核验

未新增题目。公开检索命中仍可归入 `RAG-SCENE-014`、`RAG-SCENE-016` 和 `RAG-SCENE-022`；本轮补的是这些路由与权限题的协议级证据和故障分类，不把官方规范自行改写成“公开面试题”。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 已覆盖语义路由、查询—语料兼容性和授权资源边界 |
| 实现（Implementation） | `covered` | 策略层（Policy Layer）、受众校验和独立上游令牌已有实现契约 |
| 工程问题（Engineering Problem） | `covered` | 误路由、令牌透传、回退扩大权限和缓存跨域均已登记 |
| 解决方案（Solution） | `covered` | 授权前置裁剪、失败状态机和失败关闭（Fail Closed）已覆盖 |
| 评估（Evaluation） | `covered` | 增加权限感知故障注入（Permission-aware Fault Injection） |
| 公开面试题（Public Interview Question） | `covered` | 沿用已有可回链题目，不伪造新题 |
| 时效（Freshness） | `covered` | 当前 MCP 规范（MCP Specification）和 OWASP 指南（OWASP Guidance）已登记版本 |
| 安全或治理（Security or Governance） | `covered` | 身份传播、受众绑定、驻留、日志和失败关闭已形成闭环 |
| 跨节点关系（Cross-stage Relation） | `covered` | 已连接查询理解、检索、工具调用、生产治理和智能体检索增强生成（Agentic RAG） |

## 7. 冲突、版本与未验证假设

- MCP 授权规范（MCP Authorization Specification）约束 MCP 客户端（MCP Client）与 MCP 服务器（MCP Server）；非 MCP 架构仍需映射到自身的 OAuth 2.0（OAuth 2.0）或服务身份契约，不能机械套用。
- 路由缓存（Routing Cache）的缓存键至少要反映身份、权限、受众、知识源版本、策略版本和驻留边界；若无法证明隔离，宁可禁用跨域复用。
- 模型记忆回答（Model-memory Answer）可以作为明确标注的产品模式，但不能在授权失败后静默触发，否则用户无法区分“无证据”和“无权限”。
- 数据驻留（Data Residency）取决于提供商、部署类型、区域和合同；本轮来源不能支持跨提供商通用承诺。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 2 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

将误路由成本矩阵（Misrouting Cost Matrix）与本轮故障状态机合并为可回放用例；下一轮重点检查多工具扇出时的并发取消、部分成功（Partial Success）和审计事件关联。

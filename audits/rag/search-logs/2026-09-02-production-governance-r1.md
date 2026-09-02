---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-PRODUCTION-GOVERNANCE
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：生产治理（Production Governance）第一轮

## 1. 本轮目标与边界

核查访问控制、租户隔离、Prompt Injection、知识库投毒、可观测性、发布回滚、成本性能和灾难恢复。本节点跨越摄取到答案全链路，不把安全只放在最终 Prompt。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 安全标准 | `site:owasp.org Top 10 LLM prompt injection data poisoning 2025` | OWASP 官方资料 |
| Q-002 | 风险框架 | `site:nist.gov NIST AI 600-1 Generative AI Profile` | NIST 官方资料 |
| Q-003 | 投毒 | `site:arxiv.org PoisonedRAG knowledge corruption attacks` | 原始论文 |
| Q-004 | 间接注入 | `site:arxiv.org indirect prompt injection retrieval RAG 2026` | 原始论文 |
| Q-005 | 可观测性 | `site:docs.langchain.com LangSmith observability tracing` | 官方文档 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `owasp-llm-top10-2025` | 官方文档 | `included` | 威胁分类，不作为具体产品防护保证 |
| `nist-genai-profile-2024` | 官方文档 | `included` | 风险治理流程 |
| `poisonedrag-2024` | 原始论文 | `included` | 知识库投毒攻击模型 |
| `indirect-prompt-injection-wild-2026` | 原始论文 | `included` | 外部文档中的真实注入风险 |
| `azure-document-access-control-2026` | 官方文档 | `included` | 文档级权限和 Preview 边界 |
| `langsmith-observability-docs-2026` | 官方文档 | `included` | Tracing 实现入口 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `PROD-K-001` | `knowledge` | RAG 攻击面包括数据源、解析、索引、检索、上下文和生成 | `new` |
| `PROD-P-001` | `problem_question` | ACL 只在答案层检查时已经发生越权检索和日志泄露 | `new` |
| `PROD-P-002` | `problem_question` | 恶意文档通过检索进入上下文并覆盖系统目标 | `new` |
| `PROD-P-003` | `problem_question` | 模型/索引/Prompt 多版本混用导致无法回滚和归因 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 短转述 | 来源类型 | 是否真实面试 | 技术核验 |
|---|---|---|---|---|
| `RAG-SCENE-008` | 生产 RAG 的权限、更新、延迟和监控怎样治理 | 公开题库 | 否 | OWASP、NIST、Azure 官方文档 |
| `RAG-SCENE-009` | 文档更新删除怎样保证一致和回滚 | 公开题库 | 否 | 数据库与索引官方文档 |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理 | `covered` | 威胁模型、权限、可靠性、观测 |
| 实现 | `partial` | 具体网关、策略引擎和备份脚本待补 |
| 工程问题 | `covered` | 越权、注入、投毒、版本、成本 |
| 解决方案 | `partial` | Red Team、来源签名、回滚 Runbook 待补 |
| 评估 | `partial` | 安全和灾备演练指标待补 |
| 公开面试题 | `covered` | 生产与更新题目有来源 |
| 时效 | `covered` | 2025 OWASP、2026 攻击与官方文档 |
| 安全或治理 | `covered` | 本节点核心 |
| 跨节点关系 | `covered` | 全链路 |

## 7. 冲突、版本与未验证假设

- RAG 不会天然消除 Prompt Injection 或数据泄露；
- 文档级 ACL、Chunk ACL 和查询时身份过滤需保持同一权限语义；
- 下一轮补租户隔离、缓存污染、灾备 RPO/RTO、红队和 Incident Response。

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

补租户隔离、策略引擎、缓存污染、SLO、RPO/RTO、红队、应急响应和成本容量模型。

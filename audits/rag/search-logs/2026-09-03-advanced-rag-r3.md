---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-ADVANCED-RAG
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 高级检索增强生成（Advanced RAG）第三轮独立补漏

## 1. 本轮目标与边界

本轮完成第二轮登记的四项缺口：跨范式选型、逐跳轨迹、Multimodal Indirect Prompt Injection（多模态间接提示注入）、Tool Permission Propagation（工具权限传播）和 Evidence-saturation Stopping（证据饱和停止）。高级检索增强生成（Advanced RAG）继续被建模为能力组合，不把产品名或论文名当作单一成熟度阶梯。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 多模态统一比较（Unified Multimodal Comparison） | `document-centric multimodal RAG benchmark text image fusion joint retrieval standardized candidate pools` | arXiv 原始论文（Original Paper） |
| Q-302 | 多模态攻击面（Multimodal Attack Surface） | `multimodal RAG metadata poisoning image text entry retrieval generator attack` | arXiv 原始论文（Original Paper） |
| Q-303 | 网页间接注入（Web Indirect Injection） | `social web indirect prompt injection RAG sparse dense retriever sanitization benchmark` | arXiv 原始论文（Original Paper） |
| Q-304 | 轨迹级安全（Trajectory-level Safety） | `agent trajectory safety delayed trigger heterogeneous tool pools benchmark 2026` | arXiv 原始论文（Original Paper） |
| Q-305 | 工具权限（Tool Permission） | `MCP authorization security tool poisoning cross server permissions official` | MCP 规范与 OWASP 指导（Official Sources） |
| Q-306 | 公开面试问题（Public Interview Question） | `site:nowcoder.com Deep Research Agentic RAG MCP 权限 工具注册 面试` | 牛客公开页面（Nowcoder Public Pages） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `unidoc-bench-2026` | 原始论文（Original Paper） | `included` | 在相同候选池、提示和指标下比较 Text-only（纯文本）、Image-only（纯图像）、Text-image Fusion（图文融合）和 Joint Retrieval（联合检索） |
| `mm-mepa-multimodal-rag-poisoning-2026` | 原始论文（Original Paper） | `included` | 明确展示只修改图文条目的 Metadata（元数据）也能同时影响检索和生成 |
| `openrag-soc-indirect-injection-2026` | 原始论文（Original Paper） | `included` | 补网页原生载体穿过摄取链路、稀疏和稠密排序位移以及防御效用—延迟共同评估 |
| `atbench-agent-trajectory-safety-2026` | 原始论文（Original Paper） | `included` | 风险来源、失败模式和现实伤害三维分类，包含异构工具池和延迟触发长轨迹 |
| `owasp-mcp-security-cheat-sheet-2026` | 官方指导（Official Guidance） | `included` | 工具定义、返回值、跨服务器关系和权限均纳入不可信边界 |
| `enterprise-deep-research-termination-2026` | 原始论文（Original Paper） | `included_existing` | 继续约束 Evidence-aware Termination（证据感知停止），不使用固定轮数代替充分性 |
| `nowcoder-ai-app-intern-rag-eval-2026` | 第一人称面经（First-person Interview Report） | `included_question` | 补工具参数、权限和作用范围的公开追问；仍未找到独立 Deep Research（深度研究）第一人称原题 |
| `trustworthy-agentic-multimodal-defense-2025` | 预印本（Preprint） | `excluded_lower_priority` | 提出跨智能体多模态防御，但本轮已有更直接的多模态 RAG 攻击实验和正式安全指导，避免重复登记较弱证据 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `ADV-K-301` | `knowledge` | Multimodal RAG（多模态检索增强生成）至少包含纯文本、纯图像、后置图文融合和联合多模态检索等不同证据路径；应固定候选池和生成条件比较，而不是只换 Embedding（嵌入）模型 | `unidoc-bench-2026` | `new` |
| `ADV-K-302` | `knowledge` | Agentic RAG（智能体检索增强生成）的安全单位是完整 Trajectory（轨迹）：风险可在多轮后触发，最终回答无害也不能抹去中间越权或危险动作 | `atbench-agent-trajectory-safety-2026` | `new` |
| `ADV-P-301` | `problem_question` | OCR（光学字符识别）把页面压成文本会丢失布局和视觉语义，但引入图像、图文 Metadata（元数据）和 Vision-language Model（视觉语言模型）又增加新的检索与注入攻击面 | 两项多模态来源 | `new` |
| `ADV-P-302` | `problem_question` | 仅清洗正文不足以防多模态投毒；攻击指令或诱导特征可位于 HTML/Markdown（超文本标记语言/Markdown 标记）、Unicode（统一码）、图片、图文 Metadata（元数据）或 Tool Return（工具返回） | 多项新增来源 | `new` |
| `ADV-P-303` | `problem_question` | 检索授权通过不代表工具授权通过：Agent（智能体）把用户证据交给另一个服务器或以服务器自身广泛凭据执行时，会形成跨安全域 Confused Deputy（混淆代理）和数据外泄 | MCP 规范与 OWASP | `new` |
| `ADV-P-304` | `problem_question` | Evidence-saturation Stopping（证据饱和停止）若只看连续两轮无新文档，会被同源重复、未覆盖子问题、冲突未解或权限不可访问误导 | 既有停止论文与本轮统一轨迹约束 | `new` |
| `ADV-P-305` | `problem_question` | 跨范式比较如果预算、工具权限、候选池、模型和停止规则不同，答案质量差异无法归因于 GraphRAG（图检索增强生成）、Agentic RAG（智能体检索增强生成）或 Multimodal RAG（多模态检索增强生成）本身 | 新增与既有来源 | `new` |
| `ADV-S-301` | `solution` | 每一跳显式记录父动作、子查询、检索器或工具、身份、权限决策、输入输出证据、版本、成本、状态、风险标签和停止理由；工具返回继续视为不可信数据 | ATBench、OpenTelemetry、MCP 与 OWASP | `extends` |
| `ADV-S-302` | `solution` | 证据停止同时检查子问题覆盖、声明支持、来源独立性、冲突状态、边际信息增益、权限边界、剩余预算和硬上限；任何单项阈值都不能独立证明充分 | 既有停止论文与新增评估来源 | `extends` |
| `ADV-E-301` | `evaluation` | 多模态和网页安全回归同时报告 Attack Success（攻击成功）、Retriever Rank Shift（检索排序位移）、Utility（效用）、Latency（延迟）、证据覆盖和跨模态来源追踪 | `openrag-soc-indirect-injection-2026`; `mm-mepa-multimodal-rag-poisoning-2026` | `new` |

## 5. 跨范式选型矩阵

| 范式 | 主要证据拓扑 | 何时增加价值 | 新增成本或风险 | 必须固定的比较条件 |
|---|---|---|---|---|
| Naive RAG（朴素检索增强生成） | 单次 Query（查询）→ 单次检索 → 生成 | 事实边界清楚、单跳、低延迟 | 复杂问题覆盖不足 | 语料、Top-k（前 k 项）、模型、Token（词元）预算 |
| Modular RAG（模块化检索增强生成） | 可重构模块与路由 | 多场景需要不同解析、检索和生成策略 | 配置空间与契约漂移 | 模块版本、输入输出 Schema（模式）、路由策略 |
| GraphRAG（图检索增强生成） | 实体—关系—社区或路径 | 跨文档关系、多跳、全局主题 | 图构建成本、路径爆炸和更新复杂度 | 图快照、遍历预算、剪枝和向量基线 |
| Agentic RAG（智能体检索增强生成） | 规划—行动—观察循环 | 查询需动态分解、外部工具和纠错 | 权限、长轨迹、非确定性和注入 | 工具目录与哈希、权限、轮数、预算、停止规则 |
| Multimodal RAG（多模态检索增强生成） | 文本、表格、图像与布局证据 | 答案依赖视觉或空间语义 | 解析、跨模态对齐、Metadata（元数据）投毒 | 候选池、模态、融合点、模型和证据标注 |
| Deep Research（深度研究） | 多源迭代搜索与证据综合 | 开放问题、来源交叉验证和长报告 | 时延、成本、来源动态性、注入和停止困难 | 搜索范围、来源策略、权限、预算、停止、引用核验 |

矩阵是对已登记原始论文和官方资料的归纳，不把任一行写成固定技术栈；同一系统可以按请求路由到多条路径。

## 6. 逐跳轨迹模式

| 字段组 | 最小字段 | 作用 |
|---|---|---|
| 结构（Structure） | `trace_id`, `step_id`, `parent_step_id`, `attempt` | 还原分支、重试和因果顺序 |
| 意图（Intent） | `goal_id`, `subquery_id`, `action_type`, `stop_reason` | 区分覆盖哪个子问题和为何继续或停止 |
| 执行（Execution） | `retriever_or_tool`, `definition_hash`, `input_ref`, `output_ref`, `status` | 固定检索器、工具目录和引用，不默认保存敏感原文 |
| 权限（Authorization） | `subject`, `tenant`, `resource`, `audience`, `scope`, `decision_id` | 验证每一跳使用请求用户的允许范围 |
| 证据（Evidence） | `source_id`, `snapshot`, `claim_ids`, `support`, `conflict_set` | 计算覆盖、声明支持、来源独立性和冲突 |
| 成本（Budget） | `latency`, `tokens`, `calls`, `remaining_budget` | 比较范式并执行硬上限 |
| 安全（Safety） | `trust_label`, `injection_signal`, `approval_id`, `policy_result` | 发现最终答案之外的中间危险动作 |

该模式是知识图谱和后续实验的候选合同，不是某个框架的现成 API（应用程序接口）。

## 7. 证据停止的可复现实验

固定 Query Set（查询集）、Source Snapshot（来源快照）、模型、工具目录、权限、总调用和 Token Budget（词元预算），对以下停止器做成对回放：Fixed Hop（固定跳数）、No-new-document（无新文档）、Marginal Gain（边际增益）和 Evidence-aware（证据感知）。逐轮记录子问题覆盖、受支持声明、独立来源数、未解冲突、重复率、成本与安全失败；在相同硬上限下比较最终完整性、可核验性、引用正确性、轨迹安全和超预算率。

这个实验只能回答“在给定来源快照与权限下哪种停止器更合适”，不能证明整个开放网页已被穷尽；权限拒绝与来源不可达必须作为未观测状态单独报告。

## 8. 公开面试题来源核验

新增 `RAG-SCENE-026`，对应工具注册、参数、权限和作用范围这一 Agentic RAG（智能体检索增强生成）交叉问题。Deep Research（深度研究）检索仍未找到可独立验证的第一人称原题，不从论文标题反造面试问题；相关工程知识保留，题目来源缺口继续公开标记。

## 9. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 模块化、多模态、图、智能体和深度研究的证据拓扑已区分 |
| 实现（Implementation） | `covered` | 逐跳模式、权限字段和停止实验已给出可落地合同 |
| 工程问题（Engineering Problem） | `covered` | 跨模态投毒、工具越权、停止误判和比较混杂已登记 |
| 解决方案（Solution） | `covered` | 来源追踪、每跳授权、工具哈希、联合停止条件和硬预算已连接 |
| 评估（Evaluation） | `covered` | 答案、证据、轨迹、成本、停止和安全指标共同进入比较 |
| 公开面试题（Public Interview Question） | `partial` | 工具权限有第一人称来源；Deep Research（深度研究）第一人称原题仍缺 |
| 时效（Freshness） | `covered` | 2026-08 最新轨迹基准与 2026 多模态攻击、网页注入研究已登记 |
| 安全或治理（Security or Governance） | `covered` | 模态、网页、Metadata（元数据）、工具定义、返回值和跨服务器均纳入威胁面 |
| 跨节点关系（Cross-stage Relation） | `covered` | 解析、检索、路由、生成、引用、评估、工具和治理可由同一轨迹连接 |

## 10. 冲突、版本与未验证假设

- UniDoc-Bench（统一文档基准）的实验显示其设置下图文融合优于单模态和联合 Embedding（嵌入）检索，但不能据此规定所有业务都选择融合路线。
- MM-MEPA（多模态元数据投毒攻击）的成功率来自指定检索器、生成器和数据；本项目只采纳“Metadata（元数据）也是攻击面”这一类型与实验方法。
- ATBench（智能体轨迹基准）评估通用智能体安全，不等同于 RAG 专属基准；本轮仅迁移轨迹级观察原则和风险分类维度。
- OpenRAG-Soc（开放社会网页检索增强生成基准）的网页载体与防御不能覆盖图片隐写、文档附件和所有脚本行为；多模态和网页安全必须分层测试。

## 11. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 5 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 12. 下一轮动作

第四轮从独立来源族验证跨范式矩阵、逐跳模式和停止实验；专项查找 Deep Research（深度研究）第一人称面试来源，并检验工具权限在 LangGraph（LangGraph 图编排框架）、LlamaIndex（LlamaIndex 数据框架）或其他实现中的实际传播边界，但不把框架默认行为当安全保证。

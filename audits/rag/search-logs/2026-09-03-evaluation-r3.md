---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-EVALUATION
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 评估（Evaluation）第三轮独立补漏

## 1. 本轮目标与边界

本轮补查询问覆盖（Query Coverage）、原子声明可核验性（Atomic-claim Verifiability）、联合约束通过率（Joint-constraint Pass Rate）和非理想企业检索（Non-ideal Enterprise Retrieval）。评估（Evaluation）不只给一个总分，还要指出错误发生在子查询、候选、声明、约束组合还是安全策略。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 查询无关评估（Query-agnostic Evaluation） | `Q-CARE query coverage claim verifiability reference-free RAG evaluation COLM 2026` | arXiv 原始论文（Original Paper） |
| Q-302 | 可执行框架（Runnable Framework） | `repo:DISL-Lab/Q-CaRE-COLM-26 C-Prec C-nDCG completeness conciseness verifiableness` | GitHub 官方仓库（Official Repository） |
| Q-303 | 企业压力测试（Enterprise Stress Test） | `EnterpriseRAG retrieval noise knowledge gaps factual conflicts multi-constraint instruction adherence` | arXiv 原始论文（Original Paper） |
| Q-304 | 公开工程问题（Public Engineering Problem） | `site:nowcoder.com RAG 评估 Trace Bad Case Golden Dataset 面试` | 牛客公开页面（Nowcoder Public Pages） |
| Q-305 | 当前核验服务（Current Verification Service） | `Google check grounding claim-level score citation threshold official` | Google Cloud 官方文档（Official Documentation） |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `qcare-rag-evaluation-2026` | 原始论文（Original Paper） | `included` | 提供按子查询覆盖和原子声明支持统一检索器与生成器诊断的最新研究 |
| `qcare-official-repository-2026` | 官方仓库（Official Repository） | `included` | 固定提交包含评估脚本、提示、800 条查询和逐样本中间判断 |
| `enterprise-rag-benchmark-2026` | 预印本（Preprint） | `included` | 补检索噪声、知识缺口、事实冲突和多约束共同出现的压力测试设计 |
| `google-check-grounding-docs-2026` | 官方文档（Official Documentation） | `included_cross_stage` | 作为声明级核验服务实现，不替代人工标注真值 |
| `nowcoder-rag-evaluation-funnel-2026` | 公开工程讲解（Public Engineering Explainer） | `included_problem_framing` | 补链路漏斗、Trace（追踪）、Bad Case（坏样本）和 Golden Dataset（黄金数据集）的公开问题表达；不采纳其技术结论作为一手证据 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 关系 |
|---|---|---|---|---|
| `EVAL-K-301` | `knowledge` | 查询可分解为多个最小子查询，候选对不同子查询的覆盖程度提供分级相关性；二元 Relevant/Irrelevant（相关/不相关）标签会丢失“覆盖多少需求”的信息 | `qcare-rag-evaluation-2026` | `new` |
| `EVAL-K-302` | `knowledge` | 生成评估需要同时区分 Completeness（完整性）、Conciseness（简洁性）和 Verifiableness（可核验性）：回答完所有子问题、没有多余声明、每个声明有证据是三个不同目标 | `qcare-rag-evaluation-2026` | `new` |
| `EVAL-P-301` | `problem_question` | Reference-free Evaluation（无参考答案评估）仍依赖查询分解器和声明—证据对齐判断器；若分解错误，多个派生指标会同时偏移而显得彼此一致 | 论文与固定仓库 | `new` |
| `EVAL-P-302` | `problem_question` | 只统计单项约束平均通过率，会掩盖整条响应同时满足格式、语气、引用、权限、拒答和长度要求的联合失败 | `enterprise-rag-benchmark-2026` | `new` |
| `EVAL-P-303` | `problem_question` | 在干净检索集上提升总分，不能证明系统对检索噪声、知识缺口和事实冲突稳健；三类条件必须独立注入和分层报告 | `enterprise-rag-benchmark-2026` | `new` |
| `EVAL-P-304` | `problem_question` | 评估框架代码、评估模型、提示模板、解析模式和测试数据任何一项变化都可能改变得分；只固定被测 RAG 版本无法复现结论 | `qcare-official-repository-2026` | `new` |
| `EVAL-S-301` | `solution` | 评估清单固定查询、候选快照、答案、被测系统、分解器、裁判模型、提示、解析器和指标版本；逐样本保留子查询、原子声明和对齐判断供人工抽检 | 论文与固定仓库 | `extends` |
| `EVAL-E-301` | `evaluation` | 发布门禁同时报告 C-Prec@K（覆盖感知 K 位精确率）、C-nDCG@K（覆盖感知 K 位归一化折损累积增益）、完整性、简洁性、可核验性、联合约束全通过率、分层置信区间和安全回归失败数 | 新增与既有来源 | `new` |

## 5. 公开面试题来源核验

未新增题目编号。新检索到的公开工程讲解继续归入 `RAG-SCENE-001` 与 `RAG-SCENE-021` 的“如何构建评测集”和“如何定位 RAG 链路坏样本”；它不是明确的公司原题或第一人称面经，故只增加来源，不增加题目计数。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 子查询覆盖、声明核验、联合合规和统计不确定性已覆盖 |
| 实现（Implementation） | `covered` | Q-CARE（查询覆盖与声明可核验）固定仓库和当前核验 API 已登记 |
| 工程问题（Engineering Problem） | `covered` | 分解误差、干净集偏差、联合约束失败、版本漂移和长尾已登记 |
| 解决方案（Solution） | `covered` | 冻结清单、逐样本轨迹、人工抽检、分层和成对回放已覆盖 |
| 评估（Evaluation） | `covered` | 节点、声明、联合约束、端到端、安全和统计层均有指标 |
| 公开面试题（Public Interview Question） | `covered` | 公开问题表达可回链，未把工程文章冒充公司面经 |
| 时效（Freshness） | `covered` | 2026-08 论文、固定仓库和当前产品文档已登记 |
| 安全或治理（Security or Governance） | `covered` | 安全回归、权限和数据分层进入发布门禁 |
| 跨节点关系（Cross-stage Relation） | `covered` | 同一分解连接查询、检索、生成、引用和端到端诊断 |

## 7. 冲突、版本与未验证假设

- Q-CARE（查询覆盖与声明可核验）的论文报告与公开仓库是最新路线，但其自动判断仍需目标语言和领域人工校准；不能因“与人类相关性更高”而视为真值。
- Q-CARE 测试集（Q-CARE Testbed）包含八个数据集各 100 条查询；它不代表本项目未来业务流量，必须另建中文和领域分层集。
- EnterpriseRAG（企业检索增强生成基准）公开摘要给出 983 条专家验证样本，但当前声明资产将在发表后发布；未释放前只能采用压力维度，不能声称完成复现。
- C-Prec@K（覆盖感知 K 位精确率）与 C-nDCG@K（覆盖感知 K 位归一化折损累积增益）依赖子查询分解；与传统标注指标冲突时应回到样本级判断，而不是只比较总分。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 本轮新增知识类型数 | 2 |
| 本轮新增问题类型数 | 4 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete`，不得标记饱和 |

## 9. 下一轮动作

生成可执行评估清单（Evaluation Manifest）和样本级结果格式；先对中文事实、数值、时间、多跳、冲突、无答案、权限和注入样本校准分解器与裁判，再决定自动发布阈值。

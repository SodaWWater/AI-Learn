---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DATA-GOVERNANCE
round: 4
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 数据治理（Data Governance）第四轮独立补漏

## 1. 独立检索设计

本轮按第三轮缺口使用 OpenLineage Specification（OpenLineage 规范）验证 RAG 派生资产映射，并从 Design-time Lineage（设计时血缘）与 Runtime Lineage（运行时血缘）的差异反查删除证明和版本审计。

| 检索族 | 查询或入口 | 独立性 |
|---|---|---|
| 对象模型（Object Model） | `OpenLineage Job Run Dataset input output facets object model 1.53` | 新标准来源族 |
| 生命周期（Lifecycle） | `OpenLineage Dataset lifecycleStateChange version facet drop overwrite rename truncate` | 从删除和版本状态反查 |
| 设计/运行冲突（Design/Runtime Conflict） | `DatasetEvent JobEvent not associated with Run versus RunEvent` | 主动寻找静态登记无法证明执行的边界 |
| 跨节点映射（Cross-stage Mapping） | `source document parse chunk embedding index lineage mapping` | 连接摄取、解析、切分、嵌入和索引 |

## 2. 来源处理

| 来源 ID | 状态 | 用途 |
|---|---|---|
| `openlineage-object-model-1-53-0` | `included` | Job/Run/Dataset（作业/运行/数据集）、输入输出、设计时事件、运行时事件、版本和生命周期 Facet（切面） |
| `gdpr-article-17-2026` | `included_existing` | 删除权适用条件与例外继续作为法律边界 |
| `spdx-3-1-rc-2026` | `included_existing` | 许可证表达继续作为来源属性，不替代许可判断 |

## 3. 新增类型与映射

| 类型 ID | 类别 | 内容 | 关系 |
|---|---|---|---|
| `GOV-K-401` | `knowledge` | DatasetEvent/JobEvent（数据集事件/作业事件）描述设计时元数据且不关联 Run（运行）；只有登记删除或新 Schema（模式）不能证明对应处理任务已经成功执行 | `new` |
| `GOV-P-401` | `problem_question` | 删除请求只把文档标为 `deleted`，但没有连接解析、Chunk（文本块）、Embedding（嵌入）、索引、缓存和备份的各次 Run（运行），无法证明派生对象是否全部处理 | `extends` |
| `GOV-P-402` | `problem_question` | 将每个 Chunk（文本块）直接建成独立 Dataset（数据集）会造成血缘高基数；只把整个知识库建成一个 Dataset（数据集）又无法定位单文档删除和权限传播 | `new` |
| `GOV-S-401` | `solution` | 建议把物理集合/索引建模为 Dataset（数据集），把文档与 Chunk（文本块）身份、版本和许可作为可扩展 Facet（切面）或受控外部实体引用；每个解析、嵌入、索引和删除操作建为可关联 Run（运行） | `new` |
| `GOV-E-401` | `evaluation` | 删除验证同时检查设计事件、运行事件、输入输出版本、失败 Run（运行）、重试和最终检索不可见；抽样回查引用和缓存是否仍暴露旧对象 | `extends` |

此映射是项目设计，不声称 OpenLineage（开放数据血缘）已经定义 RAG 专用 Chunk（文本块）或 Embedding（嵌入）实体。

## 4. 公开题与覆盖检查

未新增公开题。`RAG-SCENE-009/022` 已覆盖删除传播和企业多租户系统，但没有把论文或规范问题改写成真实面试题。九类覆盖中实现与解决方案已有标准对象入口；法律适用与产品备份擦除语义仍需按法域和供应商继续核验。

## 5. 冲突与边界

- Static Lineage（静态血缘）说明预期输入输出，Runtime Lineage（运行时血缘）说明发生过的观测；二者都不自动证明业务数据被物理删除。
- OpenLineage Facet（OpenLineage 切面）可扩展，不意味着任意自定义字段都被所有后端查询、保留或理解。
- 高基数和可定位性存在权衡；最终粒度要按数据量、审计问题和存储成本基准，而不是预设每个 Chunk（文本块）一条全局血缘节点。

## 6. 饱和判定与下一步

本轮新增知识类型 1、问题类型 1；连续无新增类型轮数保持 0，状态为 `round_complete`。下一轮把 RAG 血缘映射写成机器可读 Schema（模式），并用一次更新、一次删除和一次权限撤销生成完整事件样例验证。

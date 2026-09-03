---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DATA-GOVERNANCE
round: 3
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 数据治理（Data Governance）第三轮独立补漏

## 1. 本轮目标与边界

本轮从“能否证明一条知识如何产生、为何仍可被检索、是否已经删除”出发，专项检查 Provenance/Lineage（来源追踪/数据血缘）、Erasure（删除）、Accountability（可问责性）、Data Residency（数据驻留）和 License Metadata（许可证元数据）。法规来源只用于界定特定法域的原始要求，不把工程建议写成通用法律结论。

## 2. 实际检索式

| 编号 | 检索族 | 检索式 | 入口 |
|---|---|---|---|
| Q-301 | 数据血缘 | `site:w3.org/TR/prov-o entity activity agent derivation invalidation provenance` | W3C Recommendation |
| Q-302 | 删除与问责 | `site:eur-lex.europa.eu 32016R0679 Article 17 erasure accountability official` | EUR-Lex 欧盟官方法规 |
| Q-303 | 数据驻留 | `site:learn.microsoft.com Foundry deployment types global data zone regional data processing` | Microsoft Learn 官方文档 |
| Q-304 | 许可证表达 | `site:spdx.github.io/spdx-spec license expression AND OR WITH NOASSERTION` | SPDX 官方规范 |
| Q-305 | 公开题目 | `site:nowcoder.com 企业 RAG 多租户 数据隔离 合规 审计 面试` | 牛客公开页面 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 状态 | 理由 |
|---|---|---|---|
| `w3c-prov-o-2013` | 官方标准文档 | `included` | 提供 Entity/Activity/Agent（实体/活动/主体）、派生、修订和失效关系的可交换模型 |
| `eu-gdpr-official-2016` | 官方法规文本 | `included_bounded` | 补 Storage Limitation（存储限制）、Accountability（可问责性）、Article 17 Erasure（第 17 条删除权）及例外；仅用于欧盟场景 |
| `azure-foundry-deployment-types-2026` | 官方文档 | `included` | 明确 Global、Data Zone、Single Region（全球、数据区、单区域）处理位置的当前差异 |
| `spdx-license-expressions-3-1-rc1` | 官方候选规范 | `included_bounded` | 补机器可读许可证表达；RC 状态和软件许可证适用边界已标注 |
| `nowcoder-enterprise-rag-system-interview-2026` | 第一人称公开面经 | `existing_duplicate_type` | 多租户隔离和合规审计已登记为 `RAG-SCENE-022` |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 关联来源 | 与现有内容关系 |
|---|---|---|---|---|
| `GOV-K-301` | `knowledge` | Lineage（数据血缘）不是一个 source_url 字段，而是 Entity、Activity、Agent（实体、活动、主体）以及 used、wasGeneratedBy、wasDerivedFrom、wasRevisionOf、wasInvalidatedBy（使用、生成、派生、修订、失效）组成的可查询图 | `w3c-prov-o-2013` | `new` |
| `GOV-P-301` | `problem_question` | 源文档删除后，派生 Chunk（文本块）、Embedding（嵌入）、向量/倒排索引、缓存、评测集、日志和备份可能仍保留可恢复副本；删除成功必须按适用政策证明传播范围与残留状态 | `eu-gdpr-official-2016` 与血缘模型的工程推导 | `new` |
| `GOV-K-302` | `knowledge` | Data Residency（数据驻留）要分别描述静态存储位置和推理处理位置；Global、Data Zone、Single Region（全球、数据区、单区域）是不同处理边界，不能只看资源创建区域 | `azure-foundry-deployment-types-2026` | `new` |
| `GOV-I-301` | `implementation` | License Metadata（许可证元数据）至少区分可解析表达、`NONE`、`NOASSERTION` 和自定义 `LicenseRef`；能记录许可证不等于已经获得内容的 RAG 使用权 | `spdx-license-expressions-3-1-rc1` | `new` |
| `GOV-S-301` | `solution` | 删除工作流应使用可追踪 Tombstone（墓碑事件）或 Invalidation（失效事件）沿血缘图传播，并记录请求范围、依据、处理者、时间、派生对象状态、例外和验证结果 | W3C PROV-O 与 GDPR Accountability（可问责性）的工程推导 | `extends` |

## 5. 公开面试题来源核验

| 题目线索 ID | 自己的短转述 | 来源类型 | 原始定位 | 是否可声称真实面试 | 技术答案的一手核验来源 |
|---|---|---|---|---|---|
| `RAG-SCENE-022` | 大量企业租户的向量数据如何隔离、授权并保留合规审计？ | 第一人称面经（First-person Interview Report） | 牛客页面“追问 2：2000 家企业客户，数据隔离怎么做” | 只能声称发布者自述 | W3C PROV-O、适用法域原始法规、云服务数据处理位置和数据库权限官方文档 |
| `RAG-SCENE-008` | 生产 RAG 的敏感信息、权限、监控和增量索引如何统一治理？ | 公开题库（Public Question Bank） | 牛客公开题库 Q10 | 否 | 同上及既有 ACL/PII 官方资料 |
| `RAG-SCENE-009` | 更新和删除怎样保证索引一致性与回滚？ | 公开题库（Public Question Bank） | GitHub 公开题库 Naive RAG Q8 | 否 | GDPR 只在适用场景界定义务；工程实现另由血缘、CDC 和数据库官方资料核验 |

本轮未创建新 Scenario（场景题）：删除证明、数据驻留和许可证是现有综合题的新治理分支，不伪造成“真实面试问过”。

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理（Principle） | `covered` | 数据血缘图、删除/失效、存储限制、问责和处理位置已有原始来源 |
| 实现（Implementation） | `partial` | PROV-O 与 SPDX 提供表示；具体 Lineage Store（血缘存储）和删除编排框架仍需产品级文档 |
| 工程问题（Engineering Problem） | `covered` | 派生副本残留、跨域处理、许可未知、审计不可证明均已分型 |
| 解决方案（Solution） | `partial` | Tombstone（墓碑）、失效边和审计记录已有方案；备份擦除与法域例外需按场景设计 |
| 评估（Evaluation） | `partial` | 需建立删除覆盖率、权限泄露率、血缘完整率、驻留违规率和审计可复现率 |
| 公开面试题（Public Interview Question） | `covered` | `RAG-SCENE-008/009/022` 可定位；本轮没有新题型 |
| 时效（Freshness） | `covered` | 规范稳定来源与 2026-08 云部署文档组合；均于 2026-09-03 复核 |
| 安全或治理（Security or Governance） | `covered` | ACL、PII、来源、删除、驻留、许可和问责形成主干覆盖 |
| 跨节点关系（Cross-stage Relation） | `covered` | 覆盖摄取、切分、Embedding（嵌入）、存储、检索、引用和生产治理 |

## 7. 冲突、版本与未验证假设

- GDPR Article 17（《通用数据保护条例》第 17 条）存在适用条件和例外；“所有数据必须立即物理擦除”不是来源支持的通用结论。
- “删除证明”是由 Accountability（可问责性）、处理记录和派生链路共同得到的工程控制目标，不等同于法规中存在一个同名固定技术标准。
- 数据驻留能力按云、模型、部署类型和区域变化；正式内容必须携带审核日期，不把 Azure 结论推广到其他平台。
- SPDX 3.1 当前为 RC；且 SPDX License Expression（SPDX 许可证表达式）主要标准化表达，不判断某份内容能否用于检索、Embedding（嵌入）或生成。
- Content Deletion（内容删除）、Access Revocation（访问撤销）、Cryptographic Erasure（密码学擦除）和 Backup Expiration（备份过期）是不同状态，不能用一个布尔值替代。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 是 |
| 九类覆盖是否全部完成 | 否；实现、方案和评估仍为 `partial` |
| 一手资料缺口检查是否完成 | 是 |
| 公开面试题专项搜索是否完成 | 是 |
| 本轮新增知识/实现/解决类型数 | 4 |
| 本轮新增问题类型数 | 1 |
| 连续无新增类型轮数 | 0 |
| 未解决冲突是否已登记 | 是 |
| 当前结论 | `round_complete`，不得标记 `coverage_saturated` |

## 9. 下一轮动作

- 补 OpenLineage（开放数据血缘）或同类实现规范，验证 RAG 派生对象怎样映射到 Job/Run/Dataset（作业/运行/数据集）；
- 补备份、密钥销毁、日志保留和删除验证的官方产品语义；
- 分法域建立“适用条件—控制目标—技术实现—证据”映射，不提供脱离场景的法律结论；
- 用不同来源继续搜索治理型公开面试题；若下一轮无新增，连续无新增计数才变为 1。

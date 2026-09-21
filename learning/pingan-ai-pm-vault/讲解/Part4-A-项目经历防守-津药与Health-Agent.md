---
id: PINGAN-AI-PM-PART4-A
title: Part4-A 项目经历防守：津药采购分析自动化 + Personal Health Agent
status: interview_defense_draft
updated: 2026-09-17
purpose: 深圳平安科技 AI / 大模型产品经理最终面试防守
---

# Part4-A 项目经历防守：津药采购分析自动化 + Personal Health Agent

> 这份材料不是让你背两段“项目介绍”。真正目标是：**让面试官无论从业务、产品、AI、数据、Agent、RAG、Tool、权限、可靠性还是复盘角度追问，你都知道这个问题为什么存在、当时为什么这样设计、替代方案是什么、边界在哪里。**
>
> 两个项目承担不同证明责任：
>
> - **津药项目**：证明你能进入真实企业业务流程，理解脏数据、人工流程、系统边界和落地问题；
> - **Personal Health Agent**：证明你不仅会调用模型，而是理解 Agent、RAG、Tool、权限、状态、可靠性和 Evaluation 如何组合成一个 AI 产品。
>
> 它们合在一起形成的不是“我做过两个项目”，而是：
>
> **我有软件工程技术底座，也真正进入过企业业务；我会先把业务流程和数据问题搞清楚，再判断哪些步骤适合 AI、哪些必须交给确定性系统，并考虑权限、证据、错误处理和评估，而不是把所有问题都包装成一个聊天机器人。**

---

# 一、先建立项目面试的统一思维

面试官问“介绍一下你的项目”，真正想判断的通常不只是“你做了什么功能”。他会逐渐确认五件事：

```text
1. 你是不是真的理解业务？
2. 这个问题是不是真的存在？
3. 为什么要这样设计，而不是别的方法？
4. 你到底亲自思考和推动了什么？
5. 如果系统出错、规模变大、进入真实生产，你知道问题在哪里吗？
```

所以项目讲解最好始终沿着：

```text
真实业务
↓
原流程
↓
真正痛点
↓
问题拆解
↓
方案选择
↓
AI / 非AI边界
↓
系统执行链
↓
可靠性
↓
效果验证
↓
不足与下一步
```

而不是先列：

```text
用了 LangGraph
用了 RAG
用了 pgvector
用了大模型
```

技术名词应该在“为什么需要它”之后出现，而不是在业务问题之前出现。

---

# 二、两个项目之间为什么不是割裂的

表面上，一个是企业采购分析，一个是个人健康 AI，看起来跨度很大。但真正的方法论是一致的：

```text
现实世界信息很乱
↓
先整理数据和业务边界
↓
把确定性问题和不确定性问题分开
↓
确定性问题交给程序 / 数据系统
↓
语言理解、信息组织、动态判断交给 LLM / Agent
↓
所有重要结果考虑来源、权限、错误和人工确认
```

这会成为你整场面试非常重要的一条主线。

---

# 三、津药项目：先从真实业务讲，而不是先说 AI

## 3.1 这个项目真正是什么

你的实习场景不是“我做了一个采购 AI Agent”。更准确的说法是：

> **企业采购数据分析流程自动化和智能化改造。**

原始工作链大致属于：

```text
ERP / SRM 等业务系统
↓
下载不同底表
↓
Excel 清洗
↓
字段映射
↓
修正异常数据
↓
透视 / 聚合
↓
形成不同分析视角
↓
人工解读
↓
报告 / 看板
```

这是很典型的企业数字化问题。很多公司并不是“没有系统”，而是“系统很多，但数据不能直接用于管理分析”。

ERP、SRM 最初主要服务的是：

```text
业务录入
流程审批
订单 / 合同 / 采购执行
```

它们不一定天然按照：

```text
跨组织比较
跨年度分析
统一管理口径
AI 使用
```

来设计数据。

所以真实痛点往往不是“没有数据”，而是：

```text
数据分散
字段名称不同
口径不同
粒度不同
历史规则不同
还有人工修正
```

这就是这个项目最有价值的业务起点。

---

# 四、为什么 RPA 并没有解决整个问题

你的前任流程已经用影刀 RPA 帮忙从系统下载数据。这个事实反而让你的项目更真实，因为它说明企业已经自动化了第一层：

```text
“重复点击网页、登录、下载文件”
```

RPA 擅长的是：

```text
登录系统
点击菜单
下载文件
上传文件
按固定步骤操作
```

但下载完成以后，真正分析工作才开始：

```text
文件 A
文件 B
文件 C
文件 D
↓
这些字段怎么对应？
金额口径一样吗？
同一供应商有没有多个名称？
哪些异常是数据问题，哪些是业务事实？
管理者到底想看什么？
```

所以 RPA 主要解决：

> **Process Automation，流程操作自动化。**

而你继续往下处理的是：

> **Data / Decision Automation，数据处理和分析决策辅助。**

这两层不能混为一谈。

---

# 五、第一层核心问题其实是数据治理，不是大模型

假设不同系统导出的采购数据：

```text
表A：供应商名称
表B：供应商简称
表C：合作方
表D：供应商编码
```

业务人员知道它们可能表达同一个概念，但程序不知道。

再比如：

```text
含税金额
未税金额
订单金额
入库金额
结算金额
```

它们都可能被粗略叫成“金额”，但业务意义完全不同。

如果直接把这些表扔给 LLM，让它“分析采购情况”，模型即使语言能力很好，也不知道企业内部真正认可的业务口径是什么。

所以你先做的是：

```text
Field Mapping
Business Definition
Canonical Schema
```

这个顺序非常重要：

> **先把数据的“事实语言”统一，再让 AI 使用。**

---

# 六、Canonical Schema 是什么

这个词不要觉得太技术。它实际上就是：

> **先规定一套统一语言，让所有来源最终都翻译成这套语言。**

例如统一成：

```text
enterprise_id
enterprise_name
supplier_id
supplier_name
material_code
material_name
purchase_date
quantity
unit_price
amount
source_system
```

不同源：

```text
ERP A
ERP B
SRM C
```

都先经过：

```text
Adapter / Mapping
```

转成统一格式。

可以理解成：

```text
不同地方的人讲不同方言
↓
先翻译成普通话
↓
再讨论同一个问题
```

这就是“统一数据模型”的产品意义。

---

# 七、Adapter Layer 为什么重要

如果系统 A 某天把字段改名，没有 Adapter 的系统可能导致后续很多分析代码一起改。

有 Adapter 以后：

```text
Source A
↓
Adapter A
↓
Canonical Schema
↓
后面的分析逻辑保持稳定
```

新增系统 E 时，也优先增加：

```text
Adapter E
```

而不是推翻整个分析系统。

从产品视角，这叫：

> **把“来源变化”隔离在接入层，让核心分析能力稳定复用。**

这比“我做了字段清洗”表达得更完整。

---

# 八、为什么 AI 不是用来算采购金额的

这是津药项目最值得防守的一点。

假设：

```text
单价 23.7
数量 1876
```

或者企业已经有明确金额字段。

这种问题有三个特点：

```text
确定公式
唯一结果
必须可复现
```

所以更适合：

```text
Python / SQL / Excel Engine
```

而不是让 LLM 自由计算。

原因不是“LLM 完全不会算术”，而是企业要求：

```text
同样输入
→ 必须得到同样输出
→ 能复算
→ 能审计
→ 能 Debug
```

于是形成一条很重要的 AI 产品原则：

```text
LLM
负责不确定性的理解与表达

Deterministic Tool
负责确定性的计算与规则
```

这条原则后面可以直接迁移到金融。

---

# 九、那为什么还需要 LLM？

如果整个需求永远只有固定报表、固定字段、固定指标，那么 BI + Python + RPA 完全可以，不应该为了 AI 而 AI。

LLM 真正有价值的地方，是原流程里仍然存在大量：

```text
自然语言需求理解
分析模块选择
非结构化解释
报告生成
```

例如用户说：

> “帮我看看今年哪些供应商采购额特别集中，有没有需要关注的？”

这句话包含：

```text
时间范围
分析对象
分析意图
分析维度
输出目标
```

LLM 可以把它先理解成结构化任务，例如：

```json
{
  "analysis_type": "supplier_concentration",
  "period": "current_year",
  "scope": "all_suppliers"
}
```

然后真正计算交给分析 Tool，最后再由 LLM 将结果解释成人能读懂的文字。

所以 AI 的合理位置不是“替代整个分析系统”，而是：

```text
入口：理解人说的话
中间：选择已有能力
出口：解释计算结果
```

---

# 十、津药项目的完整执行链

可以把你的设计思维理解成：

```text
用户需求
↓
LLM 理解任务
↓
结构化任务参数
↓
参数校验
↓
调用分析 Tool
↓
Python / Data Pipeline
↓
统一数据模型
↓
确定性计算
↓
Structured Result
↓
LLM 解释
↓
报告 / 看板
```

核心边界：

```text
LLM 不定义正式业务口径
LLM 不自由计算核心指标
LLM 不直接修改正式底表
```

它主要负责语言理解和结果解释。

---

# 十一、Structured Output 到底有什么用

如果 LLM 只输出：

> “我觉得应该分析供应商。”

后端程序很难可靠执行。

如果输出：

```json
{
  "analysis_type": "supplier_analysis",
  "period": "2026Q2",
  "dimension": "supplier"
}
```

后端就可以校验并执行。

所以 Structured Output 可以通俗理解为：

> **让 LLM 按照程序约定的数据合同说话。**

它把：

```text
自然语言
```

和：

```text
传统软件系统
```

真正接起来。

---

# 十二、Tool Calling 在这里的本质

Tool Calling 不是“让模型直接执行 Python”。

更准确是：

```text
LLM 判断：
当前需要哪项能力？
需要哪些参数？
```

然后后端收到 Tool Call：

```text
参数检查
↓
权限 / 业务检查
↓
真正执行 Python
↓
返回结构化结果
↓
LLM 再解释
```

所以：

```text
LLM = 决策和表达层
Tool = 能力执行层
```

这就是你后面所有 Agent 场景可以复用的基本思想。

---

# 十三、数据异常为什么不能都让 AI 自动修

企业数据一定会有：

```text
空值
别名
错误编码
重复记录
金额异常
业务特殊情况
```

危险设计是：

```text
LLM 看见异常
↓
猜一个“看起来合理”的值
↓
直接改正式数据
```

错误很可能被“修得很自然”，反而更难被发现。

更稳妥的是：

```text
规则可确定
→ 自动修

映射表可确定
→ 自动映射

无法确定
→ 标记异常

业务人员确认
→ 再更新规则 / 映射
```

AI 可以建议，但不能把“推测”直接升级成“正式事实”。

这就是 Human-in-the-loop 在企业数据里的朴素版本。

---

# 十四、这个项目真正带来的产品价值

不要只说“提升效率”。真正价值可以拆成：

```text
效率
→ 减少重复下载、清洗、透视等机械操作

一致性
→ 同一指标统一口径计算

可复用性
→ 不同企业 / 来源共享统一分析框架

可扩展性
→ 新增来源或分析模块不用推翻系统

可解释性
→ AI 的文字解释建立在真实计算结果上
```

如果没有正式统计，不要现场编：

```text
效率提升 80%
成本下降 60%
```

更成熟的说法是：

> 我会用单次处理时长、人工步骤数、返工次数、交付周期以及错误率做前后对比；如果没有长期正式数据，我不会把估算值包装成验证结论。

---

# 十五、津药项目最容易被追问的核心点

### 为什么不用纯 BI？

本质是在问 AI 是否真的必要。

回答思路：

> 固定指标、固定分析完全适合 BI；LLM 的增量价值主要在自然语言需求理解、动态分析路由和结果解释。

### 为什么不用纯 RPA？

本质是在问 RPA 和 AI 的边界。

回答思路：

> RPA 自动化固定操作路径，但不能解决跨系统数据语义、业务口径和动态分析需求。

### 为什么不全部让 LLM 做？

本质是在问你是否理解 LLM 的可靠性边界。

回答思路：

> 核心金额、聚合、Join、字段映射、正式数据修改都应由可验证程序控制。

### LLM 如果理解错需求怎么办？

本质是在问可靠性。

回答思路：

```text
Structured Output
Schema Validation
Business Validation
异常时 Clarify / Human Review
```

---

# 十六、如果重做津药项目，下一步怎么升级

不要只说“换更强模型”。

更成熟的升级顺序：

```text
1. 正式化统一数据契约和版本
2. 把映射、异常、业务规则从脚本沉淀为可配置规则
3. 每个分析 Tool 建独立测试和数据质量检查
4. 建任务级 Eval：意图路由、参数、计算一致性、事实一致性
5. 做真正工作台：让用户看到数据来源、异常、计算口径和 AI 解释
```

这代表从“自动化脚本”往“企业 AI 产品”演进。

---

# 十七、进入 Personal Health Agent：不要先说 LangGraph

这个项目真正的问题不是“我想做个 Agent”。

而是：

> **个人健康数据是长期的、异构的、有来源要求的，而且 AI 生成内容不能未经确认就变成正式健康事实。**

当前仓库公开边界很明确：

```text
本地优先
个人健康记录与循证辅助
来源追溯
版本化记录
明确确认
```

同时明确：

```text
不是医疗器械
不提供诊断或处方
使用合成数据
```

这些边界面试时一定要守住。

---

# 十八、为什么普通 Chatbot 不够

普通 Chatbot：

```text
用户问
↓
LLM 回答
```

适合一次性对话。

但真实长期健康场景可能是：

```text
用户上传历史报告
↓
记录指标
↓
一个月后新增数据
↓
问半年趋势
↓
生成周期报告
↓
追问报告依据
```

这已经需要：

```text
长期数据
状态
检索
工具
任务
权限
来源
```

所以产品从：

```text
Question → Answer
```

变成：

```text
User Goal
↓
读取状态和正式记录
↓
决定需要哪些 Evidence / Tool
↓
调用能力
↓
组织结果
↓
保存任务状态
↓
后续继续
```

这就是 Agent / Workflow 开始有价值的原因。

---

# 十九、为什么不是所有流程都交给 Agent

例如：

```text
创建记录
↓
字段校验
↓
用户确认
↓
正式提交
```

这应该是固定 Workflow。

因为每一步业务责任非常明确，不需要 LLM 自由决定。

但用户问：

> “结合最近几个月的数据，帮我看看有什么变化，并告诉我依据。”

系统可能动态决定：

```text
先查哪些指标
是否需要历史记录
是否需要读取报告
证据是否足够
是否继续补充 Tool
```

这种局部分析过程才适合 Agent。

所以真实架构思想是：

> **确定流程用 Workflow，只有需要动态理解、选择 Tool、补证和调整路径的局部环节才引入 Agent。**

---

# 二十、Health Agent 的系统架构怎么通俗理解

当前仓库公开架构是：

```text
React
↓
FastAPI
↓
PostgreSQL 17 + pgvector
↓
Redis / Celery
↓
MinIO

同时存在：
LangGraph Checkpoints
```

逐个理解它们为什么存在。

## FastAPI

后端应用入口，负责：

```text
API
业务流程
身份 / 权限边界
调用服务
```

## PostgreSQL

项目把它当作：

```text
System of Record
```

通俗讲：

> **真正算数的正式业务数据最终以数据库为准。**

当前架构文档明确：PostgreSQL 保存 domain data、task state、outbox rows、ledgers、durable events、LangGraph checkpoints。

## pgvector

在 PostgreSQL 中提供向量检索能力。

所以项目不需要为了 RAG 必然再部署一个独立 Vector DB。

## Redis

当前架构中主要是 Broker / Notification Transport，而不是恢复真相源。

通俗讲：

> 它负责告诉 Worker“有任务来了”，但正式业务事实仍以持久数据库为准。

## Celery

执行异步任务，例如文件导入、报告生成、批处理。

为什么要异步？因为这些任务可能慢、可能失败、可能需要重试，不适合让一个 HTTP 请求一直等。

## MinIO

保存文件和 Artifact 这类对象数据。

## LangGraph Checkpoint

保存 Graph / Agent 执行状态，使长任务可以持久化和恢复，而不是中断后全部从头开始。

---

# 二十一、State、Checkpoint、Domain Data、Conversation 不要混

假设用户要求生成一份健康报告。

### Domain Data

```text
用户正式健康记录
```

回答的是：

> 用户真实保存了什么。

### Agent State

```text
当前任务已经做到哪里
当前有哪些中间结果
下一步要做什么
```

回答的是：

> Agent 现在处于什么执行状态。

### Checkpoint

是 Agent State 的持久化快照。

回答的是：

> 如果任务中断，从哪里恢复。

### Conversation

记录用户和助手说过什么。

这些可以相互关联，但职责不同。

成熟 Agent 系统不会把所有信息都只塞进 `messages[]`。

---

# 二十二、为什么健康数据需要版本化

当前项目的表单和指标定义是版本化的。

假设今天表单：

```text
睡眠时长
体重
静息心率
```

半年后改为：

```text
睡眠时长
睡眠质量
体重
静息心率
```

如果只保留最新表单，以后看半年前记录时就不清楚：

> 当时这条数据到底是按照哪个结构提交的？

所以需要：

```text
Form Definition Version
+
Submission
```

这叫 Versioned Data Contract。

它的意义不是复杂，而是让历史事实仍然可解释。

---

# 二十三、为什么是“草稿 → 确认 → 正式记录”

当前公开 README 的正式流程包含：

```text
选择版本化表单
↓
创建并校验草稿
↓
确认提交
↓
不可变正式记录
```

如果 AI 从上传文件里识别出一个指标，不能马上写入正式健康档案，因为：

```text
OCR 可能错
抽取可能错
语义理解可能错
```

因此先进入 Draft，让用户确认，再形成 Formal Record。

这体现一个非常重要的高风险产品原则：

> **AI 建议 ≠ 正式事实。**

这个思想可以直接迁移到金融尽调、合同审核和任何正式业务记录场景。

---

# 二十四、Tool Gateway 为什么比 Agent 直接连数据库更合理

当前架构明确：

```text
Agent Tools
↓
Tool Gateway
↓
Authorization Envelope
```

而不是：

```text
Agent
↓
Raw Database Session
```

最通俗的理解：

> **Agent 不应该拿数据库万能钥匙。**

它应该只看到明确能力，比如：

```text
读取某类记录
查询某个报告来源
检索某个 Evidence
```

每次调用还必须带：

```text
谁在调用
属于哪个 workspace
当前允许访问什么
当前任务范围是什么
```

Authorization Envelope 可以理解成：

> **每次工具调用外面都包着一层真实身份和权限上下文。**

---

# 二十五、为什么 Prompt 不能承担权限控制

不能只写：

```text
System Prompt:
“不要访问其他用户的数据。”
```

Prompt 是软约束，是给模型的行为指导。

真正权限必须在 Runtime / Tool 层：

```text
User A
↓
Tool Gateway
↓
只允许 Workspace A
```

即使模型错误生成了 B 的 ID，后端仍然应该拒绝。

这就是：

```text
Soft Constraint
vs
Hard Constraint
```

这在金融 Agent 里尤其重要。

---

# 二十六、RAG 在 Health Agent 里真正解决什么

RAG 不应该被理解成“把所有健康数据都向量化”。

它更适合：

```text
非结构化历史材料
报告
知识证据
长期文档
```

如果是确定性结构化指标，更适合直接走数据库 / Tool。

用户问：

> “你为什么说最近某个趋势有变化？”

系统真正需要的不只是文字回答，还要：

```text
Claim
+
Evidence
```

所以 RAG 的目标不是“找相似文本”，而是：

> **找到能支撑回答的证据。**

---

# 二十七、为什么 Retrieval 要版本化

项目已经设计了：

```text
immutable generation
publish
rollback
revoke
run-pinned retrieval version
```

通俗讲，知识库今天可能是 Version 7，明天更新成 Version 8。

如果一个 Agent Run 开始时使用 v7，执行到一半切到 v8，那么同一个任务前后可能基于不同事实集合。

所以：

```text
Run starts
↓
pin retrieval generation = v7
↓
整个 Run 都查 v7
```

这就是 `run-pinned retrieval version`。

它保证：

> **同一次任务内部使用同一知识快照。**

---

# 二十八、Publish / Rollback / Revoke 怎么理解

### Publish

新知识版本验证完成，正式成为可用版本。

### Rollback

新版有问题，恢复到之前稳定版本。

### Revoke

某份知识或某个版本不应该再被使用，明确撤销。

它们共同说明：

> **企业知识库不是静态文件夹，而是有发布生命周期的数据产品。**

---

# 二十九、Citation 为什么是产品能力

如果系统回答：

> “最近某个指标有变化。”

用户应该能够继续问：

> “依据是什么？”

理想链路：

```text
Claim
↓
Citation
↓
Source
↓
具体记录 / 文件 / Chunk
```

Citation 的价值不是“看起来专业”，而是：

```text
用户可核验
降低盲目信任
人工复核更快
发生错误时可 Debug
```

所以 Citation 本身就是可靠性 UX。

---

# 三十、Health Agent 的幻觉治理不是“加 RAG”

真正是多层：

```text
知识版本
↓
Evidence Retrieval
↓
Tool 获取确定事实
↓
Citation
↓
Structured Output
↓
权限
↓
明确确认
↓
No-answer / Fail-closed
↓
Eval
```

而仓库边界明确：

```text
AI 输出只提供上下文辅助
不构成医疗诊断或治疗建议
```

这本身就是 Product Boundary，也是风险治理的一部分。

---

# 三十一、Fail-closed 是什么意思

当前仓库公开架构说明外部健康数据 Provider 默认关闭，并采用 fail-closed。

最通俗的理解：

> **如果系统无法确认当前状态是安全、被授权的，就默认不允许继续。**

相反，fail-open 是：

> 检查出错也先放行。

在权限、隐私、高风险 Tool 中，fail-closed 通常更符合安全设计。

---

# 三十二、为什么需要异步任务

报告生成、文件导入等任务可能需要较长时间。

如果全部让 HTTP 请求一直等待，会带来：

```text
请求超时
连接长期占用
失败难恢复
```

因此更合理：

```text
API 接受任务
↓
记录 Task
↓
进入 Queue
↓
Worker 执行
↓
持久化结果
↓
前端通过查询 / SSE 获得状态
```

这就是异步任务系统。

---

# 三十三、Outbox 是什么

这是后端可靠性里的真实经典问题。

假设：

```text
数据库已经写成功
```

但：

```text
发送任务消息失败
```

那么会出现：

```text
数据库认为任务存在
Worker 却永远不知道
```

Outbox Pattern 的思路是：

```text
业务记录
+
待发送事件
```

先放进同一个可靠数据库事务。

再由 Publisher：

```text
读取 Outbox
↓
发消息
↓
标记已发送
```

它降低的是：

```text
数据库状态
和
消息系统状态
```

不一致的问题。

它不是 AI 专属技术，但长任务 Agent 同样需要。

---

# 三十四、Ledger / Idempotency 为什么重要

异步消息可能重复投递。

例如：

```text
Worker 已经执行成功
但 ACK 丢失
↓
Broker 再次投递
```

如果任务涉及正式记录、通知、删除等副作用，重复执行可能出问题。

所以要考虑 Idempotency：

> **同一个逻辑操作即使被重试，也不能把业务结果重复放大。**

Ledger 可以记录：

```text
operation 是否执行过
执行结果是什么
```

重试前先查账。

---

# 三十五、Lease / Epoch Fencing 怎么理解

这是较深的技术追问，不需要主动讲，但理解以后你会更稳。

假设：

```text
Worker A 拿到任务
↓
执行很久
↓
系统以为 A 挂了
↓
Worker B 接管
```

但 A 实际没死，又继续执行，于是 A、B 都认为自己拥有任务。

Lease 可以理解为：

> **任务所有权只有一段有效时间。**

Epoch / Fencing Token 可以理解为：

> **每次新接管都会换一张更高版本的门禁卡。**

例如：

```text
A epoch=4
B 接管 epoch=5
```

以后 A 用 epoch=4 提交，系统发现已经过期，直接拒绝。

这就是 Fencing。

---

# 三十六、为什么这些后端技术和 Agent 有关系

因为 Agent 不再只是一次短请求。

它可能：

```text
执行长任务
等待外部 Tool
异步运行
被中断
重试
恢复
```

所以传统分布式系统里的：

```text
Idempotency
Lease
Checkpoint
Recovery
```

都会重新进入 Agent 工程。

这也是你的项目比普通“LangChain Demo”更值得讲的地方：

> **你开始考虑 AI 任务失败以后怎么恢复、重复以后怎么不产生错误副作用，而不是只考虑一次正常路径。**

---

# 三十七、Health Agent 的 Evaluation 不是只测“准确率”

当前仓库评估方法明确分成：

```text
Scheduling
Recovery
Tool Security
RAG
```

其中 RAG 公开指标包括：

```text
Recall@5
MRR@5
Citation correctness
No-answer precision / recall / F1
Generation mismatch
Withdrawn leaks
Cross-workspace private hits
Missing-license publication
```

这套指标很值得防守，因为它说明 Eval 是系统性的。

---

# 三十八、为什么 No-answer 要单独评估

健康问答中有些问题系统没有足够 Evidence。

正确行为应该是：

```text
明确证据不足
```

而不是猜。

但如果系统什么都拒绝，又没有产品价值。

所以要同时测试：

```text
该拒答时能不能拒答
不该拒答时能不能正常回答
```

这就是 No-answer precision / recall / F1 的意义。

---

# 三十九、Cross-workspace private hit 是什么

假设：

```text
Workspace A
Workspace B
```

A 用户做 RAG 时，即使 B 的 Chunk 语义非常相关，也绝对不能被召回。

所以测试：

```text
cross-workspace private hits
```

本质不是普通检索准确率，而是：

```text
Privacy / Authorization Eval
```

这体现“检索系统也必须遵守权限”。

---

# 四十、为什么不能把本地评估包装成生产 SLA

当前仓库明确把证据边界限定为：

```text
本地可复现
合成 workspace
Deterministic / Mock Provider
真实 PostgreSQL / Redis-Celery / LangGraph / Tool Gateway / Retrieval 路径
```

但它不代表：

```text
真实生产用户规模
真实模型容量
医疗正确性
生产 SLA
真实健康结局
```

所以如果面试官问“是不是生产级”，更成熟的回答是：

> 我的目标是用生产系统思路把权限、恢复、版本和 Eval 机制做完整，但当前仓库明确是本地可复现工程项目，使用合成数据和受控 Provider，所以我不会把本地性能结论外推成真实医疗生产 SLA。

这是 Evidence Boundary 意识，不是示弱。

---

# 四十一、两个项目放在一起，面试官最终应该看到什么

津药证明：

```text
真实企业业务
↓
流程与数据口径
↓
确定性计算边界
↓
AI 应该放在哪
```

Health Agent 证明：

```text
进一步把这些思想工程化
↓
Agent
RAG
Tool
State
Permission
Reliability
Eval
```

所以这两个项目可以形成一条成长路径：

```text
企业真实业务
↓
发现 AI 落地首先是数据与流程问题
↓
进一步学习 Agent 系统设计
↓
开始关注权限、可靠性、证据和 Evaluation
```

这就是很合理的 AI 产品经理成长叙事。

---

# 四十二、把前面学的知识全部挂回项目

| 知识 | 津药 | Health Agent |
|---|---|---|
| Workflow | 固定数据处理链 | 记录/报告等固定流程 |
| Agent | 任务理解与模块选择可局部引入 | 动态查证与工具调用 |
| Structured Output | 分析参数 / 结果契约 | Agent / Tool 数据合同 |
| Tool Calling | 调 Python 分析模块 | Tool Gateway |
| RAG | 非核心 | Evidence Retrieval |
| Chunk / Retrieval | 非核心 | 文档证据处理 |
| Citation | 结果需追溯到底层数据 | 明确的来源与引用机制 |
| State | 普通任务执行状态 | LangGraph Checkpoint / Task State |
| Memory | 非核心 | 持久会话与长期上下文 |
| Permission | 企业系统账号边界 | Workspace / Tool Authorization |
| Hallucination | 核心数字不交给 LLM | Grounding + Citation + Boundary |
| HITL | 异常数据人工确认 | 正式记录 / 风险动作明确确认 |
| Eval | 计算一致性 / 效率 | RAG / Tool Security / Recovery |
| Reliability | 自动化失败处理 | Outbox / Ledger / Lease / Recovery |

这个表不是用来背，而是让技术问题随时能挂回真实项目。

---

# 四十三、两个项目都要主动守住的“不要夸大”

## 津药不要说

```text
“我负责集团 AI 平台”
“上线完整企业 Agent”
“模型自动做采购决策”
```

除非事实真的如此。

更准确：

```text
真实企业采购数据分析自动化
+
AI 能力探索 / 结构化任务理解
+
确定性分析 Tool
```

## Health Agent 不要说

```text
“用于真实患者”
“医疗诊断 Agent”
“达到生产医疗 SLA”
“已接入真实外部医疗系统”
```

当前仓库明确不是这些。

应该说：

```text
本地可复现个人健康 Agent 工程
使用合成数据
强调来源、权限、恢复和 Eval
不提供诊断和处方
```

---

# 四十四、如果面试官问：“你最有代表性的 AI 产品思考是什么？”

可以把两个项目共同收束为：

> 我最大的一个认识是，企业 AI 落地不是把整个业务流程都交给大模型。真正可靠的方案应该先把业务事实、数据口径和权限边界定义清楚，再把确定性的计算和规则交给传统系统，把语言理解、非结构化信息处理、动态工具选择和解释生成交给模型。对于高风险结果，还需要 Citation、Validator、人工确认和 Eval。津药项目让我先理解了“AI 和确定性系统的边界”，Health Agent 则让我进一步把这件事落实到 Agent、Tool Gateway、RAG、权限和可靠性架构里。

这不是要求逐字背，而是你整个 Part4-A 的中心思想。

---

# 四十五、如果面试官说：“这不就是工程设计吗，产品经理为什么要懂？”

AI 产品和传统产品有一个很现实的差别。

传统软件很多需求可以写成：

```text
点击按钮
↓
固定后端逻辑
↓
固定结果
```

AI 产品却天然存在：

```text
概率输出
Context
Prompt
Tool
RAG
Model
Retry
Fallback
```

如果产品经理完全不理解这些，就很难定义：

```text
什么能做
什么不能做
怎么失败
什么时候人工介入
如何验收
成本是多少
延迟是多少
```

所以你学习技术架构，不是为了替工程师写所有代码，而是为了：

> **把业务需求翻译成一个现实可实现、可验收、风险边界清楚的 AI 产品方案，并能和算法、后端、数据团队讨论同一件事。**

这就是你的软件工程背景转向 AI 产品经理时真正的优势。

---

# 四十六、最终项目防守心智

## 津药

不要背：

```text
RPA
Excel
LLM
Python
```

而要记：

```text
真实采购流程
↓
自动下载只是第一步
↓
真正难点是数据口径和重复分析
↓
先统一数据模型
↓
确定性计算程序化
↓
LLM 做理解与解释
↓
异常保留人工确认
↓
目标是稳定、可复用、可追溯
```

## Health Agent

不要背：

```text
LangGraph
FastAPI
pgvector
Celery
```

而要记：

```text
长期健康信息天然需要记录、证据和状态
↓
固定流程用 Workflow
动态查证用 Agent
↓
正式事实和 AI 建议分离
↓
RAG 提供 Evidence
↓
Tool Gateway 控权限
↓
Checkpoint / Outbox / Ledger 保可靠
↓
Citation / No-answer / Eval 控错误
↓
整个项目明确不越过医疗诊断边界
```

---

# 四十七、Part4-A 一句话总复盘

> **津药项目体现的是“如何把 AI 放进真实企业业务”；Health Agent 体现的是“如何把 AI 做成一个有状态、有工具、有证据、有权限、有失败恢复和评估机制的系统”。两者共同证明的不是我会几个框架，而是我开始具备从业务问题、数据事实、AI 能力到系统落地边界完整思考产品的能力。**

---

# 附：Personal Health Agent 当前公开事实边界

本文对 Health Agent 的描述依据当前仓库公开信息，以下事实应保持一致：

```text
- Local-first personal health record / evidence assistance
- 使用合成数据
- 不是医疗器械
- 不提供诊断或处方
- React + FastAPI
- PostgreSQL 17 + pgvector
- Redis + Celery
- MinIO
- LangGraph checkpoints
- persistent conversations
- tool authorization envelope
- event replay
- citation
- controlled provider
- versioned forms / records
- source traceability
- explicit confirmation
- external health-data providers fail-closed
```

仓库：

https://github.com/SodaWWater/personal-health-agent

重点文档：

```text
README.md
docs/architecture.md
docs/evidence/evaluation-methodology.md
docs/security.md
docs/privacy.md
```

当前 Evaluation Methodology 公开记录的 RAG 验证项包括：

```text
Recall@5
MRR@5
Citation correctness
No-answer precision / recall / F1
Generation mismatch
Withdrawn leaks
Cross-workspace private hits
Missing-license publication
```

同时仓库明确限定：

```text
本地可复现工程结果
不能直接等同于：
生产用户表现
生产 SLA
医疗正确性
真实健康结局
```

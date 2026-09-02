# AI-Learn 项目整体规划

> 文档状态：`approved_direction / execution_ready`  
> 当前试点：检索增强生成（Retrieval-Augmented Generation，RAG）  
> 更新日期：2026-09-02  
> 权威性：本文件是项目范围、产出结构、执行顺序和验收口径的主规划。其他文件与本规划冲突时，应先修正文档冲突，再继续生产内容。

## 1. 项目背景

现有人工智能（Artificial Intelligence，AI）学习资料和面试资料普遍存在以下问题：

1. 同一知识点在不同题目和仓库中反复出现；
2. 相似题目包含不同条件、实现和反例，简单去重会丢失信息；
3. 单道题能够看懂，但题目之间缺乏清晰的系统位置和关系；
4. 纯知识分类便于查阅，却不适合通过工程问题快速建立完整理解；
5. 技术术语翻译不统一，容易偏离国内工程语境；
6. 原理讲解和实际开发实现分离，学习者知道“是什么”，却不知道“在项目哪里使用”；
7. 面试题、工程问题、解决方案、具体技术和评估方法没有形成可跳转网络；
8. 框架接口、模型、产品能力和高级范式变化快，资料容易过时。

本项目不建设一个简单的文章收藏夹，也不把不同仓库全文拼接起来。项目要建立一套来源可追踪、知识可审计、关系可计算、问题可定位、内容可持续更新的人工智能学习知识库（AI Learning Knowledge Base）。

## 2. 项目愿景

最终形成：

> 一套可以沿完整技术流程学习、沿工程问题定位、沿面试题复习、沿技术节点深入、沿来源证据核验的人工智能知识网络（AI Knowledge Network）。

检索增强生成（Retrieval-Augmented Generation，RAG）是第一套端到端试点。试点完成后，同一生产方法扩展到：

- 大语言模型（Large Language Model，LLM）基础；
- 提示工程（Prompt Engineering）；
- 智能体（Agent）；
- 多智能体系统（Multi-Agent System）；
- 工具调用（Tool Calling）；
- 模型上下文协议（Model Context Protocol，MCP）等协议；
- 向量数据库（Vector Database）；
- 评估（Evaluation）；
- 人工智能应用工程（AI Application Engineering）。

## 3. 核心目标

### 3.1 完整性目标

- 对登记来源进行全量盘点，而不是抽样整理；
- 只合并语义、条件和结论均等价的信息；
- 实现、补充、反例、版本差异、冲突和不同业务条件不得作为重复内容删除；
- 针对每个流程节点继续检索公开面试题、工程资料、一手论文和官方文档；
- 建立来源到知识、知识到来源的双向映射；
- 建立问题到节点、节点到问题的多对多映射；
- 用版本化覆盖矩阵（Coverage Matrix）说明“当前资料覆盖了什么”，不使用无法证明的“永久绝对完整”。

### 3.2 学习目标

- 学习者先理解当前完整的检索增强生成流程（RAG Workflow）；
- 学习者可以沿流程节点依次学习工程问题/面试题（Engineering Problem / Interview Question）；
- 学习者遇到不熟悉的技术时，可跳转到详细知识节点；
- 学习者完成节点题后，再进入跨节点综合问题和完整系统设计；
- 学习路线不依赖背诵式话术，由学习者自行组织面试表达。

### 3.3 工程目标

- 每个知识点同时解释技术原理和实际开发使用方式；
- 每个知识点说明可使用的具体框架、组件、接口或代码结构；
- 每个工程问题说明现象、定位、根因、方案、选择、实现和验证；
- 变化较快的框架接口和产品能力记录版本、审核日期和替代方案；
- 所有正式产物可通过脚本检查结构、引用、覆盖和状态。

### 3.4 协作目标

- 新的执行 Agent 不需要依赖聊天记录理解项目；
- 每个工作包（Work Package）有输入、输出、依赖、完成定义和验收命令；
- 工作状态同时提供人类可读和机器可读版本；
- 禁止在没有更新工作状态和覆盖证据的情况下宣布模块完成。

## 4. 非目标

本项目当前不生成：

- 脱离原理的口诀和记忆压缩；
- 遮住答案式自测题；
- 30 秒或 2 分钟背诵话术；
- 虚构为某公司真实面试的题目；
- 未经授权的外部文章、图片或 PDF 全文镜像；
- 只列工具名称、不解释工作方式的框架清单；
- 只生成一张无法阅读的超大静态图；
- 未完成来源审计却标记为正式完成的章节。

## 5. 目标用户与主要使用路径

### 5.1 快速学习路径

```text
完整检索增强生成流程（RAG Workflow）
→ 主干节点工程问题/面试题（Engineering Problem / Interview Question）
→ 问题定位与方案比较
→ 跳转相关知识节点
→ 返回问题完成理解
→ 跨节点综合问题
→ 完整系统设计
```

### 5.2 系统复习路径

```text
全局地铁图（Global Metro Map）
→ 选择一条主干（Backbone）
→ 选择节点（Node）
→ 查看节点局部图（Local Graph）
→ 查看相关问题和知识
```

### 5.3 问题排查路径

```text
实际工程现象
→ 工程问题/面试题（Engineering Problem / Interview Question）
→ 可能受影响的多个节点
→ 根因分支
→ 解决方案
→ 具体实现
→ 验证结果
```

### 5.4 来源核验路径

```text
知识结论或题目
→ 来源映射
→ 固定提交、论文版本或原始页面
→ 冲突与时效说明
```

## 6. 总体信息架构

底层只维护一张有向知识图谱（Directed Knowledge Graph），上层从同一份关系数据生成多个学习视图。

### 6.1 底层数据层

底层包含：

- 来源登记（Source Registry）；
- 来源单元（Source Unit）；
- 术语表（Terminology Glossary）；
- 知识节点（Knowledge Node）；
- 流程节点（Pipeline Stage）；
- 工程问题/面试题（Engineering Problem / Interview Question）；
- 解决方案（Solution）；
- 框架或组件（Framework or Component）；
- 评估方法（Evaluation Method）；
- 有向关系（Directed Relation）；
- 冲突和版本关系（Conflict and Version Relation）。

### 6.2 展示层

展示层至少生成：

1. 全局地铁图（Global Metro Map）；
2. 检索增强生成流程图（RAG Workflow Map）；
3. 跨主干重叠图（Cross-backbone Overlap Map）；
4. 节点局部图（Local Node Map）；
5. 用户问题执行路径图（User Query Execution Path）；
6. 工程问题路径图（Engineering Problem Path）；
7. 节点面试题索引（Stage Interview Index）；
8. 跨节点综合问题索引（Cross-stage Problem Index）；
9. 详细知识章节（Knowledge Chapter）；
10. 来源覆盖与冲突报告（Source Coverage and Conflict Report）。

### 6.3 为什么不是一张图

底层关系必须完整且允许复杂多对多连接，但单张静态图不能同时承担总览、局部学习、问题定位和工程实现。项目采用“一份图数据，多种投影视图”的方式：

- 全局图只展示主干和换乘节点；
- 局部图展示一个节点的一至两跳关系；
- 问题图从实际现象反向连接受影响节点；
- 具体技术和框架实现放在正文，而不是塞进图中。

## 7. 检索增强生成主干设计

### 7.1 离线知识构建主干（Offline Knowledge Construction）

```text
数据源（Data Source）
→ 数据摄取（Data Ingestion）
→ 文档解析（Document Parsing）
→ 数据治理（Data Governance）
→ 文本切分（Chunking）
→ 向量嵌入（Embedding）
→ 存储与索引（Storage and Indexing）
→ 索引发布（Index Release）
```

### 7.2 在线问答主干（Online Query and Answering）

```text
用户问题（User Query）
→ 查询理解（Query Understanding）
→ 查询改写（Query Rewrite）
→ 查询路由（Query Routing）
→ 检索（Retrieval）
→ 结果融合（Result Fusion）
→ 重排（Reranking）
→ 上下文组装（Context Assembly）
→ 答案生成（Answer Generation）
→ 引用与验证（Citation and Verification）
```

### 7.3 评估反馈主干（Evaluation and Feedback）

```text
用户反馈（User Feedback）
→ 失败归因（Failure Attribution）
→ 检索评估（Retrieval Evaluation）
→ 生成评估（Generation Evaluation）
→ 端到端评估（End-to-end Evaluation）
→ 数据、策略或模型更新（Data, Strategy or Model Update）
```

### 7.4 生产治理主干（Production Governance）

```text
权限控制（Access Control）
→ 安全治理（Security Governance）
→ 可观测性（Observability）
→ 性能和成本（Performance and Cost）
→ 版本发布（Version Release）
→ 故障恢复（Failure Recovery）
```

### 7.5 交叉主干（Cross-domain Backbone）

向量数据库（Vector Database）、智能体（Agent）、提示工程（Prompt Engineering）、知识图谱（Knowledge Graph）和评估（Evaluation）拥有自己的完整主干，只在部分节点与检索增强生成（Retrieval-Augmented Generation，RAG）重叠。

例如向量数据库（Vector Database）在向量嵌入（Embedding）、向量存储（Vector Storage）、向量索引（Vector Index）、元数据过滤（Metadata Filtering）、检索（Retrieval）、索引更新（Index Update）等节点与检索增强生成（Retrieval-Augmented Generation，RAG）重叠；近似最近邻检索（Approximate Nearest Neighbor Search，ANN）只是向量数据库（Vector Database）的一项索引和检索能力。

## 8. 知识图谱模型

### 8.1 节点类型

| 类型 | 作用 |
|---|---|
| `backbone` | 独立技术主干，例如检索增强生成（RAG）或向量数据库（Vector Database） |
| `pipeline_stage` | 流程节点，例如文本切分（Chunking） |
| `knowledge` | 可独立讲解的概念、原理或方法 |
| `algorithm` | 算法，例如分层可导航小世界图（Hierarchical Navigable Small World，HNSW） |
| `capability` | 系统能力，例如元数据过滤（Metadata Filtering） |
| `problem_question` | 工程问题/面试题（Engineering Problem / Interview Question） |
| `solution` | 解决方案或方案分支 |
| `implementation` | 框架、组件、接口或代码实现 |
| `evaluation` | 指标、数据集或评估方法 |
| `source` | 论文、官方文档、面经、题库或仓库来源 |

### 8.2 关系类型

| 关系 | 语义 |
|---|---|
| `contains` | A 包含 B |
| `next_stage` | A 的正常下游阶段是 B |
| `branches_to` | A 按条件分支到 B |
| `merges_into` | A 汇合到 B |
| `depends_on` | A 依赖 B |
| `uses` | A 使用 B |
| `implements` | A 实现 B |
| `overlaps_with` | 两条主干或节点在能力上重叠 |
| `alternative_to` | A 与 B 是可替代路线 |
| `combined_with` | A 与 B 可以组合 |
| `observed_as` | 根因或故障表现为某个现象 |
| `problem_at` | 问题可能位于某个节点 |
| `caused_by` | 问题可能由某个原因导致 |
| `solved_by` | 问题可以由某个方案解决 |
| `implemented_by` | 方案由框架、组件或代码实现 |
| `evaluated_by` | 节点或方案由指标和实验评估 |
| `asked_as` | 工程问题在公开来源中被问成某道题 |
| `supported_by` | 结论或题目由来源证据支持 |
| `supersedes` | 新版本替代旧版本 |
| `conflicts_with` | 两项来源结论存在冲突 |

完整字段和约束见 [`taxonomy/rag-graph-model.json`](../taxonomy/rag-graph-model.json)。

## 9. 内容模型

### 9.1 知识章节（Knowledge Chapter）

每个知识章节固定为四个主体部分：

1. 知识点概要；
2. 技术原理；
3. 实际开发中的位置和使用方式；
4. 具体技术或框架实现。

章节末尾只增加：

- 相关工程问题/面试题链接；
- 相关知识节点；
- 来源、版本和审核状态。

故障排查、选型比较和验证过程主要放入具体问题页面，避免每个知识章节重复相同模板。

### 9.2 工程问题/面试题（Engineering Problem / Interview Question）

统一内容结构：

1. 问题或题目；
2. 来源类型和原始定位；
3. 实际工程现象和业务条件；
4. 关联流程节点；
5. 根因分支；
6. 解决方案分支；
7. 方案选择依据；
8. 具体技术或框架实现；
9. 验证方法；
10. 关联知识章节；
11. 相关追问和跨节点关系。

没有原始面试来源的问题标记为工程问题，不标记为真实面试题。一个问题允许连接多个流程节点，一个流程节点允许连接多道问题。

### 9.3 完整流程前置内容

完整检索增强生成流程（RAG Workflow）是前置学习内容，不包装成一道面试题。它负责说明：

- 当前完整流程；
- 不同主干；
- 分支和汇合；
- 用户问题的动态执行路径；
- 与其他技术主干的重叠；
- 节点题和综合题的学习顺序。

## 10. 术语与表达规范

### 10.1 双语强制规则

每次出现专业技术术语，都使用统一双语表达，不只在第一次出现时说明。

示例：

- 文档解析（Document Parsing）；
- 文本切分（Chunking）；
- 向量嵌入（Embedding）；
- 查询改写（Query Rewrite）；
- 混合检索（Hybrid Search）；
- 幂等性（Idempotency）；
- 灰度发布（Canary Release）。

代码标识符、类名、函数名、参数、应用程序编程接口（Application Programming Interface，API）和配置项保持原样。

### 10.2 翻译原则

- 使用国内工程领域的常见表达，不机械直译；
- 括号内使用真正的专业英文名称；
- 缩写必须与英文全称一致；
- 同一术语不得在不同文件中随意变换中文名称；
- 图、正文、表格、标题和索引使用同一规范名称。

术语权威表见 [`knowledge/rag/TERMINOLOGY.md`](../knowledge/rag/TERMINOLOGY.md)。

## 11. 来源策略与“尽可能完整”的操作定义

### 11.1 来源分层

技术结论来源优先级：

1. 官方文档、官方代码仓库和原始论文；
2. 有实验设计、数据和代码的技术报告；
3. 有明确环境和证据的工程实践；
4. 教程、博客和二次汇总只用于发现线索或补充解释。

面试题来源类型：

1. 第一人称面经（First-person Interview Report）；
2. 公开题库（Public Question Bank）；
3. 项目型考题（Project Interview Exercise）；
4. 二次索引（Secondary Index）。

### 11.2 检索范围

针对每个流程节点分别使用中英文检索：

- 节点名称；
- 常见故障表现；
- 系统设计问题；
- 框架实现；
- 评估和基准；
- 公开面经和题库；
- 经典方法和当前高级方法。

### 11.3 搜索停止条件

一个节点只有满足以下条件，才可标记为当前版本的 `coverage_saturated`：

- 登记来源全部处理；
- 节点的原理、实现、问题、方案和评估均有覆盖；
- 一手资料缺口检查完成；
- 公开面试题专项搜索完成；
- 连续两轮独立补漏未产生新的知识类型或问题类型；
- 未解决冲突和不确定项已显式登记；
- 记录搜索日期、检索式和来源范围。

`coverage_saturated` 只表示固定日期和登记范围内达到饱和，不表示互联网永久绝对无遗漏。

## 12. 内容生产流水线

```text
来源发现（Source Discovery）
→ 来源登记与版本冻结（Source Registration and Version Pinning）
→ 来源单元提取（Source Unit Extraction）
→ 术语规范化（Terminology Normalization）
→ 知识、问题和实现拆解（Knowledge, Problem and Implementation Extraction）
→ 保守去重与冲突审计（Conservative Deduplication and Conflict Audit）
→ 知识图谱关系构建（Knowledge Graph Construction）
→ 覆盖与补漏搜索（Coverage and Gap Search）
→ 学习视图生成（Learning View Generation）
→ 节点题生成（Stage Question Production）
→ 综合题生成（Cross-stage Problem Production）
→ 正文生成（Chapter Production）
→ 自动与人工验收（Automated and Manual Acceptance）
```

关键规则：先完成来源和关系数据，再从同一数据生成正文和图；禁止不同产物各自维护一套无法对齐的知识结论。

## 13. 阶段规划

### Phase 0：仓库与来源基线

状态：`completed`

已完成：

- 公开仓库结构；
- 首批来源及版本冻结；
- 许可和发布边界；
- 695 个来源单元盘点；
- 187 个原子知识目录草案；
- 基础校验脚本；
- 用户 PDF 页级映射。

### Phase 1：需求重构与协作基线

状态：`completed`

输出：

- 本项目整体规划；
- Agent 工作入口；
- 统一术语表（Terminology Glossary）；
- 知识图谱模型（Knowledge Graph Model）；
- 机器可读工作状态；
- 新知识章节和问题页面模板；
- 现有前三章的重写标记。

完成定义：所有后续 Agent 能只依赖仓库文件解释目标、约束、当前状态和下一任务。

### Phase 2：来源扩充与题目全量盘点

状态：`in_progress`

输出：

- 扩充来源登记；
- 面试题和工程问题清单；
- 节点专项检索日志；
- 来源许可与发布策略；
- 新来源单元；
- 面试题来源到原始页面的回链。

完成定义：每个检索增强生成流程（RAG Workflow）节点完成第一轮中英文公开资料搜索并登记结果。

### Phase 3：底层知识图谱构建

状态：`pending`

输出：

- 主干和流程节点；
- 知识、算法、能力、问题、方案、实现和评估节点；
- 有向关系；
- 来源证据关系；
- 冲突和版本关系；
- 孤立节点和无来源节点报告。

完成定义：所有已审核来源单元都映射到图节点或明确排除原因，所有图边使用受控关系类型。

### Phase 4：完整流程和多视图

状态：`pending`

输出：

- 完整检索增强生成流程（RAG Workflow）前置内容；
- 全局地铁图（Global Metro Map）；
- 四条检索增强生成主干（RAG Backbone）；
- 向量数据库（Vector Database）和智能体（Agent）重叠视图；
- 用户问题执行路径；
- 每个节点局部图。

完成定义：每个正式图都由底层关系数据生成或校验，节点和关系可回到知识图谱（Knowledge Graph）。

### Phase 5：主干节点工程问题和面试题

状态：`pending`

输出顺序：

1. 数据摄取（Data Ingestion）；
2. 文档解析（Document Parsing）；
3. 数据治理（Data Governance）；
4. 文本切分（Chunking）；
5. 向量嵌入（Embedding）；
6. 存储与索引（Storage and Indexing）；
7. 查询理解（Query Understanding）；
8. 查询改写（Query Rewrite）；
9. 查询路由（Query Routing）；
10. 检索（Retrieval）；
11. 结果融合（Result Fusion）；
12. 重排（Reranking）；
13. 上下文组装（Context Assembly）；
14. 答案生成（Answer Generation）；
15. 引用与验证（Citation and Verification）；
16. 评估（Evaluation）；
17. 生产治理（Production Governance）；
18. 高级检索增强生成（Advanced RAG）。

完成定义：每个节点都有经来源核验的问题集，并连接根因、方案、实现、验证和知识章节。

### Phase 6：跨节点综合问题

状态：`pending`

优先主题：

- 零召回；
- 噪声召回；
- 召回正确但答案错误；
- 新旧知识冲突；
- 高延迟和高成本；
- 权限和多租户；
- 间接提示注入（Indirect Prompt Injection）；
- 大规模索引和高并发；
- 检索增强生成（RAG）、长上下文（Long Context）和微调（Fine-tuning）选型；
- 从零设计生产级检索增强生成系统（Production-grade RAG System）。

完成定义：综合问题明确连接多个流程节点，不重复复制底层知识正文。

### Phase 7：标准知识章节重写与补全

状态：`pending`

输出：

- 按新四段式标准重写 `RAG-01` 至 `RAG-03`；
- 继续完成其他知识节点；
- 每个知识点加入具体框架或自研实现；
- 每次出现专业术语均使用双语表达；
- 每个知识点反向关联工程问题/面试题。

完成定义：章节通过术语、来源、图关系、问题链接和实际实现检查。

### Phase 8：严格验收与发布

状态：`pending`

输出：

- 来源覆盖报告；
- 知识覆盖报告；
- 问题覆盖报告；
- 图覆盖报告；
- 冲突和时效报告；
- 严格校验结果；
- 当前版本发布说明。

完成定义：全部验收门通过，未完成项为零或被明确列入下一版本范围。

## 14. 工作包执行规范

每个工作包（Work Package）必须声明：

- `work_item_id`；
- 目标；
- 输入文件；
- 允许修改的文件；
- 依赖工作包；
- 来源边界；
- 产出文件；
- 完成定义；
- 验证命令；
- 剩余风险和待处理项。

工作包不得同时混合大规模来源审计、分类重构和正式正文生成，避免无法判断错误来自哪个阶段。

## 15. Agent 交接规范

新的执行 Agent 开始前必须依次阅读：

1. [`AGENTS.md`](../AGENTS.md)；
2. 本项目整体规划；
3. [`audits/rag/work-status.json`](../audits/rag/work-status.json)；
4. [`knowledge/rag/TERMINOLOGY.md`](../knowledge/rag/TERMINOLOGY.md)；
5. [`knowledge/rag/CONTENT_STANDARD.md`](../knowledge/rag/CONTENT_STANDARD.md)；
6. [`taxonomy/rag-graph-model.json`](../taxonomy/rag-graph-model.json)；
7. 当前工作包涉及的来源、审计和模板文件。

交接时必须记录：

- 已完成内容；
- 修改文件；
- 验证结果；
- 尚未验证的假设；
- 下一工作项；
- 不得重复执行的已完成工作；
- 当前工作区和 Git 状态。

## 16. 质量门和验收指标

### Gate A：来源

- 来源有稳定标识、版本、许可状态和纳管范围；
- 题目可定位到原始页面或固定提交；
- 技术结论回到一手资料核验。

### Gate B：知识和问题拆解

- 独立信息没有因“主题相似”被删除；
- 每个问题保留业务条件和独有解决方案；
- 知识去重不等于题目去重。

### Gate C：关系

- 所有关系使用受控类型；
- 一个问题允许关联多个节点；
- 分支和汇合方向明确；
- 跨主干重叠有明确关系。

### Gate D：术语

- 每次出现专业术语均为统一双语表达；
- 没有机械或不符合国内工程语境的翻译；
- 图和正文名称一致。

### Gate E：内容

- 知识章节完成四个主体部分；
- 实际开发说明与原理自然结合；
- 框架实现不是简单列名；
- 问题页面包含定位、方案、实现和验证；
- 不生成背诵式面试答案。

### Gate F：覆盖

- 来源到图节点无未说明遗漏；
- 节点到来源可追踪；
- 问题到节点和节点到问题双向可查；
- 正式图没有孤立且不可访问的节点。

## 17. 主要风险与控制措施

| 风险 | 控制措施 |
|---|---|
| 互联网内容无法证明绝对完整 | 固定检索日期、来源范围、检索式和饱和条件 |
| 面试题重复导致错误删除 | 知识去重、题目保留独有条件，分开审计 |
| 术语双语导致文本冗长 | 使用统一短名称，但仍保证每次双语；代码标识符不翻译 |
| 图过大无法阅读 | 一份底层图数据，生成全局、局部、问题和重叠视图 |
| 框架接口迅速变化 | 记录版本和审核日期，使用官方文档，设置复核周期 |
| 未授权内容被重新发布 | 保存定位和自己的转述，不镜像未知许可原文 |
| Agent 自行改变方向 | 以本规划、机器状态和完成定义作为硬约束 |
| 过早生成正文造成信息压缩 | 来源、节点和关系先验收，再生成正式正文 |

## 18. 当前基线

截至 2026-09-02：

- 已登记来源：4 个首批来源；
- 已盘点来源单元：695 个；
- 当前原子知识目录：187 个草案原子；
- 已人工映射用户 PDF：37 个来源单元；
- 严格校验仍有 522 个来源单元待人工复核；
- 严格验收清单仍有 16 项未完成；
- `RAG-01` 至 `RAG-03` 的旧第一版正文和关系图需要按新标准重写；
- 当前 13 个一级模块继续用于分类和覆盖审计，但不再作为唯一线性学习入口。

## 19. 紧接着执行的工作顺序

1. 完成本规划、Agent 入口、术语表、图模型和工作状态；
2. 更新模板和校验脚本，使新标准可以自动检查；
3. 建立完整检索增强生成流程（RAG Workflow）的流程节点清单；
4. 扩充面试题和技术来源，逐节点建立检索日志；
5. 生成底层知识图谱（Knowledge Graph）的第一版；
6. 生成完整流程前置内容和全局地铁图（Global Metro Map）；
7. 从数据摄取（Data Ingestion）节点开始整理节点工程问题/面试题；
8. 节点题完成后生成跨节点综合问题；
9. 按新标准重写知识正文；
10. 完成严格覆盖审计和当前版本发布。

## 20. 变更控制

以下变更需要先修改本规划和机器状态，再执行内容生产：

- 新增或删除一级主干；
- 修改知识章节主体结构；
- 修改问题页面主体结构；
- 修改术语双语规则；
- 修改面试题来源要求；
- 修改严格完成定义；
- 将当前版本标记为正式完成。

普通新增来源、知识节点、问题节点、实现节点和关系，不需要改变项目方向，但必须更新对应登记和覆盖状态。

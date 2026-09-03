# 关系图集：检索增强生成（Retrieval-Augmented Generation，RAG）可学习骨架版

> 状态：`draft / backbone-v0.1 / 非正式`

图中实线箭头表示正常下游或明确依赖；虚线箭头表示反馈、风险传播或跨主干重叠。图只表达当前已确认架构关系，不替代未来由有向知识图谱（Directed Knowledge Graph）生成的正式视图。

## 1. 离线知识构建主干图（Offline Knowledge Construction Map）

```mermaid
flowchart LR
    DS["数据源（Data Source）"] --> DI["数据摄取（Data Ingestion）"] --> DP["文档解析（Document Parsing）"] --> DG["数据治理（Data Governance）"]
    DG --> CH["文本切分（Chunking）"] --> EM["向量嵌入（Embedding）"] --> SI["存储与索引（Storage and Indexing）"] --> IR["索引发布（Index Release）"]
    DG -->|"分支到（Branches To）"| ACL["访问控制（Access Control）"]
    ACL -->|"汇合到（Merges Into）"| SI
    DI -. "变更事件（Change Event）" .-> UP["增量更新（Incremental Update）"]
    UP --> DI
```

## 2. 在线查询与答案生成主干图（Online Query and Answering Map）

```mermaid
flowchart LR
    UQ["用户问题（User Query）"] --> QU["查询理解（Query Understanding）"] --> QW["查询改写（Query Rewrite）"] --> QT["查询路由（Query Routing）"]
    QT --> RT["检索（Retrieval）"] --> RF["结果融合（Result Fusion）"] --> RK["重排（Reranking）"] --> CA["上下文组装（Context Assembly）"] --> AA["答案生成（Answer Generation）"] --> CV["引用与验证（Citation and Verification）"]
    QT -->|"分支到（Branches To）"| NO["不检索路径（No-Retrieval Path）"]
    NO --> CA
    CV -->|"分支到（Branches To）"| AB["拒答（Abstention）"]
    CV -->|"汇合到（Merges Into）"| OUT["用户输出（User Output）"]
    AB --> OUT
```

## 3. 检索优化局部图（Retrieval Optimization Local Map）

```mermaid
flowchart TD
    QU["查询理解（Query Understanding）"] --> QW["查询改写（Query Rewrite）"]
    QW --> DR["稠密检索（Dense Retrieval）"]
    QW --> SR["稀疏检索（Sparse Retrieval）"]
    QW --> MR["元数据过滤（Metadata Filtering）"]
    DR --> FU["结果融合（Result Fusion）"]
    SR --> FU
    MR --> FU
    FU --> RR["重排（Reranking）"] --> MMR["最大边际相关性（Maximal Marginal Relevance，MMR）"] --> CA["上下文组装（Context Assembly）"]
    RR -. "失败传播（Failure Propagation）" .-> LOW["低相关候选（Low-Relevance Candidate）"]
    LOW -. "反馈（Feedback）" .-> QW
```

## 4. 答案可信度与幻觉治理图（Answer Trustworthiness and Hallucination Control Map）

```mermaid
flowchart TD
    RET["检索（Retrieval）"] --> EVI["检索证据（Retrieved Evidence）"] --> CA["上下文组装（Context Assembly）"] --> GEN["答案生成（Answer Generation）"]
    GEN --> CIT["引用（Citation）"] --> VER["引用与验证（Citation and Verification）"]
    EVI --> SRC["来源可信度（Source Trustworthiness）"] --> VER
    VER --> GR["事实依据性（Groundedness）"]
    VER --> FA["忠实度（Faithfulness）"]
    VER -->|"分支到（Branches To）"| ABS["拒答（Abstention）"]
    CA -. "风险传播（Risk Propagation）" .-> HAL["幻觉（Hallucination）"]
    GEN -. "风险传播（Risk Propagation）" .-> HAL
    HAL --> VER
```

## 5. 评估反馈与生产治理图（Evaluation Feedback and Production Governance Map）

```mermaid
flowchart LR
    LOG["运行日志（Runtime Log）"] --> EVA["评估（Evaluation）"] --> ATT["失败归因（Failure Attribution）"]
    ATT -->|"分支到（Branches To）"| DATA["数据更新（Data Update）"]
    ATT -->|"分支到（Branches To）"| RET["检索策略更新（Retrieval Strategy Update）"]
    ATT -->|"分支到（Branches To）"| GEN["生成策略更新（Generation Strategy Update）"]
    DATA --> REL["版本发布（Version Release）"]
    RET --> REL
    GEN --> REL
    REL --> MON["可观测性（Observability）"] --> LOG
    GOV["生产治理（Production Governance）"] --> REL
    GOV --> MON
    GOV --> SEC["安全治理（Security Governance）"]
```

## 6. 向量数据库与检索增强生成重叠图（Vector Database and RAG Overlap Map）

```mermaid
flowchart TB
    RAG["检索增强生成（Retrieval-Augmented Generation，RAG）"]
    VDB["向量数据库（Vector Database）"]
    RAG --> EM["向量嵌入（Embedding）"]
    RAG --> RT["检索（Retrieval）"]
    VDB --> VI["向量索引（Vector Index）"]
    VDB --> ANN["近似最近邻检索（Approximate Nearest Neighbor Search）"]
    EM --- VI
    VI --> ANN
    ANN --- RT
    VDB --> MF["元数据过滤（Metadata Filtering）"]
    MF --- RT
    RAG --> CA["上下文组装（Context Assembly）"]
    RAG --> AG["答案生成（Answer Generation）"]
```

## 7. 智能体、图检索增强生成与传统检索增强生成重叠图（Agent, GraphRAG and Traditional RAG Overlap Map）

```mermaid
flowchart TB
    TR["传统检索增强生成（Traditional RAG）"] --> RET["检索（Retrieval）"] --> GEN["答案生成（Answer Generation）"]
    GR["图检索增强生成（GraphRAG）"] --> KG["知识图谱（Knowledge Graph）"] --> GRET["图结构检索（Graph Retrieval）"]
    AGT["智能体（Agent）"] --> PLAN["任务规划（Task Planning）"] --> TOOL["工具调用（Tool Calling）"]
    RET --- GRET
    GRET --> GEN
    PLAN --> RET
    PLAN --> GRET
    TOOL --> RET
    TOOL --> GRET
    AGT -. "动态控制（Dynamic Control）" .-> TR
    AGT -. "动态控制（Dynamic Control）" .-> GR
```

## 8. 工程问题到故障节点反向定位图（Engineering Problem to Failure-node Diagnosis Map）

```mermaid
flowchart RL
    SYM["工程现象（Engineering Symptom）"] --> P["工程问题（Engineering Problem）"]
    P -->|"出现问题于（Problem At）"| RET["检索（Retrieval）"]
    P -->|"出现问题于（Problem At）"| CA["上下文组装（Context Assembly）"]
    P -->|"出现问题于（Problem At）"| GEN["答案生成（Answer Generation）"]
    P -->|"出现问题于（Problem At）"| GOV["生产治理（Production Governance）"]
    RET --> C1["召回不足（Recall Deficit）"]
    CA --> C2["上下文预算不足（Context Budget Deficit）"]
    GEN --> C3["证据不忠实（Evidence Unfaithfulness）"]
    GOV --> C4["权限或版本不一致（Permission or Version Mismatch）"]
    C1 --> SOL["解决方案（Solution）"]
    C2 --> SOL
    C3 --> SOL
    C4 --> SOL
    SOL --> VAL["验证（Validation）"]
```

继续阅读：[一页式总览](01-one-page-overview.md) | [18 节点概要学习卡](03-stage-cards.md)

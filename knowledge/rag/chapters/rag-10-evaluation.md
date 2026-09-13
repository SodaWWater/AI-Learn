---
id: RAG-10
title: 检索增强生成评估
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: mixed
chapter_path: knowledge/rag/chapters/rag-10-evaluation.md
atoms: [RAG-10-001, RAG-10-002, RAG-10-003, RAG-10-004, RAG-10-005, RAG-10-006, RAG-10-007, RAG-10-008, RAG-10-009, RAG-10-010, RAG-10-011, RAG-10-012, RAG-10-013, RAG-10-014]
related_problem_ids: [PQ-RAG-0001, PQ-RAG-0003, PQ-RAG-0006, PQ-RAG-0007, PQ-RAG-0008, PQ-RAG-0010, PQ-RAG-0014, PQ-RAG-0018, PQ-RAG-0019, PQ-RAG-0020, PQ-RAG-0021, PQ-RAG-0023, PQ-RAG-0024, PQ-RAG-0025]
---

# 检索增强生成评估

> 本章状态：`formal_bounded`（范围受限正式，已通过当前登记范围严格验收）。指标只用于已登记数据和版本的比较，不把单次实验或公开题目当作普遍性能结论。

## 一、知识点概要

检索增强生成（Retrieval-Augmented Generation，RAG）评估（Evaluation）要把解析、切分、检索、重排、上下文、生成、引用和线上任务拆开，再用端到端结果检查整体价值（`RAG-10-001`）。只看最终答案准确率会把“没有召回证据”和“模型没有遵循证据”混在一起。

可靠评估依赖黄金数据集（Golden Dataset）及问题、可接受答案、证据和权限标注（`RAG-10-002`），并结合人工样本、真实日志和受控合成数据（`RAG-10-003`）。排序指标、答案质量、事实依据性（Groundedness）、引用质量、人工一致性和线上实验各自回答不同问题（`RAG-10-004` 至 `RAG-10-014`）。

## 二、技术原理

### 2.1 数据集和分层漏斗

数据集应按租户、语言、文档类型、问题意图、难度、时间和权限分层。每条样本固定 `query`、参考答案、证据 ID、允许的替代表达、不可接受事实和数据集版本。人工标注建立基准，日志反映真实分布，合成样本扩展长尾；合成数据必须抽样人工核验，避免把生成器偏差写入基准。

评估漏斗从解析质量、证据召回、排序质量、上下文充分性、答案正确性和引用完整性逐层收敛。每层保存输入快照和版本，能够定位第一个失败阶段（`RAG-10-001`、`RAG-10-002`、`RAG-10-003`）。

### 2.2 检索和排序指标

精确率（Precision）衡量返回候选中相关项比例，召回率（Recall）衡量目标证据被找回的比例，命中率（Hit Rate）关注 Top-K 是否至少包含一个目标，Coverage 衡量问题集合被可回答证据覆盖的范围（`RAG-10-004`）。排序质量使用平均倒数排名（Mean Reciprocal Rank，MRR）、平均精度均值（Mean Average Precision，MAP）和归一化折损累计增益（Normalized Discounted Cumulative Gain，nDCG），分别适合首个命中、多个相关项和分级相关性（`RAG-10-005`）。

重排器（Reranker）评估必须固定候选集大小、检索器版本和延迟预算；重排器不能找回候选集之外的证据。比较重排前后指标时同时报告候选召回、最终排序、截断率和 P95/P99 延迟，避免用排序收益掩盖召回损失（`RAG-10-006`）。

### 2.3 生成、忠实度和引用

答案正确性（Answer Correctness）比较事实与参考答案；相关性（Relevancy）判断是否回答问题；完整性（Completeness）检查必要要点是否缺失（`RAG-10-007`）。忠实度（Faithfulness）和事实依据性（Groundedness）要求断言能由上下文支持，幻觉评估应按断言而非只按整段文本计分（`RAG-10-008`）。

引用准确率（Citation Accuracy）检查引用是否真正支持断言，引用完整性（Citation Completeness）检查重要断言是否都带引用；应记录来源版本、定位和引用覆盖范围（`RAG-10-009`）。自动框架如 RAGAS、ARES、RAGChecker 和 QCare 可以批量计算指标，但其模型、提示词和阈值属于评估器配置，不能被当成绝对真值（`RAG-10-010`）。

### 2.4 人工评估、裁判和线上实验

大语言模型裁判（LLM-as-a-Judge）易受位置、措辞、模型偏好、长度和提示词影响。校准方法包括人工金样、盲评、双向交换、分层抽样、阈值校准和与人工分数的相关性报告；不应只报告裁判平均分（`RAG-10-011`）。人工抽检使用明确评分量表、正反例和双人重叠样本，报告一致性与仲裁规则（`RAG-10-012`）。

线上任务成功、满意度、追问率、人工接管率和成本是业务指标；A/B 实验应冻结索引、模型和策略版本，定义主要指标、护栏指标、样本量和停止规则。离线指标提升不等于线上收益（`RAG-10-013`）。失败归因将解析、召回、排序、上下文、生成、引用和安全错误分开；消融实验一次移除一个能力，回归测试覆盖历史样本和已修复故障（`RAG-10-014`）。

## 三、实际开发中的位置和使用方式

评估服务读取摄取快照、检索日志、证据包和最终答案，输出带 `dataset_version`、`index_version`、`model_version`、`prompt_version` 的明细。离线流水线用于发布门禁；影子流量（Shadow Traffic）用于新模型和新路由；线上 A/B 只改变一个主要变量并保留权限和成本护栏。

最小运行表应同时保存 `retrieval_recall`、`nDCG`、`answer_correctness`、`faithfulness`、`citation_accuracy`、P95 延迟、Token 成本和拒答率。出现答案下降时，先按 trace 回放证据，再做分层指标和消融，不直接调大 Top-K 或温度。

## 四、具体技术或框架实现

可用如下评估记录结构：

```python
record = {
    "query": query,
    "gold_evidence_ids": gold_ids,
    "retrieved_ids": retrieved_ids,
    "answer": answer,
    "citations": citations,
    "versions": versions,
}
scores = evaluator.run(record, metrics=["recall@k", "ndcg", "faithfulness", "citation_accuracy"])
```

RAGAS、RAGChecker、ARES 和 QCare 可作为自动评测适配器；Sentence Transformers、Cohere Rerank 等用于固定重排实验；LangSmith 与 OpenTelemetry 可提供追踪和线上样本。框架的指标实现、默认提示词和 API 需锁定登记版本，最终发布仍需人工金样和业务回放确认。

## 相关工程问题/面试题

- [PQ-RAG-0001：Recall@5 与评测集设计](../../../interview/rag/stages/evaluation.md#pq-rag-0001)
- [PQ-RAG-0006：VectorRAG/GraphRAG 日志评测](../../../interview/rag/stages/evaluation.md#pq-rag-0006)
- [PQ-RAG-0021：全链路失败归因](../../../interview/rag/stages/evaluation.md#pq-rag-0021)
- [PQ-RAG-0025：异常高命中率与数据污染](../../../interview/rag/stages/evaluation.md#pq-rag-0025)

## 相关知识节点

`RAG-04` 至 `RAG-09` 提供被评估的阶段产物；`RAG-11` 提供可观测性和发布门禁；`RAG-12` 的高级检索策略必须通过分层和端到端实验验证；`RAG-13` 将指标转化为项目与面试中的证据。

### 关系与评估链路

评估沿 `query → retrieval candidates → ranked evidence → answer → citation` 关系链定位失败阶段；分层指标、消融实验（Ablation Study，消融实验）和回归测试（Regression Test，回归测试）共同决定策略是否发布，不以单一指标替代端到端判断。

## 来源、版本与审核状态

主要来源包括 `SRC-RAGAS-EACL-2024`、`SRC-ARES-RAG-EVALUATION-2024`、`SRC-RAGCHECKER-2024`、`SRC-ALCE-CITATION-EVALUATION-2023`、`SRC-LLM-AS-JUDGE-MTBENCH-2023`、`SRC-LLM-JUDGE-VULNERABILITIES-2025`、`SRC-NOWCODER-RAG-EVALUATION-FUNNEL-2026`、`SRC-NOWCODER-RAG-RETRIEVAL-EVOLUTION-2026`、`SRC-AGENTIC-RAG-TRACER-2026` 与已登记官方文档。题库和面经只证明问题场景存在，不单独证明指标结论。指标阈值、评测框架 API、线上实验平台和模型能力需按登记版本复核。本章覆盖 14 个原子。

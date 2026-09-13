---
id: RAG-04
title: 文本切分（Chunking）与检索单元设计
status: formal_bounded
reviewed_at: 2026-09-04
freshness_class: active
chapter_path: knowledge/rag/chapters/rag-04-chunking.md
atoms:
  - RAG-04-001
  - RAG-04-002
  - RAG-04-003
  - RAG-04-004
  - RAG-04-005
  - RAG-04-006
  - RAG-04-007
  - RAG-04-008
  - RAG-04-009
  - RAG-04-010
  - RAG-04-011
  - RAG-04-012
  - RAG-04-013
  - RAG-04-014
  - RAG-04-015
  - RAG-04-016
  - RAG-04-017
related_problem_ids: [PQ-RAG-0002, PQ-RAG-0003, PQ-RAG-0007, PQ-RAG-0010, PQ-RAG-0011, PQ-RAG-0022]
---

# 文本切分（Chunking）与检索单元设计

> 本章是 `formal_bounded`（范围受限正式），只整理已登记来源和图谱原子，不把问题库存当作答案。

## 一、知识点概要

文本切分（Chunking）把文档解析（Document Parsing）输出组织成可嵌入、可检索、可引用和可回溯的片段。它同时受检索相关性、生成上下文预算、引用粒度、索引规模和更新成本约束（`RAG-04-001`）。固定字符或词元（Token）长度（`RAG-04-002`）建立可重复基线；递归字符切分（Recursive Character Splitting，`RAG-04-003`）按分隔符逐级退化；标题、段落和条款切分（`RAG-04-004`）优先保留文档结构。

语义切分（Semantic Chunking）使用相邻句表示变化和边界阈值（`RAG-04-005`）；滑动窗口和分块重叠（Chunk Overlap，`RAG-04-006`）减少边界丢失但增加冗余。父子切分（Parent-child Chunking，`RAG-04-007`）和句窗检索（Sentence Window Retrieval，`RAG-04-008`）让小片段召回、大片段回溯。命题化切分（Proposition Chunking，`RAG-04-009`）形成可验证事实；上下文化切分（Contextual Chunking，`RAG-04-010`）补入标题、路径等局部上下文。

表格、代码和多模态元素需专项切分（`RAG-04-011`）。分块大小（Chunk Size）与重叠比例必须按查询集选择（`RAG-04-012`、`RAG-04-013`），并保存 Chunk ID、Parent ID 和版本（`RAG-04-014`）。策略以离线评估和消融实验（Ablation Study，`RAG-04-015`）决定；延迟切分（Late Chunking，`RAG-04-016`）先编码后池化；假设问题索引（Hypothetical Question Indexing，`RAG-04-017`）在文档侧增加问题表示。

## 二、技术原理

设文档被切为片段集合 `C={c_i}`。好的片段应主题集中、证据足够、长度可控且能回到原始定位。固定长度方法简单稳定；递归方法按段落、换行和句号等分隔符从粗到细拆分；结构方法把标题层级、页码和元素类型作为边界信号。语义方法计算相邻句的向量距离，超过阈值才断开，阈值与向量嵌入（Embedding）模型绑定。

Overlap 复制相邻片段尾部，提升跨边界命中概率，却会放大索引体积和重复上下文。父子方案以子片段做召回，以父片段做上下文和引用；句窗方案在命中句周围恢复邻句，均应限制回溯窗口。命题切分拆出“条件—主体—结论”，便于事实级引用但可能丢失跨命题依赖。上下文化切分增加标题、路径或摘要，改善脱离正文后的检索性，同时增加词元成本。

表格必须保留表头、行列关系和单位；代码必须保留函数、类、缩进和依赖；图像应关联 OCR（Optical Character Recognition，光学字符识别）、图注和坐标。延迟切分先对长文编码，再按 token 隐状态池化，减少片段间断裂但受模型上下文窗口和显存限制。假设问题索引生成的问题只能作为检索表示，不能替代原文证据。

## 三、实际开发中的位置和使用方式

切分位于数据治理（Data Governance）之后、向量嵌入（Embedding）之前。离线任务接收 `DocumentElement`，输出：

```text
Chunk { chunk_id, parent_id, document_id, document_version,
        text, element_type, page_start, page_end, heading_path,
        token_count, overlap_from, acl, valid_time }
```

按文档类型路由：结构明确的文档先按标题和段落；普通长文本以递归方法做基线；跨段引用使用父子或句窗；表格、代码和图片使用专项序列化。按查询分布调节 `chunk_size`、`chunk_overlap`、语义阈值和回溯窗口。更新时让 Chunk ID 继承 `document_version`，删除旧版本的全部子片段，避免新旧混检。

实验应固定文档快照、解析器、向量嵌入模型和检索器，只切换策略，比较命中率、MRR（Mean Reciprocal Rank，平均倒数排名）、nDCG（Normalized Discounted Cumulative Gain，归一化折损累计增益）、引用完整性、索引体积、词元成本和 P99 延迟（P99 Latency）。长尾长度、跨页条款及表格应单独统计。

## 四、具体技术或框架实现

- LangChain `RecursiveCharacterTextSplitter` 实现递归切分；`chunk_size` 应按 tokenizer 实测。标题解析后可对叶节点再次递归。
- LangChain `ParentDocumentRetriever` 与 LlamaIndex Sentence Window 实现子片段召回、父片段或邻句回溯；回溯前再次做权限过滤。
- Unstructured 与 Docling 可保留标题、表格、代码和多模态元素；结构化序列化文本与原始元素并存，引用使用页码和元素定位。
- Contextual Chunking、Late Chunking、语义切分和 Hypothetical Question Indexing 都是可验证的替代策略，参数需按登记版本复核。
- 评估脚本应输出长度分布、证据命中、重复率、词元成本和 P99 延迟，并保存 `chunk_id → parent_id → source_id` 追踪链。

### 完整性检查：对比、关系、错误与评估

固定长度（Fixed-size）、递归（Recursive）、语义（Semantic）和父子（Parent-child）切分按结构稳定性、跨段引用和更新成本取舍；它们保持 `document → chunk → embedding → retrieval → citation` 关系链。常见错误包括跨页断裂、表格行错位、Chunk ID 重用和权限字段丢失；用固定快照回归 Recall@K、Citation Completeness、重复率、索引体积和 P99 延迟定位首个失败阶段。

## 相关工程问题/面试题

- [`PQ-RAG-0002`](../../../interview/rag/stages/chunking.md#pq-rag-0002)
- [`PQ-RAG-0003`](../../../interview/rag/stages/chunking.md#pq-rag-0003)
- [`PQ-RAG-0007`](../../../interview/rag/stages/chunking.md#pq-rag-0007)
- [`PQ-RAG-0010`](../../../interview/rag/stages/chunking.md#pq-rag-0010)
- [`PQ-RAG-0011`](../../../interview/rag/stages/chunking.md#pq-rag-0011)
- [`PQ-RAG-0022`](../../../interview/rag/stages/chunking.md#pq-rag-0022)

## 图谱与来源边界

覆盖 `RAG-04-001` 至 `RAG-04-017`（17/17），图谱原子均已完成来源映射，章节审核状态为 `formal_bounded`。来源包括登记的 LangChain、LlamaIndex、Unstructured、Docling、Late Chunking、Contextual Retrieval、语义切分研究和已纳管学习材料；本章未新增来源、节点或关系。用户 PDF 仅作页级补充。阈值、上下文窗口、框架 API、成本和性能需按来源登记版本复核。

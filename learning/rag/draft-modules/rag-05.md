# RAG-05 Embedding（审计草案）

> 图中每个叶子节点对应原子目录中的一个独立知识点；只有完全同义的来源表述才会合并到同一节点。

```mermaid
mindmap
  root(("RAG-05 Embedding"))
    RAG_05_001["RAG-05-001 Embedding 的语义空间与检索作用"]
    RAG_05_002["RAG-05-002 Word2Vec、BERT、SBERT 与现代 Embedding 演进"]
    RAG_05_003["RAG-05-003 对比学习、正负样本和训练目标"]
    RAG_05_004["RAG-05-004 Query 与 Document 的非对称编码"]
    RAG_05_005["RAG-05-005 通用、领域、多语言 Embedding 选择"]
    RAG_05_006["RAG-05-006 向量维度、精度、速度和存储权衡"]
    RAG_05_007["RAG-05-007 Cosine、Inner Product 与 L2 距离"]
    RAG_05_008["RAG-05-008 向量归一化与相似度实现细节"]
    RAG_05_009["RAG-05-009 Matryoshka 与可截断向量"]
    RAG_05_010["RAG-05-010 Embedding Benchmark 与业务数据集评估"]
    RAG_05_011["RAG-05-011 批量 Embedding、缓存与吞吐优化"]
    RAG_05_012["RAG-05-012 Embedding 模型升级与向量重建"]
```

共 **12** 个原子知识点。来源映射和事实核验状态以 `audits/rag/` 为准。

# 来源管理

`sources/` 是证据目录，不是第三方资料镜像。

## 规则

1. 每个来源必须记录 URL、固定 Commit、拉取日期和许可状态。
2. 每个进入标准知识库的结论必须能回溯到至少一个来源单元。
3. 未声明许可证的来源只保存必要的定位信息，不复制发布完整正文。
4. 上游更新不能直接覆盖标准知识库，必须先生成差异并重新审计。
5. PDF、图片和项目清单可以登记为参考资源，但不会因主导图篇幅限制而消失。

RAG 的首批纳管文件见 [`rag-scope.json`](rag-scope.json)。

## 检索增强生成（Retrieval-Augmented Generation，RAG）扩充入口

- [`rag-current-sources.json`](rag-current-sources.json)：论文、官方文档、官方代码仓库、工程实践和公开题目的当前来源登记；
- [`rag-search-matrix.json`](rag-search-matrix.json)：18 个流程节点（Pipeline Stage）的中英文检索矩阵与阶段性饱和规则；
- [`../audits/rag/search-coverage.json`](../audits/rag/search-coverage.json)：逐节点检索轮次和覆盖状态；
- [`../audits/rag/search-logs/`](../audits/rag/search-logs/)：实际检索式、候选来源、取舍、冲突和缺口记录；
- [`../templates/source-search-log.md`](../templates/source-search-log.md)：后续检索轮次的统一模板。

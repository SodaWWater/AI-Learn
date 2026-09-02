# 检索增强生成（Retrieval-Augmented Generation，RAG）第二轮 12/18 检查点

日期：2026-09-02

工作项：`WP-P2-002`

状态：`in_progress`

## 本检查点结果

- 第一轮节点检索：18/18；
- 第二轮节点检索：12/18；
- 已登记来源：108；
- 已登记公开工程问题/面试题线索：24；
- 当前覆盖饱和（Coverage Saturated）节点：0/18。

本批完成：

1. 查询路由（Query Routing）；
2. 检索（Retrieval）；
3. 结果融合（Result Fusion）；
4. 重排序（Reranking）。

## 本批新增的重要边界

- 路由选择不只取决于查询复杂度，还取决于查询—语料兼容性（Query–Corpus Compatibility）、最终任务效果、成本和权限；
- 多跳检索（Multi-hop Retrieval）的后续查询依赖中间证据，需分别诊断跳数覆盖、干扰锁定（Distractor Latch）、过早停止（Early Stop）和组合失败；
- 排名融合（Rank Fusion）与分数融合（Score Fusion）依赖不同契约，归一化、候选预算、层级去重和访问控制列表（Access Control List，ACL）不可省略；
- 最大边际相关性（Maximal Marginal Relevance，MMR）解决相关性—冗余权衡，动态重排序（Dynamic Reranking）进一步把文档数和生成效用纳入选择；
- Cross-Encoder（交叉编码器）的模型、候选数、批大小、最大长度、精度和推理后端共同构成生产配置，必须按目标硬件和流量回归。

## 公开题目新增

- `RAG-SCENE-023`：检索偏置（Retrieval Bias）、证据不足、拒答、回退和迭代检索的选择；
- `RAG-SCENE-024`：多文档事实、时间或观点冲突的可信度、交叉验证和显式呈现。

两项均来自可定位公开题库，不标记为企业真实面经，页面答案不作为技术结论证据。

## 为什么仍未标记覆盖饱和

四个节点的第二轮均发现新的知识类型或问题类型，连续无新增类型轮数仍为 0。项目规则要求至少连续两轮独立补漏没有新增类型，并完成来源、冲突、九类覆盖和图谱前置项后，才能标记当前版本的覆盖饱和（Coverage Saturated）。

## 下一步

继续第二轮：上下文组装（Context Assembly）、答案生成（Answer Generation）、引用核验（Citation Verification）、评估（Evaluation）、生产治理（Production Governance）和高级检索增强生成（Advanced RAG）。

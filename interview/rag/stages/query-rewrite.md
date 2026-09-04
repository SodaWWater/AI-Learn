# 查询改写（Query Rewrite）节点问题集合

> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`
>
> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。

## 节点边界

查询改写（Query Rewrite）将原始查询转换为适合检索的表达，并控制语义漂移和额外延迟。当前图谱包含 0 个知识原子，并映射 0 道问题。题目来源只证明出处或工程场景，技术结论仍需回到已登记的一手证据。

## 通用诊断路径

1. 先固定原始查询、上下文、模型版本、路由策略和服务目标，再区分理解错误、改写漂移与路由错误。
2. 记录拒识、歧义、长尾表达和新业务类型，使用影子流量与错误样本评估覆盖，而不是只看平均准确率。
3. 将质量收益与额外调用、延迟、成本、隐私和可回滚性一起比较。
4. 图谱未登记的根因或评估关系保持为待验证缺口，不以推断替代证据。

## 问题明细

当前阶段没有图谱 `contains` 原子，无法建立受控问题映射；这是结构性覆盖缺口，不新增无来源题目。

## 来源与限制

- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。
- 第一人称面经（First-person Interview Report）、公开题库（Public Question Bank）和项目型考题（Project Interview Exercise）只证明题目出处或场景，不证明企业官方面试事实。
- 当前状态为 inventory-only；正式页面仍需按模板补充完整现象、根因分支、方案权衡、实现细节和验证证据。

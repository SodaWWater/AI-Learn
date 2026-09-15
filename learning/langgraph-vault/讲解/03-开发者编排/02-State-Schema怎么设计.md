---
id: LANGGRAPH-P3-02
title: State Schema 怎么设计
status: teaching_draft
---

# 02｜State Schema 怎么设计：不是“把所有变量都塞进去”

State（状态）是 Graph 中多个 Node 共同读写的应用状态。Part 2 里我们看到它会从 S0 一直演化到最终结果；Part 3 要反过来决定：**哪些字段应该进入 State？**

## 1. 先用一句话判断

> 如果一份信息需要跨 Node 共享、影响后续控制流，或者需要随 Graph 生命周期被持久化，那么它通常适合进入 State。

反过来，一个函数内部只用一次的临时变量，通常没必要进入 State。

## 2. 本项目的 State

```python
import operator
from typing import Annotated
from typing_extensions import TypedDict

class AnalysisState(TypedDict, total=False):
    user_query: str
    analysis_month: str
    analysis_plan: list[str]
    data_rows: list[dict]
    data_quality_ok: bool
    errors: list[str]
    metrics: dict[str, float]
    anomalies: list[str]
    drilldown_results: Annotated[list[dict], operator.add]
    findings: list[str]
    report: str
```

`TypedDict` 主要负责描述“这个 State 有哪些 key、每个 key 大概是什么类型”。LangGraph 官方 Graph API 当前也把 `TypedDict` 作为主要 State Schema 写法之一。

## 3. 一张字段责任表比只看代码更重要

| 字段 | 谁写 | 谁读 | 为什么放 State |
|---|---|---|---|
| `user_query` | App 输入 | plan / report | 整个任务都可能需要 |
| `analysis_plan` | plan Node | 后续分析 Node | 跨步骤共享计划 |
| `data_rows` | load Node | validate / metrics | 多步骤使用数据 |
| `data_quality_ok` | validate | routing | 直接决定控制流 |
| `metrics` | calculate | detect / report | 后续异常判断依赖 |
| `anomalies` | detect | drilldown routing | 决定是否下钻 |
| `drilldown_results` | 三个并行 Node | synthesize | 多 Worker 汇总 |
| `findings` | synthesize | report | 报告需要 |
| `report` | report Node | App 输出 | 最终结果 |

## 4. 为什么 `drilldown_results` 要用 `Annotated[..., operator.add]`

```python
drilldown_results: Annotated[list[dict], operator.add]
```

这行里有两个层次：

- `Annotated[...]` 是 Python 类型系统提供的元数据能力；
- `operator.add` 被 LangGraph 读取为这个 State key 的 reducer（合并规则）。

假设当前：

```python
left = [
    {"dimension": "category", "finding": "黄芪上涨明显"}
]
```

另一个并行 Node 返回：

```python
right = [
    {"dimension": "company", "finding": "药材公司 B 贡献最大"}
]
```

Reducer 做的事情就是：

```python
new_value = operator.add(left, right)
```

得到：

```python
[
    {"dimension": "category", "finding": "黄芪上涨明显"},
    {"dimension": "company", "finding": "药材公司 B 贡献最大"},
]
```

如果没有 reducer，官方默认语义是**新更新覆盖旧值**。并行 Node 同时写一个 key 时，这种设计往往就不符合我们的“汇总多个分析结果”需求。

## 5. 类比：State 是共享项目看板，不是每个人的草稿纸

共享项目看板应该放：

- 当前目标；
- 当前阶段结果；
- 下一个岗位需要的信息；
- 需要保存和恢复的信息。

但某个分析员自己算到一半的循环变量、临时 DataFrame、数据库连接对象，不一定适合放在共享看板上。

## 6. 大表到底要不要直接放 State？

教学代码会直接放 5 条数据，方便观察。但生产环境可能有几百万行。

真实系统更可能保存：

```python
{
    "dataset_id": "procurement-2026-08",
    "query_id": "q_123",
    "summary": {...}
}
```

而不是把完整大表塞进 Checkpoint。

是否把数据放 State，需要考虑：

- 数据大小；
- Checkpoint 序列化成本；
- 安全与敏感字段；
- 是否需要恢复后重新访问；
- 外部数据是否可稳定重取。

## 7. State 和 Runtime Context 不要混

“分析出了什么”属于 State；“这次运行连接哪个数据库、当前租户是谁、使用哪个模型配置”更像 Runtime Context。

可以先记：

```text
State = 任务本身正在变化的事实
Context = 运行这次任务所需的外部依赖 / 配置
```

## 8. State 设计常见坏味道

- 什么都塞 State，导致持久化对象巨大；
- 所有 Node 都读所有字段，职责耦合；
- 多个并行 Node 写同一 key，却没有 reducer；
- 把数据库连接、客户端实例等不可序列化对象放入需要 Checkpoint 的 State；
- 用 State 代替真正的长期业务数据库。

> [!important]
> State Schema 本质上是在设计 Graph 内部的“共享协议”。字段不是越多越好，而是要让不同 Node 清楚地知道它们如何交换事实。
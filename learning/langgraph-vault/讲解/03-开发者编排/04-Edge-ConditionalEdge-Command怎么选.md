---
id: LANGGRAPH-P3-04
title: Edge、Conditional Edge、Command 怎么选
status: teaching_draft
---

# 04｜Edge、Conditional Edge、Command 怎么选

它们都和“下一步去哪”有关，但职责不完全一样。

## 1. 普通 Edge：下一步固定

```python
builder.add_edge("plan_analysis", "load_data")
builder.add_edge("load_data", "validate_data")
```

适合：

```text
A 做完以后一定到 B
```

类比成生产线里的固定传送带。

## 2. Conditional Edge：下一步由当前 State 决定

数据质量检查后：

```python
def route_after_validation(state: AnalysisState):
    if state["data_quality_ok"]:
        return "calculate_metrics"
    return "data_error"
```

注册：

```python
builder.add_conditional_edges(
    "validate_data",
    route_after_validation,
    ["calculate_metrics", "data_error"],
)
```

它的特点是：**router 主要负责读 State 和返回目标 Node 名，不负责完成主要业务工作。**

类比成高速公路分叉口：看路牌和当前条件决定走哪条路。

## 3. Conditional Edge 可以一次路由到多个 Node

异常检测后，如果要同时做三个维度分析：

```python
def route_after_detection(state: AnalysisState):
    if not state["anomalies"]:
        return "generate_report"
    return [
        "analyze_category",
        "analyze_company",
        "analyze_supplier",
    ]
```

这会形成 fan-out：多个 Node 在同一轮被激活。

## 4. Command：在 Node 内同时更新 State + 决定 goto

有时 Node 在完成业务工作以后已经知道下一步，而且这个决定与刚产生的 State Update 强绑定。

官方当前提供 `Command`：

```python
from langgraph.types import Command
from typing import Literal

def decide_next(state: AnalysisState) -> Command[
    Literal["calculate_metrics", "data_error"]
]:
    ok = check_data(state["data_rows"])
    return Command(
        update={"data_quality_ok": ok},
        goto="calculate_metrics" if ok else "data_error",
    )
```

这和“Node 返回 update + 另写 Conditional Edge”相比，区别主要在代码组织方式。

## 5. 怎么选

| 情况 | 更自然的选择 |
|---|---|
| A 后面永远是 B | Edge |
| Node 做完后，单独根据 State 进行路由 | Conditional Edge |
| 同一个 Node 既产生关键 State Update，又紧接着决定去哪 | Command |
| 运行时动态创建多个 Worker | Send |

这不是绝对规则，而是可读性和职责边界的选择。

## 6. 为什么不建议“所有地方都用 Command”

`Command` 很强，但如果每个 Node 都把控制流藏在函数内部，Graph 的静态结构会变得不够直观。

对于我们这种需要面试解释和架构可视化的学习项目：

- 固定路径优先 Edge；
- 清晰分支优先 Conditional Edge；
- 状态更新和 goto 强耦合时再用 Command。

这样图结构更容易阅读。

## 7. 一个完整片段

```python
builder.add_edge(START, "plan_analysis")
builder.add_edge("plan_analysis", "load_data")
builder.add_edge("load_data", "validate_data")

builder.add_conditional_edges(
    "validate_data",
    route_after_validation,
    ["calculate_metrics", "data_error"],
)
```

你现在应该能看到：

```text
Node 负责做事
Edge / Conditional Edge 负责流转
Command 可以把做事后的 update 与 goto 合在一次返回里
```

> [!important]
> 面试里真正值得解释的不是“API 名字不同”，而是控制流放在哪里、是否和业务更新耦合，以及这种选择对 Graph 可读性有什么影响。
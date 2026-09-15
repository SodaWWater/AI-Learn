---
id: LANGGRAPH-P3-07
title: compile、invoke、stream 怎么串起来
status: teaching_draft
---

# 07｜compile、invoke、stream 怎么串起来

很多初学者看到：

```python
builder = StateGraph(...)
graph = builder.compile()
graph.invoke(...)
```

会把它们当成三行固定模板。实际上它们分别属于**定义、编译、运行**三个阶段。

## 1. 定义阶段：还没有真正处理用户任务

```python
builder = StateGraph(AnalysisState)
builder.add_node("load_data", load_data)
builder.add_edge(START, "load_data")
```

你在描述：

- State 结构；
- Graph 里有哪些 Node；
- Node 之间如何连接。

## 2. compile：把定义变成可执行 Graph

```python
graph = builder.compile()
```

官方当前说明 `compile()` 会对图结构做基本检查，也是接入 Checkpointer 等运行参数的位置。

类比：前面画的是生产线设计图；`compile()` 像把设计图装配成可以开机的生产线。

## 3. invoke：运行一次并等待最终结果

```python
result = graph.invoke(initial_state)
```

适合你只关心：

```text
输入 → 最终 State
```

比如：

```python
result = graph.invoke({
    "user_query": "分析 2026 年 8 月采购异常",
    "analysis_month": "2026-08",
    "drilldown_results": [],
})

print(result["report"])
```

## 4. stream：边运行边观察

学习和前端交互时，`stream()` 很有价值。

```python
for chunk in graph.stream(
    initial_state,
    stream_mode="updates",
    version="v2",
):
    print(chunk)
```

`updates` 关注的是每一步**哪个 Node 更新了什么**，特别适合你观察 Part 2 中的 State 演化。

当前官方 Streaming 文档还支持多种模式，例如：

- `values`：完整 State 值；
- `updates`：每步 State Update；
- `messages`：LLM message / token；
- `custom`：自定义进度事件；
- `checkpoints`：Checkpoint 事件；
- `tasks`：任务开始 / 结束事件；
- `debug`：更完整的调试信息。

Part 3 先掌握 `updates` 即可。

## 5. 一个常见前端场景

用户提交“生成采购分析报告”后，如果你只用 `invoke()`，前端可能一直转圈。

使用 Streaming 可以向前端暴露：

```text
已完成：数据加载
已完成：指标计算
正在执行：三个维度下钻
已完成：综合归因
正在生成：报告
```

这里不一定全部来自 token streaming，也可以是 Node progress / custom event。

## 6. Graph 可视化

编译后可以从 Graph 对象取得结构用于可视化，例如官方示例经常调用 `graph.get_graph().draw_mermaid_png()`。

对学习而言，最重要的是做到：

```text
代码 add_node / add_edge
      ↓
可以重新画成 Graph
      ↓
运行 stream 时能看到这些 Node 依次产生 update
```

这三者要对应起来。

> [!important]
> `compile()` 负责从“图定义”得到可运行对象；`invoke()` 关心最终结果；`stream()` 让运行过程本身也成为可观察的输出。
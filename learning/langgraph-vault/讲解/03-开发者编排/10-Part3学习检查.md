---
id: LANGGRAPH-P3-10
title: Part 3 学习检查
status: teaching_draft
---

# 10｜Part 3 学习检查

这不是背 API 参数，而是检查你能否把业务需求变成一个 LangGraph 设计。

## 检查 1：拿到需求会先做什么

正确方向：

```text
先画业务执行步骤和分支
→ 再设计 State
→ 再拆 Node
→ 再设计控制流
```

而不是先写一个大 Prompt。

## 检查 2：能否解释 State Schema

至少能说明：

- 为什么 `metrics` 放 State；
- 为什么临时循环变量不需要放 State；
- 为什么并行 Worker 共写的 `drilldown_results` 需要 reducer；
- 为什么生产环境不一定把整张大表放 State。

## 检查 3：能否区分 Node、LLM、Tool

你应该能直接说：

```text
Node 是 Graph 执行位置
LLM 是 Node 可调用的推理 / 生成能力
Tool 是 Node / Agent 可调用的外部能力
```

## 检查 4：能否选择控制方式

- 固定 A → B：Edge；
- 根据 State 分支：Conditional Edge；
- Node 同时产生 Update 并决定 goto：Command；
- 动态 N 个 Worker：Send。

不是死记 API，而是说明为什么。

## 检查 5：能否解释并行 + Reducer

面对：

```text
品类 / 公司 / 供应商三个分析并行
```

你应该知道：

- 三个 Node 属于同一 Super-step；
- 它们不会通过随机先后顺序读取彼此刚写的 State；
- 各自返回 State Update；
- Reducer 把 `drilldown_results` 合并；
- 下一个 Super-step 的 `synthesize_findings` 再读完整结果。

## 检查 6：能否解释 compile 和 invoke

```text
StateGraph + add_node + add_edge = 定义图
compile() = 生成可执行 Graph
invoke() / stream() = 真正开始一次运行
```

## 检查 7：能否接入持久化

至少知道：

```python
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
config = {"configurable": {"thread_id": "..."}}
```

并能解释 `InMemorySaver` 只适合学习 / 测试。

## 检查 8：能否看懂完整代码

打开 [[../../示例代码/Part3-采购经营分析Graph.py|完整代码]]，尝试不看正文回答：

1. State 在哪里定义？
2. 哪几个 Node 是确定性计算？
3. 哪两个位置发生 Conditional Routing？
4. 哪里发生并行？
5. 为什么 `drilldown_results` 有 reducer？
6. Checkpointer 在哪里接入？
7. Runtime 从哪一行真正开始？

如果大部分能答出来，前三个 Part 的基础阶段就可以结束。

## 下一阶段

Part 4 会开始切换到面试追问方式：

- State 和普通变量有什么区别？
- Reducer 为什么存在？
- Edge 和 Command 怎么选？
- Checkpointer 保存什么？
- Thread 和 Store 有什么区别？
- Super-step 为什么影响并行和恢复？
- ToolNode 和普通 Node 有什么区别？

这时每道题都会回到前三个 Part 的整体地图，而不是重新孤立背概念。
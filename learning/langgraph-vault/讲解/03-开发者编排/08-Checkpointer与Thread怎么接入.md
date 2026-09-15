---
id: LANGGRAPH-P3-08
title: Checkpointer 与 Thread 怎么接入
status: teaching_draft
---

# 08｜Checkpointer 与 Thread 怎么接入代码

Part 2 已经理解：Thread 是一条持续的执行状态线，Checkpoint 是状态快照，Checkpointer 负责保存这些快照。现在只看“代码怎么接进来”。

## 1. 编译时接入 Checkpointer

教学环境可以使用：

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
```

官方当前明确说明：`InMemorySaver` / `MemorySaver` 只把 Checkpoint 存在内存里，进程重启就会丢失，因此适合学习 / 测试，不是生产持久化方案。

## 2. invoke 时提供 thread_id

```python
config = {
    "configurable": {
        "thread_id": "procurement-analysis-2026-08-001"
    }
}

result = graph.invoke(initial_state, config=config)
```

现在这次运行就属于指定 Thread。

## 3. 类比：编译时装档案系统，运行时给任务一个案件号

```text
compile(checkpointer=...)
        ↓
系统具备保存档案的能力

thread_id
        ↓
告诉系统：这次运行属于哪一个持续任务
```

没有 `thread_id`，Checkpointer 就无法把一系列 Checkpoint 组织到正确 Thread 下。

## 4. Thread ID 应该是什么

它应该是稳定的“执行上下文标识”，例如：

```text
procurement-analysis-2026-08-001
```

而不是把用户所有业务数据都拼进一个超长字符串。

真实系统里通常会用业务任务 ID、会话 ID 或 UUID。

## 5. Checkpointer 不是业务数据库

Checkpointer 保存 Graph 执行状态，不代表它应该替代：

- 采购事实表；
- ERP；
- 报表仓库；
- 用户权限数据库。

可以理解成：

```text
业务数据库：真实业务事实
Checkpointer：Agent 执行到哪里、当时 State 是什么
```

## 6. Store 也不要混进来

同一个采购分析任务当前执行状态：Checkpointer / Thread。

跨多个 Thread 长期记住：

> 这个用户偏好先看公司，再看品类。

这类长期信息更适合 Store。

## 7. 为什么现在就要考虑持久化

虽然 Part 3 只是基础代码，但持久化不是上线前最后加的一行配置。State 里存什么、Node 是否有外部副作用、任务是否可能等待人工确认，都会受到恢复语义影响。

生产级细节，例如：

- 恢复时某 Node 是否会重执行；
- 外部 API 已成功但响应丢失怎么办；
- 如何设计幂等键；

会放到 Part 5。

> [!important]
> Part 3 只要能写出 `compile(checkpointer=...)` + `thread_id`，并准确解释它们在整个生命周期中的位置，就达标。
---
id: LANGGRAPH-P2-07
title: Part 2 学习检查
status: teaching_draft
---

# 07｜Part 2 学习检查：你能不能在脑中真正跑一次 Graph？

Part 2 的验收不是背 API，也不是把术语逐个定义一遍。

## 检查 1：不用资料，说出一条完整执行链

你应该能够顺着说：

```text
用户输入
→ graph.invoke
→ Runtime 接收 / 加载 State
→ START 激活首个 Node
→ Node 读取 State
→ 普通代码 / LLM / Tool 完成工作
→ Node 返回 State Update
→ Reducer 应用更新
→ 得到 Updated State
→ Edge / Conditional Edge 决定下一批 Node
→ 继续下一 Super-step
→ parallel fan-out / fan-in
→ report
→ END
```

如果中间某一步你只能背词，但说不出“前一步为什么导致它出现”，就回到对应笔记。

## 检查 2：拿真实数据讲 State

看到这条记录：

```text
乙公司 / 中药材 / 供应商C / 数量1600 / 本期55 / 去年41
```

你应该能解释：

1. `load_data` 后，它如何进入 State；
2. `calculate_metrics` 后，为什么得到约 34.1% 涨幅；
3. `detect_anomalies` 后为什么进入 anomalies；
4. 后续三个并行 Node 为什么都能读到这一异常；
5. 各分支结果如何通过 Reducer 汇总到 `drilldown_results`。

## 检查 3：分清 Node、LLM、Tool、Runtime

你应该能回答：

- LLM 想调用工具时，是否等于工具已经执行？——不是。
- Tool 是否就是 Node？——不是，Tool 是能力，Node 是 Graph 执行单位。
- Node 是否一定调用 LLM？——不是。
- 谁决定“现在执行哪个 Node”？——Graph Runtime 根据 Edge / Routing 推进。

## 检查 4：解释同一 Super-step 的并行语义

你应该能解释：

> `analyze_category`、`analyze_company`、`analyze_supplier` 在同一 Super-step 中基于同一轮开始时可见的 State 执行；它们的 State Update 在该轮结束时通过对应 Reducer 形成新的 State，后续 `synthesize_findings` 才读取汇总结果。

不需要背 Pregel 算法细节，但必须知道 Super-step 是并行状态语义的重要边界。

## 检查 5：解释 Checkpoint 的位置

你应该能区分：

```text
Thread      = 这条持续执行 / 会话状态线的 ID
Checkpoint  = 某个 Super-step 边界上的 Graph 状态快照
Checkpointer= 保存和读取这些 Checkpoint 的组件
Store       = 跨 Thread 的长期应用数据
```

同时知道 Checkpoint 不等于“每行代码自动存档”。

## 检查 6：把三张图画出来

如果你能手画下面三张图，Part 2 基本达到目标：

### 图 A：业务 Graph

```text
Plan → Load → Validate → Metrics → Detect
                              ↓
                 Category / Company / Supplier
                              ↓
                         Synthesize → Report
```

### 图 B：Runtime Loop

```text
State → Node → Update → Reducer → New State → Routing → Next Node
```

### 图 C：Persistence

```text
Thread
 ├─ Checkpoint 0
 ├─ Checkpoint 1
 ├─ Checkpoint 2
 └─ ...
```

## Part 2 还没有要求你会什么

你现在仍然不必：

- 独立从零写出完整 Graph；
- 掌握所有 `StateGraph` API 参数；
- 设计生产级 State Schema；
- 处理 Tool 失败重试、业务幂等和权限；
- 解释 interrupt 重执行边界；
- 设计 Supervisor / Handoff 多 Agent。

这些内容不应该抢走 Part 2 的目标。

## 下一步 Part 3 要解决什么

Part 3 会反过来站在开发者视角：拿今天已经看懂的这次运行，真正设计并编排它：

```text
业务需求
→ State Schema
→ Node 划分
→ Edge / Conditional Edge
→ Parallel / Reducer
→ LLM / Tool 接入
→ compile
→ invoke / stream
→ Checkpointer
```

Part 2 是“看懂系统怎么跑”；Part 3 才是“自己把系统搭出来”。

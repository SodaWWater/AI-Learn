---
id: LANGGRAPH-P3-03
title: Node 怎么拆、怎么写
status: teaching_draft
---

# 03｜Node 怎么拆、怎么写：Node 是执行单元，不等于 LLM

官方 Graph API 的核心定义很直接：Node 是函数，它读取当前 State，执行计算或副作用，然后返回 State Update。

## 1. 一个最典型的 Node

```python
def calculate_metrics(state: AnalysisState):
    rows = state["data_rows"]
    metrics = calculate_category_increase(rows)
    return {"metrics": metrics}
```

这里可以拆成三步：

```text
读 State
→ 做工作
→ 返回 Partial State Update
```

Node **不用返回整个 State**。

如果旧 State 有 10 个字段，这个 Node 只需要更新 `metrics`，那么：

```python
return {"metrics": metrics}
```

就够了。

## 2. 类比：Node 像一个岗位提交“本岗位产出”

数据质量岗位不需要重新抄一遍整份项目资料，只需要交：

```python
{
    "data_quality_ok": True,
    "errors": []
}
```

LangGraph Runtime 再把这些更新合并回共享 State。

## 3. 我们的 Node 怎样拆

```text
plan_analysis        理解任务并生成分析计划
load_data            获取数据
validate_data        做数据质量检查
calculate_metrics    做确定性指标计算
detect_anomalies     发现异常
analyze_category     品类下钻
analyze_company      公司下钻
analyze_supplier     供应商下钻
synthesize_findings  汇总多个分析结果
generate_report      生成报告
```

## 4. 哪些 Node 应该用普通代码

下面这些通常不应该先交给 LLM：

- 求和；
- 分组；
- 同比；
- 日期转换；
- 字段映射；
- 业务阈值判断；
- 数据完整性校验。

原因不是“LLM 一定做不了”，而是这些任务有确定规则，普通代码通常更可复现、更容易测试。

## 5. 哪些 Node 更适合 LLM

例如：

```python
def synthesize_findings(state: AnalysisState):
    # 真实项目里可以在这里调用 llm.invoke(...)
    ...
```

更适合 LLM 的工作包括：

- 从自然语言目标生成分析计划；
- 对多个结构化结果做业务解释；
- 结合知识库写原因分析；
- 把结构化事实组织成报告。

## 6. Node 和 Tool 到底区别在哪

这是非常容易混的地方。

```text
Node = Graph 的执行位置
Tool = 某个 Node / Agent 可以调用的能力
```

比如：

```text
load_data Node
    ↓
query_procurement_data Tool
    ↓
数据中台 API
```

Node 是流程里的“工位”；Tool 是工位使用的“设备”。

某些 Tool 也可以由 `ToolNode` 统一执行，但那仍然是“工具执行逻辑被包装成一个 Graph Node”。

## 7. Node 粒度怎么判断

一个步骤更值得独立成 Node，通常因为它具有下面一种或多种特征：

- 独立输入 / 输出；
- 独立失败边界；
- 独立重试策略；
- 独立并行价值；
- 独立人工审批点；
- 独立可观测性价值；
- 独立状态更新。

## 8. 不要在一个 Node 里偷偷控制整个 Graph

如果一个 Node 内部写成：

```python
def giant_node(state):
    load()
    clean()
    calculate()
    if ...:
        analyze_a()
    else:
        analyze_b()
    report()
```

它当然能运行，但你实际上又把 Graph 退化成一个黑盒大函数。

LangGraph 的价值之一就是把执行边界显式化。

> [!important]
> Node 设计不是“把函数越拆越小”，而是让业务步骤、状态变化、失败边界和控制流具有可解释的结构。
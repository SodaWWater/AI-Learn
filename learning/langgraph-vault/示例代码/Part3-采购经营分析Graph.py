from __future__ import annotations

import operator
from collections.abc import Sequence
from typing import Annotated, Literal

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph


class PurchaseRow(TypedDict):
    company: str
    category: str
    supplier: str
    quantity: int
    current_price: float
    last_year_price: float


class DrilldownResult(TypedDict):
    dimension: str
    key: str
    finding: str


class AnalysisState(TypedDict, total=False):
    user_query: str
    analysis_month: str
    analysis_plan: list[str]
    data_rows: list[PurchaseRow]
    data_quality_ok: bool
    errors: list[str]
    metrics: dict[str, float]
    anomalies: list[str]
    drilldown_results: Annotated[list[DrilldownResult], operator.add]
    findings: list[str]
    report: str


TEACHING_ROWS: list[PurchaseRow] = [
    {
        "company": "制造公司 A",
        "category": "黄芪",
        "supplier": "供应商甲",
        "quantity": 1000,
        "current_price": 48.0,
        "last_year_price": 40.0,
    },
    {
        "company": "制造公司 A",
        "category": "当归",
        "supplier": "供应商乙",
        "quantity": 500,
        "current_price": 72.0,
        "last_year_price": 70.0,
    },
    {
        "company": "药材公司 B",
        "category": "黄芪",
        "supplier": "供应商丙",
        "quantity": 1600,
        "current_price": 55.0,
        "last_year_price": 41.0,
    },
    {
        "company": "药材公司 B",
        "category": "包材",
        "supplier": "供应商丁",
        "quantity": 800,
        "current_price": 12.0,
        "last_year_price": 12.0,
    },
    {
        "company": "制造公司 C",
        "category": "原料药",
        "supplier": "供应商戊",
        "quantity": 600,
        "current_price": 91.0,
        "last_year_price": 80.0,
    },
]


def plan_analysis(state: AnalysisState) -> dict:
    """教学版：用确定性结果代替真实 LLM 规划。"""
    return {
        "analysis_plan": [
            "加载采购明细",
            "校验数据质量",
            "计算同比价格变化",
            "识别异常品类",
            "从品类、公司、供应商三个维度并行下钻",
            "综合结论并生成报告",
        ]
    }


def load_data(state: AnalysisState) -> dict:
    """教学版：真实项目可替换为 SQL、API 或数据平台 Tool。"""
    return {"data_rows": TEACHING_ROWS}


def validate_data(state: AnalysisState) -> dict:
    errors: list[str] = []
    for index, row in enumerate(state["data_rows"]):
        if row["quantity"] <= 0:
            errors.append(f"row {index}: quantity must be positive")
        if row["current_price"] <= 0 or row["last_year_price"] <= 0:
            errors.append(f"row {index}: prices must be positive")

    return {
        "data_quality_ok": not errors,
        "errors": errors,
    }


def route_after_validation(
    state: AnalysisState,
) -> Literal["calculate_metrics", "data_error"]:
    if state["data_quality_ok"]:
        return "calculate_metrics"
    return "data_error"


def data_error(state: AnalysisState) -> dict:
    return {
        "report": "数据质量检查失败：" + "; ".join(state.get("errors", []))
    }


def calculate_metrics(state: AnalysisState) -> dict:
    """按品类计算简单平均同比涨幅，演示确定性计算 Node。"""
    by_category: dict[str, list[float]] = {}

    for row in state["data_rows"]:
        increase = (row["current_price"] - row["last_year_price"]) / row[
            "last_year_price"
        ]
        by_category.setdefault(row["category"], []).append(increase)

    metrics = {
        category: sum(values) / len(values)
        for category, values in by_category.items()
    }
    return {"metrics": metrics}


def detect_anomalies(state: AnalysisState) -> dict:
    """教学规则：平均同比涨幅 >= 15% 视为异常。"""
    anomalies = [
        category
        for category, increase in state["metrics"].items()
        if increase >= 0.15
    ]
    return {"anomalies": anomalies}


def route_after_detection(state: AnalysisState) -> Sequence[str] | str:
    if not state["anomalies"]:
        return "generate_report"
    return [
        "analyze_category",
        "analyze_company",
        "analyze_supplier",
    ]


def _largest_price_increase_row(rows: list[PurchaseRow]) -> tuple[PurchaseRow, float]:
    row = max(
        rows,
        key=lambda item: (item["current_price"] - item["last_year_price"])
        / item["last_year_price"],
    )
    increase = (row["current_price"] - row["last_year_price"]) / row[
        "last_year_price"
    ]
    return row, increase


def analyze_category(state: AnalysisState) -> dict:
    abnormal_rows = [
        row for row in state["data_rows"] if row["category"] in state["anomalies"]
    ]
    row, increase = _largest_price_increase_row(abnormal_rows)
    result: DrilldownResult = {
        "dimension": "category",
        "key": row["category"],
        "finding": f"{row['category']} 单条记录最大同比涨幅约 {increase:.1%}",
    }
    return {"drilldown_results": [result]}


def analyze_company(state: AnalysisState) -> dict:
    abnormal_rows = [
        row for row in state["data_rows"] if row["category"] in state["anomalies"]
    ]
    row, increase = _largest_price_increase_row(abnormal_rows)
    result: DrilldownResult = {
        "dimension": "company",
        "key": row["company"],
        "finding": f"{row['company']} 存在本次异常记录，最高同比涨幅约 {increase:.1%}",
    }
    return {"drilldown_results": [result]}


def analyze_supplier(state: AnalysisState) -> dict:
    abnormal_rows = [
        row for row in state["data_rows"] if row["category"] in state["anomalies"]
    ]
    row, increase = _largest_price_increase_row(abnormal_rows)
    result: DrilldownResult = {
        "dimension": "supplier",
        "key": row["supplier"],
        "finding": f"{row['supplier']} 对应记录同比涨幅约 {increase:.1%}",
    }
    return {"drilldown_results": [result]}


def synthesize_findings(state: AnalysisState) -> dict:
    """教学版：真实项目可替换为 LLM + 业务知识。"""
    findings = [item["finding"] for item in state["drilldown_results"]]
    return {"findings": findings}


def generate_report(state: AnalysisState) -> dict:
    if state.get("report"):
        return {}

    anomaly_text = "、".join(state.get("anomalies", [])) or "未发现达到阈值的异常品类"
    finding_lines = state.get("findings", [])

    report_lines = [
        f"分析月份：{state['analysis_month']}",
        f"异常品类：{anomaly_text}",
    ]
    report_lines.extend(f"- {finding}" for finding in finding_lines)

    return {"report": "\n".join(report_lines)}


def build_graph():
    builder = StateGraph(AnalysisState)

    builder.add_node("plan_analysis", plan_analysis)
    builder.add_node("load_data", load_data)
    builder.add_node("validate_data", validate_data)
    builder.add_node("data_error", data_error)
    builder.add_node("calculate_metrics", calculate_metrics)
    builder.add_node("detect_anomalies", detect_anomalies)
    builder.add_node("analyze_category", analyze_category)
    builder.add_node("analyze_company", analyze_company)
    builder.add_node("analyze_supplier", analyze_supplier)
    builder.add_node("synthesize_findings", synthesize_findings)
    builder.add_node("generate_report", generate_report)

    builder.add_edge(START, "plan_analysis")
    builder.add_edge("plan_analysis", "load_data")
    builder.add_edge("load_data", "validate_data")

    builder.add_conditional_edges(
        "validate_data",
        route_after_validation,
        ["calculate_metrics", "data_error"],
    )
    builder.add_edge("data_error", END)

    builder.add_edge("calculate_metrics", "detect_anomalies")
    builder.add_conditional_edges(
        "detect_anomalies",
        route_after_detection,
        [
            "analyze_category",
            "analyze_company",
            "analyze_supplier",
            "generate_report",
        ],
    )

    builder.add_edge("analyze_category", "synthesize_findings")
    builder.add_edge("analyze_company", "synthesize_findings")
    builder.add_edge("analyze_supplier", "synthesize_findings")
    builder.add_edge("synthesize_findings", "generate_report")
    builder.add_edge("generate_report", END)

    checkpointer = InMemorySaver()
    return builder.compile(checkpointer=checkpointer)


def run_demo() -> None:
    graph = build_graph()

    initial_state: AnalysisState = {
        "user_query": "分析 2026 年 8 月集团采购成本变化并生成报告",
        "analysis_month": "2026-08",
        "drilldown_results": [],
    }
    config = {
        "configurable": {
            "thread_id": "procurement-analysis-2026-08-001",
        }
    }

    result = graph.invoke(initial_state, config=config)
    print(result["report"])


if __name__ == "__main__":
    run_demo()

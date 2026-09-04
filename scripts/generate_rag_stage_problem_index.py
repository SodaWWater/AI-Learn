"""Generate the graph-backed RAG stage problem index.

This is a P5-001 inventory projection. It only lists existing problem_question
nodes, their graph-derived stage mappings, provenance and source locators; it
does not create question pages or technical answers.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "knowledge/rag/graph.json"
MODEL_PATH = ROOT / "taxonomy/rag-graph-model.json"
OUTPUT_PATH = ROOT / "interview/rag/stage-problem-index.md"


STAGE_ORDER = (
    "PS-DATA-INGESTION",
    "PS-DOCUMENT-PARSING",
    "PS-DATA-GOVERNANCE",
    "PS-CHUNKING",
    "PS-EMBEDDING",
    "PS-STORAGE-INDEXING",
    "PS-QUERY-UNDERSTANDING",
    "PS-QUERY-REWRITE",
    "PS-QUERY-ROUTING",
    "PS-RETRIEVAL",
    "PS-RESULT-FUSION",
    "PS-RERANKING",
    "PS-CONTEXT-ASSEMBLY",
    "PS-ANSWER-GENERATION",
    "PS-CITATION-VERIFICATION",
    "PS-EVALUATION",
    "PS-PRODUCTION-GOVERNANCE",
    "PS-ADVANCED-RAG",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def node_label(node: dict[str, Any]) -> str:
    return f"{node['label_zh']}（{node['label_en']}）"


def validate(
    nodes: dict[str, dict[str, Any]],
    edges: list[dict[str, Any]],
    relations: set[str],
) -> None:
    missing = sorted(set(STAGE_ORDER) - set(nodes))
    wrong_type = sorted(
        stage_id for stage_id in STAGE_ORDER if stage_id in nodes and nodes[stage_id]["type"] != "pipeline_stage"
    )
    if missing or wrong_type:
        raise ValueError(f"Stage configuration mismatch: missing={missing}, wrong_type={wrong_type}")
    problem_ids = {node_id for node_id, node in nodes.items() if node["type"] == "problem_question"}
    unknown = sorted({edge["type"] for edge in edges} - relations)
    if unknown:
        raise ValueError(f"Graph contains unregistered relations: {unknown}")
    for problem_id in problem_ids:
        if not any(edge["from"] == problem_id and edge["type"] == "problem_at" for edge in edges):
            raise ValueError(f"Problem node has no problem_at mapping: {problem_id}")


def render(graph: dict[str, Any], model: dict[str, Any]) -> str:
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = graph["edges"]
    validate(nodes, edges, {item["id"] for item in model["edge_types"]})

    stage_atoms: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge["type"] == "contains" and edge["from"] in STAGE_ORDER:
            stage_atoms[edge["from"]].add(edge["to"])

    problems = [node for node in nodes.values() if node["type"] == "problem_question"]
    problems_by_stage: dict[str, list[dict[str, Any]]] = defaultdict(list)
    problem_stages: dict[str, list[str]] = defaultdict(list)
    for problem in problems:
        atom_ids = set(problem.get("knowledge_node_ids", []))
        for stage_id in STAGE_ORDER:
            if atom_ids & stage_atoms[stage_id]:
                problems_by_stage[stage_id].append(problem)
                problem_stages[problem["id"]].append(stage_id)

    lines = [
        "# RAG 主干节点工程问题与公开面试题索引（RAG Stage Problem and Public Interview Question Index）",
        "",
        "> 状态：`candidate / WP-P5-001 / graph-backed / inventory-only`",
        ">",
        "> 图谱输入：[`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)；生成器：[`scripts/generate_rag_stage_problem_index.py`](../../scripts/generate_rag_stage_problem_index.py)。",
        "",
        "本索引只投影已有工程问题/面试题（Engineering Problem / Interview Question）节点和图谱关系，不生成答案、不新增题目，也不把公开题库或第一人称面经升级为企业官方面试结论。一个问题可以出现在多个流程节点（Pipeline Stage），这是图谱中的多对多映射。",
        "",
        "## 生成审计（Generation Audit）",
        "",
        f"- 图谱版本：`{graph.get('generated_at', 'unknown')}`；节点：{len(nodes)}；边：{len(edges)}。",
        f"- 流程节点：{len(STAGE_ORDER)}；问题节点：{len(problems)}；已映射问题：{len(problem_stages)}。",
        f"- 未映射问题节点：{len(set(node['id'] for node in problems) - set(problem_stages))}；未映射项必须在正式页面生产前处理。",
        "- 来源定位、来源类型和技术证据边界沿用图谱字段；本索引不把题目来源当作技术结论证据。",
        "",
        "## 18 节点索引（18-stage Index）",
        "",
        "| 顺序 | 流程节点（Pipeline Stage） | 问题数 | 问题 ID |",
        "|---:|---|---:|---|",
    ]
    for index, stage_id in enumerate(STAGE_ORDER, 1):
        stage_problems = sorted(problems_by_stage[stage_id], key=lambda item: item["id"])
        problem_links = ", ".join(f"[`{problem['id']}`](#{problem['id'].lower()})" for problem in stage_problems) or "无"
        lines.append(f"| {index} | {node_label(nodes[stage_id])} [`{stage_id}`] | {len(stage_problems)} | {problem_links} |")
    lines.extend(["", "## 问题明细（Problem Details）", ""])
    for problem in sorted(problems, key=lambda item: item["id"]):
        source_refs = ", ".join(f"`{ref}`" for ref in sorted(problem.get("source_refs", []))) or "无（工程问题或待补来源）"
        stages = ", ".join(f"{node_label(nodes[stage_id])} [`{stage_id}`]" for stage_id in sorted(problem_stages[problem["id"]], key=STAGE_ORDER.index)) or "未映射"
        lines.extend(
            [
                f"<a id=\"{problem['id'].lower()}\"></a>",
                f"### {problem['id']}：{problem['label_zh']}（{problem['label_en']}）",
                "",
                "| 字段 | 内容 |",
                "|---|---|",
                f"| 来源类型（Provenance Type） | `{problem.get('provenance_type', '未声明')}` |",
                f"| 原始定位（Source Locator） | {problem.get('source_locator') or '未声明'} |",
                f"| 来源引用（Source References） | {source_refs} |",
                f"| 关联流程节点（Pipeline Stages） | {stages} |",
                f"| 知识节点（Knowledge Nodes） | {', '.join(f'`{atom_id}`' for atom_id in sorted(problem.get('knowledge_node_ids', []))) or '无'} |",
                "",
                "该条仅作为问题入口；正式页面必须补充工程现象、根因、方案、实现和验证，并继续遵守来源与术语规范。",
                "",
            ]
        )
    lines.extend(
        [
            "## 生产边界（Production Boundary）",
            "",
            "- `first_person_interview` 只证明发布者自述的面试经历；`public_question_bank` 和 `project_interview_exercise` 不证明企业真实面试。",
            "- `engineering_case` 明确标记为工程问题（Engineering Case），不得补写为真实面试题。",
            "- 技术结论必须回到已登记的官方文档（Official Documentation）、官方代码仓库（Official Repository）或原始论文（Original Paper）；本索引不替代证据核验。",
            "- `RAG-07-001` 与 `RAG-13-011` 仍是无来源库存草稿（Inventory Draft），不能在正式页面中作为已核验结论。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.write_text(render(load(GRAPH_PATH), load(MODEL_PATH)), encoding="utf-8")


if __name__ == "__main__":
    main()

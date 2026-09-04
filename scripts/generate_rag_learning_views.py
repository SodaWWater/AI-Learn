"""Generate auditable RAG learning views from the canonical graph inventory.

The generated Markdown is deliberately a projection of ``knowledge/rag/graph.json``:
it does not add sources, graph nodes, graph edges, or knowledge prose.  Static
configuration only partitions existing pipeline-stage IDs into the four workflow
backbones already accepted by WP-P4-001; every configured ID is validated before
rendering.
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "knowledge/rag/graph.json"
MODEL_PATH = ROOT / "taxonomy/rag-graph-model.json"
OUTPUT_PATH = ROOT / "learning/rag/graph-views.md"


# The accepted WP-P4-001 workflow assigns every current pipeline stage to one
# of these four learning backbones. They are graph IDs, not new graph entities.
BACKBONES = (
    (
        "offline",
        "离线知识构建（Offline Knowledge Construction）",
        (
            "PS-DATA-INGESTION",
            "PS-DOCUMENT-PARSING",
            "PS-DATA-GOVERNANCE",
            "PS-CHUNKING",
            "PS-EMBEDDING",
            "PS-STORAGE-INDEXING",
        ),
    ),
    (
        "online",
        "在线问答（Online Query and Answering）",
        (
            "PS-QUERY-UNDERSTANDING",
            "PS-QUERY-REWRITE",
            "PS-QUERY-ROUTING",
            "PS-RETRIEVAL",
            "PS-RESULT-FUSION",
            "PS-RERANKING",
            "PS-CONTEXT-ASSEMBLY",
            "PS-ANSWER-GENERATION",
            "PS-CITATION-VERIFICATION",
        ),
    ),
    (
        "feedback",
        "评估反馈（Evaluation and Feedback）",
        ("PS-EVALUATION",),
    ),
    (
        "governance",
        "生产治理（Production Governance）",
        ("PS-PRODUCTION-GOVERNANCE", "PS-ADVANCED-RAG"),
    ),
)

PROBLEM_PATH_ID = "PQ-RAG-0017"
LOCAL_DETAIL_TYPES = {
    "problem_at",
    "solved_by",
    "implemented_by",
    "evaluated_by",
    "implements",
}
LOCAL_STAGE_EDGE_TYPES = {"contains", "next_stage", "branches_to", "merges_into"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def node_label(node: dict[str, Any]) -> str:
    return f"{node['label_zh']}（{node['label_en']}）"


def node_ref(node: dict[str, Any]) -> str:
    return f"{node_label(node)} [`{node['id']}`]"


def relation_label(edge: dict[str, Any], relations: dict[str, str]) -> str:
    return f"{relations[edge['type']]} `{edge['type']}`"


def edge_ref(
    edge: dict[str, Any], nodes: dict[str, dict[str, Any]], relations: dict[str, str]
) -> str:
    return (
        f"`{edge['id']}`：{node_ref(nodes[edge['from']])} "
        f"→ {node_ref(nodes[edge['to']])}（{relation_label(edge, relations)}）"
    )


def validate_inputs(
    nodes: dict[str, dict[str, Any]], edges: list[dict[str, Any]], relations: dict[str, str]
) -> None:
    configured_stages = [stage for _, _, stages in BACKBONES for stage in stages]
    missing = sorted(set(configured_stages) - set(nodes))
    non_stages = sorted(
        stage for stage in configured_stages if nodes[stage]["type"] != "pipeline_stage"
    )
    if missing or non_stages:
        raise ValueError(
            "Workflow configuration no longer matches the graph: "
            f"missing={missing}, non_pipeline_stage={non_stages}"
        )
    if len(configured_stages) != len(set(configured_stages)):
        raise ValueError("A pipeline stage is assigned to more than one learning backbone.")
    pipeline_stages = {node_id for node_id, node in nodes.items() if node["type"] == "pipeline_stage"}
    if set(configured_stages) != pipeline_stages:
        raise ValueError(
            "Workflow configuration must cover every graph pipeline stage: "
            f"unassigned={sorted(pipeline_stages - set(configured_stages))}, "
            f"unknown={sorted(set(configured_stages) - pipeline_stages)}"
        )
    if PROBLEM_PATH_ID not in nodes or nodes[PROBLEM_PATH_ID]["type"] != "problem_question":
        raise ValueError(f"Configured problem path {PROBLEM_PATH_ID} is not a graph problem node.")
    unknown_relations = sorted({edge["type"] for edge in edges} - set(relations))
    if unknown_relations:
        raise ValueError(f"Graph has relations absent from the controlled model: {unknown_relations}")


def edges_between(
    edges: Iterable[dict[str, Any]], node_ids: set[str], edge_type: str | None = None
) -> list[dict[str, Any]]:
    return sorted(
        (
            edge
            for edge in edges
            if edge["from"] in node_ids
            and edge["to"] in node_ids
            and (edge_type is None or edge["type"] == edge_type)
        ),
        key=lambda edge: edge["id"],
    )


def mermaid(
    node_ids: Iterable[str],
    edges: Iterable[dict[str, Any]],
    nodes: dict[str, dict[str, Any]],
    relations: dict[str, str],
) -> list[str]:
    ordered_nodes = list(dict.fromkeys(node_ids))
    alias = {node_id: f"n{index}" for index, node_id in enumerate(ordered_nodes)}
    lines = ["```mermaid", "flowchart LR"]
    for node_id in ordered_nodes:
        node = nodes[node_id]
        label = f"{node_label(node)}<br/>{node_id}".replace('"', "'")
        lines.append(f'    {alias[node_id]}["{label}"]')
    for edge in sorted(edges, key=lambda item: item["id"]):
        if edge["from"] not in alias or edge["to"] not in alias:
            continue
        label = f"{edge['type']}<br/>{edge['id']}"
        if edge["type"] in {"overlaps_with", "alternative_to", "combined_with", "conflicts_with"}:
            lines.append(f"    {alias[edge['from']]} ---|{label}| {alias[edge['to']]}")
        elif edge["type"] == "contains":
            lines.append(f"    {alias[edge['from']]} -.->|{label}| {alias[edge['to']]}")
        else:
            lines.append(f"    {alias[edge['from']]} -->|{label}| {alias[edge['to']]}")
    lines.append("```")
    return lines


def edge_table(
    edges: Iterable[dict[str, Any]],
    nodes: dict[str, dict[str, Any]],
    relations: dict[str, str],
) -> list[str]:
    rows = ["| 边 ID | 受控关系 | 起点 | 终点 |", "|---|---|---|---|"]
    for edge in sorted(edges, key=lambda item: item["id"]):
        rows.append(
            "| "
            + " | ".join(
                (
                    f"`{edge['id']}`",
                    f"{relations[edge['type']]} `{edge['type']}`",
                    markdown_cell(node_ref(nodes[edge["from"]])),
                    markdown_cell(node_ref(nodes[edge["to"]])),
                )
            )
            + " |"
        )
    return rows


def stage_local_edges(
    stage_id: str,
    outgoing: dict[str, list[dict[str, Any]]],
    incoming: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], set[str], set[str]]:
    """Return a semantically bounded one/two-hop stage projection.

    A generic two-hop walk through ``contains`` would immediately travel from a
    stage to BB-RAG and then to the whole graph. The local map instead follows
    the intended learning boundary: stage -> contained knowledge, adjacent stage
    transitions, then problem/solution/evaluation/implementation relations that
    touch its contained knowledge. This preserves direction on every emitted edge.
    """

    one_hop = [
        edge
        for edge in outgoing[stage_id]
        if edge["type"] in LOCAL_STAGE_EDGE_TYPES
    ] + [
        edge
        for edge in incoming[stage_id]
        if edge["type"] in {"next_stage", "branches_to", "merges_into"}
    ]
    one_hop = sorted({edge["id"]: edge for edge in one_hop}.values(), key=lambda edge: edge["id"])
    contained = {edge["to"] for edge in one_hop if edge["type"] == "contains"}

    two_hop: list[dict[str, Any]] = []
    for node_id in contained:
        two_hop.extend(
            edge
            for edge in incoming[node_id] + outgoing[node_id]
            if edge["type"] in LOCAL_DETAIL_TYPES
        )
    two_hop = sorted({edge["id"]: edge for edge in two_hop}.values(), key=lambda edge: edge["id"])
    node_ids = {stage_id}
    for edge in one_hop + two_hop:
        node_ids.update((edge["from"], edge["to"]))
    return one_hop + two_hop, node_ids, contained


def grouped_node_ids(node_ids: Iterable[str], nodes: dict[str, dict[str, Any]]) -> str:
    groups: dict[str, list[str]] = defaultdict(list)
    for node_id in sorted(node_ids):
        groups[nodes[node_id]["type"]].append(node_id)
    return "; ".join(f"{node_type}: {', '.join(f'`{node_id}`' for node_id in ids)}" for node_type, ids in sorted(groups.items()))


def problem_path_edges(
    problem_id: str,
    outgoing: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    selected = [
        edge
        for edge in outgoing[problem_id]
        if edge["type"] in {"problem_at", "solved_by", "evaluated_by", "supported_by"}
    ]
    solutions = {edge["to"] for edge in selected if edge["type"] == "solved_by"}
    for solution_id in solutions:
        selected.extend(
            edge
            for edge in outgoing[solution_id]
            if edge["type"] in {"implemented_by", "supported_by"}
        )
    return sorted({edge["id"]: edge for edge in selected}.values(), key=lambda edge: edge["id"])


def render(graph: dict[str, Any], model: dict[str, Any]) -> str:
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = sorted(graph["edges"], key=lambda edge: edge["id"])
    relations = {item["id"]: item["name"] for item in model["edge_types"]}
    validate_inputs(nodes, edges, relations)

    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        outgoing[edge["from"]].append(edge)
        incoming[edge["to"]].append(edge)

    stage_ids = [stage for _, _, stages in BACKBONES for stage in stages]
    root_contains = [
        edge
        for edge in outgoing["BB-RAG"]
        if edge["type"] == "contains" and edge["to"] in stage_ids
    ]
    stage_transitions = [edge for edge in edges if edge["type"] == "next_stage"]
    branch_edges = [edge for edge in edges if edge["type"] == "branches_to"]
    merge_edges = [edge for edge in edges if edge["type"] == "merges_into"]
    projection_counts = {
        "backbone_nodes": len([node for node in nodes.values() if node["type"] == "backbone"]),
        "overlap_edges": len([edge for edge in edges if edge["type"] == "overlaps_with"]),
        "branch_edges": len(branch_edges),
        "merge_edges": len(merge_edges),
    }

    # Branch targets are explicit graph nodes (for example Agent or Knowledge
    # Graph). Include them in the global projection so conditional execution
    # is visible without inventing a path through an unrelated backbone.
    global_relation_edges = [*branch_edges, *merge_edges]
    global_relation_node_ids = sorted(
        {endpoint for edge in global_relation_edges for endpoint in (edge["from"], edge["to"])}
    )
    global_edges = [*root_contains, *stage_transitions, *branch_edges, *merge_edges]

    lines = [
        "# 检索增强生成（Retrieval-Augmented Generation，RAG）学习视图",
        "",
        "> 状态：`candidate / WP-P4-002 / generated / graph-first`",
        ">",
        "> 生成器：[`scripts/generate_rag_learning_views.py`](../../scripts/generate_rag_learning_views.py)",
        ">",
        "> 图谱输入：[`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)；图模型：[`taxonomy/rag-graph-model.json`](../../taxonomy/rag-graph-model.json)。",
        "",
        "本页是有向知识图谱（Directed Knowledge Graph）的可重复投影，不是知识章节（Knowledge Chapter）或工程问题/面试题（Engineering Problem / Interview Question）正文。每条图线和表格行都保留图谱节点 ID、边 ID 与受控关系；重新执行生成器会从当前图谱重建本页。",
        "",
        "## 生成边界",
        "",
        f"- 图谱基线：`{graph.get('generated_at', 'unknown')}`，{len(nodes)} 个节点、{len(edges)} 条边。",
        f"- 当前主干（Backbone）：{node_ref(nodes['BB-RAG'])}；流程节点（Pipeline Stage）：{len(stage_ids)} 个。",
        "- 本投影不引入外部来源（External Source），不改变图谱，也不把库存草稿（Inventory Draft）升级为正式内容。来源证据（Source Evidence）仍以图中的 `supported_by` 边为准。",
        "",
        "## 生成审计元数据（Generation Audit Metadata）",
        "",
        "| 投影项 | 图谱受控类型 | 当前计数 | 生成处置 |",
        "|---|---|---:|---|",
        f"| 主干（Backbone） | `backbone` | {projection_counts['backbone_nodes']} | 投影已登记主干。 |",
        f"| 跨主干重叠（Cross-backbone Overlap） | `overlaps_with` | {projection_counts['overlap_edges']} | 仅投影图谱已登记的受控重叠关系；不根据共同主题推断。 |",
        f"| 条件分支（Conditional Branch） | `branches_to` | {projection_counts['branch_edges']} | 投影图谱已登记的条件分支；不推断未登记路径。 |",
        f"| 汇合（Merge） | `merges_into` | {projection_counts['merge_edges']} | 仅投影图谱已登记的汇合关系。 |",
        "",
        "## 全局地铁图（Global Metro Map）",
        "",
        "全局地铁图（Global Metro Map）投影当前主干（Backbone）、流程节点（Pipeline Stage）以及图谱已登记的 `contains`、`next_stage`、`branches_to` 和 `merges_into` 关系。实线表示有向流程或条件分支，虚线表示包含（Contains），汇合关系沿受控边保留。",
        "",
        *mermaid(["BB-RAG", *stage_ids, *global_relation_node_ids], global_edges, nodes, relations),
        "",
        *edge_table(global_edges, nodes, relations),
        "",
            "## 四条 RAG 主干图（Four RAG Backbone Maps）",
        "",
    ]

    for key, title, stages in BACKBONES:
        stage_set = set(stages)
        internal_edges = edges_between(stage_transitions, stage_set, "next_stage")
        boundary_edges = [
            edge
            for edge in stage_transitions
            if (edge["from"] in stage_set) != (edge["to"] in stage_set)
        ]
        lines.extend(
            [
                f"### {title}",
                "",
                f"当前流程节点（Pipeline Stage）：{', '.join(node_ref(nodes[stage]) for stage in stages)}。",
                "",
                *mermaid(stages, internal_edges, nodes, relations),
                "",
                *edge_table(internal_edges, nodes, relations),
                "",
                "与其他主干（Backbone）的已登记衔接：",
                "",
            ]
        )
        if boundary_edges:
            lines.extend(edge_table(boundary_edges, nodes, relations))
        else:
            lines.append("当前没有以 `next_stage` 登记的外部衔接。")
        lines.append("")

    overlap_edges = [edge for edge in edges if edge["type"] == "overlaps_with"]
    backbone_nodes = [node for node in nodes.values() if node["type"] == "backbone"]
    branch_node_ids = sorted({endpoint for edge in branch_edges for endpoint in (edge["from"], edge["to"])})
    lines.extend(
        [
            "## 跨主干重叠图（Cross-backbone Overlap Map）",
            "",
            f"跨主干重叠图（Cross-backbone Overlap Map）只展示图谱中已登记的 `overlaps_with` 关系，并单独列出已登记的条件分支（Conditional Branch）。当前已登记 {len(backbone_nodes)} 个主干（Backbone）、{len(overlap_edges)} 条重叠边和 {len(branch_edges)} 条条件分支；投影不根据共同主题推断未注册关系。",
            "",
        ]
    )
    if overlap_edges:
        overlap_node_ids = sorted({endpoint for edge in overlap_edges for endpoint in (edge["from"], edge["to"])})
        lines.extend(mermaid(overlap_node_ids, overlap_edges, nodes, relations))
        lines.append("")
        lines.extend(edge_table(overlap_edges, nodes, relations))
    else:
        lines.extend(
            [
                "| 已登记主干（Backbone） | `overlaps_with` 边数 | 结论 |",
                "|---|---:|---|",
                f"| {', '.join(node_ref(node) for node in sorted(backbone_nodes, key=lambda item: item['id']))} | 0 | 当前投影为空；待底层图谱登记其他主干和受控重叠关系后自动扩展。 |",
            ]
        )
    lines.append("")

    lines.extend(["### 已登记条件分支（Registered Conditional Branches）", ""])
    if branch_edges:
        lines.extend(mermaid(branch_node_ids, branch_edges, nodes, relations))
        lines.append("")
        lines.extend(edge_table(branch_edges, nodes, relations))
    else:
        lines.append("当前图谱没有登记 `branches_to` 条件分支。")
    lines.append("")

    online_stages = next(stages for key, _, stages in BACKBONES if key == "online")
    query_edges = [
        edge
        for edge in stage_transitions
        if edge["from"] in online_stages and edge["to"] in online_stages
    ]
    query_branch_edges = [edge for edge in branch_edges if edge["from"] in online_stages]
    query_path_edges = [*query_edges, *query_branch_edges]
    query_node_ids = [*online_stages, *sorted({edge["to"] for edge in query_branch_edges})]
    lines.extend(
        [
            "## 用户问题执行路径（User Query Execution Path）",
            "",
            "当前图谱没有独立的用户问题（User Query）节点；因此本路径从查询理解（Query Understanding）开始，严格投影在线问答（Online Query and Answering）的已登记 `next_stage` 与条件分支（`branches_to`）。分支只表示图谱中的可选路由，不表示每个请求都必然执行所有策略。",
            "",
            *mermaid(query_node_ids, query_path_edges, nodes, relations),
            "",
            *edge_table(query_path_edges, nodes, relations),
            "",
        ]
    )

    path_edges = problem_path_edges(PROBLEM_PATH_ID, outgoing)
    path_node_ids = sorted({endpoint for edge in path_edges for endpoint in (edge["from"], edge["to"])})
    lines.extend(
        [
            "## 工程问题反向路径（Engineering Problem Diagnosis Path）",
            "",
            f"本示例从 {node_ref(nodes[PROBLEM_PATH_ID])} 反向定位受影响知识节点（Knowledge Node），并沿已登记解决方案（Solution）、具体实现（Implementation）、评估方法（Evaluation Method）和来源证据（Source Evidence）关系展开。该问题的来源类型和定位仍以图谱节点字段为准。",
            "",
            *mermaid(path_node_ids, path_edges, nodes, relations),
            "",
            *edge_table(path_edges, nodes, relations),
            "",
        ]
    )

    lines.extend(
        [
            "## 流程节点局部图索引（Pipeline-stage Local Map Index）",
            "",
            "为避免主观判断“复杂”，本索引导出全部 18 个流程节点（Pipeline Stage）。每个局部图（Local Node Map）保留一跳的阶段包含（Contains）、下一阶段（Next Stage）、条件分支（Branches To）和汇合（Merges Into）关系；二跳仅沿问题定位（Problem At）、解决方案（Solved By）、具体实现（Implemented By）、评估（Evaluated By）与实现（Implements）关系展开。它不会经由 `BB-RAG` 或来源证据（Source Evidence）节点扩散为全图。",
            "",
            "| 流程节点（Pipeline Stage） | 一跳边数 | 二跳扩展边数 | 局部图锚点 |",
            "|---|---:|---:|---|",
        ]
    )
    local_payloads: list[tuple[str, list[dict[str, Any]], set[str], set[str]]] = []
    for stage_id in stage_ids:
        local_edges, local_nodes, contained = stage_local_edges(stage_id, outgoing, incoming)
        one_hop_count = sum(edge["type"] in LOCAL_STAGE_EDGE_TYPES for edge in local_edges)
        local_payloads.append((stage_id, local_edges, local_nodes, contained))
        lines.append(
            f"| {node_ref(nodes[stage_id])} | {one_hop_count} | {len(local_edges) - one_hop_count} | [查看局部图](#{stage_id.lower()}) |"
        )
    lines.append("")

    for stage_id, local_edges, local_nodes, contained in local_payloads:
        one_hop = [edge for edge in local_edges if edge["type"] in LOCAL_STAGE_EDGE_TYPES]
        two_hop = [edge for edge in local_edges if edge["type"] not in LOCAL_STAGE_EDGE_TYPES]
        diagram_edges = one_hop
        # Mermaid remains readable by showing the stage and its immediate owned
        # knowledge. The following table records all retained two-hop edges.
        one_hop_nodes = {stage_id}
        for edge in one_hop:
            one_hop_nodes.update((edge["from"], edge["to"]))
        lines.extend(
            [
                f"<a id=\"{stage_id.lower()}\"></a>",
                f"### {node_ref(nodes[stage_id])}",
                "",
                f"一跳局部图（One-hop Local Map）含 {len(one_hop)} 条边；二跳扩展（Two-hop Expansion）含 {len(two_hop)} 条边。包含的知识节点（Knowledge Node）：{', '.join(f'`{node_id}`' for node_id in sorted(contained)) or '无'}。",
                "",
                *mermaid(sorted(one_hop_nodes), diagram_edges, nodes, relations),
                "",
                "局部节点（Local Nodes）：" + grouped_node_ids(local_nodes, nodes) + "。",
                "",
                *edge_table(local_edges, nodes, relations),
                "",
            ]
        )

    lines.extend(
        [
            "## 回查与限制",
            "",
            "- 所有节点、边、关系和来源引用均回查 [`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)；关系名称由 [`taxonomy/rag-graph-model.json`](../../taxonomy/rag-graph-model.json) 的受控枚举读取。",
            "- 结构与覆盖结果见 [`audits/rag/graph-structure-audit.json`](../../audits/rag/graph-structure-audit.json) 与 [`audits/rag/graph-coverage-audit.json`](../../audits/rag/graph-coverage-audit.json)。",
            "- `RAG-07-001` 与 `RAG-13-011` 是无来源引用的库存草稿（Inventory Draft）知识节点；本页只把它们作为图谱现状的一部分，不将其表述为正式结论。",
            "- 已豁免的 EUR-Lex 来源保持非证据性（Non-evidentiary），本投影不把它用于任何技术或法律结论。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    graph = load_json(GRAPH_PATH)
    model = load_json(MODEL_PATH)
    OUTPUT_PATH.write_text(render(graph, model), encoding="utf-8")


if __name__ == "__main__":
    main()

"""Generate a bounded P5 stage-problem inventory from the canonical graph.

The batch is intentionally inventory-only: it projects existing
problem_question nodes through existing contains/problem_at edges and does
not infer new mappings from source metadata or create technical answers.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "knowledge/rag/graph.json"
OUTPUT_PATH = ROOT / "interview/rag/p5-001-foundation-stage-problems.md"

STAGES = (
    "PS-DATA-INGESTION",
    "PS-DOCUMENT-PARSING",
    "PS-DATA-GOVERNANCE",
    "PS-CHUNKING",
)

ALL_STAGE_IDS = (
    "PS-DATA-INGESTION", "PS-DOCUMENT-PARSING", "PS-DATA-GOVERNANCE", "PS-CHUNKING",
    "PS-EMBEDDING", "PS-STORAGE-INDEXING", "PS-QUERY-UNDERSTANDING", "PS-QUERY-REWRITE",
    "PS-QUERY-ROUTING", "PS-RETRIEVAL", "PS-RESULT-FUSION", "PS-RERANKING",
    "PS-CONTEXT-ASSEMBLY", "PS-ANSWER-GENERATION", "PS-CITATION-VERIFICATION",
    "PS-EVALUATION", "PS-PRODUCTION-GOVERNANCE", "PS-ADVANCED-RAG",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def label(node: dict[str, Any]) -> str:
    return f"{node['label_zh']}（{node['label_en']}）"


def bilingual_problem_label(value: str) -> str:
    replacements = {
        "父子 Chunk": "父子文本切分（Parent-Child Chunking）",
        "Metadata": "元数据（Metadata）",
        "Hybrid Retrieval": "混合检索（Hybrid Retrieval）",
        "Rerank": "重排（Reranking）",
        "固定 Token": "固定词元（Token）",
        "P99 延迟": "P99 尾延迟（P99 Tail Latency）",
    }
    for source, target in replacements.items():
        value = value.replace(source, target)
    return value


def render(graph: dict[str, Any]) -> str:
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = graph["edges"]
    stage_atoms: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge["type"] == "contains" and edge["from"] in STAGES:
            stage_atoms[edge["from"]].add(edge["to"])

    problems = [node for node in nodes.values() if node["type"] == "problem_question"]
    problem_ids = {problem["id"] for problem in problems}
    problem_at_atoms: dict[str, set[str]] = defaultdict(set)
    problem_supported_sources: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge["from"] not in problem_ids:
            continue
        if edge["type"] == "problem_at":
            problem_at_atoms[edge["from"]].add(edge["to"])
        elif edge["type"] == "supported_by":
            problem_supported_sources[edge["from"]].add(edge["to"])
    for problem in problems:
        pid = problem["id"]
        declared_atoms = set(problem.get("knowledge_node_ids", []))
        if declared_atoms != problem_at_atoms[pid]:
            raise ValueError(f"{pid} knowledge_node_ids does not match problem_at edges")
        declared_sources = set(problem.get("source_refs", []))
        if declared_sources != problem_supported_sources[pid]:
            raise ValueError(f"{pid} source_refs does not match supported_by edges")
    problems_by_stage: dict[str, list[dict[str, Any]]] = defaultdict(list)
    mapped_atoms: dict[tuple[str, str], list[str]] = {}
    all_problem_stages: dict[str, list[str]] = defaultdict(list)
    for problem in problems:
        atom_ids = problem_at_atoms[problem["id"]]
        for stage_id in ALL_STAGE_IDS:
            overlap = sorted(atom_ids & stage_atoms[stage_id])
            if overlap:
                problems_by_stage[stage_id].append(problem)
                mapped_atoms[(problem["id"], stage_id)] = overlap
                all_problem_stages[problem["id"]].append(stage_id)

    lines = [
        "# P5-001 基础流程节点问题索引增量（Foundation Stage Problem Batch）",
        "",
        "> 状态：`candidate / WP-P5-001 / graph-backed / inventory-only`",
        ">",
        "> 范围：数据摄取（Data Ingestion）、文档解析（Document Parsing）、数据治理（Data Governance）、文本切分（Chunking）。",
        ">",
        "> 图谱输入：[`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)；生成器：[`scripts/generate_rag_stage_problem_batch.py`](../../scripts/generate_rag_stage_problem_batch.py)。",
        "",
        "本批只投影已有问题节点（Problem Question Nodes）以及图谱中的 `contains`、`problem_at` 和 `supported_by` 关系；不新增题目、不生成正式答案、不把来源登记中的阶段提示替换为图谱关系。",
        "",
        "## 生成审计（Generation Audit）",
        "",
        f"- 图谱版本：`{graph.get('generated_at', 'unknown')}`；节点：{len(nodes)}；边：{len(edges)}。",
        f"- 批次流程节点：{len(STAGES)}；图谱问题节点：{len(problems)}；本批已投影问题：{len(set().union(*(set(item['id'] for item in problems_by_stage[s]) for s in STAGES))) if STAGES else 0}。",
        "- 题目来源只证明题目出处或工程场景；技术结论仍需回到图谱已登记的一手证据（First-party Evidence）。",
        "",
        "## 节点覆盖（Stage Coverage）",
        "",
        "| 流程节点（Pipeline Stage） | 图谱包含原子数 | 已映射问题数 | 问题 ID | 覆盖结论 |",
        "|---|---:|---:|---|---|",
    ]
    for stage_id in STAGES:
        stage_problems = sorted(problems_by_stage[stage_id], key=lambda item: item["id"])
        problem_ids = ", ".join(f"[`{item['id']}`](#{item['id'].lower()})" for item in stage_problems) or "无"
        if stage_problems:
            conclusion = "可由现有 `contains` 与 `problem_at` 边投影；仅作为问题入口。"
        elif stage_atoms[stage_id]:
            conclusion = "该阶段已有 `contains` 原子，但当前没有问题节点通过 `problem_at` 映射；保留为覆盖缺口。"
        else:
            conclusion = "当前图谱没有该阶段的 `contains` 原子，不能从来源元数据推断题目映射；保留为覆盖缺口。"
        lines.append(
            f"| {label(nodes[stage_id])} [`{stage_id}`] | {len(stage_atoms[stage_id])} | {len(stage_problems)} | {problem_ids} | {conclusion} |"
        )

    lines.extend(["", "## 问题映射（Problem Mappings）", ""])
    emitted_anchors: set[str] = set()
    for stage_id in STAGES:
        stage_problems = sorted(problems_by_stage[stage_id], key=lambda item: item["id"])
        lines.extend([f"### {label(nodes[stage_id])} [`{stage_id}`]", ""])
        if not stage_problems:
            lines.extend(
                [
                    "当前图谱没有可投影的问题节点。数据摄取（Data Ingestion）来源检索和来源登记仍存在候选证据，但本批不新增 `problem_at` 或 `contains` 边；待图谱映射审计后再进入正式问题生产。",
                    "",
                ]
            )
            continue
        for problem in stage_problems:
            pid = problem["id"]
            source_refs = ", ".join(f"`{ref}`" for ref in sorted(problem.get("source_refs", []))) or "无（工程问题或待补来源）"
            atom_ids = mapped_atoms[(pid, stage_id)]
            related_stages = ", ".join(
                f"{label(nodes[sid])} [`{sid}`]"
                for sid in sorted(all_problem_stages[pid], key=ALL_STAGE_IDS.index)
            )
            lines.extend(
                [
                    *( [f"<a id=\"{pid.lower()}\"></a>"] if pid not in emitted_anchors else [] ),
                    f"#### {pid}：{bilingual_problem_label(problem['label_zh'])}（{problem['label_en']}）",
                    "",
                    "| 字段 | 内容 |",
                    "|---|---|",
                    f"| 来源类型（Provenance Type） | `{problem.get('provenance_type', '未声明')}` |",
                    f"| 原始定位（Source Locator） | {problem.get('source_locator') or '未声明'} |",
                    f"| 来源引用（Source References） | {source_refs} |",
                    f"| 当前节点关联原子（Stage Knowledge Atoms） | {', '.join(f'`{atom_id}`' for atom_id in atom_ids)} |",
                f"| 本问题全部流程节点（All Mapped Stages） | {related_stages} |",
                    "",
                    "该记录是问题入口（Inventory Entry），不是答案页面。正式页面生产时必须补充工程现象、根因、方案、实现和验证，并逐项回链来源；不得把公开题库（Public Question Bank）或第一人称面经（First-person Interview Report）升级为企业官方面试结论。",
                    "",
                ]
            )
            emitted_anchors.add(pid)

    lines.extend(
        [
            "## 关系与边界（Relations and Boundaries）",
            "",
            "- 节点映射仅使用图谱已有 `contains`（Contains）和问题到知识原子的 `problem_at`（Problem At）边；没有因题目语义相近而合并问题。",
            "- `supported_by`（Supported By）沿用图谱的来源引用；公开题目来源支持题目出处，不直接支持技术结论。",
            "- 数据摄取（Data Ingestion）目前为零映射是结构性缺口，不代表该流程没有工程问题；补映射前不得生成无来源问题节点。",
            "- 文档解析（Document Parsing）、数据治理（Data Governance）和文本切分（Chunking）的跨节点问题必须保留其全部流程节点，不强制拆成单节点题目。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    OUTPUT_PATH.write_text(render(load(GRAPH_PATH)), encoding="utf-8")


if __name__ == "__main__":
    main()

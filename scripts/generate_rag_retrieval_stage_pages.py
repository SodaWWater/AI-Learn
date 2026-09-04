"""Generate inventory-only retrieval-stage problem pages from graph relations."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "knowledge/rag/graph.json"
OUT_DIR = ROOT / "interview/rag/stages"

STAGES = (
    ("PS-RETRIEVAL", "retrieval", "检索（Retrieval）", "从一个或多个知识源产生候选证据，并处理召回、过滤、权限和延迟约束。"),
    ("PS-RESULT-FUSION", "result-fusion", "结果融合（Result Fusion）", "合并稠密、稀疏或多路检索结果，处理分数尺度、重复和通道偏置。"),
    ("PS-RERANKING", "reranking", "重排（Reranking）", "对候选证据进行更精细排序，在相关性、多样性、成本和尾延迟之间取舍。"),
)
ALL_STAGES = (
    "PS-DATA-INGESTION", "PS-DOCUMENT-PARSING", "PS-DATA-GOVERNANCE", "PS-CHUNKING",
    "PS-EMBEDDING", "PS-STORAGE-INDEXING", "PS-QUERY-UNDERSTANDING", "PS-QUERY-REWRITE",
    "PS-QUERY-ROUTING", "PS-RETRIEVAL", "PS-RESULT-FUSION", "PS-RERANKING",
    "PS-CONTEXT-ASSEMBLY", "PS-ANSWER-GENERATION", "PS-CITATION-VERIFICATION",
    "PS-EVALUATION", "PS-PRODUCTION-GOVERNANCE", "PS-ADVANCED-RAG",
)


def load() -> dict[str, Any]:
    return json.loads(GRAPH_PATH.read_text(encoding="utf-8"))


def bilingual(text: str) -> str:
    replacements = (
        ("Query/Document Embedding", "查询/文档向量嵌入（Query/Document Embedding）"),
        ("FAISS Top-K", "FAISS 前 K 个结果（Top-K Results）"),
        ("VectorRAG", "向量检索增强生成（VectorRAG）"),
        ("长尾 Query", "长尾查询（Long-tail Query）"),
        ("Multi-Query", "多查询扩展（Multi-Query Expansion）"),
        ("Step-back Prompting", "退步提示（Step-back Prompting）"),
        ("HyDE", "假设文档嵌入（Hypothetical Document Embeddings，HyDE）"),
        ("Retrieval Bias", "检索偏置（Retrieval Bias）"),
        ("Dense", "稠密检索（Dense Retrieval）"),
        ("Sparse", "稀疏检索（Sparse Retrieval）"),
        ("Hybrid Search", "混合检索（Hybrid Search）"),
        ("Reranker", "重排模型（Reranker）"),
        ("Recall", "召回率（Recall）"),
        ("NDCG", "归一化折损累计增益（NDCG）"),
        ("MRR", "平均倒数排名（MRR）"),
        ("Metadata", "元数据（Metadata）"),
        ("Token", "词元（Token）"),
        ("Chunk", "文本片段（Chunk）"),
        ("PDF", "便携式文档格式（PDF）"),
    )
    placeholders = {}
    for index, (old, new) in enumerate(replacements):
        marker = f"__RETRIEVAL_TERM_{index}__"
        if old in text:
            text = text.replace(old, marker)
            placeholders[marker] = new
    for marker, new in placeholders.items():
        text = text.replace(marker, new)
    return text


def render(graph: dict[str, Any], stage_id: str, label: str, boundary: str) -> str:
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = graph["edges"]
    stage_atoms = {edge["to"] for edge in edges if edge["type"] == "contains" and edge["from"] == stage_id}
    problems = [node for node in graph["nodes"] if node["type"] == "problem_question"]
    problem_ids = {problem["id"] for problem in problems}
    problem_at: dict[str, set[str]] = defaultdict(set)
    supported: dict[str, set[str]] = defaultdict(set)
    stages_by_problem: dict[str, set[str]] = defaultdict(set)
    solved: dict[str, list[str]] = defaultdict(list)
    evaluated: dict[str, list[str]] = defaultdict(list)
    contains_by_atom: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        if edge["type"] == "contains":
            contains_by_atom[edge["to"]].add(edge["from"])
        elif edge["type"] == "problem_at" and edge["from"] in problem_ids:
            problem_at[edge["from"]].add(edge["to"])
        elif edge["type"] == "supported_by" and edge["from"] in problem_ids:
            supported[edge["from"]].add(edge["to"])
        elif edge["type"] == "solved_by" and edge["from"] in problem_ids:
            solved[edge["from"]].append(edge["to"])
        elif edge["type"] == "evaluated_by" and edge["from"] in problem_ids:
            evaluated[edge["from"]].append(edge["to"])
    selected: list[tuple[dict[str, Any], list[str]]] = []
    for problem in problems:
        pid = problem["id"]
        if set(problem.get("knowledge_node_ids", [])) != problem_at[pid]:
            raise ValueError(f"{pid} knowledge_node_ids does not match problem_at edges")
        if set(problem.get("source_refs", [])) != supported[pid]:
            raise ValueError(f"{pid} source_refs does not match supported_by edges")
        for atom in problem_at[pid]:
            stages_by_problem[pid].update(contains_by_atom[atom])
        overlap = sorted(problem_at[pid] & stage_atoms)
        if overlap:
            selected.append((problem, overlap))
    selected.sort(key=lambda item: item[0]["id"])
    lines = [
        f"# {label}节点问题集合", "", 
        "> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`", ">",
        "> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。", "",
        "## 节点边界", "", f"{label}{boundary}当前图谱包含 {len(stage_atoms)} 个知识原子，并映射 {len(selected)} 道问题。题目来源只证明出处或工程场景，技术结论仍需回到已登记的一手证据。", "",
        "## 通用诊断路径", "",
        "1. 先固定查询、数据快照、过滤条件、候选数和模型版本，再区分召回缺失、融合偏置与重排误差。",
        "2. 同时记录命中率、召回率、排序质量、延迟、吞吐、成本和权限过滤后的有效候选数。",
        "3. 用离线基线、影子流量和失败样本验证通道贡献，不把单一数据集或固定参数当作普遍最优。",
        "4. 图谱未登记的根因或评估关系保持为待验证缺口，不以推断替代证据。", "", "## 问题明细", "",
    ]
    if not selected:
        lines.extend(["当前阶段已有图谱 `contains` 原子，但没有问题节点通过 `problem_at` 映射；这是覆盖缺口，不从来源元数据推断题目。" if stage_atoms else "当前阶段没有图谱 `contains` 原子，无法建立受控问题映射；这是结构性覆盖缺口，不新增无来源题目。", ""])
    for problem, overlap in selected:
        pid = problem["id"]
        refs = sorted(problem.get("source_refs", []))
        details = "; ".join(f"`{ref}`: {nodes[ref].get('source_locator', '未登记定位')}；审核日期 {nodes[ref].get('reviewed_at', '未登记')}" for ref in refs if ref in nodes) or "无（待补来源）"
        related = ", ".join(f"{nodes[s]['label_zh']}（{nodes[s]['label_en']}） [`{s}`]" for s in ALL_STAGES if s in stages_by_problem[pid])
        lines.extend([
            f"<a id=\"{pid.lower()}\"></a>", f"### {pid}：{bilingual(problem['label_zh'])}（{problem['label_en']}）", "",
            "| 字段 | 内容 |", "|---|---|",
            f"| 来源类型（Provenance Type） | `{problem.get('provenance_type', '未声明')}` |",
            f"| 原始定位（Source Locator） | {problem.get('source_locator') or '未声明'} |",
            f"| 来源引用（Source References） | {', '.join(f'`{x}`' for x in refs) or '无'} |",
            f"| 来源定位与审核（Locator and Review） | {details} |",
            f"| 当前节点关联原子（Stage Knowledge Atoms） | {', '.join(f'`{x}`' for x in overlap)} |",
            f"| 本问题全部流程节点（All Mapped Stages） | {related or '未映射'} |",
            f"| 图谱解决方案边（Solved By） | {', '.join(f'`{x}`' for x in sorted(solved[pid])) or '未登记（图谱无 solved_by 边）'} |",
            f"| 图谱评估边（Evaluated By） | {', '.join(f'`{x}`' for x in sorted(evaluated[pid])) or '未登记（图谱无 evaluated_by 边）'} |", "",
            "**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。", "",
            "**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。", "",
            "**验证与追问**：固定数据和版本，做分通道召回、融合/重排消融、离线指标、影子流量和延迟成本压测；没有 `evaluated_by` 时保留为待验证项。", "",
        ])
    lines.extend(["## 来源与限制", "", "- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。", "- 第一人称面经（First-person Interview Report）、公开题库（Public Question Bank）和项目型考题（Project Interview Exercise）只证明题目出处或场景，不证明企业官方面试事实。", "- 当前状态为 inventory-only；正式页面仍需按模板补充完整现象、根因分支、方案权衡、实现细节和验证证据。", ""])
    return "\n".join(lines)


def main() -> None:
    graph = load()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stage_id, slug, label, boundary in STAGES:
        (OUT_DIR / f"{slug}.md").write_text(render(graph, stage_id, label, boundary), encoding="utf-8")


if __name__ == "__main__":
    main()

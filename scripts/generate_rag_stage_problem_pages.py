"""Generate inventory-only P5 stage problem pages from graph relations."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "knowledge/rag/graph.json"
OUT_DIR = ROOT / "interview/rag/stages"

STAGES = (
    ("PS-EMBEDDING", "embedding", "向量嵌入（Embedding）", "向量表示和模型选择、批处理、维度、成本与迁移约束。"),
    ("PS-STORAGE-INDEXING", "storage-indexing", "存储与索引（Storage and Indexing）", "向量数据库、索引构建与发布、更新删除、一致性、扩展和恢复约束。"),
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
    replacements = {
        "Query/Document Embedding": "查询/文档向量嵌入（Query/Document Embedding）",
        "Embedding 模型": "向量嵌入模型（Embedding Model）",
        "Embedding Model": "向量嵌入模型（Embedding Model）",
        "Embedding": "向量嵌入（Embedding）",
        "Metadata": "元数据（Metadata）",
        "Exact、HNSW 或 IVF": "精确最近邻（Exact）、分层可导航小世界图（HNSW）或倒排文件索引（IVF）",
        "FAISS Top-K": "FAISS 前 K 个结果（Top-K Results）",
        "Chunk": "文本片段（Chunk）",
        "Token": "词元（Token）",
        "P99 延迟": "P99 尾延迟（P99 Tail Latency）",
        "PDF": "便携式文档格式（PDF）",
    }
    placeholders = {}
    for index, (old, new) in enumerate(replacements.items()):
        marker = f"__TERM_{index}__"
        if old in text:
            text = text.replace(old, marker)
            placeholders[marker] = new
    for marker, new in placeholders.items():
        text = text.replace(marker, new)
    return text


def render(graph: dict[str, Any], stage_id: str, slug: str, stage_label: str, boundary: str) -> str:
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = graph["edges"]
    stage_atoms = {edge["to"] for edge in edges if edge["type"] == "contains" and edge["from"] == stage_id}
    problems = [node for node in graph["nodes"] if node["type"] == "problem_question"]
    problem_at: dict[str, set[str]] = defaultdict(set)
    supported: dict[str, set[str]] = defaultdict(set)
    stages_by_problem: dict[str, set[str]] = defaultdict(set)
    solved: dict[str, list[str]] = defaultdict(list)
    evaluated: dict[str, list[str]] = defaultdict(list)
    for edge in edges:
        if edge["type"] == "problem_at":
            problem_at[edge["from"]].add(edge["to"])
            if edge["to"] in stage_atoms:
                stages_by_problem[edge["from"]].add(stage_id)
        elif edge["type"] == "supported_by":
            supported[edge["from"]].add(edge["to"])
        elif edge["type"] == "solved_by":
            solved[edge["from"]].append(edge["to"])
        elif edge["type"] == "evaluated_by":
            evaluated[edge["from"]].append(edge["to"])
    for edge in edges:
        if edge["type"] == "problem_at" and edge["from"] in problem_at:
            if edge["to"] in {e["to"] for e in edges if e["type"] == "contains"}:
                for contains in edges:
                    if contains["type"] == "contains" and contains["to"] == edge["to"]:
                        stages_by_problem[edge["from"]].add(contains["from"])
    selected = []
    for problem in problems:
        pid = problem["id"]
        declared_atoms = set(problem.get("knowledge_node_ids", []))
        if declared_atoms != problem_at[pid] or set(problem.get("source_refs", [])) != supported[pid]:
            raise ValueError(f"Graph field/edge mismatch for {pid}")
        overlap = sorted(problem_at[pid] & stage_atoms)
        if overlap:
            selected.append((problem, overlap))
    selected.sort(key=lambda item: item[0]["id"])
    lines = [
        f"# {stage_label}节点问题集合",
        "",
        f"> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`",
        ">",
        f"> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。",
        "",
        "## 节点边界",
        "",
        f"{stage_label}{boundary}当前图谱包含 {len(stage_atoms)} 个知识原子，并映射 {len(selected)} 道问题。题目来源只证明出处或工程场景，技术结论仍需回到已登记的一手证据。",
        "",
        "## 通用诊断路径",
        "",
        "1. 先固定文档快照、模型版本、数据模式和服务目标，再区分表示质量、索引质量与在线一致性问题。",
        "2. 将向量维度、相似度度量、索引参数、过滤条件和版本标识作为同一条可追踪链路记录。",
        "3. 用离线检索指标、资源成本、延迟和失败样本做对照实验，不把题目中的参数当作通用最佳值。",
        "4. 图谱未登记的根因或评估关系保持为待验证缺口，不以推断替代证据。",
        "",
        "## 问题明细",
        "",
    ]
    for problem, overlap in selected:
        pid = problem["id"]
        source_refs = sorted(problem.get("source_refs", []))
        source_details = "; ".join(
            f"`{ref}`: {nodes[ref].get('source_locator', '未登记定位')}；审核日期 {nodes[ref].get('reviewed_at', '未登记')}"
            for ref in source_refs if ref in nodes
        ) or "无（待补来源）"
        all_stages = [s for s in ALL_STAGES if s in stages_by_problem[pid]]
        related = ", ".join(f"{nodes[s]['label_zh']}（{nodes[s]['label_en']}） [`{s}`]" for s in all_stages)
        solution_ids = sorted(solved[pid]) or ["未登记（图谱无 solved_by 边）"]
        eval_ids = sorted(evaluated[pid]) or ["未登记（图谱无 evaluated_by 边）"]
        lines.extend([
            f"<a id=\"{pid.lower()}\"></a>",
            f"### {pid}：{bilingual(problem['label_zh'])}（{problem['label_en']}）",
            "",
            "| 字段 | 内容 |",
            "|---|---|",
            f"| 来源类型（Provenance Type） | `{problem.get('provenance_type', '未声明')}` |",
            f"| 原始定位（Source Locator） | {problem.get('source_locator') or '未声明'} |",
            f"| 来源引用（Source References） | {', '.join(f'`{x}`' for x in source_refs) or '无'} |",
            f"| 来源定位与审核（Locator and Review） | {source_details} |",
            f"| 当前节点关联原子（Stage Knowledge Atoms） | {', '.join(f'`{x}`' for x in overlap)} |",
            f"| 本问题全部流程节点（All Mapped Stages） | {related or '未映射'} |",
            f"| 图谱解决方案边（Solved By） | {', '.join(f'`{x}`' for x in solution_ids)} |",
            f"| 图谱评估边（Evaluated By） | {', '.join(f'`{x}`' for x in eval_ids)} |",
            "",
            "**工程现象与候选诊断点**：该题涉及的现象、约束和候选知识原子以 `problem_at` 映射为边界；图谱未声明因果关系时，不把候选点写成已证实根因。",
            "",
            "**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和相关知识原子展开，比较质量、延迟、吞吐、存储、成本、权限和迁移风险；本页不补写图谱之外的框架结论。",
            "",
            "**验证与追问**：固定数据快照和版本，分别做召回/排序回归、资源压测、更新删除一致性和失败样本复查；缺少 `evaluated_by` 时保留为待验证项。",
            "",
        ])
    lines.extend([
        "## 来源与限制",
        "",
        "- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。",
        "- 第一人称面经（First-person Interview Report）、公开题库（Public Question Bank）和项目型考题（Project Interview Exercise）只证明题目出处或场景，不证明企业官方面试事实。",
        "- 当前状态为 inventory-only；正式问题页面仍需按模板补充完整现象、根因分支、方案权衡、实现细节和验证证据。",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    graph = load()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stage_id, slug, label, boundary in STAGES:
        (OUT_DIR / f"{slug}.md").write_text(render(graph, stage_id, slug, label, boundary), encoding="utf-8")


if __name__ == "__main__":
    main()

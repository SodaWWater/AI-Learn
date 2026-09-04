"""Generate inventory-only query-stage problem pages from graph relations."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH_PATH = ROOT / "knowledge/rag/graph.json"
OUT_DIR = ROOT / "interview/rag/stages"

STAGES = (
    ("PS-QUERY-UNDERSTANDING", "query-understanding", "查询理解（Query Understanding）", "识别意图、实体、上下文、歧义和拒识条件。"),
    ("PS-QUERY-REWRITE", "query-rewrite", "查询改写（Query Rewrite）", "将原始查询转换为适合检索的表达，并控制语义漂移和额外延迟。"),
    ("PS-QUERY-ROUTING", "query-routing", "查询路由（Query Routing）", "根据问题、置信度、成本和能力边界选择检索源、检索策略或外部工具。"),
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
        ("Multi-Query", "多查询扩展（Multi-Query Expansion）"),
        ("Query/Document Embedding", "查询/文档向量嵌入（Query/Document Embedding）"),
        ("Query Expansion", "查询扩展（Query Expansion）"),
        ("长尾 Query", "长尾查询（Long-tail Query）"),
        ("HyDE", "假设文档嵌入（Hypothetical Document Embeddings，HyDE）"),
        ("Step-back Prompting", "退步提示（Step-back Prompting）"),
        ("Adaptive RAG", "自适应检索增强生成（Adaptive RAG）"),
        ("Iterative RAG", "迭代检索增强生成（Iterative RAG）"),
        ("Self-RAG", "自反思检索增强生成（Self-RAG）"),
        ("Agentic RAG", "智能体检索增强生成（Agentic RAG）"),
        ("子问题分解", "查询分解（Query Decomposition）"),
        ("会话改写", "会话查询改写（Conversational Query Rewrite）"),
        ("影子流量", "影子流量（Shadow Traffic）"),
        ("拒识", "拒识（Abstention）"),
        ("错误路由", "错误路由（Misrouting）"),
        ("召回低", "召回率（Recall）低"),
        ("置信度", "置信度（Confidence）"),
        ("降级", "降级（Graceful Degradation）"),
        ("外部工具", "外部工具（External Tool）"),
        ("Query", "查询（Query）"),
        ("Confidence", "置信度（Confidence）"),
        ("Embedding", "向量嵌入（Embedding）"),
    )
    placeholders: dict[str, str] = {}
    for index, (old, new) in enumerate(replacements):
        marker = f"__QUERY_TERM_{index}__"
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
        declared_atoms = set(problem.get("knowledge_node_ids", []))
        if declared_atoms != problem_at[pid]:
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
        f"# {label}节点问题集合",
        "",
        "> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`",
        ">",
        "> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。",
        "",
        "## 节点边界",
        "",
        f"{label}{boundary}当前图谱包含 {len(stage_atoms)} 个知识原子，并映射 {len(selected)} 道问题。题目来源只证明出处或工程场景，技术结论仍需回到已登记的一手证据。",
        "",
        "## 通用诊断路径",
        "",
        "1. 先固定原始查询、上下文、模型版本、路由策略和服务目标，再区分理解错误、改写漂移与路由错误。",
        "2. 记录拒识、歧义、长尾表达和新业务类型，使用影子流量与错误样本评估覆盖，而不是只看平均准确率。",
        "3. 将质量收益与额外调用、延迟、成本、隐私和可回滚性一起比较。",
        "4. 图谱未登记的根因或评估关系保持为待验证缺口，不以推断替代证据。",
        "",
        "## 问题明细",
        "",
    ]
    if not selected:
        if stage_atoms:
            lines.append("当前阶段已有 `contains` 原子，但没有问题节点通过 `problem_at` 映射；这是覆盖缺口，不从来源元数据推断题目。")
        else:
            lines.append("当前阶段没有图谱 `contains` 原子，无法建立受控问题映射；这是结构性覆盖缺口，不新增无来源题目。")
        lines.append("")
    for problem, overlap in selected:
        pid = problem["id"]
        refs = sorted(problem.get("source_refs", []))
        details = "; ".join(
            f"`{ref}`: {nodes[ref].get('source_locator', '未登记定位')}；审核日期 {nodes[ref].get('reviewed_at', '未登记')}"
            for ref in refs if ref in nodes
        ) or "无（待补来源）"
        related = ", ".join(
            f"{nodes[s]['label_zh']}（{nodes[s]['label_en']}） [`{s}`]"
            for s in ALL_STAGES if s in stages_by_problem[pid]
        )
        lines.extend([
            f"<a id=\"{pid.lower()}\"></a>",
            f"### {pid}：{bilingual(problem['label_zh'])}（{problem['label_en']}）",
            "",
            "| 字段 | 内容 |",
            "|---|---|",
            f"| 来源类型（Provenance Type） | `{problem.get('provenance_type', '未声明')}` |",
            f"| 原始定位（Source Locator） | {problem.get('source_locator') or '未声明'} |",
            f"| 来源引用（Source References） | {', '.join(f'`{ref}`' for ref in refs) or '无'} |",
            f"| 来源定位与审核（Locator and Review） | {details} |",
            f"| 当前节点关联原子（Stage Knowledge Atoms） | {', '.join(f'`{atom}`' for atom in overlap)} |",
            f"| 本问题全部流程节点（All Mapped Stages） | {related or '未映射'} |",
            f"| 图谱解决方案边（Solved By） | {', '.join(f'`{x}`' for x in sorted(solved[pid])) or '未登记（图谱无 solved_by 边）'} |",
            f"| 图谱评估边（Evaluated By） | {', '.join(f'`{x}`' for x in sorted(evaluated[pid])) or '未登记（图谱无 evaluated_by 边）'} |",
            "",
            "**工程现象与候选诊断点**：候选诊断点严格来自 `problem_at` 关系；图谱未声明因果关系时，不把候选点写成已证实根因。",
            "",
            "**方案、实现与选择依据**：正式答案应沿 `solved_by`、`implemented_by` 和知识原子展开，比较质量、延迟、吞吐、成本、权限与迁移风险；本页不补写图谱之外的技术结论。",
            "",
            "**验证与追问**：固定数据和版本，做离线分类/改写/路由评估、影子流量对比、延迟成本压测和失败样本复查；没有 `evaluated_by` 时保留为待验证项。",
            "",
        ])
    lines.extend([
        "## 来源与限制",
        "",
        "- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。",
        "- 第一人称面经（First-person Interview Report）、公开题库（Public Question Bank）和项目型考题（Project Interview Exercise）只证明题目出处或场景，不证明企业官方面试事实。",
        "- 当前状态为 inventory-only；正式页面仍需按模板补充完整现象、根因分支、方案权衡、实现细节和验证证据。",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    graph = load()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for stage_id, slug, label, boundary in STAGES:
        (OUT_DIR / f"{slug}.md").write_text(render(graph, stage_id, label, boundary), encoding="utf-8")


if __name__ == "__main__":
    main()

"""Generate graph-backed cross-stage problem inventory for WP-P6-001."""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "knowledge/rag/graph.json"
OUT = ROOT / "interview/rag/cross-stage-problem-inventory.md"
GRAPH_OUT = ROOT / "interview/rag/cross-stage-graph.md"
STAGES = ("PS-DATA-INGESTION","PS-DOCUMENT-PARSING","PS-DATA-GOVERNANCE","PS-CHUNKING","PS-EMBEDDING","PS-STORAGE-INDEXING","PS-QUERY-UNDERSTANDING","PS-QUERY-REWRITE","PS-QUERY-ROUTING","PS-RETRIEVAL","PS-RESULT-FUSION","PS-RERANKING","PS-CONTEXT-ASSEMBLY","PS-ANSWER-GENERATION","PS-CITATION-VERIFICATION","PS-EVALUATION","PS-PRODUCTION-GOVERNANCE","PS-ADVANCED-RAG")

def bilingual(text: str) -> str:
    replacements = (("Chunk", "文本片段（Chunk）"), ("Metadata", "元数据（Metadata）"), ("Hybrid Retrieval", "混合检索（Hybrid Retrieval）"), ("Hybrid Search", "混合检索（Hybrid Search）"), ("Rerank", "重排（Rerank）"), ("Embedding", "向量嵌入（Embedding）"), ("Query", "查询（Query）"), ("Dense", "稠密检索（Dense Retrieval）"), ("Sparse", "稀疏检索（Sparse Retrieval）"), ("Agentic RAG", "智能体检索增强生成（Agentic RAG）"), ("VectorRAG", "向量检索增强生成（VectorRAG）"), ("Token", "词元（Token）"), ("Recall", "召回率（Recall）"))
    placeholders = {}
    for i, (old, new) in enumerate(replacements):
        marker = f"__CROSS_TERM_{i}__"
        if old in text:
            text = text.replace(old, marker); placeholders[marker] = new
    for marker, new in placeholders.items(): text = text.replace(marker, new)
    return text

def main() -> None:
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in graph["nodes"]}
    problems = {n["id"]: n for n in graph["nodes"] if n["type"] == "problem_question"}
    atom_stages = defaultdict(set); mapped_atoms = defaultdict(set); supported = defaultdict(set); solved = defaultdict(list); evaluated = defaultdict(list)
    for e in graph["edges"]:
        if e["type"] == "contains" and e["from"] in STAGES: atom_stages[e["to"]].add(e["from"])
        elif e["type"] == "problem_at" and e["from"] in problems and e["to"] in nodes: mapped_atoms[e["from"]].add(e["to"])
        elif e["type"] == "supported_by" and e["from"] in problems: supported[e["from"]].add(e["to"])
        elif e["type"] == "solved_by" and e["from"] in problems: solved[e["from"]].append(e["to"])
        elif e["type"] == "evaluated_by" and e["from"] in problems: evaluated[e["from"]].append(e["to"])
    mapped = {pid: {stage for atom in atoms for stage in atom_stages[atom]} for pid, atoms in mapped_atoms.items()}
    selected = [(problems[pid], sorted(mapped[pid], key=lambda x: STAGES.index(x))) for pid in sorted(problems) if len(mapped[pid]) >= 2]
    lines = ["# 跨节点工程问题与系统设计问题库存（Cross-stage Problem and System Design Inventory）", "", "> 状态：`candidate / WP-P6-001 / graph-backed / inventory-only`", ">", "> 本页只投影已有问题节点及 `problem_at`、`supported_by`、`solved_by`、`evaluated_by` 关系；不新增综合题、系统设计题、来源或正式答案。", "", "## 生成审计（Generation Audit）", "", f"图谱版本：`{graph.get('generated_at', '未登记')}`；跨节点问题：{len(selected)}；问题节点总数：{len(problems)}。", "", "跨节点定义为同一问题通过 `problem_at` 映射到两个及以上流程节点。未达到该条件的问题保留在节点页面，不在此重复展开。", "", "## 问题库存（Problem Inventory）", ""]
    for p, stages in selected:
        pid = p["id"]; refs = sorted(supported[pid]); source_details = "; ".join(f"`{r}`: {nodes[r].get('source_locator','未登记定位')}；审核日期 {nodes[r].get('reviewed_at','未登记')}" for r in refs if r in nodes) or "无（待补来源）"
        stage_text = ", ".join(f"{nodes[s]['label_zh']}（{nodes[s]['label_en']}） [`{s}`]" for s in stages)
        lines.extend([f"<a id=\"{pid.lower()}\"></a>", f"### {pid}：{bilingual(p['label_zh'])}（{p['label_en']}）", "", "| 字段 | 内容 |", "|---|---|", f"| 来源类型（Provenance Type） | `{p.get('provenance_type', '未声明')}` |", f"| 原始定位（Source Locator） | {p.get('source_locator') or '未声明'} |", f"| 来源引用（Source References） | {', '.join('`'+r+'`' for r in refs) or '无'} |", f"| 来源定位与审核（Locator and Review） | {source_details} |", f"| 跨节点映射（Cross-stage Mapping） | {stage_text} |", f"| 图谱解决方案边（Solved By） | {', '.join('`'+x+'`' for x in sorted(solved[pid])) or '未登记'} |", f"| 图谱评估边（Evaluated By） | {', '.join('`'+x+'`' for x in sorted(evaluated[pid])) or '未登记'} |", "", "该条是跨节点问题入口；正式综合题或系统设计题必须在后续工作包中补充场景边界、跨节点依赖、方案权衡、实现和验证证据。", ""])
    lines += ["## 来源与限制（Sources and Limits）", "", "- 所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../knowledge/rag/graph.json)。", "- 面经和公开题库只证明题目出处或工程场景，不升级为企业官方面试结论。", "- 当前状态为 inventory-only；本页不替代正式问题答案或知识章节。", ""]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    pair_counts = defaultdict(int)
    for pid, stages in mapped.items():
        ordered = sorted(stages, key=STAGES.index)
        for i, left in enumerate(ordered):
            for right in ordered[i + 1:]:
                pair_counts[(left, right)] += 1
    graph_lines = ["# 跨节点问题关系视图（Cross-stage Problem Graph View）", "", "> 状态：`candidate / WP-P6-001 / graph-backed / inventory-only`", ">", "> 本视图由 `problem_at` 经知识原子反向连接到流程节点，并统计共享问题数量；不新增关系。", "", "## 节点对重叠（Stage-pair Overlap）", "", "| 节点 A | 节点 B | 共享问题数 |", "|---|---|---:|"]
    for (left, right), count in sorted(pair_counts.items(), key=lambda item: (-item[1], STAGES.index(item[0][0]), STAGES.index(item[0][1]))):
        graph_lines.append(f"| {nodes[left]['label_zh']}（{nodes[left]['label_en']}） [`{left}`] | {nodes[right]['label_zh']}（{nodes[right]['label_en']}） [`{right}`] | {count} |")
    graph_lines += ["", "## 生成限制（Limits）", "", "- 共享问题数来自现有问题节点的 `problem_at` 与知识原子的 `contains` 关系。", "- 该视图用于定位跨节点复习路径，不等同于正式系统设计方案或因果证明。", "- 来源、解决方案和评估证据仍需回到问题库存及图谱原始关系。", ""]
    GRAPH_OUT.write_text("\n".join(graph_lines), encoding="utf-8")

if __name__ == "__main__":
    main()

"""Generate inventory-only pages for context, answer, and citation stages."""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "knowledge/rag/graph.json"
OUT = ROOT / "interview/rag/stages"
STAGES = (
    ("PS-CONTEXT-ASSEMBLY", "context-assembly", "上下文组装（Context Assembly）", "选择、排序、压缩并组织证据，使模型输入满足相关性、完整性、窗口和权限约束。"),
    ("PS-ANSWER-GENERATION", "answer-generation", "答案生成（Answer Generation）", "基于查询和受控上下文生成答案，并处理忠实性、拒答、格式和输出边界。"),
    ("PS-CITATION-VERIFICATION", "citation-verification", "引用与验证（Citation and Verification）", "将答案主张绑定到证据并执行可追溯性、事实一致性和发布前验证。"),
    ("PS-EVALUATION", "evaluation", "评估（Evaluation）", "用离线数据、在线流量和端到端指标验证检索增强生成质量、成本与稳定性。"),
    ("PS-PRODUCTION-GOVERNANCE", "production-governance", "生产治理（Production Governance）", "管理权限、安全、可观测性、性能、成本、版本发布与故障恢复。"),
    ("PS-ADVANCED-RAG", "advanced-rag", "高级检索增强生成（Advanced RAG）", "组合迭代检索、智能体、自反思和图谱等能力，并明确适用边界与验证要求。"),
)
ALL = ("PS-DATA-INGESTION","PS-DOCUMENT-PARSING","PS-DATA-GOVERNANCE","PS-CHUNKING","PS-EMBEDDING","PS-STORAGE-INDEXING","PS-QUERY-UNDERSTANDING","PS-QUERY-REWRITE","PS-QUERY-ROUTING","PS-RETRIEVAL","PS-RESULT-FUSION","PS-RERANKING","PS-CONTEXT-ASSEMBLY","PS-ANSWER-GENERATION","PS-CITATION-VERIFICATION","PS-EVALUATION","PS-PRODUCTION-GOVERNANCE","PS-ADVANCED-RAG")

def bilingual(s: str) -> str:
    terms = (("Context", "上下文（Context）"),("Answer", "答案（Answer）"),("Citation", "引用（Citation）"),("Verification", "验证（Verification）"),("Token", "词元（Token）"),("Prompt", "提示（Prompt）"),("Faithfulness", "忠实性（Faithfulness）"),("Grounded", "基于证据（Grounded）"),("Hallucination", "幻觉（Hallucination）"),("Recall", "召回率（Recall）"))
    for old,new in terms: s=s.replace(old,new)
    return s

def render(g: dict[str,Any], sid: str, slug: str, label: str, boundary: str) -> str:
    nodes={n["id"]:n for n in g["nodes"]}; edges=g["edges"]
    atoms={e["to"] for e in edges if e["type"]=="contains" and e["from"]==sid}
    probs=[n for n in g["nodes"] if n["type"]=="problem_question"]; pids={p["id"] for p in probs}
    pat=defaultdict(set); sup=defaultdict(set); solved=defaultdict(list); evald=defaultdict(list); cab=defaultdict(set)
    for e in edges:
        if e["type"]=="contains": cab[e["to"]].add(e["from"])
        elif e["type"]=="problem_at" and e["from"] in pids: pat[e["from"]].add(e["to"])
        elif e["type"]=="supported_by" and e["from"] in pids: sup[e["from"]].add(e["to"])
        elif e["type"]=="solved_by" and e["from"] in pids: solved[e["from"]].append(e["to"])
        elif e["type"]=="evaluated_by" and e["from"] in pids: evald[e["from"]].append(e["to"])
    selected=[]
    for p in probs:
        pid=p["id"]
        if set(p.get("knowledge_node_ids",[])) != pat[pid] or set(p.get("source_refs",[])) != sup[pid]: raise ValueError(f"{pid} relation mismatch")
        overlap=sorted(pat[pid]&atoms)
        if overlap: selected.append((p,overlap))
    lines=[f"# {label}节点问题集合","","> 状态：`candidate / WP-P5-001 / graph-backed / stage-generated`","","> 本页只投影图谱中已有 `contains`、`problem_at`、`supported_by`、`solved_by` 和 `evaluated_by` 关系；不新增题目、来源或正式知识章节。","","## 节点边界","",f"{label}{boundary}当前图谱包含 {len(atoms)} 个知识原子，并映射 {len(selected)} 道问题。","","## 通用诊断路径","","1. 固定查询、证据集合、模型版本、提示模板和发布策略，区分上下文缺失、生成偏差与引用失配。","2. 记录窗口截断、权限过滤、拒答、未支撑主张和格式错误，按失败样本而非平均指标复查。","3. 同时比较质量、延迟、成本、隐私、可回滚性与审计可追溯性。","4. 图谱未登记的根因、方案或评估关系保持为待验证缺口。","","## 问题明细",""]
    if not selected: lines += ["当前阶段没有问题节点通过 `problem_at` 映射；这是覆盖缺口，不新增无来源题目。",""]
    for p,overlap in selected:
        pid=p["id"]; refs=sorted(p.get("source_refs",[])); details="; ".join(f"`{r}`: {nodes[r].get('source_locator','未登记定位')}；审核日期 {nodes[r].get('reviewed_at','未登记')}" for r in refs if r in nodes) or "无（待补来源）"
        lines += [f"<a id=\"{pid.lower()}\"></a>",f"### {pid}：{bilingual(p['label_zh'])}（{p['label_en']}）","","| 字段 | 内容 |","|---|---|",f"| 来源类型（Provenance Type） | `{p.get('provenance_type','未声明')}` |",f"| 原始定位（Source Locator） | {p.get('source_locator') or '未声明'} |",f"| 来源引用（Source References） | {', '.join('`'+r+'`' for r in refs) or '无'} |",f"| 来源定位与审核（Locator and Review） | {details} |",f"| 当前节点关联原子（Stage Knowledge Atoms） | {', '.join('`'+a+'`' for a in overlap)} |",f"| 图谱解决方案边（Solved By） | {', '.join('`'+x+'`' for x in sorted(solved[pid])) or '未登记（图谱无 solved_by 边）'} |",f"| 图谱评估边（Evaluated By） | {', '.join('`'+x+'`' for x in sorted(evald[pid])) or '未登记（图谱无 evaluated_by 边）'} |","","**工程现象与候选诊断点**：候选点严格来自 `problem_at` 关系；图谱未声明因果时不写成已证实根因。","","**方案、实现与验证**：正式答案应沿 `solved_by`、实现关系和知识原子展开；本页不补写图谱之外的结论。","","**限制**：当前为 inventory-only，缺失关系保留为待验证项。",""]
    lines += ["## 来源与限制","","- 本页所有问题、节点、来源和关系 ID 均来自 [`knowledge/rag/graph.json`](../../../knowledge/rag/graph.json)。","- 当前状态为 inventory-only；正式页面仍需按模板补充完整证据。",""]
    return "\n".join(lines)

def main():
    g=json.loads(GRAPH.read_text(encoding="utf-8")); OUT.mkdir(parents=True,exist_ok=True)
    for sid,slug,label,boundary in STAGES: (OUT/f"{slug}.md").write_text(render(g,sid,slug,label,boundary),encoding="utf-8")
if __name__ == "__main__": main()

"""Generate a graph-backed audit of chapter atoms and problem links."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "knowledge/rag/graph.json"
OUT_JSON = ROOT / "audits/rag/chapter-problem-links.json"
OUT_MD = ROOT / "audits/rag/chapter-problem-links.md"

CHAPTERS = {
    "RAG-01": "knowledge/rag/chapters/rag-01-foundations.md",
    "RAG-02": "knowledge/rag/chapters/rag-02-architecture-lifecycle.md",
    "RAG-03": "knowledge/rag/chapters/rag-03-document-parsing-governance.md",
}


def main() -> None:
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = {node["id"]: node for node in graph["nodes"]}
    edges = graph["edges"]
    contains = {(edge["from"], edge["to"]) for edge in edges if edge["type"] == "contains"}
    problem_at = {(edge["from"], edge["to"]) for edge in edges if edge["type"] == "problem_at"}

    result = {"schema_version": 1, "generated_at": graph["generated_at"], "chapters": []}
    for chapter_id, path in CHAPTERS.items():
        atoms = sorted(node_id for node_id in nodes if node_id.startswith(chapter_id + "-"))
        stages = sorted({source for source, atom in contains if atom in atoms})
        problems = sorted({problem for problem, atom in problem_at if atom in atoms})
        result["chapters"].append({
            "chapter_id": chapter_id,
            "chapter_path": path,
            "atom_ids": atoms,
            "atom_count": len(atoms),
            "pipeline_stage_ids": stages,
            "problem_ids": problems,
            "problem_count": len(problems),
            "link_status": "graph_backed",
        })

    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# 知识章节与问题双向链接审计（Chapter-Problem Link Audit）",
        "",
        "> 由 `knowledge/rag/graph.json` 的 `contains` 和 `problem_at` 边生成；不新增知识、问题或关系。",
        "",
        f"图谱版本：`{graph['generated_at']}`。",
        "",
        "| 章节 | 原子数 | 流程节点数 | 关联问题数 | 状态 |",
        "|---|---:|---:|---:|---|",
    ]
    lines.extend(
        f"| `{chapter['chapter_id']}` | {chapter['atom_count']} | "
        f"{len(chapter['pipeline_stage_ids'])} | {chapter['problem_count']} | `graph_backed` |"
        for chapter in result["chapters"]
    )
    for chapter in result["chapters"]:
        lines.extend([
            "",
            f"### {chapter['chapter_id']}",
            "",
            f"章节：`{chapter['chapter_path']}`",
            "",
            "原子：" + ", ".join(f"`{item}`" for item in chapter["atom_ids"]),
            "",
            "关联问题：" + (", ".join(f"`{item}`" for item in chapter["problem_ids"]) or "无"),
        ])
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

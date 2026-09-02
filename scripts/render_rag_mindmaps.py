#!/usr/bin/env python3
"""Render auditable draft RAG mind maps from the atomic catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "knowledge/rag/catalog.json"
LEARNING = ROOT / "learning/rag"
MODULES = LEARNING / "draft-modules"


def mermaid_id(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value)


def quoted(value: str) -> str:
    return value.replace('"', "'")


def main() -> None:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    sections = catalog["sections"]
    MODULES.mkdir(parents=True, exist_ok=True)

    overview = [
        "# RAG 全景思维导图（审计草案）",
        "",
        "> 本图由原子知识目录自动生成。它保证分类骨架不漏项，但在严格验收通过前不代表正文已经完备。",
        "",
        "```mermaid",
        "mindmap",
        '  root(("RAG 知识体系"))',
    ]
    for section in sections:
        overview.append(
            f'    {mermaid_id(section["id"])}["{section["id"]} {quoted(section["title"])} · {len(section["atoms"])} 点"]'
        )
    overview.extend(
        [
            "```",
            "",
            "## 建议学习顺序",
            "",
            "1. 先掌握基础、系统流程和数据入口：`RAG-01` → `RAG-04`。",
            "2. 再掌握检索核心：`RAG-05` → `RAG-08`。",
            "3. 然后掌握答案质量与评估：`RAG-09` → `RAG-10`。",
            "4. 再进入生产、安全与高级范式：`RAG-11` → `RAG-12`。",
            "5. 最后用项目设计和面试表达闭环：`RAG-13`。",
            "",
            "## 模块子图",
            "",
        ]
    )
    for section in sections:
        filename = f'{section["id"].lower()}.md'
        overview.append(
            f'- [`{section["id"]}` {section["title"]}](draft-modules/{filename})'
        )
    overview.append("")
    (LEARNING / "draft-overview.md").write_text("\n".join(overview), encoding="utf-8")

    for section in sections:
        lines = [
            f'# {section["id"]} {section["title"]}（审计草案）',
            "",
            "> 图中每个叶子节点对应原子目录中的一个独立知识点；只有完全同义的来源表述才会合并到同一节点。",
            "",
            "```mermaid",
            "mindmap",
            f'  root(("{section["id"]} {quoted(section["title"])}"))',
        ]
        for atom in section["atoms"]:
            lines.append(
                f'    {mermaid_id(atom["id"])}["{atom["id"]} {quoted(atom["title"])}"]'
            )
        lines.extend(
            [
                "```",
                "",
                f'共 **{len(section["atoms"])}** 个原子知识点。来源映射和事实核验状态以 `audits/rag/` 为准。',
                "",
            ]
        )
        (MODULES / f'{section["id"].lower()}.md').write_text(
            "\n".join(lines), encoding="utf-8"
        )

    print(
        f"rendered overview and {len(sections)} module maps "
        f"with {sum(len(section['atoms']) for section in sections)} atoms"
    )


if __name__ == "__main__":
    main()

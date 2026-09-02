#!/usr/bin/env python3
"""Render the machine-readable RAG atom catalog as reviewable Markdown."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    catalog = json.loads((ROOT / "knowledge/rag/catalog.json").read_text(encoding="utf-8"))
    total = sum(len(section["atoms"]) for section in catalog["sections"])
    lines = [
        "# RAG 原子知识目录", "",
        f"当前版本共 **{total}** 个原子知识点，状态为 `{catalog['status']}`。", "",
        "> 原子目录用于防止去重时丢失不同角度的信息；它不是已完成的标准答案。", "",
    ]
    for section in catalog["sections"]:
        lines.extend([f"## {section['id']} {section['title']}", ""])
        for atom in section["atoms"]:
            lines.append(f"- `{atom['id']}` {atom['title']}")
        lines.append("")
    (ROOT / "knowledge/rag/catalog.md").write_text("\n".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


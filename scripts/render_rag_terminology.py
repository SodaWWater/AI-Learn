#!/usr/bin/env python3
"""Render a machine-readable RAG terminology registry from the Markdown table."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "knowledge/rag/TERMINOLOGY.md"
OUTPUT = ROOT / "taxonomy/rag-terminology.json"


def main() -> None:
    terms: list[dict[str, str]] = []
    section = ""
    for raw_line in SOURCE.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^## \d+\. (.+)$", raw_line)
        if heading:
            section = heading.group(1)
            continue
        if not raw_line.startswith("|") or raw_line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in raw_line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] == "规范表达":
            continue
        match = re.fullmatch(r"(.+?)（(.+)）", cells[0])
        if not match:
            continue
        terms.append(
            {
                "id": f"TERM-RAG-{len(terms) + 1:03d}",
                "display": cells[0],
                "label_zh": match.group(1),
                "label_en": match.group(2),
                "alias": cells[1],
                "section": section,
                "note": cells[2],
            }
        )

    payload = {
        "schema_version": 1,
        "updated_at": "2026-09-02",
        "source": "knowledge/rag/TERMINOLOGY.md",
        "rule": "Every occurrence of a professional technical term uses its canonical bilingual display form.",
        "term_count": len(terms),
        "terms": terms,
    }
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"rendered {len(terms)} terminology entries to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()


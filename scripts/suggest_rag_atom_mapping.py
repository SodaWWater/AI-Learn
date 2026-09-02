#!/usr/bin/env python3
"""Suggest atom mappings for human review; never marks a mapping as accepted."""

from __future__ import annotations

import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized(text: str) -> str:
    text = text.lower()
    text = re.sub(r"^[\d.、\s]+", "", text)
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", text)
    return text


def grams(text: str) -> set[str]:
    text = normalized(text)
    if len(text) < 2:
        return {text} if text else set()
    return {text[index:index + 2] for index in range(len(text) - 1)}


def similarity(left: str, right: str) -> float:
    a = grams(left)
    b = grams(right)
    jaccard = len(a & b) / len(a | b) if a and b else 0.0
    sequence = SequenceMatcher(None, normalized(left), normalized(right)).ratio()
    return round(0.65 * jaccard + 0.35 * sequence, 4)


def main() -> int:
    inventory = load(ROOT / "audits/rag/source-units.json")
    catalog = load(ROOT / "knowledge/rag/catalog.json")
    atoms_by_section = {
        section["id"]: section["atoms"]
        for section in catalog["sections"]
    }

    suggestions = []
    for unit in inventory["units"]:
        topic = unit.get("canonical_topic")
        if unit.get("review_status") != "mapped" or not topic:
            suggestions.append({
                "source_unit_id": unit["id"],
                "review_status": "not_applicable",
                "reason": unit["review_status"],
                "accepted_atom_id": None,
                "candidates": [],
            })
            continue
        scored = sorted(
            (
                {
                    "atom_id": atom["id"],
                    "atom_title": atom["title"],
                    "score": similarity(f"{unit['title']} {unit['path']}", atom["title"]),
                }
                for atom in atoms_by_section[topic]
            ),
            key=lambda item: (-item["score"], item["atom_id"]),
        )
        suggestions.append({
            "source_unit_id": unit["id"],
            "review_status": "pending",
            "reason": "机器候选，必须人工确认；低分不代表可以遗漏。",
            "accepted_atom_id": None,
            "candidates": scored[:3],
        })

    status_counts = Counter(item["review_status"] for item in suggestions)
    payload = {
        "schema_version": 1,
        "generated_at": inventory["generated_at"],
        "warning": "本文件仅提供人工复核候选，不是已接受的覆盖矩阵。",
        "counts": dict(sorted(status_counts.items())),
        "mappings": suggestions,
    }
    output = ROOT / "audits/rag/atom-suggestions.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

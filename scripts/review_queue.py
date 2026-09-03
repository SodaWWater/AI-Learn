#!/usr/bin/env python3
"""Show the deterministic queue of RAG source units pending manual review."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PRIORITY = {
    "xiaolin-ai-learning": 0,
    "ai-agent-interview-guide": 1,
    "agent-guide": 2,
    "user-rag-experience-pdf": 3,
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def reviewed_ids() -> set[str]:
    result: set[str] = set()
    accepted = load_json(ROOT / "audits/rag/accepted-mappings.json")
    for mapping in accepted.get("mappings", []):
        source_unit_id = mapping.get("source_unit_id")
        if source_unit_id:
            result.add(source_unit_id)

    for path in sorted((ROOT / "audits/rag/reviewed").glob("*.json")):
        data = load_json(path)
        for mapping in data.get("mappings", []):
            result.update(mapping.get("source_unit_ids", []))
    return result


def pending_units(source_id: str | None = None) -> tuple[list[dict], list[dict], set[str]]:
    units = load_json(ROOT / "audits/rag/source-units.json").get("units", [])
    accepted = reviewed_ids()
    semantic = [item for item in units if item.get("review_status") == "mapped"]
    indexed = list(enumerate(semantic))
    indexed.sort(
        key=lambda pair: (
            SOURCE_PRIORITY.get(pair[1].get("source_id", ""), 999),
            pair[0],
        )
    )
    pending = [
        item
        for _, item in indexed
        if item.get("id") not in accepted
        and (source_id is None or item.get("source_id") == source_id)
    ]
    return units, pending, accepted


def print_summary(units: list[dict], pending: list[dict], accepted: set[str]) -> None:
    semantic = [item for item in units if item.get("review_status") == "mapped"]
    semantic_by_source = Counter(item.get("source_id") for item in semantic)
    reviewed_by_source = Counter(
        item.get("source_id") for item in semantic if item.get("id") in accepted
    )
    print("source_id\tsemantic\treviewed\tpending")
    for source_id, _ in sorted(SOURCE_PRIORITY.items(), key=lambda item: item[1]):
        semantic_count = semantic_by_source[source_id]
        reviewed_count = reviewed_by_source[source_id]
        print(
            f"{source_id}\t{semantic_count}\t{reviewed_count}"
            f"\t{semantic_count - reviewed_count}"
        )
    print(
        f"TOTAL\t{len(semantic)}\t{len(semantic) - len(pending)}\t{len(pending)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=sorted(SOURCE_PRIORITY))
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    units, pending, accepted = pending_units(args.source)
    if args.summary:
        _, all_pending, _ = pending_units()
        print_summary(units, all_pending, accepted)
        return 0

    selected = pending[: max(args.limit, 0)]
    if args.json:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return 0

    print("source_id\tsource_unit_id\tpath\tlocator\ttitle\tcanonical_topic")
    for item in selected:
        print(
            "\t".join(
                str(item.get(key, ""))
                for key in (
                    "source_id",
                    "id",
                    "path",
                    "locator",
                    "title",
                    "canonical_topic",
                )
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

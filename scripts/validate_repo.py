#!/usr/bin/env python3
"""Validate AI-Learn's machine-readable indexes and publication gates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "sources/registry.json",
    "sources/rag-scope.json",
    "taxonomy/domains.json",
    "taxonomy/rag-topics.json",
    "knowledge/rag/README.md",
    "audits/rag/acceptance.md",
    "templates/knowledge-note.md",
]


def load_json(rel_path: str, errors: list[str]):
    path = ROOT / rel_path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # validation should report all format errors together
        errors.append(f"{rel_path}: {exc}")
        return {}


def duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return sorted(repeated)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict-rag", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []

    for rel_path in REQUIRED:
        if not (ROOT / rel_path).is_file():
            errors.append(f"缺少必需文件：{rel_path}")

    registry = load_json("sources/registry.json", errors)
    scope = load_json("sources/rag-scope.json", errors)
    domains = load_json("taxonomy/domains.json", errors)
    rag_topics = load_json("taxonomy/rag-topics.json", errors)

    sources = registry.get("sources", [])
    source_ids = [item.get("id", "") for item in sources]
    if repeated := duplicates(source_ids):
        errors.append(f"来源 ID 重复：{repeated}")
    for source in sources:
        if not re.fullmatch(r"[0-9a-f]{40}", source.get("commit", "")):
            errors.append(f"来源 {source.get('id')} 的 Commit 不是 40 位 SHA")
        if not source.get("import_policy"):
            errors.append(f"来源 {source.get('id')} 缺少 import_policy")

    domain_ids = [item.get("id", "") for item in domains.get("domains", [])]
    if repeated := duplicates(domain_ids):
        errors.append(f"领域 ID 重复：{repeated}")
    if "RAG" not in domain_ids:
        errors.append("domains.json 缺少 RAG 领域")

    topic_ids = [item.get("id", "") for item in rag_topics.get("topics", [])]
    if repeated := duplicates(topic_ids):
        errors.append(f"RAG 主题 ID 重复：{repeated}")
    if topic_ids != [f"RAG-{index:02d}" for index in range(1, 14)]:
        errors.append("RAG 主题必须连续覆盖 RAG-01 到 RAG-13")

    for item in scope.get("sources", []):
        if item.get("source_id") not in source_ids:
            errors.append(f"rag-scope 引用了未知来源：{item.get('source_id')}")
        files = item.get("files", [])
        if not files or len(files) != len(set(files)):
            errors.append(f"rag-scope 的 {item.get('source_id')} 文件为空或重复")

    inventory_path = ROOT / "audits/rag/source-units.json"
    if inventory_path.exists():
        inventory = load_json("audits/rag/source-units.json", errors)
        units = inventory.get("units", [])
        unit_ids = [item.get("id", "") for item in units]
        if repeated := duplicates(unit_ids):
            errors.append(f"来源单元 ID 重复：{repeated[:10]}")
        for unit in units:
            topic = unit.get("canonical_topic")
            if topic is not None and topic not in topic_ids:
                errors.append(f"来源单元 {unit.get('id')} 引用了未知主题 {topic}")
        if inventory.get("unit_count") != len(units):
            errors.append("source-units.json 的 unit_count 与实际数组长度不一致")
        if args.strict_rag:
            unresolved = [u for u in units if u.get("review_status") in {"unmapped", "missing"}]
            if unresolved:
                errors.append(f"严格 RAG 验收仍有 {len(unresolved)} 个未映射或缺失单元")
    elif args.strict_rag:
        errors.append("严格 RAG 验收缺少 audits/rag/source-units.json")

    if args.strict_rag:
        acceptance = (ROOT / "audits/rag/acceptance.md").read_text(encoding="utf-8")
        unchecked = len(re.findall(r"^- \[ \]", acceptance, re.M))
        if unchecked:
            errors.append(f"RAG 验收清单仍有 {unchecked} 项未完成")

    if errors:
        print("VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALIDATION PASSED")
    print(f"sources={len(source_ids)} domains={len(domain_ids)} rag_topics={len(topic_ids)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())


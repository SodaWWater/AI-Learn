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
    "knowledge/rag/catalog.json",
    "knowledge/rag/catalog.md",
    "learning/rag/draft-overview.md",
    "audits/rag/source-units.json",
    "audits/rag/atom-suggestions.json",
    "audits/rag/accepted-mappings.json",
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
    rag_catalog = load_json("knowledge/rag/catalog.json", errors)

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

    catalog_sections = rag_catalog.get("sections", [])
    catalog_section_ids = [section.get("id", "") for section in catalog_sections]
    if catalog_section_ids != topic_ids:
        errors.append("RAG catalog 的章节顺序必须与 rag-topics.json 一致")
    atom_ids: list[str] = []
    for section in catalog_sections:
        section_id = section.get("id", "")
        atoms = section.get("atoms", [])
        if not atoms:
            errors.append(f"RAG catalog 的 {section_id} 没有知识原子")
        for atom in atoms:
            atom_id = atom.get("id", "")
            atom_ids.append(atom_id)
            if not re.fullmatch(rf"{re.escape(section_id)}-\d{{3}}", atom_id):
                errors.append(f"知识原子 ID 与章节不匹配：{atom_id}")
            if not atom.get("title"):
                errors.append(f"知识原子缺少标题：{atom_id}")
    if repeated := duplicates(atom_ids):
        errors.append(f"知识原子 ID 重复：{repeated}")

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

    suggestions_path = ROOT / "audits/rag/atom-suggestions.json"
    if suggestions_path.exists():
        suggestions = load_json("audits/rag/atom-suggestions.json", errors)
        mappings = suggestions.get("mappings", [])
        source_unit_ids = {
            item.get("id")
            for item in load_json("audits/rag/source-units.json", errors).get("units", [])
        }
        mapped_unit_ids = [item.get("source_unit_id") for item in mappings]
        if set(mapped_unit_ids) != source_unit_ids:
            errors.append("atom-suggestions.json 未与来源单元形成一一对应")
        if repeated := duplicates(mapped_unit_ids):
            errors.append(f"atom-suggestions.json 来源单元重复：{repeated[:10]}")
        for mapping in mappings:
            accepted = mapping.get("accepted_atom_id")
            if accepted is not None and accepted not in atom_ids:
                errors.append(f"接受了未知知识原子：{accepted}")
            for candidate in mapping.get("candidates", []):
                if candidate.get("atom_id") not in atom_ids:
                    errors.append(f"候选引用未知知识原子：{candidate.get('atom_id')}")
    accepted_path = ROOT / "audits/rag/accepted-mappings.json"
    accepted_source_unit_ids: set[str] = set()
    if accepted_path.exists():
        accepted_files = [accepted_path, *sorted((ROOT / "audits/rag/reviewed").glob("*.json"))]
        accepted_mappings = []
        for path in accepted_files:
            payload = load_json(str(path.relative_to(ROOT)), errors)
            accepted_mappings.extend(payload.get("mappings", []))
        accepted_ids: list[str] = []
        for item in accepted_mappings:
            if "source_unit_ids" in item:
                accepted_ids.extend(item.get("source_unit_ids", []))
            else:
                accepted_ids.append(item.get("source_unit_id"))
        accepted_source_unit_ids = set(accepted_ids)
        if repeated := duplicates(accepted_ids):
            errors.append(f"accepted-mappings.json 来源单元重复：{repeated[:10]}")
        for mapping in accepted_mappings:
            unit_refs = mapping.get("source_unit_ids", [mapping.get("source_unit_id")])
            for unit_ref in unit_refs:
                if unit_ref not in source_unit_ids:
                    errors.append(f"人工映射引用未知来源单元：{unit_ref}")
            decision = mapping.get("decision")
            atom_refs = mapping.get("atom_ids", [])
            if decision == "map" and not atom_refs:
                errors.append(f"人工 map 决策没有知识原子：{unit_refs[:3]}")
            for atom_id in atom_refs:
                if atom_id not in atom_ids:
                    errors.append(f"人工映射引用未知知识原子：{atom_id}")
    elif args.strict_rag:
        errors.append("严格 RAG 验收缺少 accepted-mappings.json")

    mindmap_dir = ROOT / "learning/rag/draft-modules"
    mindmap_files = sorted(mindmap_dir.glob("rag-*.md"))
    expected_mindmap_files = {
        f"{section.get('id', '').lower()}.md" for section in rag_catalog.get("sections", [])
    }
    actual_mindmap_files = {path.name for path in mindmap_files}
    if actual_mindmap_files != expected_mindmap_files:
        errors.append("RAG 模块思维导图文件未与目录模块一一对应")
    mindmap_atom_ids: list[str] = []
    for path in mindmap_files:
        mindmap_atom_ids.extend(
            re.findall(r"RAG-\d{2}-\d{3}", path.read_text(encoding="utf-8"))
        )
    if set(mindmap_atom_ids) != set(atom_ids):
        errors.append("RAG 模块思维导图没有覆盖全部原子知识点")
    if repeated := duplicates(mindmap_atom_ids):
        errors.append(f"RAG 模块思维导图重复知识原子：{repeated[:10]}")

    if args.strict_rag and inventory_path.exists():
        reviewable_ids = {
            unit.get("id")
            for unit in load_json("audits/rag/source-units.json", errors).get("units", [])
            if unit.get("review_status") == "mapped"
        }
        remaining = reviewable_ids - accepted_source_unit_ids
        if remaining:
            errors.append(f"严格 RAG 验收仍有 {len(remaining)} 个来源单元待人工复核")

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
    print(
        f"sources={len(source_ids)} domains={len(domain_ids)} "
        f"rag_topics={len(topic_ids)} rag_atoms={len(atom_ids)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

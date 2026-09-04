"""Audit the inventory-level RAG graph for coverage and evidence traceability.

This is a conservative P3-003 audit.  It reports missing graph structure and
explicit version or conflict records already present in local evidence; it does
not infer a technical conflict merely because a relationship is not yet modeled.
No external search is performed.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "audits/rag/graph-coverage-audit.json"
UNDIRECTED_EDGE_TYPES = {
    "alternative_to",
    "combined_with",
    "conflicts_with",
    "overlaps_with",
}
VERSION_PATTERN = re.compile(r"\b(version|versions|versioned|api|commit|release|revision|preview)\b", re.I)
CONFLICT_PATTERN = re.compile(r"\b(conflict\w*|contradict\w*|inconsisten\w*)\b", re.I)


def load_json(relative_path: str) -> Any:
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def load_json_files(directory: str) -> list[tuple[str, dict[str, Any]]]:
    return [
        (path.name, json.loads(path.read_text(encoding="utf-8")))
        for path in sorted((ROOT / directory).glob("*.json"))
    ]


def source_node_id(source_id: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", source_id).strip("-").upper()
    return f"SRC-{normalized}"


def sorted_unique(items: Iterable[str]) -> list[str]:
    return sorted(set(items))


def mapping_summary(payloads: Iterable[dict[str, Any]]) -> dict[str, Any]:
    decision_counts: Counter[str] = Counter()
    source_unit_ids: set[str] = set()
    atom_ids: set[str] = set()
    records = 0
    for payload in payloads:
        for mapping in payload.get("mappings", []):
            records += 1
            decision_counts[mapping.get("decision", "unspecified")] += 1
            source_unit_ids.update(filter(None, mapping.get("source_unit_ids", [])))
            if mapping.get("source_unit_id"):
                source_unit_ids.add(mapping["source_unit_id"])
            atom_ids.update(mapping.get("atom_ids", []))
    return {
        "mapping_records": records,
        "mapped_source_units": len(source_unit_ids),
        "mapped_catalog_atoms": len(atom_ids),
        "decision_counts": dict(sorted(decision_counts.items())),
    }


def evidence_findings(
    evidence_files: list[tuple[str, dict[str, Any]]], source_metadata: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    version_records: list[dict[str, Any]] = []
    conflict_topic_records: list[dict[str, Any]] = []
    for filename, payload in evidence_files:
        for record in payload.get("records", []):
            text = " ".join(
                [*record.get("verified_claims", []), record.get("boundary", "")]
            )
            item = {
                "evidence_file": filename,
                "source_id": record.get("source_id"),
                "source_version": source_metadata.get(record.get("source_id"), {}).get("version"),
                "status": record.get("status"),
                "atom_ids": sorted(record.get("atom_ids", [])),
                "boundary": record.get("boundary", ""),
            }
            if VERSION_PATTERN.search(text):
                version_records.append(item)
            if CONFLICT_PATTERN.search(text):
                conflict_topic_records.append(item)
    order_key = lambda item: (item["source_id"] or "", item["evidence_file"])
    return {
        "explicit_graph_conflicts": [],
        "explicit_graph_supersedes": [],
        "evidence_conflict_topic_records": sorted(conflict_topic_records, key=order_key),
        "evidence_version_boundary_records": sorted(version_records, key=order_key),
        "interpretation": (
            "Evidence records may describe conflicting retrieved content or version-dependent behavior. "
            "They are not source-to-source conclusion conflicts unless the graph has an explicit conflicts_with edge."
        ),
    }


def main() -> None:
    graph = load_json("knowledge/rag/graph.json")
    catalog = load_json("knowledge/rag/catalog.json")
    accepted = load_json("audits/rag/accepted-mappings.json")
    reviewed_files = load_json_files("audits/rag/reviewed")
    evidence_files = load_json_files("audits/rag/evidence")
    registry = load_json("sources/registry.json")
    current_sources = load_json("sources/rag-current-sources.json")
    scenarios = load_json("interview/rag/public-scenarios.json")
    verification = load_json("audits/rag/evidence-verification-status.json")

    nodes = sorted(graph["nodes"], key=lambda item: item["id"])
    edges = sorted(graph["edges"], key=lambda item: item["id"])
    source_node_ids = {node["id"] for node in nodes if node["type"] == "source"}
    registered_source_ids = {
        source["id"] for source in [*registry["sources"], *current_sources["sources"]]
    }
    source_metadata = {
        source["id"]: source
        for source in [*registry["sources"], *current_sources["sources"]]
    }
    waived_source_ids = sorted(
        item["source_id"] for item in verification.get("waived_sources", [])
    )
    waived_node_ids = {source_node_id(source_id) for source_id in waived_source_ids}

    incoming: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    outgoing: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    supported_by_targets: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    problem_to_knowledge: defaultdict[str, set[str]] = defaultdict(set)
    knowledge_to_problem: defaultdict[str, set[str]] = defaultdict(set)
    for edge in edges:
        outgoing[edge["from"]].append(edge)
        incoming[edge["to"]].append(edge)
        if edge["type"] in UNDIRECTED_EDGE_TYPES:
            outgoing[edge["to"]].append(edge)
            incoming[edge["from"]].append(edge)
        if edge["type"] == "supported_by":
            supported_by_targets[edge["from"]].append(edge)
        if edge["type"] == "problem_at":
            problem_to_knowledge[edge["from"]].add(edge["to"])
            knowledge_to_problem[edge["to"]].add(edge["from"])

    catalog_atom_ids = sorted(
        atom["id"] for section in catalog["sections"] for atom in section["atoms"]
    )
    graph_knowledge_ids = sorted(
        node["id"] for node in nodes if node["type"] == "knowledge"
    )
    non_source_nodes = [node for node in nodes if node["type"] != "source"]
    node_type_coverage: list[dict[str, Any]] = []
    for node_type in sorted({node["type"] for node in nodes}):
        typed_nodes = [node for node in nodes if node["type"] == node_type]
        node_type_coverage.append(
            {
                "node_type": node_type,
                "total": len(typed_nodes),
                "with_node_source_refs": sum(bool(node.get("source_refs")) for node in typed_nodes),
                "with_supported_by": sum(bool(supported_by_targets[node["id"]]) for node in typed_nodes),
                "with_any_graph_connection": sum(
                    bool(incoming[node["id"]] or outgoing[node["id"]]) for node in typed_nodes
                ),
            }
        )

    missing_supported_by = [
        {
            "id": node["id"],
            "type": node["type"],
            "status": node["status"],
            "source_refs": sorted(node.get("source_refs", [])),
        }
        for node in non_source_nodes
        if not supported_by_targets[node["id"]]
    ]
    isolated_nodes = [
        {"id": node["id"], "type": node["type"], "status": node["status"]}
        for node in nodes
        if not incoming[node["id"]] and not outgoing[node["id"]]
    ]
    unreferenced_knowledge = [
        {
            "id": node["id"],
            "label_zh": node["label_zh"],
            "status": node["status"],
            "source_refs": sorted(node.get("source_refs", [])),
        }
        for node in nodes
        if node["type"] == "knowledge" and not knowledge_to_problem[node["id"]]
    ]

    unregistered_refs: defaultdict[str, set[str]] = defaultdict(set)
    for node in nodes:
        for reference in node.get("source_refs", []):
            if reference not in source_node_ids:
                unregistered_refs[reference].add(f"node:{node['id']}")
    for edge in edges:
        for reference in edge.get("source_refs", []):
            if reference not in source_node_ids:
                unregistered_refs[reference].add(f"edge:{edge['id']}")
    source_ref_without_source_node = [
        {"source_ref": reference, "referenced_by": sorted(owners)}
        for reference, owners in sorted(unregistered_refs.items())
    ]

    waived_violations: list[dict[str, Any]] = []
    for node in non_source_nodes:
        for reference in sorted(set(node.get("source_refs", [])) & waived_node_ids):
            waived_violations.append(
                {"kind": "node_source_ref", "owner": node["id"], "waived_source": reference}
            )
    for edge in edges:
        for reference in sorted(set(edge.get("source_refs", [])) & waived_node_ids):
            waived_violations.append(
                {"kind": "edge_source_ref", "owner": edge["id"], "waived_source": reference}
            )
        if edge["type"] == "supported_by" and edge["to"] in waived_node_ids:
            waived_violations.append(
                {"kind": "supported_by_target", "owner": edge["id"], "waived_source": edge["to"]}
            )

    reverse_problem_mapping = [
        {
            "knowledge_id": knowledge_id,
            "problem_ids": sorted(knowledge_to_problem[knowledge_id]),
        }
        for knowledge_id in graph_knowledge_ids
    ]
    problem_mapping_mismatches: list[dict[str, Any]] = []
    for problem in (node for node in nodes if node["type"] == "problem_question"):
        declared = set(problem.get("knowledge_node_ids", []))
        edged = problem_to_knowledge[problem["id"]]
        if declared != edged:
            problem_mapping_mismatches.append(
                {
                    "problem_id": problem["id"],
                    "declared_knowledge_ids": sorted(declared),
                    "problem_at_knowledge_ids": sorted(edged),
                }
            )

    conflict_and_version = evidence_findings(evidence_files, source_metadata)
    conflict_and_version["explicit_graph_conflicts"] = [
        {
            "edge_id": edge["id"],
            "from": edge["from"],
            "to": edge["to"],
            "source_refs": sorted(edge.get("source_refs", [])),
        }
        for edge in edges
        if edge["type"] == "conflicts_with"
    ]
    conflict_and_version["explicit_graph_supersedes"] = [
        {
            "edge_id": edge["id"],
            "from": edge["from"],
            "to": edge["to"],
            "source_refs": sorted(edge.get("source_refs", [])),
        }
        for edge in edges
        if edge["type"] == "supersedes"
    ]

    all_mapping_payloads = [accepted, *(payload for _, payload in reviewed_files)]
    cross_backbone_ids = {
        "BB-VECTOR-DATABASE",
        "BB-AGENT",
        "BB-PROMPT-ENGINEERING",
        "BB-KNOWLEDGE-GRAPH",
    }
    cross_backbone_capability_ids = {
        "CAP-VECTOR-INDEX",
        "CAP-METADATA-FILTERING",
        "CAP-AGENTIC-PLANNING",
        "CAP-TOOL-USE",
        "CAP-PROMPT-ABSTRACTION",
        "CAP-PROMPT-CONTEXT-ASSEMBLY",
        "CAP-GRAPH-INDEXING",
        "CAP-GRAPH-RETRIEVAL",
    }
    cross_backbone_entity_ids = cross_backbone_ids | cross_backbone_capability_ids
    cross_backbone_nodes = [node for node in nodes if node["id"] in cross_backbone_entity_ids]
    cross_backbone_edges = [
        edge
        for edge in edges
        if edge["type"] in {"overlaps_with", "branches_to", "merges_into"}
        and (edge["from"] in cross_backbone_entity_ids or edge["to"] in cross_backbone_entity_ids)
    ]
    expected_cross_backbones = sorted(cross_backbone_ids)
    cross_backbone_audit = {
        "expected_backbone_ids": expected_cross_backbones,
        "present_backbone_ids": sorted(cross_backbone_ids & {node["id"] for node in cross_backbone_nodes}),
        "missing_backbone_ids": sorted(cross_backbone_ids - {node["id"] for node in cross_backbone_nodes}),
        "expected_capability_ids": sorted(cross_backbone_capability_ids),
        "present_capability_ids": sorted(cross_backbone_capability_ids & {node["id"] for node in cross_backbone_nodes}),
        "missing_capability_ids": sorted(cross_backbone_capability_ids - {node["id"] for node in cross_backbone_nodes}),
        "entities_with_source_refs": sorted(node["id"] for node in cross_backbone_nodes if node.get("source_refs")),
        "cross_backbone_edge_count": len(cross_backbone_edges),
        "edge_type_counts": dict(sorted(Counter(edge["type"] for edge in cross_backbone_edges).items())),
        "edges": [
            {
                "id": edge["id"],
                "type": edge["type"],
                "from": edge["from"],
                "to": edge["to"],
                "source_refs": sorted(edge.get("source_refs", [])),
            }
            for edge in cross_backbone_edges
        ],
        "status": "complete" if len(cross_backbone_nodes) == len(expected_cross_backbones) and cross_backbone_edges else "gap",
        "boundary": "Cross-backbone inventory is limited to registered verified evidence and does not assert equivalence, universal quality, or product-neutral behavior.",
    }
    audit = {
        "schema_version": 1,
        "work_item_id": "WP-P3-003",
        "generated_at": graph.get("generated_at"),
        "status": "completed_inventory_audit",
        "scope": "Coverage, isolation, source traceability, reverse problem mappings, and explicit conflict/version evidence for the inventory-level RAG graph; no external search.",
        "inputs": {
            "graph": "knowledge/rag/graph.json",
            "catalog": "knowledge/rag/catalog.json",
            "manual_mappings": ["audits/rag/accepted-mappings.json", "audits/rag/reviewed/*.json"],
            "evidence": "audits/rag/evidence/*.json",
            "source_registries": ["sources/registry.json", "sources/rag-current-sources.json"],
            "public_scenarios": "interview/rag/public-scenarios.json",
        },
        "input_summary": {
            "registered_source_ids": len(registered_source_ids),
            "graph_source_nodes": len(source_node_ids),
            "evidence_files": len(evidence_files),
            "reviewed_mapping_files": len(reviewed_files),
            "manual_mapping_summary": mapping_summary(all_mapping_payloads),
            "public_scenarios": len(scenarios["scenarios"]),
        },
        "node_type_coverage": node_type_coverage,
        "catalog_alignment": {
            "catalog_knowledge_atoms": len(catalog_atom_ids),
            "graph_knowledge_nodes": len(graph_knowledge_ids),
            "catalog_atoms_missing_from_graph": sorted(set(catalog_atom_ids) - set(graph_knowledge_ids)),
            "graph_knowledge_nodes_missing_from_catalog": sorted(set(graph_knowledge_ids) - set(catalog_atom_ids)),
        },
        "cross_backbone_audit": cross_backbone_audit,
        "source_registry_alignment": {
            "registered_sources_missing_graph_source_node": sorted(
                source_node_id(source_id)
                for source_id in registered_source_ids
                if source_node_id(source_id) not in source_node_ids
            ),
            "graph_source_nodes_not_in_registered_sources": sorted(
                source_id
                for source_id in source_node_ids
                if source_id not in {source_node_id(item) for item in registered_source_ids}
            ),
        },
        "missing_supported_by_for_non_source_nodes": missing_supported_by,
        "isolated_nodes": isolated_nodes,
        "knowledge_not_referenced_by_problem": unreferenced_knowledge,
        "source_refs_without_graph_source_node": source_ref_without_source_node,
        "waived_source_audit": {
            "waived_source_ids": waived_source_ids,
            "waived_source_node_ids": sorted(waived_node_ids),
            "violations": sorted(waived_violations, key=lambda item: (item["owner"], item["kind"])),
            "allowed_representation": "The waived source may remain as a source node tagged waived_unavailable and non_evidentiary, but may not support a non-source node or edge.",
        },
        "reverse_problem_mapping": reverse_problem_mapping,
        "problem_mapping_mismatches": problem_mapping_mismatches,
        "conflict_and_version_audit": conflict_and_version,
        "limitations": [
            "This report does not infer a missing relationship, unreferenced knowledge node, or common topic as a technical conflict.",
            "Evidence conflict-topic records describe source content about conflict handling; they do not establish a conflict between registered sources.",
            "Inventory_draft and source_mapped nodes are not final knowledge chapters or final canonical claims.",
        ],
        "next_actions": [
            "Add supported_by edges only where an existing registered, non-waived source explicitly supports the node boundary.",
            "Classify isolated and problem-unreferenced nodes as intentional inventory, future mapping work, or candidates for removal only after semantic review.",
            "Model a conflicts_with or supersedes edge only when a specific source-to-source conflict or version replacement is explicitly recorded.",
        ],
    }
    OUTPUT_PATH.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

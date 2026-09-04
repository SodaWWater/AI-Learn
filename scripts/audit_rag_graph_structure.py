"""Audit the RAG directed knowledge graph against its controlled model.

The audit is intentionally read-only with respect to graph inputs. It writes a
deterministic, machine-readable report so graph construction and later coverage
audits can distinguish structural defects from inventory-level gaps.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "taxonomy/rag-graph-model.json"
GRAPH_PATH = ROOT / "knowledge/rag/graph.json"
WAIVER_PATH = ROOT / "audits/rag/evidence-verification-status.json"
REPORT_PATH = ROOT / "audits/rag/graph-structure-audit.json"

UNDIRECTED_EDGE_TYPES = {
    "overlaps_with",
    "alternative_to",
    "combined_with",
    "conflicts_with",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_node_id(source_id: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", source_id).strip("-").upper()
    return f"SRC-{normalized}"


def diagnostic(code: str, entity_type: str, entity_id: str, message: str, **context: Any) -> dict[str, Any]:
    item = {
        "code": code,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "message": message,
    }
    if context:
        item["context"] = context
    return item


def sort_diagnostics(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        items,
        key=lambda item: (item["code"], item["entity_type"], item["entity_id"]),
    )


def type_counts(items: list[dict[str, Any]], prefix: str) -> dict[str, int]:
    counts = Counter(item.get("type", "<missing>") for item in items)
    return {f"{prefix}_{key}": counts[key] for key in sorted(counts)}


def main() -> None:
    model = load_json(MODEL_PATH)
    graph = load_json(GRAPH_PATH)
    waiver_status = load_json(WAIVER_PATH)

    allowed_node_types = {item["id"] for item in model["node_types"]}
    allowed_edge_types = {item["id"] for item in model["edge_types"]}
    allowed_review_statuses = set(model["review_statuses"])
    allowed_provenance_types = {
        item["id"] for item in model["problem_provenance_types"]
    }
    required_node_fields = model["required_node_fields"]
    required_edge_fields = model["required_edge_fields"]
    id_patterns = {
        node_type: re.compile(pattern)
        for node_type, pattern in model["node_id_patterns"].items()
    }
    waived_source_ids = sorted(
        item["source_id"] for item in waiver_status.get("waived_sources", [])
    )
    waived_source_nodes = {source_node_id(source_id) for source_id in waived_source_ids}

    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list):
        errors.append(
            diagnostic(
                "graph_nodes_not_list",
                "graph",
                "knowledge/rag/graph.json",
                "nodes must be a JSON array.",
            )
        )
        nodes = []
    if not isinstance(edges, list):
        errors.append(
            diagnostic(
                "graph_edges_not_list",
                "graph",
                "knowledge/rag/graph.json",
                "edges must be a JSON array.",
            )
        )
        edges = []

    node_by_id: dict[str, dict[str, Any]] = {}
    node_id_counts = Counter()
    for index, node in enumerate(nodes):
        entity_id = str(node.get("id", f"<node-index-{index}>"))
        if not isinstance(node, dict):
            errors.append(
                diagnostic(
                    "node_not_object", "node", entity_id, "Each node must be a JSON object."
                )
            )
            continue
        for field in required_node_fields:
            if field not in node:
                errors.append(
                    diagnostic(
                        "missing_required_node_field",
                        "node",
                        entity_id,
                        "Node is missing a required graph-model field.",
                        field=field,
                    )
                )
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            errors.append(
                diagnostic(
                    "invalid_node_id", "node", entity_id, "Node id must be a non-empty string."
                )
            )
            continue
        node_id_counts[node_id] += 1
        node_by_id.setdefault(node_id, node)
        node_type = node.get("type")
        if node_type not in allowed_node_types:
            errors.append(
                diagnostic(
                    "unregistered_node_type",
                    "node",
                    node_id,
                    "Node type is not registered in the graph model.",
                    node_type=node_type,
                )
            )
        elif not id_patterns[node_type].fullmatch(node_id):
            errors.append(
                diagnostic(
                    "node_id_pattern_mismatch",
                    "node",
                    node_id,
                    "Node id does not match the registered pattern for its type.",
                    node_type=node_type,
                    pattern=id_patterns[node_type].pattern,
                )
            )
        if node.get("status") not in allowed_review_statuses:
            errors.append(
                diagnostic(
                    "unregistered_node_status",
                    "node",
                    node_id,
                    "Node status is not registered in the graph model.",
                    status=node.get("status"),
                )
            )
        source_refs = node.get("source_refs")
        if not isinstance(source_refs, list):
            errors.append(
                diagnostic(
                    "node_source_refs_not_list",
                    "node",
                    node_id,
                    "Node source_refs must be a JSON array.",
                )
            )

    for node_id, count in sorted(node_id_counts.items()):
        if count > 1:
            errors.append(
                diagnostic(
                    "duplicate_node_id",
                    "node",
                    node_id,
                    "Node id occurs more than once.",
                    occurrences=count,
                )
            )

    source_node_ids = {
        node_id
        for node_id, node in node_by_id.items()
        if node.get("type") == "source"
    }
    edge_by_id: dict[str, dict[str, Any]] = {}
    edge_id_counts = Counter()
    relation_counts = Counter()
    incoming: dict[str, list[dict[str, Any]]] = defaultdict(list)
    outgoing: dict[str, list[dict[str, Any]]] = defaultdict(list)
    edge_keys: dict[tuple[str, str, str], list[str]] = defaultdict(list)

    for index, edge in enumerate(edges):
        entity_id = str(edge.get("id", f"<edge-index-{index}>")) if isinstance(edge, dict) else f"<edge-index-{index}>"
        if not isinstance(edge, dict):
            errors.append(
                diagnostic(
                    "edge_not_object", "edge", entity_id, "Each edge must be a JSON object."
                )
            )
            continue
        for field in required_edge_fields:
            if field not in edge:
                errors.append(
                    diagnostic(
                        "missing_required_edge_field",
                        "edge",
                        entity_id,
                        "Edge is missing a required graph-model field.",
                        field=field,
                    )
                )
        edge_id = edge.get("id")
        if not isinstance(edge_id, str) or not edge_id:
            errors.append(
                diagnostic(
                    "invalid_edge_id", "edge", entity_id, "Edge id must be a non-empty string."
                )
            )
            continue
        edge_id_counts[edge_id] += 1
        edge_by_id.setdefault(edge_id, edge)
        edge_type = edge.get("type")
        from_id = edge.get("from")
        to_id = edge.get("to")
        if edge_type not in allowed_edge_types:
            errors.append(
                diagnostic(
                    "unregistered_edge_type",
                    "edge",
                    edge_id,
                    "Edge type is not registered in the graph model.",
                    edge_type=edge_type,
                )
            )
        if not isinstance(from_id, str) or from_id not in node_by_id:
            errors.append(
                diagnostic(
                    "dangling_edge_from",
                    "edge",
                    edge_id,
                    "Edge from endpoint does not resolve to a graph node.",
                    endpoint=from_id,
                )
            )
        if not isinstance(to_id, str) or to_id not in node_by_id:
            errors.append(
                diagnostic(
                    "dangling_edge_to",
                    "edge",
                    edge_id,
                    "Edge to endpoint does not resolve to a graph node.",
                    endpoint=to_id,
                )
            )
        if isinstance(from_id, str) and isinstance(to_id, str):
            if from_id == to_id:
                errors.append(
                    diagnostic(
                        "self_referential_edge",
                        "edge",
                        edge_id,
                        "An edge must not point to the same node at both endpoints.",
                    )
                )
            key_from, key_to = from_id, to_id
            if edge_type in UNDIRECTED_EDGE_TYPES and key_to < key_from:
                errors.append(
                    diagnostic(
                        "unnormalized_undirected_edge",
                        "edge",
                        edge_id,
                        "Undirected edge endpoints must use ascending stable id order.",
                        expected_from=key_to,
                        expected_to=key_from,
                    )
                )
                key_from, key_to = key_to, key_from
            edge_keys[(str(edge_type), key_from, key_to)].append(edge_id)
            relation_counts[str(edge_type)] += 1
            outgoing[from_id].append(edge)
            incoming[to_id].append(edge)
        source_refs = edge.get("source_refs")
        if not isinstance(source_refs, list):
            errors.append(
                diagnostic(
                    "edge_source_refs_not_list",
                    "edge",
                    edge_id,
                    "Edge source_refs must be a JSON array.",
                )
            )
        elif not source_refs and edge_type not in {"contains", "next_stage"}:
            warnings.append(
                diagnostic(
                    "edge_without_direct_source_refs",
                    "edge",
                    edge_id,
                    "Non-structural edge has no direct source reference; retain explicit evidence before formal publication.",
                    edge_type=edge_type,
                )
            )

    for edge_id, count in sorted(edge_id_counts.items()):
        if count > 1:
            errors.append(
                diagnostic(
                    "duplicate_edge_id",
                    "edge",
                    edge_id,
                    "Edge id occurs more than once.",
                    occurrences=count,
                )
            )
    for (edge_type, from_id, to_id), edge_ids in sorted(edge_keys.items()):
        if len(edge_ids) > 1:
            errors.append(
                diagnostic(
                    "duplicate_edge_relation",
                    "edge_relation",
                    f"{edge_type}:{from_id}:{to_id}",
                    "Multiple edges encode the same normalized relation.",
                    edge_ids=sorted(edge_ids),
                )
            )

    # Verify every declared source reference resolves to an actual source node and
    # that the waived EUR-Lex record never becomes evidentiary support.
    for entity_type, entities in (("node", nodes), ("edge", edges)):
        for index, entity in enumerate(entities):
            if not isinstance(entity, dict):
                continue
            entity_id = str(entity.get("id", f"<{entity_type}-index-{index}>"))
            refs = entity.get("source_refs")
            if not isinstance(refs, list):
                continue
            for ref in sorted(set(refs)):
                if ref not in source_node_ids:
                    errors.append(
                        diagnostic(
                            "unresolved_source_ref",
                            entity_type,
                            entity_id,
                            "source_refs entry does not resolve to a source node.",
                            source_ref=ref,
                        )
                    )
                if ref in waived_source_nodes:
                    errors.append(
                        diagnostic(
                            "waived_source_used_as_evidence",
                            entity_type,
                            entity_id,
                            "A waived non-evidentiary source must not support a node or edge.",
                            source_ref=ref,
                        )
                    )

    for source_id in waived_source_ids:
        source_id_in_graph = source_node_id(source_id)
        source_node = node_by_id.get(source_id_in_graph)
        if source_node is None:
            errors.append(
                diagnostic(
                    "missing_waived_source_node",
                    "source",
                    source_id_in_graph,
                    "The approved waiver has no source node in the graph.",
                    source_id=source_id,
                )
            )
            continue
        tags = set(source_node.get("tags", []))
        required_tags = {"waived_unavailable", "non_evidentiary"}
        missing_tags = sorted(required_tags - tags)
        if missing_tags:
            errors.append(
                diagnostic(
                    "waived_source_missing_boundary_tags",
                    "source",
                    source_id_in_graph,
                    "The waived source must retain non-evidentiary boundary tags.",
                    missing_tags=missing_tags,
                )
            )

    def node_type(node_id: str) -> str | None:
        node = node_by_id.get(node_id)
        return node.get("type") if node else None

    # Controlled direction checks apply only where the model gives an explicit
    # role relationship. Other controlled edge types remain open for later P3
    # semantic review rather than being constrained by assumptions here.
    allowed_endpoint_types = {
        "next_stage": ({"pipeline_stage"}, {"pipeline_stage"}),
        "supported_by": (allowed_node_types - {"source"}, {"source"}),
        "problem_at": ({"problem_question"}, {"pipeline_stage", "knowledge", "algorithm", "capability"}),
        "solved_by": ({"problem_question"}, {"solution"}),
        "implemented_by": ({"solution"}, {"implementation"}),
        "evaluated_by": ({"problem_question", "knowledge", "solution", "implementation", "pipeline_stage"}, {"evaluation"}),
        "implements": ({"implementation", "algorithm"}, {"knowledge", "capability", "pipeline_stage"}),
    }
    for edge_id, edge in sorted(edge_by_id.items()):
        edge_type = edge.get("type")
        if edge_type not in allowed_endpoint_types:
            continue
        from_type = node_type(edge.get("from"))
        to_type = node_type(edge.get("to"))
        valid_from, valid_to = allowed_endpoint_types[edge_type]
        if from_type not in valid_from or to_type not in valid_to:
            errors.append(
                diagnostic(
                    "edge_direction_or_endpoint_type_mismatch",
                    "edge",
                    edge_id,
                    "Edge endpoints do not match the controlled relation direction.",
                    edge_type=edge_type,
                    from_type=from_type,
                    to_type=to_type,
                    allowed_from_types=sorted(valid_from),
                    allowed_to_types=sorted(valid_to),
                )
            )

    for node_id, node in sorted(node_by_id.items()):
        node_type_value = node.get("type")
        source_refs = node.get("source_refs") if isinstance(node.get("source_refs"), list) else []
        support_edges = [
            edge
            for edge in outgoing.get(node_id, [])
            if edge.get("type") == "supported_by"
        ]
        if node_type_value != "source" and node.get("status") == "reviewed" and not support_edges:
            errors.append(
                diagnostic(
                    "reviewed_node_without_supported_by_edge",
                    "node",
                    node_id,
                    "Reviewed non-source node lacks required supported_by evidence edge.",
                )
            )
        if node_type_value != "source" and node.get("status") == "source_mapped" and not source_refs:
            errors.append(
                diagnostic(
                    "source_mapped_node_without_source_refs",
                    "node",
                    node_id,
                    "source_mapped node must declare at least one source reference.",
                )
            )
        if node_type_value == "problem_question":
            if not any(edge.get("type") == "problem_at" for edge in outgoing.get(node_id, [])):
                errors.append(
                    diagnostic(
                        "problem_without_problem_at_edge",
                        "node",
                        node_id,
                        "Every problem_question node must have at least one outgoing problem_at edge.",
                    )
                )
            provenance_type = node.get("provenance_type")
            if provenance_type not in allowed_provenance_types:
                errors.append(
                    diagnostic(
                        "invalid_problem_provenance_type",
                        "node",
                        node_id,
                        "Problem provenance_type is not registered in the graph model.",
                        provenance_type=provenance_type,
                    )
                )
            elif provenance_type != "engineering_case" and not node.get("source_locator"):
                errors.append(
                    diagnostic(
                        "problem_missing_source_locator",
                        "node",
                        node_id,
                        "Non-engineering_case problem must declare a source locator.",
                    )
                )
        if node_type_value == "solution":
            connected_problems = [
                edge
                for edge in incoming.get(node_id, []) + outgoing.get(node_id, [])
                if edge.get("type") == "solved_by"
                and (
                    node_type(edge.get("from")) == "problem_question"
                    or node_type(edge.get("to")) == "problem_question"
                )
            ]
            if not connected_problems:
                errors.append(
                    diagnostic(
                        "solution_without_problem_connection",
                        "node",
                        node_id,
                        "Every solution node must connect to at least one problem_question node through solved_by.",
                    )
                )
        if node_type_value == "implementation":
            connected_knowledge_or_solution = [
                edge
                for edge in incoming.get(node_id, []) + outgoing.get(node_id, [])
                if (
                    node_type(edge.get("from")) in {"knowledge", "solution"}
                    or node_type(edge.get("to")) in {"knowledge", "solution"}
                )
            ]
            if not connected_knowledge_or_solution:
                errors.append(
                    diagnostic(
                        "implementation_without_knowledge_or_solution_connection",
                        "node",
                        node_id,
                        "Every implementation node must connect to a knowledge or solution node.",
                    )
                )

    # Inventory-level graph gaps are warnings, preserved for WP-P3-003 rather
    # than misclassified as P3-002 schema violations.
    for node_id, node in sorted(node_by_id.items()):
        if node.get("type") == "source":
            continue
        if not incoming.get(node_id) and not outgoing.get(node_id):
            warnings.append(
                diagnostic(
                    "isolated_non_source_node",
                    "node",
                    node_id,
                    "Node has no graph relationships and requires P3-003 disposition.",
                )
            )
        if node.get("status") == "inventory_draft" and not node.get("source_refs"):
            warnings.append(
                diagnostic(
                    "inventory_node_without_source_refs",
                    "node",
                    node_id,
                    "Inventory node has no source reference; it must be resolved or explicitly excluded before formal publication.",
                )
            )

    errors = sort_diagnostics(errors)
    warnings = sort_diagnostics(warnings)
    status = "needs_correction" if errors else "passed_with_warnings" if warnings else "passed"
    report = {
        "schema_version": 1,
        "work_item_id": "WP-P3-002",
        "generated_at": graph.get("generated_at"),
        "audited_graph": "knowledge/rag/graph.json",
        "audited_graph_generated_at": graph.get("generated_at"),
        "model": "taxonomy/rag-graph-model.json",
        "overall_status": status,
        "status": status,
        "scope": "Directed Knowledge Graph structural audit: fields, identifiers, controlled relations, endpoints, source references, graph invariants, duplicates, and waived non-evidentiary evidence.",
        "waived_source_ids": waived_source_ids,
        "counts": {
            "nodes_total": len(nodes),
            "edges_total": len(edges),
            **type_counts(nodes, "nodes"),
            **type_counts(edges, "edges"),
            "errors_total": len(errors),
            "warnings_total": len(warnings),
            "isolated_non_source_nodes": sum(
                1
                for node_id, node in node_by_id.items()
                if node.get("type") != "source"
                and not incoming.get(node_id)
                and not outgoing.get(node_id)
            ),
            "inventory_nodes_without_source_refs": sum(
                1
                for node in node_by_id.values()
                if node.get("type") != "source"
                and node.get("status") == "inventory_draft"
                and not node.get("source_refs")
            ),
            "edge_types": {
                edge_type: relation_counts[edge_type]
                for edge_type in sorted(relation_counts)
            },
        },
        "errors": errors,
        "warnings": warnings,
        "notes": [
            "The report is deterministic for an unchanged graph: generated_at is inherited from the graph rather than the current clock.",
            "Inventory-level nodes without source references are warnings for WP-P3-003 unless their declared status is source_mapped or reviewed.",
            "The user-approved EUR-Lex waiver is checked as non-evidentiary and must not appear in node or edge source_refs.",
        ],
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"RAG graph structural audit: {status}; "
        f"{len(nodes)} nodes, {len(edges)} edges, "
        f"{len(errors)} errors, {len(warnings)} warnings."
    )


if __name__ == "__main__":
    main()

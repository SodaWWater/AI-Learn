"""Build the first canonical RAG graph inventory from audited local data.

This script deliberately produces an inventory/source-mapped graph, not final
knowledge prose. It only uses accepted manual mappings, registered sources,
verified evidence batches, and the existing public scenario inventory.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def dump(path: str, payload) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def source_node_id(source_id: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", source_id).strip("-").upper()
    return f"SRC-{normalized}"


def edge_id(kind: str, left: str, right: str) -> str:
    raw = f"{kind}-{left}-{right}".upper()
    return re.sub(r"[^A-Z0-9-]+", "-", raw)


def add_edge(edges, seen, kind, left, right, explanation, refs, status="source_mapped"):
    directed = kind not in {"overlaps_with", "alternative_to", "combined_with", "conflicts_with"}
    a, b = (left, right)
    if not directed and b < a:
        a, b = b, a
    key = (kind, a, b)
    if key in seen:
        return
    seen.add(key)
    edges.append(
        {
            "id": edge_id(kind, a, b),
            "type": kind,
            "from": a,
            "to": b,
            "explanation": explanation,
            "source_refs": sorted(set(refs)),
            "review_status": status,
        }
    )


def main() -> None:
    catalog = load("knowledge/rag/catalog.json")
    source_units = load("audits/rag/source-units.json")["units"]
    unit_by_id = {item["id"]: item for item in source_units}
    current_sources = load("sources/rag-current-sources.json")["sources"]
    registry_sources = load("sources/registry.json")["sources"]
    scenarios = load("interview/rag/public-scenarios.json")["scenarios"]
    waiver = load("audits/rag/evidence-verification-status.json")["waived_sources"]
    waived_ids = {item["source_id"] for item in waiver}

    source_meta = {}
    for item in registry_sources + current_sources:
        source_meta.setdefault(item["id"], item)
    verification_by_source = defaultdict(list)
    evidence_atom_refs = defaultdict(set)
    evidence_status = {}
    for path in sorted((ROOT / "audits/rag/evidence").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        for record in payload.get("records", []):
            sid = record.get("source_id")
            if not sid:
                continue
            evidence_status[sid] = record.get("status", "verified")
            verification_by_source[sid].append(path.name)
            evidence_atom_refs[sid].update(record.get("atom_ids", []))

    accepted = [load("audits/rag/accepted-mappings.json")]
    accepted.extend(
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "audits/rag/reviewed").glob("*.json"))
    )
    atom_source_ids = defaultdict(set)
    atom_decisions = defaultdict(set)
    for payload in accepted:
        for mapping in payload.get("mappings", []):
            unit_ids = mapping.get("source_unit_ids") or [mapping.get("source_unit_id")]
            decision = mapping.get("decision")
            for unit_id in filter(None, unit_ids):
                unit = unit_by_id.get(unit_id)
                if not unit or decision == "non_rag":
                    continue
                sid = unit.get("source_id")
                for atom_id in mapping.get("atom_ids", []):
                    atom_source_ids[atom_id].add(sid)
                    atom_decisions[atom_id].add(decision)

    nodes = []
    edges = []
    edge_seen = set()

    nodes.append(
        {
            "id": "BB-RAG",
            "type": "backbone",
            "label_zh": "检索增强生成",
            "label_en": "Retrieval-Augmented Generation",
            "status": "source_mapped",
            "reviewed_at": "2026-09-04",
            "source_refs": [source_node_id("rag-original-2020")],
            "summary": "RAG pilot backbone; graph inventory only.",
            "freshness_class": "stable",
        }
    )

    # Cross-backbone nodes are deliberately limited to capabilities that have
    # already been mapped to the RAG inventory and have registered evidence.
    # They identify a bounded overlap for generated views; they do not claim
    # that a product, framework, or every system in either backbone is
    # interchangeable with RAG.
    cross_backbones = [
        {
            "id": "BB-VECTOR-DATABASE",
            "label_zh": "向量数据库",
            "label_en": "Vector Database",
            "source_ids": ["faiss-official-repository-2026", "qdrant-indexing-docs-2026"],
            "summary": "Vector-index and structured-filter capabilities that overlap RAG storage and retrieval.",
            "capabilities": [
                {
                    "id": "CAP-VECTOR-INDEX",
                    "label_zh": "向量索引",
                    "label_en": "Vector Index",
                    "source_ids": ["faiss-official-repository-2026", "qdrant-indexing-docs-2026"],
                },
                {
                    "id": "CAP-METADATA-FILTERING",
                    "label_zh": "元数据过滤",
                    "label_en": "Metadata Filtering",
                    "source_ids": ["qdrant-indexing-docs-2026", "azure-document-access-control-2026"],
                },
            ],
        },
        {
            "id": "BB-AGENT",
            "label_zh": "智能体",
            "label_en": "Agent",
            "source_ids": ["agentic-rag-survey-2025", "azure-ai-search-rag-overview-2026"],
            "summary": "Planning, tool use, and iterative workflow capabilities that overlap Agentic RAG.",
            "capabilities": [
                {
                    "id": "CAP-AGENTIC-PLANNING",
                    "label_zh": "智能体规划",
                    "label_en": "Agentic Planning",
                    "source_ids": ["agentic-rag-survey-2025", "azure-ai-search-rag-overview-2026"],
                },
                {
                    "id": "CAP-TOOL-USE",
                    "label_zh": "工具使用",
                    "label_en": "Tool Use",
                    "source_ids": ["agentic-rag-survey-2025"],
                },
            ],
        },
        {
            "id": "BB-PROMPT-ENGINEERING",
            "label_zh": "提示工程",
            "label_en": "Prompt Engineering",
            "source_ids": ["step-back-prompting-2024"],
            "summary": "Prompt transformations and prompt-context assembly that overlap RAG query and answer paths.",
            "capabilities": [
                {
                    "id": "CAP-PROMPT-ABSTRACTION",
                    "label_zh": "提示抽象",
                    "label_en": "Prompt Abstraction",
                    "source_ids": ["step-back-prompting-2024"],
                },
                {
                    "id": "CAP-PROMPT-CONTEXT-ASSEMBLY",
                    "label_zh": "提示上下文组装",
                    "label_en": "Prompt Context Assembly",
                    "source_ids": ["user-rag-experience-pdf"],
                },
            ],
        },
        {
            "id": "BB-KNOWLEDGE-GRAPH",
            "label_zh": "知识图谱",
            "label_en": "Knowledge Graph",
            "source_ids": ["microsoft-graphrag-docs", "graphrag-local-global-2024"],
            "summary": "Graph indexing and graph retrieval capabilities that overlap GraphRAG workflows.",
            "capabilities": [
                {
                    "id": "CAP-GRAPH-INDEXING",
                    "label_zh": "图索引",
                    "label_en": "Graph Indexing",
                    "source_ids": ["microsoft-graphrag-docs", "graphrag-local-global-2024"],
                },
                {
                    "id": "CAP-GRAPH-RETRIEVAL",
                    "label_zh": "图检索",
                    "label_en": "Graph Retrieval",
                    "source_ids": ["microsoft-graphrag-docs", "graphrag-local-global-2024"],
                },
            ],
        },
    ]
    for backbone in cross_backbones:
        refs = [source_node_id(source_id) for source_id in backbone["source_ids"]]
        nodes.append(
            {
                "id": backbone["id"],
                "type": "backbone",
                "label_zh": backbone["label_zh"],
                "label_en": backbone["label_en"],
                "status": "source_mapped",
                "reviewed_at": "2026-09-04",
                "source_refs": refs,
                "summary": backbone["summary"],
                "freshness_class": "mixed",
                "tags": ["cross_backbone_inventory"],
            }
        )
        for ref in refs:
            add_edge(edges, edge_seen, "supported_by", backbone["id"], ref, "Registered verified evidence supports this bounded cross-backbone inventory entry.", refs)
        for capability in backbone["capabilities"]:
            capability_refs = [source_node_id(source_id) for source_id in capability["source_ids"]]
            nodes.append(
                {
                    "id": capability["id"],
                    "type": "capability",
                    "label_zh": capability["label_zh"],
                    "label_en": capability["label_en"],
                    "status": "source_mapped",
                    "reviewed_at": "2026-09-04",
                    "source_refs": capability_refs,
                    "freshness_class": "mixed",
                    "tags": ["cross_backbone_inventory"],
                }
            )
            add_edge(edges, edge_seen, "contains", backbone["id"], capability["id"], "Registered evidence supports this capability as part of the bounded backbone inventory.", capability_refs)
            for ref in capability_refs:
                add_edge(edges, edge_seen, "supported_by", capability["id"], ref, "Registered verified evidence supports this bounded cross-backbone capability.", capability_refs)

    # These are explicit, bounded intersections with the RAG workflow.  The
    # edge source is the evidence that names the capability or workflow; an
    # overlap is not an assertion that the two systems are equivalent.
    overlap_defs = [
        ("PS-STORAGE-INDEXING", "BB-VECTOR-DATABASE", ["faiss-official-repository-2026", "qdrant-indexing-docs-2026"], "Vector indexes and filtering are shared concerns of RAG storage and vector databases."),
        ("CAP-VECTOR-INDEX", "PS-STORAGE-INDEXING", ["faiss-official-repository-2026", "qdrant-indexing-docs-2026"], "The vector-index capability is used at the RAG storage and indexing stage."),
        ("CAP-METADATA-FILTERING", "PS-RETRIEVAL", ["qdrant-indexing-docs-2026", "azure-document-access-control-2026"], "Metadata and access filtering constrain RAG retrieval candidates."),
        ("BB-AGENT", "PS-ADVANCED-RAG", ["agentic-rag-survey-2025", "azure-ai-search-rag-overview-2026"], "Agent planning and iterative control overlap the Agentic RAG stage."),
        ("CAP-AGENTIC-PLANNING", "PS-QUERY-ROUTING", ["agentic-rag-survey-2025", "azure-ai-search-rag-overview-2026"], "Agentic planning can select retrieval paths and knowledge sources."),
        ("CAP-TOOL-USE", "PS-QUERY-ROUTING", ["agentic-rag-survey-2025"], "Tool use overlaps query routing when an agent selects external retrieval or action tools."),
        ("BB-PROMPT-ENGINEERING", "PS-QUERY-REWRITE", ["step-back-prompting-2024"], "Prompt transformations overlap query rewriting before retrieval."),
        ("CAP-PROMPT-ABSTRACTION", "PS-QUERY-REWRITE", ["step-back-prompting-2024"], "Step-back prompt abstraction is a query-rewrite technique with an explicit original-query boundary."),
        ("CAP-PROMPT-CONTEXT-ASSEMBLY", "PS-CONTEXT-ASSEMBLY", ["user-rag-experience-pdf"], "Prompt assembly combines the query, evidence and generation instructions at context assembly."),
        ("BB-KNOWLEDGE-GRAPH", "PS-RETRIEVAL", ["microsoft-graphrag-docs", "graphrag-local-global-2024"], "Graph retrieval is an alternative retrieval representation for entity-connection questions."),
        ("CAP-GRAPH-INDEXING", "PS-STORAGE-INDEXING", ["microsoft-graphrag-docs", "graphrag-local-global-2024"], "Graph indexing is an additional index-building concern alongside RAG storage and indexing."),
        ("CAP-GRAPH-RETRIEVAL", "PS-RETRIEVAL", ["microsoft-graphrag-docs", "graphrag-local-global-2024"], "Graph retrieval overlaps the RAG retrieval stage for graph-oriented queries."),
    ]
    for left, right, source_ids, explanation in overlap_defs:
        refs = [source_node_id(source_id) for source_id in source_ids]
        add_edge(edges, edge_seen, "overlaps_with", left, right, explanation, refs)

    branch_defs = [
        ("PS-QUERY-ROUTING", "BB-AGENT", ["azure-ai-search-rag-overview-2026"], "Agentic retrieval is a conditional query-planning branch from RAG query routing; the registered source distinguishes it from classic RAG."),
        ("PS-RETRIEVAL", "BB-KNOWLEDGE-GRAPH", ["microsoft-graphrag-docs", "graphrag-local-global-2024"], "GraphRAG search is a conditional retrieval branch for questions requiring entity connections; its quality and cost remain workload-specific."),
    ]
    for left, right, source_ids, explanation in branch_defs:
        refs = [source_node_id(source_id) for source_id in source_ids]
        add_edge(edges, edge_seen, "branches_to", left, right, explanation, refs)

    stages = [
        ("PS-DATA-INGESTION", "数据摄取", "Data Ingestion"),
        ("PS-DOCUMENT-PARSING", "文档解析", "Document Parsing"),
        ("PS-DATA-GOVERNANCE", "数据治理", "Data Governance"),
        ("PS-CHUNKING", "文本切分", "Chunking"),
        ("PS-EMBEDDING", "向量嵌入", "Embedding"),
        ("PS-STORAGE-INDEXING", "存储与索引", "Storage and Indexing"),
        ("PS-QUERY-UNDERSTANDING", "查询理解", "Query Understanding"),
        ("PS-QUERY-REWRITE", "查询改写", "Query Rewrite"),
        ("PS-QUERY-ROUTING", "查询路由", "Query Routing"),
        ("PS-RETRIEVAL", "检索", "Retrieval"),
        ("PS-RESULT-FUSION", "结果融合", "Result Fusion"),
        ("PS-RERANKING", "重排", "Reranking"),
        ("PS-CONTEXT-ASSEMBLY", "上下文组装", "Context Assembly"),
        ("PS-ANSWER-GENERATION", "答案生成", "Answer Generation"),
        ("PS-CITATION-VERIFICATION", "引用与验证", "Citation and Verification"),
        ("PS-EVALUATION", "评估", "Evaluation"),
        ("PS-PRODUCTION-GOVERNANCE", "生产治理", "Production Governance"),
        ("PS-ADVANCED-RAG", "高级检索增强生成", "Advanced RAG"),
    ]
    for index, (sid, zh, en) in enumerate(stages):
        refs = [source_node_id("rag-original-2020")]
        nodes.append(
            {
                "id": sid,
                "type": "pipeline_stage",
                "label_zh": zh,
                "label_en": en,
                "status": "source_mapped",
                "reviewed_at": "2026-09-04",
                "source_refs": refs,
                "domain_ids": ["RAG"],
            }
        )
        add_edge(edges, edge_seen, "contains", "BB-RAG", sid, "RAG backbone stage inventory.", refs)
        if index:
            add_edge(edges, edge_seen, "next_stage", stages[index - 1][0], sid, "Fixed RAG stage order from the execution roadmap.", refs)

    atom_labels = {}
    for section in catalog["sections"]:
        for atom in section["atoms"]:
            atom_labels[atom["id"]] = (section["id"], section["title"], atom["title"])
            refs = {source_node_id(sid) for sid in atom_source_ids.get(atom["id"], set()) if sid}
            refs.update(source_node_id(sid) for sid, atoms in evidence_atom_refs.items() if atom["id"] in atoms)
            refs = sorted(refs)
            status = "source_mapped" if refs else "inventory_draft"
            nodes.append(
                {
                    "id": atom["id"],
                    "type": "knowledge",
                    "label_zh": atom["title"],
                    "label_en": f"RAG knowledge atom {atom['id']}",
                    "status": status,
                    "reviewed_at": "2026-09-04" if refs else None,
                    "source_refs": refs,
                    "module_ids": [section["id"]],
                    "freshness_class": "mixed",
                    "tags": sorted(atom_decisions.get(atom["id"], set())),
                }
            )
            for ref in refs:
                add_edge(edges, edge_seen, "supported_by", atom["id"], ref, "Accepted manual mapping or verified evidence supports atom coverage; detailed claim boundaries remain source-specific.", refs)

    source_ids = sorted(source_meta)
    for sid in source_ids:
        meta = source_meta[sid]
        is_verified = sid in evidence_status and sid not in waived_ids
        status = "fact_checked" if is_verified else "source_mapped"
        node = {
            "id": source_node_id(sid),
            "type": "source",
            "label_zh": meta.get("name", sid),
            "label_en": sid,
            "status": status,
            "reviewed_at": "2026-09-04" if is_verified else None,
            "source_refs": [],
            "source_locator": meta.get("url") or meta.get("repository") or meta.get("artifact_name"),
            "freshness_class": meta.get("freshness") or meta.get("evidence_quality") or "stable",
            "tags": [],
        }
        if sid in waived_ids:
            node["tags"] = ["waived_unavailable", "non_evidentiary"]
        if sid in verification_by_source:
            node["verification_records"] = sorted(set(verification_by_source[sid]))
        nodes.append(node)

    url_to_source = {}
    repository_prefixes = []
    for sid, meta in source_meta.items():
        for key in (meta.get("url"), meta.get("repository")):
            if key:
                url_to_source[key] = sid
        repository = meta.get("repository") or meta.get("url")
        if repository and "github.com/" in repository:
            repository_prefixes.append((repository.rstrip("/") + "/", sid))

    def source_for_scenario_url(url: str | None) -> str | None:
        if not url:
            return None
        if source_id := url_to_source.get(url):
            return source_id
        # Public question inventories can locate a pinned file below a
        # registered GitHub repository root. The repository identity remains
        # the registered source; this only normalizes the locator form.
        for prefix, source_id in repository_prefixes:
            if url.startswith(prefix):
                return source_id
        return None

    solution_defs = [
        ("SOL-RAG-0001", "增量与版本化索引更新", "Incremental and Versioned Index Updates", ["RAG-SCENE-008", "RAG-SCENE-009", "RAG-SCENE-013", "RAG-SCENE-022"], ["azure-indexer-change-delete-detection-2026", "qdrant-incremental-embedding-updates-2026", "qdrant-blue-green-deployment-2026"]),
        ("SOL-RAG-0002", "混合检索与排名融合", "Hybrid Retrieval and Rank Fusion", ["RAG-SCENE-017", "RAG-SCENE-018", "RAG-SCENE-019"], ["azure-hybrid-rrf-ranking-2026", "elasticsearch-rrf-retriever-docs-2026", "reciprocal-rank-fusion-2009"]),
        ("SOL-RAG-0003", "结构感知与父子上下文切分", "Structure-aware and Parent-child Chunking", ["RAG-SCENE-002", "RAG-SCENE-007", "RAG-SCENE-010", "RAG-SCENE-011"], ["unstructured-chunking-docs-2026", "langchain-parent-document-retriever-2026", "llamaindex-sentence-window-docs-2026"]),
        ("SOL-RAG-0004", "分层评估与回归诊断", "Layered Evaluation and Regression Diagnosis", ["RAG-SCENE-001", "RAG-SCENE-003", "RAG-SCENE-006", "RAG-SCENE-021", "RAG-SCENE-025"], ["nowcoder-rag-evaluation-funnel-2026", "ragas-eacl-2024", "ragchecker-2024"]),
        ("SOL-RAG-0005", "权限过滤与多租户隔离", "Access Filtering and Tenant Isolation", ["RAG-SCENE-002", "RAG-SCENE-008", "RAG-SCENE-022", "RAG-SCENE-026"], ["azure-document-access-control-2026", "mcp-authorization-security-2026", "owasp-rag-security-cheat-sheet-2026"]),
        ("SOL-RAG-0006", "自适应与迭代检索路由", "Adaptive and Iterative Retrieval Routing", ["RAG-SCENE-015", "RAG-SCENE-016", "RAG-SCENE-023"], ["adaptive-rag-2024", "iterative-rag-diagnostic-2026", "azure-semantic-query-rewrite-2026"]),
    ]
    impl_defs = [
        ("IMP-RAG-0001", "VectorRAG 与 FAISS 链路", "VectorRAG and FAISS Pipeline", ["RAG-SCENE-004", "RAG-SCENE-005"], ["faiss-official-repository-2026", "hebutbryant-rag-interview"]),
        ("IMP-RAG-0002", "LangChain MultiQueryRetriever", "LangChain MultiQueryRetriever", ["RAG-SCENE-015", "RAG-SCENE-017"], ["langchain-multi-query-retriever-2026"]),
        ("IMP-RAG-0003", "LlamaIndex QueryFusionRetriever", "LlamaIndex QueryFusionRetriever", ["RAG-SCENE-018", "RAG-SCENE-019"], ["llamaindex-query-fusion-retriever-2026"]),
        ("IMP-RAG-0004", "Unstructured 解析与切分策略", "Unstructured Partitioning and Chunking", ["RAG-SCENE-002", "RAG-SCENE-007", "RAG-SCENE-011"], ["unstructured-partitioning-docs-2026", "unstructured-chunking-docs-2026"]),
        ("IMP-RAG-0005", "Qdrant/Azure 索引更新与迁移", "Qdrant/Azure Index Updates and Migration", ["RAG-SCENE-008", "RAG-SCENE-009", "RAG-SCENE-013", "RAG-SCENE-022"], ["qdrant-incremental-embedding-updates-2026", "qdrant-blue-green-deployment-2026", "azure-indexer-change-delete-detection-2026"]),
        ("IMP-RAG-0006", "非对称 Embedding 与 Rerank API", "Asymmetric Embedding and Rerank APIs", ["RAG-SCENE-012", "RAG-SCENE-019"], ["cohere-embedding-docs-2026", "cohere-rerank-api-v2-2026"]),
    ]
    eval_defs = [
        ("EVAL-RAG-LAYERED", "分层 RAG 评估", "Layered RAG Evaluation", ["RAG-SCENE-001", "RAG-SCENE-006", "RAG-SCENE-021", "RAG-SCENE-025"], ["ragas-eacl-2024", "ragchecker-2024", "nowcoder-rag-evaluation-funnel-2026"]),
        ("EVAL-RAG-RETRIEVAL", "检索排序与召回评估", "Retrieval and Ranking Evaluation", ["RAG-SCENE-003", "RAG-SCENE-018", "RAG-SCENE-019"], ["vibe-vector-index-benchmark-2026", "bm25-foundations-2009", "reciprocal-rank-fusion-2009"]),
        ("EVAL-RAG-CITATION", "引用准确性与完整性评估", "Citation Accuracy and Completeness", ["RAG-SCENE-001", "RAG-SCENE-002", "RAG-SCENE-003", "RAG-SCENE-024"], ["anthropic-citations-docs-2026", "google-check-grounding-docs-2026", "alce-citation-evaluation-2023"]),
    ]
    scenario_by_id = {item["id"]: item for item in scenarios}
    for node_id, zh, en, scenario_ids, source_list in solution_defs + impl_defs + eval_defs:
        refs = [source_node_id(sid) for sid in source_list if sid in source_meta and sid not in waived_ids]
        node_type = "solution" if node_id.startswith("SOL-") else "implementation" if node_id.startswith("IMP-") else "evaluation"
        nodes.append({"id": node_id, "type": node_type, "label_zh": zh, "label_en": en, "status": "source_mapped" if refs else "inventory_draft", "reviewed_at": "2026-09-04" if refs else None, "source_refs": sorted(set(refs)), "tags": ["derived_inventory", "preserve_conditions"]})
        for ref in refs:
            add_edge(edges, edge_seen, "supported_by", node_id, ref, "Candidate node derived from verified evidence and public scenario mappings; not final prose.", refs)

    for scenario in scenarios:
        sid = scenario["id"]
        source_id = source_for_scenario_url(scenario.get("source_url"))
        refs = [source_node_id(source_id)] if source_id else []
        scenario_source_type = scenario["source_type"]
        provenance_type = (
            "engineering_case"
            if scenario_source_type == "engineering_practice"
            else scenario_source_type
        )
        tags = ["public_scenario_inventory"]
        if scenario_source_type != provenance_type:
            # The scenario inventory has a more specific source category than
            # the graph model. Preserve it without publishing an unregistered
            # problem provenance type.
            tags.append(f"scenario_source_type:{scenario_source_type}")
        nodes.append({"id": f"PQ-RAG-{int(sid.rsplit('-', 1)[1]):04d}", "type": "problem_question", "label_zh": scenario["question_summary"], "label_en": f"RAG engineering problem {sid}", "status": "source_mapped" if refs else "inventory_draft", "reviewed_at": "2026-09-04" if refs else None, "source_refs": refs, "provenance_type": provenance_type, "source_locator": scenario["source_locator"], "knowledge_node_ids": scenario["atom_ids"], "tags": tags})
        problem_id = f"PQ-RAG-{int(sid.rsplit('-', 1)[1]):04d}"
        for atom_id in scenario["atom_ids"]:
            add_edge(edges, edge_seen, "problem_at", problem_id, atom_id, "Scenario is explicitly mapped to this canonical knowledge atom.", refs)
        for ref in refs:
            add_edge(edges, edge_seen, "supported_by", problem_id, ref, "Public scenario source supports question provenance only; it is not technical evidence.", refs)

    scenario_atoms = {
        scenario_id: set(scenario_by_id[scenario_id].get("atom_ids", []))
        for scenario_id in scenario_by_id
    }

    definition_refs = {
        node_id: sorted(
            source_node_id(source_id)
            for source_id in source_list
            if source_id in source_meta and source_id not in waived_ids
        )
        for node_id, _zh, _en, _scenario_ids, source_list
        in solution_defs + impl_defs + eval_defs
    }

    def connect_defs(defs, edge_kind):
        for node_id, _zh, _en, scenario_ids, _source_list in defs:
            refs = definition_refs[node_id]
            for scenario_id in scenario_ids:
                problem_id = f"PQ-RAG-{int(scenario_id.rsplit('-', 1)[1]):04d}"
                if problem_id not in {n["id"] for n in nodes}:
                    continue
                if edge_kind == "solved_by":
                    add_edge(edges, edge_seen, edge_kind, problem_id, node_id, "Registered technical sources support this candidate solution branch; the public scenario only supplies its problem context, and business conditions remain preserved.", refs)
                elif edge_kind == "implemented_by":
                    # Implementations are linked to the knowledge they realize. The
                    # problem association remains represented by problem_at edges.
                    for atom_id in sorted(scenario_atoms.get(scenario_id, set())):
                        add_edge(edges, edge_seen, "implements", node_id, atom_id, "Implementation candidate realizes knowledge required by the mapped scenario.", refs)
                else:
                    add_edge(edges, edge_seen, edge_kind, problem_id, node_id, "Registered technical sources support this candidate evaluation method; the public scenario only supplies its problem context.", refs)

    connect_defs(solution_defs, "solved_by")
    connect_defs(impl_defs, "implemented_by")
    connect_defs(eval_defs, "evaluated_by")

    # Preserve solution-to-implementation relationships with the direction
    # defined by the graph model. Shared scenarios are the conservative join
    # key; no equivalence beyond that overlap is inferred.
    solution_scenarios = {node_id: set(scenario_ids) for node_id, _zh, _en, scenario_ids, _refs in solution_defs}
    implementation_scenarios = {node_id: set(scenario_ids) for node_id, _zh, _en, scenario_ids, _refs in impl_defs}
    for solution_id, solution_ids in solution_scenarios.items():
        for implementation_id, implementation_ids in implementation_scenarios.items():
            if solution_ids & implementation_ids:
                refs = sorted(
                    set(definition_refs[solution_id])
                    | set(definition_refs[implementation_id])
                )
                add_edge(edges, edge_seen, "implemented_by", solution_id, implementation_id, "Registered technical sources support the candidate implementation relationship; shared scenarios preserve its contextual boundary.", refs)

    # Catalog modules are an existing organizational boundary, not a new
    # technical claim. Add the corresponding stage membership so source-less
    # inventory atoms remain structurally reachable while their evidence gaps
    # continue to be reported separately.
    module_stages = {
        "RAG-01": ["BB-RAG"],
        "RAG-02": ["BB-RAG"],
        "RAG-03": ["PS-DOCUMENT-PARSING", "PS-DATA-GOVERNANCE"],
        "RAG-04": ["PS-CHUNKING"],
        "RAG-05": ["PS-EMBEDDING"],
        "RAG-06": ["PS-STORAGE-INDEXING"],
        "RAG-07": ["PS-QUERY-UNDERSTANDING"],
        "RAG-08": ["PS-RETRIEVAL", "PS-RESULT-FUSION", "PS-RERANKING"],
        "RAG-09": ["PS-CONTEXT-ASSEMBLY", "PS-ANSWER-GENERATION", "PS-CITATION-VERIFICATION"],
        "RAG-10": ["PS-EVALUATION"],
        "RAG-11": ["PS-PRODUCTION-GOVERNANCE"],
        "RAG-12": ["PS-ADVANCED-RAG"],
        "RAG-13": ["BB-RAG"],
    }
    for node in nodes:
        if node["type"] != "knowledge":
            continue
        for stage_id in module_stages[node["module_ids"][0]]:
            add_edge(
                edges,
                edge_seen,
                "contains",
                stage_id,
                node["id"],
                "Catalog module membership for graph navigation; it does not add an independent technical conclusion.",
                node["source_refs"],
                status="inventory_draft",
            )

    nodes.sort(key=lambda item: item["id"])
    edges.sort(key=lambda item: item["id"])
    graph = {
        "schema_version": 1,
        "generated_at": "2026-09-04",
        "domain": "RAG",
        "status": "inventory_draft",
        "phase": "P3-canonical-knowledge-graph",
        "scope": "WP-P3 canonical node consolidation with bounded cross-backbone inventory; no new external search; no final chapters",
        "source_policy": "Only accepted manual mappings, registered sources, verified evidence batches, and the public scenario inventory are used.",
        "waived_sources": sorted(waived_ids),
        "nodes": nodes,
        "edges": edges,
    }
    dump("knowledge/rag/graph.json", graph)

    counts = defaultdict(int)
    for node in nodes:
        counts[f"nodes_{node['type']}"] += 1
    edge_counts = defaultdict(int)
    for edge in edges:
        edge_counts[f"edges_{edge['type']}"] += 1
    covered_atoms = sum(1 for atom_id in atom_labels if any(node["id"] == atom_id and node["source_refs"] for node in nodes))
    audit = {
        "schema_version": 1,
        "work_item_id": "WP-P3-001",
        "generated_at": "2026-09-04",
        "status": "completed_inventory_draft",
        "inputs": ["knowledge/rag/catalog.json", "audits/rag/accepted-mappings.json", "audits/rag/reviewed/*.json", "audits/rag/evidence/*.json", "sources/registry.json", "sources/rag-current-sources.json", "interview/rag/public-scenarios.json"],
        "counts": {**dict(counts), **dict(edge_counts), "catalog_atoms": len(atom_labels), "atoms_with_source_refs": covered_atoms, "registered_sources": len(source_ids), "waived_sources_excluded_from_evidence": len(waived_ids), "public_problem_scenarios": len(scenarios)},
        "deduplication_rule": "Only exact semantic, condition, and conclusion equivalence may be removed; implementation, constraints, counterexamples, conflicts, versions, and business conditions remain represented through source links, tags, and separate candidate nodes.",
        "limitations": ["Knowledge labels are catalog labels; final four-part chapters are intentionally not generated.", "Candidate solution, implementation, and evaluation nodes are inventory-level and remain source_mapped until WP-P3-002/P3-003 audits.", "The waived EUR-Lex source is retained only as a non-evidentiary source record and does not support any node."],
        "next_work_item": "WP-P4-002",
    }
    dump("audits/rag/canonical-consolidation.json", audit)


if __name__ == "__main__":
    main()

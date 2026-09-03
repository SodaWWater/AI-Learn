#!/usr/bin/env python3
"""Validate AI-Learn's machine-readable indexes and publication gates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "README.md",
    "docs/PROJECT_PLAN.md",
    "sources/registry.json",
    "sources/rag-scope.json",
    "sources/rag-current-sources.json",
    "taxonomy/domains.json",
    "taxonomy/rag-topics.json",
    "knowledge/rag/README.md",
    "knowledge/rag/CONTENT_STANDARD.md",
    "knowledge/rag/TERMINOLOGY.md",
    "knowledge/rag/catalog.json",
    "knowledge/rag/catalog.md",
    "learning/rag/draft-overview.md",
    "learning/rag/overview.md",
    "learning/rag/formal-status.json",
    "taxonomy/rag-graph-model.json",
    "taxonomy/rag-terminology.json",
    "audits/rag/work-status.json",
    "docs/LOCAL_AGENT_HANDOFF.md",
    "docs/RAG_EXECUTION_ROADMAP.md",
    "audits/rag/manual-review-status.json",
    "audits/rag/original-source-coverage.md",
    "sources/rag-search-matrix.json",
    "audits/rag/search-coverage.json",
    "interview/rag/public-scenarios.json",
    "audits/rag/source-units.json",
    "audits/rag/atom-suggestions.json",
    "audits/rag/accepted-mappings.json",
    "audits/rag/acceptance.md",
    "templates/knowledge-note.md",
    "templates/problem-question.md",
    "templates/source-search-log.md",
    "templates/source-review-batch.json",
    "scripts/review_queue.py",
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
    formal_status = load_json("learning/rag/formal-status.json", errors)
    graph_model = load_json("taxonomy/rag-graph-model.json", errors)
    terminology = load_json("taxonomy/rag-terminology.json", errors)
    work_status = load_json("audits/rag/work-status.json", errors)
    current_sources = load_json("sources/rag-current-sources.json", errors)
    search_matrix = load_json("sources/rag-search-matrix.json", errors)
    search_coverage = load_json("audits/rag/search-coverage.json", errors)
    manual_review = load_json("audits/rag/manual-review-status.json", errors)

    sources = registry.get("sources", [])
    source_ids = [item.get("id", "") for item in sources]
    if repeated := duplicates(source_ids):
        errors.append(f"来源 ID 重复：{repeated}")
    for source in sources:
        if source.get("source_type") == "user_provided_pdf":
            if not re.fullmatch(r"[0-9a-f]{64}", source.get("sha256", "")):
                errors.append(f"来源 {source.get('id')} 的 SHA-256 不是 64 位")
        elif not re.fullmatch(r"[0-9a-f]{40}", source.get("commit", "")):
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

    graph_node_type_ids = [
        item.get("id", "") for item in graph_model.get("node_types", [])
    ]
    graph_edge_type_ids = [
        item.get("id", "") for item in graph_model.get("edge_types", [])
    ]
    if repeated := duplicates(graph_node_type_ids):
        errors.append(f"知识图谱节点类型重复：{repeated}")
    if repeated := duplicates(graph_edge_type_ids):
        errors.append(f"知识图谱关系类型重复：{repeated}")
    required_graph_nodes = {
        "backbone", "pipeline_stage", "knowledge", "problem_question",
        "solution", "implementation", "evaluation", "source",
    }
    if missing := required_graph_nodes - set(graph_node_type_ids):
        errors.append(f"知识图谱缺少核心节点类型：{sorted(missing)}")
    required_graph_edges = {
        "contains", "branches_to", "merges_into", "overlaps_with",
        "problem_at", "solved_by", "implemented_by", "evaluated_by",
        "supported_by",
    }
    if missing := required_graph_edges - set(graph_edge_type_ids):
        errors.append(f"知识图谱缺少核心关系类型：{sorted(missing)}")

    term_items = terminology.get("terms", [])
    term_ids = [item.get("id", "") for item in term_items]
    term_displays = [item.get("display", "") for item in term_items]
    if terminology.get("term_count") != len(term_items):
        errors.append("rag-terminology.json 的 term_count 与实际数组长度不一致")
    if len(term_items) < 100:
        errors.append("RAG 机器术语表少于 100 条，可能没有从 Markdown 完整生成")
    if repeated := duplicates(term_ids):
        errors.append(f"术语 ID 重复：{repeated[:10]}")
    if repeated := duplicates(term_displays):
        errors.append(f"术语规范表达重复：{repeated[:10]}")
    for term in term_items:
        if not term.get("label_zh") or not term.get("label_en"):
            errors.append(f"术语缺少中英文名称：{term.get('id')}")

    phase_ids = [item.get("id", "") for item in work_status.get("phases", [])]
    work_item_ids = [
        item.get("id", "") for item in work_status.get("work_items", [])
    ]
    if repeated := duplicates(phase_ids):
        errors.append(f"项目阶段 ID 重复：{repeated}")
    if repeated := duplicates(work_item_ids):
        errors.append(f"工作项 ID 重复：{repeated}")
    next_work_item = work_status.get("next_action", {}).get("work_item_id")
    if next_work_item not in work_item_ids:
        errors.append(f"下一工作项不存在：{next_work_item}")
    for item in work_status.get("work_items", []):
        for dependency in item.get("depends_on", []):
            if dependency not in work_item_ids:
                errors.append(
                    f"工作项 {item.get('id')} 依赖未知工作项：{dependency}"
                )

    manual_counts = manual_review.get("counts", {})
    if manual_counts.get("all_source_units") != 695:
        errors.append("人工审核状态的来源单元总数必须为 695")
    if manual_counts.get("semantic_units") != 653:
        errors.append("人工审核状态的语义单元总数必须为 653")
    reviewed_semantic = manual_counts.get("manually_reviewed_semantic_units", 0)
    pending_semantic = manual_counts.get("pending_manual_semantic_units", 0)
    if reviewed_semantic + pending_semantic != 653:
        errors.append("人工审核状态的已审核与待审核数量之和必须为 653")
    allowed_review_decisions = {
        "retain", "exact_duplicate", "partial_overlap", "cross_node", "non_rag",
    }
    if set(manual_review.get("decision_types", [])) != allowed_review_decisions:
        errors.append("人工审核状态的判断类型与项目规范不一致")
    if manual_review.get("external_search", {}).get("status") != (
        "paused_by_user_after_three_complete_rounds"
    ):
        errors.append("当前外部搜索必须保持用户决定的暂停状态")

    expected_stage_ids = [
        "PS-DATA-INGESTION",
        "PS-DOCUMENT-PARSING",
        "PS-DATA-GOVERNANCE",
        "PS-CHUNKING",
        "PS-EMBEDDING",
        "PS-STORAGE-INDEXING",
        "PS-QUERY-UNDERSTANDING",
        "PS-QUERY-REWRITE",
        "PS-QUERY-ROUTING",
        "PS-RETRIEVAL",
        "PS-RESULT-FUSION",
        "PS-RERANKING",
        "PS-CONTEXT-ASSEMBLY",
        "PS-ANSWER-GENERATION",
        "PS-CITATION-VERIFICATION",
        "PS-EVALUATION",
        "PS-PRODUCTION-GOVERNANCE",
        "PS-ADVANCED-RAG",
    ]
    search_stages = search_matrix.get("stages", [])
    matrix_stage_ids = [item.get("id", "") for item in search_stages]
    if matrix_stage_ids != expected_stage_ids:
        errors.append("RAG 检索矩阵必须按规划顺序完整覆盖 18 个流程节点")
    required_stage_fields = {
        "order", "id", "label_zh", "label_en", "track",
        "query_terms_zh", "query_terms_en", "problem_terms_zh",
        "problem_terms_en", "cross_stage_targets",
    }
    for index, stage in enumerate(search_stages, 1):
        if missing := required_stage_fields - set(stage):
            errors.append(f"检索矩阵节点 {stage.get('id')} 缺少字段：{sorted(missing)}")
        if stage.get("order") != index:
            errors.append(f"检索矩阵节点顺序错误：{stage.get('id')}")
        for target in stage.get("cross_stage_targets", []):
            if target not in expected_stage_ids:
                errors.append(f"检索矩阵节点 {stage.get('id')} 引用了未知关联节点：{target}")
    search_family_ids = [
        item.get("id", "") for item in search_matrix.get("search_families", [])
    ]
    required_search_families = {
        "concept_and_principle", "engineering_problem", "implementation",
        "evaluation", "public_interview", "freshness_and_security",
    }
    if missing := required_search_families - set(search_family_ids):
        errors.append(f"RAG 检索矩阵缺少检索族：{sorted(missing)}")

    coverage_stages = search_coverage.get("stages", [])
    coverage_stage_ids = [item.get("stage_id", "") for item in coverage_stages]
    if coverage_stage_ids != expected_stage_ids:
        errors.append("RAG 检索覆盖记录未与 18 个流程节点一一对应")
    allowed_search_statuses = {
        "not_started", "searching", "round_complete", "coverage_saturated",
    }
    for stage in coverage_stages:
        if stage.get("status") not in allowed_search_statuses:
            errors.append(f"检索覆盖状态无效：{stage.get('stage_id')}")
        if stage.get("completed_rounds", 0) < 0:
            errors.append(f"检索轮数不能为负数：{stage.get('stage_id')}")
        if stage.get("status") == "coverage_saturated":
            if stage.get("completed_rounds", 0) < 2:
                errors.append(f"检索覆盖过早标记饱和：{stage.get('stage_id')}")
            if stage.get("consecutive_rounds_without_new_type", 0) < 2:
                errors.append(f"检索覆盖缺少连续两轮无新增证据：{stage.get('stage_id')}")
        for rel_path in stage.get("log_paths", []):
            if not (ROOT / rel_path).is_file():
                errors.append(f"检索覆盖引用了不存在的日志：{rel_path}")

    current_source_items = current_sources.get("sources", [])
    current_source_ids = [item.get("id", "") for item in current_source_items]
    if repeated := duplicates(current_source_ids):
        errors.append(f"RAG 当前来源 ID 重复：{repeated}")
    allowed_current_source_types = {
        "paper", "official_documentation", "official_repository",
        "official_engineering_report", "first_person_interview",
        "public_question_bank", "project_interview_exercise",
        "engineering_practice", "secondary_index",
    }
    for source in current_source_items:
        source_id = source.get("id")
        if source.get("type") not in allowed_current_source_types:
            errors.append(f"RAG 当前来源类型无效：{source_id}")
        if not str(source.get("url", "")).startswith("https://"):
            errors.append(f"RAG 当前来源缺少 HTTPS 链接：{source_id}")
        if not source.get("version") or not source.get("freshness"):
            errors.append(f"RAG 当前来源缺少版本或时效等级：{source_id}")
        if not source.get("use_for"):
            errors.append(f"RAG 当前来源缺少纳管范围：{source_id}")
        for stage_id in source.get("stage_ids", []):
            if stage_id not in expected_stage_ids:
                errors.append(f"RAG 当前来源 {source_id} 引用了未知流程节点：{stage_id}")

    expansion = work_status.get("research_expansion", {})
    if expansion.get("current_sources") != len(current_source_items):
        errors.append("工作状态中的 RAG 当前来源数与来源登记不一致")
    if expansion.get("search_stages_total") != len(expected_stage_ids):
        errors.append("工作状态中的检索节点总数与检索矩阵不一致")
    round_one_complete = sum(
        item.get("completed_rounds", 0) >= 1 for item in coverage_stages
    )
    if expansion.get("search_stages_round_1_complete") != round_one_complete:
        errors.append("工作状态中的第一轮完成节点数与覆盖记录不一致")
    saturated_count = sum(
        item.get("status") == "coverage_saturated" for item in coverage_stages
    )
    if expansion.get("coverage_saturated_stages") != saturated_count:
        errors.append("工作状态中的覆盖饱和节点数与覆盖记录不一致")

    search_log_template = (ROOT / "templates/source-search-log.md").read_text(
        encoding="utf-8"
    )
    required_search_log_headings = [
        "## 2. 实际检索式",
        "## 3. 候选来源和取舍",
        "## 4. 本轮新增类型",
        "## 5. 公开面试题来源核验",
        "## 6. 九类覆盖检查",
        "## 8. 饱和判定",
    ]
    for heading in required_search_log_headings:
        if heading not in search_log_template:
            errors.append(f"来源检索日志模板缺少标题：{heading}")

    knowledge_template = (ROOT / "templates/knowledge-note.md").read_text(
        encoding="utf-8"
    )
    required_knowledge_headings = [
        "## 1. 知识点概要",
        "## 2. 技术原理",
        "## 3. 实际开发中的位置和使用方式",
        "## 4. 具体技术或框架实现",
        "## 相关工程问题/面试题",
    ]
    for heading in required_knowledge_headings:
        if heading not in knowledge_template:
            errors.append(f"知识模板缺少标题：{heading}")
    problem_template = (ROOT / "templates/problem-question.md").read_text(
        encoding="utf-8"
    )
    required_problem_headings = [
        "## 1. 问题或题目",
        "## 4. 关联流程节点",
        "## 5. 根因分支",
        "## 6. 解决方案分支",
        "## 8. 具体技术或框架实现",
        "## 9. 验证方法",
        "## 10. 关联知识章节",
    ]
    for heading in required_problem_headings:
        if heading not in problem_template:
            errors.append(f"问题模板缺少标题：{heading}")

    catalog_atoms_by_section = {
        section.get("id", ""): {
            atom.get("id", "") for atom in section.get("atoms", [])
        }
        for section in catalog_sections
    }
    completed_module_ids: list[str] = []
    for module in formal_status.get("completed_modules", []):
        module_id = module.get("id", "")
        completed_module_ids.append(module_id)
        if module_id not in catalog_atoms_by_section:
            errors.append(f"正式产物登记了未知模块：{module_id}")
            continue
        for artifact_type in ("map", "chapter"):
            rel_path = module.get(artifact_type, "")
            path = ROOT / rel_path
            if not rel_path or not path.is_file():
                errors.append(f"{module_id} 缺少正式 {artifact_type}：{rel_path}")
                continue
            artifact_atom_ids = set(
                re.findall(r"RAG-\d{2}-\d{3}", path.read_text(encoding="utf-8"))
            )
            missing_atoms = catalog_atoms_by_section[module_id] - artifact_atom_ids
            if missing_atoms:
                errors.append(
                    f"{module_id} 正式 {artifact_type} 漏掉知识原子："
                    f"{sorted(missing_atoms)}"
                )
    if repeated := duplicates(completed_module_ids):
        errors.append(f"正式产物模块重复登记：{repeated}")

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
            file_mappings = payload.get("mappings", [])
            batch_meta = payload.get("batch")
            if isinstance(batch_meta, dict) and batch_meta.get("unit_count") is not None:
                actual_unit_count = sum(
                    len(mapping.get("source_unit_ids", [mapping.get("source_unit_id")]))
                    for mapping in file_mappings
                )
                if batch_meta.get("unit_count") != actual_unit_count:
                    errors.append(
                        f"审核批次 {path.name} 的 unit_count 与实际来源单元数不一致"
                    )
                declared_counts = payload.get("decision_counts", {})
                if declared_counts:
                    actual_counts: Counter[str] = Counter()
                    for mapping in file_mappings:
                        actual_counts[mapping.get("decision")] += len(
                            mapping.get("source_unit_ids", [mapping.get("source_unit_id")])
                        )
                    normalized_actual_counts = {
                        key: actual_counts[key] for key in declared_counts
                    }
                    undeclared_nonzero = set(actual_counts) - set(declared_counts)
                    if normalized_actual_counts != declared_counts or undeclared_nonzero:
                        errors.append(f"审核批次 {path.name} 的 decision_counts 不一致")
                if not batch_meta.get("source_body_reviewed"):
                    errors.append(f"审核批次 {path.name} 未确认阅读来源正文")
            accepted_mappings.extend(file_mappings)
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
            allowed_mapping_decisions = {
                "map", "retain", "exact_duplicate", "partial_overlap",
                "cross_node", "non_rag",
            }
            if decision not in allowed_mapping_decisions:
                errors.append(f"人工审核判断类型无效：{decision}，来源单元 {unit_refs[:3]}")
            if decision in {"retain", "partial_overlap", "cross_node"} and not atom_refs:
                errors.append(f"人工 {decision} 决策没有知识原子：{unit_refs[:3]}")
            if decision == "exact_duplicate" and not (
                atom_refs or mapping.get("duplicate_of_atom_ids")
            ):
                errors.append(f"人工 exact_duplicate 决策没有规范知识指向：{unit_refs[:3]}")
            if decision == "non_rag" and not mapping.get("note"):
                errors.append(f"人工 non_rag 决策缺少排除原因：{unit_refs[:3]}")
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

    scenarios = load_json("interview/rag/public-scenarios.json", errors).get("scenarios", [])
    scenario_ids = [item.get("id", "") for item in scenarios]
    if repeated := duplicates(scenario_ids):
        errors.append(f"公开场景题 ID 重复：{repeated[:10]}")
    allowed_scenario_types = {
        "first_person_interview", "public_question_bank",
        "project_interview_exercise", "engineering_practice",
        "secondary_index",
    }
    for scenario in scenarios:
        if scenario.get("source_type") not in allowed_scenario_types:
            errors.append(f"公开场景题来源类型无效：{scenario.get('id')}")
        if not str(scenario.get("source_url", "")).startswith("https://"):
            errors.append(f"公开场景题缺少 HTTPS 来源：{scenario.get('id')}")
        if not scenario.get("verification"):
            errors.append(f"公开场景题缺少核验说明：{scenario.get('id')}")
        for atom_id in scenario.get("atom_ids", []):
            if atom_id not in atom_ids:
                errors.append(f"公开场景题引用未知知识原子：{atom_id}")

    if args.strict_rag and inventory_path.exists():
        reviewable_ids = {
            unit.get("id")
            for unit in load_json("audits/rag/source-units.json", errors).get("units", [])
            if unit.get("review_status") == "mapped"
        }
        remaining = reviewable_ids - accepted_source_unit_ids
        if remaining:
            errors.append(f"严格 RAG 验收仍有 {len(remaining)} 个来源单元待人工复核")

    if inventory_path.exists():
        reviewable_units = [
            unit
            for unit in load_json("audits/rag/source-units.json", errors).get("units", [])
            if unit.get("review_status") == "mapped"
        ]
        reviewable_ids = {unit.get("id") for unit in reviewable_units}
        derived_reviewed = len(reviewable_ids & accepted_source_unit_ids)
        derived_pending = len(reviewable_ids - accepted_source_unit_ids)
        if manual_counts.get("manually_reviewed_semantic_units") != derived_reviewed:
            errors.append("人工审核状态的已审核数量与审核批次不一致")
        if manual_counts.get("pending_manual_semantic_units") != derived_pending:
            errors.append("人工审核状态的待审核数量与审核批次不一致")
        expected_percent = round(derived_reviewed / len(reviewable_units) * 100, 2)
        if manual_counts.get("manual_semantic_coverage_percent") != expected_percent:
            errors.append("人工审核状态的覆盖百分比与审核批次不一致")
        work_manual = work_status.get("manual_review", {})
        if work_manual.get("semantic_units") != len(reviewable_units):
            errors.append("工作状态的语义单元数量与来源盘点不一致")
        if work_manual.get("manually_reviewed_semantic_units") != derived_reviewed:
            errors.append("工作状态的已人工审核数量与审核批次不一致")
        if work_manual.get("pending_manual_semantic_units") != derived_pending:
            errors.append("工作状态的待人工审核数量与审核批次不一致")
        derived_by_source = Counter(
            unit.get("source_id")
            for unit in reviewable_units
            if unit.get("id") in accepted_source_unit_ids
        )
        semantic_by_source = Counter(unit.get("source_id") for unit in reviewable_units)
        queue_by_source = {
            item.get("source_id"): item
            for item in manual_review.get("source_queue", [])
        }
        for source_id, semantic_count in semantic_by_source.items():
            queue_item = queue_by_source.get(source_id, {})
            reviewed_count = derived_by_source[source_id]
            if queue_item.get("semantic_units") != semantic_count:
                errors.append(f"人工审核队列 {source_id} 的语义单元数不一致")
            if queue_item.get("manually_reviewed_semantic_units") != reviewed_count:
                errors.append(f"人工审核队列 {source_id} 的已审核数量不一致")
            if queue_item.get("pending_manual_semantic_units") != (
                semantic_count - reviewed_count
            ):
                errors.append(f"人工审核队列 {source_id} 的待审核数量不一致")

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

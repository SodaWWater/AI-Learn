#!/usr/bin/env python3
"""Collect source-level RAG units without copying third-party full text."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERIC_HEADINGS = {
    "目录", "小结", "总结", "概述", "引言", "参考资料", "参考资源",
    "相关资料", "相关资源", "相关文档", "学习资源", "引用格式", "更新日志",
    "贡献", "适用对象", "从这里开始", "核心观点", "内容涵盖", "研究目标",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def clean_text(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", "", value))
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def make_id(source_id: str, path: str, locator: str, title: str) -> str:
    raw = f"{source_id}\n{path}\n{locator}\n{title}".encode("utf-8")
    return f"RU-{hashlib.sha1(raw).hexdigest()[:12]}"


def classify(title: str, path: str, kind: str) -> tuple[str | None, str]:
    text = f"{title} {path}".lower()
    normalized = re.sub(r"^[\d.、\s]+", "", title).strip()
    normalized = re.sub(r"^[^A-Za-z0-9\u4e00-\u9fff]+", "", normalized).strip()

    if kind == "missing":
        return None, "missing"
    if kind == "placeholder":
        return None, "placeholder"
    if kind == "resource":
        if any(k in text for k in ("agentic", "graphrag", "multimodal", "多模态")):
            return "RAG-12", "resource"
        return "RAG-13", "resource"
    if normalized in GENERIC_HEADINGS or normalized.startswith("附录"):
        return None, "structural"
    if path.endswith("README.md") and any(
        marker in normalized.lower()
        for marker in ("资源总览", "论文分类", "从这里开始", "相关资源", "rag papers", "categories", "目录")
    ):
        return None, "structural"

    rules = [
        ("RAG-12", ("agentic", "self-rag", "crag", "adaptive rag", "graphrag", "graph rag", "deep research", "多模态", "multi-step", "高级模式", "高级范式", "复杂的 rag 范式", "不同的 rag 范式", "三代 rag", "四代演进", "不值得上图数据库")),
        ("RAG-11", ("生产", "增量", "缓存", "高并发", "延迟", "吞吐", "多租户", "权限", "安全", "成本", "可观测", "时间衰减", "动态与持续更新", "知识库更新", "更新 rag 知识库", "文档是否发生", "变更感知", "全量重建", "灰度更新", "性能瓶颈", "实际落地", "落地中")),
        ("RAG-10", ("评估", "评测", "指标", "ragas", "recall", "mrr", "ndcg", "faithfulness", "消融", "golden case", "失败归因", "量化你的 rag", "量化.*rag")),
        ("RAG-06", ("向量数据库", "vector-db", "vector db", "faiss", "milvus", "qdrant", "chroma", "pinecone", "hnsw", "ivf", "索引算法", "索引结构", "数据组织", "数据规模和实测性能")),
        ("RAG-05", ("embedding", "嵌入", "向量化", "相似度", "维度、速度", "对比学习", "静态词向量", "word2vec", "glove", "fasttext")),
        ("RAG-04", ("chunk", "切块", "切分", "分块", "splitter", "父子", "滑动窗口", "语义被切割", "文档切割", "粒度怎么定", "重叠切割", "语义边界", "contextual retrieval", "特殊内容专项")),
        ("RAG-03", ("文档解析", "document-parsing", "parser", "ocr", "表格", "图片", "清洗", "预处理", "版式", "公式解析", "文本识别", "数据治理", "文档是怎么存", "/etl/")),
        ("RAG-07", ("query", "查询改写", "查询扩展", "子问题", "hyde", "step-back", "意图识别", "查询增强", "搜索规划")),
        ("RAG-08", ("检索", "召回", "bm25", "hybrid", "混合", "rrf", "重排序", "rerank", "mmr", "cross-encoder", "retriever", "搜索系统", "结果过滤", "四层优化", "索引优化", "查询优化", "优化怎么组合", "核心区别对比")),
        ("RAG-09", ("生成", "generator", "prompt", "上下文", "引用", "拒答", "grounding", "lost in the middle", "幻觉", "答案", "证据", "事实性", "交叉验证", "来源编号", "方案怎么组合")),
        ("RAG-02", ("完整流程", "完整工作流程", "系统是怎样的工作流程", "流水线", "pipeline", "离线阶段", "在线阶段", "全链路", "架构", "ingestion", "indexing", "generation")),
        ("RAG-01", ("什么是 rag", "rag（retrieval", "rag 基础", "为什么需要 rag", "主要用来解决", "微调", "长上下文", "传统搜索", "定义与原理", "知识截止", "知识冻结", "知识过期", "知识空白", "私有数据", "不改参数")),
        ("RAG-13", ("面试", "项目", "代码", "框架", "工具", "选型", "实战", "场景", "问题", "开源", "学习路径")),
    ]
    for topic, terms in rules:
        if any(term in text for term in terms):
            return topic, "mapped"

    path_defaults = [
        ("document-parsing", "RAG-03"),
        ("vector-db", "RAG-06"),
        ("agentic_rag", "RAG-12"),
        ("multimodal", "RAG-12"),
        ("evaluation", "RAG-10"),
        ("context-engineering", "RAG-09"),
        ("interview", "RAG-13"),
        ("projects.md", "RAG-13"),
        ("rag技术.md", "RAG-01"),
    ]
    for marker, topic in path_defaults:
        if marker in text:
            return topic, "mapped"
    return None, "unmapped"


def add_unit(units: list[dict], source_id: str, path: str, locator: str,
             title: str, kind: str, level: int | None = None) -> None:
    topic, status = classify(title, path, kind)
    units.append({
        "id": make_id(source_id, path, locator, title),
        "source_id": source_id,
        "path": path,
        "locator": locator,
        "title": clean_text(title),
        "kind": kind,
        "heading_level": level,
        "canonical_topic": topic,
        "review_status": status,
    })


def markdown_units(units: list[dict], source_id: str, repo: Path, rel_path: str) -> None:
    path = repo / rel_path
    if not path.exists():
        add_unit(units, source_id, rel_path, "file", "文件未拉取或不存在", "missing")
        return
    suffix = path.suffix.lower()
    if suffix not in {".md", ".markdown"}:
        kind = "resource" if suffix in {".pdf", ".svg", ".png", ".jpg", ".webp"} else "implementation"
        add_unit(units, source_id, rel_path, "file", path.name, kind)
        return

    content = path.read_text(encoding="utf-8-sig", errors="replace")
    if "正在编写中" in content and len(content) < 1200:
        add_unit(units, source_id, rel_path, "file", path.stem, "placeholder")
        return

    in_fence = False
    found = False
    for line_no, line in enumerate(content.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r"^(#{1,4})\s+(.+?)\s*$", stripped)
        if not match:
            continue
        found = True
        level = len(match.group(1))
        title = re.sub(r"\s+#+$", "", match.group(2)).strip()
        add_unit(units, source_id, rel_path, f"L{line_no}", title, "heading", level)
    if not found:
        add_unit(units, source_id, rel_path, "file", path.stem, "resource")


def xiaolin_units(units: list[dict], source_id: str, repo: Path) -> None:
    manifest_path = repo / "source-manifest.json"
    data_path = repo / "questions-data.js"
    if not manifest_path.exists() or not data_path.exists():
        add_unit(units, source_id, "source-manifest.json", "file", "RAG 题库文件缺失", "missing")
        return

    manifest = load_json(manifest_path)
    questions = [q for q in manifest.get("questions", []) if q.get("category") == "rag"]
    for question in questions:
        add_unit(
            units, source_id, "source-manifest.json", question["id"],
            question["title"], "question", 1,
        )

    raw = data_path.read_text(encoding="utf-8")
    start = raw.find("[")
    end = raw.rfind("]")
    payload = json.loads(raw[start:end + 1])
    generic = {"💡 简要回答", "📝 详细解析", "🎯 面试总结", "📚 参考资料"}
    for question in payload:
        if question.get("category") != "rag":
            continue
        question_id = question.get("id", "unknown")
        headings = re.findall(r"<h([23])[^>]*>(.*?)</h\1>", question.get("content_html", ""), re.I | re.S)
        semantic_index = 0
        for level, value in headings:
            title = clean_text(value)
            if title in generic:
                continue
            semantic_index += 1
            add_unit(
                units, source_id, "questions-data.js",
                f"{question_id}:H{level}:{semantic_index}", title, "heading", int(level),
            )


def write_outputs(units: list[dict], output_json: Path, output_md: Path) -> None:
    by_source = Counter(unit["source_id"] for unit in units)
    by_status = Counter(unit["review_status"] for unit in units)
    by_topic = Counter(unit["canonical_topic"] or "NONE" for unit in units)
    payload = {
        "schema_version": 1,
        "generated_at": load_json(REPO_ROOT / "sources/registry.json")["retrieved_at"],
        "unit_count": len(units),
        "counts": {
            "by_source": dict(sorted(by_source.items())),
            "by_status": dict(sorted(by_status.items())),
            "by_topic": dict(sorted(by_topic.items())),
        },
        "units": units,
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# RAG 来源单元盘点", "",
        f"生成日期：{payload['generated_at']}", "",
        f"来源单元总数：**{len(units)}**", "",
        "## 状态汇总", "",
        "| 状态 | 数量 |", "|---|---:|",
    ]
    lines.extend(f"| `{key}` | {value} |" for key, value in sorted(by_status.items()))
    lines.extend(["", "## 标准主题覆盖", "", "| 主题 | 数量 |", "|---|---:|"])
    lines.extend(f"| `{key}` | {value} |" for key, value in sorted(by_topic.items()))
    lines.extend(["", "## 未映射或缺失", ""])
    problems = [u for u in units if u["review_status"] in {"unmapped", "missing"}]
    if not problems:
        lines.append("当前自动盘点未发现未映射或缺失单元；仍需人工复核自动分类是否准确。")
    else:
        for unit in problems:
            lines.append(f"- `{unit['id']}` `{unit['source_id']}` `{unit['path']}` — {unit['title']}")
    lines.extend([
        "", "## 说明", "",
        "本文件证明来源内容已进入盘点，但不证明知识已经完成去重或事实核验。",
        "`structural`、`resource` 和 `placeholder` 会保留，不计入标准知识正文。",
    ])
    output_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xiaolin", type=Path, default=REPO_ROOT.parent / "src-xiaolin")
    parser.add_argument("--guide1", type=Path, default=REPO_ROOT.parent / "src-guide1")
    parser.add_argument("--guide2", type=Path, default=REPO_ROOT.parent / "src-guide2")
    parser.add_argument("--output-json", type=Path, default=REPO_ROOT / "audits/rag/source-units.json")
    parser.add_argument("--output-md", type=Path, default=REPO_ROOT / "audits/rag/source-units.md")
    args = parser.parse_args()

    roots = {
        "xiaolin-ai-learning": args.xiaolin,
        "ai-agent-interview-guide": args.guide1,
        "agent-guide": args.guide2,
    }
    scope = load_json(REPO_ROOT / "sources/rag-scope.json")
    units: list[dict] = []
    for source in scope["sources"]:
        source_id = source["source_id"]
        root = roots[source_id]
        if source["collector"] == "xiaolin_question_bank":
            xiaolin_units(units, source_id, root)
        else:
            for rel_path in source["files"]:
                markdown_units(units, source_id, root, rel_path)

    units.sort(key=lambda item: (item["source_id"], item["path"], item["locator"], item["id"]))
    write_outputs(units, args.output_json, args.output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

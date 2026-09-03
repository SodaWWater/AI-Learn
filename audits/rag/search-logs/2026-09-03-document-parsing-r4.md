---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-DOCUMENT-PARSING
round: 4
searched_at: 2026-09-03
reviewer: Codex
status: round_complete
---

# 文档解析（Document Parsing）第四轮独立补漏

## 1. 独立检索设计

本轮从 Parser Intermediate Representation（解析器中间表示）和 PDF Rendering Mode（PDF 渲染模式）反查引用锚点与隐藏文本安全，不复用第三轮基准查询。使用 Docling 官方文档（Official Documentation）与固定源码提交（Pinned Source Commit）。

| 检索族 | 查询或入口 | 独立性 |
|---|---|---|
| 中间表示（Intermediate Representation） | `DoclingDocument hierarchy furniture bounding box provenance JSON pointer` | 从可执行数据模型核验字段 |
| 隐藏文本（Invisible Text） | `PDF backend visible text cells rendering mode paints nothing` | 从源码能力接口反查安全边界 |
| 引用稳定（Citation Stability） | `document provenance bounding box parent child chunk citation anchor` | 跨切分与引用核验 |
| 冲突查询（Conflict Search） | `parser empty result versus unsupported capability None` | 主动区分无内容和无法判断 |

## 2. 来源处理

| 来源 ID | 状态 | 用途 |
|---|---|---|
| `docling-document-model-2026` | `included` | 类型化文本、表格、图片、层级、Body/Furniture（正文/版面附属物）、Bounding Box（边界框）和 Provenance（来源信息） |
| `docling-pdf-backend-visible-text-2026` | `included` | 固定源码区分可见文本、不可见文本、空结果和能力未知，并暴露页面、形状与位图接口 |
| `mpdocbench-parse-2026` | `included_existing` | 继续提供跨页任务和评估压力，不重复登记 |

## 3. 新增类型与工程链路

| 类型 ID | 类别 | 内容 | 关系 |
|---|---|---|---|
| `PARSE-K-401` | `knowledge` | 文档中间表示应同时保存内容对象与结构树；Header/Footer Furniture（页眉/页脚版面附属物）和正文必须可区分，Reading Order（阅读顺序）由结构关系而非纯坐标排序单独表达 | `new` |
| `PARSE-K-402` | `knowledge` | Parser Capability Unknown（解析器能力未知）、Capability Supported but Empty（支持但结果为空）和 Invalid Page（无效页面）是三种状态；将 `None`、空列表和异常合并会造成错误回退 | `new` |
| `PARSE-P-401` | `problem_question` | PDF 可包含不绘制墨迹的文本层；若解析器无条件索引该层，隐藏指令、错误 OCR（光学字符识别）层或重复文本可能进入检索，而用户在页面上看不到 | `new` |
| `PARSE-P-402` | `problem_question` | Chunker（文本切分器）只复制纯文本不复制结构指针、页码和 Bounding Box（边界框）时，Citation Anchor（引用锚点）无法稳定回到原页面区域 | `extends` |
| `PARSE-S-401` | `solution` | 中间表示保留 `document_version + item_pointer + page + bbox + hierarchy + reading_order + visibility + parser_version`；切分产物保存源 Item（对象）跨度列表而非单一页码 | `new` |
| `PARSE-E-401` | `evaluation` | 目标集新增可见/不可见文本冲突、重复 OCR（光学字符识别）层、Body/Furniture（正文/版面附属物）、跨页表格和结构指针回放，分别测内容、结构和锚点正确率 | `extends` |

## 4. 公开题与覆盖检查

未新增公开题编号。`RAG-SCENE-002/007/008/010` 可承载复杂 PDF、扫描件、切分和部署问题，但“不可见文本进入索引”尚没有独立一手面试题，只登记工程问题。九类覆盖中安全由 `partial` 提升为有直接实现入口，但中文竖排和印章数据实验仍未执行。

## 5. 冲突与边界

- DoclingDocument（Docling 文档对象）表达 Bounding Box（边界框）和 Provenance（来源信息），不等于所有输入格式或后端都能提供这些字段。
- 固定源码中的 `get_visible_text_cells` 允许返回 `None`，因此“开启可见文本过滤”仍必须处理后端无法判断的状态。
- 结构指针跨 Parser Version（解析器版本）可能变化；稳定引用需同时固定文档内容哈希、解析器版本和源坐标，不能只保存 JSON Pointer（JSON 指针）。

## 6. 饱和判定与下一步

本轮新增知识类型 2、问题类型 1；连续无新增类型轮数保持 0，状态为 `round_complete`。下一轮执行解析—切分—引用联合回放，验证结构指针和坐标在重解析、增量更新与跨版本迁移后的稳定性。

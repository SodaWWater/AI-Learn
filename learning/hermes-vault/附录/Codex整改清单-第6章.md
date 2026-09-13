---
id: HERMES-CH06-CODEX-FIX
title: 第 6 章阅读问题整改清单（给 Codex）
status: action
reviewed_at: 2026-09-12
source_commit: f97a4102dd3864eed0c85132850ce7e06f13e09a
course_commit: d9e02cbed9dbeb2ad30f7a63905a831ca30cdba6
---

# 第 6 章整改清单（给 Codex）

## 0. 任务是什么 / 不是什么

**做：** 按下面每一条改 `chapters/06-memory-history-external-provider.md`。必要时同步 `附录/术语与源码索引.md`、`00-开始这里.md`、`章节总览.md`。把会卡住的机制**写进正文讲清楚**，修正与 `f97a410` 不一致的事实，补上漏掉的对象和钩子。

**不要做：**

- 不要把本文件的问答原文、对话记录、或「读者问了什么」贴进章节。
- 不要新增 FAQ / 学习对话栏目。
- 不要用 `reference-course/.../hermes-study/` 当实现证据。
- 不要把教学分层名写成源码类型（「五种信息」「是否值得长期复用」都不是源码对象）。
- 不要把第六章改成第五章那种 22 节算法稿；**保留现有架构-先、生命周期-后的骨架**，只改错、补漏、把图和表对齐源码。
- `python scripts/validate_repo.py --strict-rag` 和 `git diff --check` **不能**当作 Hermes 章节验收。

固定官方源码：`C:\Users\lmh\Downloads\hermes-study-work\hermes-agent` @ `f97a4102dd3864eed0c85132850ce7e06f13e09a`。改完后抽查所引 `def`/`class` 是否仍在该行。

已核对、**不要改坏**的口径：

- 工作消息 / Session 历史 / `USER.md` / `MEMORY.md` / 外部 Provider 是不同持久化路径
- 压缩摘要不自动升级成 `MEMORY.md`
- `ext_prefetch_cache` 是 `TurnContext` 运行时字段，不是 Memory 文件
- `trim_memory` 是进程 RSS
- 后台 review 用 messages 快照；无人值守的 replace/remove 进 pending，`add` 仍可走
- 源码地图里这 7 个行号是对的：`get_memory_dir:38`、`MemoryStore:66`、`memory_tool:172`、`_memory_turn_start_and_prefetch:754`、`build_api_messages:1018`、`finalize_turn:433`、`_rebuild_system_prompt_at_boundary:2782`

---

## 1. 函数名写错：没有 `MemoryStore.load`

**位置：** §5.2

**错误：** 「`MemoryStore.load` 会读取两个 Markdown 文件并捕获 frozen system-prompt snapshot」

**改成：** 读取入口是 `MemoryStore.load_from_disk()`（`tools/memory_tool_store.py:111`）。进程侧还有 `tools/memory_tool.py:47` `load_on_disk_store()`，内部调用 `load_from_disk()`。

正文第一次出现必须写源码函数名，不要发明 `load`。

---

## 2. 快照其实是四层，不是三层

**位置：** §5.2 的三层 `text` 块

**错误：** 只写磁盘文件 → MemoryStore → `_cached_system_prompt`。读者会以为 MemoryStore 里只有一份内容。

**改成四层（必须全部写进正文）：**

```text
1. 磁盘 USER.md / MEMORY.md          持久文件
2. MemoryStore.user_entries / memory_entries
     活列表；memory_tool 写入会改这里和磁盘
3. MemoryStore._system_prompt_snapshot
     load_from_disk 时冻结，给 system prompt 用（prefix-cache 稳定）
4. agent._cached_system_prompt
     已经拼进当前 Session 请求的提示词
```

点明：tool 写入后 **1 和 2 会变，3 和 4 通常仍是旧的**，直到压缩边界或下一次 Session 重建。这和第五章「磁盘改了 ≠ 模型马上看见」是同一件事，不要再写成「MemoryStore 已经加载的文件内容」糊成一层。

源码：`memory_tool_store.py:66-83`、`:111-133`、`:343`。

---

## 3. 「何时能看见 MEMORY.md」前后矛盾

**位置：** §2 末段 vs §8 表 vs §13 验证第 5 条

**错误：** §2 写「可能要等下一次 Session 重建 system prompt」。§8 / 验证第 5 条写压缩边界重建后也能看到。

**改成（全文统一，以 §8 为准）：**

- 普通 Turn：继续用冻结快照，磁盘变了模型也不一定看见
- 当前 Turn 要立刻用新内容：靠 Memory tool 返回或 prefetch 进工作上下文 / user API content
- 整份文件快照进入 system：压缩成功后的 `_rebuild_system_prompt_at_boundary`，或下一次 Session 启动加载
- 不是只有 `/new` 才刷新

§2 那句必须改掉「下一次 Session」这种唯一路径。

---

## 4. 总图不要画成自动分类器

**位置：** §1 mermaid（`D{是否值得长期复用}` → USER.md / MEMORY.md / External）、§4 mermaid（`C{判断复用价值}`）

**错误：** 看起来 Hermes 运行时会自动判断「用户偏好 vs 项目事实 vs 外部」并分流写入。源码没有这个分类器。

**改成：** 图里改成**写入入口**，不是价值判断：

```text
工作消息 / Session 历史     ← Turn 收尾默认路径
memory_tool(target=user|memory)  ← 模型或用户显式写入 USER.md / MEMORY.md
后台 memory review           ← 提议；add 可走，replace/remove 无人值守则 pending
外部 Memory Provider         ← prefetch 召回，sync_turn / session-end 同步
```

正文补一句：「用户偏好 vs 项目事实」是**写入时选定 `target`**（`user` 或 `memory`），不是单独一个分流模块。

---

## 5. pending 不只是后台 review

**位置：** §5.3、§7、§11

**错误：** 只写「后台 review 不能删/改，要 `/memory pending`」。读者会以为前台永远直写。

**改成两道门，分开写：**

| 门 | 源码 | 默认 | 行为 |
|---|---|---|---|
| 后台删除保护 | `memory_tool.py` 无人值守 + `_BG_DELETE_ACTIONS`（replace/remove） | 始终 | add 仍可走；replace/remove（含 batch）`stage_write`，`/memory pending` |
| 总闸门 | `tools/write_approval.py` `memory.write_approval` | **关**（`false`） | 打开后前台跨 Session 写入也不直接提交，同样 stage |

不要把 `write_approval` 默认写成开。源码注释：`false` (default) writes freely。

---

## 6. 补上 Memory 的真实对象，不要只列 tool 文件

**位置：** §6、§10 源码地图

**漏了：** 外部记忆的运行时对象。读者学完第四章会问「到底是哪个类」。

**§10 表必须增加（行号以 `f97a410` 为准，写入前再 `rg` 一次）：**

| 架构位置 | 固定源码入口 | 作用 |
|---|---|---|
| 协议 | `agent/memory_provider.py` `MemoryProvider` | prefetch / sync_turn / 可选钩子 |
| 编排 | `agent/memory_manager.py:289` `MemoryManager` | 多 Provider、prefetch_all、on_pre_compress |
| 后台审查 | `agent/background_review.py` | Turn 后 fork，用 messages 快照 |
| 写入审批 | `tools/write_approval.py` | pending 目录与 `/memory pending` |

§6 开头点明：外部 Provider **不是** `MEMORY.md` 的别名；本地文件走 `MemoryStore`，外部走 `MemoryManager` 里注册的 `MemoryProvider`。

---

## 7. 接上第五章已经提过、本章却没写的钩子

这些必须写进 §6 或 §8，不要另开 FAQ。

### 7.1 `on_pre_compress`

- `MemoryManager.on_pre_compress`（`memory_manager.py:664`）和协议 `MemoryProvider.on_pre_compress`
- **只**给压缩摘要模型喂 `memory_context` / checkpoint，**不是**把摘要写入 `MEMORY.md`
- `require_checkpoint` 失败则调用方应保住未压缩 transcript
- 与第五章「压缩 ≠ 更新 MEMORY.md」对齐

### 7.2 `prefetch` 会跳过 trivial prompt

- `_memory_turn_start_and_prefetch`：`is_trivial_prompt(_query)` 为真则不召回
- 空结果 ≠「外部没有相关事实」，也可能是跳过或失败（失败已被 `suppress`）

### 7.3 `system_prompt_block` vs `prefetch`

协议写得很清楚（`memory_provider.py:90-97`）：

- `system_prompt_block()`：静态、可进 system；召回内容**不要**走这里
- `prefetch()`：本轮按问题召回的候选，进 user API content / 工作上下文

禁止再把外部召回画进 `volatile` 里的 `MEMORY.md` 快照。

### 7.4 Session 换绑不是只有 `sync_turn`

补 `on_session_switch` / `on_session_end`（`memory_provider.py:129-138`）：

- `on_session_end`：真 Session 边界，不是每 Turn
- `on_session_switch`：`/resume`、`/branch`、`/reset`、`/new`、**压缩轮换** 改了 `session_id` 时换绑；`reset=True` 才是全新对话

否则读者会以为第五章轮换与外部记忆无关。

### 7.5 本地 Memory 有字符上限

`MemoryStore.__init__` 默认 `memory_char_limit=2200`、`user_char_limit=1375`。超限会 consolidation 失败，每 Turn 有失败次数上限（`_MAX_CONSOLIDATION_FAILURES_PER_TURN = 3`），不能当成无限追加。

---

## 8. 导航和术语同步

- `00-开始这里.md` 仍写只产出第 4、5 章 → 补上第 6 章初稿路径 `chapters/06-memory-history-external-provider.md`
- `章节总览.md` 已写「初稿已建立」可保留，但不要写成已严格验收
- `附录/术语与源码索引.md` 增补（若尚无）：`MemoryStore`、`load_from_disk`、`_system_prompt_snapshot`、`MemoryManager`、`MemoryProvider`、`ext_prefetch_cache`、`on_pre_compress`、`write_approval`；继续强调教学名 ≠ 字段

章节 frontmatter 补 `course_commit: d9e02cbed9dbeb2ad30f7a63905a831ca30cdba6`（与第 4、5 章一致）。课程只作线索，实现仍以官方提交为准。

---

## 9. 验收

1. 正文无 `MemoryStore.load`，只有 `load_from_disk` / `load_on_disk_store`。
2. §5.2 能读出四层：磁盘 / 活列表 / `_system_prompt_snapshot` / `_cached_system_prompt`。
3. 「模型何时看见 MEMORY.md」在 §2、§8、验证练习中口径一致，包含压缩边界。
4. §1 / §4 图是写入入口，不是「是否值得长期复用」分类器。
5. pending 同时写清后台 replace/remove 保护和默认关闭的 `write_approval`。
6. 源码地图含 `MemoryManager`、`MemoryProvider`、`background_review`、`write_approval`；正文有 `on_pre_compress`、trivial prefetch、`system_prompt_block` vs `prefetch`、`on_session_switch`。
7. 没有 FAQ / 「读者问」。
8. 表格无多余 `||`。
9. 所引行号能在 `f97a410` 对上对应 `def`/`class`。
10. 不要用 RAG 的 `validate_repo.py --strict-rag` 当本章通过证明。

---
id: HERMES-CH04-CH05-CODEX-FIX
title: 第 4–5 章阅读问题整改清单（给 Codex）
status: action
reviewed_at: 2026-09-12
source_commit: f97a4102dd3864eed0c85132850ce7e06f13e09a
course_commit: d9e02cbed9dbeb2ad30f7a63905a831ca30cdba6
---

# 第 4–5 章整改清单（给 Codex）

## 0. 任务是什么 / 不是什么

**做：** 按下面每一条去改 `chapters/04-*.md`、`chapters/05-*.md`（必要时同步 `附录/术语与源码索引.md`、`讲解/05-压缩-讲解稿.md`）。把读者会卡住的地方**写进正文讲清楚**，补全缺失步骤，修正与 `f97a410` 不一致的事实。

**不要做：**

- 不要把本文件的问答原文、对话记录、或「读者问了什么」整段贴进章节。
- 不要新增「常见问题 / FAQ / 学习对话」栏目来交差。
- 不要用 `reference-course/08-hermes-agent/hermes-study/` 当实现证据（剪枝副本：compressor 3244 行 vs 官方 4931 行）。
- 不要把教学分类名写成源码字段（`对话轨迹`、`活动消息`、`working_messages`、`runtime_controls` 都不是 `TurnContext` 字段）。
- 不要把第五章改回「先堆术语表」的旧结构；保留现有 22 节讲法，只补事实和缺的机制。

固定官方源码：`C:\Users\lmh\Downloads\hermes-study-work\hermes-agent` @ `f97a4102dd3864eed0c85132850ce7e06f13e09a`。行号以该树为准，改完后抽查 `def`/`class` 是否仍在所引行。

---

## 1. 必须恢复：第四章完整结构树

读者发现 **Codex 改第四章时把「完整结构树图」删掉了**。当前 §3.1 只有 mermaid 分层图 + 四类表 + JSON 快照，缺少一张**一眼能扫完的嵌套树**。

**要求：** 在 `chapters/04-context-engineering-request-assembly.md` 的 **§3.1「Context 本身的内部组成」** 中，mermaid 分层图之后、四类表之前（或紧挨四类表），重新加入下面这棵树。可以微调排版，**不得再删减层级，不得把 Skills 索引画进 tools 域。**

```text
本次请求的 Context（工程过程 / 概念集合，不是一个源码类）
│
├── 1. 指令文本  → 最终成为 Provider 的 system
│   ├── 源码产物：active_system_prompt（一个字符串）
│   ├── 语义分区（不是三个 Python 对象）：
│   │   ├── stable：SOUL.md、基础指导、编码简报
│   │   ├── context：system_message、AGENTS.md / 项目上下文、工作区说明
│   │   └── volatile：
│   │       ├── Skills 索引（已安装 skill 的目录：名字+简述）
│   │       ├── USER.md 快照
│   │       ├── MEMORY.md 快照
│   │       ├── 插件段
│   │       └── 时间行
│   └── 缓存：_cached_system_prompt / _cached_system_prompt_static
│
├── 2. 对话轨迹  → 最终成为 Provider 的 messages
│   ├── 「对话轨迹」是教学模块名，不是 TurnContext 字段
│   ├── conversation_history：本轮开始时已落盘基线（不单独发给模型）
│   ├── messages：工作稿 = 历史拷贝 + 本轮 user + 随后的 tool 轮
│   └── SessionDB messages 表
│       ├── active=1     下次请求还会带上（教学说法：活动行）
│       └── active=0, compacted=1  已被摘要归档，可搜索，不进下次请求
│
├── 3. 能力与环境  → 最终成为 Provider 的 tools + api_kwargs
│   ├── agent.tools / tools_for_api：函数 JSON Schema
│   │     （read_file、skill_view、terminal … 的参数说明书）
│   ├── 工作区快照 / cwd
│   └── Provider 配置：model / api_mode / …
│   └── 【Skills 索引不在这里】索引在 volatile；这里只有 skill_view 等函数定义
│
├── 4. 运行控制  → 通常不发给模型
│   ├── turn_id / effective_task_id / current_turn_user_idx
│   ├── 预算、压缩器、preflight_compression_blocked
│   └── plugin_user_context / ext_prefetch_cache
│
└── 组装结果（不是 TurnContext 字段）
    ├── api_messages     messages 的发送副本
    ├── tools_for_api    Schema 的 Provider 格式
    └── api_kwargs       最终 API 参数
```

树下用两三句话钉死：

- `Context` ≠ `TurnContext` ≠ Provider request。
- 树里带源码标识符的是真字段/真文件；「对话轨迹」「活动行」是教学名。
- Skills 有三层，见第 2 节，禁止画成两份相同文件。

---

## 2. 第四章：Skills 索引 vs 工具定义（读者卡住的点）

**现象：** `volatile` 里有 Skills 索引；「能力与环境」格里又写了 Skills 索引 / 像有一份 `SKILLS.md`。读者以为文档把同一份东西贴了两次。

**事实（`f97a410`）：**

| 层 | 是什么 | 去向 |
|---|---|---|
| Skills **索引** | `build_skills_system_prompt()` 扫各 skill frontmatter 生成的短目录，不是名为 `SKILLS.md` 的上下文文件 | `volatile` → system |
| **工具定义** | `agent.tools`：`skill_view` / `skills_list` / `read_file` 等 JSON Schema | 请求的 `tools` 参数 |
| Skill **正文** | 某个 skill 的 `SKILL.md` | 只有 `skill_view` 之后作为 tool 结果进 `messages` |

**要改：**

1. §3 开头四类表「能力与环境」那一行：删掉把「Skills 索引」和 `agent.tools` 捆在一起、去向写成 `tools` 的写法。索引归指令文本 / volatile；`agent.tools` 才去 `tools`。
2. §2.1 身份层表里「工具说明」容易和 `tools` 参数混。写明：system 里最多是能力目录/使用政策；函数 Schema 走 `tools` 参数。
3. §2.15 已有三对象表，保留并让它和结构树、四类表一致。点明：**没有**一份像 `AGENTS.md` 那样整段塞进 Context 的 `SKILLS.md`。
4. 教学 JSON 已分开（`volatile` 有 `## Skills`，`tools_for_api` 只有 `read_file`）。在 JSON 前后用一句话把三层指回去，避免读者只看表。

---

## 3. 第四章：生命周期漏了压缩预检（读者以为「预算与准入」没展开）

**现象：** §4 生命周期有「预算与准入」，§5 调用链却写成 `build_turn_context` → `assemble_api_request` → 发给模型。读者学第五章时无法把压缩插回第四章顺序。

**事实：** 压缩预检在 `build_turn_context` **内部**，对象 return 之前；loop 里每次即将调模型前还有一次。

**要改第四章（细节仍归第五章，但第四章必须标插入点）：**

1. §5 调用链改为（教学顺序，函数名保持原样）：

```text
_run_conversation_turn
  build_turn_context
    读历史、接上本轮 user、恢复 system          ← 原材料
    run_turn_start_compaction                   ← 时机 1：Turn 开头预检
    return TurnContext(...)                     ← 此时对象才出现，可能已是压过的
  拷字段到 _LoopState
  while:
    begin_iteration / prepare_iteration
    assemble_api_request                        ← 抽出即将寄出的整包
    run_preflight_gate                          ← 时机 2：每次发送前（含第一圈）
    _run_api_retry_loop                         ← 调 Provider
    normalize_model_response
    有 tool_calls → run_tool_round
         append_message(assistant / tool 结果)   ← 拼到 s.messages，不是 TurnContext 方法
         continue while
    纯文本 → finish_text_response
  finalize_turn
```

2. 「预算与准入」写清测的是**即将寄出的请求**（system + messages + tools Schema + 输出预留），不是 `TurnContext` 字段个数，也不是只数会话消息。
3. 写清：`conversation_history` 不进入这包；删掉该字段不会让压缩更少触发。
4. 写清：loop 拼接由 `run_tool_round` 对 `_LoopState.messages` 做 `append_message`；`TurnContext` 只在 Turn 开头构造一次。

源码锚点：

- `agent/turn_context.py` `build_turn_context`（约 898+）内调 `run_turn_start_compaction`
- `agent/turn_context_compaction.py` `run_turn_start_compaction`
- `agent/conversation_loop.py` `_run_conversation_turn`（约 1420–1565）
- `agent/turn_preflight_gate.py` `run_preflight_gate`（比较的是完整请求，不是裸 messages）
- `agent/turn_tool_round.py` `run_tool_round` + `append_message`

---

## 4. 第四章 / 第五章交界：压缩到底改哪一类 Context

读者的核心问题：**第四章把 Context 分成很多部分，第五章压的是哪几块？**

必须在第五章靠前（建议 §2 三个区别之后，或新开一小节，不要另开 FAQ）写进正文：

| 第四章的类 | 压不压 | 说明 |
|---|---|---|
| 指令文本 system | 不把文字拿去摘要 | 计入压力；提交成功后边界重建快照 |
| 对话轨迹 `messages` | **唯一主要改写对象** | 已含历史拷贝 + 本轮；减枝旧 tool 结果，摘要 middle |
| 能力与环境 tools Schema | 不摘要 | 计入压力；边界上可能刷新定义 |
| 运行控制 | 不发给模型、不压缩 | 只决定能不能压、失败怎么回滚 |

补一句：Skill 正文只有变成 `messages` 里的 tool 结果后才会被减枝。`MEMORY.md` 不是压缩产物。

---

## 5. 第五章必须讲清：`messages` vs `conversation_history`

读者反复卡在「为什么存两份、会不会浪费 Context 容量」。

**要写进第五章正文（建议减枝/提交附近，或「压什么」小节）：**

1. 二者都是 `TurnContext` 真字段，不是文档笔误。
2. 角色：`messages` = 本轮工作稿；`conversation_history` = 已落盘基线 / flush 指针 / 失败回滚参照。不是两份发给模型的全文。
3. Turn 开始：`messages = list(conversation_history)` 再 append 本轮 user。压缩器改的是这份已含历史的 `messages`。
4. **不占模型 token：** 寄出只有 `messages` → `api_messages`。基线只在进程内存里。
5. 提交成功后 `conversation_history_after_compression`（`conversation_compression.py:1864`）换指针：原地 → `list(messages)`；轮换 → `None`；失败 → 旧基线不动。
6. 「多久的历史」= 该 Session 当前 `active=1` 的全部行，不是「最近 N 分钟」。压过之后活动列表变成摘要+近尾，旧行 `active=0, compacted=1`。

禁止再写「只压最近会话、历史不压」。历史已经在 `messages` 里被压；history 字段事后换绑定。

---

## 6. 第五章必须讲清：活动行、阈值、MEMORY 快照

### 6.1 「活动消息」

教学说法，对应表列 `messages.active`。第一次出现就写：`active=1` 下次还会带上；`archive_and_compact` 把旧活动行打成 `active=0, compacted=1` 再插入短列表。不是对外 API 类型名。

### 6.2 阈值测整包

灯亮看 system + messages + tools（+ 输出预留）。Skills 索引变长、工具 Schema 变多也会亮灯。动手改的仍是 `messages`。

预检读数三级：`last_prompt_tokens` 锚点 → native estimate → rough。无锚点的 rough 超阈值会 `should_defer_preflight_to_real_usage`（`context_compressor.py:2449`），等一次真实 usage。

双层阈值必须写回（读者改稿后丢掉了）：

- Agent compressor 默认约 **50%**
- Gateway session hygiene 约 **85%**（`gateway/run_turn.py`）
- 锁/租约在 `compress_context` 内获取，不在预检 `if` 里

### 6.3 压缩 ≠ 写 MEMORY.md

三件分开写：

1. 压缩产物 = 较短的 `messages`，给下次请求用。
2. `on_pre_compress()` 可能给摘要模型喂 `memory_context` / checkpoint，不是把摘要写入 `MEMORY.md`。
3. `_rebuild_system_prompt_at_boundary`（`:2782`）在**提交成功后**失效缓存并重读 Memory/Skills。普通 Turn 用冻结 `_cached_system_prompt`；磁盘改了不等于模型马上看见。

`trim_memory(reason="post-compression")` 是把进程 RSS 还给 OS，与 `MEMORY.md` 无关。禁止再写成「压完就更新记忆文件」。

「重建」不是 new 一个全新 Context / 新开 Session：`session_id` 在原地压实时不变。只是前缀变了、prompt cache 必断，所以在这个合法窗口刷新 system / tools / history 基线 / usage 锚点 / skill 去重。字节完全一样则保留原 prompt 对象。

---

## 7. 第五章必须讲清：原地压实 vs 轮换

读者没有 Session 行概念，且会把轮换理解成 `/new`。

**正文要求（用本地 `hermes` CLI 举例，不要用 Telegram 当主例）：**

1. 减枝和摘要已经把字变短。压实/轮换只决定**短历史写进哪条 Session 记录**。
2. **默认原地**（`compression_in_place=True`，属性缺失也必须当 True，`:3600`）。同一 `session_id`，旧活动行归档，新列表成为活动页。本地一直聊就是这个。
3. **轮换不是运行时自动挑的特例**，不是「必须换物理行时产品会判断」。它是 `in_place: false` 的旧提交路径（测试称 legacy rotation）：关父行、开子行、摘要当子 Session 第一页、迁 `/goal` `/heartbeat` `/loop`。Gateway 卫生压缩和后台 review **强制** in_place。
4. 对比用户 `/new`：`/new` 是空白新对话；轮换是同一项工作换内部档案号，界面仍应像同一场。不是「你开新 session 就走轮换」。
5. 对本地学习：按默认原地记即可。轮换只需知道「系统有时会换内部 ID，不是用户 `/new`」。

---

## 8. 第五章源码事实：读者改稿后掉回去的，必须改回

保留 22 节结构，只改错句。

| 位置 | 错误 | 改成 |
|---|---|---|
| §9.1 序列化标签 | `[TOOL:read_file]` | `[TOOL RESULT {tool_call_id}]:`；助手调用是 `[Tool calls:\n  name(args)\n]`；去重占位 `[Duplicate tool output — same content as a more recent call]` |
| §12.1 | 「三个硬检查」 | `_candidate_rejected` 四段：中止 / 无进展（含忽略 `_db_persisted`）/ 空列表 / attempt 被取代。反增长在旁边的 `_salvage_or_refuse_grown_transcript` |
| §19 源码地图最后一行 | 「微压实同步 \| micro_compaction.py:201」 | 删掉或改写。`:199` `_micro_compact` 是**默认关闭**的滚动轮次摘要，不是 `prune_tool_results_only` 的 DB 同步。减枝提交在 `prune_tool_results_only` 自己的 `archive_and_compact` |

改稿后仍缺失、要补进合适小节（不要另开 FAQ）：

- `in_place` 缺省 True
- `protect_first_n` 默认 3，第一次压缩后 `_effective_protect_first_n` 变为 0
- 两套 prompt：摘要模型 `task=compression` vs 主模型看到的 `SUMMARY_PREFIX` 用户消息
- Gateway 85% vs Agent 50%
- `should_defer_preflight_to_real_usage`
- 术语：禁止再把 `prune_tool_results_only` 叫做 Micro-compaction；`micro_compaction.py` 单独一行，默认 off

---

## 9. 第五章：两个预检时机（读者最后问到的）

必须写进正文，建议紧挨「测压力」和「提交」之间，或生命周期专节：

```text
每个用户 Turn（不是「开 Session 一次」）：

时机 1  build_turn_context 内部、TurnContext return 之前
        测：messages + system（原材料）
        该压则压并刷新快照，再 return TurnContext

时机 2  while 每一圈：assemble_api_request 之后、run_preflight_gate
        测：已组装的完整请求（含 tools、注入、api_content）
        第一圈也会走，不是等有模型回复才有
        第二圈起：先 run_tool_round 把结果 append 到 s.messages，再 assemble + 预检

Turn 结束 finalize_turn 落盘 ≠ 第二次预检
```

钉死：

- 不是「先 new 完 TurnContext 再检测」。
- 拼接不是 TurnContext 的方法。
- 两拍都是为了挡住**下一包过大的请求**。

---

## 10. 术语表 / 讲解稿 / 总览同步

`附录/术语与源码索引.md` 增补（若尚无）：

- `对话轨迹`：教学名 = `conversation_history` + `messages`
- `活动行`：`messages.active=1`
- `in_place` 默认 True；轮换 = `in_place: false` 旧路径，≠ `/new`
- Skills 三层：索引 / Schema / `SKILL.md` 正文

`讲解/05-压缩-讲解稿.md`：序列化标签、四段检查、不要把 micro_compaction 当减枝同步；生命周期两拍与 loop 函数序和第五章一致。

`章节总览.md` / `00-开始这里.md`：若仍写「第五章已完成源码核对」，加一句「以本清单落地后的正文为准」。

---

## 11. 验收

改完后自检：

1. 第四章 §3.1 能看到完整结构树，Skills 索引只出现在 volatile，不在 tools 域。
2. 第四章四类表、§2.15、结构树、JSON 对 Skills 的说法一致。
3. 第四章调用链含 `run_turn_start_compaction` 与 `run_preflight_gate`，不再是「build_turn_context 直接 assemble」。
4. 第五章能独立回答：压的是 `messages`；history 是基线指针；阈值看整包；轮换 ≠ `/new`；默认原地。
5. 第五章无 `[TOOL:read_file]`、无「三个硬检查」当 `_candidate_rejected` 的定义、无「微压实同步 | micro_compaction.py:201」当减枝提交。
6. 正文没有「读者问：… / 答：…」问答体。
7. 所有行号能在 `f97a410` 对上对应 `def`/`class`。
8. Markdown 表格不要多写 `||`。

本机官方树：`C:\Users\lmh\Downloads\hermes-study-work\hermes-agent`。

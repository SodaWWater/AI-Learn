---
work_item_id: WP-P2-002
domain: RAG
stage_id: PS-CONTEXT-ASSEMBLY
round: 1
searched_at: 2026-09-02
reviewer: Codex
status: round_complete
---

# 节点检索日志（Stage Search Log）：上下文组装（Context Assembly）第一轮

## 1. 本轮目标与边界

核查 Token 预算、证据排序、去重、压缩、冲突处理和 Lost in the Middle。上下文组装负责把候选证据变成生成器输入，不把检索相关性等同于最终证据价值。

## 2. 实际检索式

| 编号 | 检索族 | 实际检索式 | 入口与范围 |
|---|---|---|---|
| Q-001 | 位置效应 | `site:arxiv.org lost in the middle long context position effect` | 原始论文 |
| Q-002 | 压缩 | `site:arxiv.org RECOMP context compression RAG selective augmentation` | RECOMP 原始论文 |
| Q-003 | 充分性 | `site:arxiv.org sufficient context RAG abstention` | Sufficient Context 原始论文 |
| Q-004 | 安全 | `site:arxiv.org indirect prompt injection retrieved documents` | 2026 原始论文 |
| Q-005 | 公开题目 | `site:nowcoder.com/discuss Lost in the Middle RAG 面试` | 牛客公开题库 |

## 3. 候选来源和取舍

| 来源 ID | 类型 | 纳入状态 | 取舍与回链 |
|---|---|---|---|
| `lost-in-the-middle-2023` | 原始论文（Original Paper） | `included` | 证据位置影响，不推广到所有模型 |
| `recomp-context-compression-2023` | 原始论文（Original Paper） | `included` | Extractive/Abstractive Compression 与 Selective Augmentation |
| `sufficient-context-2024` | 原始论文（Original Paper） | `included` | 区分上下文不足和模型未使用上下文 |
| `indirect-prompt-injection-wild-2026` | 原始论文（Original Paper） | `included` | 组装外部文档时的指令/数据边界 |

## 4. 本轮新增类型

| 类型 ID | 类别 | 简要说明 | 与现有内容关系 |
|---|---|---|---|
| `CTX-K-001` | `knowledge` | 相关性排序、证据覆盖、位置和 Token 成本需要联合优化 | `new` |
| `CTX-P-001` | `problem_question` | 重复 Chunk 消耗预算并放大同一来源权重 | `new` |
| `CTX-P-002` | `problem_question` | 压缩可能删掉限定条件、否定和引用边界 | `new` |
| `CTX-P-003` | `problem_question` | 冲突证据被无标记拼接后模型会隐式选边 | `new` |

## 5. 公开面试题来源核验

| 题目线索 ID | 短转述 | 来源类型 | 是否真实面试 | 技术核验 |
|---|---|---|---|---|
| `RAG-SCENE-020` | 长上下文中证据被忽略时怎样组装 | 公开题库（Public Question Bank） | 否 | Lost in the Middle、RECOMP、Sufficient Context |

## 6. 九类覆盖检查

| 覆盖面 | 状态 | 证据或缺口 |
|---|---|---|
| 原理 | `covered` | 预算、位置、压缩、充分性 |
| 实现 | `partial` | 框架级 Compressor 和 Token Counter 待补 |
| 工程问题 | `covered` | 超长、重复、冲突、跨片段关系 |
| 解决方案 | `partial` | 父子展开、聚类去重和冲突 Schema 待补 |
| 评估 | `partial` | 压缩保真度与证据覆盖率待补 |
| 公开面试题 | `covered` | 公开题库已有 |
| 时效 | `covered` | 2023–2026 资料 |
| 安全或治理 | `partial` | 间接注入过滤与信任分区待补 |
| 跨节点关系 | `covered` | 连接切分、重排、生成、引用 |

## 7. 冲突、版本与未验证假设

- 不接受“把更多 Chunk 放入长上下文即可”的无条件结论；
- 压缩后的文本不能默认保留引用完备性；
- 下一轮补 Contextual Compression 框架实现、冲突证据和去重键策略。

## 8. 饱和判定

| 判定项 | 结果 |
|---|---|
| 已登记来源是否全部处理 | 否 |
| 九类覆盖是否全部完成 | 否 |
| 本轮新增知识类型数 | 1 |
| 本轮新增问题类型数 | 3 |
| 连续无新增类型轮数 | 0 |
| 当前结论 | `round_complete` |

## 9. 下一轮动作

补 Token 分配算法、压缩保真度、父子展开、冲突 Schema、去重与间接注入隔离。

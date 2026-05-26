---
name: project-sinan
description: Project Sinan helps Codex and other coding agents add a durable AGENTS.md entrypoint and lightweight .project memory to any long-running project. Use it when starting a new project, taking over a messy folder, continuing previous work, preventing goal drift, or asking an agent to remember the original goal, current status, tasks, and handoff notes across sessions.
---

# 项目司南 Project Sinan

项目司南的核心原则：

不要把长对话当作项目记忆。把稳定上下文写入项目目录，让新会话先读再做。

`AGENTS.md` 是 AI 对话入口，负责告诉任何新会话“开工先读什么、做事怎么落盘、结束前回写哪里”。`.project/` 是轻量项目记忆后端：

| 文件 | 职责 | 更新频率 |
| --- | --- | --- |
| `AGENTS.md` | AI 开工协议、真源优先级、收尾协议 | 项目规则改变时 |
| `.project/BRIEF.md` | 最初目标、成功标准、范围和关键产出 | 目标改变时 |
| `.project/STATUS.md` | 当前阶段、事实、决策、阻塞和交接说明 | 每次重要推进后 |
| `.project/TASKS.md` | 未完成动作、完成判据和验证证据 | 执行任务时 |
| `.project/tasks/` | 单个任务完成后的归档记录 | 每个独立任务收尾时 |

不要把日常小问答都写入状态文件；只沉淀会影响后续执行的事实、选择、阻塞或产出。

## 接管前诊断

初始化前先判断项目已有真源，不要机械套同一个结构：

| 项目情况 | 模式 | 做法 |
| --- | --- | --- |
| 空文件夹 | 新建模式 | 创建 `AGENTS.md` 和 `.project/` 三件套 |
| 已经混乱的旧项目或散乱文件夹 | 接管模式 | 首轮只读盘点，建立项目地图和交接台，不移动、不删除、不重命名 |
| 已有 brief、decision log、roadmap | 适配模式 | 保留原文档为事实真源，`.project/BRIEF.md` 只做索引和目标摘要 |
| 大型 monorepo | 子项目模式 | 根 `AGENTS.md` 只放通用协议；具体任务在 feature/issue 层维护状态 |
| Notion、数据库或平台运营项目 | 外部真源模式 | 本地只记录外部真源链接、当前任务和恢复步骤，不复制敏感或动态数据 |

## 运行前检查

1. 识别目标项目目录：优先使用用户指定路径；否则使用当前工作目录。
2. 读取已有 `AGENTS.md`、项目说明、任务文件、`docs/**` 中的 brief/decision log/roadmap 和 `git status --short`，避免覆盖已有规则或用户改动。
3. 从本 `SKILL.md` 所在目录定位脚本，不依赖固定安装路径：

```bash
python3 "<skill_dir>/scripts/init_project.py" --project "<project_dir>" --check
```

`--check` 是只读检查；缺少司南文件会返回非零状态并列出待初始化项目。脚本仅使用 Python 标准库，不需要凭证、网络或额外依赖。

## 初始化项目

当用户要开新项目、为现有目录接入管理，或当前项目因散乱文档而缺少真源时：

1. 从用户请求和现有文件中提炼项目标题、目标与首个可验证结果。只在目标无法合理推断且写错会误导项目时，询问一个简短问题。
2. 如需先预览将新增哪些文件，运行：

```bash
python3 "<skill_dir>/scripts/init_project.py" \
  --project "<project_dir>" \
  --title "<项目标题>" \
  --goal "<一句话目标>" \
  --truth-source "docs/00-project/decision-log.md" \
  --dry-run
```

3. 初始化：

```bash
python3 "<skill_dir>/scripts/init_project.py" \
  --project "<project_dir>" \
  --title "<项目标题>" \
  --goal "<一句话目标>" \
  --success "<首个成功标准>" \
  --truth-source "docs/00-project/decision-log.md"
```

4. 读取新建或既有的 `AGENTS.md` 和三份 `.project` 文件，用真实上下文补全占位项。初始化脚本不会覆盖已存在的状态文件，也只会向已有 `AGENTS.md` 追加一个带边界标记的项目司南入口区块。

## 中途接管混乱项目

当用户已经打开一个旧项目、文件夹很乱、历史方案很多，或不确定哪些文件还能用时，进入接管模式。接管模式第一轮目标是建立地图，不是重新装修房子。

首轮必须遵守：

1. 只读盘点项目结构、`AGENTS.md`、README、`docs/**`、最近修改文件、任务/计划文件和 `git status --short`。
2. 不移动、不删除、不重命名任何既有文件；不把旧文件自动归档。
3. 先判断候选真源：需求/brief、decision log、roadmap、代码入口、数据源、外部链接、最近正在编辑的文件。
4. 初始化或追加项目司南入口后，在 `.project/STATUS.md` 记录“项目地图”“候选真源”“混乱点/疑问”“当前可继续的工作入口”。
5. 在 `.project/TASKS.md` 写入“确认真源与整理方案”的待办，而不是直接执行整理。

只有在用户明确确认整理方案后，才进入第二阶段整理。

## 每次继续项目

当用户在已接入的项目中提出任何会产生文件、决策或多步骤执行的任务：

1. 先读 `AGENTS.md`、`.project/BRIEF.md`、`.project/STATUS.md` 和 `.project/TASKS.md`。
2. 用一句话复述本轮与最初目标的关系；若请求偏离范围，指出偏离并确认是否修改 `BRIEF.md`。
3. 执行前将明确的新任务写入 `TASKS.md`，带上可检查的完成判据；很小的即时问答无需入账。
4. 执行工作并验证实际结果，不把“讨论过”标成“已完成”。
5. 在形成决定、完成阶段、遇到阻塞或即将结束会话时，回写 `STATUS.md` 和 `TASKS.md`。

回复用户时优先报告：当前目标、已完成证据、剩余下一步和阻塞。

## 文件管理规则

- `.project/` 只放管理面文件，不放正式交付物或素材。
- 正式产出沿用项目已有目录约定；没有约定时，先按产出类型建立少量清晰目录，如 `docs/`、`src/`、`assets/`、`deliverables/`。
- 新产生的研究结论若只是支撑执行，先写入 `STATUS.md` 的相关事实或决策。
- 不删除或重命名用户既有文件来“整理”项目，除非用户明确授权。

## 收口检查

宣告一项任务或阶段完成前：

1. 对照 `BRIEF.md` 的成功标准。
2. 运行适合该项目的最小验证，例如测试、构建、链接检查或文档核读。
3. 在 `TASKS.md` 将事项勾选完成并记录验证证据。
4. 在 `STATUS.md` 写明当前阶段、关键产出路径、仍未完成事项和下一次接手入口。
5. 如果本轮是一个可独立交付的任务，在 `.project/tasks/YYYY-MM-DD-短任务名.md` 归档。

## 示例触发

- “我新建了一个文件夹，帮我把这个新产品研究项目管起来。”
- “继续上次那个课程迁移项目，看看还有哪些任务没完成。”
- “这个目录里文档很乱，先整理项目目标和下一步，不要丢上下文。”
- “把这次开发的决定记下来，下次打开 Codex 能直接接着做。”

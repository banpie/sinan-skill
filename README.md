# 项目司南 Project Sinan

[English README](README.en.md)

项目司南是一个给 AI 协作项目使用的轻量 Skill：它会为项目建立 `AGENTS.md` 入口和 `.project/` 项目记忆，让 Codex、OpenCode、Claude Code 等 Agent 每次接手时先读取目标、状态和任务，再继续推进。

它解决的问题很朴素：不要把长对话当作项目记忆。把稳定上下文写回项目文件。

## 适合谁

- 正在开发网站、落地页、小工具或产品原型的人。
- 正在整理课程、资料包、交付文档或训练营 SOP 的人。
- 用 AI 连续推进一个项目，但经常发现“越改越乱”的人。
- 接手旧项目、散乱文件夹，想先建立项目地图再整理的人。

## 它会创建什么

项目司南会在目标项目中创建或补齐：

- `AGENTS.md`：AI 的开工说明书。
- `.project/BRIEF.md`：项目目标、成功标准、范围和真源索引。
- `.project/STATUS.md`：当前阶段、关键事实、决策、阻塞和交接入口。
- `.project/TASKS.md`：未完成任务、完成判据和验证证据。
- `.project/tasks/`：可选的单任务归档目录。

一句话记忆：

> `BRIEF` 管“为什么做”，`STATUS` 管“现在到哪”，`TASKS` 管“下一步做什么”。

## 快速开始

克隆仓库：

```bash
git clone https://github.com/banpie/project-sinan.git
```

先做只读检查：

```bash
python3 project-sinan/scripts/init_project.py --project /path/to/your/project --check
```

预览将新增哪些文件：

```bash
python3 project-sinan/scripts/init_project.py \
  --project /path/to/your/project \
  --title "我的项目" \
  --goal "用一句话说明项目目标" \
  --dry-run
```

正式初始化：

```bash
python3 project-sinan/scripts/init_project.py \
  --project /path/to/your/project \
  --title "我的项目" \
  --goal "用一句话说明项目目标" \
  --success "定义一个可验证的阶段成功标准"
```

脚本只使用 Python 标准库，不需要 API Key、账号 Cookie、网络请求或额外依赖。

## 给 Agent 的提示词

在 Codex、OpenCode 或其它支持 Skill / 文件读写的 Agent 中，可以这样使用：

```text
请使用「项目司南」的方式接管这个项目。

先不要修改任何正式文件。

请先读取当前项目里的说明、任务、文档和最近修改文件，判断项目目标、当前阶段、候选真源和混乱点。

如果项目还没有项目记忆，请帮我建立 AGENTS.md 和 .project 三件套。

建好以后，先告诉我：这个项目现在从哪里继续最合适。

如果这是一个旧项目，第一轮只读盘点，不移动、不删除、不重命名任何文件。
```

## 重要原则

- 第一轮接管旧项目时，只读盘点，不移动、不删除、不重命名。
- `.project/` 只放项目管理记忆，不放正式交付物或素材。
- 已有业务文档、代码规则、数据库、Notion 或平台后台是真源时，以这些位置为准。
- 敏感信息不要写入项目记忆，只记录“真源在哪里”和“下一步怎么继续”。

## 开源与隐私

项目司南本身不需要任何密钥或登录态，也不会上传你的项目内容。它只在你指定的项目目录中创建文本文件。

但请注意：如果你把真实客户资料、账号密码、内部报价写进项目文件，这些内容仍然属于你的项目数据，需要你自己做好访问控制和脱敏。

## License

MIT

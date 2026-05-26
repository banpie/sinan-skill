# 司南 Skill Sinan Skill

[English README](README.en.md)

司南 Skill 是一个给 AI 协作项目使用的轻量 Skill：它会为项目建立 `AGENTS.md` 入口和 `.project/` 项目记忆，让 Codex、OpenCode、Claude Code 等 Agent 每次接手时先读取目标、状态和任务，再继续推进。

它解决的问题很朴素：不要把长对话当作项目记忆。把稳定上下文写回项目文件。

## 适合谁

- 刚创建了一个新项目，想让 AI 从一开始就别跑偏。
- 项目已经在跑，但文件、任务、文档有点乱，需要重新梳理。
- 正在开发网站、落地页、小工具或产品原型的人。
- 正在整理课程、资料包、交付文档或训练营 SOP 的人。
- 用 AI 连续推进一个项目，但经常发现“越改越乱”的人。
- 接手旧项目、散乱文件夹，想先建立项目地图再整理的人。

## 它会创建什么

司南 Skill 会在目标项目中创建或补齐：

- `AGENTS.md`：AI 的开工说明书。
- `.project/BRIEF.md`：项目目标、成功标准、范围和真源索引。
- `.project/STATUS.md`：当前阶段、关键事实、决策、阻塞和交接入口。
- `.project/TASKS.md`：未完成任务、完成判据和验证证据。
- `.project/tasks/`：可选的单任务归档目录。

一句话记忆：

> `BRIEF` 管“为什么做”，`STATUS` 管“现在到哪”，`TASKS` 管“下一步做什么”。

## 快速开始

### 1. 让 Agent 直接安装（推荐）

如果你正在用 Codex、OpenCode 或其它能读网页/执行命令的 Agent，可以直接把仓库链接发给它：

```text
请打开这个开源仓库并阅读 README：

https://github.com/banpie/sinan-skill

请帮我把这个 Skill 安装到当前 Agent 可用的 Skill 目录里。

安装后请不要立刻修改我的项目文件，先告诉我安装到了哪里，以及下一步怎么在当前项目里使用。
```

### 2. 手动安装到 Codex

把 Skill 放到 Codex 的 Skill 目录：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/banpie/sinan-skill.git ~/.codex/skills/sinan-skill
```

如果 Codex 已经打开，安装后建议新开一个会话，让它重新读取 Skill 列表。

### 3. 手动安装到 OpenCode

把 Skill 放到 OpenCode 的 Skill 目录：

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/banpie/sinan-skill.git ~/.config/opencode/skills/sinan-skill
```

也可以只给某个项目使用：

```bash
mkdir -p .opencode/skills
git clone https://github.com/banpie/sinan-skill.git .opencode/skills/sinan-skill
```

### 4. 直接说关键词

安装好以后，打开你的目标项目，不用输入复杂命令。直接对 Agent 说这些话就可以：

```text
初始化项目
```

```text
接管这个项目
```

```text
整理这个项目
```

```text
继续项目
```

```text
帮我建立项目记忆，别丢上下文
```

Agent 会自动读取 `SKILL.md`，判断当前目录是新项目、已经在跑的项目，还是需要先盘点的混乱项目。

如果你同时安装过旧版“项目管家”或其它项目管理类 Skill，Agent 可能会优先命中旧 Skill。遇到这种情况，第一次可以说得更明确：

```text
使用 sinan-skill 初始化项目
```

确认能正常触发后，日常再说“初始化项目”“接管项目”“继续项目”就可以。

### 5. 验证安装成功

最简单的自测方式：

1. 新建一个空文件夹。
2. 用 Codex 或 OpenCode 打开这个文件夹。
3. 只说一句：

```text
初始化项目
```

成功时，你会看到新建了这些文件：

```text
AGENTS.md
.project/BRIEF.md
.project/STATUS.md
.project/TASKS.md
```

如果没有创建，先检查两件事：

- Skill 是否放在正确目录：Codex 是 `~/.codex/skills/sinan-skill/`，OpenCode 是 `~/.config/opencode/skills/sinan-skill/`。
- OpenCode 是否能正常调用模型；如果它提示模型不可用，请先在 OpenCode 里切换到可用模型，再重新说“初始化项目”。

## 新项目和旧项目怎么用

司南 Skill 有两条主线：新项目从一开始建立项目记忆；老项目先只读接手，再判断下一步。

新项目可以说：

```text
初始化项目。项目目标：做一个 AI 课程资料整理工具。
```

已经在跑的项目可以说：

```text
接管这个项目。第一轮只读盘点，不移动、不删除、不重命名文件。
```

项目很乱时可以说：

```text
整理这个项目。先按旧项目接手流程开始，不要直接整理文件。
```

继续上次的项目可以说：

```text
继续项目。请从项目记忆和未完成任务接上。
```

## 这个仓库为什么不只有 SKILL.md

标准入口仍然是仓库根目录的 `SKILL.md`。其它目录是为了让 Skill 更稳定：

- `SKILL.md`：给 Agent 看的核心工作流和触发规则。
- `scripts/init_project.py`：初始化 `AGENTS.md` 和 `.project/` 的辅助脚本。
- `agents/openai.yaml`：给 Codex 等平台展示名称、简介和默认提示词。

## 手动运行脚本

如果你的 Agent 不支持 Skill，也可以手动运行脚本。先克隆仓库：

```bash
git clone https://github.com/banpie/sinan-skill.git
```

先做只读检查：

```bash
python3 sinan-skill/scripts/init_project.py --project /path/to/your/project --check
```

预览将新增哪些文件：

```bash
python3 sinan-skill/scripts/init_project.py \
  --project /path/to/your/project \
  --title "我的项目" \
  --goal "用一句话说明项目目标" \
  --dry-run
```

正式初始化：

```bash
python3 sinan-skill/scripts/init_project.py \
  --project /path/to/your/project \
  --title "我的项目" \
  --goal "用一句话说明项目目标" \
  --success "定义一个可验证的阶段成功标准"
```

脚本只使用 Python 标准库，不需要 API Key、账号 Cookie、网络请求或额外依赖。

## 重要原则

- 第一轮接管旧项目时，只读盘点，不移动、不删除、不重命名。
- `.project/` 只放项目管理记忆，不放正式交付物或素材。
- 已有业务文档、代码规则、数据库、Notion 或平台后台是真源时，以这些位置为准。
- 敏感信息不要写入项目记忆，只记录“真源在哪里”和“下一步怎么继续”。

## 开源与隐私

司南 Skill 本身不需要任何密钥或登录态，也不会上传你的项目内容。它只在你指定的项目目录中创建文本文件。

但请注意：如果你把真实客户资料、账号密码、内部报价写进项目文件，这些内容仍然属于你的项目数据，需要你自己做好访问控制和脱敏。

## License

MIT

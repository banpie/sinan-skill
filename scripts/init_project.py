#!/usr/bin/env python3
"""Initialize an AGENTS.md AI entrypoint and project memory for AI-assisted projects."""

from __future__ import annotations

import argparse
import datetime as dt
import pathlib
import sys


START_MARKER = "<!-- sinan-skill:start -->"
END_MARKER = "<!-- sinan-skill:end -->"
LEGACY_START_MARKER = "<!-- project-sinan:start -->"
LEGACY_END_MARKER = "<!-- project-sinan:end -->"


def agents_block() -> str:
    return f"""\
{START_MARKER}
## 司南 Skill 入口

本项目主要通过 AI 对话推进。`AGENTS.md` 是每次新会话的入口，`.project/` 是跨会话项目记忆后端。

### 开工协议

- 开始任何多步任务或会产生文件的工作前，先读取本文件。
- 再读取 `.project/BRIEF.md`、`.project/STATUS.md`、`.project/TASKS.md`，以及当前任务相关的既有真源文档。
- 如果用户请求偏离 `.project/BRIEF.md` 的目标或范围，先指出偏离并确认是否更新项目目标。

### 真源优先级

- 既有业务文档、代码规则、数据库、Notion 或平台后台是真源时，以这些位置为准；`.project/` 只做摘要、索引和交接。
- `.project/BRIEF.md` 记录目标、范围、成功标准和真源索引；除非用户调整目标，不随意改写。
- `.project/STATUS.md` 记录当前阶段、事实、决策、阻塞和下一次接手入口。
- `.project/TASKS.md` 记录待办、完成判据和验证证据。

### 文件与收尾

- 新文档必须服务于明确产出；临时探索结论优先收拢到状态文件，不散落无主说明文件。
- 宣告阶段完成前，对照成功标准，运行必要验证，并更新 `.project/STATUS.md` 和 `.project/TASKS.md`。

### 中途接管乱项目

- 如果这是中途接管的旧项目，第一轮只做只读盘点和索引：识别项目目标、候选真源、当前工作入口、混乱点和待确认问题。
- 未经用户确认，不移动、删除、重命名或归档既有文件。
- 整理文件夹属于第二阶段；先在 `.project/TASKS.md` 写入整理方案确认任务。
{END_MARKER}
"""


def agents_template(title: str) -> str:
    return f"""\
# {title} AGENTS.md

本文件是 AI 会话进入本项目时优先读取的项目规则入口。

{agents_block()}
"""


def format_truth_sources(sources: list[str]) -> str:
    if not sources:
        return "- 待补充：列出已有 brief、decision log、roadmap、Notion、数据库或外部平台真源。"
    return "\n".join(f"- `{source}`" for source in sources)


def brief_template(title: str, goal: str, success: str, date: str, truth_sources: list[str]) -> str:
    return f"""\
# 项目简报

- 项目：{title}
- 初始化日期：{date}

## 最初目标

{goal}

## 成功标准

- {success}

## 真源索引

{format_truth_sources(truth_sources)}

## 范围

### 包含

- 待补充：本项目必须交付的内容。

### 不包含

- 待补充：明确暂不处理的内容，防止目标漂移。

## 约束与偏好

- 待补充：时间、技术、格式、预算或协作约束。

## 关键产出

| 产出 | 路径 | 状态 |
| --- | --- | --- |
| 待补充 | 待确定 | 未开始 |
"""


def status_template(date: str) -> str:
    return f"""\
# 当前状态

- 最后更新：{date}
- 当前阶段：初始化
- 总体状态：待补全项目简报并拆解第一阶段任务

## 已知事实

- 已建立项目目标、状态和任务的持久记录入口。

## 项目地图

| 区域/文件 | 初步判断 | 备注 |
| --- | --- | --- |
| 待盘点 | 未确认 | 中途接管旧项目时，先列出候选真源、当前工作文件和历史参考文件 |

## 关键决策

| 日期 | 决策 | 原因 |
| --- | --- | --- |
| {date} | 使用 `.project/` 作为项目管理真源 | 让后续 AI 会话可以恢复上下文 |

## 阻塞与风险

- 待识别。混乱项目首轮不要移动、删除、重命名或归档既有文件。

## 混乱点与待确认问题

- 待补充：哪些文件重复、哪些是真源、哪些只是历史方案。

## 交接入口

- 下一步：补全 `BRIEF.md` 的范围与关键产出，并把第一阶段工作拆入 `TASKS.md`。
- 重要路径：`.project/BRIEF.md`、`.project/STATUS.md`、`.project/TASKS.md`。
"""


def tasks_template(date: str) -> str:
    return f"""\
# 任务清单

每项任务都应有可验证的完成判据；完成后补充产出路径或验证结果。

## 进行中

- [ ] 补全 `.project/BRIEF.md` 的范围、约束和关键产出。完成判据：占位项已替换为真实信息。

## 待办

- [ ] 拆解第一阶段任务。完成判据：任务包含产出或验证方式。
- [ ] 如果这是中途接管的混乱项目，先确认真源与整理方案。完成判据：已列出保留、继续编辑、历史参考、建议归档/合并/重命名/删除的文件清单，并获得用户确认。

## 阻塞

- 无。

## 已完成

- [x] {date} 初始化司南 Skill 文件。证据：`.project/` 与司南入口规则已创建。
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="为 AI 协作项目创建 AGENTS.md 入口和轻量持久记忆；适合新项目初始化和旧项目接管整理；默认仅补缺，不覆盖已有内容。"
    )
    parser.add_argument("--project", default=".", help="目标项目目录，默认当前目录。")
    parser.add_argument("--title", help="项目标题；未提供时使用目录名。")
    parser.add_argument("--goal", help="一句话最初目标。")
    parser.add_argument("--success", help="首个可验证成功标准。")
    parser.add_argument(
        "--truth-source",
        action="append",
        default=[],
        help="已有事实真源路径或链接，可重复传入，例如 docs/00-project/decision-log.md。",
    )
    parser.add_argument("--check", action="store_true", help="只读检查项目是否已接入司南 Skill。")
    parser.add_argument("--dry-run", action="store_true", help="预览需要新增的文件，不实际写入。")
    return parser.parse_args()


def required_state(project: pathlib.Path) -> list[tuple[pathlib.Path, str]]:
    date = dt.date.today().isoformat()
    title = ARGS.title or project.name or "未命名项目"
    goal = ARGS.goal or "- 待补充：用一句话说明这个项目最终要解决什么问题。"
    success = ARGS.success or "待补充：定义一个能够判断阶段完成的结果。"
    return [
        (project / ".project" / "BRIEF.md", brief_template(title, goal, success, date, ARGS.truth_source)),
        (project / ".project" / "STATUS.md", status_template(date)),
        (project / ".project" / "TASKS.md", tasks_template(date)),
    ]


def required_dirs(project: pathlib.Path) -> list[pathlib.Path]:
    return [
        project / ".project" / "tasks",
    ]


def agents_action(path: pathlib.Path) -> str:
    if not path.exists():
        return "create"
    text = path.read_text(encoding="utf-8")
    if (START_MARKER in text and END_MARKER in text) or (
        LEGACY_START_MARKER in text and LEGACY_END_MARKER in text
    ):
        return "ready"
    return "append"


def check_project(project: pathlib.Path) -> int:
    missing = [str(path.relative_to(project)) for path, _ in required_state(project) if not path.exists()]
    missing.extend(str(path.relative_to(project)) for path in required_dirs(project) if not path.exists())
    action = agents_action(project / "AGENTS.md")
    if action != "ready":
        missing.append("AGENTS.md 中的司南入口")
    if missing:
        print(f"项目尚未完全接入司南 Skill：{project}")
        for item in missing:
            print(f"- 缺少：{item}")
        return 1
    print(f"司南 Skill 检查通过：{project}")
    return 0


def initialize(project: pathlib.Path, dry_run: bool) -> int:
    if not dry_run:
        project.mkdir(parents=True, exist_ok=True)
    changes: list[str] = []
    for path in required_dirs(project):
        if path.exists():
            continue
        changes.append(f"创建 {path.relative_to(project)}")
        if not dry_run:
            path.mkdir(parents=True, exist_ok=True)

    for path, content in required_state(project):
        if path.exists():
            continue
        changes.append(f"创建 {path.relative_to(project)}")
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    agents_path = project / "AGENTS.md"
    action = agents_action(agents_path)
    if action == "create":
        changes.append("创建 AGENTS.md 并写入司南入口")
        if not dry_run:
            title = ARGS.title or project.name or "未命名项目"
            agents_path.write_text(agents_template(title), encoding="utf-8")
    elif action == "append":
        changes.append("向现有 AGENTS.md 追加司南入口")
        if not dry_run:
            existing = agents_path.read_text(encoding="utf-8")
            separator = "\n\n" if existing and not existing.endswith("\n\n") else ""
            agents_path.write_text(existing + separator + agents_block(), encoding="utf-8")

    if not changes:
        print(f"项目已接入司南 Skill，无需修改：{project}")
        return 0

    prefix = "将执行" if dry_run else "已完成"
    print(f"{prefix}：{project}")
    for change in changes:
        print(f"- {change}")
    return 0


def main() -> int:
    global ARGS
    ARGS = parse_args()
    project = pathlib.Path(ARGS.project).expanduser().resolve()
    if ARGS.check:
        return check_project(project)
    return initialize(project, ARGS.dry_run)


ARGS: argparse.Namespace

if __name__ == "__main__":
    sys.exit(main())

# Project Sinan

[中文说明](README.md)

Project Sinan is a lightweight skill for long-running AI-assisted projects. It adds an `AGENTS.md` entrypoint and a `.project/` memory folder so Codex, OpenCode, Claude Code, and similar agents can read the project goal, status, tasks, and handoff notes before continuing the work.

The core idea is simple: do not treat a long chat as project memory. Persist stable context back into project files.

## Who It Is For

- People building websites, landing pages, tools, or product prototypes with AI.
- People preparing courses, deliverables, documentation, or operating SOPs.
- People who use AI across many rounds and feel the project becoming harder to control.
- People taking over messy folders who want a project map before reorganizing anything.

## What It Creates

Project Sinan creates or completes these files in your target project:

- `AGENTS.md`: the agent's entrypoint and working protocol.
- `.project/BRIEF.md`: the original goal, success criteria, scope, and source-of-truth index.
- `.project/STATUS.md`: current phase, facts, decisions, blockers, and handoff notes.
- `.project/TASKS.md`: open tasks, completion criteria, and verification evidence.
- `.project/tasks/`: optional archive records for completed standalone tasks.

Quick mental model:

> `BRIEF` explains why the project exists, `STATUS` explains where it stands, and `TASKS` explains what to do next.

## Quick Start

### Install As A Skill

The standard Skill entrypoint is the repository-level `SKILL.md`. The `scripts/` directory contains helper scripts the Skill can run; `agents/` contains display or adapter metadata for different agent platforms.

Install globally for Codex:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/banpie/project-sinan.git ~/.codex/skills/project-sinan
```

Install globally for OpenCode:

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/banpie/project-sinan.git ~/.config/opencode/skills/project-sinan
```

For project-local use, you can also clone or symlink this repository into the project's Skill directory, for example `.opencode/skills/project-sinan/` for OpenCode.

After installing, open the target project in Codex, OpenCode, or another `SKILL.md`-aware agent and say:

```text
Use project-sinan to initialize this project.
```

Or:

```text
Use Project Sinan to take over this project. First do a read-only audit, then create AGENTS.md and the .project memory files.
```

The agent reads `SKILL.md`, decides whether the current directory is a new project, an existing project, or a messy takeover, and then runs `scripts/init_project.py` when appropriate.

### Run The Script Manually

Clone the repository:

```bash
git clone https://github.com/banpie/project-sinan.git
```

Run a read-only check:

```bash
python3 project-sinan/scripts/init_project.py --project /path/to/your/project --check
```

Preview the changes:

```bash
python3 project-sinan/scripts/init_project.py \
  --project /path/to/your/project \
  --title "My Project" \
  --goal "Describe the project goal in one sentence" \
  --dry-run
```

Initialize the project:

```bash
python3 project-sinan/scripts/init_project.py \
  --project /path/to/your/project \
  --title "My Project" \
  --goal "Describe the project goal in one sentence" \
  --success "Define a verifiable first success criterion"
```

The script uses only the Python standard library. It requires no API key, cookie, network request, or extra dependency.

## Prompt For Agents

Use this with Codex, OpenCode, or any file-aware coding agent:

```text
Use Project Sinan to take over this project.

Do not modify any production files yet.

First, read the existing project notes, task files, documentation, and recently modified files. Identify the project goal, current phase, candidate sources of truth, and confusing areas.

If the project has no durable project memory yet, create the AGENTS.md and .project files.

After that, tell me where this project should continue next.

If this is an old or messy project, the first pass must be read-only. Do not move, delete, or rename any existing files.
```

## Principles

- When taking over an old project, the first pass is read-only: map first, reorganize later.
- `.project/` stores project-management memory, not final deliverables or source assets.
- If business docs, code conventions, databases, Notion pages, or platform backends are the real source of truth, keep them as the source of truth.
- Do not write sensitive information into project memory. Record where the source lives and how to continue the work.

## Privacy

Project Sinan does not need credentials or login state, and it does not upload your project content. It only creates text files inside the project directory you specify.

You are still responsible for the data you put in your project. Avoid writing customer data, passwords, internal pricing, or other secrets into project memory.

## License

MIT

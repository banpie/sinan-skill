# Sinan Skill

[中文说明](README.md)

Sinan Skill is a lightweight skill for long-running AI-assisted projects. It adds an `AGENTS.md` entrypoint and a `.project/` memory folder so Codex, OpenCode, Claude Code, and similar agents can read the project goal, status, tasks, and handoff notes before continuing the work.

The core idea is simple: do not treat a long chat as project memory. Persist stable context back into project files.

## Who It Is For

- People starting a brand-new project who want the agent to keep the goal stable from day one.
- People with an already-running project that needs to be reorganized before the next round of work.
- People building websites, landing pages, tools, or product prototypes with AI.
- People preparing courses, deliverables, documentation, or operating SOPs.
- People who use AI across many rounds and feel the project becoming harder to control.
- People taking over messy folders who want a project map before reorganizing anything.

## What It Creates

Sinan Skill creates or completes these files in your target project:

- `AGENTS.md`: the agent's entrypoint and working protocol.
- `.project/BRIEF.md`: the original goal, success criteria, scope, and source-of-truth index.
- `.project/STATUS.md`: current phase, facts, decisions, blockers, and handoff notes.
- `.project/TASKS.md`: open tasks, completion criteria, and verification evidence.
- `.project/tasks/`: optional archive records for completed standalone tasks.

Quick mental model:

> `BRIEF` explains why the project exists, `STATUS` explains where it stands, and `TASKS` explains what to do next.

## Quick Start

### 1. Ask Your Agent To Install It (Recommended)

If you are using Codex, OpenCode, or another agent that can read webpages and run commands, give it the repository link directly:

```text
Please open this open-source repository and read the README:

https://github.com/banpie/sinan-skill

Install this Skill into the Skill directory that is usable by the current agent.

After installing, do not modify my project files yet. First tell me where it was installed and how I should use it in the current project.
```

### 2. Install For Codex Manually

Put the Skill in Codex's skills directory:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/banpie/sinan-skill.git ~/.codex/skills/sinan-skill
```

If Codex is already open, start a new session after installing so it can reload the Skill list.

### 3. Install For OpenCode Manually

Put the Skill in OpenCode's global skills directory:

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/banpie/sinan-skill.git ~/.config/opencode/skills/sinan-skill
```

Or install it for one project only:

```bash
mkdir -p .opencode/skills
git clone https://github.com/banpie/sinan-skill.git .opencode/skills/sinan-skill
```

### 4. Use Simple Trigger Phrases

After installing, open the target project and say one of these:

```text
Initialize this project.
```

```text
Take over this project.
```

```text
Organize this project.
```

```text
Continue this project.
```

```text
Set up project memory so we do not lose context.
```

The agent reads `SKILL.md`, decides whether the current directory is a new project, an already-running project, or a messy takeover, and then runs `scripts/init_project.py` when appropriate.

If you also have an older project-management Skill installed, the agent may route to that older Skill first. In that case, be explicit the first time:

```text
Use sinan-skill to initialize this project.
```

After you confirm it works, short phrases such as “Initialize this project”, “Take over this project”, and “Continue this project” should be enough.

### 5. Verify The Install

The simplest smoke test:

1. Create an empty folder.
2. Open that folder with Codex or OpenCode.
3. Say only:

```text
Initialize this project.
```

When it works, these files should appear:

```text
AGENTS.md
.project/BRIEF.md
.project/STATUS.md
.project/TASKS.md
```

If they do not appear, check two things first:

- The Skill is in the right directory: `~/.codex/skills/sinan-skill/` for Codex, or `~/.config/opencode/skills/sinan-skill/` for OpenCode.
- OpenCode can call its configured model. If OpenCode says the model is unavailable, switch to an available model first, then say “Initialize this project” again.

## New Projects And Existing Projects

Sinan Skill has two main paths: set up durable memory for a new project from day one, or take over an existing project with a read-only audit first.

For a new project, say:

```text
Initialize this project. Project goal: build an AI course resource organizer.
```

For an existing project, say:

```text
Take over this project. First pass is read-only. Do not move, delete, or rename files.
```

For a messy folder, say:

```text
Organize this project. Start with the existing-project takeover flow. Do not reorganize files directly.
```

To continue previous work, say:

```text
Continue this project. Pick up from the project memory and open tasks.
```

## Why This Repository Has More Than SKILL.md

The standard Skill entrypoint is still the repository-level `SKILL.md`. The other files make the Skill more reliable:

- `SKILL.md`: the core agent workflow and trigger rules.
- `scripts/init_project.py`: a helper script that creates `AGENTS.md` and `.project/`.
- `agents/openai.yaml`: display metadata and default prompt for Codex-like platforms.

## Run The Script Manually

If your agent does not support Skills, you can run the script manually. First clone the repository:

```bash
git clone https://github.com/banpie/sinan-skill.git
```

Run a read-only check:

```bash
python3 sinan-skill/scripts/init_project.py --project /path/to/your/project --check
```

Preview the changes:

```bash
python3 sinan-skill/scripts/init_project.py \
  --project /path/to/your/project \
  --title "My Project" \
  --goal "Describe the project goal in one sentence" \
  --dry-run
```

Initialize the project:

```bash
python3 sinan-skill/scripts/init_project.py \
  --project /path/to/your/project \
  --title "My Project" \
  --goal "Describe the project goal in one sentence" \
  --success "Define a verifiable first success criterion"
```

The script uses only the Python standard library. It requires no API key, cookie, network request, or extra dependency.

## Principles

- When taking over an old project, the first pass is read-only: map first, reorganize later.
- `.project/` stores project-management memory, not final deliverables or source assets.
- If business docs, code conventions, databases, Notion pages, or platform backends are the real source of truth, keep them as the source of truth.
- Do not write sensitive information into project memory. Record where the source lives and how to continue the work.

## Privacy

Sinan Skill does not need credentials or login state, and it does not upload your project content. It only creates text files inside the project directory you specify.

You are still responsible for the data you put in your project. Avoid writing customer data, passwords, internal pricing, or other secrets into project memory.

## License

MIT

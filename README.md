# NYLDN Skills

Shared Codex and AI-assistant skills maintained by NYLDN.

## Quick Install

Install the default skills into Codex:

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash
```

Install the Graphify skill and also install or update the Graphify CLI:

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- graphify --with-graphify-cli
```

The installer clones this repo to `~/.codex/nyldn-skills` and symlinks skills into `~/.codex/skills`. Re-running it pulls the latest repo changes and refreshes the symlinks.

## Available Skills

### Graphify

Use `$graphify` or ask Codex to use the Graphify skill when you need to build, refresh, query, troubleshoot, or operationalize project knowledge graphs.

What it includes:

- A graph-first workflow for architecture and relationship questions.
- Install and troubleshooting guidance for Graphify's `graphifyy` package and `graphify` CLI.
- A `graphify_doctor.py` diagnostic script that checks CLI state, Codex config, graph freshness, `.graphifyignore`, Google Workspace pointer files, and likely next steps.
- Research notes summarizing Graphify v7 docs and recent Reddit usage patterns.

Graphify CLI install, if you do it manually:

```bash
uv tool install --force "graphifyy[office,video,mcp]"
graphify install --platform codex
```

For a project that should always use an existing graph:

```bash
cd /path/to/project
graphify codex install
```

Codex uses `$graphify` in chat. Some upstream Graphify examples use `/graphify`, which is the Claude-style command.

## Manual Install

```bash
git clone https://github.com/nyldn/skills.git ~/.codex/nyldn-skills
mkdir -p ~/.codex/skills
ln -sfn ~/.codex/nyldn-skills/skills/graphify ~/.codex/skills/graphify
```

If `~/.codex/skills/graphify` already exists as a real directory, move it aside before symlinking:

```bash
mv ~/.codex/skills/graphify ~/.codex/skills/graphify.backup.$(date +%Y%m%d%H%M%S)
ln -sfn ~/.codex/nyldn-skills/skills/graphify ~/.codex/skills/graphify
```

## Development

Skill directories live under `skills/<name>/`.

Each skill should include:

- `SKILL.md` with concise frontmatter and operational instructions.
- `agents/openai.yaml` when UI metadata or a default prompt is useful.
- `scripts/` for executable diagnostics or helpers.
- `references/` for longer research notes or detailed guidance.

Validate a skill locally:

```bash
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/graphify
python3 -m py_compile skills/graphify/scripts/graphify_doctor.py
```

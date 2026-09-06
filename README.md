# NYLDN skills

[![skills.sh](https://skills.sh/b/nyldn/skills)](https://skills.sh/nyldn/skills)

Small, practical workflows that help coding agents do recurring engineering
work consistently.

Instead of explaining the same process in every prompt, install a skill once.
The agent gets a clear method, useful checks, and a definition of done. Every
skill is a readable Markdown file, so you can inspect it and adapt it.

## Installation (30-second setup)

Run this from a terminal:

```bash
npx skills@latest add nyldn/skills
```

Choose the skills you want and the coding agents that should receive them. The
installer currently finds two skills:

- `graphify`
- `repo-delivery`

Use `--global` if you want the selected skills available in every project:

```bash
npx skills@latest add nyldn/skills --global
```

Start a new agent session if an installed skill does not appear immediately.

## Why use these skills?

- **Less repeated prompting:** describe the result you want without restating
  the full workflow.
- **More reliable work:** each skill gives the agent ordered steps and checks.
- **Easy to trust:** the instructions are ordinary files you can read before
  using them.
- **Easy to adapt:** install only what helps and change your local copy when a
  project needs different rules.

## Included skills

| Skill | What it helps you do |
|---|---|
| [Graphify](skills/graphify/SKILL.md) | Map how code and documents connect, answer questions about a project, and diagnose stale or broken knowledge graphs. |
| [Repository delivery](skills/repo-delivery/SKILL.md) | Make installation, updates, and removal easier for users. Choose packaging that fits the project and test the steps a new user will follow. |

## Using a skill

Name the skill in your prompt and describe the result you want:

```text
$repo-delivery Review this project's setup and make it easier for a new user
to install, update, and remove.
```

```text
$graphify Map this project and explain how authentication connects to billing.
```

Repository delivery needs no separate runtime. Graphify needs the Graphify CLI
when you want it to build or query a knowledge graph; those setup steps are
under **Other installation options** below.

## More standalone skills

[Claude Octopus](https://github.com/nyldn/claude-octopus) includes several
skills whose core workflows work without installing Octopus. A few mention
optional Octopus helpers or related skills, but those references are not needed
to complete the main workflow.

These links open the source skills in the Octopus repository. The installer
above does not install them.

| Skill | What it helps you do |
|---|---|
| [Agent topology audit](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-agent-topology/SKILL.md) | Decide whether each agent in a multi-agent workflow adds enough value to justify its coordination cost. |
| [Content analysis pipeline](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-content-pipeline/SKILL.md) | Study successful articles and posts, then turn their structure and techniques into a reusable guide. |
| [Decision support](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-decision-support/SKILL.md) | Compare practical options, explain the tradeoffs, and recommend a clear course of action. |
| [Documentation sync](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-doc-sync/SKILL.md) | Bring project documentation back in line with the code after a change or release. |
| [Meta-prompt](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-meta-prompt/SKILL.md) | Turn a rough request into precise instructions with clear constraints, output requirements, and checks. |
| [PRD writing](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-prd/SKILL.md) | Turn a product idea into clear requirements, priorities, success measures, and acceptance criteria. |
| [Review response](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-review-response/SKILL.md) | Check review feedback against the code before accepting it, fixing it, or explaining why it should not be applied. |
| [Security framing](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-security-framing/SKILL.md) | Handle outside URLs and content safely without treating untrusted text as instructions. |
| [Systematic audit](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-audit/SKILL.md) | Check a codebase methodically, record evidence, and turn findings into a prioritized repair plan. |
| [Test coverage audit](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-coverage-audit/SKILL.md) | Find important changed code that tests do not exercise and add focused coverage. |
| [Thought partner](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-thought-partner/SKILL.md) | Explore an early idea through questions, alternatives, and concrete next steps. |
| [Verification gate](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-verification-gate/SKILL.md) | Require fresh evidence before claiming that work is complete, fixed, or ready to ship. |
| [Visual feedback](https://github.com/nyldn/claude-octopus/blob/main/.claude/skills/skill-visual-feedback/SKILL.md) | Turn screenshots and visual bug reports into scoped fixes and repeatable checks. |

## Updating or removing skills

Update skills installed through the standard installer:

```bash
npx skills@latest update
```

Choose installed skills to remove:

```bash
npx skills@latest remove
```

Add `--global` when updating globally installed skills.

## Other installation options

<details>
<summary><strong>Install a linked copy for Codex</strong></summary>

The repository's installer maintains one checkout under
`~/.codex/nyldn-skills` and links the selected skill into
`~/.codex/skills`.

**Repository delivery**

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- repo-delivery
```

**Graphify**

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- graphify
```

Rerun a command to pull updates. If a real directory already occupies the
destination, the installer moves it to a timestamped backup before linking.
You can [read the installer](install.sh) before running it.

</details>

<details>
<summary><strong>Install or update the Graphify CLI</strong></summary>

With [uv](https://docs.astral.sh/uv/getting-started/installation/) installed,
run:

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- graphify --with-graphify-cli
```

This installs or updates the `graphifyy` package with its office, video, and
MCP extras, then attempts Graphify's Codex integration. The executable is named
`graphify`. The [Graphify skill](skills/graphify/SKILL.md) includes project
setup and troubleshooting.

</details>

<details>
<summary><strong>Change where the Codex installer stores skills</strong></summary>

Set `CODEX_HOME` to use a different Codex home. Set
`NYLDN_SKILLS_HOME` to choose where the shared repository checkout is stored.
Run `bash install.sh --help` from a checkout to see every option.

</details>

## Developing a skill

Skills live in `skills/<name>/`. Keep the main workflow in `SKILL.md`,
longer guidance in `references/`, and executable helpers in `scripts/`. Add
`agents/openai.yaml` when a skill needs interface metadata.

If Codex's skill-creator tools are installed, validate a skill from this
checkout:

```bash
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/repo-delivery
```

Use `skills/graphify` instead to validate Graphify. Check its diagnostic
script with:

```bash
python3 -m py_compile skills/graphify/scripts/graphify_doctor.py
```

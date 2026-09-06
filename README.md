# NYLDN skills

Practical skills for understanding codebases and making software easier to
install and use.

Each skill gives your coding agent a repeatable workflow for a specific job.
Pick the ones you need. The instructions live in readable Markdown files you
can inspect and adapt to your project.

## Skills

| Skill | What it helps you do |
|---|---|
| [Graphify](skills/graphify/SKILL.md) | Map how code and documents connect, answer questions about a project, and diagnose stale or broken knowledge graphs. |
| [Repository delivery](skills/repo-delivery/SKILL.md) | Make installation, updates, and removal easier for users. Choose packaging that fits the project and test the steps a new user will follow. |

## More standalone skills

[Claude Octopus](https://github.com/nyldn/claude-octopus) includes several
skills whose core workflows work without installing Octopus. A few mention
optional Octopus helpers or related skills, but those references are not needed
to complete the main workflow. These links open the source skills in that
repository. They are not installed by this repository's installer.

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

## Install

The included installer sets up skills for **Codex**. Run the command for the
skill you want in a terminal with Bash, Git, and curl available.

**Repository delivery**

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- repo-delivery
```

**Graphify**

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- graphify
```

You can [read the installer](install.sh) before running it. Start a new Codex
session if the installed skill does not appear.

## Use

Name the skill in your prompt and describe the result you want:

```text
$repo-delivery Review this project's setup and make it easier for a new user
to install, update, and remove. Keep the approach appropriate for this repo.
```

```text
$graphify Map this project and explain how authentication connects to billing.
```

Repository delivery needs no separate runtime. Graphify also needs the
Graphify CLI. Its setup option is below.

## Setup and updates

<details>
<summary>Install or update the Graphify CLI</summary>

With [uv](https://docs.astral.sh/uv/getting-started/installation/) installed, run:

```bash
curl -fsSL https://raw.githubusercontent.com/nyldn/skills/main/install.sh | bash -s -- graphify --with-graphify-cli
```

This installs or updates the `graphifyy` package with its office, video, and MCP
extras, then attempts Graphify's Codex integration. The executable is named
`graphify`. The [Graphify skill](skills/graphify/SKILL.md) has the project setup
and troubleshooting steps.

</details>

<details>
<summary>Where skills live and how to update them</summary>

The installer clones this repository to `~/.codex/nyldn-skills` and links the
selected skill into `~/.codex/skills`. If a real directory already occupies the
destination, the installer moves it to a timestamped backup before linking.

Rerun an install command to pull the latest repository changes. All skills
linked to that checkout receive those updates. If you edit the cloned files,
preserve your changes before updating.

Set `CODEX_HOME` to use a different Codex home, or `NYLDN_SKILLS_HOME` to choose
where the repository is cloned. Run `bash install.sh --help` from a checkout
for the available options.

</details>

<details>
<summary>Develop or adapt a skill</summary>

Skills live in `skills/<name>/`. Keep the workflow in `SKILL.md`, longer guidance
in `references/`, and executable helpers in `scripts/`. Add `agents/openai.yaml`
when a skill needs UI metadata.

If Codex's skill-creator tools are installed, validate a skill from this checkout:

```bash
uv run --with pyyaml python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/repo-delivery
```

Use `skills/graphify` instead to validate Graphify. Its diagnostic script can
also be checked with:

```bash
python3 -m py_compile skills/graphify/scripts/graphify_doctor.py
```

</details>

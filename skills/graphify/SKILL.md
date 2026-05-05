---
name: graphify
description: Use when a user asks to build, update, query, troubleshoot, install, or operationalize Graphify knowledge graphs for code, docs, papers, images, office files, video or audio, URLs, team workflows, CI, MCP, or slash command confusion such as $graphify vs /graphify.
---

# Graphify

Graphify turns project material into a traversable knowledge graph. Use this skill to make the agent actually read, refresh, and query that graph instead of treating Graphify as a passive background index.

## Fast Paths

Use these defaults unless the user gives a narrower instruction:

- `Why is Graphify not working?` Run the doctor script, fix the first concrete blocker, then re-run the check.
- `Build a graph for this project`: inspect scope first, add or recommend `.graphifyignore` for noisy projects, then run `graphify extract .`.
- `Use the graph to answer this`: read `GRAPH_REPORT.md`, run a traversal command, then inspect source files only for exact details.
- `Set this up for the team`: install platform instructions/hooks, configure merge-driver support, and document which `graphify-out` files should be committed.
- `Make it always-on`: run the platform installer, verify Codex `multi_agent = true`, and confirm the project instructions mention reading `GRAPH_REPORT.md`.

When reporting back, include the exact command run, graph freshness, whether the answer came from graph traversal or raw files, and the next useful command.

## First Move

Classify the request, then check the local state before acting:

- `answer from graph`: read `graphify-out/GRAPH_REPORT.md` first, then use `graphify query`, `graphify path`, or `graphify explain` before raw grep.
- `build or refresh`: inspect install state, scope, `.graphifyignore`, and graph freshness.
- `diagnose`: run `python scripts/graphify_doctor.py <project-path>` from this skill directory, or read the script and adapt it if the environment differs.
- `install`: remember the PyPI package is `graphifyy`, while the CLI is `graphify`.
- `Codex command`: use `$graphify`; upstream README examples for Claude often use `/graphify`.

For broad or expensive corpora, pause long enough to define scope. Start with one high-value subfolder when the project has large docs/media, cloud-drive archives, generated files, dependency folders, or unclear ownership.

## Build Or Refresh

Use the current Graphify CLI when possible:

```bash
uv tool install --force "graphifyy[office,video,mcp]"
graphify install
graphify codex install
```

Pick the smallest command that satisfies the request:

```bash
graphify extract .
graphify update .
graphify update --force .
graphify query "How does authentication relate to billing?"
graphify path "Concept A" "Concept B"
graphify explain "Concept"
graphify tree
```

Prefer `graphify extract <path>` for headless, CI, scripts, docs-only corpora, or runs where no Claude slash-command surface is available. Prefer `graphify update <path>` after code edits when a graph already exists; use `--force` only after confirming the normal update is stuck or stale.

Use `.graphifyignore` aggressively. Exclude generated output, dependency directories, binary dumps, caches, vendor folders, and irrelevant cloud-sync artifacts. If the graph output is not in `graphify-out`, check `GRAPHIFY_OUT`.

For Google Workspace projects, do not treat `.gdoc`, `.gsheet`, or `.gslides` files as document contents. They are pointer files. Export them to Markdown, `.docx`, `.xlsx`, `.pptx`, or another real content format before expecting Graphify to extract useful semantic nodes.

## Graph-First Answers

When a graph exists, do not answer architecture, dependency, or relationship questions from raw files alone.

1. Read `graphify-out/GRAPH_REPORT.md` for god nodes, communities, surprising connections, and suggested questions.
2. Check whether the graph is fresh enough for the task. Look at `needs_update`, `built_at_commit`, `graphify check-update .`, and recent file edits.
3. Use graph traversal for relationship questions:

```bash
graphify query "What modules own patient interview ingestion?"
graphify path "Google Docs export" "Markdown conversion registry"
graphify explain "conversion registry"
```

4. Use raw files afterward for exact line references, implementation details, or anything the graph does not cover.
5. If you modify code in a project with Graphify installed, run `graphify update .` before claiming the graph is current.

Good graph-first responses say what was checked:

- `Graph source`: `GRAPH_REPORT.md`, `graphify query`, `graphify path`, or `graphify explain`.
- `Freshness`: current commit match, `needs_update`, or why freshness could not be verified.
- `Limits`: missing line numbers, stale docs, skipped file types, or areas that still required source inspection.

## Team And CI Setup

For shared repos, keep the useful graph artifacts versioned and keep noisy state out of git:

```gitignore
graphify-out/cache/
graphify-out/costs*
graphify-out/manifest*
```

Usually commit `graphify-out/graph.json`, `graphify-out/GRAPH_REPORT.md`, and any intentionally shared visualization or wiki output. Run `graphify hook install` for merge-driver support and `graphify codex install` for Codex instructions/hooks. Re-run platform install when Graphify warns that the installed skill is older than the package.

For CI, use `graphify extract <path>` with the needed API keys or backend environment. Treat `graphify-out/needs_update` as a freshness signal rather than a failure by itself; decide whether CI should warn or block based on the repo workflow.

## Make It Easy For Users

Be proactive about the parts users should not have to remember:

- If `$graphify` or `/graphify` confusion appears, state the correct command for the current assistant.
- If the install is stale, update the platform skill before debugging the graph.
- If the project is huge, propose a focused first run and the `.graphifyignore` entries before spending tokens.
- After a successful build, summarize god nodes, communities, surprising links, and 2-3 suggested follow-up queries.
- If Graphify is useful but incomplete, say exactly where to use grep/source reads next.
- If the user wants recurring freshness, suggest hooks, CI `graphify extract`, or scheduled updates depending on whether this is code, docs, or mixed content.

## Troubleshooting

Common fixes:

- `/graphify` does nothing in Codex: use `$graphify`, or call `graphify ...` directly in the shell.
- The package imports fail in system `python3`: uv tool installs may isolate Graphify under the tool interpreter; use the `graphify` CLI or inspect the CLI shebang.
- Help output says the skill is stale: run `graphify install` and the relevant platform installer, such as `graphify codex install`.
- Docs, office files, video, or audio are skipped: reinstall with the relevant extras, for example `graphifyy[office,video]`.
- Cloud-drive projects are noisy: add `.graphifyignore`, scope to a subfolder, and avoid indexing sync metadata or generated exports.
- The graph is too large or expensive: build a graph for a smaller subtree first, then merge or expand when the initial map proves useful.
- Relationship answers feel shallow: inspect `GRAPH_REPORT.md`, then ask path/query/explain questions against named nodes from the report.

## Research Reference

Load `references/research-notes.md` when you need the current rationale behind this workflow, official v7 behavior, command inventory, or recent community usage notes.

# Graphify Research Notes

These notes are a compact reference for the skill. Refresh them against upstream docs when Graphify changes meaningfully.

## Official Sources Reviewed

- Repository: https://github.com/safishamsi/graphify
- v7 docs: https://github.com/safishamsi/graphify/tree/v7/docs
- v7 README: https://raw.githubusercontent.com/safishamsi/graphify/v7/README.md
- How it works: https://raw.githubusercontent.com/safishamsi/graphify/v7/docs/how-it-works.md
- Docker MCP SQLite runbook: https://raw.githubusercontent.com/safishamsi/graphify/v7/docs/docker-mcp-sqlite.md
- Changelog in v7 clone: `CHANGELOG.md`

## Current Model

Graphify builds a project graph in stages:

- Code structure is extracted locally with tree-sitter. This is the cheapest and safest pass.
- Video and audio use local faster-whisper transcription, seeded by important graph nodes, with transcript caching.
- Docs, papers, images, and similar semantic material use Claude subagents or supported backends, so they can cost API tokens.
- Leiden community detection provides clusters without embedding vectors.
- Edges carry confidence categories such as extracted, inferred, and ambiguous.
- Caches live under `graphify-out/cache/` and are keyed by content hash.

Important current commands and features:

- `graphify extract <path>` supports headless full extraction for CI and scripts.
- `graphify update <path>` refreshes an existing graph.
- `graphify update --force <path>` forces refresh when normal update is insufficient.
- `graphify query`, `graphify path`, and `graphify explain` are the primary graph traversal commands.
- `graphify tree` provides a tree viewer.
- `graphify hook install` installs merge-driver support for team workflows.
- `graphify codex install` adds Codex instructions/hooks.
- `GRAPHIFY_OUT` can relocate graph output.
- `.graphifyignore` uses gitignore-style patterns.

## Practical Community Signals From Reddit, Last 30 Days

Searches covered Graphify posts and comments in r/ClaudeAI, r/ClaudeCode, r/LocalLLaMA, and broader Reddit results. The visible pattern was strong interest in using Graphify as a relationship map for large codebases and mixed corpora, especially with Claude Code, Cursor, Codex, OpenCode, Gemini CLI, Aider, Copilot CLI, and VS Code.

Useful patterns surfaced by posts and comments:

- People value the graph most when it is used before context gathering, not after a normal file search.
- The highest-value output is often the project map: god nodes, communities, surprising connections, and suggested questions.
- Big codebases need scoped first runs and careful ignores; users asked for demos and examples of concrete results before trusting full-project runs.
- Recent releases added multi-platform support, tree viewing, MCP edge filtering, dynamic import handling, docs-only corpora, and headless extraction.
- The main failure mode reported by users is assistant noncompliance: Claude or another agent has Graphify installed but does not read the report, query the graph, or run updates unless explicitly instructed.

Skill implication: always make graph usage explicit. Check the graph, show what was checked, and use traversal commands for relationship questions.

Best-use examples from the discussion:

- Use Graphify as the first context map for a fresh chat, then use source reads for file-line evidence and behavioral failure analysis.
- Combine code with SQL schemas, dependency docs, meeting transcripts, project notes, or scraped official docs when the real question crosses repo boundaries.
- Keep long-running knowledge bases fresh with hooks or scheduled diffs instead of treating the graph as a one-time artifact.
- Use it to produce diagrams, project briefs, onboarding maps, and "how do I" internal skills after the graph has identified the important entities.
- Be cautious on massive legacy codebases where generic utility calls can dominate the graph; start with focused subsystems and tune ignores.

Representative Reddit links:

- https://www.reddit.com/r/ClaudeAI/comments/1t18eeh/i_built_graphify_26_days_450k_downloads_40k_stars/
- https://www.reddit.com/r/ClaudeAI/search/?q=graphify&restrict_sr=1&t=month
- https://www.reddit.com/search/?q=graphify%20safishamsi&t=month

## Version Notes From Changelog

Recent v7-era highlights:

- 0.7.5 added incremental `graphify extract`, semantic content-hash caching, deduplication, label preservation in hooks, and Gemini install fixes.
- 0.7.4 improved JSONC tsconfig aliases and Svelte dynamic imports.
- 0.7.3 introduced headless CI extraction and better docs-only corpus behavior.
- 0.7.0 focused on multi-developer workflows, deterministic Leiden clustering, content-only graph hashes, and merge-driver support.
- 0.6.9 added `GRAPHIFY_OUT`, VS Code instructions, and Codex hook checks.
- 0.6.8 improved `.graphifyignore` negation and Codex hook behavior.
- 0.6.7 added the tree viewer, MCP context filters, and dynamic import support.

## Agent Guidance

- For Codex, prefer `$graphify` in chat-facing guidance. Use shell `graphify` commands for direct execution.
- Do not call `graphify install --help` as a harmless probe in user projects; `graphify --help` and the doctor script are safer checks.
- If a generated Graphify skill is stale, update it with Graphify's installer instead of editing generated package output by hand.
- When making a durable custom skill, keep it independent from Graphify's generated platform skill so package updates do not overwrite local workflow guidance.

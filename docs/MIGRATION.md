# Migration To Codex Blog

Codex Blog is a runtime port, not a string rename. The package keeps the upstream blog workflows and delivery contract while changing the install, configuration, agent, and wrapper surfaces for Codex.

## What Changed

- Package name: `codex-blog`.
- Manifest: `.codex-plugin/plugin.json`.
- Agents: five `agents/blog-*.toml` profiles.
- Install root: `${CODEX_HOME:-$HOME/.codex}`.
- MCP setup: `config.toml` blocks under Codex configuration.
- Runtime artifacts: `output/` and `.codex-blog-cache/`.
- Headless execution: `scripts/run_blog_workflow.py` and `scripts/run_api_smoke_suite.py`.

Legacy upstream runtime paths are never written by this port. If old local data exists, migration helpers may read it only when explicitly documented.

## Source Facts

- Upstream source commit: `49842ea9e7b9a1f6f8a3774a3fcfb082ab6a7d25`.
- Upstream branch: `main`.
- Reference Codex port commit: `97c59bcdac3c9538bf0e3ae456c1e73aa387f85a`.
- Inspection date: `2026-06-20`.

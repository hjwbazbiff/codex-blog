# Codex Blog

Codex Blog is a Codex-native blog creation, review, localization, media, and publishing plugin. It ports the 30-skill upstream blog suite into Codex packaging with `.codex-plugin/plugin.json`, five TOML agent profiles, CODEX_HOME-aware installers, deterministic workflow wrappers, grouped requirements, and the preserved five-gate Blog Delivery Contract.

## Install

```bash
git clone https://github.com/hjwbazbiff/codex-blog.git
cd codex-blog
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}" ./install.sh
```

PowerShell:

```powershell
./install.ps1 -CodexHome "$env:USERPROFILE/.codex"
```

The installer copies skills to `$CODEX_HOME/skills`, agents to `$CODEX_HOME/agents`, plugin metadata to `$CODEX_HOME/plugins/codex-blog`, grouped requirement files to the installed blog skill, and bootstraps a skill-local virtual environment when Python is available.

## Quickstart

Use the skills directly in Codex or run deterministic wrappers from a shell:

```bash
python scripts/run_blog_workflow.py --skill blog-analyze tests/fixtures/sample-post.md --json
python scripts/run_blog_workflow.py --skill blog-brief "AI search content operations" --json
python scripts/run_blog_workflow.py --skill blog-preflight tests/fixtures/valid-draft --json
```

Wrappers write stable artifacts under `output/` and return documented exit codes: `0` success, `1` blocking findings, `2` invalid usage, `3` missing dependency or credential, `4` unexpected runtime failure.

## Skill Inventory

Codex Blog ships these 30 skills: `blog`, `blog-analyze`, `blog-audio`, `blog-audit`, `blog-brand`, `blog-brief`, `blog-calendar`, `blog-cannibalization`, `blog-chart`, `blog-cluster`, `blog-discourse`, `blog-factcheck`, `blog-flow`, `blog-geo`, `blog-google`, `blog-image`, `blog-locale-audit`, `blog-localize`, `blog-multilingual`, `blog-notebooklm`, `blog-outline`, `blog-persona`, `blog-repurpose`, `blog-rewrite`, `blog-schema`, `blog-seo-check`, `blog-strategy`, `blog-taxonomy`, `blog-translate`, and `blog-write`.

## Delivery Contract

The Blog Delivery Contract remains a five-gate publication guard:

1. Preflight capability discovery.
2. Render and format completeness.
3. Hero and visual verification.
4. Reviewer nonce and blocking decision.
5. Asset and link integrity.

Required artifacts are `.review-nonce`, `.iteration-count`, `review.md`, `capabilities.json`, and `preflight-report.json`. The reviewer must echo the nonce and end with `BLOCKING: YES|NO (reason)`.

## Providers And MCP

Core wrappers run without paid APIs. Optional Google, image, audio, and NotebookLM workflows require credentials and report structured `missing_credential` results when absent. Copy relevant examples from `.codex/config.example.toml` into `$CODEX_HOME/config.toml` and keep secrets in environment variables.

## Provenance

Source baseline: `AgriciDaniel/claude-blog` main at `49842ea9e7b9a1f6f8a3774a3fcfb082ab6a7d25`. Codex reference pattern: `AgriciDaniel/codex-seo` at `97c59bcdac3c9538bf0e3ae456c1e73aa387f85a`. See `CREDITS.md` and `docs/MIGRATION.md`.

## Verify

```bash
python -m pytest tests/
python scripts/verify_environment.py --json
python scripts/bootstrap_environment.py --json --json-output /tmp/codex-blog-bootstrap.json
python scripts/run_api_smoke_suite.py --json
```

#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
SKILL_DIR="$CODEX_HOME/skills"
AGENT_DIR="$CODEX_HOME/agents"
PLUGIN_DIR="$CODEX_HOME/plugins/codex-blog"
# Installed root script inventory: analyze_blog.py, blog_pipeline_utils.py, blog_preflight.py, blog_render.py, bootstrap_environment.py, cognitive_load.py, discourse_research.py, generate_hero.py, lint_prose.py, load_untrusted_root.py, run_api_smoke_suite.py, run_blog_workflow.py, sync_flow.py, verify_environment.py

rm -rf "$SKILL_DIR/blog" "$SKILL_DIR"/blog-* "$PLUGIN_DIR"
rm -f "$AGENT_DIR"/blog-*.toml

echo "Removed Codex Blog installed skills, agents, and plugin metadata from $CODEX_HOME."
echo "User outputs and caches were preserved."

#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
PLUGIN_NAME="codex-blog"
TEMP_DIR=""

make_temp_dir() {
  mktemp -d 2>/dev/null || mktemp -d -t codex-blog
}

main() {
  local script_dir skill_dir agent_dir plugin_dir runtime_dir bootstrap_json_file
  skill_dir="$CODEX_HOME/skills"
  agent_dir="$CODEX_HOME/agents"
  plugin_dir="$CODEX_HOME/plugins/$PLUGIN_NAME"
  runtime_dir="$CODEX_HOME/skills/blog/.venv"

  echo "Codex Blog installer"
  echo "CODEX_HOME=$CODEX_HOME"

  if [ -f "${BASH_SOURCE[0]:-}" ] && [ -d "$(dirname "${BASH_SOURCE[0]}")/skills/blog" ]; then
    script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  else
    TEMP_DIR="$(make_temp_dir)"
    trap 'rm -rf "$TEMP_DIR"' EXIT
    git clone --depth 1 https://github.com/hjwbazbiff/codex-blog.git "$TEMP_DIR/codex-blog" >/dev/null 2>&1
    script_dir="$TEMP_DIR/codex-blog"
  fi

  mkdir -p "$skill_dir" "$agent_dir" "$plugin_dir" "$CODEX_HOME/cache/codex-blog"
  rm -rf "$skill_dir/blog" "$skill_dir"/blog-* "$agent_dir"/blog-*.toml

  for skill_path in "$script_dir"/skills/*; do
    [ -d "$skill_path" ] || continue
    name="$(basename "$skill_path")"
    case "$name" in *[!a-z0-9-]*) echo "Skipping unexpected skill name: $name" >&2; continue ;; esac
    mkdir -p "$skill_dir/$name"
    cp -R "$skill_path/." "$skill_dir/$name/"
  done

  cp "$script_dir"/agents/blog-*.toml "$agent_dir/"
  cp -R "$script_dir/.codex-plugin" "$plugin_dir/"
  cp "$script_dir"/requirements*.txt "$skill_dir/blog/" 2>/dev/null || true
  mkdir -p "$skill_dir/blog/scripts"
  cp "$script_dir"/scripts/*.py "$skill_dir/blog/scripts/"
  chmod +x "$skill_dir/blog/scripts/"*.py 2>/dev/null || true

  if command -v python3 >/dev/null 2>&1; then
    [ -n "$TEMP_DIR" ] || TEMP_DIR="$(make_temp_dir)"
    bootstrap_json_file="$TEMP_DIR/bootstrap-result.json"
    python3 "$script_dir/scripts/bootstrap_environment.py" --venv "$runtime_dir" --json --json-output "$bootstrap_json_file" >/dev/null || true
    echo "Bootstrap summary: $bootstrap_json_file"
  else
    echo "python3 not found; install Python 3.11+ before running wrappers."
  fi

  echo "Installed Codex Blog skills to $skill_dir and agents to $agent_dir."
  echo "Restart Codex or open a new session to load the plugin."
}

main "$@"

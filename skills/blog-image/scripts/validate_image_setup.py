#!/usr/bin/env python3
"""Validate Codex Blog image MCP setup without printing secrets."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def codex_config_path() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "config.toml"


def validate(path: Path) -> dict:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    return {
        "ok": "[mcp_servers.nanobanana]" in text,
        "config_path": str(path),
        "server_declared": "[mcp_servers.nanobanana]" in text,
        "google_ai_api_key_env_present": bool(os.environ.get("GOOGLE_AI_API_KEY")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Codex Blog image setup")
    parser.add_argument("--config", help="Explicit config.toml path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.config).expanduser() if args.config else codex_config_path()
    result = validate(path)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Image MCP declared: {'YES' if result['server_declared'] else 'NO'}")
        print(f"Credential env present: {'YES' if result['google_ai_api_key_env_present'] else 'NO'}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

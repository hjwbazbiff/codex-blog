#!/usr/bin/env python3
"""Configure the nanobanana MCP server for Codex Blog image workflows."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

SERVER_BLOCK = """
[mcp_servers.nanobanana]
command = "npx"
args = ["-y", "@ycse/nanobanana-mcp"]
env_vars = ["GOOGLE_AI_API_KEY"]
startup_timeout_sec = 20
tool_timeout_sec = 120
"""


def codex_config_path() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "config.toml"


def configure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if "[mcp_servers.nanobanana]" not in existing:
        if existing and not existing.endswith("\n"):
            existing += "\n"
        existing += SERVER_BLOCK
        path.write_text(existing, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Configure Codex MCP for Blog Image")
    parser.add_argument("--config", help="Explicit config.toml path")
    args = parser.parse_args()
    path = Path(args.config).expanduser() if args.config else codex_config_path()
    configure(path)
    print(f"Configured nanobanana MCP in {path}")
    print("Set GOOGLE_AI_API_KEY in your environment before starting Codex.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

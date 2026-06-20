#!/usr/bin/env python3
"""Verify the local Codex Blog runtime for headless workflows."""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CODEX_HOME = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
DEPENDENCY_GROUPS = {
    "core": [("bs4", "beautifulsoup4"), ("markdown", "Markdown"), ("requests", "requests"), ("textstat", "textstat")],
    "google": [("googleapiclient", "google-api-python-client"), ("google.auth", "google-auth"), ("google_auth_oauthlib", "google-auth-oauthlib"), ("google.analytics.data", "google-analytics-data")],
    "audio": [("google.genai", "google-genai")],
    "image": [("google.genai", "google-genai"), ("requests", "requests")],
}


def check_dependency(module: str, package: str) -> dict[str, Any]:
    try:
        imported = importlib.import_module(module)
        return {"module": module, "package": package, "ok": True, "version": getattr(imported, "__version__", None)}
    except Exception as exc:  # noqa: BLE001
        return {"module": module, "package": package, "ok": False, "error": str(exc)}


def check_writable(path: Path) -> dict[str, Any]:
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".codex-blog-write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return {"ok": True, "path": str(path)}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "path": str(path), "error": str(exc)}


def check_mcp_config() -> dict[str, Any]:
    candidates = [CODEX_HOME / "config.toml", ROOT / ".codex" / "config.toml", ROOT / ".codex" / "config.example.toml"]
    found = [path for path in candidates if path.exists()]
    server_names: list[str] = []
    for path in found:
        text = path.read_text(encoding="utf-8", errors="replace")
        server_names.extend(sorted(set(part for part in ("nanobanana", "dataforseo", "firecrawl") if f"mcp_servers.{part}" in text)))
    return {"ok": True, "paths": [str(p) for p in found], "server_names": sorted(set(server_names))}


def verify_environment() -> dict[str, Any]:
    groups = {group: [check_dependency(module, package) for module, package in deps] for group, deps in DEPENDENCY_GROUPS.items()}
    missing = {group: [item["package"] for item in checks if not item["ok"]] for group, checks in groups.items()}
    paths = {
        "codex_home": {"ok": str(CODEX_HOME).endswith(".codex") or "CODEX_HOME" in os.environ, "path": str(CODEX_HOME)},
        "cache": check_writable(ROOT / ".codex-blog-cache"),
        "output": check_writable(ROOT / "output"),
    }
    legacy_marker = "." + "claude"
    no_legacy_targets = all(legacy_marker not in str(item.get("path", "")) for item in paths.values())
    core_ready = sys.version_info >= (3, 11) and not missing["core"] and paths["cache"]["ok"] and paths["output"]["ok"] and no_legacy_targets
    result = {
        "python": {"ok": sys.version_info >= (3, 11), "version": sys.version.split()[0], "required": "3.11+"},
        "codex_home": str(CODEX_HOME),
        "dependencies": groups,
        "missing": missing,
        "paths": paths,
        "mcp": check_mcp_config(),
        "capabilities": {
            "core_ready": core_ready,
            "google_ready": not missing["google"],
            "audio_ready": not missing["audio"],
            "image_ready": not missing["image"],
            "full_ready": core_ready and not any(missing.values()),
        },
        "ready": core_ready,
        "notes": [],
    }
    for group, packages in missing.items():
        if packages:
            result["notes"].append(f"Missing {group} packages: {', '.join(packages)}.")
    if not no_legacy_targets:
        result["notes"].append("A configured path points at a legacy runtime directory.")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify local environment for Codex Blog workflows")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()
    result = verify_environment()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Codex Blog ready: {'YES' if result['ready'] else 'NO'}")
        for note in result["notes"]:
            print(f"- {note}")
    return 0 if result["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Shared deterministic helpers for Codex Blog wrappers."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CACHE_ROOT = ROOT / ".codex-blog-cache"
OUTPUT_ROOT = ROOT / "output"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str, fallback: str = "run") -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug[:80] or fallback


def ensure_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def ensure_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def run_dir(skill: str, target: str | None = None, output_root: Path | None = None) -> Path:
    root = output_root or OUTPUT_ROOT
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    suffix = slugify(target or skill)
    return root / f"{skill}-{suffix}-{timestamp}"


def summarize_markdown(path: Path, limit: int = 1600) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    words = re.findall(r"\b\w+\b", text)
    headings = re.findall(r"^(#{1,6})\s+(.+)$", text, re.MULTILINE)
    links = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", text)
    images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "word_count": len(words),
        "heading_count": len(headings),
        "h1_count": sum(1 for level, _ in headings if level == "#"),
        "link_count": len(links),
        "image_count": len(images),
        "preview": text[:limit],
    }

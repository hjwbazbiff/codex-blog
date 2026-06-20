from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
AGENTS_DIR = ROOT / "agents"


def test_agents_are_toml_without_shell_grants():
    assert not list(AGENTS_DIR.glob("blog-*.md"))
    for path in AGENTS_DIR.glob("blog-*.toml"):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        assert "developer_instructions" in data
        assert "shell" not in data.get("tools", [])


def test_skill_names_are_unique_and_complete():
    names = []
    for path in SKILLS_DIR.glob("*/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^name:\s*(\S+)", text, re.MULTILINE)
        assert match, f"missing name in {path}"
        names.append(match.group(1))
    assert len(names) == len(set(names))


def test_google_and_notebooklm_helpers_keep_private_permissions():
    google_auth = ROOT / "skills" / "blog-google" / "scripts" / "google_auth.py"
    notebook_auth = ROOT / "skills" / "blog-notebooklm" / "scripts" / "auth_manager.py"
    for path in [google_auth, notebook_auth]:
        text = path.read_text(encoding="utf-8")
        assert "0o600" in text or "chmod" in text

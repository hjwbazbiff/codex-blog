from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "blog", "blog-analyze", "blog-audio", "blog-audit", "blog-brand", "blog-brief", "blog-calendar", "blog-cannibalization", "blog-chart", "blog-cluster", "blog-discourse", "blog-factcheck", "blog-flow", "blog-geo", "blog-google", "blog-image", "blog-locale-audit", "blog-localize", "blog-multilingual", "blog-notebooklm", "blog-outline", "blog-persona", "blog-repurpose", "blog-rewrite", "blog-schema", "blog-seo-check", "blog-strategy", "blog-taxonomy", "blog-translate", "blog-write",
}
EXPECTED_AGENTS = {"blog-researcher", "blog-writer", "blog-seo", "blog-reviewer", "blog-translator"}
STALE_TERMS = [
    "." + "claude",
    "." + "claude-plugin",
    "CLAUDE" + ".md",
    "Claude " + "Code",
    "claude " + "plugin",
    "claude " + "mcp",
    "Task " + "tool",
    "Web" + "Fetch",
    "Web" + "Search",
    "allowed" + "-tools",
]
STALE_RE = re.compile("|".join(re.escape(term) for term in STALE_TERMS))


def test_codex_manifest_contract():
    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "codex-blog"
    assert manifest["repository"] == "https://github.com/hjwbazbiff/codex-blog"
    assert manifest["skills"] == "./skills/"
    assert manifest["interface"]["displayName"] == "Codex Blog"
    assert manifest["interface"]["category"] == "Marketing"


def test_skills_inventory_and_frontmatter():
    skill_dirs = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    assert EXPECTED_SKILLS == skill_dirs
    for skill in EXPECTED_SKILLS:
        text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---\n")
        assert re.search(r"^name:\s*", text, re.MULTILINE)
        assert re.search(r"^description:\s*", text, re.MULTILINE)
        assert len(text.splitlines()) <= 500, f"{skill} exceeds progressive-disclosure limit"


def test_toml_agents_contract():
    agent_paths = sorted((ROOT / "agents").glob("blog-*.toml"))
    assert {p.stem for p in agent_paths} == EXPECTED_AGENTS
    assert not list((ROOT / "agents").glob("blog-*.md"))
    for path in agent_paths:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        assert data["name"] == path.stem
        assert data["description"]
        assert data["nickname_candidates"]
        assert data["developer_instructions"]
    reviewer = (ROOT / "agents" / "blog-reviewer.toml").read_text(encoding="utf-8")
    assert "Nonce:" in reviewer
    assert "BLOCKING: YES|NO" in reviewer
    assert "must not mutate files" in reviewer


def test_no_stale_runtime_references_in_active_files():
    ignored = {"plan.md", "context.md"}
    ignored_parts = {
        ".codex-blog-cache",
        ".codex-blog-venv",
        ".git",
        ".pytest_cache",
        "output",
    }
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ignored_parts.intersection(path.parts) or path.name in ignored:
            continue
        if path.suffix.lower() not in {".md", ".py", ".toml", ".yml", ".yaml", ".json", ".txt", ".cff", ".sh", ".ps1", ".svg", ".html"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if STALE_RE.search(text):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders


def test_wrapper_registry_covers_all_skills():
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import run_blog_workflow

    for skill in EXPECTED_SKILLS:
        assert skill in run_blog_workflow.SKILL_REGISTRY
    assert "blog-preflight" in run_blog_workflow.SKILL_REGISTRY

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_wrapper(*args: str):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "run_blog_workflow.py"), *args, "--json"], cwd=ROOT, capture_output=True, text=True, check=False)


def test_blog_analyze_wrapper_smoke():
    result = run_wrapper("--skill", "blog-analyze", "tests/fixtures/sample-post.md")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["skill"] == "blog-analyze"
    assert Path(payload["artifacts"]["summary_json"]).exists()


def test_blog_preflight_wrapper_smoke():
    result = run_wrapper("--skill", "blog-preflight", "tests/fixtures/valid-draft")
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["skill"] == "blog-preflight"
    assert "preflight_report" in payload["artifacts"]


def test_missing_credential_returns_stable_code():
    result = run_wrapper("--skill", "blog-image", "hero prompt")
    assert result.returncode in {0, 3}
    payload = json.loads(result.stdout)
    assert payload["status"] in {"missing_credential", "credential_detected_context_ready"}


def test_invalid_skill_returns_usage_code():
    result = run_wrapper("--skill", "not-a-skill", "x")
    assert result.returncode == 2
    payload = json.loads(result.stdout)
    assert payload["ok"] is False

#!/usr/bin/env python3
"""Run non-credentialed smoke checks for Codex Blog wrappers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SKILLS = ["blog-analyze", "blog-brief", "blog-write", "blog-translate", "blog-image", "blog-preflight"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Codex Blog API/headless smoke suite")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()
    sample = ROOT / "tests" / "fixtures" / "sample-post.md"
    draft = ROOT / "tests" / "fixtures" / "valid-draft"
    invocations = {
        "blog-analyze": [str(sample)],
        "blog-brief": ["content operations for AI search"],
        "blog-write": ["content operations for AI search"],
        "blog-translate": [str(sample)],
        "blog-image": ["editorial hero for content operations"],
        "blog-preflight": [str(draft)],
    }
    results: list[dict[str, Any]] = []
    ok = True
    for skill in DEFAULT_SKILLS:
        cmd = [sys.executable, str(ROOT / "scripts" / "run_blog_workflow.py"), "--skill", skill, *invocations[skill], "--json"]
        completed = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        allowed = {0}
        if skill == "blog-image":
            allowed.add(3)
        if skill == "blog-preflight":
            allowed.add(1)
        ok = ok and completed.returncode in allowed
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = {"stdout": completed.stdout, "stderr": completed.stderr}
        results.append({"skill": skill, "returncode": completed.returncode, "accepted": completed.returncode in allowed, "payload": payload})
    suite = {"ok": ok, "skills": DEFAULT_SKILLS, "results": results}
    if args.json:
        print(json.dumps(suite, indent=2))
    else:
        for item in results:
            print(f"{item['skill']}: {item['returncode']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

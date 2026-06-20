#!/usr/bin/env python3
"""Run a Codex Blog skill deterministically and write standard artifacts."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from blog_pipeline_utils import ensure_json, ensure_text, now_iso, run_dir, summarize_markdown
from verify_environment import verify_environment

ROOT = Path(__file__).resolve().parent.parent
EXIT_SUCCESS = 0
EXIT_BLOCKING = 1
EXIT_USAGE = 2
EXIT_MISSING = 3
EXIT_FAILURE = 4

SKILL_REGISTRY: dict[str, dict[str, Any]] = {
    "blog": {"kind": "manual", "input": "topic"},
    "blog-analyze": {"kind": "analyze", "input": "file"},
    "blog-audio": {"kind": "optional_provider", "provider": "GOOGLE_AI_API_KEY", "input": "file_or_text"},
    "blog-audit": {"kind": "audit", "input": "directory"},
    "blog-brand": {"kind": "manual", "input": "topic"},
    "blog-brief": {"kind": "planning", "input": "topic"},
    "blog-calendar": {"kind": "planning", "input": "topic"},
    "blog-cannibalization": {"kind": "analysis_context", "input": "directory"},
    "blog-chart": {"kind": "planning", "input": "data_or_topic"},
    "blog-cluster": {"kind": "planning", "input": "topic"},
    "blog-discourse": {"kind": "research_context", "input": "topic"},
    "blog-factcheck": {"kind": "file_context", "input": "file"},
    "blog-flow": {"kind": "planning", "input": "stage_or_topic"},
    "blog-geo": {"kind": "file_context", "input": "file"},
    "blog-google": {"kind": "optional_provider", "provider": "GOOGLE_APPLICATION_CREDENTIALS", "input": "url_or_property"},
    "blog-image": {"kind": "optional_provider", "provider": "GOOGLE_AI_API_KEY", "input": "prompt"},
    "blog-locale-audit": {"kind": "analysis_context", "input": "directory"},
    "blog-localize": {"kind": "file_context", "input": "file"},
    "blog-multilingual": {"kind": "manual", "input": "topic"},
    "blog-notebooklm": {"kind": "optional_provider", "provider": "NOTEBOOKLM_SESSION", "input": "question"},
    "blog-outline": {"kind": "planning", "input": "topic"},
    "blog-persona": {"kind": "planning", "input": "persona"},
    "blog-repurpose": {"kind": "file_context", "input": "file"},
    "blog-rewrite": {"kind": "file_context", "input": "file"},
    "blog-schema": {"kind": "file_context", "input": "file"},
    "blog-seo-check": {"kind": "file_context", "input": "file"},
    "blog-strategy": {"kind": "planning", "input": "topic"},
    "blog-taxonomy": {"kind": "analysis_context", "input": "directory"},
    "blog-translate": {"kind": "file_context", "input": "file"},
    "blog-write": {"kind": "manual", "input": "topic"},
    "blog-preflight": {"kind": "preflight", "input": "draft_directory"},
}


def _target_arg(args: argparse.Namespace) -> str | None:
    return " ".join(args.target).strip() if args.target else None


def _write_common(skill: str, target: str, status: str, output_dir: Path, result: dict[str, Any], report: str, exit_code: int = EXIT_SUCCESS) -> tuple[int, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ensure_json(output_dir / "SUMMARY.json", result)
    ensure_json(output_dir / "environment-verification.json", verify_environment())
    ensure_text(output_dir / "WORKFLOW.md", report)
    payload = {"ok": exit_code == 0, "skill": skill, "target": target, "status": status, "exit_code": exit_code, "output_dir": str(output_dir), "artifacts": {"summary_json": str(output_dir / "SUMMARY.json"), "environment_verification": str(output_dir / "environment-verification.json"), "workflow_report": str(output_dir / "WORKFLOW.md")}, "result": result}
    return exit_code, payload


def run_analyze(skill: str, target: str, output_root: Path | None) -> tuple[int, dict[str, Any]]:
    path = Path(target)
    if not path.is_file():
        return EXIT_USAGE, {"ok": False, "skill": skill, "target": target, "error": "Expected an existing file path."}
    output_dir = run_dir(skill, path.stem, output_root)
    cmd = [sys.executable, str(ROOT / "scripts" / "analyze_blog.py"), str(path)]
    completed = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    try:
        analysis = json.loads(completed.stdout)
    except json.JSONDecodeError:
        analysis = {"stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode}
    result = {"cache_type": skill, "analyzed_at": now_iso(), "source": summarize_markdown(path), "analysis": analysis, "command_returncode": completed.returncode}
    report = f"# {skill} Workflow\n\nAnalyzed `{path}` with `scripts/analyze_blog.py`.\n"
    exit_code = EXIT_SUCCESS if completed.returncode == 0 else EXIT_BLOCKING
    return _write_common(skill, target, "completed" if exit_code == 0 else "blocking_findings", output_dir, result, report, exit_code)


def run_preflight(skill: str, target: str, output_root: Path | None) -> tuple[int, dict[str, Any]]:
    draft = Path(target)
    if not draft.is_dir():
        return EXIT_USAGE, {"ok": False, "skill": skill, "target": target, "error": "Expected an existing draft directory."}
    output_dir = run_dir(skill, draft.name, output_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(ROOT / "scripts" / "blog_preflight.py"), "--draft", str(draft), "--reset-iterations", "--json"]
    completed = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    try:
        preflight = json.loads(completed.stdout)
    except json.JSONDecodeError:
        preflight = {"stdout": completed.stdout, "stderr": completed.stderr, "returncode": completed.returncode}
    if (draft / "preflight-report.json").exists():
        shutil.copy2(draft / "preflight-report.json", output_dir / "preflight-report.json")
    result = {"cache_type": skill, "analyzed_at": now_iso(), "draft": str(draft), "preflight": preflight, "command_returncode": completed.returncode}
    report = f"# Blog Preflight Workflow\n\nDraft: `{draft}`\n\nReturn code: {completed.returncode}\n"
    exit_code = EXIT_SUCCESS if completed.returncode == 0 else EXIT_BLOCKING
    code, payload = _write_common(skill, target, "completed" if exit_code == 0 else "blocking_findings", output_dir, result, report, exit_code)
    if (output_dir / "preflight-report.json").exists():
        payload["artifacts"]["preflight_report"] = str(output_dir / "preflight-report.json")
    return code, payload


def run_context(skill: str, target: str, output_root: Path | None, status: str = "manual_codex_reasoning_required") -> tuple[int, dict[str, Any]]:
    meta = SKILL_REGISTRY[skill]
    output_dir = run_dir(skill, target, output_root)
    source: dict[str, Any] | None = None
    maybe_path = Path(target)
    if maybe_path.is_file():
        source = summarize_markdown(maybe_path)
    elif maybe_path.is_dir():
        source = {"path": str(maybe_path), "files": sorted(str(p.relative_to(maybe_path)) for p in maybe_path.rglob("*") if p.is_file())[:200]}
    result = {"cache_type": skill, "analyzed_at": now_iso(), "status": status, "input_contract": meta, "source": source, "limitations": ["This deterministic wrapper prepares context and artifacts. Final editorial judgment must happen in Codex."], "next_steps": [f"Invoke `${skill}` in Codex with the recorded context."]}
    report = f"# {skill} Workflow\n\nStatus: `{status}`\n\nInput: `{target}`\n\nThis wrapper created deterministic context artifacts and did not fabricate external API data.\n"
    return _write_common(skill, target, status, output_dir, result, report, EXIT_SUCCESS)


def run_optional(skill: str, target: str, output_root: Path | None) -> tuple[int, dict[str, Any]]:
    meta = SKILL_REGISTRY[skill]
    provider = meta.get("provider")
    if provider and not os.environ.get(provider):
        output_dir = run_dir(skill, target, output_root)
        result = {"cache_type": skill, "analyzed_at": now_iso(), "status": "missing_credential", "missing": [provider], "input_contract": meta, "limitations": ["Credentialed external APIs were not called."]}
        report = f"# {skill} Setup Required\n\nMissing credential: `{provider}`.\n"
        return _write_common(skill, target, "missing_credential", output_dir, result, report, EXIT_MISSING)
    return run_context(skill, target, output_root, status="credential_detected_context_ready")


def run_skill(skill: str, target: str | None, output_root: Path | None = None) -> tuple[int, dict[str, Any]]:
    if skill not in SKILL_REGISTRY:
        return EXIT_USAGE, {"ok": False, "skill": skill, "error": f"Unsupported skill: {skill}", "supported_skills": sorted(SKILL_REGISTRY)}
    if not target:
        return EXIT_USAGE, {"ok": False, "skill": skill, "error": "Missing required target/input."}
    kind = SKILL_REGISTRY[skill]["kind"]
    if kind == "analyze":
        return run_analyze(skill, target, output_root)
    if kind == "preflight":
        return run_preflight(skill, target, output_root)
    if kind == "optional_provider":
        return run_optional(skill, target, output_root)
    return run_context(skill, target, output_root)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Codex Blog workflow deterministically")
    parser.add_argument("--skill", required=True, help="Skill name, such as blog-analyze or blog-write")
    parser.add_argument("target", nargs="*", help="File, directory, topic, prompt, or provider input")
    parser.add_argument("--output-root", help="Optional root directory for artifacts")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()
    output_root = Path(args.output_root).resolve() if args.output_root else None
    try:
        code, payload = run_skill(args.skill, _target_arg(args), output_root)
    except Exception as exc:  # noqa: BLE001
        code = EXIT_FAILURE
        payload = {"ok": False, "skill": args.skill, "target": _target_arg(args), "error": str(exc), "exit_code": code}
    if args.json:
        print(json.dumps(payload, indent=2))
    elif payload.get("ok"):
        print(f"{payload['skill']}: {payload['status']} -> {payload['output_dir']}")
    else:
        print(payload.get("error", payload.get("status", "failed")), file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())

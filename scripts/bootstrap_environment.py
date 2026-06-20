#!/usr/bin/env python3
"""Bootstrap a Codex Blog runtime for headless CLI/API execution."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import traceback
import venv
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_VENV = ROOT / ".codex-blog-venv"
OUTPUT_LIMIT = 12000
CORE_REQUIREMENTS = ROOT / "requirements-core.txt"
OPTIONAL_REQUIREMENTS = [("google", ROOT / "requirements-google.txt"), ("audio", ROOT / "requirements-audio.txt"), ("image", ROOT / "requirements-image.txt")]


def truncate(text: str, limit: int = OUTPUT_LIMIT) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    half = limit // 2
    return f"{text[:half]}\n...[truncated]...\n{text[-half:]}", True


def run_command(cmd: list[str], cwd: Path | None = None) -> dict[str, Any]:
    completed = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True, check=False)
    stdout, stdout_truncated = truncate(completed.stdout)
    stderr, stderr_truncated = truncate(completed.stderr)
    return {"cmd": cmd, "returncode": completed.returncode, "stdout": stdout, "stderr": stderr, "stdout_truncated": stdout_truncated, "stderr_truncated": stderr_truncated, "ok": completed.returncode == 0}


def python_in_venv(venv_dir: Path) -> Path:
    if sys.platform == "win32":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def install_requirements(python: Path, path: Path, group: str, required: bool) -> dict[str, Any]:
    step = run_command([str(python), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(path)])
    step["group"] = group
    step["required"] = required
    return step


def parse_json_stdout(step: dict[str, Any]) -> dict[str, Any] | None:
    if not step["stdout"].strip():
        return None
    try:
        return json.loads(step["stdout"])
    except json.JSONDecodeError:
        return None


def bootstrap_environment(venv_dir: Path | None = None, install_optional: bool = True) -> dict[str, Any]:
    venv_dir = venv_dir or DEFAULT_VENV
    created = False
    if not venv_dir.exists():
        venv.EnvBuilder(with_pip=True).create(venv_dir)
        created = True
    python = python_in_venv(venv_dir)
    if not python.exists():
        raise RuntimeError(f"Virtual environment Python not found: {python}")
    steps: list[dict[str, Any]] = []
    pip_step = run_command([str(python), "-m", "pip", "install", "--disable-pip-version-check", "--upgrade", "pip"])
    pip_step.update({"group": "pip", "required": True})
    steps.append(pip_step)
    steps.append(install_requirements(python, CORE_REQUIREMENTS if CORE_REQUIREMENTS.exists() else ROOT / "requirements.txt", "core", True))
    if install_optional and steps[-1]["ok"]:
        for group, path in OPTIONAL_REQUIREMENTS:
            if path.exists():
                steps.append(install_requirements(python, path, group, False))
    verify_step = run_command([str(python), str(ROOT / "scripts" / "verify_environment.py"), "--json"])
    verify_step.update({"group": "verification", "required": True})
    steps.append(verify_step)
    verification = parse_json_stdout(verify_step)
    optional_failed = [step.get("group", "unknown") for step in steps if not step.get("required") and not step["ok"]]
    ok = all(step["ok"] for step in steps if step.get("required")) and bool(verification and verification.get("ready"))
    return {"ok": ok, "full_ready": bool(verification and verification.get("capabilities", {}).get("full_ready")), "created_venv": created, "venv": str(venv_dir), "python": str(python), "optional_failed_groups": optional_failed, "steps": steps, "verification": verification}


def write_json_output(path: str | None, payload: dict[str, Any]) -> None:
    if not path:
        return
    out = Path(path).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def exception_payload(exc: BaseException) -> dict[str, Any]:
    return {"ok": False, "full_ready": False, "created_venv": False, "venv": "", "python": "", "optional_failed_groups": [], "steps": [], "verification": None, "error": str(exc), "exception_type": type(exc).__name__, "traceback": traceback.format_exc()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Bootstrap a Codex Blog runtime environment")
    parser.add_argument("--venv", help="Virtual environment directory")
    parser.add_argument("--skip-optional", action="store_true", help="Install only core requirements")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--json-output", help="Write JSON payload to this file")
    args = parser.parse_args()
    try:
        result = bootstrap_environment(Path(args.venv) if args.venv else None, install_optional=not args.skip_optional)
    except Exception as exc:  # pragma: no cover
        result = exception_payload(exc)
    if args.json:
        write_json_output(args.json_output, result)
        print(json.dumps(result, indent=2))
    else:
        print(f"OK: {'YES' if result['ok'] else 'NO'}")
        print(f"Venv: {result.get('venv', '')}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

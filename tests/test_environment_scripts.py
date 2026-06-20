from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_verify_environment_shape():
    sys.path.insert(0, str(ROOT / "scripts"))
    from verify_environment import verify_environment
    result = verify_environment()
    assert "python" in result
    assert "dependencies" in result
    assert "capabilities" in result
    assert "mcp" in result
    assert ("." + "claude") not in str(result)


def test_bootstrap_cli_writes_json_output(monkeypatch, tmp_path, capsys):
    sys.path.insert(0, str(ROOT / "scripts"))
    import bootstrap_environment
    payload = {"ok": True, "full_ready": False, "created_venv": False, "venv": "v", "python": "p", "optional_failed_groups": [], "steps": [], "verification": {"ready": True}}
    out = tmp_path / "bootstrap.json"
    monkeypatch.setattr(bootstrap_environment, "bootstrap_environment", lambda *args, **kwargs: payload)
    monkeypatch.setattr(sys, "argv", ["bootstrap_environment.py", "--json", "--json-output", str(out)])
    assert bootstrap_environment.main() == 0
    assert json.loads(out.read_text(encoding="utf-8")) == payload
    assert json.loads(capsys.readouterr().out) == payload


def test_verify_cli_survives_without_site_packages():
    completed = subprocess.run([sys.executable, "-S", str(ROOT / "scripts" / "verify_environment.py"), "--json"], cwd=ROOT, capture_output=True, text=True, check=False)
    assert completed.returncode in {0, 1}
    result = json.loads(completed.stdout)
    assert "dependencies" in result

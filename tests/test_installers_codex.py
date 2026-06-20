from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_installers_use_codex_home_and_not_legacy_paths():
    for name in ["install.sh", "uninstall.sh", "install.ps1", "uninstall.ps1"]:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "CODEX_HOME" in text or "CodexHome" in text
        assert ("." + "claude") not in text


def test_powershell_installer_builds_runtime_dir_without_prompting():
    text = (ROOT / "install.ps1").read_text(encoding="utf-8")
    assert '$RuntimeDir = Join-Path (Join-Path $SkillDir "blog") ".venv"' in text
    assert "Join-Path (Join-Path (Join-Path" not in text


def test_temp_codex_home_install_and_uninstall(tmp_path):
    env = os.environ.copy()
    env["CODEX_HOME"] = str(tmp_path / ".codex")
    install = subprocess.run([str(ROOT / "install.sh")], cwd=ROOT, env=env, capture_output=True, text=True, check=False)
    assert install.returncode == 0, install.stdout + install.stderr
    codex_home = Path(env["CODEX_HOME"])
    assert (codex_home / "skills" / "blog" / "SKILL.md").exists()
    assert len(list((codex_home / "skills").glob("blog*/SKILL.md"))) == 30
    assert len(list((codex_home / "agents").glob("blog-*.toml"))) == 5
    assert (codex_home / "plugins" / "codex-blog" / ".codex-plugin" / "plugin.json").exists()
    uninstall = subprocess.run([str(ROOT / "uninstall.sh")], cwd=ROOT, env=env, capture_output=True, text=True, check=False)
    assert uninstall.returncode == 0, uninstall.stdout + uninstall.stderr
    assert not (codex_home / "skills" / "blog").exists()

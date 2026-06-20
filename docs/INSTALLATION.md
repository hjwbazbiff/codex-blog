# Installation

Unix:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}" ./install.sh
```

PowerShell:

```powershell
./install.ps1 -CodexHome "$env:USERPROFILE/.codex"
```

Installed inventory:

- `$CODEX_HOME/skills/blog` and `$CODEX_HOME/skills/blog-*`.
- `$CODEX_HOME/agents/blog-*.toml`.
- `$CODEX_HOME/plugins/codex-blog/.codex-plugin/plugin.json`.
- Grouped requirements copied into the installed blog skill.

Uninstall:

```bash
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}" ./uninstall.sh
```

PowerShell:

```powershell
./uninstall.ps1 -CodexHome "$env:USERPROFILE/.codex"
```

Uninstall removes installed Codex Blog skills, agents, and plugin metadata. User outputs and caches are preserved.

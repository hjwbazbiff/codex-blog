param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" })
)

$ErrorActionPreference = "Stop"
$SkillDir = Join-Path $CodexHome "skills"
$AgentDir = Join-Path $CodexHome "agents"
$PluginDir = Join-Path (Join-Path $CodexHome "plugins") "codex-blog"
$RuntimeDir = Join-Path (Join-Path $SkillDir "blog") ".venv"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Codex Blog installer"
Write-Host "CODEX_HOME=$CodexHome"

New-Item -ItemType Directory -Force -Path $SkillDir, $AgentDir, $PluginDir | Out-Null
Get-ChildItem -Path $SkillDir -Directory -Filter "blog*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Path $AgentDir -Filter "blog-*.toml" -ErrorAction SilentlyContinue | Remove-Item -Force

Get-ChildItem -Path (Join-Path $ScriptDir "skills") -Directory | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path $SkillDir $_.Name) -Recurse -Force
}
Copy-Item -Path (Join-Path $ScriptDir "agents/blog-*.toml") -Destination $AgentDir -Force
Copy-Item -Path (Join-Path $ScriptDir ".codex-plugin") -Destination $PluginDir -Recurse -Force
Copy-Item -Path (Join-Path $ScriptDir "requirements*.txt") -Destination (Join-Path $SkillDir "blog") -Force
New-Item -ItemType Directory -Force -Path (Join-Path (Join-Path $SkillDir "blog") "scripts") | Out-Null
Copy-Item -Path (Join-Path $ScriptDir "scripts/*.py") -Destination (Join-Path (Join-Path $SkillDir "blog") "scripts") -Force

$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    $tempDir = New-Item -ItemType Directory -Force -Path (Join-Path ([System.IO.Path]::GetTempPath()) ("codex-blog-" + [guid]::NewGuid().ToString()))
    $bootstrapJsonPath = Join-Path $tempDir "bootstrap-result.json"
    & $python.Source (Join-Path $ScriptDir "scripts/bootstrap_environment.py") --venv $RuntimeDir --json --json-output $bootstrapJsonPath | Out-Null
    Write-Host "Bootstrap summary: $bootstrapJsonPath"
}

Write-Host "Installed Codex Blog skills to $SkillDir and agents to $AgentDir."
Write-Host "Restart Codex or open a new session to load the plugin."

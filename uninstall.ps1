param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" })
)

$SkillDir = Join-Path $CodexHome "skills"
$AgentDir = Join-Path $CodexHome "agents"
$PluginDir = Join-Path (Join-Path $CodexHome "plugins") "codex-blog"
# Installed root script inventory: analyze_blog.py, blog_pipeline_utils.py, blog_preflight.py, blog_render.py, bootstrap_environment.py, cognitive_load.py, discourse_research.py, generate_hero.py, lint_prose.py, load_untrusted_root.py, run_api_smoke_suite.py, run_blog_workflow.py, sync_flow.py, verify_environment.py

Get-ChildItem -Path $SkillDir -Directory -Filter "blog*" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Path $AgentDir -Filter "blog-*.toml" -ErrorAction SilentlyContinue | Remove-Item -Force
if (Test-Path $PluginDir) { Remove-Item -Recurse -Force $PluginDir }

Write-Host "Removed Codex Blog installed skills, agents, and plugin metadata from $CodexHome."
Write-Host "User outputs and caches were preserved."

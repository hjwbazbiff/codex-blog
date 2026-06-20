# Architecture

```text
codex-blog/
  .codex-plugin/plugin.json
  AGENTS.md
  agents/blog-*.toml
  skills/*/SKILL.md
  scripts/bootstrap_environment.py
  scripts/verify_environment.py
  scripts/run_blog_workflow.py
  scripts/run_api_smoke_suite.py
  tests/
```

The `blog` skill is the orchestrator. Specialist skills handle analysis, writing, planning, localization, media, Google integrations, discourse research, schema, taxonomy, and delivery checks.

The main `blog` skill has 21 references in `skills/blog/references/`. Load references only when the selected workflow needs them.

The five-gate Blog Delivery Contract is implemented by root scripts and the reviewer TOML profile. It must fail closed when required artifacts are missing.

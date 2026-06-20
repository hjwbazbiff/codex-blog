# Contributing

Run tests before opening changes:

```bash
python -m pytest tests/
python scripts/verify_environment.py --json
```

Keep changes Codex-native:

- Manifest changes belong in `.codex-plugin/plugin.json`.
- Agent profiles are TOML files under `agents/`.
- Skills must have `name` and `description` frontmatter.
- Wrapper-visible skills need entries in `scripts/run_blog_workflow.py`.
- Do not commit secrets or generated output.
- Preserve the five-gate Blog Delivery Contract.

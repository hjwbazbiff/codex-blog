# Development

Run the focused Codex port checks before shipping:

```bash
python -m pytest tests/
python scripts/verify_environment.py --json
python scripts/run_blog_workflow.py --skill blog-analyze tests/fixtures/sample-post.md --json
python scripts/run_blog_workflow.py --skill blog-preflight tests/fixtures/valid-draft --json
```

## Skill Rules

- Keep each `SKILL.md` focused and below 500 lines unless a test documents an exception.
- Move long operational detail to `references/`.
- Every skill needs `name` and `description` frontmatter.
- User-invokable workflows need a registry entry in `scripts/run_blog_workflow.py`.

## Release Process

1. Run local tests and smoke checks.
2. Run a temporary `CODEX_HOME` install and uninstall smoke.
3. Push main to `hjwbazbiff/codex-blog`.
4. Wait for CI.
5. Tag the version from `.codex-plugin/plugin.json`.
6. Publish a GitHub release with source commit, port summary, install instructions, known optional-provider limits, and verification status.

# Command Reference

## Command Overview

| Command | Skill | Purpose |
| --- | --- | --- |
| `write` | blog-write | Draft a new post |
| `rewrite` | blog-rewrite | Improve an existing post |
| `analyze` | blog-analyze | Score a post |
| `brief` | blog-brief | Build a content brief |
| `calendar` | blog-calendar | Plan an editorial calendar |
| `cannibalization` | blog-cannibalization | Find overlapping search targets |
| `strategy` | blog-strategy | Create content strategy |
| `outline` | blog-outline | Build a SERP-informed outline |
| `seo-check` | blog-seo-check | Validate post SEO |
| `schema` | blog-schema | Generate JSON-LD |
| `repurpose` | blog-repurpose | Adapt content for other channels |
| `geo` | blog-geo | Audit AI citation readiness |
| `image` | blog-image | Generate or edit images |
| `audit` | blog-audit | Assess a blog directory |
| `factcheck` | blog-factcheck | Verify claims and citations |
| `persona` | blog-persona | Manage writing personas |
| `brand` | blog-brand | Create durable brand context |
| `discourse` | blog-discourse | Research recent public discussion |
| `taxonomy` | blog-taxonomy | Manage tags and categories |
| `notebooklm` | blog-notebooklm | Query NotebookLM sources |
| `audio` | blog-audio | Generate narration |
| `google` | blog-google | Use Google data providers |
| `cluster` | blog-cluster | Plan or execute topic clusters |
| `multilingual` | blog-multilingual | Create multilingual packages |
| `translate` | blog-translate | Translate posts |
| `localize` | blog-localize | Adapt translated posts |
| `locale-audit` | blog-locale-audit | Audit multilingual coverage |
| `flow` | blog-flow | Apply FLOW prompts |
| `update` | blog-rewrite | Refresh stale content |
---

Use deterministic wrappers for headless contexts:

```bash
python scripts/run_blog_workflow.py --skill blog-analyze tests/fixtures/sample-post.md --json
python scripts/run_blog_workflow.py --skill blog-outline "topic" --json
```

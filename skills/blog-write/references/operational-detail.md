# Blog Write Operational Detail

</figure>
```

#### 5k. Video Embedding
Embed YouTube videos using srcdoc lazy-loading pattern from `skills/blog/references/video-embeds.md`.
Include aria-label, noscript fallback for AI crawlers. Place after relevant H2, 500+ words apart.

#### 5l. Citation Format
Inline attribution (always):
```markdown
Organic CTR declined 61% with AI Overviews ([Seer Interactive](https://www.seerinteractive.com/), 2025).
```

#### 5m. FAQ Section
Add 3-5 FAQ items with 40-60 word answers. Each answer must contain a statistic.

For MDX with FAQSchema component:
```mdx
<FAQSchema faqs={[
  { question: "Question?", answer: "40-60 word answer with statistic and source." },
]} />
```

For standard markdown:
```markdown
## Frequently Asked Questions

### Question text here?

Answer with statistic and source attribution (40-60 words).
```

#### 5n. Internal Linking
- 5-10 internal links per 2,000-word post
- Link to relevant existing content naturally
- Use descriptive anchor text (not "click here")

### Phase 6: Quality Check

Before delivering, verify:

#### Structure and Content
1. Every H2 opens with a statistic + source
2. No paragraph exceeds 150 words
3. All statistics have named tier 1-3 sources
4. 2-4 charts with type diversity
5. 3-5 inline images with descriptive alt text
6. Cover image present in frontmatter (coverImage + ogImage)
7. FAQ section present with 3-5 items
8. Heading hierarchy is clean (H1 -> H2 -> H3)
9. Meta description is 150-160 chars with a stat

#### New Element Verification
10. TL;DR box present after introduction (40-60 words, contains statistic + source)
11. At least 2-3 information gain markers (`[ORIGINAL DATA]`, `[PERSONAL EXPERIENCE]`, or `[UNIQUE INSIGHT]`)
12. Citation capsules present in major H2 sections (40-60 words, self-contained, quotable)
13. Internal linking zones marked in introduction, H2 sections, FAQ, and conclusion
14. No AI-detectable phrases from banned list (see `agents/blog-writer.md`)

#### Burstiness and Naturalness Check
15. **Sentence length variance** - Verify a mix of short (8-word) and long (25-word) sentences. Uniform sentence length signals AI authorship.
16. **Banned AI phrase scan** - Check for and remove:
    - "in today's digital landscape", "it's important to note", "dive into"
    - "game-changer", "navigate the landscape", "revolutionize", "seamlessly"
    - "cutting-edge", "harness the power of", "leverage" (as verb)
    - "delve", "crucial", "elevate", "foster", "landscape" (overused)
    - "multifaceted", "robust", "tapestry", "embark"
    - Full list in `agents/blog-writer.md`
17. **Contractions** - Verify natural use of contractions ("it's", "we've", "don't", "isn't"). Formal AI prose avoids contractions; natural writing uses them.
18. **Rhetorical questions** - Verify at least one rhetorical question every 200-300 words to break up declarative patterns.
19. **YouTube videos** - 2-3 embeds with lazy loading, aria-labels, and noscript fallback (see `skills/blog/references/video-embeds.md`)

### Phase 6.5: Delivery Contract Enforcement (v1.9.0)

Before Phase 7, run the 5-gate delivery contract per `skills/blog/references/blog-delivery-contract.md`. The user is never the first reviewer; the gates are.

Steps:

1. **Capability discovery + hero**: run `python scripts/blog_preflight.py --draft <folder> --gate 1` to enumerate available paths. If `nanobanana-mcp` is loaded, generate the hero via the MCP tool. Otherwise run `python scripts/generate_hero.py --topic "<title>" --tags "<tags>" --out <folder>` (uses the Gemini, Unsplash, Pexels, Pixabay, Openverse ladder).

2. **Format completeness**: render the canonical `.md` to `.html` and `.pdf` via `python scripts/blog_render.py --md <slug>.md --out-dir <folder>`. All three artifacts plus `hero.<ext>` must end up in the draft folder.

3. **Content review (blocking)**: dispatch the `blog-reviewer` agent (Codex subagent workflow) against the rendered `.html`. The agent emits its scorecard to `<folder>/review.md` ending with `BLOCKING: true|false (reason)`. Threshold: overall score 90/100 or higher AND zero P0 issues per `editorial-heuristics.md`.

4. **Visual + asset gates**: run `python scripts/blog_preflight.py --draft <folder> --strict`. This runs Gate 3 (visual verification via patchright at 3 viewport widths), Gate 4 (reads review.md BLOCKING line), and Gate 5 (asset + link integrity). Exit 0 = ship; exit 1 = block.

5. **Iteration**: on any block, capture the failure diagnostic from `<folder>/preflight-report.json`, re-dispatch the blog-writer agent with the diagnostic as input, and re-run from step 1. Maximum 3 iterations. On the 3rd failure, STOP and present the failure diagnostic instead of the draft.

The orchestrator holds the loop counter; this sub-skill never loops itself.

### Phase 7: Delivery

Present the completed article ONLY after Phase 6.5 returns all gates passing. Include the screenshots from `<folder>/preview/*.png` in the summary so the user can see what they are getting before reading the prose.

Summary template:

```
## Blog Post Complete: [Title]

### Template Used
- [Template name] (or "generic outline - no template matched")

### Statistics
- [N] sourced statistics from tier 1-3 sources
- [N] unique sources cited

### Visual Elements
- Cover image: [source - Pixabay/Unsplash/Pexels or generated SVG]
- [N] inline images (Pixabay/Unsplash/Pexels)
- [N] SVG charts (types: bar, lollipop, donut, line)
- [N] YouTube video embeds (titles: ...)

### Dual-Optimization Elements
- TL;DR box: present (N words)
- Information gain markers: [N] ([types used])
- Citation capsules: [N] across H2 sections
- Internal linking zones: [N] marked

### Structure
- [N] H2 sections with answer-first formatting
- [N] FAQ items with schema
- Word count: ~[N] words
- Estimated reading time: [N] min

### Naturalness
- Sentence length variance: [pass/fail]
- AI phrase scan: [pass/fail]
- Contractions used: [yes/no]
- Rhetorical questions: [N] (target: 1 per 200-300 words)

### Next Steps
- Review and customize for your brand voice
- Resolve [INTERNAL-LINK] placeholders with actual URLs
- Add internal links to your existing content
- Run `/blog analyze <file>` to verify quality score
- Generate VideoObject schema: `/blog schema <file>` (includes video markup)
- Generate audio narration: `/blog audio generate <file>` (optional)
```

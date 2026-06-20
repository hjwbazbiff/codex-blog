# MCP And Credentials

Codex MCP servers are configured in `config.toml`. Use user-level `$CODEX_HOME/config.toml` or a trusted project `.codex/config.toml`.

See `.codex/config.example.toml` for sanitized examples covering:

- `nanobanana` for image generation with `GOOGLE_AI_API_KEY` supplied from the environment.
- `dataforseo` for paid SERP and keyword intelligence with credentials supplied from the environment.

Do not commit real keys, bearer tokens, cookies, or absolute private credential paths. Wrapper scripts must report missing credentials instead of inventing external API results.

# blog2vault

Substack blog → Obsidian vault pipeline for avikde.me.

## Project layout

Vault content (posts/, topics/, concepts/, citations/, _meta/, MOC.md) lives at the repo root alongside the Python source. The repo root IS the Obsidian vault.

## Key commands

```bash
# Install dependencies
uv sync --all-extras

# Run tests (104 tests, no network)
uv run pytest tests/ -v

# Full sync (fetches from Substack API, requires .env with ANTHROPIC_API_KEY)
uv run python sync.py --force

# Incremental sync (only new posts)
uv run python sync.py

# Dry run (no writes)
uv run python sync.py --dry-run

# TF-IDF only (no API calls)
uv run python sync.py --no-ai
```

## Module responsibilities

- `config.py` — all tunables, paths, thresholds. Env vars evaluated at import time (use `importlib.reload` in tests).
- `scrape.py` — Substack API client. Rate-limited, paginated. Cache is append-only with timestamp guards.
- `extract.py` — AI extraction (1 topic + concepts per post), TF-IDF fallback, citation extraction, crosslink inference, concept/topic clustering, domain collapsing.
- `vault.py` — Obsidian note generation. Atomic writes, wikilink verification, MOC/timeline/authors builders.
- `sync.py` — 7-stage pipeline orchestrator. Entry point. Loads `.env` via python-dotenv before config.

## Ontology

- **Topics**: what a post is ABOUT. 1 per post, assigned by AI, clustered to merge near-duplicates.
- **Concepts**: ideas/techniques INVOKED in a post. Many per post, expected to recur. Iteratively clustered until <=10% are sparse (scaled for corpus size).
- **Citations**: external URLs grouped by parent domain (subdomains collapsed via `_DOMAIN_PARENTS` in extract.py).

## Testing conventions

- All I/O tests use `tmp_path` + `patch_config_paths` fixture from conftest.py to isolate from real filesystem.
- HTTP calls are mocked via `unittest.mock.patch`.
- Config env var tests require `importlib.reload(config)` since values are computed at module load time.
- The `mock_graph` fixture in conftest.py must include keys: tags, topics, post_topic, concepts, concept_names, citations, crosslinks.

## Things to watch

- `config.VAULT_DIR` is `REPO_ROOT` (the repo root), not a subdirectory. Vault content is written directly alongside source files.
- The concept clustering threshold adapts to corpus size. With <100 posts the sparse ratio target is relaxed.
- AI extraction results are cached in `data/concepts_cache.json` keyed by `slug::updated_at`. Delete this file to force re-extraction.
- The 2 broken wikilinks in `jerboa-hopping-video.md` (`[[1]]`, `[[2]]`) are footnote artifacts from html2text, not real bugs.

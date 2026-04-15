# avikde-vault

An Obsidian knowledge vault of [Avik De's blog](https://www.avikde.me), auto-synced weekly from Substack.

Built by [mzargham](https://github.com/mzargham) for the author -- your grad school roommate gets a searchable, wikilinked, local-first archive of everything he's written.

---

## Using this vault in Obsidian

### Quick start

1. Clone the repo:
   ```bash
   git clone https://github.com/mzargham/avikde-vault.git
   ```
2. Open Obsidian and select **Open folder as vault**.
3. Point it at the cloned `avikde-vault` directory (the repo root).
4. The **Map of Content** (`MOC.md`) opens as the landing page.

The `.obsidian/` config is committed to the repo, so file filters are pre-configured -- you'll only see vault content (posts, topics, concepts, citations, meta notes) in the file explorer, not Python scripts or config files.

### Navigating the vault

- **MOC.md** -- the home page. All posts by year, topics, and concepts with counts.
- **posts/** -- one note per blog post, with YAML frontmatter, wikilinks, and full Markdown body.
- **topics/** -- tag-based groupings (e.g. `robotics`, `computing`).
- **concepts/** -- AI-extracted or TF-IDF-derived concepts cross-linked to posts.
- **citations/** -- external references grouped by source domain.
- **_meta/** -- Timeline (chronological) and Authors (bio) notes.

Every note is wikilinked: click `[[concepts/feedback-loops]]` from a post to see all other posts referencing that concept, or explore the **graph view** to see the full knowledge network.

### Staying up to date

```bash
cd avikde-vault
git pull
```

The vault is updated weekly by GitHub Actions. Just pull to get the latest posts.

---

## What's in the vault

```
MOC.md                          # Map of Content -- start here
posts/
    YYYY-MM-DD--{slug}.md       # One note per blog post
topics/
    {tag-slug}.md               # Aggregated by Substack tag
concepts/
    {concept-slug}.md           # Extracted key concepts, cross-linked
citations/
    {domain-slug}.md            # External references grouped by source domain
_meta/
    Timeline.md                 # All posts in chronological order
    Authors.md                  # About Avik De
```

Each post note contains:
- **YAML frontmatter** -- title, date, tags, concepts, canonical URL
- **Wikilink block** -- `[[topics/...]]`, `[[concepts/...]]`, `[[posts/...]]` (See Also), `[[citations/...]]`
- **Full body** -- HTML converted to Obsidian-compatible Markdown

---

## Setup (for developers / maintainers)

### Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- An [Anthropic API key](https://console.anthropic.com/) (for AI concept extraction; falls back to TF-IDF without one)

### Install

```bash
git clone https://github.com/mzargham/avikde-vault.git
cd avikde-vault
uv venv --python 3.12
uv sync --all-extras
```

### Environment

Create a `.env` file at the repo root (gitignored):

```
ANTHROPIC_API_KEY=sk-ant-...
```

This is loaded automatically by the sync pipeline via `python-dotenv`.

### First run (full build)

```bash
source .env && uv run python sync.py --force
```

This fetches all public posts, runs concept extraction, and writes the complete vault.

### Subsequent runs (incremental)

```bash
source .env && uv run python sync.py
```

Only processes new or updated posts. Nothing is written if the vault is already up to date.

### Options

```
python sync.py [--force] [--dry-run] [--no-ai]

  --force     Rebuild all notes even if no new posts detected.
  --dry-run   Fetch and compare; print what would change; write nothing.
  --no-ai     Use TF-IDF concept extraction instead of Anthropic API.
```

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Recommended | Powers AI concept extraction. Falls back to TF-IDF if absent. |
| `BLOG_CUSTOM_DOMAIN` | No | Override blog URL (default: `https://www.avikde.me`) |
| `SUBSTACK_SUBDOMAIN` | No | Fallback subdomain if auto-discovery fails |

---

## Automated weekly sync

A GitHub Actions workflow (`.github/workflows/weekly-sync.yml`) runs every Sunday at 06:00 UTC.

### Setup (one-time)

1. Fork or create this repo on GitHub.
2. Add your Anthropic API key as a repository secret:
   `Settings > Secrets and variables > Actions > New secret`
   Name: `ANTHROPIC_API_KEY`
3. That's it. The workflow commits new vault notes and pushes automatically.

### Manual trigger

In the Actions tab, select **Weekly Vault Sync** > **Run workflow**.
Enable **Rebuild all notes** to force a full refresh.

---

## Development

### Run tests

```bash
uv run pytest tests/ -v
```

Tests use mock data (`tests/fixtures/mock_posts.json`) -- no network required.

### Architecture

```
config.py    # All tunables (thresholds, paths, flags)
scrape.py    # Substack API client + cache management
extract.py   # Concept/tag/citation extraction (TF-IDF + AI)
vault.py     # Obsidian note generation + wikilink verification
sync.py      # Pipeline orchestrator + CLI
```

**Enforced constraints:**

| Constraint | Where enforced |
|------------|---------------|
| `PUBLIC_ONLY` -- only `audience=="everyone"` posts | `scrape.fetch_post_list` |
| `RATE_LIMIT` -- >= 0.5s between API requests | `scrape._get` |
| `CACHE_STABLE` -- cache entries not overwritten unless `updated_at` is newer | `scrape.save_cache` |
| `FILENAME_STABLE` -- filenames are deterministic | `vault._post_filename` |
| `NO_BROKEN_LINKS` -- all `[[wikilinks]]` resolve to a file | `vault._verify_wikilinks` |
| `SELF_CONSISTENT` -- every link target is written in the same pass | `vault.write_vault` |
| `GRACEFUL_DEGRADE` -- AI extraction failure falls back to TF-IDF | `extract.run_extraction` |

---

## Data files

`data/` is committed to the repo so CI/CD can perform incremental updates:

| File | Purpose |
|------|---------|
| `data/posts_cache.json` | Raw Substack API payloads, keyed by slug |
| `data/vault_state.json` | Maps slug -> filename for built notes |
| `data/concepts_cache.json` | AI extraction results, keyed by (slug, updated_at) |

---

## License

This vault is a personal archival tool for non-commercial use. The blog content belongs to Avik De. The vault-building code is MIT licensed.

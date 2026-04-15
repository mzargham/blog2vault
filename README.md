# avikde-vault

An Obsidian knowledge vault of [Avik De's blog](https://www.avikde.me), auto-synced weekly from Substack.

Built by [mzargham](https://github.com/mzargham) for the author -- who gets a searchable, wikilinked, local-first archive of everything he's written.

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
- **topics/** -- AI-assigned subject categories. Each post has exactly one topic; multiple posts can share the same topic. Semantically similar topics are clustered automatically.
- **concepts/** -- specific ideas, techniques, and frameworks invoked across posts. Concepts repeat across posts and are clustered to merge near-duplicates.
- **citations/** -- external references grouped by source domain (subdomains collapsed to parent organizations, e.g. `ai.mit.edu` -> `mit.edu`).
- **_meta/** -- Timeline (chronological) and Authors (bio) notes.

Every note is wikilinked: click `[[concepts/model-predictive-control]]` from a post to see all other posts referencing that concept, or explore the **graph view** to see the full knowledge network.

### Topic/concept ontology

The vault distinguishes two kinds of knowledge nodes:

- **Topics** are what a post is *about* -- the subject matter being discussed. Each post has exactly one topic, but multiple posts can share the same topic (e.g. "End-to-End Robotics Pipelines" spans 4 posts in a series).
- **Concepts** are ideas, techniques, or frameworks *invoked* while discussing a topic. A post references many concepts, and concepts are expected to recur across posts. A concept can also be a topic when a post is specifically about that concept.

Both are extracted by the Anthropic API and then clustered using TF-IDF + agglomerative clustering to merge semantic near-duplicates. The clustering picks the most semantically central member of each cluster as the canonical label.

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
    {topic-slug}.md             # AI-assigned topics (1 per post)
concepts/
    {concept-slug}.md           # Recurring concepts, clustered
citations/
    {domain-slug}.md            # External references grouped by domain
_meta/
    Timeline.md                 # All posts in chronological order
    Authors.md                  # About Avik De
```

Each post note contains:

- **YAML frontmatter** -- title, date, topic, concepts, canonical URL
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
uv run python sync.py --force
```

This fetches all public posts, runs extraction and clustering, and writes the complete vault.

### Subsequent runs (incremental)

```bash
uv run python sync.py
```

Only processes new or updated posts. Nothing is written if the vault is already up to date.

### Options

```
uv run python sync.py [--force] [--dry-run] [--no-ai]

  --force     Rebuild all notes even if no new posts detected.
  --dry-run   Fetch and compare; print what would change; write nothing.
  --no-ai     Use TF-IDF concept extraction instead of Anthropic API.
```

### Environment variables

| Variable             | Required    | Description                                                          |
| -------------------- | ----------- | -------------------------------------------------------------------- |
| `ANTHROPIC_API_KEY`  | Recommended | Powers AI concept extraction. Falls back to TF-IDF if absent.        |
| `BLOG_CUSTOM_DOMAIN` | No          | Override blog URL (default: `https://www.avikde.me`)                 |
| `SUBSTACK_SUBDOMAIN` | No          | Fallback subdomain if auto-discovery fails                           |

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

Tests use mock data (`tests/fixtures/mock_posts.json`) -- no network required. 104 tests covering all modules.

### Architecture

```
config.py    # All tunables (thresholds, paths, flags)
scrape.py    # Substack API client + cache management
extract.py   # Topic/concept extraction (AI + TF-IDF), citation extraction, clustering
vault.py     # Obsidian note generation + wikilink verification
sync.py      # Pipeline orchestrator + CLI entry point
```

### Pipeline stages

1. **DISCOVER** -- find canonical Substack base URL (custom domain -> subdomain fallback)
2. **FETCH** -- paginate all public posts, hydrate truncated bodies
3. **CACHE** -- update `data/posts_cache.json` (append-only, timestamp-guarded)
4. **DIFF** -- identify posts not yet in vault state
5. **EXTRACT** -- run topic/concept/citation extraction on full corpus, then cluster
6. **BUILD** -- generate all vault notes with wikilink verification
7. **REPORT** -- print summary, set GitHub Actions outputs

### Extraction pipeline

1. **AI extraction** (per post): Anthropic API assigns 1 topic + 3-8 concepts per post. Cached by `(slug, updated_at)` to avoid redundant API calls.
2. **Concept clustering**: TF-IDF on concept names + post titles -> cosine distance -> agglomerative clustering. Threshold relaxes iteratively until <= 10% of concepts appear in fewer than 3 posts (scaled for corpus size).
3. **Topic clustering**: same algorithm at a fixed threshold (0.85) to merge near-duplicate topics.
4. **Citation domain collapsing**: subdomains merged to parent organizations (e.g. `ai.mit.edu` -> `mit.edu`, `youtu.be` -> `youtube.com`).
5. **TF-IDF fallback**: if no API key, concepts are extracted locally via TF-IDF with stopword filtering and aggregate-score ranking.

### Enforced constraints

| Constraint        | Where enforced            |
| ----------------- | ------------------------- |
| `PUBLIC_ONLY`     | `scrape.fetch_post_list`  |
| `RATE_LIMIT`      | `scrape._get`             |
| `CACHE_STABLE`    | `scrape.save_cache`       |
| `FILENAME_STABLE` | `vault._post_filename`    |
| `NO_BROKEN_LINKS` | `vault._verify_wikilinks` |
| `SELF_CONSISTENT` | `vault.write_vault`       |
| `GRACEFUL_DEGRADE`| `extract.run_extraction`  |

---

## Data files

`data/` is committed to the repo so CI/CD can perform incremental updates:

| File                       | Purpose                                             |
| -------------------------- | --------------------------------------------------- |
| `data/posts_cache.json`    | Raw Substack API payloads, keyed by slug            |
| `data/vault_state.json`    | Maps slug -> filename for built notes               |
| `data/concepts_cache.json` | AI extraction results, keyed by (slug, updated_at)  |

---

## License

This vault is a personal archival tool for non-commercial use. The blog content belongs to Avik De. The vault-building code is MIT licensed.

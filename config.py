"""
config.py — Central configuration for the avikde-vault pipeline.

All tunable parameters are defined here. Override via environment variables
for CI/CD (see .github/workflows/weekly-sync.yml for expected secrets).

Layers (following conceptual/functional/logical/physical separation):
  Conceptual  : What blog, what vault
  Functional  : API pagination, extraction thresholds
  Logical     : File layout, slug conventions
  Physical    : Paths, timeouts, cache filenames
"""

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Conceptual layer: identity of the blog
# ---------------------------------------------------------------------------

# Custom domain for Avik's blog. The scraper will auto-detect the
# underlying Substack subdomain from this URL.
BLOG_CUSTOM_DOMAIN: str = os.getenv("BLOG_CUSTOM_DOMAIN", "https://www.avikde.me")

# Fallback Substack subdomain if auto-detection fails.
SUBSTACK_SUBDOMAIN_FALLBACK: str = os.getenv("SUBSTACK_SUBDOMAIN", "avikde")

# ---------------------------------------------------------------------------
# Functional layer: API and extraction behaviour
# ---------------------------------------------------------------------------

# Substack API pagination page size (max ~12 for public endpoint)
API_PAGE_SIZE: int = 12

# Seconds between API requests (polite rate limiting)
API_RATE_LIMIT_S: float = 0.5

# HTTP timeout in seconds
HTTP_TIMEOUT_S: int = 15

# Number of top TF-IDF terms to extract per post as concept candidates
TFIDF_TOP_N: int = 8

# Minimum document frequency for a concept to get its own note
# (appears in at least this many posts)
CONCEPT_MIN_DF: int = 2

# Maximum number of concepts total in the vault (to avoid noise)
CONCEPT_MAX_TOTAL: int = 40

# Whether to use Anthropic API for richer concept/theme extraction.
# Requires ANTHROPIC_API_KEY env var. Falls back to TF-IDF if False or key absent.
USE_AI_EXTRACTION: bool = os.getenv("USE_AI_EXTRACTION", "true").lower() == "true"

# Anthropic model for extraction (sonnet: good balance of cost and quality)
ANTHROPIC_MODEL: str = "claude-sonnet-4-20250514"

# ---------------------------------------------------------------------------
# Logical layer: vault structure conventions
# ---------------------------------------------------------------------------

# Folder names inside vault/
POSTS_FOLDER: str = "posts"
TOPICS_FOLDER: str = "topics"
CONCEPTS_FOLDER: str = "concepts"
CITATIONS_FOLDER: str = "citations"
META_FOLDER: str = "_meta"

# Filenames for special notes
MOC_FILENAME: str = "MOC.md"
TIMELINE_FILENAME: str = f"{META_FOLDER}/Timeline.md"
AUTHORS_FILENAME: str = f"{META_FOLDER}/Authors.md"

# ---------------------------------------------------------------------------
# Physical layer: filesystem paths
# ---------------------------------------------------------------------------

REPO_ROOT: Path = Path(__file__).resolve().parent
VAULT_DIR: Path = REPO_ROOT  # Vault content lives at the repo root (Obsidian opens here)
DATA_DIR: Path = REPO_ROOT / "data"

# Raw API cache: keyed by post slug, preserves original API payloads
POSTS_CACHE_FILE: Path = DATA_DIR / "posts_cache.json"

# Vault state: tracks what notes have been generated, for incremental updates
VAULT_STATE_FILE: Path = DATA_DIR / "vault_state.json"

# Concept extraction cache (avoids re-running AI extraction on unchanged posts)
CONCEPTS_CACHE_FILE: Path = DATA_DIR / "concepts_cache.json"

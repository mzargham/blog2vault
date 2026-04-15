"""
scrape.py — Substack API client with auto-discovery, pagination, and caching.

Responsibilities (functional layer):
  1. Discover the canonical Substack base URL from a custom domain.
  2. Paginate through all public posts via the unofficial /api/v1/posts endpoint.
  3. Fetch full post bodies when the list endpoint returns truncated HTML.
  4. Cache raw API payloads to data/posts_cache.json for incremental updates.

Constraints enforced:
  - Only public posts (audience == "everyone") are fetched. [PUBLIC_ONLY]
  - Rate limiting: ≥ API_RATE_LIMIT_S seconds between requests. [RATE_LIMIT]
  - HTTP errors raise immediately; caller decides retry strategy. [FAIL_FAST]
  - Cache is append-only keyed by slug; existing entries are never overwritten
    unless the post's updated_at timestamp changes. [CACHE_STABLE]
"""

import json
import time
import logging
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config import (
    BLOG_CUSTOM_DOMAIN,
    SUBSTACK_SUBDOMAIN_FALLBACK,
    API_PAGE_SIZE,
    API_RATE_LIMIT_S,
    HTTP_TIMEOUT_S,
    POSTS_CACHE_FILE,
    DATA_DIR,
)

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Shared HTTP session
# ---------------------------------------------------------------------------

_SESSION = requests.Session()
_SESSION.headers.update(
    {
        "User-Agent": (
            "Mozilla/5.0 (compatible; avikde-vault/1.0; "
            "research archival tool; contact via mzargham)"
        )
    }
)


def _get(url: str) -> requests.Response:
    """GET with timeout and rate limiting. Raises on HTTP error."""
    time.sleep(API_RATE_LIMIT_S)  # RATE_LIMIT: always sleep before request
    resp = _SESSION.get(url, timeout=HTTP_TIMEOUT_S)
    resp.raise_for_status()
    return resp


# ---------------------------------------------------------------------------
# Substack URL discovery
# ---------------------------------------------------------------------------

def discover_substack_base_url(custom_domain: str = BLOG_CUSTOM_DOMAIN) -> str:
    """
    Discover the canonical Substack API base URL for a custom-domain blog.

    Strategy (in order):
      1. Try the custom domain's /api/v1/posts directly — Substack proxies it.
      2. Parse the homepage HTML for a substack.com <link> or meta reference.
      3. Fall back to SUBSTACK_SUBDOMAIN_FALLBACK.substack.com.

    Returns the base URL (no trailing slash) that serves the /api/v1/ endpoints.
    """
    domain = custom_domain.rstrip("/")

    # Attempt 1: custom domain API (works when Substack proxies it)
    try:
        resp = _SESSION.get(
            f"{domain}/api/v1/posts?limit=1",
            timeout=HTTP_TIMEOUT_S,
        )
        if resp.status_code == 200 and resp.json():
            log.info("Custom domain API works: %s", domain)
            return domain
    except Exception as exc:
        log.debug("Custom domain API attempt failed: %s", exc)

    # Attempt 2: scrape homepage for substack.com references
    try:
        resp = _SESSION.get(domain, timeout=HTTP_TIMEOUT_S)
        soup = BeautifulSoup(resp.text, "html.parser")

        # Look for <link rel="canonical"> or og:url pointing to substack.com
        for tag in soup.find_all(["link", "meta"]):
            href = tag.get("href") or tag.get("content") or ""
            if "substack.com" in href:
                # Extract subdomain: https://SUBDOMAIN.substack.com/...
                parts = href.split("//")[-1].split(".")
                if len(parts) >= 3 and parts[1] == "substack":
                    subdomain = parts[0]
                    base = f"https://{subdomain}.substack.com"
                    log.info("Discovered Substack subdomain from HTML: %s", base)
                    return base
    except Exception as exc:
        log.debug("HTML discovery attempt failed: %s", exc)

    # Attempt 3: fallback
    base = f"https://{SUBSTACK_SUBDOMAIN_FALLBACK}.substack.com"
    log.warning("Using fallback Substack base URL: %s", base)
    return base


# ---------------------------------------------------------------------------
# Post fetching
# ---------------------------------------------------------------------------

def fetch_post_list(base_url: str) -> list[dict]:
    """
    Paginate through all public posts.

    Constraint PUBLIC_ONLY: posts with audience != "everyone" are dropped.
    Constraint RATE_LIMIT: enforced via _get().

    Returns list of raw post dicts from the API (may have truncated body_html).
    """
    posts: list[dict] = []
    offset = 0

    while True:
        url = f"{base_url}/api/v1/posts?limit={API_PAGE_SIZE}&offset={offset}"
        log.info("Fetching post list: offset=%d", offset)
        batch = _get(url).json()

        if not batch:
            break

        # CONSTRAINT PUBLIC_ONLY
        public_batch = [p for p in batch if p.get("audience") == "everyone"]
        posts.extend(public_batch)
        log.info(
            "  Got %d posts (%d public) at offset %d",
            len(batch),
            len(public_batch),
            offset,
        )

        if len(batch) < API_PAGE_SIZE:
            break  # Last page

        offset += API_PAGE_SIZE

    return posts


def fetch_post_body(base_url: str, slug: str) -> Optional[str]:
    """
    Fetch full body_html for a single post by slug.

    Used when the list endpoint returns a truncated body.
    Returns None on failure (caller should use truncated version).
    """
    try:
        url = f"{base_url}/api/v1/posts/by-slug/{slug}"
        data = _get(url).json()
        return data.get("body_html")
    except Exception as exc:
        log.warning("Could not fetch full body for %s: %s", slug, exc)
        return None


def _is_body_truncated(body_html: Optional[str]) -> bool:
    """Heuristic: Substack truncates at ~500 chars when behind paywall or in list."""
    if not body_html:
        return True
    return len(body_html) < 600


def fetch_all_posts(base_url: str) -> list[dict]:
    """
    Fetch all public posts with full bodies.

    For each post in the list, if the body appears truncated, attempts a
    secondary fetch via the by-slug endpoint.

    Returns fully-hydrated post dicts.
    """
    posts = fetch_post_list(base_url)

    for post in posts:
        slug = post.get("slug", "")
        body = post.get("body_html", "")

        if _is_body_truncated(body):
            log.info("Body truncated for '%s', fetching full post…", slug)
            full_body = fetch_post_body(base_url, slug)
            if full_body:
                post["body_html"] = full_body

    return posts


# ---------------------------------------------------------------------------
# Cache management
# ---------------------------------------------------------------------------

def load_cache() -> dict[str, dict]:
    """
    Load raw post cache from disk.

    Cache schema: { slug -> post_dict }
    Returns empty dict if cache file does not exist.
    """
    if not POSTS_CACHE_FILE.exists():
        return {}
    with open(POSTS_CACHE_FILE) as f:
        return json.load(f)


def save_cache(posts: list[dict]) -> None:
    """
    Merge new posts into the cache.

    CONSTRAINT CACHE_STABLE: existing entries are only overwritten if the
    incoming post has a strictly newer updated_at timestamp.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    existing = load_cache()

    updated_count = 0
    new_count = 0

    for post in posts:
        slug = post.get("slug")
        if not slug:
            continue

        if slug in existing:
            # Only overwrite if incoming is newer
            old_ts = existing[slug].get("updated_at", "")
            new_ts = post.get("updated_at", "")
            if new_ts > old_ts:
                existing[slug] = post
                updated_count += 1
        else:
            existing[slug] = post
            new_count += 1

    with open(POSTS_CACHE_FILE, "w") as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    log.info("Cache saved: %d new, %d updated, %d total", new_count, updated_count, len(existing))


def get_new_slugs(posts: list[dict], cache: dict[str, dict]) -> list[str]:
    """
    Return slugs present in posts but absent from cache.
    Used to identify new posts for incremental processing.
    """
    cached_slugs = set(cache.keys())
    return [p["slug"] for p in posts if p.get("slug") not in cached_slugs]

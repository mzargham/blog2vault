"""
extract.py — Concept, citation, and wikilink extraction from post corpora.

Two extraction modes:

  TF-IDF mode (default fallback):
    Uses sklearn TfidfVectorizer on post bodies. Terms appearing in ≥ CONCEPT_MIN_DF
    posts with high IDF scores become concept candidates. Entirely local, no API calls.

  AI mode (preferred, requires ANTHROPIC_API_KEY):
    Each post's title + body excerpt is sent to Claude for structured extraction of:
      - key_concepts: named ideas/techniques/frameworks referenced
      - themes: cross-cutting topics (feeds into topic notes)
      - citations: explicitly cited works or authors
    Results are cached in data/concepts_cache.json keyed by (slug, updated_at)
    so re-runs do not re-call the API for unchanged posts.

Citation extraction (always runs):
    Regex + BeautifulSoup URL extraction from body_html.
    Groups citations by domain → data structure for citation notes.

Wikilink graph construction:
    Returns a bipartite adjacency structure:
      post_slug → {concepts, topics, citations, linked_posts}
    This is consumed by vault.py to inject [[wikilinks]] into note bodies.

Constraints:
  - AI extraction failures are non-fatal; falls back to TF-IDF. [GRACEFUL_DEGRADE]
  - Citation URLs are normalized (scheme + netloc + path, query stripped). [URL_NORM]
  - Concept slugs are deterministic (python-slugify). [SLUG_STABLE]
  - All extraction is read-only on post data. [READ_ONLY]
"""

import json
import logging
import os
import re
from collections import defaultdict
from typing import Optional
from urllib.parse import urlparse

import html2text
from bs4 import BeautifulSoup
from slugify import slugify

from config import (
    TFIDF_TOP_N,
    CONCEPT_MIN_DF,
    CONCEPT_MAX_TOTAL,
    USE_AI_EXTRACTION,
    ANTHROPIC_MODEL,
    CONCEPTS_CACHE_FILE,
    DATA_DIR,
    BLOG_CUSTOM_DOMAIN,
)

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# HTML → plain text utility
# ---------------------------------------------------------------------------

_html2text = html2text.HTML2Text()
_html2text.ignore_links = True
_html2text.ignore_images = True
_html2text.body_width = 0  # no line wrapping


def html_to_text(html: str) -> str:
    """Convert HTML to plain text for NLP processing."""
    if not html:
        return ""
    return _html2text.handle(html).strip()


def html_to_markdown(html: str) -> str:
    """Convert HTML to Obsidian-compatible Markdown, preserving links."""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    h.protect_links = True
    h.wrap_links = False
    return h.handle(html).strip()


# ---------------------------------------------------------------------------
# Tag / topic extraction (from API metadata)
# ---------------------------------------------------------------------------

def extract_tags(posts: list[dict]) -> dict[str, list[str]]:
    """
    Extract tags from Substack post metadata.

    Returns:
        tag_slug → [post_slug, ...]   (tag → which posts carry it)
    """
    tag_to_posts: dict[str, list[str]] = defaultdict(list)

    for post in posts:
        slug = post.get("slug", "")
        tags = post.get("postTags") or post.get("tags") or []

        for tag in tags:
            # Substack tags can be dicts or strings
            if isinstance(tag, dict):
                tag_name = tag.get("name") or tag.get("slug") or ""
            else:
                tag_name = str(tag)

            if tag_name:
                tag_slug = slugify(tag_name)
                tag_to_posts[tag_slug].append(slug)

    return dict(tag_to_posts)


# ---------------------------------------------------------------------------
# TF-IDF concept extraction
# ---------------------------------------------------------------------------

def extract_concepts_tfidf(posts: list[dict]) -> tuple[dict[str, list[str]], dict[str, str]]:
    """
    TF-IDF based concept extraction across the post corpus.

    Returns:
        concept_slug → [post_slug, ...]   (concept → which posts reference it)
        concept_slug → display_name       (slug → human-readable name)

    Constraints:
        - Only concepts appearing in ≥ CONCEPT_MIN_DF posts are retained.
        - At most CONCEPT_MAX_TOTAL concepts are returned (by IDF score).
        - Single-character or purely numeric terms are discarded.
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np
    except ImportError:
        log.warning("scikit-learn not available; skipping TF-IDF extraction")
        return {}, {}

    # Prepare corpus: title + subtitle + plain-text body
    slugs = []
    corpus = []
    for post in posts:
        text = " ".join(
            [
                post.get("title") or "",
                post.get("subtitle") or "",
                html_to_text(post.get("body_html") or ""),
            ]
        )
        slugs.append(post.get("slug", ""))
        corpus.append(text)

    if len(corpus) < 2:
        log.info("Fewer than 2 posts; skipping TF-IDF")
        return {}, {}

    vec = TfidfVectorizer(
        ngram_range=(1, 3),
        min_df=CONCEPT_MIN_DF,
        max_df=0.70,
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{3,}\b",  # ≥4 chars, letters only
        max_features=500,
    )

    tfidf_matrix = vec.fit_transform(corpus)
    feature_names = vec.get_feature_names_out()

    # Rank features by aggregate TF-IDF score across all documents.
    # This favors terms that are both frequent AND discriminative,
    # filtering out rare one-off terms that IDF alone would surface.
    agg_scores = np.asarray(tfidf_matrix.sum(axis=0)).flatten()
    ranked_idx = np.argsort(agg_scores)[::-1]
    candidates = [feature_names[i] for i in ranked_idx[:CONCEPT_MAX_TOTAL * 3]]

    # Generic / noisy terms to suppress
    _STOPLIST = {
        "post", "blog", "article", "part", "like", "just", "also", "one",
        "new", "use", "using", "used", "way", "make", "see", "get",
        "first", "two", "even", "much", "well", "many", "need", "want",
        "know", "think", "take", "come", "look", "find", "give", "tell",
        "work", "good", "time", "year", "thing", "point", "case", "example",
        "question", "problem", "idea", "approach", "really", "something",
    }

    concept_to_posts: dict[str, list[str]] = {}
    concept_display: dict[str, str] = {}

    count = 0
    for feat in candidates:
        if count >= CONCEPT_MAX_TOTAL:
            break
        # Skip single-word generic terms
        if feat.lower() in _STOPLIST:
            continue
        feat_idx = list(feature_names).index(feat)
        col = tfidf_matrix[:, feat_idx].toarray().flatten()
        referencing_posts = [slugs[i] for i, score in enumerate(col) if score > 0]

        if len(referencing_posts) >= CONCEPT_MIN_DF:
            cslug = slugify(feat)
            # Avoid duplicate slugs (e.g. "robot" and "robots" → same slug)
            if cslug in concept_to_posts:
                continue
            concept_to_posts[cslug] = referencing_posts
            concept_display[cslug] = feat.title()
            count += 1

    log.info("TF-IDF extracted %d concepts", len(concept_to_posts))
    return concept_to_posts, concept_display


# ---------------------------------------------------------------------------
# AI concept extraction (Anthropic API)
# ---------------------------------------------------------------------------

_EXTRACTION_SYSTEM = """You are an expert research assistant helping build a knowledge graph
from an academic blog. For each blog post excerpt, extract structured information.

Respond ONLY with a valid JSON object — no markdown fences, no preamble. Schema:
{
  "key_concepts": ["concept1", "concept2"],
  "themes": ["theme1", "theme2"],
  "cited_works": ["Author Year", "Paper Title"],
  "related_fields": ["field1", "field2"]
}

Rules:
- key_concepts: 3–6 named ideas, techniques, or frameworks central to the post
- themes: 2–4 broad cross-cutting topics (e.g., "systems thinking", "control theory")
- cited_works: explicit academic works or authors mentioned in the text
- related_fields: 1–3 academic disciplines relevant to this post
- Use title case for all entries
- Be specific, not generic ("Lyapunov Stability" not "Math")
"""


def _load_concepts_cache() -> dict:
    if not CONCEPTS_CACHE_FILE.exists():
        return {}
    with open(CONCEPTS_CACHE_FILE) as f:
        return json.load(f)


def _save_concepts_cache(cache: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONCEPTS_CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def extract_concepts_ai(posts: list[dict]) -> tuple[dict[str, list[str]], dict[str, str], dict[str, list[str]]]:
    """
    AI-powered concept extraction using the Anthropic API.

    For each post sends: title + subtitle + first ~1200 chars of body text.
    Results cached by (slug, updated_at) to avoid redundant API calls.

    Returns:
        concept_slug → [post_slug, ...]
        concept_slug → display_name
        theme_slug → [post_slug, ...]    (merged into tags for topic notes)

    CONSTRAINT GRACEFUL_DEGRADE: returns empty dicts on API failure.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.warning("ANTHROPIC_API_KEY not set; skipping AI extraction")
        return {}, {}, {}

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
    except ImportError:
        log.warning("anthropic SDK not installed; skipping AI extraction")
        return {}, {}, {}

    cache = _load_concepts_cache()
    concept_to_posts: dict[str, list[str]] = defaultdict(list)
    concept_display: dict[str, str] = {}
    theme_to_posts: dict[str, list[str]] = defaultdict(list)

    for post in posts:
        slug = post.get("slug", "")
        updated_at = post.get("updated_at", "")
        cache_key = f"{slug}::{updated_at}"

        if cache_key in cache:
            log.debug("AI extraction cache hit: %s", slug)
            extracted = cache[cache_key]
        else:
            body_text = html_to_text(post.get("body_html") or "")[:1200]
            prompt = (
                f"Title: {post.get('title', '')}\n"
                f"Subtitle: {post.get('subtitle', '')}\n\n"
                f"Excerpt:\n{body_text}"
            )
            try:
                msg = client.messages.create(
                    model=ANTHROPIC_MODEL,
                    max_tokens=400,
                    system=_EXTRACTION_SYSTEM,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw = msg.content[0].text.strip()
                extracted = json.loads(raw)
                cache[cache_key] = extracted
                log.info("AI extracted concepts for: %s", slug)
            except Exception as exc:
                log.warning("AI extraction failed for %s: %s", slug, exc)
                extracted = {}

        # Accumulate concepts
        for concept in extracted.get("key_concepts", []):
            cslug = slugify(concept)
            concept_to_posts[cslug].append(slug)
            concept_display[cslug] = concept

        for concept in extracted.get("related_fields", []):
            cslug = slugify(concept)
            concept_to_posts[cslug].append(slug)
            concept_display[cslug] = concept

        # Accumulate themes (go into topic notes)
        for theme in extracted.get("themes", []):
            tslug = slugify(theme)
            theme_to_posts[tslug].append(slug)
            # Also add to concept display for theme notes
            concept_display[tslug] = theme

    _save_concepts_cache(cache)

    log.info(
        "AI extraction: %d concepts, %d themes across %d posts",
        len(concept_to_posts),
        len(theme_to_posts),
        len(posts),
    )
    return dict(concept_to_posts), concept_display, dict(theme_to_posts)


# ---------------------------------------------------------------------------
# Citation extraction
# ---------------------------------------------------------------------------

# Domains to exclude from citation notes (infrastructure, not content citations)
_SKIP_DOMAINS = {
    "substack.com", "avikde.me", "avikde.substack.com",
    "twitter.com", "x.com", "facebook.com", "instagram.com",
    "fonts.googleapis.com", "cdn.substack.com", "substackcdn.com",
    "google.com", "goo.gl", "bit.ly", "t.co",
}


def _normalize_url(url: str) -> Optional[str]:
    """
    Normalize a URL to scheme + netloc + path, stripping query and fragment.
    Returns None for URLs matching _SKIP_DOMAINS. [URL_NORM]
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme.startswith("http"):
            return None
        domain = parsed.netloc.lower().removeprefix("www.")
        if any(domain == skip or domain.endswith(f".{skip}") for skip in _SKIP_DOMAINS):
            return None
        path = parsed.path.rstrip("/")
        return f"{parsed.scheme}://{parsed.netloc}{path}"
    except Exception:
        return None


def extract_citations(posts: list[dict]) -> dict[str, dict]:
    """
    Extract external URLs from post bodies as citation records.

    Returns:
        url → {
            "url": str,
            "domain": str,
            "domain_slug": str,
            "posts": [post_slug, ...],
            "anchor_texts": [str, ...]   (link text used in posts)
        }
    """
    citations: dict[str, dict] = {}

    for post in posts:
        slug = post.get("slug", "")
        body_html = post.get("body_html") or ""
        if not body_html:
            continue

        soup = BeautifulSoup(body_html, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            raw_url = a_tag["href"]
            norm = _normalize_url(raw_url)
            if not norm:
                continue

            anchor = a_tag.get_text(strip=True)
            parsed = urlparse(norm)
            domain = parsed.netloc.lower().removeprefix("www.")

            if norm not in citations:
                citations[norm] = {
                    "url": norm,
                    "domain": domain,
                    "domain_slug": slugify(domain),
                    "posts": [],
                    "anchor_texts": [],
                }

            if slug not in citations[norm]["posts"]:
                citations[norm]["posts"].append(slug)
            if anchor and anchor not in citations[norm]["anchor_texts"]:
                citations[norm]["anchor_texts"].append(anchor)

    log.info("Extracted %d unique citations across all posts", len(citations))
    return citations


# ---------------------------------------------------------------------------
# Cross-post link inference (post ↔ post wikilinks)
# ---------------------------------------------------------------------------

def infer_post_crosslinks(posts: list[dict]) -> dict[str, list[str]]:
    """
    Detect when one post's body text explicitly mentions another post's title.

    Returns:
        source_slug → [target_slug, ...]
    """
    title_to_slug = {
        post.get("title", "").lower(): post.get("slug", "")
        for post in posts
        if post.get("title") and post.get("slug")
    }

    crosslinks: dict[str, list[str]] = defaultdict(list)

    for post in posts:
        src_slug = post.get("slug", "")
        body_text = html_to_text(post.get("body_html") or "").lower()

        for title, tgt_slug in title_to_slug.items():
            if tgt_slug == src_slug:
                continue
            if len(title) > 10 and title in body_text:
                crosslinks[src_slug].append(tgt_slug)

    return dict(crosslinks)


# ---------------------------------------------------------------------------
# Main extraction orchestrator
# ---------------------------------------------------------------------------

def run_extraction(posts: list[dict]) -> dict:
    """
    Full extraction pipeline. Returns a graph dict consumed by vault.py:

    {
        "tags":          { tag_slug → [post_slug] },
        "concepts":      { concept_slug → [post_slug] },
        "concept_names": { concept_slug → display_name },
        "themes":        { theme_slug → [post_slug] },
        "citations":     { url → citation_dict },
        "crosslinks":    { post_slug → [post_slug] },
    }
    """
    log.info("Starting extraction for %d posts", len(posts))

    tags = extract_tags(posts)
    log.info("Tags: %d", len(tags))

    citations = extract_citations(posts)
    crosslinks = infer_post_crosslinks(posts)

    if USE_AI_EXTRACTION and os.getenv("ANTHROPIC_API_KEY"):
        concepts, concept_names, themes = extract_concepts_ai(posts)
    else:
        log.info("Using TF-IDF extraction (AI disabled or key absent)")
        concepts, concept_names = extract_concepts_tfidf(posts)
        themes = {}

    return {
        "tags": tags,
        "concepts": concepts,
        "concept_names": concept_names,
        "themes": themes,
        "citations": citations,
        "crosslinks": crosslinks,
    }

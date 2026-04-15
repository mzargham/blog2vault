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

    # Adapt min_df/max_df for small corpora to avoid sklearn ValueError
    effective_min_df = min(CONCEPT_MIN_DF, len(corpus) - 1)
    effective_max_df = max(0.70, (effective_min_df + 1) / len(corpus))

    vec = TfidfVectorizer(
        ngram_range=(1, 3),
        min_df=effective_min_df,
        max_df=effective_max_df,
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

_EXTRACTION_SYSTEM = """You are an expert research assistant building a knowledge graph
from an academic/engineering blog. For each post, extract a TOPIC and CONCEPTS.

Ontology:
- TOPIC: what this post is fundamentally ABOUT. Each post has exactly ONE topic.
  Topics are the subject matter — the thing being discussed, explained, or argued.
  Examples: "End-to-End Robotics Pipelines", "Legged Locomotion", "Systolic Arrays",
  "Cybernetics", "Vision-Language-Action Models"
- CONCEPTS: specific ideas, techniques, frameworks, or methods INVOKED while
  discussing the topic. A post uses concepts as building blocks, references, or tools.
  Concepts recur across posts — the same concept appears in different topical contexts.
  Examples: "Model Predictive Control", "Feedback Loops", "Template-Based Design",
  "Von Neumann Architecture", "Transfer Learning"

A concept CAN be a topic when the post is specifically about that concept.
But usually the topic is broader and the concepts are the pieces used to discuss it.

Respond ONLY with a valid JSON object — no markdown fences, no preamble. Schema:
{
  "topic": "The Single Topic Of This Post",
  "concepts": ["Concept 1", "Concept 2", "Concept 3"]
}

Rules:
- topic: exactly 1 string — the subject of this post (title case, specific not generic)
- concepts: 3–8 named ideas, techniques, or frameworks invoked in the post (title case)
- Be specific: "Raibert Hopping Controller" not "Control", "Cache Line Effects" not "Performance"
- Prefer established terms from the field over invented phrases
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


def extract_concepts_ai(posts: list[dict]) -> tuple[dict[str, list[str]], dict[str, str], dict[str, str]]:
    """
    AI-powered extraction using the Anthropic API.

    Ontology:
      - TOPIC: what the post is about (exactly 1 per post).
      - CONCEPTS: ideas/techniques invoked while discussing the topic (many per post).

    For each post sends: title + subtitle + first ~1200 chars of body text.
    Results cached by (slug, updated_at) to avoid redundant API calls.

    Returns:
        concept_slug → [post_slug, ...]
        concept_slug → display_name
        post_slug → topic_slug              (1:1 mapping, each post has one topic)

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
    post_topic: dict[str, str] = {}  # post_slug → topic_slug

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
                log.info("AI extracted for: %s → topic=%s", slug, extracted.get("topic", "?"))
            except Exception as exc:
                log.warning("AI extraction failed for %s: %s", slug, exc)
                extracted = {}

        # Assign topic (1 per post)
        topic = extracted.get("topic", "")
        if topic:
            tslug = slugify(topic)
            post_topic[slug] = tslug
            concept_display[tslug] = topic  # topics also get display names

        # Accumulate concepts
        for concept in extracted.get("concepts", []):
            cslug = slugify(concept)
            concept_to_posts[cslug].append(slug)
            concept_display[cslug] = concept

    _save_concepts_cache(cache)

    log.info(
        "AI extraction: %d topics, %d concepts across %d posts",
        len(set(post_topic.values())),
        len(concept_to_posts),
        len(posts),
    )
    return dict(concept_to_posts), concept_display, post_topic


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
# Concept clustering (reduce semantic near-duplicates)
# ---------------------------------------------------------------------------

def _cluster_at_threshold(
    concepts: dict[str, list[str]],
    concept_names: dict[str, str],
    posts: list[dict],
    distance_threshold: float,
) -> tuple[dict[str, list[str]], dict[str, str]]:
    """
    Single-pass agglomerative clustering of concepts at a given threshold.

    Uses TF-IDF on concept names (triple-weighted) plus associated post titles
    to build a semantic representation, then clusters by cosine distance.

    For each cluster, the concept closest to the cluster centroid is chosen
    as the canonical label — the most semantically central member.

    Returns:
        merged_concepts: concept_slug → [post_slug, ...]
        merged_names:    concept_slug → display_name
    """
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import AgglomerativeClustering
    from sklearn.metrics.pairwise import cosine_distances
    import numpy as np

    post_titles = {p.get("slug", ""): p.get("title", "") for p in posts}
    concept_slugs = list(concepts.keys())
    documents = []
    for cslug in concept_slugs:
        display = concept_names.get(cslug, cslug.replace("-", " "))
        titles = " ".join(post_titles.get(ps, "") for ps in concepts[cslug])
        documents.append(f"{display} {display} {display} {titles}")

    vec = TfidfVectorizer(stop_words="english", token_pattern=r"(?u)\b\w{3,}\b")
    tfidf_matrix = vec.fit_transform(documents)
    dist_matrix = cosine_distances(tfidf_matrix)

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=distance_threshold,
        metric="precomputed",
        linkage="average",
    )
    labels = clustering.fit_predict(dist_matrix)

    cluster_groups: dict[int, list[str]] = defaultdict(list)
    for slug, label in zip(concept_slugs, labels):
        cluster_groups[label].append(slug)

    merged_concepts: dict[str, list[str]] = {}
    merged_names: dict[str, str] = {}

    for cluster_id, members in cluster_groups.items():
        member_indices = [concept_slugs.index(m) for m in members]
        member_vectors = tfidf_matrix[member_indices]
        centroid = np.asarray(member_vectors.mean(axis=0))
        centroid_dists = cosine_distances(centroid, member_vectors).flatten()
        canonical_idx = member_indices[int(np.argmin(centroid_dists))]
        canonical = concept_slugs[canonical_idx]

        all_posts = []
        seen = set()
        for m in members:
            for p in concepts[m]:
                if p not in seen:
                    all_posts.append(p)
                    seen.add(p)

        merged_concepts[canonical] = all_posts
        merged_names[canonical] = concept_names.get(canonical, canonical.replace("-", " ").title())

        if len(members) > 1:
            absorbed = [concept_names.get(m, m) for m in members if m != canonical]
            log.debug(
                "Cluster: %s ← %s",
                concept_names.get(canonical, canonical),
                ", ".join(absorbed),
            )

    return merged_concepts, merged_names


def cluster_concepts(
    concepts: dict[str, list[str]],
    concept_names: dict[str, str],
    posts: list[dict],
    max_sparse_ratio: float = 0.10,
    min_posts_for_strict: int = 100,
) -> tuple[dict[str, list[str]], dict[str, str]]:
    """
    Iteratively cluster concepts, relaxing the distance threshold until at most
    `max_sparse_ratio` of concepts appear in fewer than CONCEPT_MIN_DF posts.

    For small corpora (< `min_posts_for_strict` posts), the target ratio is
    relaxed proportionally — a 29-post blog can't achieve 10% sparsity without
    destroying semantic coherence.

    Starts at threshold=0.65 (conservative) and increments by 0.05 each round,
    capping at 0.95 to avoid collapsing everything into one cluster.

    Returns:
        merged_concepts: concept_slug → [post_slug, ...]
        merged_names:    concept_slug → display_name
    """
    if len(concepts) < 2:
        return concepts, concept_names

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: F401
    except ImportError:
        log.warning("scikit-learn not available; skipping concept clustering")
        return concepts, concept_names

    # Scale the target: small corpora get a looser target, converging to
    # max_sparse_ratio as the blog grows past min_posts_for_strict posts.
    n_posts = len(posts)
    scale = min(1.0, n_posts / min_posts_for_strict)
    effective_target = 1.0 - scale * (1.0 - max_sparse_ratio)  # 1.0 → max_sparse_ratio
    log.info(
        "Clustering target: %.0f%% sparse (corpus=%d posts, strict target=%.0f%%)",
        effective_target * 100, n_posts, max_sparse_ratio * 100,
    )

    threshold = 0.65
    max_threshold = 0.95
    step = 0.05
    best_concepts = concepts
    best_names = concept_names

    while threshold <= max_threshold:
        merged, names = _cluster_at_threshold(concepts, concept_names, posts, threshold)
        sparse = sum(1 for v in merged.values() if len(v) < CONCEPT_MIN_DF)
        ratio = sparse / len(merged) if merged else 0

        log.info(
            "Concept clustering pass: threshold=%.2f → %d concepts "
            "(%d sparse, %.0f%% < min_df=%d)",
            threshold, len(merged), sparse, ratio * 100, CONCEPT_MIN_DF,
        )

        best_concepts = merged
        best_names = names

        if ratio <= effective_target:
            break

        threshold += step

    log.info(
        "Concept clustering final: %d → %d (merged %d, threshold=%.2f)",
        len(concepts), len(best_concepts),
        len(concepts) - len(best_concepts), threshold,
    )
    return best_concepts, best_names


# ---------------------------------------------------------------------------
# Main extraction orchestrator
# ---------------------------------------------------------------------------

def run_extraction(posts: list[dict]) -> dict:
    """
    Full extraction pipeline. Returns a graph dict consumed by vault.py:

    {
        "tags":          { tag_slug → [post_slug] },       (Substack metadata)
        "topics":        { topic_slug → [post_slug] },     (1 topic per post, AI-assigned)
        "post_topic":    { post_slug → topic_slug },       (reverse lookup)
        "concepts":      { concept_slug → [post_slug] },   (many per post, expected to repeat)
        "concept_names": { concept_slug → display_name },  (display names for topics + concepts)
        "citations":     { url → citation_dict },
        "crosslinks":    { post_slug → [post_slug] },
    }

    Ontology:
      - Topics are what posts are ABOUT (1 per post, many posts can share a topic).
      - Concepts are ideas/techniques INVOKED when discussing a topic (many per post).
      - Concepts below CONCEPT_MIN_DF are kept but logged as warnings (may be new).
    """
    log.info("Starting extraction for %d posts", len(posts))

    tags = extract_tags(posts)
    log.info("Substack tags: %d", len(tags))

    citations = extract_citations(posts)
    crosslinks = infer_post_crosslinks(posts)

    if USE_AI_EXTRACTION and os.getenv("ANTHROPIC_API_KEY"):
        concepts, concept_names, post_topic = extract_concepts_ai(posts)
    else:
        log.info("Using TF-IDF extraction (AI disabled or key absent)")
        concepts, concept_names = extract_concepts_tfidf(posts)
        post_topic = {}

    # Cluster semantically similar concepts to reduce near-duplicates
    concepts, concept_names = cluster_concepts(concepts, concept_names, posts)

    # Build topic → [post_slugs] from post_topic reverse lookup
    topics_raw: dict[str, list[str]] = defaultdict(list)
    for post_slug, topic_slug in post_topic.items():
        topics_raw[topic_slug].append(post_slug)

    # Cluster topics the same way (they're often too granular from AI extraction)
    if len(topics_raw) >= 2:
        topics, topic_names = _cluster_at_threshold(
            dict(topics_raw), concept_names, posts, distance_threshold=0.85,
        )
        # Update concept_names with any new canonical topic names
        concept_names.update(topic_names)
        # Rebuild post_topic to point at merged topic slugs
        post_topic = {}
        for topic_slug, topic_posts in topics.items():
            for ps in topic_posts:
                post_topic[ps] = topic_slug
        log.info(
            "Topic clustering: %d → %d (merged %d)",
            len(topics_raw), len(topics), len(topics_raw) - len(topics),
        )
    else:
        topics = dict(topics_raw)

    # Log concepts below min_df as warnings (they may be new or niche)
    low_df = {c: slugs for c, slugs in concepts.items() if len(slugs) < CONCEPT_MIN_DF}
    if low_df:
        log.warning(
            "%d concepts appear in fewer than %d posts (may be new): %s",
            len(low_df),
            CONCEPT_MIN_DF,
            ", ".join(sorted(low_df.keys())[:10]) + ("..." if len(low_df) > 10 else ""),
        )

    return {
        "tags": tags,
        "topics": topics,
        "post_topic": post_topic,
        "concepts": concepts,
        "concept_names": concept_names,
        "citations": citations,
        "crosslinks": crosslinks,
    }

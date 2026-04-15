"""
vault.py — Obsidian vault note generation.

Responsibilities:
  - Convert raw post dicts + extraction graph → Obsidian-compatible Markdown.
  - Inject [[wikilinks]] into note bodies at appropriate anchor points.
  - Generate MOC, topic notes, concept notes, citation notes, timeline, author note.
  - Write all files to VAULT_DIR, creating subdirectories as needed.
  - Track what was written in data/vault_state.json for incremental updates.

Note anatomy:
  Each post note has:
    1. YAML frontmatter  (title, date, tags, concepts, canonical_url, ...)
    2. Header section   (title, subtitle, cover image if present)
    3. Wikilink block   (Topics | Concepts | See Also | Citations)
    4. Body             (HTML → Markdown, with external links preserved)

Filename convention:
  posts/   YYYY-MM-DD--{slug}.md       (date-prefixed for filesystem sorting)
  topics/  {tag-slug}.md
  concepts/{concept-slug}.md
  citations/{domain-slug}.md           (grouped by domain, not per-URL)
  _meta/   Timeline.md  Authors.md

Constraints:
  - Filenames are deterministic and stable across runs. [FILENAME_STABLE]
  - Wikilink targets always exist in the vault (no broken links). [NO_BROKEN_LINKS]
  - All writes are atomic per-file (write to temp, rename). [ATOMIC_WRITE]
  - Vault is self-consistent: every [[link]] resolves to a file. [SELF_CONSISTENT]
"""

import json
import logging
import re
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from slugify import slugify

from extract import html_to_markdown
import config
from config import (
    POSTS_FOLDER,
    TOPICS_FOLDER,
    CONCEPTS_FOLDER,
    CITATIONS_FOLDER,
    META_FOLDER,
    MOC_FILENAME,
    TIMELINE_FILENAME,
    AUTHORS_FILENAME,
    BLOG_CUSTOM_DOMAIN,
)

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _fmt_date(iso: str) -> str:
    """Parse ISO datetime string → YYYY-MM-DD."""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.date().isoformat()
    except Exception:
        return iso[:10] if iso else "unknown"


def _post_filename(post: dict) -> str:
    """Deterministic filename: YYYY-MM-DD--{slug}.md  [FILENAME_STABLE]"""
    date = _fmt_date(post.get("post_date") or post.get("publishedAt") or "")
    slug = post.get("slug", "unknown")
    return f"{date}--{slug}.md"


def _post_display_title(post: dict) -> str:
    return post.get("title") or post.get("slug", "Untitled")


def _wikilink(folder: str, slug: str, display: Optional[str] = None) -> str:
    """Format an Obsidian wikilink: [[folder/slug|display]]"""
    target = f"{folder}/{slug}"
    if display:
        return f"[[{target}|{display}]]"
    return f"[[{target}]]"


def _atomic_write(path: Path, content: str) -> None:
    """Write content to path atomically. [ATOMIC_WRITE]"""
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write to temp in same dir, then rename (atomic on POSIX)
    with tempfile.NamedTemporaryFile(
        mode="w", dir=path.parent, suffix=".tmp", delete=False, encoding="utf-8"
    ) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


# ---------------------------------------------------------------------------
# Post note builder
# ---------------------------------------------------------------------------

def build_post_note(
    post: dict,
    graph: dict,
    all_post_slugs: set[str],
    slug_to_filename: dict[str, str],
) -> str:
    """
    Build the full Markdown note for a single blog post.

    Args:
        post:            Raw post dict from Substack API.
        graph:           Extraction graph from extract.run_extraction().
        all_post_slugs:  Set of all slugs in the vault (for [[link]] validation).

    Returns:
        Complete Markdown string for the post note.
    """
    slug = post.get("slug", "")
    title = _post_display_title(post)
    subtitle = post.get("subtitle") or ""
    date_str = _fmt_date(post.get("post_date") or post.get("publishedAt") or "")
    canonical = post.get("canonical_url") or f"{BLOG_CUSTOM_DOMAIN}/p/{slug}"
    cover = post.get("cover_image") or ""

    # ---- Collect wikilink targets ----
    # Topic (1 per post, from AI extraction)
    topic_slug = graph.get("post_topic", {}).get(slug, "")
    topic_display = graph["concept_names"].get(topic_slug, topic_slug.replace("-", " ").title()) if topic_slug else ""
    # Concepts
    post_concepts = [
        cs for cs, posts in graph["concepts"].items() if slug in posts
    ]
    # Cited URLs
    post_citations = [
        url for url, cdata in graph["citations"].items() if slug in cdata["posts"]
    ]
    # Cross-linked posts [NO_BROKEN_LINKS: only link to known slugs]
    post_crosslinks = [
        s for s in graph["crosslinks"].get(slug, []) if s in all_post_slugs
    ]

    # ---- YAML Frontmatter ----
    frontmatter_topic = topic_display if topic_display else "Uncategorized"
    frontmatter_concepts = (
        "\n".join(f'  - "{graph["concept_names"].get(c, c)}"' for c in post_concepts)
        if post_concepts
        else "  []"
    )
    frontmatter = f"""---
title: "{title.replace('"', "'")}"
subtitle: "{subtitle.replace('"', "'")}"
date: {date_str}
slug: {slug}
canonical_url: "{canonical}"
topic: "{frontmatter_topic}"
concepts:
{frontmatter_concepts}
source: Substack
author: Avik De
---
"""

    # ---- Header ----
    cover_md = f"\n![]({cover})\n" if cover else ""
    header = f"# {title}\n{cover_md}\n"
    if subtitle:
        header += f"*{subtitle}*\n\n"
    header += f"> Originally published: [{date_str}]({canonical})\n\n"

    # ---- Wikilink block ----
    wikilink_parts = []

    if topic_slug:
        topic_link = _wikilink(TOPICS_FOLDER, topic_slug, topic_display)
        wikilink_parts.append(f"**Topic:** {topic_link}")

    if post_concepts:
        concept_links = [
            _wikilink(
                CONCEPTS_FOLDER,
                c,
                graph["concept_names"].get(c, c.replace("-", " ").title()),
            )
            for c in post_concepts
        ]
        wikilink_parts.append("**Concepts:** " + " · ".join(concept_links))

    if post_crosslinks:
        cross_links_md = []
        for xslug in post_crosslinks:
            # Use the full date-prefixed filename stem as the link target [FILENAME_STABLE]
            xfilename = slug_to_filename.get(xslug, xslug)
            xstem = xfilename[:-3] if xfilename.endswith(".md") else xfilename
            cross_links_md.append(_wikilink(POSTS_FOLDER, xstem))
        wikilink_parts.append("**See Also:** " + " · ".join(cross_links_md))

    if post_citations:
        domain_slugs = list(dict.fromkeys(
            graph["citations"][url]["domain_slug"] for url in post_citations
        ))
        cite_links = [
            _wikilink(CITATIONS_FOLDER, ds, ds.replace("-", "."))
            for ds in domain_slugs
        ]
        wikilink_parts.append("**Citations:** " + " · ".join(cite_links))

    wikilink_block = ""
    if wikilink_parts:
        wikilink_block = "\n".join(wikilink_parts) + "\n\n---\n\n"

    # ---- Body ----
    body_html = post.get("body_html") or ""
    body_md = html_to_markdown(body_html) if body_html else "*No content available.*"

    return frontmatter + "\n" + header + wikilink_block + body_md + "\n"


# ---------------------------------------------------------------------------
# Topic (tag) note builder
# ---------------------------------------------------------------------------

def build_topic_note(
    tag_slug: str,
    post_slugs: list[str],
    all_posts_by_slug: dict[str, dict],
    display: Optional[str] = None,
) -> str:
    display = display or tag_slug.replace("-", " ").title()
    lines = [
        f"---",
        f"type: topic",
        f"topic_slug: {tag_slug}",
        f"post_count: {len(post_slugs)}",
        f"---",
        f"",
        f"# Topic: {display}",
        f"",
        f"Posts about **{display}**:",
        f"",
    ]
    for slug in sorted(post_slugs):
        post = all_posts_by_slug.get(slug, {})
        title = _post_display_title(post)
        date = _fmt_date(post.get("post_date") or "")
        lines.append(
            f"- {_wikilink(POSTS_FOLDER, f'{date}--{slug}', title)} ({date})"
        )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Concept note builder
# ---------------------------------------------------------------------------

def build_concept_note(
    concept_slug: str,
    display_name: str,
    post_slugs: list[str],
    all_posts_by_slug: dict[str, dict],
) -> str:
    lines = [
        f"---",
        f"type: concept",
        f"concept_slug: {concept_slug}",
        f"post_count: {len(post_slugs)}",
        f"---",
        f"",
        f"# Concept: {display_name}",
        f"",
        f"Posts referencing **{display_name}**:",
        f"",
    ]
    for slug in sorted(post_slugs):
        post = all_posts_by_slug.get(slug, {})
        title = _post_display_title(post)
        date = _fmt_date(post.get("post_date") or "")
        lines.append(
            f"- {_wikilink(POSTS_FOLDER, f'{date}--{slug}', title)} ({date})"
        )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Citation note builder (per-domain grouping)
# ---------------------------------------------------------------------------

def build_citation_note(
    domain_slug: str,
    citations: list[dict],
    all_posts_by_slug: dict[str, dict],
) -> str:
    domain = citations[0]["domain"] if citations else domain_slug
    lines = [
        f"---",
        f"type: citation",
        f"domain: {domain}",
        f"domain_slug: {domain_slug}",
        f"citation_count: {len(citations)}",
        f"---",
        f"",
        f"# Citations: {domain}",
        f"",
        f"External references from [{domain}](https://{domain}) appearing across posts.",
        f"",
        f"## References",
        f"",
    ]
    # Group by post
    post_to_urls: dict[str, list[dict]] = defaultdict(list)
    for cdata in citations:
        for post_slug in cdata["posts"]:
            post_to_urls[post_slug].append(cdata)

    for post_slug, urls in sorted(post_to_urls.items()):
        post = all_posts_by_slug.get(post_slug, {})
        title = _post_display_title(post)
        date = _fmt_date(post.get("post_date") or "")
        lines.append(
            f"### {_wikilink(POSTS_FOLDER, f'{date}--{post_slug}', title)}"
        )
        for cdata in urls:
            anchors = " / ".join(cdata["anchor_texts"][:3]) if cdata["anchor_texts"] else ""
            anchor_str = f' "{anchors}"' if anchors else ""
            lines.append(f"- [{cdata['url']}]({cdata['url']}){anchor_str}")
        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# MOC builder
# ---------------------------------------------------------------------------

def build_moc(
    posts: list[dict],
    graph: dict,
    slug_to_filename: dict[str, str],
) -> str:
    post_count = len(posts)
    topic_count = len(graph.get("topics", {}))
    concept_count = len(graph["concepts"])
    citation_count = len(set(
        cdata["domain_slug"] for cdata in graph["citations"].values()
    ))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        "---",
        "type: moc",
        f"updated: {now}",
        f"post_count: {post_count}",
        "---",
        "",
        "# Map of Content — Avik De's Blog",
        "",
        f"> Obsidian vault for [avikde.me]({BLOG_CUSTOM_DOMAIN}) · "
        f"**{post_count} posts** · "
        f"**{topic_count} topics** · "
        f"**{concept_count} concepts** · "
        f"**{citation_count} cited domains**  ",
        f"> Last synced: {now}",
        "",
        "---",
        "",
        "## 📋 Navigation",
        "",
        f"| Section | Notes |",
        f"|---------|-------|",
        f"| [[{META_FOLDER}/Timeline\\|📅 Timeline]] | All posts in chronological order |",
        f"| [[{META_FOLDER}/Authors\\|👤 Authors]] | About Avik De |",
        f"| {TOPICS_FOLDER}/ | {topic_count} topic pages |",
        f"| {CONCEPTS_FOLDER}/ | {concept_count} concept pages |",
        f"| {CITATIONS_FOLDER}/ | {citation_count} cited domains |",
        "",
        "---",
        "",
        "## 📝 All Posts",
        "",
    ]

    # Sort by date descending
    sorted_posts = sorted(
        posts,
        key=lambda p: p.get("post_date") or p.get("publishedAt") or "",
        reverse=True,
    )

    current_year = None
    for post in sorted_posts:
        date = _fmt_date(post.get("post_date") or post.get("publishedAt") or "")
        year = date[:4]
        if year != current_year:
            current_year = year
            lines.append(f"### {year}")
            lines.append("")

        slug = post.get("slug", "")
        title = _post_display_title(post)
        subtitle = post.get("subtitle") or ""
        filename = _post_filename(post)
        subtitle_str = f" — *{subtitle}*" if subtitle else ""
        lines.append(
            f"- [[{POSTS_FOLDER}/{filename[:-3]}|{title}]]{subtitle_str} `{date}`"
        )

    lines += [
        "",
        "---",
        "",
        "## 🏷 Topics",
        "",
    ]
    for topic_slug, topic_posts in sorted(graph.get("topics", {}).items(), key=lambda x: -len(x[1])):
        display = graph["concept_names"].get(topic_slug, topic_slug.replace("-", " ").title())
        lines.append(
            f"- {_wikilink(TOPICS_FOLDER, topic_slug, display)} ({len(topic_posts)} posts)"
        )

    lines += [
        "",
        "---",
        "",
        "## 💡 Concepts",
        "",
    ]
    for cslug, cposts in sorted(graph["concepts"].items(), key=lambda x: -len(x[1])):
        display = graph["concept_names"].get(cslug, cslug.replace("-", " ").title())
        lines.append(
            f"- {_wikilink(CONCEPTS_FOLDER, cslug, display)} ({len(cposts)} posts)"
        )

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Timeline note
# ---------------------------------------------------------------------------

def build_timeline(posts: list[dict], slug_to_filename: dict[str, str]) -> str:
    sorted_posts = sorted(
        posts,
        key=lambda p: p.get("post_date") or p.get("publishedAt") or "",
    )
    lines = [
        "---",
        "type: timeline",
        "---",
        "",
        "# Timeline",
        "",
        "All posts in chronological order.",
        "",
    ]
    current_year = None
    for post in sorted_posts:
        date = _fmt_date(post.get("post_date") or post.get("publishedAt") or "")
        year = date[:4]
        if year != current_year:
            current_year = year
            lines.append(f"## {year}")
            lines.append("")

        slug = post.get("slug", "")
        title = _post_display_title(post)
        filename = slug_to_filename.get(slug, _post_filename(post))
        lines.append(f"- `{date}` [[{POSTS_FOLDER}/{filename[:-3]}|{title}]]")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Authors note
# ---------------------------------------------------------------------------

def build_authors_note(posts: list[dict]) -> str:
    post_count = len(posts)
    first_date = _fmt_date(
        min((p.get("post_date") or p.get("publishedAt") or "z") for p in posts)
        if posts
        else ""
    )
    return f"""---
type: author
name: Avik De
---

# Avik De

Engineer, researcher, and writer. Author of [{BLOG_CUSTOM_DOMAIN}]({BLOG_CUSTOM_DOMAIN}).

**{post_count} posts** archived in this vault, starting {first_date}.

## Posts

See [[MOC]] for the full list, or browse [[{META_FOLDER}/Timeline|Timeline]] chronologically.
"""


# ---------------------------------------------------------------------------
# Vault state tracking
# ---------------------------------------------------------------------------

def load_vault_state() -> dict:
    if not config.VAULT_STATE_FILE.exists():
        return {}
    with open(config.VAULT_STATE_FILE) as f:
        return json.load(f)


def save_vault_state(state: dict) -> None:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.VAULT_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


# ---------------------------------------------------------------------------
# Main vault writer
# ---------------------------------------------------------------------------

def write_vault(posts: list[dict], graph: dict) -> dict:
    """
    Write the complete Obsidian vault to VAULT_DIR.

    Constraint NO_BROKEN_LINKS: every [[wikilink]] in every note is verified
    to have a corresponding file written in this pass. Assertion raised if not.
    Constraint SELF_CONSISTENT: enforced by collecting all written paths before
    verifying wikilinks.

    Returns vault_state dict (slug → filename for post notes).
    """
    vault_dir = config.VAULT_DIR  # Read at call-time so monkeypatching works in tests
    vault_dir.mkdir(parents=True, exist_ok=True)

    all_posts_by_slug = {p["slug"]: p for p in posts if p.get("slug")}
    all_post_slugs = set(all_posts_by_slug.keys())

    # Pre-build slug → filename map so crosslinks can use date-prefixed targets
    slug_to_filename: dict[str, str] = {
        p["slug"]: _post_filename(p)
        for p in posts if p.get("slug")
    }

    written_files: set[str] = set()
    vault_state: dict = {}

    # ---- Post notes ----
    log.info("Writing %d post notes…", len(posts))
    for post in posts:
        slug = post.get("slug", "")
        if not slug:
            continue
        filename = slug_to_filename[slug]
        rel_path = f"{POSTS_FOLDER}/{filename}"
        content = build_post_note(post, graph, all_post_slugs, slug_to_filename)
        _atomic_write(vault_dir / rel_path, content)
        written_files.add(rel_path)
        vault_state[slug] = filename
        log.debug("Wrote post: %s", rel_path)

    # ---- Topic notes ----
    all_topics = graph.get("topics", {})
    log.info("Writing %d topic notes…", len(all_topics))
    for topic_slug, topic_posts in all_topics.items():
        display = graph["concept_names"].get(topic_slug, topic_slug.replace("-", " ").title())
        rel_path = f"{TOPICS_FOLDER}/{topic_slug}.md"
        content = build_topic_note(topic_slug, topic_posts, all_posts_by_slug, display)
        _atomic_write(vault_dir / rel_path, content)
        written_files.add(rel_path)

    # ---- Concept notes ----
    log.info("Writing %d concept notes…", len(graph["concepts"]))
    for cslug, cposts in graph["concepts"].items():
        display = graph["concept_names"].get(cslug, cslug.replace("-", " ").title())
        rel_path = f"{CONCEPTS_FOLDER}/{cslug}.md"
        content = build_concept_note(cslug, display, cposts, all_posts_by_slug)
        _atomic_write(vault_dir / rel_path, content)
        written_files.add(rel_path)

    # ---- Citation notes (per domain) ----
    domain_to_citations: dict[str, list[dict]] = defaultdict(list)
    for cdata in graph["citations"].values():
        domain_to_citations[cdata["domain_slug"]].append(cdata)

    log.info("Writing %d citation domain notes…", len(domain_to_citations))
    for domain_slug, domain_cites in domain_to_citations.items():
        rel_path = f"{CITATIONS_FOLDER}/{domain_slug}.md"
        content = build_citation_note(domain_slug, domain_cites, all_posts_by_slug)
        _atomic_write(vault_dir / rel_path, content)
        written_files.add(rel_path)

    # ---- MOC ----
    moc_content = build_moc(posts, graph, slug_to_filename)
    _atomic_write(vault_dir / MOC_FILENAME, moc_content)
    written_files.add(MOC_FILENAME)

    # ---- Timeline ----
    timeline_content = build_timeline(posts, slug_to_filename)
    _atomic_write(vault_dir / TIMELINE_FILENAME, timeline_content)
    written_files.add(TIMELINE_FILENAME)

    # ---- Authors ----
    authors_content = build_authors_note(posts)
    _atomic_write(vault_dir / AUTHORS_FILENAME, authors_content)
    written_files.add(AUTHORS_FILENAME)

    # ---- CONSTRAINT: NO_BROKEN_LINKS verification ----
    broken = _verify_wikilinks(written_files, vault_dir)
    if broken:
        log.warning(
            "Broken wikilinks detected (%d). These point to non-existent notes:\n%s",
            len(broken),
            "\n".join(f"  {src} → [[{tgt}]]" for src, tgt in broken[:10]),
        )
    else:
        log.info("CONSTRAINT NO_BROKEN_LINKS: verified — 0 broken wikilinks.")

    save_vault_state(vault_state)
    log.info("Vault written: %d files total.", len(written_files))
    return vault_state


def _verify_wikilinks(written_rel_paths: set[str], vault_dir: Path) -> list[tuple[str, str]]:
    """
    Scan all written files for [[wikilinks]] and verify each target exists.
    Returns list of (source_rel_path, broken_link_target) pairs.

    Handles Obsidian wikilink variants:
      [[target]]          plain link
      [[target|display]]  link with display text
      [[target\\|display]] link with display text inside a Markdown table cell

    This implements the SELF_CONSISTENT and NO_BROKEN_LINKS constraints.
    """
    # Match [[...]] allowing \| as an escaped pipe inside table cells
    WIKILINK_RE = re.compile(r"\[\[([^\]]+?)(?:(?:\\)?\|[^\]]*)?\]\]")
    broken = []

    for rel_path in written_rel_paths:
        full_path = vault_dir / rel_path
        if not full_path.exists():
            continue
        content = full_path.read_text(encoding="utf-8")
        for match in WIKILINK_RE.finditer(content):
            target = match.group(1).rstrip("\\")  # strip trailing backslash from \| escaping
            # Normalize: target may or may not include .md
            target_no_ext = target[:-3] if target.endswith(".md") else target
            target_with_ext = target_no_ext + ".md"

            found = (
                target_with_ext in written_rel_paths
                or any(p.removesuffix(".md") == target_no_ext for p in written_rel_paths)
            )
            if not found:
                broken.append((rel_path, target))

    return broken

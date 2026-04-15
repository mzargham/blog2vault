"""
sync.py — Main orchestrator for the avikde-vault pipeline.

Usage:
    python scripts/sync.py [--force] [--dry-run] [--no-ai]

Options:
    --force     Rebuild all notes even if no new posts detected.
    --dry-run   Fetch and compare, report what would change, write nothing.
    --no-ai     Skip Anthropic API extraction, use TF-IDF only.

Exit codes:
    0  Success (no new posts, or new posts processed)
    1  Fatal error (network, parse, file I/O)
    2  New posts found (useful for CI/CD conditional steps)

Pipeline stages (in order):
    1. DISCOVER  — find canonical Substack base URL
    2. FETCH     — paginate API, hydrate full bodies
    3. CACHE     — update data/posts_cache.json
    4. DIFF      — identify new/updated posts vs cache
    5. EXTRACT   — run concept/tag/citation extraction on full corpus
    6. BUILD     — generate all vault notes
    7. REPORT    — print summary, set GitHub Actions outputs if in CI

Constraints enforced throughout:
    - DISCOVERY_FALLBACK: proceeds with fallback URL on discovery failure
    - INCREMENTAL: on no-change, skips BUILD unless --force
    - DRY_RUN: no files written, no cache mutated when --dry-run
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Allow running from repo root or scripts/ directory
sys.path.insert(0, str(Path(__file__).parent))

import config  # noqa: E402 — must come after sys.path
from scrape import (  # noqa: E402
    discover_substack_base_url,
    fetch_all_posts,
    load_cache,
    save_cache,
    get_new_slugs,
)
from extract import run_extraction  # noqa: E402
from vault import write_vault, load_vault_state  # noqa: E402

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("sync")


# ---------------------------------------------------------------------------
# GitHub Actions output helpers
# ---------------------------------------------------------------------------

def _gha_output(key: str, value: str) -> None:
    """Write a GitHub Actions step output variable."""
    output_file = os.getenv("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"{key}={value}\n")
    else:
        log.info("GHA output: %s=%s", key, value)


def _gha_summary(markdown: str) -> None:
    """Append to GitHub Actions step summary."""
    summary_file = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a") as f:
            f.write(markdown + "\n")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run(force: bool = False, dry_run: bool = False, no_ai: bool = False) -> int:
    """
    Execute the full sync pipeline.
    Returns exit code (0=ok, 1=error, 2=new posts found).
    """
    if no_ai:
        os.environ["USE_AI_EXTRACTION"] = "false"

    # ---- Stage 1: DISCOVER ----
    log.info("=== Stage 1: DISCOVER ===")
    try:
        base_url = discover_substack_base_url(config.BLOG_CUSTOM_DOMAIN)
        log.info("Base URL: %s", base_url)
    except Exception as exc:
        log.error("Discovery failed: %s", exc)
        return 1

    # ---- Stage 2: FETCH ----
    log.info("=== Stage 2: FETCH ===")
    try:
        live_posts = fetch_all_posts(base_url)
        log.info("Fetched %d public posts from API", len(live_posts))
    except Exception as exc:
        log.error("Fetch failed: %s", exc)
        return 1

    if not live_posts:
        log.warning("No public posts returned from API. Aborting.")
        return 1

    # ---- Stage 3: CACHE ----
    log.info("=== Stage 3: CACHE ===")
    cache = load_cache()

    if not dry_run:
        save_cache(live_posts)
        cache = load_cache()  # Reload after save

    # ---- Stage 4: DIFF ----
    log.info("=== Stage 4: DIFF ===")
    new_slugs = get_new_slugs(live_posts, load_cache() if dry_run else {})
    # In non-dry-run mode, compare against pre-save cache
    pre_save_cache = load_cache()
    new_posts = [p for p in live_posts if p.get("slug") in
                 {p["slug"] for p in live_posts} - set(pre_save_cache.keys() if not dry_run else load_cache().keys())]

    # Simpler diff: what slugs in live_posts weren't in the cache before this run
    vault_state = load_vault_state()
    unbuilt_slugs = [p["slug"] for p in live_posts if p.get("slug") not in vault_state]
    log.info("Posts not yet in vault: %d", len(unbuilt_slugs))

    if not unbuilt_slugs and not force:
        log.info("No new posts and --force not set. Nothing to do.")
        _gha_output("new_posts", "0")
        _gha_output("new_post_titles", "")
        _gha_summary("## ✅ avikde-vault sync\n\nNo new posts found. Vault is up to date.")
        return 0

    # ---- Stage 5: EXTRACT ----
    log.info("=== Stage 5: EXTRACT (full corpus) ===")
    try:
        # Always extract on the full corpus so concept/wikilink graph is coherent
        all_posts = list({p["slug"]: p for p in live_posts if p.get("slug")}.values())
        graph = run_extraction(all_posts)
    except Exception as exc:
        log.error("Extraction failed: %s", exc)
        return 1

    # ---- Stage 6: BUILD ----
    log.info("=== Stage 6: BUILD ===")
    if dry_run:
        log.info("DRY RUN: skipping vault write.")
        log.info("Would write %d post notes, %d topic notes, %d concept notes, %d citation domains.",
                 len(all_posts),
                 len(graph["tags"]) + len(graph.get("themes", {})),
                 len(graph["concepts"]),
                 len({c["domain_slug"] for c in graph["citations"].values()}))
    else:
        try:
            write_vault(all_posts, graph)
        except Exception as exc:
            log.error("Vault build failed: %s", exc)
            return 1

    # ---- Stage 7: REPORT ----
    log.info("=== Stage 7: REPORT ===")
    new_titles = [p.get("title", p.get("slug")) for p in live_posts
                  if p.get("slug") in unbuilt_slugs]

    _gha_output("new_posts", str(len(unbuilt_slugs)))
    _gha_output("new_post_titles", "; ".join(new_titles[:5]))

    summary_lines = [
        "## ✅ avikde-vault sync",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total posts | {len(all_posts)} |",
        f"| New posts this run | {len(unbuilt_slugs)} |",
        f"| Topics | {len(graph['tags']) + len(graph.get('themes', {}))} |",
        f"| Concepts | {len(graph['concepts'])} |",
        f"| Cited domains | {len({c['domain_slug'] for c in graph['citations'].values()})} |",
    ]
    if new_titles:
        summary_lines += ["", "### New posts", ""] + [f"- {t}" for t in new_titles]

    _gha_summary("\n".join(summary_lines))

    log.info(
        "Sync complete. %d new posts, %d total, %d concepts, %d topics.",
        len(unbuilt_slugs),
        len(all_posts),
        len(graph["concepts"]),
        len(graph["tags"]) + len(graph.get("themes", {})),
    )

    return 2 if unbuilt_slugs else 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync Avik De's Substack blog → Obsidian vault."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild all vault notes even if no new posts detected.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and diff only; write nothing.",
    )
    parser.add_argument(
        "--no-ai",
        action="store_true",
        help="Skip Anthropic API extraction; use TF-IDF only.",
    )
    args = parser.parse_args()

    exit_code = run(force=args.force, dry_run=args.dry_run, no_ai=args.no_ai)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

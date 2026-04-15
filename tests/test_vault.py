"""Tests for vault.py — formatters, note builders, file I/O, wikilink verification."""

import json
import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Formatter / helper tests
# ---------------------------------------------------------------------------


class TestFmtDate:
    def test_iso_datetime(self):
        from vault import _fmt_date

        assert _fmt_date("2024-03-15T10:30:00Z") == "2024-03-15"

    def test_iso_with_offset(self):
        from vault import _fmt_date

        assert _fmt_date("2024-03-15T10:30:00+05:00") == "2024-03-15"

    def test_invalid_string(self):
        from vault import _fmt_date

        result = _fmt_date("garbage-text")
        assert result == "garbage-te"  # first 10 chars

    def test_empty_string(self):
        from vault import _fmt_date

        assert _fmt_date("") == "unknown"


class TestPostFilename:
    def test_basic(self, sample_post):
        from vault import _post_filename

        result = _post_filename(sample_post)
        assert result == "2024-03-15--control-theory-basics.md"

    def test_uses_publishedAt_fallback(self):
        from vault import _post_filename

        post = {"slug": "test", "publishedAt": "2024-06-01T00:00:00Z"}
        result = _post_filename(post)
        assert result == "2024-06-01--test.md"


class TestPostDisplayTitle:
    def test_with_title(self):
        from vault import _post_display_title

        assert _post_display_title({"title": "My Title"}) == "My Title"

    def test_fallback_slug(self):
        from vault import _post_display_title

        assert _post_display_title({"slug": "my-slug"}) == "my-slug"

    def test_fallback_untitled(self):
        from vault import _post_display_title

        assert _post_display_title({}) == "Untitled"


class TestWikilink:
    def test_simple(self):
        from vault import _wikilink

        assert _wikilink("topics", "foo") == "[[topics/foo]]"

    def test_with_display(self):
        from vault import _wikilink

        assert _wikilink("topics", "foo", "Foo Bar") == "[[topics/foo|Foo Bar]]"


# ---------------------------------------------------------------------------
# Atomic write
# ---------------------------------------------------------------------------


class TestAtomicWrite:
    def test_writes_content(self, tmp_path):
        from vault import _atomic_write

        target = tmp_path / "test.md"
        _atomic_write(target, "hello world")
        assert target.read_text() == "hello world"

    def test_creates_parent_dirs(self, tmp_path):
        from vault import _atomic_write

        target = tmp_path / "sub" / "dir" / "test.md"
        _atomic_write(target, "nested content")
        assert target.exists()
        assert target.read_text() == "nested content"


# ---------------------------------------------------------------------------
# Note builder tests
# ---------------------------------------------------------------------------


class TestBuildPostNote:
    def test_has_frontmatter(self, sample_post, mock_graph):
        from vault import build_post_note

        slug_to_filename = {"control-theory-basics": "2024-03-15--control-theory-basics.md"}
        result = build_post_note(
            sample_post, mock_graph, {"control-theory-basics"}, slug_to_filename
        )
        assert result.startswith("---\n")
        assert 'title: "Control Theory Basics for Engineers"' in result
        assert "date: 2024-03-15" in result
        assert "slug: control-theory-basics" in result

    def test_has_wikilinks(self, sample_post, mock_graph):
        from vault import build_post_note

        slug_to_filename = {"control-theory-basics": "2024-03-15--control-theory-basics.md"}
        result = build_post_note(
            sample_post, mock_graph, {"control-theory-basics"}, slug_to_filename
        )
        assert "[[topics/" in result
        assert "[[concepts/" in result

    def test_body_converted_to_markdown(self, sample_post, mock_graph):
        from vault import build_post_note

        slug_to_filename = {"control-theory-basics": "2024-03-15--control-theory-basics.md"}
        result = build_post_note(
            sample_post, mock_graph, {"control-theory-basics"}, slug_to_filename
        )
        # HTML should be converted - check heading is present
        assert "Introduction" in result
        assert "Control theory is a branch" in result

    def test_cover_image_included(self, sample_post, mock_graph):
        from vault import build_post_note

        slug_to_filename = {"control-theory-basics": "2024-03-15--control-theory-basics.md"}
        result = build_post_note(
            sample_post, mock_graph, {"control-theory-basics"}, slug_to_filename
        )
        assert "https://cdn.example.com/cover1.jpg" in result

    def test_crosslinks_validated(self, sample_post, mock_graph):
        from vault import build_post_note

        # crosslinks reference "control-theory-basics" from "token-engineering"
        # But if we build note for a post that has crosslinks to unknown slugs, they get filtered
        post = {
            "slug": "token-engineering",
            "title": "Token Engineering",
            "post_date": "2024-04-20T12:00:00Z",
            "body_html": "<p>Test</p>",
        }
        slug_to_filename = {
            "token-engineering": "2024-04-20--token-engineering.md",
            "control-theory-basics": "2024-03-15--control-theory-basics.md",
        }
        result = build_post_note(
            post,
            mock_graph,
            {"token-engineering", "control-theory-basics"},
            slug_to_filename,
        )
        assert "See Also" in result


class TestBuildTopicNote:
    def test_basic(self, sample_post):
        from vault import build_topic_note

        posts_by_slug = {"control-theory-basics": sample_post}
        result = build_topic_note("engineering", ["control-theory-basics"], posts_by_slug)
        assert "# Topic: Engineering" in result
        assert "type: topic" in result
        assert "[[posts/" in result

    def test_post_count_in_frontmatter(self, sample_post):
        from vault import build_topic_note

        posts_by_slug = {"control-theory-basics": sample_post}
        result = build_topic_note("engineering", ["control-theory-basics"], posts_by_slug)
        assert "post_count: 1" in result


class TestBuildConceptNote:
    def test_basic(self, sample_post):
        from vault import build_concept_note

        posts_by_slug = {"control-theory-basics": sample_post}
        result = build_concept_note(
            "feedback-loops", "Feedback Loops", ["control-theory-basics"], posts_by_slug
        )
        assert "# Concept: Feedback Loops" in result
        assert "type: concept" in result
        assert "[[posts/" in result


class TestBuildCitationNote:
    def test_basic(self, sample_post):
        from vault import build_citation_note

        citations = [
            {
                "url": "https://arxiv.org/abs/123",
                "domain": "arxiv.org",
                "domain_slug": "arxiv-org",
                "posts": ["control-theory-basics"],
                "anchor_texts": ["paper link"],
            }
        ]
        posts_by_slug = {"control-theory-basics": sample_post}
        result = build_citation_note("arxiv-org", citations, posts_by_slug)
        assert "# Citations: arxiv.org" in result
        assert "https://arxiv.org/abs/123" in result
        assert "[[posts/" in result


class TestBuildMoc:
    def test_has_sections(self, public_posts, mock_graph):
        from vault import build_moc

        slug_to_filename = {
            p["slug"]: f"{p['post_date'][:10]}--{p['slug']}.md" for p in public_posts
        }
        result = build_moc(public_posts, mock_graph, slug_to_filename)
        assert "Map of Content" in result
        assert "All Posts" in result
        assert "Topics" in result
        assert "Concepts" in result


class TestBuildTimeline:
    def test_chronological_order(self, public_posts):
        from vault import build_timeline

        slug_to_filename = {
            p["slug"]: f"{p['post_date'][:10]}--{p['slug']}.md" for p in public_posts
        }
        result = build_timeline(public_posts, slug_to_filename)
        assert "# Timeline" in result
        # Check years appear
        assert "2024" in result

    def test_has_post_links(self, public_posts):
        from vault import build_timeline

        slug_to_filename = {
            p["slug"]: f"{p['post_date'][:10]}--{p['slug']}.md" for p in public_posts
        }
        result = build_timeline(public_posts, slug_to_filename)
        assert "[[posts/" in result


class TestBuildAuthorsNote:
    def test_content(self, public_posts):
        from vault import build_authors_note

        result = build_authors_note(public_posts)
        assert "Avik De" in result
        assert "type: author" in result
        assert f"{len(public_posts)} posts" in result


# ---------------------------------------------------------------------------
# Vault state I/O
# ---------------------------------------------------------------------------


class TestVaultState:
    def test_load_missing_returns_empty(self, patch_config_paths):
        from vault import load_vault_state

        assert load_vault_state() == {}

    def test_roundtrip(self, patch_config_paths):
        from vault import save_vault_state, load_vault_state

        state = {"post-a": "2024-01-01--post-a.md", "post-b": "2024-02-01--post-b.md"}
        save_vault_state(state)
        loaded = load_vault_state()
        assert loaded == state


# ---------------------------------------------------------------------------
# write_vault integration
# ---------------------------------------------------------------------------


class TestWriteVault:
    def test_creates_directory_structure(self, patch_config_paths, public_posts, mock_graph):
        from vault import write_vault

        vault_dir = patch_config_paths["vault_dir"]
        vault_state = write_vault(public_posts, mock_graph)

        assert (vault_dir / "posts").is_dir()
        assert (vault_dir / "topics").is_dir()
        assert (vault_dir / "concepts").is_dir()
        assert (vault_dir / "MOC.md").exists()
        assert (vault_dir / "_meta" / "Timeline.md").exists()
        assert (vault_dir / "_meta" / "Authors.md").exists()

        # Should have post notes
        post_files = list((vault_dir / "posts").glob("*.md"))
        assert len(post_files) == len(public_posts)

        # vault_state should map slug → filename
        assert len(vault_state) == len(public_posts)


# ---------------------------------------------------------------------------
# Wikilink verification
# ---------------------------------------------------------------------------


class TestVerifyWikilinks:
    def test_no_broken_links(self, tmp_path):
        from vault import _verify_wikilinks

        (tmp_path / "posts").mkdir()
        (tmp_path / "topics").mkdir()
        (tmp_path / "posts" / "2024-01-01--test.md").write_text(
            "Link to [[topics/engineering]]"
        )
        (tmp_path / "topics" / "engineering.md").write_text("# Engineering")

        written = {"posts/2024-01-01--test.md", "topics/engineering.md"}
        broken = _verify_wikilinks(written, tmp_path)
        assert broken == []

    def test_detects_broken_link(self, tmp_path):
        from vault import _verify_wikilinks

        (tmp_path / "posts").mkdir()
        (tmp_path / "posts" / "test.md").write_text("Link to [[topics/nonexistent]]")

        written = {"posts/test.md"}
        broken = _verify_wikilinks(written, tmp_path)
        assert len(broken) == 1
        assert broken[0][1] == "topics/nonexistent"

    def test_handles_display_text(self, tmp_path):
        from vault import _verify_wikilinks

        (tmp_path / "posts").mkdir()
        (tmp_path / "topics").mkdir()
        (tmp_path / "posts" / "test.md").write_text(
            "Link to [[topics/engineering|Engineering]]"
        )
        (tmp_path / "topics" / "engineering.md").write_text("# Engineering")

        written = {"posts/test.md", "topics/engineering.md"}
        broken = _verify_wikilinks(written, tmp_path)
        assert broken == []

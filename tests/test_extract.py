"""Tests for extract.py — HTML conversion, tags, TF-IDF, AI mock, citations, crosslinks."""

import json
from collections import defaultdict
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# html_to_text / html_to_markdown
# ---------------------------------------------------------------------------


class TestHtmlToText:
    def test_basic(self):
        from extract import html_to_text

        result = html_to_text("<p>Hello <b>world</b></p>")
        assert "Hello" in result
        assert "world" in result

    def test_strips_links(self):
        from extract import html_to_text

        result = html_to_text('<p>See <a href="https://example.com">this</a></p>')
        assert "this" in result
        assert "https://example.com" not in result

    def test_empty_string(self):
        from extract import html_to_text

        assert html_to_text("") == ""

    def test_none_like_falsy(self):
        from extract import html_to_text

        assert html_to_text("") == ""


class TestHtmlToMarkdown:
    def test_preserves_links(self):
        from extract import html_to_markdown

        result = html_to_markdown('<p>Visit <a href="https://example.com">here</a></p>')
        assert "https://example.com" in result
        assert "here" in result

    def test_preserves_images(self):
        from extract import html_to_markdown

        result = html_to_markdown('<img src="https://example.com/img.jpg" alt="photo">')
        assert "https://example.com/img.jpg" in result


# ---------------------------------------------------------------------------
# extract_tags
# ---------------------------------------------------------------------------


class TestExtractTags:
    def test_dict_format_tags(self):
        from extract import extract_tags

        posts = [
            {
                "slug": "post-1",
                "postTags": [
                    {"name": "Engineering", "slug": "engineering"},
                    {"name": "Math", "slug": "math"},
                ],
            }
        ]
        result = extract_tags(posts)
        assert "engineering" in result
        assert "math" in result
        assert "post-1" in result["engineering"]

    def test_string_format_tags(self):
        from extract import extract_tags

        posts = [{"slug": "post-2", "tags": ["Networks", "Graph Theory"]}]
        result = extract_tags(posts)
        assert "networks" in result
        assert "graph-theory" in result
        assert "post-2" in result["networks"]

    def test_no_tags(self):
        from extract import extract_tags

        posts = [{"slug": "post-3"}]
        result = extract_tags(posts)
        assert result == {}

    def test_multiple_posts_same_tag(self):
        from extract import extract_tags

        posts = [
            {"slug": "a", "postTags": [{"name": "Eng", "slug": "eng"}]},
            {"slug": "b", "postTags": [{"name": "Eng", "slug": "eng"}]},
        ]
        result = extract_tags(posts)
        assert sorted(result["eng"]) == ["a", "b"]


# ---------------------------------------------------------------------------
# _normalize_url
# ---------------------------------------------------------------------------


class TestNormalizeUrl:
    def test_strips_query_and_fragment(self):
        from extract import _normalize_url

        result = _normalize_url("https://example.com/path?q=1#section")
        assert result == "https://example.com/path"

    def test_skips_substack_domain(self):
        from extract import _normalize_url

        assert _normalize_url("https://avikde.substack.com/p/post") is None

    def test_skips_twitter(self):
        from extract import _normalize_url

        assert _normalize_url("https://twitter.com/user") is None

    def test_skips_x_com(self):
        from extract import _normalize_url

        assert _normalize_url("https://x.com/user") is None

    def test_non_http_returns_none(self):
        from extract import _normalize_url

        assert _normalize_url("mailto:test@example.com") is None
        assert _normalize_url("javascript:void(0)") is None

    def test_valid_url_preserved(self):
        from extract import _normalize_url

        result = _normalize_url("https://arxiv.org/abs/2301.00001")
        assert result == "https://arxiv.org/abs/2301.00001"

    def test_trailing_slash_stripped(self):
        from extract import _normalize_url

        result = _normalize_url("https://example.com/path/")
        assert result == "https://example.com/path"


# ---------------------------------------------------------------------------
# extract_citations
# ---------------------------------------------------------------------------


class TestExtractCitations:
    def test_basic_extraction(self):
        from extract import extract_citations

        posts = [
            {
                "slug": "post-1",
                "body_html": '<p>See <a href="https://arxiv.org/abs/123">paper</a></p>',
            }
        ]
        result = extract_citations(posts)
        assert len(result) == 1
        url = list(result.keys())[0]
        assert result[url]["domain"] == "arxiv.org"
        assert "post-1" in result[url]["posts"]
        assert "paper" in result[url]["anchor_texts"]

    def test_deduplicates_across_posts(self):
        from extract import extract_citations

        posts = [
            {
                "slug": "a",
                "body_html": '<a href="https://arxiv.org/abs/123">link1</a>',
            },
            {
                "slug": "b",
                "body_html": '<a href="https://arxiv.org/abs/123">link2</a>',
            },
        ]
        result = extract_citations(posts)
        assert len(result) == 1
        url = list(result.keys())[0]
        assert sorted(result[url]["posts"]) == ["a", "b"]

    def test_skips_infrastructure_domains(self):
        from extract import extract_citations

        posts = [
            {
                "slug": "a",
                "body_html": (
                    '<a href="https://twitter.com/user">tweet</a>'
                    '<a href="https://cdn.substack.com/img.jpg">img</a>'
                ),
            }
        ]
        result = extract_citations(posts)
        assert len(result) == 0

    def test_no_body_html(self):
        from extract import extract_citations

        posts = [{"slug": "empty"}]
        result = extract_citations(posts)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# infer_post_crosslinks
# ---------------------------------------------------------------------------


class TestInferPostCrosslinks:
    def test_detects_title_mention(self):
        from extract import infer_post_crosslinks

        posts = [
            {
                "slug": "a",
                "title": "Control Theory Basics for Engineers",
                "body_html": "<p>Short A</p>",
            },
            {
                "slug": "b",
                "title": "Token Engineering",
                "body_html": "<p>Building on Control Theory Basics for Engineers we see...</p>",
            },
        ]
        result = infer_post_crosslinks(posts)
        assert "b" in result
        assert "a" in result["b"]

    def test_ignores_self_reference(self):
        from extract import infer_post_crosslinks

        posts = [
            {
                "slug": "a",
                "title": "A Very Long Title Here",
                "body_html": "<p>This post A Very Long Title Here is about...</p>",
            },
        ]
        result = infer_post_crosslinks(posts)
        assert "a" not in result

    def test_ignores_short_titles(self):
        from extract import infer_post_crosslinks

        posts = [
            {"slug": "a", "title": "Networks", "body_html": "<p>Short</p>"},
            {"slug": "b", "title": "Other Post Title", "body_html": "<p>Networks are cool</p>"},
        ]
        result = infer_post_crosslinks(posts)
        # "Networks" is only 8 chars, should not match
        assert "b" not in result


# ---------------------------------------------------------------------------
# extract_concepts_tfidf
# ---------------------------------------------------------------------------


class TestExtractConceptsTfidf:
    def test_basic_extraction(self, public_posts):
        from extract import extract_concepts_tfidf

        concepts, display = extract_concepts_tfidf(public_posts)
        # Should extract some concepts from 4 posts
        assert len(concepts) > 0
        assert len(display) > 0
        # Every concept should map to a list of post slugs
        for slug_list in concepts.values():
            assert isinstance(slug_list, list)
            assert len(slug_list) >= 2  # min_df=2

    def test_too_few_posts(self):
        from extract import extract_concepts_tfidf

        posts = [{"slug": "only", "title": "Solo", "body_html": "<p>text</p>"}]
        concepts, display = extract_concepts_tfidf(posts)
        assert concepts == {}
        assert display == {}


# ---------------------------------------------------------------------------
# extract_concepts_ai
# ---------------------------------------------------------------------------


class TestExtractConceptsAi:
    def test_no_api_key_returns_empty(self, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from extract import extract_concepts_ai

        concepts, display, post_topic = extract_concepts_ai([{"slug": "test"}])
        assert concepts == {}
        assert display == {}
        assert post_topic == {}

    def test_mocked_extraction(self, monkeypatch, patch_config_paths):
        import extract
        import config

        monkeypatch.setattr(extract, "CONCEPTS_CACHE_FILE", config.CONCEPTS_CACHE_FILE)
        monkeypatch.setattr(extract, "DATA_DIR", config.DATA_DIR)
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(
                text=json.dumps(
                    {
                        "topic": "Feedback Control Systems",
                        "concepts": ["Feedback Loops", "PID Control", "Stability Analysis"],
                    }
                )
            )
        ]

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response

        mock_anthropic = MagicMock()
        mock_anthropic.Anthropic.return_value = mock_client

        with patch.dict("sys.modules", {"anthropic": mock_anthropic}):
            concepts, display, post_topic = extract.extract_concepts_ai(
                [
                    {
                        "slug": "test-post",
                        "title": "Test",
                        "subtitle": "",
                        "body_html": "<p>Test body content</p>",
                        "updated_at": "2024-01-01",
                    }
                ]
            )

        assert "feedback-loops" in concepts
        assert "pid-control" in concepts
        assert "stability-analysis" in concepts
        assert post_topic["test-post"] == "feedback-control-systems"
        assert display["feedback-loops"] == "Feedback Loops"
        assert display["feedback-control-systems"] == "Feedback Control Systems"


# ---------------------------------------------------------------------------
# run_extraction
# ---------------------------------------------------------------------------


class TestRunExtraction:
    def test_returns_all_graph_keys(self, public_posts, monkeypatch):
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        from extract import run_extraction

        graph = run_extraction(public_posts)
        assert "tags" in graph
        assert "topics" in graph
        assert "post_topic" in graph
        assert "concepts" in graph
        assert "concept_names" in graph
        assert "citations" in graph
        assert "crosslinks" in graph

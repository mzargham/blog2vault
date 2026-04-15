"""Tests for scrape.py — HTTP mocking, cache I/O, and pure logic."""

import json
from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Pure logic tests
# ---------------------------------------------------------------------------


class TestIsBodyTruncated:
    def test_short_body(self):
        from scrape import _is_body_truncated

        assert _is_body_truncated("abc") is True

    def test_none_body(self):
        from scrape import _is_body_truncated

        assert _is_body_truncated(None) is True

    def test_empty_body(self):
        from scrape import _is_body_truncated

        assert _is_body_truncated("") is True

    def test_long_body(self):
        from scrape import _is_body_truncated

        assert _is_body_truncated("x" * 700) is False

    def test_boundary_599(self):
        from scrape import _is_body_truncated

        assert _is_body_truncated("x" * 599) is True

    def test_boundary_600(self):
        from scrape import _is_body_truncated

        assert _is_body_truncated("x" * 600) is False


class TestGetNewSlugs:
    def test_basic(self):
        from scrape import get_new_slugs

        posts = [{"slug": "a"}, {"slug": "b"}, {"slug": "c"}]
        cache = {"a": {}, "b": {}}
        assert get_new_slugs(posts, cache) == ["c"]

    def test_empty_cache(self):
        from scrape import get_new_slugs

        posts = [{"slug": "x"}, {"slug": "y"}]
        assert get_new_slugs(posts, {}) == ["x", "y"]

    def test_all_cached(self):
        from scrape import get_new_slugs

        posts = [{"slug": "a"}]
        cache = {"a": {}}
        assert get_new_slugs(posts, cache) == []


# ---------------------------------------------------------------------------
# Cache I/O tests (use tmp_path via patch_config_paths)
# ---------------------------------------------------------------------------


class TestCache:
    def test_load_cache_missing_file(self, patch_config_paths, monkeypatch):
        import scrape
        import config

        monkeypatch.setattr(scrape, "POSTS_CACHE_FILE", config.POSTS_CACHE_FILE)
        result = scrape.load_cache()
        assert result == {}

    def test_save_and_load_roundtrip(self, patch_config_paths, monkeypatch):
        import scrape
        import config

        monkeypatch.setattr(scrape, "POSTS_CACHE_FILE", config.POSTS_CACHE_FILE)
        monkeypatch.setattr(scrape, "DATA_DIR", config.DATA_DIR)

        posts = [
            {"slug": "a", "title": "Post A", "updated_at": "2024-01-01"},
            {"slug": "b", "title": "Post B", "updated_at": "2024-02-01"},
        ]
        scrape.save_cache(posts)
        loaded = scrape.load_cache()
        assert "a" in loaded
        assert "b" in loaded
        assert loaded["a"]["title"] == "Post A"

    def test_cache_stable_no_overwrite_older(self, patch_config_paths, monkeypatch):
        import scrape
        import config

        monkeypatch.setattr(scrape, "POSTS_CACHE_FILE", config.POSTS_CACHE_FILE)
        monkeypatch.setattr(scrape, "DATA_DIR", config.DATA_DIR)

        # Save initial version
        scrape.save_cache([{"slug": "a", "title": "New", "updated_at": "2024-06-01"}])
        # Try to overwrite with older timestamp
        scrape.save_cache([{"slug": "a", "title": "Old", "updated_at": "2024-01-01"}])

        loaded = scrape.load_cache()
        assert loaded["a"]["title"] == "New"  # Not overwritten

    def test_cache_overwrites_newer(self, patch_config_paths, monkeypatch):
        import scrape
        import config

        monkeypatch.setattr(scrape, "POSTS_CACHE_FILE", config.POSTS_CACHE_FILE)
        monkeypatch.setattr(scrape, "DATA_DIR", config.DATA_DIR)

        scrape.save_cache([{"slug": "a", "title": "Old", "updated_at": "2024-01-01"}])
        scrape.save_cache([{"slug": "a", "title": "Updated", "updated_at": "2024-06-01"}])

        loaded = scrape.load_cache()
        assert loaded["a"]["title"] == "Updated"


# ---------------------------------------------------------------------------
# HTTP-mocked tests
# ---------------------------------------------------------------------------


class TestGet:
    @patch("scrape.time.sleep")
    @patch("scrape._SESSION")
    def test_rate_limits(self, mock_session, mock_sleep):
        from scrape import _get

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_session.get.return_value = mock_resp

        _get("https://example.com/api")
        mock_sleep.assert_called_once_with(0.5)
        mock_session.get.assert_called_once()


class TestFetchPostList:
    @patch("scrape._get")
    def test_filters_public_only(self, mock_get):
        from scrape import fetch_post_list

        mock_get.return_value.json.return_value = [
            {"slug": "public-1", "audience": "everyone"},
            {"slug": "paid-1", "audience": "only_paid"},
            {"slug": "public-2", "audience": "everyone"},
        ]
        result = fetch_post_list("https://example.com")
        slugs = [p["slug"] for p in result]
        assert "public-1" in slugs
        assert "public-2" in slugs
        assert "paid-1" not in slugs

    @patch("scrape._get")
    def test_pagination(self, mock_get):
        from scrape import fetch_post_list

        page1 = [{"slug": f"p{i}", "audience": "everyone"} for i in range(12)]
        page2 = [{"slug": "p12", "audience": "everyone"}]

        mock_get.return_value.json.side_effect = [page1, page2]
        result = fetch_post_list("https://example.com")
        assert len(result) == 13
        assert mock_get.call_count == 2


class TestFetchPostBody:
    @patch("scrape._get")
    def test_success(self, mock_get):
        from scrape import fetch_post_body

        mock_get.return_value.json.return_value = {"body_html": "<p>Full body</p>"}
        result = fetch_post_body("https://example.com", "my-post")
        assert result == "<p>Full body</p>"

    @patch("scrape._get")
    def test_failure_returns_none(self, mock_get):
        from scrape import fetch_post_body

        mock_get.side_effect = Exception("Network error")
        result = fetch_post_body("https://example.com", "my-post")
        assert result is None


class TestDiscoverSubstackBaseUrl:
    @patch("scrape._SESSION")
    def test_custom_domain_api_works(self, mock_session):
        from scrape import discover_substack_base_url

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = [{"slug": "test"}]
        mock_session.get.return_value = mock_resp

        result = discover_substack_base_url("https://blog.example.com")
        assert result == "https://blog.example.com"

    @patch("scrape._SESSION")
    def test_fallback_url(self, mock_session):
        from scrape import discover_substack_base_url

        mock_session.get.side_effect = Exception("Connection refused")
        result = discover_substack_base_url("https://broken.example.com")
        assert "substack.com" in result

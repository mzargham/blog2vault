"""Tests for sync.py — pipeline integration, CLI args, exit codes, GHA helpers."""

import os
from unittest.mock import MagicMock, patch, call

import pytest


# ---------------------------------------------------------------------------
# GHA helper tests
# ---------------------------------------------------------------------------


class TestGhaOutput:
    def test_writes_to_file(self, tmp_path, monkeypatch):
        from sync import _gha_output

        output_file = tmp_path / "output.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(output_file))

        _gha_output("new_posts", "3")
        content = output_file.read_text()
        assert "new_posts=3" in content

    def test_no_file_no_crash(self, monkeypatch):
        from sync import _gha_output

        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        # Should just log, not crash
        _gha_output("key", "value")


class TestGhaSummary:
    def test_writes_markdown(self, tmp_path, monkeypatch):
        from sync import _gha_summary

        summary_file = tmp_path / "summary.md"
        monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary_file))

        _gha_summary("## Test Summary")
        content = summary_file.read_text()
        assert "## Test Summary" in content

    def test_no_file_no_crash(self, monkeypatch):
        from sync import _gha_summary

        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
        # Should do nothing silently
        _gha_summary("## Ignored")


# ---------------------------------------------------------------------------
# Pipeline tests (heavily mocked)
# ---------------------------------------------------------------------------


class TestRun:
    def _make_posts(self):
        return [
            {
                "slug": "post-1",
                "title": "Post One",
                "post_date": "2024-01-01T00:00:00Z",
                "audience": "everyone",
                "body_html": "<p>content</p>",
            },
        ]

    @patch("sync.write_vault")
    @patch("sync.run_extraction")
    @patch("sync.save_cache")
    @patch("sync.load_cache")
    @patch("sync.load_vault_state")
    @patch("sync.fetch_all_posts")
    @patch("sync.discover_substack_base_url")
    def test_no_new_posts_returns_0(
        self, mock_discover, mock_fetch, mock_vault_state,
        mock_load_cache, mock_save_cache, mock_extract, mock_write,
        monkeypatch,
    ):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        posts = self._make_posts()
        mock_discover.return_value = "https://example.com"
        mock_fetch.return_value = posts
        mock_load_cache.return_value = {"post-1": posts[0]}
        mock_vault_state.return_value = {"post-1": "2024-01-01--post-1.md"}

        from sync import run
        result = run()
        assert result == 0
        mock_write.assert_not_called()

    @patch("sync.write_vault")
    @patch("sync.run_extraction")
    @patch("sync.save_cache")
    @patch("sync.load_cache")
    @patch("sync.load_vault_state")
    @patch("sync.fetch_all_posts")
    @patch("sync.discover_substack_base_url")
    def test_new_posts_returns_2(
        self, mock_discover, mock_fetch, mock_vault_state,
        mock_load_cache, mock_save_cache, mock_extract, mock_write,
        monkeypatch,
    ):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        posts = self._make_posts()
        mock_discover.return_value = "https://example.com"
        mock_fetch.return_value = posts
        mock_load_cache.return_value = {}
        mock_vault_state.return_value = {}  # Post not yet in vault
        mock_extract.return_value = {
            "tags": {}, "concepts": {}, "concept_names": {},
            "themes": {}, "citations": {}, "crosslinks": {},
        }
        mock_write.return_value = {}

        from sync import run
        result = run()
        assert result == 2
        mock_write.assert_called_once()

    @patch("sync.write_vault")
    @patch("sync.run_extraction")
    @patch("sync.save_cache")
    @patch("sync.load_cache")
    @patch("sync.load_vault_state")
    @patch("sync.fetch_all_posts")
    @patch("sync.discover_substack_base_url")
    def test_force_rebuilds(
        self, mock_discover, mock_fetch, mock_vault_state,
        mock_load_cache, mock_save_cache, mock_extract, mock_write,
        monkeypatch,
    ):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        posts = self._make_posts()
        mock_discover.return_value = "https://example.com"
        mock_fetch.return_value = posts
        mock_load_cache.return_value = {"post-1": posts[0]}
        mock_vault_state.return_value = {"post-1": "2024-01-01--post-1.md"}
        mock_extract.return_value = {
            "tags": {}, "concepts": {}, "concept_names": {},
            "themes": {}, "citations": {}, "crosslinks": {},
        }
        mock_write.return_value = {}

        from sync import run
        # Even though all posts are in vault, force should trigger build
        result = run(force=True)
        mock_extract.assert_called_once()
        mock_write.assert_called_once()

    @patch("sync.write_vault")
    @patch("sync.run_extraction")
    @patch("sync.save_cache")
    @patch("sync.load_cache")
    @patch("sync.load_vault_state")
    @patch("sync.fetch_all_posts")
    @patch("sync.discover_substack_base_url")
    def test_dry_run_skips_writes(
        self, mock_discover, mock_fetch, mock_vault_state,
        mock_load_cache, mock_save_cache, mock_extract, mock_write,
        monkeypatch,
    ):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        posts = self._make_posts()
        mock_discover.return_value = "https://example.com"
        mock_fetch.return_value = posts
        mock_load_cache.return_value = {}
        mock_vault_state.return_value = {}
        mock_extract.return_value = {
            "tags": {}, "concepts": {}, "concept_names": {},
            "themes": {}, "citations": {}, "crosslinks": {},
        }

        from sync import run
        result = run(dry_run=True)
        mock_write.assert_not_called()
        mock_save_cache.assert_not_called()

    @patch("sync.discover_substack_base_url")
    def test_discovery_failure_returns_1(self, mock_discover, monkeypatch):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        mock_discover.side_effect = Exception("DNS failure")
        from sync import run
        assert run() == 1

    @patch("sync.fetch_all_posts")
    @patch("sync.discover_substack_base_url")
    def test_fetch_failure_returns_1(self, mock_discover, mock_fetch, monkeypatch):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        mock_discover.return_value = "https://example.com"
        mock_fetch.side_effect = Exception("Connection timeout")
        from sync import run
        assert run() == 1

    @patch("sync.fetch_all_posts")
    @patch("sync.discover_substack_base_url")
    def test_empty_posts_returns_1(self, mock_discover, mock_fetch, monkeypatch):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        mock_discover.return_value = "https://example.com"
        mock_fetch.return_value = []
        from sync import run
        assert run() == 1

    def test_no_ai_sets_env(self, monkeypatch):
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

        with patch("sync.discover_substack_base_url") as mock_discover:
            mock_discover.side_effect = Exception("stop early")
            from sync import run
            run(no_ai=True)
            assert os.environ.get("USE_AI_EXTRACTION") == "false"

        # Cleanup
        monkeypatch.delenv("USE_AI_EXTRACTION", raising=False)


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


class TestMain:
    @patch("sync.run")
    @patch("sys.argv", ["sync.py", "--force", "--dry-run"])
    def test_parses_args(self, mock_run):
        mock_run.return_value = 0
        from sync import main

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        mock_run.assert_called_once_with(force=True, dry_run=True, no_ai=False)

    @patch("sync.run")
    @patch("sys.argv", ["sync.py", "--no-ai"])
    def test_no_ai_flag(self, mock_run):
        mock_run.return_value = 0
        from sync import main

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0
        mock_run.assert_called_once_with(force=False, dry_run=False, no_ai=True)

    @patch("sync.run")
    @patch("sys.argv", ["sync.py"])
    def test_exit_code_propagated(self, mock_run):
        mock_run.return_value = 2
        from sync import main

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2

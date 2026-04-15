"""Tests for config.py — defaults and environment variable overrides."""

import importlib
from pathlib import Path


def test_defaults():
    import config

    assert config.BLOG_CUSTOM_DOMAIN == "https://www.avikde.me"
    assert config.SUBSTACK_SUBDOMAIN_FALLBACK == "avikde"
    assert config.API_PAGE_SIZE == 12
    assert config.API_RATE_LIMIT_S == 0.5
    assert config.HTTP_TIMEOUT_S == 15
    assert config.TFIDF_TOP_N == 8
    assert config.CONCEPT_MIN_DF == 2
    assert config.CONCEPT_MAX_TOTAL == 40


def test_folder_constants():
    import config

    assert config.POSTS_FOLDER == "posts"
    assert config.TOPICS_FOLDER == "topics"
    assert config.CONCEPTS_FOLDER == "concepts"
    assert config.CITATIONS_FOLDER == "citations"
    assert config.META_FOLDER == "_meta"


def test_path_objects_are_paths():
    import config

    assert isinstance(config.VAULT_DIR, Path)
    assert isinstance(config.DATA_DIR, Path)
    assert isinstance(config.POSTS_CACHE_FILE, Path)
    assert isinstance(config.VAULT_STATE_FILE, Path)
    assert isinstance(config.CONCEPTS_CACHE_FILE, Path)


def test_blog_custom_domain_override(monkeypatch):
    monkeypatch.setenv("BLOG_CUSTOM_DOMAIN", "https://example.com")
    import config

    importlib.reload(config)
    assert config.BLOG_CUSTOM_DOMAIN == "https://example.com"
    # Restore
    monkeypatch.delenv("BLOG_CUSTOM_DOMAIN")
    importlib.reload(config)


def test_substack_subdomain_override(monkeypatch):
    monkeypatch.setenv("SUBSTACK_SUBDOMAIN", "testblog")
    import config

    importlib.reload(config)
    assert config.SUBSTACK_SUBDOMAIN_FALLBACK == "testblog"
    monkeypatch.delenv("SUBSTACK_SUBDOMAIN")
    importlib.reload(config)


def test_use_ai_extraction_default():
    import config

    # Default is true (string "true" from getenv)
    assert config.USE_AI_EXTRACTION is True


def test_use_ai_extraction_false(monkeypatch):
    monkeypatch.setenv("USE_AI_EXTRACTION", "false")
    import config

    importlib.reload(config)
    assert config.USE_AI_EXTRACTION is False
    monkeypatch.delenv("USE_AI_EXTRACTION")
    importlib.reload(config)


def test_use_ai_extraction_case_insensitive(monkeypatch):
    monkeypatch.setenv("USE_AI_EXTRACTION", "FALSE")
    import config

    importlib.reload(config)
    assert config.USE_AI_EXTRACTION is False
    monkeypatch.delenv("USE_AI_EXTRACTION")
    importlib.reload(config)

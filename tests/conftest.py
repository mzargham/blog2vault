"""Shared fixtures for the blog2vault test suite."""

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_posts():
    """Load all mock posts from fixtures (includes paid-only post)."""
    with open(FIXTURES_DIR / "mock_posts.json") as f:
        return json.load(f)


@pytest.fixture
def public_posts(mock_posts):
    """Only public posts (audience == 'everyone')."""
    return [p for p in mock_posts if p.get("audience") == "everyone"]


@pytest.fixture
def sample_post():
    """A single well-formed public post."""
    return {
        "slug": "control-theory-basics",
        "title": "Control Theory Basics for Engineers",
        "subtitle": "An introduction to feedback loops and stability",
        "post_date": "2024-03-15T10:00:00Z",
        "publishedAt": "2024-03-15T10:00:00Z",
        "updated_at": "2024-03-16T08:00:00Z",
        "audience": "everyone",
        "canonical_url": "https://www.avikde.me/p/control-theory-basics",
        "cover_image": "https://cdn.example.com/cover1.jpg",
        "body_html": (
            "<h2>Introduction</h2>"
            "<p>Control theory is a branch of engineering.</p>"
        ),
        "postTags": [
            {"name": "Engineering", "slug": "engineering"},
            {"name": "Control Theory", "slug": "control-theory"},
        ],
    }


@pytest.fixture
def mock_graph():
    """Minimal extraction graph with all expected keys."""
    return {
        "tags": {
            "engineering": ["control-theory-basics", "systems-dynamics"],
            "control-theory": ["control-theory-basics"],
        },
        "topics": {
            "control-theory-fundamentals": ["control-theory-basics"],
            "systems-dynamics-modeling": ["systems-dynamics"],
            "token-economy-design": ["token-engineering"],
        },
        "post_topic": {
            "control-theory-basics": "control-theory-fundamentals",
            "systems-dynamics": "systems-dynamics-modeling",
            "token-engineering": "token-economy-design",
        },
        "concepts": {
            "feedback-loops": ["control-theory-basics", "systems-dynamics"],
            "lyapunov-stability": ["control-theory-basics"],
        },
        "concept_names": {
            "control-theory-fundamentals": "Control Theory Fundamentals",
            "systems-dynamics-modeling": "Systems Dynamics Modeling",
            "token-economy-design": "Token Economy Design",
            "feedback-loops": "Feedback Loops",
            "lyapunov-stability": "Lyapunov Stability",
        },
        "citations": {
            "https://arxiv.org/abs/2301.00001": {
                "url": "https://arxiv.org/abs/2301.00001",
                "domain": "arxiv.org",
                "domain_slug": "arxiv-org",
                "posts": ["control-theory-basics", "token-engineering"],
                "anchor_texts": ["recent work by Smith 2023"],
            }
        },
        "crosslinks": {
            "token-engineering": ["control-theory-basics"],
            "systems-dynamics": ["control-theory-basics"],
        },
    }


@pytest.fixture
def patch_config_paths(tmp_path, monkeypatch):
    """Redirect all config paths to tmp_path so tests never touch real filesystem."""
    import config

    vault_dir = tmp_path / "vault"
    data_dir = tmp_path / "data"

    monkeypatch.setattr(config, "VAULT_DIR", vault_dir)
    monkeypatch.setattr(config, "DATA_DIR", data_dir)
    monkeypatch.setattr(config, "POSTS_CACHE_FILE", data_dir / "posts_cache.json")
    monkeypatch.setattr(config, "VAULT_STATE_FILE", data_dir / "vault_state.json")
    monkeypatch.setattr(config, "CONCEPTS_CACHE_FILE", data_dir / "concepts_cache.json")

    return {"vault_dir": vault_dir, "data_dir": data_dir}

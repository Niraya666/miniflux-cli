"""Tests for configuration management."""

import pytest

from miniflux_cli.config import Config


def test_config_with_api_key():
    cfg = Config(url="https://example.org", api_key="secret")
    assert cfg.url == "https://example.org"
    assert cfg.get_client_kwargs() == {
        "base_url": "https://example.org",
        "api_key": "secret",
        "timeout": 30.0,
    }


def test_config_with_basic_auth():
    cfg = Config(url="http://localhost", username="admin", password="admin")
    assert cfg.get_client_kwargs() == {
        "base_url": "http://localhost",
        "username": "admin",
        "password": "admin",
        "timeout": 30.0,
    }


def test_config_strips_trailing_slash():
    cfg = Config(url="https://example.org/")
    assert cfg.url == "https://example.org"


def test_config_missing_auth_raises():
    cfg = Config(url="https://example.org")
    with pytest.raises(ValueError, match="api_key"):
        cfg.get_client_kwargs()

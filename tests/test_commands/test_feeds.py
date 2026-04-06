"""Tests for feed commands."""

from unittest.mock import patch

from click.testing import CliRunner

from miniflux_cli.__main__ import cli


def _invoke(*args, env=None):
    runner = CliRunner(env=env or {"MINIFLUX_URL": "http://test", "MINIFLUX_API_KEY": "k"})
    return runner.invoke(cli, args)


def test_feeds_list_json():
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        mock_cls.return_value.get_feeds.return_value = [
            {"id": 1, "title": "Test", "feed_url": "http://a", "category": {"title": "Cat"}}
        ]
        result = _invoke("--json", "feeds", "list")
        assert result.exit_code == 0
        assert '"id": 1' in result.output


def test_feeds_list_table():
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        mock_cls.return_value.get_feeds.return_value = [
            {"id": 1, "title": "Test", "feed_url": "http://a", "category": {"title": "Cat"}}
        ]
        result = _invoke("feeds", "list")
        assert result.exit_code == 0
        assert "Test" in result.output


def test_feeds_create():
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        mock_cls.return_value.create_feed.return_value = {"feed_id": 42}
        result = _invoke("feeds", "create", "http://rss.example.com")
        assert result.exit_code == 0
        assert "Feed created: ID=42" in result.output


def test_feeds_refresh_all():
    with patch("miniflux_cli.client.miniflux.Client"):
        result = _invoke("feeds", "refresh-all")
        assert result.exit_code == 0
        assert "All feeds refreshed" in result.output


def test_feeds_mark_read():
    with patch("miniflux_cli.client.miniflux.Client"):
        result = _invoke("feeds", "mark-read", "1")
        assert result.exit_code == 0
        assert "marked as read" in result.output

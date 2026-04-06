"""Tests for entry commands."""

from unittest.mock import patch

from click.testing import CliRunner

from miniflux_cli.__main__ import cli


def _invoke(*args, env=None):
    runner = CliRunner(env=env or {"MINIFLUX_URL": "http://test", "MINIFLUX_API_KEY": "k"})
    return runner.invoke(cli, args)


def test_entries_list_json():
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        mock_cls.return_value.get_entries.return_value = {
            "entries": [{"id": 1, "title": "Hello", "status": "unread"}],
            "total": 1,
        }
        result = _invoke("--json", "entries", "list", "--status", "unread")
        assert result.exit_code == 0
        assert '"id": 1' in result.output


def test_entries_mark_read():
    with patch("miniflux_cli.client.miniflux.Client"):
        result = _invoke("entries", "mark-read", "5", "6")
        assert result.exit_code == 0
        assert "2 entries marked as read" in result.output


def test_entries_bookmark():
    with patch("miniflux_cli.client.miniflux.Client"):
        result = _invoke("entries", "bookmark", "7")
        assert result.exit_code == 0
        assert "Bookmark toggled" in result.output

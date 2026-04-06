"""Tests for system commands."""

from unittest.mock import patch

from click.testing import CliRunner

from miniflux_cli.__main__ import cli


def _invoke(*args, env=None):
    runner = CliRunner(env=env or {"MINIFLUX_URL": "http://test", "MINIFLUX_API_KEY": "k"})
    return runner.invoke(cli, args)


def test_system_version():
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        mock_cls.return_value.get_version.return_value = "2.0.50"
        result = _invoke("system", "version")
        assert result.exit_code == 0
        assert "2.0.50" in result.output


def test_system_counters():
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        mock_cls.return_value.get_feed_counters.return_value = {"unread": 5, "read": 10}
        result = _invoke("--json", "system", "counters")
        assert result.exit_code == 0
        assert '"unread": 5' in result.output

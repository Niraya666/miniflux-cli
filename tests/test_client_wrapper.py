"""Tests for the miniflux client wrapper."""

from unittest.mock import MagicMock, patch

import miniflux
import pytest

from miniflux_cli.client import MinifluxClientWrapper
from miniflux_cli.config import Config
from miniflux_cli.exceptions import AuthError, CLIError, NotFoundError, ServerError


def _make_response(status_code: int) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.headers = {"Content-Type": "application/json"}
    resp.json.return_value = {"error_message": "oops"}
    return resp


def test_wrapper_delegates_successfully() -> None:
    cfg = Config(url="https://example.org", api_key="secret")
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        instance = mock_cls.return_value
        instance.get_feeds.return_value = [{"id": 1}]
        with MinifluxClientWrapper(cfg) as wrapper:
            result = wrapper.get_feeds()
            assert result == [{"id": 1}]
            instance.get_feeds.assert_called_once()
        instance.close.assert_called_once()


def test_wrapper_not_found() -> None:
    cfg = Config(url="https://example.org", api_key="secret")
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        instance = mock_cls.return_value
        instance.get_feed.side_effect = miniflux.ResourceNotFound(_make_response(404))
        wrapper = MinifluxClientWrapper(cfg)
        with pytest.raises(NotFoundError):
            wrapper.get_feed(1)


def test_wrapper_unauthorized() -> None:
    cfg = Config(url="https://example.org", api_key="secret")
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        instance = mock_cls.return_value
        instance.get_feeds.side_effect = miniflux.AccessUnauthorized(_make_response(401))
        wrapper = MinifluxClientWrapper(cfg)
        with pytest.raises(AuthError):
            wrapper.get_feeds()


def test_wrapper_forbidden() -> None:
    cfg = Config(url="https://example.org", api_key="secret")
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        instance = mock_cls.return_value
        instance.get_feeds.side_effect = miniflux.AccessForbidden(_make_response(403))
        wrapper = MinifluxClientWrapper(cfg)
        with pytest.raises(AuthError):
            wrapper.get_feeds()


def test_wrapper_server_error() -> None:
    cfg = Config(url="https://example.org", api_key="secret")
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        instance = mock_cls.return_value
        instance.get_feeds.side_effect = miniflux.ServerError(_make_response(500))
        wrapper = MinifluxClientWrapper(cfg)
        with pytest.raises(ServerError):
            wrapper.get_feeds()


def test_wrapper_client_error() -> None:
    cfg = Config(url="https://example.org", api_key="secret")
    with patch("miniflux_cli.client.miniflux.Client") as mock_cls:
        instance = mock_cls.return_value
        instance.create_feed.side_effect = miniflux.ClientError(_make_response(400))
        wrapper = MinifluxClientWrapper(cfg)
        with pytest.raises(CLIError) as exc_info:
            wrapper.create_feed({"url": "x"})
        assert exc_info.value.exit_code == 2

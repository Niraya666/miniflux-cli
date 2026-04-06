"""Shared pytest fixtures."""

from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_client():
    """Return a mock MinifluxClientWrapper and patch its constructor."""
    client = MagicMock()
    with patch("miniflux_cli.client.miniflux.Client", return_value=client):
        yield client

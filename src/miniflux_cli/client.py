"""Thin wrapper around the official miniflux Python client."""

from typing import Any

import miniflux

from miniflux_cli.config import Config
from miniflux_cli.exceptions import AuthError, CLIError, NotFoundError, ServerError


class MinifluxClientWrapper:
    """Wraps miniflux.Client, transparently delegating methods and normalizing exceptions."""

    def __init__(self, config: Config) -> None:
        self._client: miniflux.Client = miniflux.Client(**config.get_client_kwargs())

    def __enter__(self) -> "MinifluxClientWrapper":
        return self

    def __exit__(self, *args: Any) -> None:
        self._client.close()

    def __getattr__(self, name: str) -> Any:
        raw = getattr(self._client, name)
        if not callable(raw):
            return raw

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return raw(*args, **kwargs)
            except miniflux.ResourceNotFound as exc:
                raise NotFoundError(str(exc)) from exc
            except (miniflux.AccessUnauthorized, miniflux.AccessForbidden) as exc:
                raise AuthError(str(exc)) from exc
            except miniflux.ServerError as exc:
                raise ServerError(str(exc)) from exc
            except miniflux.ClientError as exc:
                # Map any remaining client errors to a generic CLIError.
                # The official client doesn't expose BadRequest directly,
                # but ClientError covers 4xx responses.
                raise CLIError(str(exc), exit_code=2) from exc

        return wrapper

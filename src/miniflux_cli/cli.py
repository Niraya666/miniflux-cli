"""Root CLI definition and shared decorators."""

import functools
from collections.abc import Callable
from pathlib import Path
from typing import Any

import click

from miniflux_cli.client import MinifluxClientWrapper
from miniflux_cli.config import Config
from miniflux_cli.exceptions import CLIError
from miniflux_cli.formatting import render_json


class Context:
    """Shared CLI context object."""

    def __init__(self, json_mode: bool, verbose: bool, config_kwargs: dict[str, Any]) -> None:
        self.json_mode = json_mode
        self.verbose = verbose
        self.config_kwargs = config_kwargs


def _load_config() -> Config:
    """Instantiate Config from the context kwargs, raising on failure."""
    ctx = click.get_current_context().obj
    assert isinstance(ctx, Context)
    try:
        return Config(**ctx.config_kwargs)
    except Exception as exc:
        if ctx.verbose:
            raise
        click.echo(f"Configuration error: {exc}", err=True)
        raise click.ClickException(str(exc)) from exc


def pass_client(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that injects a MinifluxClientWrapper instance into a command."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        config = _load_config()
        with MinifluxClientWrapper(config) as client:
            return func(client, *args, **kwargs)

    return wrapper


@click.group()
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, dir_okay=False),
    help="Path to a config file.",
)
@click.option("--json", "json_mode", is_flag=True, help="Output raw JSON.")
@click.option("-v", "--verbose", is_flag=True, help="Show verbose error output.")
@click.pass_context
def cli_root(
    click_ctx: click.Context,
    config_path: Path | None,
    json_mode: bool,
    verbose: bool,
) -> None:
    """Miniflux CLI — manage RSS feeds, entries, categories, and more."""
    kwargs: dict[str, Any] = {}
    if config_path is not None and config_path.exists():
        import json

        import tomllib

        data = config_path.read_bytes()
        try:
            loaded = tomllib.loads(data.decode("utf-8"))
        except Exception:
            try:
                loaded = json.loads(data.decode("utf-8"))
            except Exception as exc:
                raise click.BadParameter(f"Unable to parse config file: {exc}") from exc
        kwargs.update(loaded)

    click_ctx.obj = Context(json_mode=json_mode, verbose=verbose, config_kwargs=kwargs)


# Register subcommand groups
@cli_root.group()
def feeds() -> None:
    """Manage feeds."""


@cli_root.group()
def categories() -> None:
    """Manage categories."""


@cli_root.group()
def entries() -> None:
    """Manage entries."""


@cli_root.group()
def opml() -> None:
    """OPML import/export."""


@cli_root.group()
def users() -> None:
    """Manage users."""


@cli_root.group(name="api-keys")
def api_keys() -> None:
    """Manage API keys."""


@cli_root.group()
def system() -> None:
    """System information and utilities."""


def _output(data: Any) -> None:
    ctx = click.get_current_context().obj
    assert isinstance(ctx, Context)
    if ctx.json_mode:
        render_json(data)
    # fall through to human-readable output handled by individual commands


def is_json_mode() -> bool:
    ctx = click.get_current_context().obj
    assert isinstance(ctx, Context)
    return ctx.json_mode


def _handle_error(exc: Exception) -> None:
    ctx = click.get_current_context().obj
    assert isinstance(ctx, Context)
    if isinstance(exc, CLIError):
        click.echo(f"Error: {exc}", err=True)
        if ctx.verbose:
            raise
        raise click.ClickException(str(exc)) from exc
    raise exc


# Expose the root command as `cli`
cli = cli_root

"""System information and utility commands."""

from typing import TYPE_CHECKING

import click

from miniflux_cli.cli import pass_client
from miniflux_cli.cli import system as system_group
from miniflux_cli.formatting import render_json, render_panel

if TYPE_CHECKING:
    from miniflux_cli.client import MinifluxClientWrapper


def _ctx_json() -> bool:
    return bool(click.get_current_context().obj.json_mode)


@system_group.command(name="health")
@pass_client
def system_health(client: "MinifluxClientWrapper") -> None:
    """Check server health."""
    data = client.get_version()
    if _ctx_json():
        render_json({"healthy": True, "version": data})
        return
    click.echo(f"Server is healthy. Version: {data}")


@system_group.command(name="version")
@pass_client
def system_version(client: "MinifluxClientWrapper") -> None:
    """Get Miniflux version."""
    data = client.get_version()
    if _ctx_json():
        render_json({"version": data})
        return
    click.echo(f"Miniflux version: {data}")


@system_group.command(name="info")
@pass_client
def system_info(client: "MinifluxClientWrapper") -> None:
    """Get build information."""
    # get_version returns a string; build info endpoint is not exposed in client.
    data = client.get_version()
    if _ctx_json():
        render_json({"version": data})
        return
    click.echo(f"Version: {data}")


@system_group.command(name="counters")
@pass_client
def system_counters(client: "MinifluxClientWrapper") -> None:
    """Get unread/read counters."""
    data = client.get_feed_counters()
    if _ctx_json():
        render_json(data)
        return
    render_panel(data, title="Feed Counters")


@system_group.command(name="integrations")
@pass_client
def system_integrations(client: "MinifluxClientWrapper") -> None:
    """Get integrations status."""
    data = client.get_integrations_status()
    if _ctx_json():
        render_json(data)
        return
    render_panel(data, title="Integrations Status")


@system_group.command(name="flush-history")
@pass_client
def system_flush_history(client: "MinifluxClientWrapper") -> None:
    """Flush history."""
    client.flush_history()
    click.echo("History flushed.")

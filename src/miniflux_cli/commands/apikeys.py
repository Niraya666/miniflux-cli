"""API key management commands."""

from typing import TYPE_CHECKING

import click

from miniflux_cli.cli import api_keys as api_keys_group
from miniflux_cli.cli import pass_client
from miniflux_cli.formatting import render_json, render_table

if TYPE_CHECKING:
    from miniflux_cli.client import MinifluxClientWrapper


def _ctx_json() -> bool:
    return bool(click.get_current_context().obj.json_mode)


@api_keys_group.command(name="list")
@pass_client
def api_keys_list(client: "MinifluxClientWrapper") -> None:
    """List API keys."""
    data = client.get_api_keys()
    if _ctx_json():
        render_json(data)
        return
    if not data:
        click.echo("No API keys found.")
        return
    render_table(
        [
            {
                "ID": k["id"],
                "Description": k.get("description", ""),
                "Token": k.get("token", "")[:16] + "...",
            }
            for k in data
        ],
        columns=["ID", "Description", "Token"],
        title="API Keys",
    )


@api_keys_group.command(name="create")
@click.argument("description")
@pass_client
def api_keys_create(client: "MinifluxClientWrapper", description: str) -> None:
    """Create an API key."""
    data = client.create_api_key(description)
    if _ctx_json():
        render_json(data)
        return
    # Show the token once because it may not be retrievable later.
    key = data.get("token", "")
    click.echo(f"API key created: ID={data.get('id')}")
    click.echo(f"Token: {key}")


@api_keys_group.command(name="delete")
@click.argument("key_id", type=int)
@pass_client
def api_keys_delete(client: "MinifluxClientWrapper", key_id: int) -> None:
    """Delete an API key."""
    client.delete_api_key(key_id)
    click.echo(f"API key {key_id} deleted.")

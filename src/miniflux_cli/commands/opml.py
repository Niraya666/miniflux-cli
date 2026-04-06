"""OPML import/export commands."""

from pathlib import Path
from typing import TYPE_CHECKING

import click

from miniflux_cli.cli import opml as opml_group
from miniflux_cli.cli import pass_client
from miniflux_cli.formatting import render_json

if TYPE_CHECKING:
    from miniflux_cli.client import MinifluxClientWrapper


def _ctx_json() -> bool:
    return bool(click.get_current_context().obj.json_mode)


@opml_group.command(name="export")
@pass_client
def opml_export(client: "MinifluxClientWrapper") -> None:
    """Export feeds as OPML."""
    data = client.export()
    click.echo(data)


@opml_group.command(name="import")
@click.argument("file_path", type=click.Path(path_type=Path, exists=True, dir_okay=False))
@pass_client
def opml_import(client: "MinifluxClientWrapper", file_path: Path) -> None:
    """Import feeds from an OPML file."""
    result = client.import_feeds(file_path.read_bytes())
    if _ctx_json():
        render_json(result if isinstance(result, dict) else {"message": str(result)})
        return
    click.echo("OPML imported successfully.")

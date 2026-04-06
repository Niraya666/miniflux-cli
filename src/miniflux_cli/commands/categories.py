"""Category management commands."""

from typing import TYPE_CHECKING

import click

from miniflux_cli.cli import categories as categories_group
from miniflux_cli.cli import pass_client
from miniflux_cli.exceptions import CLIError
from miniflux_cli.formatting import render_json, render_panel, render_table

if TYPE_CHECKING:
    from miniflux_cli.client import MinifluxClientWrapper


def _ctx_json() -> bool:
    return bool(click.get_current_context().obj.json_mode)


@categories_group.command(name="list")
@pass_client
def categories_list(client: "MinifluxClientWrapper") -> None:
    """List all categories."""
    data = client.get_categories()
    if _ctx_json():
        render_json(data)
        return
    if not data:
        click.echo("No categories found.")
        return
    render_table(
        [
            {
                "ID": c["id"],
                "Title": c["title"],
                "Feeds": c.get("nb_feeds", ""),
                "Unread": c.get("nb_unread", ""),
            }
            for c in data
        ],
        columns=["ID", "Title", "Feeds", "Unread"],
        title="Categories",
    )


@categories_group.command(name="get")
@click.argument("category_id", type=int)
@pass_client
def categories_get(client: "MinifluxClientWrapper", category_id: int) -> None:
    """Get a single category (via feeds endpoint metadata fallback)."""
    # The official client doesn't expose get_category directly; use get_categories and filter.
    cats = client.get_categories()
    match = next((c for c in cats if c["id"] == category_id), None)
    if match is None:
        raise CLIError(f"Category {category_id} not found.", exit_code=4)
    if _ctx_json():
        render_json(match)
        return
    render_panel(match, title=f"Category {category_id}")


@categories_group.command(name="create")
@click.argument("title")
@pass_client
def categories_create(client: "MinifluxClientWrapper", title: str) -> None:
    """Create a category."""
    data = client.create_category(title)
    if _ctx_json():
        render_json(data)
        return
    click.echo(f"Category created: ID={data.get('id')}")


@categories_group.command(name="update")
@click.argument("category_id", type=int)
@click.argument("title")
@pass_client
def categories_update(client: "MinifluxClientWrapper", category_id: int, title: str) -> None:
    """Update a category."""
    data = client.update_category(category_id, title)
    if _ctx_json():
        render_json(data)
        return
    click.echo(f"Category {category_id} updated.")


@categories_group.command(name="delete")
@click.argument("category_id", type=int)
@pass_client
def categories_delete(client: "MinifluxClientWrapper", category_id: int) -> None:
    """Delete a category."""
    client.delete_category(category_id)
    click.echo(f"Category {category_id} deleted.")


@categories_group.command(name="refresh")
@click.argument("category_id", type=int)
@pass_client
def categories_refresh(client: "MinifluxClientWrapper", category_id: int) -> None:
    """Refresh all feeds in a category."""
    client.refresh_category(category_id)
    click.echo(f"Category {category_id} feeds refreshed.")


@categories_group.command(name="mark-read")
@click.argument("category_id", type=int)
@pass_client
def categories_mark_read(client: "MinifluxClientWrapper", category_id: int) -> None:
    """Mark all entries in a category as read."""
    client.mark_category_entries_as_read(category_id)
    click.echo(f"All entries in category {category_id} marked as read.")


@categories_group.command(name="entries")
@click.argument("category_id", type=int)
@click.option(
    "--status", type=click.Choice(["unread", "read", "removed"]), help="Entry status filter."
)
@click.option("--order", default="published_at", help="Sort order field.")
@click.option(
    "--direction", type=click.Choice(["asc", "desc"]), default="desc", help="Sort direction."
)
@click.option("--limit", type=int, default=100, help="Max entries to return.")
@click.option("--offset", type=int, default=0, help="Offset for pagination.")
@click.option("--search", help="Search query.")
@pass_client
def categories_entries(
    client: "MinifluxClientWrapper",
    category_id: int,
    status: str | None,
    order: str,
    direction: str,
    limit: int,
    offset: int,
    search: str | None,
) -> None:
    """List entries in a category."""
    kwargs: dict = {"order": order, "direction": direction, "limit": limit, "offset": offset}
    if status is not None:
        kwargs["status"] = status
    if search is not None:
        kwargs["search"] = search
    data = client.get_category_entries(category_id, **kwargs)
    if _ctx_json():
        render_json(data)
        return
    entries = data.get("entries", []) if isinstance(data, dict) else data
    if not entries:
        click.echo("No entries found.")
        return
    render_table(
        [
            {
                "ID": e["id"],
                "Title": e.get("title", ""),
                "Author": e.get("author", ""),
                "Status": e.get("status", ""),
                "Published": str(e.get("published_at", "")),
            }
            for e in entries
        ],
        columns=["ID", "Title", "Author", "Status", "Published"],
        title=f"Category {category_id} Entries",
    )


@categories_group.command(name="feeds")
@click.argument("category_id", type=int)
@pass_client
def categories_feeds(client: "MinifluxClientWrapper", category_id: int) -> None:
    """List feeds in a category."""
    data = client.get_category_feeds(category_id)
    if _ctx_json():
        render_json(data)
        return
    if not data:
        click.echo("No feeds found in category.")
        return
    render_table(
        [
            {
                "ID": f["id"],
                "Title": f.get("title", ""),
                "URL": f.get("feed_url", ""),
            }
            for f in data
        ],
        columns=["ID", "Title", "URL"],
        title=f"Category {category_id} Feeds",
    )

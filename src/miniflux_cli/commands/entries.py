"""Entry management commands."""

from typing import TYPE_CHECKING

import click

from miniflux_cli.cli import entries as entries_group
from miniflux_cli.cli import pass_client
from miniflux_cli.exceptions import CLIError
from miniflux_cli.formatting import render_json, render_panel, render_table

if TYPE_CHECKING:
    from miniflux_cli.client import MinifluxClientWrapper


def _ctx_json() -> bool:
    return bool(click.get_current_context().obj.json_mode)


@entries_group.command(name="list")
@click.option(
    "--status", type=click.Choice(["unread", "read", "removed"]), help="Filter by status."
)
@click.option("--starred", is_flag=True, help="Only starred entries.")
@click.option("--order", default="published_at", help="Sort field.")
@click.option(
    "--direction", type=click.Choice(["asc", "desc"]), default="desc", help="Sort direction."
)
@click.option("--limit", type=int, default=100, help="Max results.")
@click.option("--offset", type=int, default=0, help="Pagination offset.")
@click.option("--before", type=int, help="Before entry ID.")
@click.option("--after", type=int, help="After entry ID.")
@click.option("--search", help="Search query.")
@click.option("--category-id", type=int, help="Filter by category ID.")
@click.option("--feed-id", type=int, help="Filter by feed ID.")
@pass_client
def entries_list(
    client: "MinifluxClientWrapper",
    status: str | None,
    starred: bool,
    order: str,
    direction: str,
    limit: int,
    offset: int,
    before: int | None,
    after: int | None,
    search: str | None,
    category_id: int | None,
    feed_id: int | None,
) -> None:
    """List entries globally."""
    kwargs: dict = {"order": order, "direction": direction, "limit": limit, "offset": offset}
    if status is not None:
        kwargs["status"] = status
    if starred:
        kwargs["starred"] = "true"
    if before is not None:
        kwargs["before_entry_id"] = before
    if after is not None:
        kwargs["after_entry_id"] = after
    if search is not None:
        kwargs["search"] = search
    if category_id is not None:
        kwargs["category_id"] = category_id
    if feed_id is not None:
        kwargs["feed_id"] = feed_id
    data = client.get_entries(**kwargs)
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
                "Title": e.get("title", "")[:60],
                "Feed": e.get("feed", {}).get("title", ""),
                "Status": e.get("status", ""),
                "Starred": "*" if e.get("starred") else "",
                "Published": str(e.get("published_at", "")),
            }
            for e in entries
        ],
        columns=["ID", "Title", "Feed", "Status", "Starred", "Published"],
        title="Entries",
    )


@entries_group.command(name="get")
@click.argument("entry_id", type=int)
@pass_client
def entries_get(client: "MinifluxClientWrapper", entry_id: int) -> None:
    """Get a single entry."""
    data = client.get_entry(entry_id)
    if _ctx_json():
        render_json(data)
        return
    render_panel(data, title=f"Entry {entry_id}")


@entries_group.command(name="update")
@click.argument("entry_id", type=int)
@click.option("--title", help="Entry title.")
@click.option("--content", help="Entry content.")
@click.option("--author", help="Entry author.")
@pass_client
def entries_update(
    client: "MinifluxClientWrapper",
    entry_id: int,
    title: str | None,
    content: str | None,
    author: str | None,
) -> None:
    """Update an entry."""
    payload: dict = {}
    if title is not None:
        payload["title"] = title
    if content is not None:
        payload["content"] = content
    if author is not None:
        payload["author"] = author
    if not payload:
        raise CLIError("No fields provided to update.", exit_code=2)
    data = client.update_entry(entry_id, **payload)
    if _ctx_json():
        render_json(data)
        return
    click.echo(f"Entry {entry_id} updated.")


@entries_group.command(name="mark-read")
@click.argument("entry_ids", type=int, nargs=-1, required=True)
@pass_client
def entries_mark_read(client: "MinifluxClientWrapper", entry_ids: tuple[int, ...]) -> None:
    """Mark entries as read."""
    client.update_entries([int(i) for i in entry_ids], status="read")
    if len(entry_ids) == 1:
        click.echo(f"Entry {entry_ids[0]} marked as read.")
    else:
        click.echo(f"{len(entry_ids)} entries marked as read.")


@entries_group.command(name="mark-unread")
@click.argument("entry_ids", type=int, nargs=-1, required=True)
@pass_client
def entries_mark_unread(client: "MinifluxClientWrapper", entry_ids: tuple[int, ...]) -> None:
    """Mark entries as unread."""
    client.update_entries([int(i) for i in entry_ids], status="unread")
    if len(entry_ids) == 1:
        click.echo(f"Entry {entry_ids[0]} marked as unread.")
    else:
        click.echo(f"{len(entry_ids)} entries marked as unread.")


@entries_group.command(name="bookmark")
@click.argument("entry_id", type=int)
@pass_client
def entries_bookmark(client: "MinifluxClientWrapper", entry_id: int) -> None:
    """Toggle bookmark for an entry."""
    client.toggle_bookmark(entry_id)
    click.echo(f"Bookmark toggled for entry {entry_id}.")


@entries_group.command(name="fetch-content")
@click.argument("entry_id", type=int)
@pass_client
def entries_fetch_content(client: "MinifluxClientWrapper", entry_id: int) -> None:
    """Fetch original article content."""
    data = client.fetch_entry_content(entry_id)
    if _ctx_json():
        render_json(data)
        return
    content = data.get("content", "") if isinstance(data, dict) else str(data)
    click.echo(content)


@entries_group.command(name="save")
@click.argument("entry_id", type=int)
@pass_client
def entries_save(client: "MinifluxClientWrapper", entry_id: int) -> None:
    """Save entry to third-party integrations."""
    client.save_entry(entry_id)
    click.echo(f"Entry {entry_id} saved to integrations.")

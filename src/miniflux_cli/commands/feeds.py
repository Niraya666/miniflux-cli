"""Feed management commands."""

from typing import TYPE_CHECKING

import click

from miniflux_cli.cli import feeds as feeds_group
from miniflux_cli.cli import pass_client
from miniflux_cli.exceptions import CLIError
from miniflux_cli.formatting import render_json, render_panel, render_table

if TYPE_CHECKING:
    from miniflux_cli.client import MinifluxClientWrapper


def _ctx_json() -> bool:
    return bool(click.get_current_context().obj.json_mode)


@feeds_group.command(name="list")
@pass_client
def feeds_list(client: "MinifluxClientWrapper") -> None:
    """List all feeds."""
    data = client.get_feeds()
    if _ctx_json():
        render_json(data)
        return
    if not data:
        click.echo("No feeds found.")
        return
    render_table(
        [
            {
                "ID": f["id"],
                "Title": f["title"],
                "URL": f["feed_url"],
                "Category": f.get("category", {}).get("title", ""),
                "Unread": f.get("_hal", {}).get("unread_comics", f.get("unread", "")),
            }
            for f in data
        ],
        columns=["ID", "Title", "URL", "Category", "Unread"],
        title="Feeds",
    )


@feeds_group.command(name="get")
@click.argument("feed_id", type=int)
@pass_client
def feeds_get(client: "MinifluxClientWrapper", feed_id: int) -> None:
    """Get a single feed."""
    data = client.get_feed(feed_id)
    if _ctx_json():
        render_json(data)
        return
    render_panel(data, title=f"Feed {feed_id}")


@feeds_group.command(name="create")
@click.argument("url")
@click.option("--category-id", type=int, help="Category ID.")
@click.option("--title", help="Custom feed title.")
@click.option("--crawler", is_flag=True, help="Enable crawler for this feed.")
@click.option("--user-agent", help="Custom user agent.")
@click.option("--username", help="Feed username.")
@click.option("--password", help="Feed password.")
@click.option("--scraper-rules", help="Scraper rules.")
@click.option("--rewrite-rules", help="Rewrite rules.")
@click.option("--blocklist-rules", help="Blocklist rules.")
@click.option("--keeplist-rules", help="Keeplist rules.")
@click.option("--ignore-htlc", is_flag=True, help="Ignore HTTP cache.")
@click.option("--fetch-original", is_flag=True, help="Fetch original article content.")
@pass_client
def feeds_create(
    client: "MinifluxClientWrapper",
    url: str,
    category_id: int | None,
    title: str | None,
    crawler: bool,
    user_agent: str | None,
    username: str | None,
    password: str | None,
    scraper_rules: str | None,
    rewrite_rules: str | None,
    blocklist_rules: str | None,
    keeplist_rules: str | None,
    ignore_htlc: bool,
    fetch_original: bool,
) -> None:
    """Create a new feed."""
    kwargs: dict = {}
    if category_id is not None:
        kwargs["category_id"] = category_id
    if title is not None:
        kwargs["title"] = title
    if crawler:
        kwargs["crawler"] = True
    if user_agent is not None:
        kwargs["user_agent"] = user_agent
    if username is not None:
        kwargs["username"] = username
    if password is not None:
        kwargs["password"] = password
    if scraper_rules is not None:
        kwargs["scraper_rules"] = scraper_rules
    if rewrite_rules is not None:
        kwargs["rewrite_rules"] = rewrite_rules
    if blocklist_rules is not None:
        kwargs["blocklist_rules"] = blocklist_rules
    if keeplist_rules is not None:
        kwargs["keeplist_rules"] = keeplist_rules
    if ignore_htlc:
        kwargs["ignore_http_cache"] = True
    if fetch_original:
        kwargs["fetch_original_content"] = True
    data = client.create_feed(url, **kwargs)
    if _ctx_json():
        render_json(data if isinstance(data, dict) else {"feed_id": data})
        return
    feed_id = data.get("feed_id") if isinstance(data, dict) else data
    click.echo(f"Feed created: ID={feed_id}")


@feeds_group.command(name="update")
@click.argument("feed_id", type=int)
@click.option("--title", help="Feed title.")
@click.option("--category-id", type=int, help="Category ID.")
@click.option("--crawler", type=bool, help="Enable crawler.")
@click.option("--user-agent", help="User agent.")
@click.option("--username", help="Username.")
@click.option("--password", help="Password.")
@click.option("--scraper-rules", help="Scraper rules.")
@click.option("--rewrite-rules", help="Rewrite rules.")
@click.option("--blocklist-rules", help="Blocklist rules.")
@click.option("--keeplist-rules", help="Keeplist rules.")
@click.option("--ignore-htlc", type=bool, help="Ignore HTTP cache.")
@click.option("--fetch-original", type=bool, help="Fetch original content.")
@click.option("--disabled", type=bool, help="Disable feed.")
@pass_client
def feeds_update(
    client: "MinifluxClientWrapper",
    feed_id: int,
    title: str | None,
    category_id: int | None,
    crawler: bool | None,
    user_agent: str | None,
    username: str | None,
    password: str | None,
    scraper_rules: str | None,
    rewrite_rules: str | None,
    blocklist_rules: str | None,
    keeplist_rules: str | None,
    ignore_htlc: bool | None,
    fetch_original: bool | None,
    disabled: bool | None,
) -> None:
    """Update a feed."""
    payload: dict = {}
    if title is not None:
        payload["title"] = title
    if category_id is not None:
        payload["category_id"] = category_id
    if crawler is not None:
        payload["crawler"] = crawler
    if user_agent is not None:
        payload["user_agent"] = user_agent
    if username is not None:
        payload["username"] = username
    if password is not None:
        payload["password"] = password
    if scraper_rules is not None:
        payload["scraper_rules"] = scraper_rules
    if rewrite_rules is not None:
        payload["rewrite_rules"] = rewrite_rules
    if blocklist_rules is not None:
        payload["blocklist_rules"] = blocklist_rules
    if keeplist_rules is not None:
        payload["keeplist_rules"] = keeplist_rules
    if ignore_htlc is not None:
        payload["ignore_http_cache"] = ignore_htlc
    if fetch_original is not None:
        payload["fetch_original_content"] = fetch_original
    if disabled is not None:
        payload["disabled"] = disabled
    if not payload:
        raise CLIError("No fields provided to update.", exit_code=2)
    data = client.update_feed(feed_id, **payload)
    if _ctx_json():
        render_json(data)
        return
    click.echo(f"Feed {feed_id} updated.")


@feeds_group.command(name="delete")
@click.argument("feed_id", type=int)
@pass_client
def feeds_delete(client: "MinifluxClientWrapper", feed_id: int) -> None:
    """Delete a feed."""
    client.delete_feed(feed_id)
    click.echo(f"Feed {feed_id} deleted.")


@feeds_group.command(name="refresh")
@click.argument("feed_id", type=int)
@pass_client
def feeds_refresh(client: "MinifluxClientWrapper", feed_id: int) -> None:
    """Refresh a single feed."""
    client.refresh_feed(feed_id)
    click.echo(f"Feed {feed_id} refreshed.")


@feeds_group.command(name="refresh-all")
@pass_client
def feeds_refresh_all(client: "MinifluxClientWrapper") -> None:
    """Refresh all feeds."""
    client.refresh_all_feeds()
    click.echo("All feeds refreshed.")


@feeds_group.command(name="discover")
@click.argument("url")
@pass_client
def feeds_discover(client: "MinifluxClientWrapper", url: str) -> None:
    """Discover subscriptions on a URL."""
    data = client.discover(url)
    if _ctx_json():
        render_json(data)
        return
    if not data:
        click.echo("No feeds discovered.")
        return
    render_table(
        [{"URL": d.get("url", ""), "Title": d.get("title", "")} for d in data],
        columns=["URL", "Title"],
        title="Discovered Feeds",
    )


@feeds_group.command(name="icon")
@click.argument("feed_id", type=int)
@pass_client
def feeds_icon(client: "MinifluxClientWrapper", feed_id: int) -> None:
    """Get feed icon."""
    data = client.get_icon_by_feed_id(feed_id)
    if _ctx_json():
        render_json(data)
        return
    render_panel(data, title="Feed Icon")


@feeds_group.command(name="entries")
@click.argument("feed_id", type=int)
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
def feeds_entries(
    client: "MinifluxClientWrapper",
    feed_id: int,
    status: str | None,
    order: str,
    direction: str,
    limit: int,
    offset: int,
    search: str | None,
) -> None:
    """List entries for a feed."""
    kwargs: dict = {"order": order, "direction": direction, "limit": limit, "offset": offset}
    if status is not None:
        kwargs["status"] = status
    if search is not None:
        kwargs["search"] = search
    data = client.get_feed_entries(feed_id, **kwargs)
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
        title=f"Feed {feed_id} Entries",
    )


@feeds_group.command(name="mark-read")
@click.argument("feed_id", type=int)
@pass_client
def feeds_mark_read(client: "MinifluxClientWrapper", feed_id: int) -> None:
    """Mark all entries in a feed as read."""
    client.mark_feed_entries_as_read(feed_id)
    click.echo(f"All entries in feed {feed_id} marked as read.")

"""User management commands."""

from typing import TYPE_CHECKING

import click

from miniflux_cli.cli import pass_client
from miniflux_cli.cli import users as users_group
from miniflux_cli.exceptions import CLIError
from miniflux_cli.formatting import render_json, render_panel, render_table

if TYPE_CHECKING:
    from miniflux_cli.client import MinifluxClientWrapper


def _ctx_json() -> bool:
    return bool(click.get_current_context().obj.json_mode)


@users_group.command(name="list")
@pass_client
def users_list(client: "MinifluxClientWrapper") -> None:
    """List all users."""
    data = client.get_users()
    if _ctx_json():
        render_json(data)
        return
    if not data:
        click.echo("No users found.")
        return
    render_table(
        [
            {
                "ID": u["id"],
                "Username": u["username"],
                "Admin": u.get("is_admin", False),
                "Theme": u.get("theme", ""),
            }
            for u in data
        ],
        columns=["ID", "Username", "Admin", "Theme"],
        title="Users",
    )


@users_group.command(name="me")
@pass_client
def users_me(client: "MinifluxClientWrapper") -> None:
    """Get current user."""
    data = client.me()
    if _ctx_json():
        render_json(data)
        return
    render_panel(data, title="Current User")


@users_group.command(name="get")
@click.argument("identifier")
@pass_client
def users_get(client: "MinifluxClientWrapper", identifier: str) -> None:
    """Get a user by ID or username."""
    if identifier.isdigit():
        data = client.get_user_by_id(int(identifier))
    else:
        data = client.get_user_by_username(identifier)
    if _ctx_json():
        render_json(data)
        return
    render_panel(data, title=f"User {identifier}")


@users_group.command(name="create")
@click.argument("username")
@click.argument("password")
@click.option("--admin", is_flag=True, help="Create as admin.")
@click.option("--theme", help="User theme.")
@click.option("--language", help="User language.")
@click.option("--timezone", help="User timezone.")
@pass_client
def users_create(
    client: "MinifluxClientWrapper",
    username: str,
    password: str,
    admin: bool,
    theme: str | None,
    language: str | None,
    timezone: str | None,
) -> None:
    """Create a user."""
    data = client.create_user(username, password, is_admin=admin)
    user_id = data.get("id")
    # The official Python client only supports username/password/is_admin on create.
    # Apply additional fields via update if necessary.
    extra: dict = {}
    if theme is not None:
        extra["theme"] = theme
    if language is not None:
        extra["language"] = language
    if timezone is not None:
        extra["timezone"] = timezone
    if extra and user_id is not None:
        data = client.update_user(user_id, **extra)
    if _ctx_json():
        render_json(data)
        return
    click.echo(f"User created: ID={user_id}")


@users_group.command(name="update")
@click.argument("user_id", type=int)
@click.option("--username", help="New username.")
@click.option("--password", help="New password.")
@click.option("--admin", type=bool, help="Admin flag.")
@click.option("--theme", help="Theme.")
@click.option("--language", help="Language.")
@click.option("--timezone", help="Timezone.")
@pass_client
def users_update(
    client: "MinifluxClientWrapper",
    user_id: int,
    username: str | None,
    password: str | None,
    admin: bool | None,
    theme: str | None,
    language: str | None,
    timezone: str | None,
) -> None:
    """Update a user."""
    payload: dict = {}
    if username is not None:
        payload["username"] = username
    if password is not None:
        payload["password"] = password
    if admin is not None:
        payload["is_admin"] = admin
    if theme is not None:
        payload["theme"] = theme
    if language is not None:
        payload["language"] = language
    if timezone is not None:
        payload["timezone"] = timezone
    if not payload:
        raise CLIError("No fields provided to update.", exit_code=2)
    data = client.update_user(user_id, **payload)
    if _ctx_json():
        render_json(data)
        return
    click.echo(f"User {user_id} updated.")


@users_group.command(name="delete")
@click.argument("user_id", type=int)
@pass_client
def users_delete(client: "MinifluxClientWrapper", user_id: int) -> None:
    """Delete a user."""
    client.delete_user(user_id)
    click.echo(f"User {user_id} deleted.")


@users_group.command(name="mark-read")
@click.argument("user_id", type=int)
@pass_client
def users_mark_read(client: "MinifluxClientWrapper", user_id: int) -> None:
    """Mark all entries for a user as read."""
    client.mark_user_entries_as_read(user_id)
    click.echo(f"All entries for user {user_id} marked as read.")

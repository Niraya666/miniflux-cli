"""Entry point for `python -m miniflux_cli` and the console script."""

from miniflux_cli.cli import cli

# Import command modules so they register themselves against the CLI groups.
from miniflux_cli.commands import (  # noqa: F401
    apikeys,
    categories,
    entries,
    feeds,
    opml,
    system,
    users,
)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()

"""Output formatting helpers: JSON and Rich tables."""

import json
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def render_json(data: Any) -> None:
    """Print data as pretty-printed JSON."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def render_table(rows: list[dict[str, Any]], columns: list[str], title: str | None = None) -> None:
    """Render a list of dicts as a Rich table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(row.get(col, "")) for col in columns])
    console.print(table)


def render_panel(data: dict[str, Any], title: str | None = None) -> None:
    """Render a single dict as a Rich panel."""
    lines = "\n".join(f"[bold]{k}:[/bold] {v}" for k, v in data.items())
    console.print(Panel(lines, title=title))

# miniflux-cli

> [中文文档](README.zh.md)

A Python CLI for managing Miniflux RSS feeds remotely, optimized for agent and programmatic usage.

## Features

- **Full API Coverage**: Feeds, Categories, Entries, OPML, Users, API Keys, System
- **Agent-friendly**: Global `--json` flag for structured output
- **Multiple Auth Methods**: API Key (recommended) or Username/Password
- **Configuration Flexibility**: Environment variables or config file (TOML/JSON)
- **Clean Exit Codes**: Suitable for scripting and automation

## Installation

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Quick Start

### Configuration

**Environment Variables** (recommended):

```bash
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="your-api-key"
```

Or use Username/Password:

```bash
export MINIFLUX_USERNAME="admin"
export MINIFLUX_PASSWORD="secret"
```

**Config File** (`~/.config/miniflux-cli/config.toml`):

```toml
url = "https://miniflux.example.org"
api_key = "your-api-key"
timeout = 30.0
```

Use custom path:

```bash
miniflux-cli --config /path/to/config.toml feeds list
```

## Usage Examples

```bash
# List all feeds
miniflux-cli feeds list

# Output as JSON for agents
miniflux-cli --json feeds list

# Create a feed
miniflux-cli feeds create "https://news.ycombinator.com/rss" --category-id 2

# Refresh all feeds
miniflux-cli feeds refresh-all

# List unread entries
miniflux-cli --json entries list --status unread --limit 10

# Mark entry as read
miniflux-cli entries mark-read 123

# Toggle bookmark
miniflux-cli entries bookmark 123

# Export OPML
miniflux-cli opml export > feeds.opml

# Import OPML
miniflux-cli opml import feeds.opml

# System health
miniflux-cli system health
```

## Command Reference

```
miniflux-cli [GLOBAL_OPTS] <NOUN> <VERB> [ARGS/OPTS]
```

### Feeds

| Command | Description |
|---------|-------------|
| `feeds list` | List all feeds |
| `feeds get <id>` | Get a single feed |
| `feeds create <url>` | Create a new feed |
| `feeds update <id>` | Update a feed |
| `feeds delete <id>` | Delete a feed |
| `feeds refresh <id>` | Refresh a single feed |
| `feeds refresh-all` | Refresh all feeds |
| `feeds discover <url>` | Discover subscriptions |
| `feeds entries <id>` | List entries for a feed |
| `feeds mark-read <id>` | Mark all entries in feed as read |

### Categories

| Command | Description |
|---------|-------------|
| `categories list` | List all categories |
| `categories create <title>` | Create a category |
| `categories update <id> <title>` | Update a category |
| `categories delete <id>` | Delete a category |
| `categories refresh <id>` | Refresh feeds in category |
| `categories mark-read <id>` | Mark category entries as read |
| `categories entries <id>` | List entries in category |
| `categories feeds <id>` | List feeds in category |

### Entries

| Command | Description |
|---------|-------------|
| `entries list` | List entries globally |
| `entries get <id>` | Get a single entry |
| `entries mark-read <id>...` | Mark entries as read |
| `entries mark-unread <id>...` | Mark entries as unread |
| `entries bookmark <id>` | Toggle bookmark |
| `entries fetch-content <id>` | Fetch original content |
| `entries save <id>` | Save to third-party integrations |

### OPML

| Command | Description |
|---------|-------------|
| `opml export` | Export feeds as OPML |
| `opml import <file>` | Import OPML file |

### Users

| Command | Description |
|---------|-------------|
| `users list` | List all users |
| `users me` | Get current user |
| `users get <id\|username>` | Get a specific user |
| `users create <username> <password>` | Create a user |
| `users update <id>` | Update a user |
| `users delete <id>` | Delete a user |
| `users mark-read <id>` | Mark all user entries as read |

### API Keys

| Command | Description |
|---------|-------------|
| `api-keys list` | List API keys |
| `api-keys create <description>` | Create an API key |
| `api-keys delete <id>` | Delete an API key |

### System

| Command | Description |
|---------|-------------|
| `system health` | Health check |
| `system version` | Get Miniflux version |
| `system counters` | Unread/read counters |
| `system integrations` | Integrations status |
| `system flush-history` | Flush history |

## Global Options

- `--config FILE` — Path to config file
- `--json` — Output raw JSON
- `-v, --verbose` — Verbose error output

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Generic CLI/API error |
| 2 | Invalid argument or bad request |
| 3 | Authentication/authorization failure |
| 4 | Resource not found |
| 5 | Server error (5xx) |

## Testing

```bash
# Run linters
make lint

# Run unit tests
make test

# Run end-to-end tests (requires Docker)
make e2e
```

## Documentation

- [中文文档](README.zh.md)
- [docs/miniflux-cli-usage.md](docs/miniflux-cli-usage.md) — detailed Chinese usage guide

## License

MIT

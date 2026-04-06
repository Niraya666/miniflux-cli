# miniflux-cli

A Python CLI for managing Miniflux RSS feeds remotely, optimized for agent and programmatic usage.

基于 Python 开发的 Miniflux RSS 远程管理命令行工具，专为 Agent 和程序化场景设计。

---

## Features | 特性

- **Full API Coverage** | 完整 API 封装: Feeds, Categories, Entries, OPML, Users, API Keys, System
- **Agent-friendly** | 适合 Agent: Global `--json` flag for structured output
- **Multiple Auth Methods** | 多种认证: API Key (recommended) or Username/Password
- **Configuration Flexibility** | 配置灵活: Environment variables or config file (TOML/JSON)
- **Clean Exit Codes** | 清晰退出码: Suitable for scripting and automation

---

## Installation | 安装

```bash
pip install -e .
```

For development | 开发依赖安装:

```bash
pip install -e ".[dev]"
```

---

## Quick Start | 快速开始

### Configuration | 配置

**Environment Variables | 环境变量** (recommended | 推荐):

```bash
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="your-api-key"
```

Or use Username/Password | 或使用用户名密码:

```bash
export MINIFLUX_USERNAME="admin"
export MINIFLUX_PASSWORD="secret"
```

**Config File | 配置文件** (`~/.config/miniflux-cli/config.toml`):

```toml
url = "https://miniflux.example.org"
api_key = "your-api-key"
timeout = 30.0
```

Use custom path | 使用自定义路径:

```bash
miniflux-cli --config /path/to/config.toml feeds list
```

---

## Usage Examples | 使用示例

```bash
# List all feeds | 列出所有订阅
miniflux-cli feeds list

# Output as JSON for agents | JSON 输出供 Agent 解析
miniflux-cli --json feeds list

# Create a feed | 添加订阅
miniflux-cli feeds create "https://news.ycombinator.com/rss" --category-id 2

# Refresh all feeds | 刷新全部订阅
miniflux-cli feeds refresh-all

# List unread entries | 列出未读文章
miniflux-cli --json entries list --status unread --limit 10

# Mark entry as read | 标记文章已读
miniflux-cli entries mark-read 123

# Toggle bookmark | 收藏/取消收藏
miniflux-cli entries bookmark 123

# Export OPML | 导出 OPML
miniflux-cli opml export > feeds.opml

# Import OPML | 导入 OPML
miniflux-cli opml import feeds.opml

# System health | 系统健康检查
miniflux-cli system health
```

---

## Command Reference | 命令参考

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

---

## Global Options | 全局选项

- `--config FILE` — Path to config file | 配置文件路径
- `--json` — Output raw JSON | 输出原始 JSON
- `-v, --verbose` — Verbose error output | 显示详细错误信息

---

## Testing | 测试

```bash
# Run linters | 运行静态检查
make lint

# Run unit tests | 运行单元测试
make test

# Run end-to-end tests (requires Docker) | 运行端到端测试（需要 Docker）
make e2e
```

---

## Documentation | 文档

See [docs/miniflux-cli-usage.md](docs/miniflux-cli-usage.md) for detailed usage in Chinese.

详细中文使用文档请查看 [docs/miniflux-cli-usage.md](docs/miniflux-cli-usage.md)。

---

## License | 许可证

MIT

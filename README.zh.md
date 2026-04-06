# miniflux-cli

> [English README](README.md)

基于 Python 开发的 Miniflux RSS 远程管理命令行工具，专为 Agent 和程序化场景设计。

## 特性

- **完整 API 封装**: Feeds, Categories, Entries, OPML, Users, API Keys, System
- **适合 Agent**: 全局 `--json` 参数输出结构化 JSON
- **多种认证方式**: 推荐使用 API Key，也支持用户名/密码
- **配置灵活**: 支持环境变量和配置文件（TOML/JSON）
- **清晰退出码**: 便于脚本和自动化场景使用

## 安装

```bash
pip install -e .
```

开发依赖安装:

```bash
pip install -e ".[dev]"
```

## 快速开始

### 配置

**环境变量** (推荐):

```bash
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="your-api-key"
```

或使用用户名密码:

```bash
export MINIFLUX_USERNAME="admin"
export MINIFLUX_PASSWORD="secret"
```

**配置文件** (`~/.config/miniflux-cli/config.toml`):

```toml
url = "https://miniflux.example.org"
api_key = "your-api-key"
timeout = 30.0
```

使用自定义路径:

```bash
miniflux-cli --config /path/to/config.toml feeds list
```

## 使用示例

```bash
# 列出所有订阅
miniflux-cli feeds list

# JSON 输出供 Agent 解析
miniflux-cli --json feeds list

# 添加订阅
miniflux-cli feeds create "https://news.ycombinator.com/rss" --category-id 2

# 刷新全部订阅
miniflux-cli feeds refresh-all

# 列出未读文章
miniflux-cli --json entries list --status unread --limit 10

# 标记文章已读
miniflux-cli entries mark-read 123

# 收藏/取消收藏
miniflux-cli entries bookmark 123

# 导出 OPML
miniflux-cli opml export > feeds.opml

# 导入 OPML
miniflux-cli opml import feeds.opml

# 系统健康检查
miniflux-cli system health
```

## 命令参考

```
miniflux-cli [全局选项] <名词> <动词> [参数/选项]
```

### Feeds

| 命令 | 说明 |
|---------|-------------|
| `feeds list` | 列出所有订阅 |
| `feeds get <id>` | 获取单个订阅 |
| `feeds create <url>` | 创建新订阅 |
| `feeds update <id>` | 更新订阅 |
| `feeds delete <id>` | 删除订阅 |
| `feeds refresh <id>` | 刷新单个订阅 |
| `feeds refresh-all` | 刷新全部订阅 |
| `feeds discover <url>` | 发现订阅源 |
| `feeds entries <id>` | 列出订阅下的文章 |
| `feeds mark-read <id>` | 标记订阅下所有文章已读 |

### Categories

| 命令 | 说明 |
|---------|-------------|
| `categories list` | 列出所有分类 |
| `categories create <title>` | 创建分类 |
| `categories update <id> <title>` | 更新分类 |
| `categories delete <id>` | 删除分类 |
| `categories refresh <id>` | 刷新分类下所有订阅 |
| `categories mark-read <id>` | 标记分类下所有文章已读 |
| `categories entries <id>` | 列出分类下文章 |
| `categories feeds <id>` | 列出分类下订阅 |

### Entries

| 命令 | 说明 |
|---------|-------------|
| `entries list` | 全局列出文章 |
| `entries get <id>` | 获取单篇文章 |
| `entries mark-read <id>...` | 标记文章已读 |
| `entries mark-unread <id>...` | 标记文章未读 |
| `entries bookmark <id>` | 切换收藏状态 |
| `entries fetch-content <id>` | 获取原始内容 |
| `entries save <id>` | 保存到第三方集成服务 |

### OPML

| 命令 | 说明 |
|---------|-------------|
| `opml export` | 导出 OPML |
| `opml import <file>` | 导入 OPML |

### Users

| 命令 | 说明 |
|---------|-------------|
| `users list` | 列出所有用户 |
| `users me` | 获取当前用户 |
| `users get <id\|username>` | 获取指定用户 |
| `users create <username> <password>` | 创建用户 |
| `users update <id>` | 更新用户 |
| `users delete <id>` | 删除用户 |
| `users mark-read <id>` | 标记用户所有文章已读 |

### API Keys

| 命令 | 说明 |
|---------|-------------|
| `api-keys list` | 列出 API 密钥 |
| `api-keys create <description>` | 创建 API 密钥 |
| `api-keys delete <id>` | 删除 API 密钥 |

### System

| 命令 | 说明 |
|---------|-------------|
| `system health` | 健康检查 |
| `system version` | 获取 Miniflux 版本 |
| `system counters` | 未读/已读统计 |
| `system integrations` | 集成状态 |
| `system flush-history` | 清空历史 |

## 全局选项

- `--config FILE` — 配置文件路径
- `--json` — 输出原始 JSON
- `-v, --verbose` — 显示详细错误信息

## 退出码

| 退出码 | 含义 |
|------|---------|
| 0 | 成功 |
| 1 | 通用 CLI/API 错误 |
| 2 | 参数错误或请求格式错误 |
| 3 | 认证/授权失败 |
| 4 | 资源不存在 |
| 5 | 服务器内部错误（5xx） |

## 测试

```bash
# 运行静态检查
make lint

# 运行单元测试
make test

# 运行端到端测试（需要 Docker）
make e2e
```

## 文档

- [English README](README.md)
- [docs/miniflux-cli-usage.md](docs/miniflux-cli-usage.md) — 详细中文使用指南

## 许可证

MIT

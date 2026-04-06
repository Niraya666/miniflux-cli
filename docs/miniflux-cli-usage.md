# miniflux-cli 使用文档

`miniflux-cli` 是一个基于 Python 开发的命令行工具，用于远程管理 Miniflux RSS 服务。它封装了 Miniflux 官方 REST API，提供人类可读的表格输出和机器友好的 `--json` 输出，非常适合 Agent 和脚本化场景使用。

---

## 目录

1. [安装](#安装)
2. [配置](#配置)
3. [命令结构](#命令结构)
4. [Feeds 管理](#feeds-管理)
5. [Categories 管理](#categories-管理)
6. [Entries 管理](#entries-管理)
7. [OPML 导入/导出](#opml-导入导出)
8. [Users 管理](#users-管理)
9. [API Keys 管理](#api-keys-管理)
10. [System 信息](#system-信息)
11. [Agent/脚本化使用建议](#agent脚本化使用建议)

---

## 安装

### 从源码安装（推荐开发方式）

```bash
cd /Users/zhongyuanlian/playground/miniflux
pip install -e .
```

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

安装完成后，系统中会出现 `miniflux-cli` 命令：

```bash
miniflux-cli --help
```

也可以用 `python -m` 方式运行：

```bash
python -m miniflux_cli --help
```

---

## 配置

`miniflux-cli` 支持两种配置方式：环境变量 和 配置文件。

### 环境变量（推荐）

```bash
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="your-api-key"
```

如果没有 API Key，也可以使用用户名/密码：

```bash
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_USERNAME="admin"
export MINIFLUX_PASSWORD="secret"
```

### 配置文件

默认配置文件路径：`~/.config/miniflux-cli/config.toml`

```toml
url = "https://miniflux.example.org"
api_key = "your-api-key"
timeout = 30.0
```

也支持 JSON 格式：

```json
{
  "url": "https://miniflux.example.org",
  "api_key": "your-api-key"
}
```

使用 `--config` 参数指定自定义路径：

```bash
miniflux-cli --config /path/to/config.toml feeds list
```

### 全局选项

```bash
miniflux-cli [GLOBAL_OPTS] <NOUN> <VERB> [ARGS/OPTS]
```

全局选项：

- `--config FILE`：指定配置文件
- `--json`：输出原始 JSON
- `-v, --verbose`：显示详细错误信息

---

## 命令结构

命令采用 `<名词> <动词>` 的层级结构：

```
miniflux-cli feeds list
miniflux-cli feeds create <url>
miniflux-cli entries list --status unread
miniflux-cli categories create "Tech"
```

支持的名词：`feeds`, `categories`, `entries`, `opml`, `users`, `api-keys`, `system`

---

## Feeds 管理

### 列出所有 Feeds

```bash
miniflux-cli feeds list
miniflux-cli --json feeds list
```

### 获取单个 Feed

```bash
miniflux-cli feeds get <feed_id>
miniflux-cli --json feeds get 42
```

### 创建 Feed

```bash
miniflux-cli feeds create "https://news.ycombinator.com/rss"

# 指定分类和其他选项
miniflux-cli feeds create "https://example.com/feed.xml" \
  --category-id 2 \
  --title "My Feed" \
  --crawler \
  --user-agent "Mozilla/5.0"
```

可用选项：

- `--category-id`：分类 ID
- `--title`：自定义标题
- `--crawler`：启用爬虫
- `--user-agent`：自定义 User-Agent
- `--username` / `--password`：Feed 认证
- `--scraper-rules` / `--rewrite-rules` / `--blocklist-rules` / `--keeplist-rules`：规则
- `--ignore-htlc`：忽略 HTTP 缓存
- `--fetch-original`：获取原始内容

### 更新 Feed

```bash
miniflux-cli feeds update <feed_id> --title "New Title" --category-id 3
```

### 删除 Feed

```bash
miniflux-cli feeds delete <feed_id>
```

### 刷新 Feed

```bash
# 刷新单个
miniflux-cli feeds refresh <feed_id>

# 刷新全部
miniflux-cli feeds refresh-all
```

### 发现订阅源

```bash
miniflux-cli feeds discover "https://example.com"
```

### 查看 Feed 下的 Entries

```bash
miniflux-cli feeds entries <feed_id> --status unread --limit 20
```

### 标记 Feed 下所有文章已读

```bash
miniflux-cli feeds mark-read <feed_id>
```

---

## Categories 管理

### 列出分类

```bash
miniflux-cli categories list
miniflux-cli --json categories list
```

### 创建分类

```bash
miniflux-cli categories create "Technology"
```

### 更新分类

```bash
miniflux-cli categories update <category_id> "New Name"
```

### 删除分类

```bash
miniflux-cli categories delete <category_id>
```

### 刷新分类下全部 Feeds

```bash
miniflux-cli categories refresh <category_id>
```

### 标记分类下全部文章已读

```bash
miniflux-cli categories mark-read <category_id>
```

### 查看分类下 Entries / Feeds

```bash
miniflux-cli categories entries <category_id> --limit 10
miniflux-cli categories feeds <category_id>
```

---

## Entries 管理

### 列出文章

```bash
# 默认列出全部
miniflux-cli entries list

# 只列出未读
miniflux-cli entries list --status unread

# 只列出收藏
miniflux-cli entries list --starred

# 按分类或 Feed 过滤
miniflux-cli entries list --category-id 2 --feed-id 5 --limit 20
```

可用过滤选项：

- `--status`：`unread` | `read` | `removed`
- `--starred`：只显示收藏
- `--limit` / `--offset`：分页
- `--before` / `--after`：按 Entry ID 范围
- `--search`：搜索关键词
- `--category-id` / `--feed-id`：按分类或 Feed 过滤

### 获取单篇文章

```bash
miniflux-cli entries get <entry_id>
```

### 标记已读 / 未读

```bash
# 标记已读（支持多个 ID）
miniflux-cli entries mark-read 123 124 125

# 标记未读
miniflux-cli entries mark-unread 123
```

### 收藏（Bookmark）

```bash
miniflux-cli entries bookmark <entry_id>
```

### 获取原始内容

```bash
miniflux-cli entries fetch-content <entry_id>
```

### 保存到第三方服务

```bash
miniflux-cli entries save <entry_id>
```

---

## OPML 导入/导出

### 导出

```bash
miniflux-cli opml export > feeds.opml
```

### 导入

```bash
miniflux-cli opml import feeds.opml
```

---

## Users 管理

### 列出用户

```bash
miniflux-cli users list
```

### 当前用户信息

```bash
miniflux-cli users me
```

### 查看指定用户

```bash
miniflux-cli users get <user_id>
miniflux-cli users get <username>
```

### 创建用户

```bash
miniflux-cli users create john secret123 --admin --theme "dark_serif"
```

### 更新用户

```bash
miniflux-cli users update <user_id> --password "newpass" --theme "light_serif"
```

### 删除用户

```bash
miniflux-cli users delete <user_id>
```

### 标记用户所有文章已读

```bash
miniflux-cli users mark-read <user_id>
```

---

## API Keys 管理

### 列出 API Keys

```bash
miniflux-cli api-keys list
```

### 创建 API Key

```bash
miniflux-cli api-keys create "CLI Access"
```

> 创建后会立即显示 Token，请妥善保存。

### 删除 API Key

```bash
miniflux-cli api-keys delete <key_id>
```

---

## System 信息

### 健康检查

```bash
miniflux-cli system health
```

### 版本信息

```bash
miniflux-cli system version
miniflux-cli system info
```

### 未读/已读统计

```bash
miniflux-cli system counters
miniflux-cli --json system counters
```

### 集成状态

```bash
miniflux-cli system integrations
```

### 清空历史

```bash
miniflux-cli system flush-history
```

---

## Agent/脚本化使用建议

### 1. 始终使用 `--json` 输出

对于需要被脚本或 Agent 解析的结果，请在全局位置加上 `--json`：

```bash
miniflux-cli --json feeds list
miniflux-cli --json entries list --status unread --limit 5
```

### 2. 结合 `jq` 使用

```bash
# 获取第一个未读文章的 ID
ENTRY_ID=$(miniflux-cli --json entries list --status unread --limit 1 | \
  jq '.entries[0].id')

# 标记已读
miniflux-cli entries mark-read "$ENTRY_ID"
```

### 3. 典型自动化脚本示例

```bash
#!/usr/bin/env bash
set -euo pipefail

export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="xxx"

# 刷新全部订阅
miniflux-cli feeds refresh-all

# 获取所有未读文章
miniflux-cli --json entries list --status unread --limit 50

# 获取分类列表
miniflux-cli --json categories list
```

### 4. 退出码说明

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | 通用 CLI/API 错误 |
| 2 | 参数错误或请求格式错误 |
| 3 | 认证/授权失败 |
| 4 | 资源不存在 |
| 5 | 服务器内部错误（5xx） |

---

## 开发与测试

```bash
# 安装开发依赖
make install-dev

# 代码格式化
make fmt

# 静态检查
make lint

# 运行单元测试
make test

# 运行端到端测试（需要 Docker）
make e2e
```

---

## 常见问题

### Q: `--json` 放在哪里？

`--json` 是全局选项，必须放在 `miniflux-cli` 后面、子命令前面：

```bash
# 正确
miniflux-cli --json feeds list

# 错误
miniflux-cli feeds list --json
```

### Q: 如何批量添加订阅？

可以用脚本循环调用 `feeds create`：

```bash
for url in $(cat urls.txt); do
  miniflux-cli feeds create "$url" --category-id 2
done
```

### Q: 是否支持本地服务端 CLI 的管理方式？

不支持。`miniflux-cli` 完全基于 Miniflux REST API 工作，因此需要目标实例暴露 HTTP 接口并配置正确的认证信息。

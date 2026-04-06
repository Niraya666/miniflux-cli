#!/usr/bin/env bash
set -euo pipefail

export MINIFLUX_URL="http://localhost"
export MINIFLUX_USERNAME="admin"
export MINIFLUX_PASSWORD="test123"

SUFFIX=$(date +%s)
CATEGORY_NAME="Tech-${SUFFIX}"

echo "=== 1. System checks ==="
miniflux-cli system health
miniflux-cli --json system version
miniflux-cli --json users me

echo "=== 2. Categories ==="
miniflux-cli categories create "${CATEGORY_NAME}"
CATEGORY_ID=$(miniflux-cli --json categories list | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(next(c['id'] for c in data if c['title'] == '${CATEGORY_NAME}'))
")
echo "Created category ID: ${CATEGORY_ID}"

echo "=== 3. Feeds ==="
miniflux-cli feeds create "https://news.ycombinator.com/rss" --category-id "${CATEGORY_ID}"
FEED_ID=$(miniflux-cli --json feeds list | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(next(f['id'] for f in data if f['feed_url'] == 'https://news.ycombinator.com/rss'))
")
echo "Created feed ID: ${FEED_ID}"

miniflux-cli --json feeds get "${FEED_ID}"
miniflux-cli feeds refresh "${FEED_ID}"
miniflux-cli feeds refresh-all

echo "=== 4. Entries ==="
# Give the scheduler a moment to populate entries
sleep 3
miniflux-cli --json entries list --limit 5

ENTRY_ID=$(miniflux-cli --json entries list --limit 1 | python3 -c "
import json, sys
data = json.load(sys.stdin)
entries = data.get('entries', []) if isinstance(data, dict) else data
if entries:
    print(entries[0]['id'])
else:
    print('')
" || true)

if [ -n "${ENTRY_ID}" ]; then
    echo "Marking entry ${ENTRY_ID} as read"
    miniflux-cli entries mark-read "${ENTRY_ID}"
    miniflux-cli entries bookmark "${ENTRY_ID}"
fi

echo "=== 5. OPML ==="
miniflux-cli opml export > /tmp/test.opml
miniflux-cli opml import /tmp/test.opml

echo "=== 6. Counters ==="
miniflux-cli --json system counters

echo "=== 7. Cleanup ==="
miniflux-cli feeds delete "${FEED_ID}"
miniflux-cli categories delete "${CATEGORY_ID}"

echo "All e2e tests passed!"

#!/usr/bin/env bash
set -euo pipefail

export MINIFLUX_URL="http://localhost"
export MINIFLUX_USERNAME="admin"
export MINIFLUX_PASSWORD="test123"

SUFFIX=$(date +%s)
CATEGORY_NAME="TestCat-${SUFFIX}"
FEED_URL="https://news.ycombinator.com/rss"
PASS=0
FAIL=0

# Pre-clean existing test feed if leftover from previous run
EXISTING_FEED_ID=$(miniflux-cli --json feeds list 2>/dev/null | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(next((f['id'] for f in data if f['feed_url'] == '${FEED_URL}'), ''))
except Exception:
    print('')
" || true)
if [ -n "${EXISTING_FEED_ID}" ]; then
    miniflux-cli feeds delete "${EXISTING_FEED_ID}" >/dev/null 2>&1 || true
fi

run_test() {
    local desc="$1"
    shift
    if "$@" >/dev/null 2>&1; then
        echo "[PASS] ${desc}"
        ((PASS++)) || true
    else
        echo "[FAIL] ${desc}"
        ((FAIL++)) || true
    fi
}

json_test() {
    local desc="$1"
    shift
    if "$@" | python3 -m json.tool >/dev/null 2>&1; then
        echo "[PASS] ${desc}"
        ((PASS++)) || true
    else
        echo "[FAIL] ${desc}"
        ((FAIL++)) || true
    fi
}

echo "========================================"
echo "System Commands"
echo "========================================"
run_test "system health" miniflux-cli system health
run_test "system version" miniflux-cli system version
run_test "system info" miniflux-cli system info
json_test "system counters --json" miniflux-cli --json system counters
json_test "system integrations --json" miniflux-cli --json system integrations
run_test "system flush-history" miniflux-cli system flush-history

echo ""
echo "========================================"
echo "User Commands"
echo "========================================"
json_test "users me" miniflux-cli --json users me
json_test "users list" miniflux-cli --json users list
json_test "users get admin" miniflux-cli --json users get admin

echo ""
echo "========================================"
echo "Category Commands"
echo "========================================"
run_test "categories create" miniflux-cli categories create "${CATEGORY_NAME}"
CATEGORY_ID=$(miniflux-cli --json categories list | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(next(c['id'] for c in data if c['title'] == '${CATEGORY_NAME}'))
")
echo "Category ID: ${CATEGORY_ID}"
json_test "categories list" miniflux-cli --json categories list
json_test "categories get" miniflux-cli --json categories get "${CATEGORY_ID}"
json_test "categories feeds" miniflux-cli --json categories feeds "${CATEGORY_ID}"
json_test "categories entries" miniflux-cli --json categories entries "${CATEGORY_ID}"
run_test "categories mark-read" miniflux-cli categories mark-read "${CATEGORY_ID}"
run_test "categories update" miniflux-cli categories update "${CATEGORY_ID}" "${CATEGORY_NAME}-Updated"

echo ""
echo "========================================"
echo "Feed Commands"
echo "========================================"
run_test "feeds create" miniflux-cli feeds create "${FEED_URL}" --category-id "${CATEGORY_ID}"
FEED_ID=$(miniflux-cli --json feeds list | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(next(f['id'] for f in data if f['feed_url'] == '${FEED_URL}'))
")
echo "Feed ID: ${FEED_ID}"
json_test "feeds list" miniflux-cli --json feeds list
json_test "feeds get" miniflux-cli --json feeds get "${FEED_ID}"
json_test "feeds icon" miniflux-cli --json feeds icon "${FEED_ID}"
json_test "feeds entries" miniflux-cli --json feeds entries "${FEED_ID}" --limit 5
run_test "feeds refresh" miniflux-cli feeds refresh "${FEED_ID}"
run_test "feeds refresh-all" miniflux-cli feeds refresh-all
run_test "feeds update" miniflux-cli feeds update "${FEED_ID}" --title "HN-Updated"
run_test "feeds mark-read" miniflux-cli feeds mark-read "${FEED_ID}"

echo ""
echo "========================================"
echo "Discover & OPML"
echo "========================================"
json_test "feeds discover" miniflux-cli --json feeds discover "https://news.ycombinator.com"
run_test "opml export" bash -c "miniflux-cli opml export > /tmp/test_${SUFFIX}.opml"
run_test "opml import" miniflux-cli opml import "/tmp/test_${SUFFIX}.opml"

echo ""
echo "========================================"
echo "Entry Commands"
echo "========================================"
sleep 3
ENTRY_ID=$(miniflux-cli --json entries list --feed-id "${FEED_ID}" --limit 1 | python3 -c "
import json, sys
data = json.load(sys.stdin)
entries = data.get('entries', [])
print(entries[0]['id'] if entries else '')
" || true)

if [ -n "${ENTRY_ID}" ]; then
    echo "Entry ID: ${ENTRY_ID}"
    json_test "entries get" miniflux-cli --json entries get "${ENTRY_ID}"
    run_test "entries mark-unread" miniflux-cli entries mark-unread "${ENTRY_ID}"
    run_test "entries mark-read" miniflux-cli entries mark-read "${ENTRY_ID}"
    run_test "entries bookmark" miniflux-cli entries bookmark "${ENTRY_ID}"
    json_test "entries fetch-content" miniflux-cli --json entries fetch-content "${ENTRY_ID}"
    # save may fail if no integration configured, so we run it but don't strictly fail
    miniflux-cli entries save "${ENTRY_ID}" >/dev/null 2>&1 && echo "[PASS] entries save" || echo "[SKIP] entries save (no integration)"
    run_test "entries update" miniflux-cli entries update "${ENTRY_ID}" --title "Updated Title"
else
    echo "[SKIP] No entries available for entry tests"
fi

echo ""
echo "========================================"
echo "User Management Commands"
echo "========================================"
run_test "users create" miniflux-cli users create "testuser_${SUFFIX}" "testpass123"
TEST_USER_ID=$(miniflux-cli --json users list | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(next(u['id'] for u in data if u['username'] == 'testuser_${SUFFIX}'))
")
echo "Test User ID: ${TEST_USER_ID}"
json_test "users get by id" miniflux-cli --json users get "${TEST_USER_ID}"
run_test "users update" miniflux-cli users update "${TEST_USER_ID}" --theme "dark_serif"
# Marking another user's entries as read may be forbidden by API even for admins.
miniflux-cli users mark-read "${TEST_USER_ID}" > /dev/null 2>&1 && echo "[PASS] users mark-read" || echo "[SKIP] users mark-read (API restriction)"
run_test "users delete" miniflux-cli users delete "${TEST_USER_ID}"

echo ""
echo "========================================"
echo "API Key Commands"
echo "========================================"
run_test "api-keys create" miniflux-cli api-keys create "TestKey-${SUFFIX}"
KEY_ID=$(miniflux-cli --json api-keys list | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(next(k['id'] for k in data if k.get('description') == 'TestKey-${SUFFIX}'))
")
echo "API Key ID: ${KEY_ID}"
json_test "api-keys list" miniflux-cli --json api-keys list
run_test "api-keys delete" miniflux-cli api-keys delete "${KEY_ID}"

echo ""
echo "========================================"
echo "Error Handling"
echo "========================================"
# auth fail
run_test "auth fail with wrong password" bash -c "MINIFLUX_PASSWORD=wrong miniflux-cli users me 2>&1 | grep -qi 'unauthorized'"
# not found feed
run_test "not found feed" bash -c "miniflux-cli feeds get 999999 2>&1 | grep -qi 'not found'"

echo ""
echo "========================================"
echo "Cleanup"
echo "========================================"
run_test "feeds delete" miniflux-cli feeds delete "${FEED_ID}"
run_test "categories delete" miniflux-cli categories delete "${CATEGORY_ID}"

echo ""
echo "========================================"
echo "Results: ${PASS} passed, ${FAIL} failed"
echo "========================================"

if [ "${FAIL}" -gt 0 ]; then
    exit 1
fi

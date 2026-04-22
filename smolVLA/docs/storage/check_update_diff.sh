#!/bin/bash
# Compare what changed after an update (default: HEAD@{1} -> HEAD).
# Works for both the superproject and the lerobot submodule pointer/content.

set -euo pipefail

BASE_REF="${1:-HEAD@{1}}"
TARGET_REF="${2:-HEAD}"

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

require_ref() {
    local ref="$1"
    if ! git -C "$ROOT_DIR" rev-parse --verify -q "$ref" >/dev/null; then
        echo "[error] ref not found in superproject: $ref"
        echo "        Try: ./check_update_diff.sh HEAD~1 HEAD"
        exit 1
    fi
}

show_section() {
    local title="$1"
    echo
    echo "===== ${title} ====="
}

require_ref "$BASE_REF"
require_ref "$TARGET_REF"

BASE_COMMIT="$(git -C "$ROOT_DIR" rev-parse "$BASE_REF")"
TARGET_COMMIT="$(git -C "$ROOT_DIR" rev-parse "$TARGET_REF")"

cd "$ROOT_DIR"

echo "[info] compare range: ${BASE_REF} -> ${TARGET_REF}"
echo "[info] repo: $ROOT_DIR"

show_section "Superproject Commits"
if git log --oneline "${BASE_REF}..${TARGET_REF}" | sed -n '1,30p' | grep -q .; then
    git log --oneline "${BASE_REF}..${TARGET_REF}" | sed -n '1,30p'
else
    echo "(no commit differences in superproject)"
fi

show_section "Superproject Changed Files"
if git diff --name-status "$BASE_REF" "$TARGET_REF" | sed -n '1,80p' | grep -q .; then
    git diff --name-status "$BASE_REF" "$TARGET_REF" | sed -n '1,80p'
else
    echo "(no file differences in superproject)"
fi

show_section "Submodule Pointer Change (lerobot)"
if git diff --submodule=log "$BASE_COMMIT" "$TARGET_COMMIT" -- lerobot | grep -q .; then
    git diff --submodule=log "$BASE_COMMIT" "$TARGET_COMMIT" -- lerobot
else
    echo "(lerobot pointer unchanged in superproject)"
fi

BASE_SUB="$(git rev-parse "${BASE_COMMIT}:lerobot" 2>/dev/null || true)"
TARGET_SUB="$(git rev-parse "${TARGET_COMMIT}:lerobot" 2>/dev/null || true)"

if [[ ! "$BASE_SUB" =~ ^[0-9a-f]{40}$ || ! "$TARGET_SUB" =~ ^[0-9a-f]{40}$ ]]; then
    show_section "Submodule Commit Analysis"
    echo "(unable to resolve lerobot gitlink SHAs for one of the refs)"
    exit 0
fi

if [[ -z "$BASE_SUB" || -z "$TARGET_SUB" ]]; then
    show_section "Submodule Commit Analysis"
    echo "(unable to resolve lerobot gitlink in one of the refs)"
    exit 0
fi

if [[ "$BASE_SUB" == "$TARGET_SUB" ]]; then
    show_section "Submodule Commit Analysis"
    echo "(lerobot commit unchanged: ${TARGET_SUB})"
    exit 0
fi

if [[ ! -d "$ROOT_DIR/lerobot/.git" && ! -f "$ROOT_DIR/lerobot/.git" ]]; then
    show_section "Submodule Commit Analysis"
    echo "(lerobot repository not initialized locally)"
    echo "Run: git submodule update --init lerobot"
    exit 0
fi

show_section "lerobot Commits (${BASE_SUB:0:8}..${TARGET_SUB:0:8})"
if git -C "$ROOT_DIR/lerobot" log --oneline --decorate "${BASE_SUB}..${TARGET_SUB}" | sed -n '1,50p' | grep -q .; then
    git -C "$ROOT_DIR/lerobot" log --oneline --decorate "${BASE_SUB}..${TARGET_SUB}" | sed -n '1,50p'
else
    echo "(no visible commit log in local lerobot clone for this range)"
fi

show_section "lerobot Changed Files"
if git -C "$ROOT_DIR/lerobot" diff --name-status "$BASE_SUB" "$TARGET_SUB" | sed -n '1,120p' | grep -q .; then
    git -C "$ROOT_DIR/lerobot" diff --name-status "$BASE_SUB" "$TARGET_SUB" | sed -n '1,120p'
else
    echo "(no changed files in lerobot range)"
fi

show_section "lerobot pyproject.toml Diff"
if git -C "$ROOT_DIR/lerobot" diff "$BASE_SUB" "$TARGET_SUB" -- pyproject.toml | grep -q .; then
    git -C "$ROOT_DIR/lerobot" diff "$BASE_SUB" "$TARGET_SUB" -- pyproject.toml
else
    echo "(pyproject.toml unchanged in this lerobot range)"
fi

#!/usr/bin/env bash
# OQ-025 — Verify git core.hooksPath is set to .githooks.
# PASS: git config output equals ".githooks"
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
EXPECTED=".githooks"
ACTUAL=$(git -C "$REPO" config core.hooksPath 2>/dev/null || echo "")
if [ "$ACTUAL" = "$EXPECTED" ]; then
    echo "PASS: core.hooksPath = '$ACTUAL'"
    exit 0
else
    echo "FAIL: expected '$EXPECTED', got '$ACTUAL' (run ./install.sh to set it)"
    exit 1
fi

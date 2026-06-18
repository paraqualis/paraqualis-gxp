#!/usr/bin/env bash
# OQ-006 — Verify hooks.json matcher covers all four writing tools.
# PASS: matcher field equals "Edit|Write|MultiEdit|NotebookEdit"
set -euo pipefail
HOOKS_JSON="$(cd "$(dirname "$0")/../.." && pwd)/hooks/hooks.json"

MATCHER=$(python3 -c "
import json
with open('$HOOKS_JSON') as f:
    d = json.load(f)
hooks = d['hooks']['PreToolUse']
print(hooks[0]['matcher'])
")

EXPECTED="Edit|Write|MultiEdit|NotebookEdit"
if [ "$MATCHER" = "$EXPECTED" ]; then
    echo "PASS: matcher = '$MATCHER'"
    exit 0
else
    echo "FAIL: expected '$EXPECTED', got '$MATCHER'"
    exit 1
fi

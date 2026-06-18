#!/usr/bin/env bash
# OQ-029 — Verify .env is git-ignored and not tracked.
# PASS: .gitignore contains .env rule; .env is not a tracked file.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
all_pass=true

# Check .gitignore contains .env rule
if grep -q "^\.env$" "$REPO/.gitignore"; then
    echo "PASS: .gitignore contains '.env' rule"
else
    echo "FAIL: .gitignore does not contain '.env' rule"
    all_pass=false
fi

# Check .env is not tracked
if git -C "$REPO" ls-files --error-unmatch .env 2>/dev/null; then
    echo "FAIL: .env IS tracked in git (credential leak risk)"
    all_pass=false
else
    echo "PASS: .env is not tracked in git"
fi

# Check .env.example IS tracked (safe template)
if git -C "$REPO" ls-files --error-unmatch .env.example 2>/dev/null; then
    echo "PASS: .env.example is tracked (template)"
else
    echo "WARN: .env.example is not tracked (no template present)"
fi

$all_pass && exit 0 || exit 1

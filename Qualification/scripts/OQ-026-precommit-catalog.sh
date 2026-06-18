#!/usr/bin/env bash
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
# OQ-026 — pre-commit hook refreshes the OVERVIEW.md catalog and never blocks a commit.
#
# Requirement (OQ.md OQ-026): the pre-commit hook runs build_catalog.py, stages the updated
# docs/OVERVIEW.md, and exits 0 regardless of whether the catalog script succeeds or fails.
#
# Behaviour SOURCED from .githooks/pre-commit:8-13:
#   ROOT="$(git rev-parse --show-toplevel ...)" || exit 0
#   if [ -f "$ROOT/docs/build_catalog.py" ]; then
#     python3 "$ROOT/docs/build_catalog.py" ... && git add "$ROOT/docs/OVERVIEW.md" ...
#   fi
#   exit 0     <- always
#
# SAFE / non-destructive: the real repo is NEVER committed to or staged. The test builds a
# THROWAWAY git repo in a private temp dir, drops in the real .githooks/pre-commit and the
# real docs/build_catalog.py, and exercises the hook there. Two contractual properties are
# checked:
#   (A) catalog refresh + staging: with a valid build_catalog.py, OVERVIEW.md is regenerated
#       and staged.
#   (B) never blocks: with build_catalog.py REMOVED (script unavailable), the hook still
#       exits 0.
# Emits PASS/FAIL; exits non-zero on FAIL.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
HOOK="$REPO/.githooks/pre-commit"
CATALOG="$REPO/docs/build_catalog.py"

for f in "$HOOK" "$CATALOG"; do
  if [ ! -f "$f" ]; then
    echo "FAIL: required source not found: $f"
    exit 1
  fi
done

if ! command -v git >/dev/null 2>&1; then
  echo "FAIL: git not available; cannot exercise the pre-commit hook"
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Build a minimal throwaway repo mirroring the structure build_catalog.py expects:
# ROOT/commands/<family>/<cmd>.md and ROOT/docs/OVERVIEW.md with CATALOG markers.
WORK="$TMP/repo"
mkdir -p "$WORK/docs" "$WORK/commands/demo" "$WORK/skills" "$WORK/agents"
cp "$CATALOG" "$WORK/docs/build_catalog.py"
printf -- '---\ndescription: A demo command.\n---\nBody.\n' > "$WORK/commands/demo/thing.md"
printf -- '# Overview\n\n<!-- CATALOG:START -->\nOLD CONTENT\n<!-- CATALOG:END -->\n' > "$WORK/docs/OVERVIEW.md"

git -C "$WORK" init -q
git -C "$WORK" config user.email oq@example.com
git -C "$WORK" config user.name "OQ Test"
git -C "$WORK" add -A
cp "$HOOK" "$WORK/pre-commit-under-test"
chmod +x "$WORK/pre-commit-under-test"

all_pass=true

# (A) valid catalog script -> OVERVIEW refreshed and staged, exit 0
set +e
( cd "$WORK" && ./pre-commit-under-test ); CODE_A=$?
set -e
if [ "$CODE_A" -ne 0 ]; then
  echo "FAIL: hook exited $CODE_A with a valid build_catalog.py (expected 0)"
  all_pass=false
elif grep -q "OLD CONTENT" "$WORK/docs/OVERVIEW.md"; then
  echo "FAIL: OVERVIEW.md catalog was not refreshed (still contains OLD CONTENT)"
  all_pass=false
elif ! grep -q "/demo:thing" "$WORK/docs/OVERVIEW.md"; then
  echo "FAIL: refreshed catalog does not list the demo command"
  all_pass=false
elif ! git -C "$WORK" diff --cached --name-only | grep -q "docs/OVERVIEW.md"; then
  echo "FAIL: refreshed OVERVIEW.md was not staged by the hook"
  all_pass=false
else
  echo "PASS: hook refreshed OVERVIEW.md catalog and staged it (exit 0)"
fi

# (B) build_catalog.py unavailable -> hook must STILL exit 0 (never blocks)
rm -f "$WORK/docs/build_catalog.py"
set +e
( cd "$WORK" && ./pre-commit-under-test ); CODE_B=$?
set -e
if [ "$CODE_B" -eq 0 ]; then
  echo "PASS: hook exits 0 even when build_catalog.py is unavailable (never blocks)"
else
  echo "FAIL: hook exited $CODE_B when catalog script missing (must never block, expected 0)"
  all_pass=false
fi

$all_pass && { echo "PASS: pre-commit catalog refresh + never-block contract holds"; exit 0; }
exit 1

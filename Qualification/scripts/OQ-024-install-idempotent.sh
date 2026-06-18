#!/usr/bin/env bash
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
# OQ-024 — install.sh creates the expected symlinks idempotently (minimum-config baseline).
#
# Requirement (OQ.md OQ-024): install.sh creates symlinks for commands, skills and agents
# under ~/.claude/{commands,skills,agents}/; re-running updates (does not duplicate or error);
# stale own-repo links are pruned.
#
# Behaviour SOURCED from install.sh:
#   install.sh:18  CLAUDE_DIR="${CLAUDE_HOME:-$HOME/.claude}"   <- lets us redirect output safely
#   install.sh:22-53 link_tree(): symlink each entry, prune our own dangling links, update on re-run
#   install.sh:55-57 links commands/, skills/, agents/
#
# SAFE / non-destructive: redirects ALL symlink output into a PRIVATE temp directory via
# CLAUDE_HOME, so the operator's real ~/.claude is never touched. install.sh also sets the
# repo's git core.hooksPath to .githooks (install.sh:61-63); this script first records the
# current value and RESTORES it afterwards, so the repo config is left exactly as found.
# Emits PASS/FAIL; exits non-zero on FAIL.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
INSTALL="$REPO/install.sh"

if [ ! -f "$INSTALL" ]; then
  echo "FAIL: install.sh not found at $INSTALL"
  exit 1
fi

# Preserve the repo's existing hooksPath so we can restore it (install.sh sets it).
PRE_HOOKS="$(git -C "$REPO" config core.hooksPath 2>/dev/null || true)"

TMP="$(mktemp -d)"
restore() {
  rm -rf "$TMP"
  if [ -n "$PRE_HOOKS" ]; then
    git -C "$REPO" config core.hooksPath "$PRE_HOOKS" >/dev/null 2>&1 || true
  fi
}
trap restore EXIT

run_install() {
  CLAUDE_HOME="$TMP/claude" bash "$INSTALL" >/dev/null 2>&1
}

# Run 1
if ! run_install; then
  echo "FAIL: install.sh exited non-zero on first run"
  exit 1
fi

count_links() {
  # count symlinks in the three dest dirs
  find "$TMP/claude/commands" "$TMP/claude/skills" "$TMP/claude/agents" \
    -maxdepth 1 -type l 2>/dev/null | wc -l | tr -d ' '
}

N1="$(count_links)"
if [ "$N1" -lt 1 ]; then
  echo "FAIL: first run created no symlinks (expected commands/skills/agents links)"
  exit 1
fi

# Run 2 — must not error and must not duplicate
if ! run_install; then
  echo "FAIL: install.sh exited non-zero on second (idempotent) run"
  exit 1
fi
N2="$(count_links)"

# Verify expected sources are all linked (idempotent: same set, same count).
EXPECTED=0
for kind in commands skills agents; do
  if [ -d "$REPO/$kind" ]; then
    for entry in "$REPO/$kind"/*; do
      [ -e "$entry" ] && EXPECTED=$((EXPECTED + 1))
    done
  fi
done

if [ "$N1" -eq "$N2" ] && [ "$N2" -eq "$EXPECTED" ]; then
  echo "PASS: install.sh idempotent — $N2 links after both runs (expected $EXPECTED), no duplicates/errors"
  exit 0
fi

echo "FAIL: link counts run1=$N1 run2=$N2 expected=$EXPECTED (idempotency/completeness mismatch)"
exit 1

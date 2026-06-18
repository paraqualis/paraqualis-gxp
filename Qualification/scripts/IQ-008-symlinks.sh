#!/usr/bin/env bash
# IQ-008: Verify all install.sh symlinks exist in ~/.claude/ and resolve to this repo.
# Expected targets sourced from install.sh (commands/, skills/, agents/ directories).
# Read-only. Emits PASS or FAIL.
set -uo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
CLAUDE_DIR="${CLAUDE_HOME:-$HOME/.claude}"
echo "IQ-008  Symlink verification"
echo "  Repo:       $REPO_DIR"
echo "  Claude dir: $CLAUDE_DIR"

FAILURES=0
check_link() {
  local LINK="$1" EXPECTED_PREFIX="$2"
  if [ ! -L "$LINK" ]; then echo "  FAIL  not a symlink: $LINK"; FAILURES=$((FAILURES+1)); return; fi
  local TARGET; TARGET=$(readlink "$LINK")
  if [ ! -e "$LINK" ]; then echo "  FAIL  dangling: $LINK -> $TARGET"; FAILURES=$((FAILURES+1)); return; fi
  case "$TARGET" in
    "$EXPECTED_PREFIX"*) echo "  OK    $LINK -> $TARGET" ;;
    *) echo "  FAIL  target outside repo: $LINK -> $TARGET"; FAILURES=$((FAILURES+1)) ;;
  esac
}

for entry in "$REPO_DIR/commands"/*/; do check_link "$CLAUDE_DIR/commands/$(basename "$entry")" "$REPO_DIR/commands/"; done
for entry in "$REPO_DIR/skills"/*/;   do check_link "$CLAUDE_DIR/skills/$(basename "$entry")"   "$REPO_DIR/skills/";   done
for entry in "$REPO_DIR/agents"/*.md; do check_link "$CLAUDE_DIR/agents/$(basename "$entry")"   "$REPO_DIR/agents/";   done

[ $FAILURES -eq 0 ] && { echo "PASS  All symlinks present and resolving to this repo"; exit 0; }
echo "FAIL  $FAILURES symlink(s) missing, dangling, or pointing outside repo"
exit 1

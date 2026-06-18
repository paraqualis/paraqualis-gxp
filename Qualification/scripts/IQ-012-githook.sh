#!/usr/bin/env bash
# IQ-012: Verify the pre-commit git hook is executable and core.hooksPath = .githooks.
# Expected values sourced from install.sh logic.
# Read-only. Emits PASS or FAIL.
set -uo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
HOOK="$REPO_DIR/.githooks/pre-commit"
echo "IQ-012  Git hook configuration check"
echo "  Repo: $REPO_DIR"

FAILURES=0
if [ -x "$HOOK" ]; then echo "  OK    .githooks/pre-commit is executable"
else echo "  FAIL  .githooks/pre-commit not executable or not found"; FAILURES=$((FAILURES+1)); fi

HOOKS_PATH=$(git -C "$REPO_DIR" config core.hooksPath 2>/dev/null || echo "(not set)")
if [ "$HOOKS_PATH" = ".githooks" ]; then echo "  OK    core.hooksPath = .githooks"
else echo "  FAIL  core.hooksPath = '$HOOKS_PATH' (expected: .githooks)"; FAILURES=$((FAILURES+1)); fi

[ $FAILURES -eq 0 ] && { echo "PASS  Git hook configured correctly"; exit 0; }
echo "FAIL  $FAILURES git hook configuration issue(s)"
exit 1

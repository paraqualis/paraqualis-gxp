#!/usr/bin/env bash
# PQ-040 — The document-protection hook refuses edits to an approved (locked) file in use.
# Traces: URS-040. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): an approved/signed GxP record must not be silently
# overwritten. The hook is meant to BLOCK any edit to a file carrying the approved-record
# marker, while leaving an unmarked file editable. This test drives the real hook the way
# Claude Code does — feeding it the same JSON event on stdin — against (a) a locked temp file
# and (b) an unmarked temp file, and checks the hook BLOCKS the first (exit 2) and ALLOWS the
# second (exit 0). It uses throwaway temp files; it never touches repo files.
#
# The marker string and the exit-code contract are SOURCED from the hook:
#   hooks/protect-approved-documents.py:27 (LOCK_MARKER) and :51-60 (exit 2 block / 0 allow).
# PASS/FAIL. Exit 0 = PASS, 1 = FAIL.
set -uo pipefail
REPO="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
HOOK="$REPO/hooks/protect-approved-documents.py"
MARKER='<!-- PARAQUALIS-LOCK: approved -->'

echo "PQ-040 approved-document lock hook"
echo "------------------------------------------------------------"
[ -f "$HOOK" ] || { echo "FAIL  hook not found at $HOOK"; exit 1; }

tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
locked="$tmpdir/locked.md"
unlocked="$tmpdir/draft.md"
printf '# Approved record\n%s\nbody\n' "$MARKER" > "$locked"
printf '# Draft record\nno marker here\nbody\n' > "$unlocked"

fail=0

# 1. Editing a LOCKED file must be blocked (exit 2).
event_locked=$(printf '{"tool_input":{"file_path":"%s"}}' "$locked")
set +e
echo "$event_locked" | python3 "$HOOK" >/dev/null 2>"$tmpdir/err_locked"
rc_locked=$?
set -e
if [ "$rc_locked" -eq 2 ]; then
  echo "PASS  edit to locked file BLOCKED (exit 2)"
  if grep -qi 'approved' "$tmpdir/err_locked"; then
    echo "PASS  block message explains it is an approved record"
  else
    echo "WARN  block message did not mention 'approved'"
  fi
else
  echo "FAIL  edit to locked file was NOT blocked (exit $rc_locked)"
  fail=1
fi

# 2. Editing an UNMARKED file must be allowed (exit 0).
event_unlocked=$(printf '{"tool_input":{"file_path":"%s"}}' "$unlocked")
set +e
echo "$event_unlocked" | python3 "$HOOK" >/dev/null 2>&1
rc_unlocked=$?
set -e
if [ "$rc_unlocked" -eq 0 ]; then
  echo "PASS  edit to unmarked file ALLOWED (exit 0)"
else
  echo "FAIL  edit to unmarked file was wrongly blocked (exit $rc_unlocked)"
  fail=1
fi

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS — locked records refused, unmarked records editable."
  exit 0
fi
echo "RESULT: FAIL — the approval-integrity control did not behave as specified."
exit 1

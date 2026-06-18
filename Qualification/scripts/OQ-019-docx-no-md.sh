#!/usr/bin/env bash
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
# OQ-019 — build_docx.py exits with a clear message when no docs/*.md are found.
#
# Requirement (OQ.md OQ-019): run as a script with an empty docs/ directory, build_docx.py
# shall call sys.exit("no docs/*.md found") — a clear, non-silent failure.
#
# Behaviour SOURCED from qualification-pack-template/build_docx.py:176-178:
#     mds = sorted(DOCS.glob("*.md"))
#     if not mds:
#         sys.exit("no docs/*.md found")
# DOCS is build_docx.py:31 -> Path(__file__).parent / "docs".
#
# Read-only / safe: COPIES build_docx.py into a private temp dir with an EMPTY docs/ subdir
# and runs that copy. The real repo is never touched. Requires python-docx (build_docx
# imports it at module load); if absent this FAILS LOUD rather than skipping.
# Emits PASS/FAIL; exits non-zero on FAIL.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$REPO/qualification-pack-template/build_docx.py"

if [ ! -f "$SRC" ]; then
  echo "FAIL: build_docx.py not found at $SRC"
  exit 1
fi

if ! python3 -c "import docx" 2>/dev/null; then
  echo "FAIL: python-docx not installed; cannot import build_docx to exercise OQ-019. Run: pip install python-docx"
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cp "$SRC" "$TMP/build_docx.py"
mkdir -p "$TMP/docs"   # empty docs dir -> no *.md present

set +e
OUT="$(cd "$TMP" && python3 build_docx.py 2>&1)"
CODE=$?
set -e

if [ "$CODE" -ne 0 ] && printf '%s' "$OUT" | grep -qF "no docs/*.md found"; then
  echo "PASS: empty docs/ -> non-zero exit ($CODE) with message 'no docs/*.md found'"
  exit 0
fi

echo "FAIL: expected non-zero exit and 'no docs/*.md found' message"
echo "  exit=$CODE output=$OUT"
exit 1

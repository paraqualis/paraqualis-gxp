#!/usr/bin/env bash
# IQ-004: Report the python3 runtime version and compare to the declared minimum.
# Expected minimum sourced from a manifest when one exists. If no minimum is
# declared, reports ACTUAL only — a gap for human review (GIQ-003).
# Read-only.
set -euo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
echo "IQ-004  Python runtime version check"

ACTUAL=$(python3 --version 2>&1)
echo "  Actual python3 version: $ACTUAL"

MIN_VER=""
if [ -f "$REPO_DIR/pyproject.toml" ]; then
  MIN_VER=$(grep -oE 'requires-python\s*=\s*"[>=~^ ]*[0-9]+\.[0-9]+' "$REPO_DIR/pyproject.toml" 2>/dev/null \
            | grep -oE '[0-9]+\.[0-9]+' | head -1 || true)
fi

# Fall back to a declared minimum in requirements.txt ("Requires Python >= X.Y")
if [ -z "$MIN_VER" ] && [ -f "$REPO_DIR/requirements.txt" ]; then
  MIN_VER=$(grep -oE "Requires Python >= ?[0-9]+\.[0-9]+" "$REPO_DIR/requirements.txt" 2>/dev/null | grep -oE "[0-9]+\.[0-9]+" | head -1 || true)
fi

if [ -z "$MIN_VER" ]; then
  echo "  WARNING: No declared minimum Python version found in any manifest."
  echo "  Establishing and approving a minimum is required — see GIQ-003."
  echo "NEEDS-HUMAN-REVIEW  Python minimum not declared — cannot assert PASS/FAIL"
  exit 0
fi

echo "  Declared minimum (from manifest): $MIN_VER"
python3 - "$MIN_VER" "$ACTUAL" <<'PY'
import sys
def parse(s): return tuple(int(x) for x in s.split(".")[:3])
min_v = parse(sys.argv[1]); actual = parse(sys.argv[2].split()[-1])
if actual >= min_v: print(f"PASS  python3 {actual} >= declared minimum {min_v}")
else: print(f"FAIL  python3 {actual} < declared minimum {min_v}"); sys.exit(1)
PY

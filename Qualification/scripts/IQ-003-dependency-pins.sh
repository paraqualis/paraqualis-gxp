#!/usr/bin/env bash
# IQ-003: Verify that a Python dependency manifest with pinned versions exists.
# A missing manifest or unpinned (floor/range) versions = FAIL.
# Read-only. Emits PASS or FAIL.
set -euo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
echo "IQ-003  Python dependency pinning check"

MANIFESTS=()
for f in requirements.txt pyproject.toml poetry.lock Pipfile setup.cfg; do
  [ -f "$REPO_DIR/$f" ] && MANIFESTS+=("$REPO_DIR/$f")
done

if [ ${#MANIFESTS[@]} -eq 0 ]; then
  echo "  No dependency manifest found (requirements.txt / pyproject.toml / poetry.lock / Pipfile / setup.cfg)"
  echo "FAIL  No Python dependency manifest — install is non-reproducible"
  exit 1
fi
echo "  Found manifests: ${MANIFESTS[*]}"

python3 - "${MANIFESTS[@]}" <<'PY'
import sys, re
content = ""
for f in sys.argv[1:]:
    with open(f) as fh: content += fh.read() + "\n"

required = ["mcp", "python-docx", "openpyxl"]
failures = []
for pkg in required:
    pinned = re.search(rf"(?i){re.escape(pkg)}\s*==\s*\d", content)
    present = re.search(rf"(?i){re.escape(pkg)}", content)
    if not present: failures.append(f"  MISSING from manifest: {pkg}")
    elif not pinned: failures.append(f"  UNPINNED (no '==' spec): {pkg}")
    else: print(f"  PINNED OK: {pkg}")

if failures:
    for f in failures: print(f)
    print("FAIL  One or more dependencies missing or not pinned to an exact version"); sys.exit(1)
print("PASS  All required Python dependencies are pinned in the manifest")
PY

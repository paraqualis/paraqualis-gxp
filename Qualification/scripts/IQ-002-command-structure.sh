#!/usr/bin/env bash
# IQ-002: Verify all slash-command .md files exist with valid YAML frontmatter
#          and a non-empty description field.
# Expected count (18) sourced from CHANGELOG.md declaration where present.
# Read-only. Emits PASS or FAIL.
set -euo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
CMD_DIR="$REPO_DIR/commands"

echo "IQ-002  Slash-command structure check"
echo "  Commands dir: $CMD_DIR"

DECLARED_COUNT=$(grep -oE 'Slash-command count is now \*\*[0-9]+\*\*' "$REPO_DIR/CHANGELOG.md" 2>/dev/null \
  | grep -oE '[0-9]+' | tail -1 || true)
[ -z "$DECLARED_COUNT" ] && DECLARED_COUNT="(not found in CHANGELOG)"
echo "  Declared command count (from CHANGELOG.md): $DECLARED_COUNT"

python3 - "$CMD_DIR" "$DECLARED_COUNT" <<'PY'
import sys, re
from pathlib import Path

cmd_dir = Path(sys.argv[1]); declared = sys.argv[2]
mds = sorted(cmd_dir.rglob("*.md"))
print(f"  Found {len(mds)} .md files")

failures = []
for md in mds:
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        failures.append(f"  NO FRONTMATTER: {md.relative_to(cmd_dir)}"); continue
    if not re.search(r"^\s*description:\s*\S", text, re.MULTILINE):
        failures.append(f"  MISSING description: {md.relative_to(cmd_dir)}")
    else:
        print(f"  OK: {md.relative_to(cmd_dir)}")

if failures:
    for f in failures: print(f)
    print(f"FAIL  {len(failures)} file(s) have missing/invalid frontmatter"); sys.exit(1)

if declared.isdigit() and int(declared) != len(mds):
    print(f"FAIL  Count mismatch: CHANGELOG declares {declared}, found {len(mds)}"); sys.exit(1)

print(f"PASS  All {len(mds)} command files present with valid frontmatter and description")
PY

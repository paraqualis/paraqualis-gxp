#!/usr/bin/env bash
# IQ-001: Verify plugin.json is valid JSON and declares required fields.
# Expected values sourced from .claude-plugin/plugin.json (the declared spec).
# Read-only. Emits PASS or FAIL with evidence.
set -euo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
MANIFEST="$REPO_DIR/.claude-plugin/plugin.json"

echo "IQ-001  Plugin manifest check"
echo "  Manifest: $MANIFEST"

if [ ! -f "$MANIFEST" ]; then
  echo "FAIL  plugin.json not found at $MANIFEST"
  exit 1
fi

python3 - "$MANIFEST" <<'PY'
import json, sys

path = sys.argv[1]
try:
    with open(path) as f:
        p = json.load(f)
except json.JSONDecodeError as e:
    print(f"FAIL  plugin.json is not valid JSON: {e}")
    sys.exit(1)

required = ["name", "version", "description", "author"]
failures = []
for k in required:
    val = p.get(k)
    if not val:
        failures.append(f"  MISSING or empty: {k}")
    else:
        print(f"  {k}: {str(val)[:80]}")

if failures:
    for f in failures:
        print(f)
    print("FAIL  One or more required fields missing from plugin.json")
    sys.exit(1)

print(f"\nDECLARED version (from manifest): {p['version']}")
print("PASS  plugin.json is valid JSON with all required fields")
PY

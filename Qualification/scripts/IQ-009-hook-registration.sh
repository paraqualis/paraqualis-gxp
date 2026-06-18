#!/usr/bin/env bash
# IQ-009: Verify protect-approved-documents.py is registered as a PreToolUse hook
#          in ~/.claude/settings.json (or a project-scoped settings.json).
# Read-only. Emits PASS or FAIL.
set -uo pipefail

SETTINGS="${CLAUDE_HOME:-$HOME/.claude}/settings.json"
echo "IQ-009  Document-protection hook registration check"
echo "  Settings file: $SETTINGS"

if [ ! -f "$SETTINGS" ]; then
  echo "FAIL  settings.json not found at $SETTINGS"; exit 1
fi

python3 - "$SETTINGS" <<'PY'
import json, sys
with open(sys.argv[1]) as f: s = json.load(f)
pre = s.get("hooks", {}).get("PreToolUse", [])
print(f"  PreToolUse entries found: {len(pre)}")
found = any("protect-approved-documents" in h.get("command", "")
           for entry in pre for h in entry.get("hooks", []))
if found:
    print("PASS  protect-approved-documents.py is registered as a PreToolUse hook")
else:
    print("FAIL  protect-approved-documents.py is NOT registered in PreToolUse hooks")
    print("  Remediation: add the PreToolUse entry from hooks/README.md to settings.json")
    sys.exit(1)
PY

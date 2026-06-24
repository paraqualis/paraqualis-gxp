#!/usr/bin/env python3
# PQ-031 — Server processes log material actions/failures server-side (not just the transcript).
# Traces: URS-031. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): when the toolkit runs as a long-lived process — the openFDA
# MCP server and the document-protection hook — material actions and failures should be
# observable in a server-side LOG, so an auditor can review what the process did independently
# of any one user's chat transcript. This test inspects both process modules for a logging
# facility (Python `logging`, a logger, or writes to a log file/syslog).
#
# Outcome expectation (honest): as-built, neither process emits a server-side log; the hook
# writes only to stderr (shown to Claude) and the MCP server returns errors in-band. So this
# test is expected to record a controlled FAIL feeding gap GPQ-003 — it is NOT skipped.
#
# What "logging present" means is SOURCED from the URS acceptance criterion (URS-031) and the
# protocol focus area (xq-qualification-protocol.md:130-135).
#
# Usage: python3 PQ-031-server-process-logging.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TARGETS = {
    "openFDA MCP server": os.path.join(REPO, "mcp-servers", "openfda", "server.py"),
    "document-protection hook": os.path.join(REPO, "hooks", "protect-approved-documents.py"),
}

print("PQ-031 server-side logging of material actions")
print("-" * 60)

# Markers of a genuine server-side log facility (NOT stderr-to-transcript, NOT in-band return).
LOG_FACILITY = re.compile(
    r"(import\s+logging|logging\.(getLogger|basicConfig|info|warning|error)"
    r"|getLogger\(|syslog|open\([^)]*\.log|RotatingFileHandler|logger\.)"
)

fail = 0
for name, path in TARGETS.items():
    if not os.path.exists(path):
        print(f"FAIL  {name}: module not found at {path}")
        fail = 1
        continue
    with open(path, encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    if LOG_FACILITY.search(text):
        print(f"PASS  {name}: server-side log facility present")
    else:
        # stderr-only is explicitly NOT a server-side audit log.
        note = "stderr-only (shown to Claude, not a server log)" if "sys.stderr" in text else "no log output"
        print(f"FAIL  {name}: no server-side log facility — {note}")
        fail = 1

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — server processes log material actions server-side.")
    sys.exit(0)
print("RESULT: FAIL — server-side logging is absent (feeds gap GPQ-003). NOT a skip — a real,")
print("        recorded FAIL: the control is unmet as-built.")
sys.exit(1)

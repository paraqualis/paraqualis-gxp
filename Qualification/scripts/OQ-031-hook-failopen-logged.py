#!/usr/bin/env python3
"""OQ-031 — Fail-open paths must emit a log entry (GIQ-007 remediation).

The hook is invoked exactly as Claude Code invokes it — as a subprocess fed the event
on stdin — and its stderr is captured. A malformed event must (a) be ALLOWED (exit 0,
fail-open, so the session is never wedged) AND (b) leave a log line on stderr, so a
fail-open decision is auditable rather than silent. Read-only / safe.
"""
import os
import subprocess
import sys

HOOK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                    "hooks", "protect-approved-documents.py"))

p = subprocess.run([sys.executable, HOOK], input="{not valid json}",
                   capture_output=True, text=True)
allowed = (p.returncode == 0)
logged = bool(p.stderr.strip())
print(f"exit={p.returncode}  stderr={p.stderr.strip()[:140]!r}")

if allowed and logged:
    print("PASS: fail-open path allowed the call AND logged the decision to stderr")
    sys.exit(0)
if allowed and not logged:
    print("FAIL: fail-open path is silent — no log emitted")
    sys.exit(1)
print(f"FAIL: unexpected exit code {p.returncode} (expected 0 = fail-open allow)")
sys.exit(1)

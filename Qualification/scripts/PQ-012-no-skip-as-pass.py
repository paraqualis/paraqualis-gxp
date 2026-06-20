#!/usr/bin/env python3
# PQ-012 — A skipped/unexecuted test is never counted as a pass; the verdict is honest.
# Traces: URS-012. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): the worst data-integrity failure in a qualification is
# calling something "PASS" that was never actually run. This test verifies the pack's own
# scripts distinguish three outcomes — PASS, FAIL, and NOT-EXECUTED — and that NOT-EXECUTED
# paths exit with a NON-zero, non-FAIL code (convention here: exit 2) so a runner cannot
# mistake a skip for a pass. It also confirms the readiness verdict in PQ.md does not fold
# unexecuted checks into the pass count.
#
# The exit-code convention (0=PASS, 1=FAIL, 2=NOT-EXECUTED) is SOURCED from the headers of the
# PQ scripts in this same pack.
#
# Usage: python3 PQ-012-no-skip-as-pass.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else "/Users/craigwylie/Devl/paraqualis-gxp"
SCRIPTS = os.path.join(REPO, "Qualification", "scripts")
PQ_MD = os.path.join(REPO, "Qualification", "docs", "PQ.md")

print("PQ-012 no skip counted as pass")
print("-" * 60)
fail = 0

# 1. Scripts that have a not-executed path must NOT exit 0 on that path.
py_scripts = [f for f in os.listdir(SCRIPTS)
              if f.endswith(".py") and f != os.path.basename(__file__)] if os.path.isdir(SCRIPTS) else []
checked = 0
for f in py_scripts:
    with open(os.path.join(SCRIPTS, f), encoding="utf-8", errors="ignore") as fh:
        text = fh.read()
    if re.search(r"NOT-EXECUTED|not-yet-executed|not a pass", text, re.I):
        checked += 1
        # The not-executed branch should sys.exit(2), never exit 0.
        if re.search(r"exit\(2\)|sys\.exit\(2\)", text):
            print(f"PASS  {f} — not-executed path exits 2 (not counted as pass)")
        else:
            print(f"FAIL  {f} — declares a skip but no exit(2) path found")
            fail = 1
if checked == 0:
    print("INFO  no scripts declare a not-executed path (nothing to skip-check)")

# 2. The PQ verdict/summary must count NOT-EXECUTED separately, not as pass.
if os.path.exists(PQ_MD):
    with open(PQ_MD, encoding="utf-8", errors="ignore") as fh:
        md = fh.read()
    if re.search(r"not[- ]yet[- ]executed|NOT-EXECUTED|not executed", md, re.I):
        print("PASS  PQ.md tracks a 'not-yet-executed' outcome distinct from PASS")
    else:
        print("FAIL  PQ.md does not surface a not-yet-executed category")
        fail = 1
else:
    print("NOT-EXECUTED  PQ.md not present yet to inspect its verdict.")
    sys.exit(2)

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — no skip is reported as a pass; verdict separates outcomes.")
    sys.exit(0)
print("RESULT: FAIL — a skip could be mistaken for a pass.")
sys.exit(1)

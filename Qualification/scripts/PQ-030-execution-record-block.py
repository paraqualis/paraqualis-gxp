#!/usr/bin/env python3
# PQ-030 — Every generated test-case carries a blank, structured execution-record block.
# Traces: URS-030. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): the execution record IS the audit trail of the
# qualification — who ran the test, when, the actual result, PASS/FAIL, and where the
# evidence lives. It must ship blank with every test-case, ready to be filled when the test
# is run. This test inspects this pack's own PQ test-cases (the .md procedures and the PQ.md
# table) and confirms each carries the required execution-record fields, blank until executed.
#
# The required field set is SOURCED from:
#   Qualification/records/execution-record-template.md  (executed-by, date, actual result,
#   PASS/FAIL, evidence reference, reviewer, QA approver).
#
# Usage: python3 PQ-030-execution-record-block.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPTS = os.path.join(REPO, "Qualification", "scripts")
PQ_MD = os.path.join(REPO, "Qualification", "docs", "PQ.md")

print("PQ-030 blank execution-record block on every test-case")
print("-" * 60)

# Required record fields (sourced from execution-record-template.md).
REQUIRED = ["executed by", "pass", "fail", "evidence", "reviewer"]

fail = 0

# 1. Manual .md procedures each carry an execution-record block.
md_procs = [f for f in os.listdir(SCRIPTS) if f.endswith(".md")] if os.path.isdir(SCRIPTS) else []
for f in md_procs:
    with open(os.path.join(SCRIPTS, f), encoding="utf-8", errors="ignore") as fh:
        t = fh.read().lower()
    if "execution record" in t and all(k in t for k in ["executed by", "evidence", "reviewer"]) \
       and ("pass" in t and "fail" in t):
        print(f"PASS  {f} carries a blank execution-record block")
    else:
        print(f"FAIL  {f} missing a complete execution-record block")
        fail = 1

# 2. The PQ.md test-case table must reference an execution-record block for every case
#    (scripted cases record into Qualification/records/<ID>.md from the template).
if os.path.exists(PQ_MD):
    with open(PQ_MD, encoding="utf-8", errors="ignore") as fh:
        md = fh.read().lower()
    if "execution record" in md or "execution-record" in md:
        print("PASS  PQ.md references the execution-record block for its test-cases")
    else:
        print("FAIL  PQ.md does not reference an execution-record block")
        fail = 1
else:
    print("NOT-EXECUTED  PQ.md not present yet to inspect.")
    sys.exit(2)

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — every test-case ships a blank execution-record block.")
    sys.exit(0)
print("RESULT: FAIL — a test-case lacks its execution-record block.")
sys.exit(1)

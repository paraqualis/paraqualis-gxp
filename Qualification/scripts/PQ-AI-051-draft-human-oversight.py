#!/usr/bin/env python3
# PQ-AI-051 — AI output is issued DRAFT and names the required human reviewer roles
#             (human-in-the-loop oversight). Traces: URS-AI-051.
# ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): AI-generated GxP evidence must never be used as-is. The
# control is human oversight: every artifact is stamped DRAFT requiring human review and names
# WHO must review/approve before it can be relied on. This test confirms the pack documents are
# DRAFT-stamped and explicitly name the reviewer/approver roles, and that the pack states AI
# output requires human review before use as formal evidence.
#
# The DRAFT requirement and reviewer roles are SOURCED from the protocol governance
#   (xq-qualification-protocol.md:277) and URS-AI-051 (URS.md:83).
#
# Usage: python3 PQ-AI-051-draft-human-oversight.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else "/Users/craigwylie/Devl/paraqualis-skills"
PQ_MD = os.path.join(REPO, "Qualification", "docs", "PQ.md")

print("PQ-AI-051 DRAFT + named human oversight roles")
print("-" * 60)

if not os.path.exists(PQ_MD):
    print("NOT-EXECUTED  PQ.md not present yet to inspect.")
    sys.exit(2)

with open(PQ_MD, encoding="utf-8", errors="ignore") as fh:
    t = fh.read()
tl = t.lower()
fail = 0

if re.search(r"DRAFT\s*[—-].*pending review and approval", t, re.I):
    print("PASS  PQ.md carries the DRAFT governance stamp")
else:
    print("FAIL  PQ.md missing the DRAFT governance stamp")
    fail = 1

for role in ("reviewer", "qa approver"):
    if role in tl:
        print(f"PASS  names required human role: {role}")
    else:
        print(f"FAIL  does not name required human role: {role}")
        fail = 1

if re.search(r"human review|human-in-the-loop|review.* before .*evidence|qualified.*personnel", tl):
    print("PASS  states AI output requires human review before use as formal evidence")
else:
    print("FAIL  does not state the human-review-before-reliance requirement")
    fail = 1

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — AI output is DRAFT with named human oversight.")
    sys.exit(0)
print("RESULT: FAIL — human-oversight stamping/roles incomplete.")
sys.exit(1)

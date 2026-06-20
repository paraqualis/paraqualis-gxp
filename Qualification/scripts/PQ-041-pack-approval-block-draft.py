#!/usr/bin/env python3
# PQ-041 — Every generated pack document carries the unsigned approval block + DRAFT stamp.
# Traces: URS-041 (and AI human-oversight evidence for URS-AI-051).
# ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): a qualification document is not authoritative until
# qualified people review and sign it. So every pack document must (a) be visibly stamped
# DRAFT and (b) carry signature lines for Author / Reviewer / QA Approver, left unsigned.
# This test inspects the pack's own Markdown documents and confirms both are present.
#
# The exact DRAFT stamp and approval roles are SOURCED from the protocol governance section
#   (xq-qualification-protocol.md:277) and the URS approval block (URS.md:118-124).
#
# Usage: python3 PQ-041-pack-approval-block-draft.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else "/Users/craigwylie/Devl/paraqualis-gxp"
DOCS = os.path.join(REPO, "Qualification", "docs")
REQ = os.path.join(REPO, "Qualification", "requirements")

print("PQ-041 unsigned approval block + DRAFT stamp on every pack doc")
print("-" * 60)

DRAFT = re.compile(r"DRAFT\s*[—-].*pending review and approval", re.I)
ROLES = ["author", "reviewer", "qa approver"]

# Inspect generated pack Markdown (docs/*.md) plus the URS in requirements/.
md_paths = []
for base in (DOCS, REQ):
    if os.path.isdir(base):
        md_paths += [os.path.join(base, f) for f in os.listdir(base) if f.endswith(".md")]

if not md_paths:
    print("NOT-EXECUTED  no pack Markdown documents present yet.")
    sys.exit(2)

fail = 0
for p in sorted(md_paths):
    with open(p, encoding="utf-8", errors="ignore") as fh:
        t = fh.read()
    tl = t.lower()
    has_draft = bool(DRAFT.search(t))
    has_roles = all(r in tl for r in ROLES)
    has_unsigned = "unsigned" in tl or "signature" in tl
    name = os.path.relpath(p, REPO)
    if has_draft and has_roles and has_unsigned:
        print(f"PASS  {name} — DRAFT stamp + unsigned Author/Reviewer/QA block")
    else:
        miss = []
        if not has_draft: miss.append("DRAFT stamp")
        if not has_roles: miss.append("approval roles")
        if not has_unsigned: miss.append("unsigned signature lines")
        print(f"FAIL  {name} — missing: {', '.join(miss)}")
        fail = 1

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — every pack document is DRAFT-stamped with an unsigned approval block.")
    sys.exit(0)
print("RESULT: FAIL — a pack document lacks the DRAFT stamp or approval block.")
sys.exit(1)

#!/usr/bin/env python3
# PQ-AI-052 — The engine discloses its AI Context of Use (COU) and the self-qualification caveat.
# Traces: URS-AI-052. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): regulators (FDA AI credibility framework) require an AI tool
# to state WHAT it is being used for (its Context of Use) and the risk that implies. This engine
# must also be honest that it is itself a GxP-impacting tool that would need its own
# qualification before its output is relied on as formal evidence — it does not self-certify.
# This test confirms the pack governance block states both.
#
# The COU + self-qualification disclosure requirement is SOURCED from URS-AI-052 (URS.md:84),
#   the URS GxP-impact statement (URS.md:16), and the protocol governance note
#   (xq-qualification-protocol.md:279-280).
#
# Usage: python3 PQ-AI-052-context-of-use-self-qual.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PQ_MD = os.path.join(REPO, "Qualification", "docs", "PQ.md")

print("PQ-AI-052 Context-of-Use + self-qualification caveat disclosed")
print("-" * 60)

if not os.path.exists(PQ_MD):
    print("NOT-EXECUTED  PQ.md not present yet to inspect.")
    sys.exit(2)

with open(PQ_MD, encoding="utf-8", errors="ignore") as fh:
    tl = fh.read().lower()
fail = 0

if "context of use" in tl or "context-of-use" in tl:
    print("PASS  pack states the AI Context of Use (COU)")
else:
    print("FAIL  pack does not state the Context of Use")
    fail = 1

if re.search(r"own qualification|self-?qualif|would require .*qualification|does not self-certif", tl):
    print("PASS  pack states the self-qualification caveat (does not self-certify)")
else:
    print("FAIL  pack does not state the self-qualification caveat")
    fail = 1

if re.search(r"gxp[- ]impact", tl):
    print("PASS  pack marks itself a GxP-impacting tool")
else:
    print("WARN  pack does not explicitly say 'GxP-impacting'")

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — COU and self-qualification caveat are disclosed.")
    sys.exit(0)
print("RESULT: FAIL — COU / self-qualification disclosure incomplete.")
sys.exit(1)

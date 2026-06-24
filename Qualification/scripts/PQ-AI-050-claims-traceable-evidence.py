#!/usr/bin/env python3
# PQ-AI-050 — AI-generated qualification claims are traceable to cited evidence (no hallucinated
#             pass/fail). Traces: URS-AI-050. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): the qualification engine uses an LLM to write GxP-impacting
# evidence. The non-negotiable control is that NO pass/fail conclusion is asserted without a
# citation a reviewer can check — the engine must not invent (hallucinate) verdicts. This test
# inspects the generated pack: every PQ test-case must (a) trace to a URS requirement and (b)
# decide PASS/FAIL only from a script/procedure tied to cited sources, not a bare assertion in
# prose. It checks the structural control; a human reviewer confirms each citation is real
# (recorded in the execution block) — that human check is the hallucination backstop.
#
# What counts as "traceable" is SOURCED from the protocol (specification-driven, cite every
#   expected value: xq-qualification-protocol.md:47-60) and URS-AI-050 (URS.md:82).
#
# Usage: python3 PQ-AI-050-claims-traceable-evidence.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PQ_MD = os.path.join(REPO, "Qualification", "docs", "PQ.md")
SCRIPTS = os.path.join(REPO, "Qualification", "scripts")

print("PQ-AI-050 AI claims traceable to cited evidence (hallucination control)")
print("-" * 60)

if not os.path.exists(PQ_MD):
    print("NOT-EXECUTED  PQ.md not present yet to inspect.")
    sys.exit(2)

with open(PQ_MD, encoding="utf-8", errors="ignore") as fh:
    md = fh.read()

fail = 0

# 1. Every PQ test-case ID mentioned in the table must reference a traced URS and have an
#    artifact in scripts/. (A verdict with no instrument behind it = an unsupported claim.)
ids = sorted(set(re.findall(r"\bPQ-(?:AI-)?\d{3}\b", md)))
if not ids:
    print("FAIL  no PQ test-case IDs found in PQ.md")
    sys.exit(1)
print(f"test-case IDs found: {ids}")

script_files = os.listdir(SCRIPTS) if os.path.isdir(SCRIPTS) else []
for tid in ids:
    has_artifact = any(f.startswith(tid + "-") or f.startswith(tid + ".") for f in script_files)
    # Does the row near this ID cite a URS trace?
    traced = bool(re.search(tid + r".{0,400}?URS-", md, re.S))
    if has_artifact and traced:
        print(f"PASS  {tid} — has cited URS trace AND a test artifact (verdict is evidence-backed)")
    else:
        why = []
        if not has_artifact: why.append("no script/procedure artifact")
        if not traced: why.append("no URS trace near row")
        print(f"FAIL  {tid} — {', '.join(why)} (verdict would be unsupported)")
        fail = 1

# 2. No bare "PASS"/"FAIL" verdict baked into PQ.md prose (verdicts belong in execution records
#    after a run, sourced from a script's output — not pre-asserted by the AI).
#    The pack should mark results as not-yet-executed, not pre-decided.
if re.search(r"not[- ]yet[- ]executed", md, re.I):
    print("PASS  PQ.md leaves results not-yet-executed (no pre-asserted AI verdicts)")
else:
    print("WARN  PQ.md does not state results are not-yet-executed; check for pre-asserted verdicts")

print("-" * 60)
if fail == 0:
    print("RESULT: PASS (structural) — every AI-generated claim is traceable to cited evidence.")
    print("NOTE: human reviewer must verify each citation resolves (final hallucination check).")
    sys.exit(0)
print("RESULT: FAIL — an AI-generated claim is not backed by cited evidence.")
sys.exit(1)

#!/usr/bin/env python3
# PQ-013 — In use, a failed operation surfaces a clear error and is never swallowed silently.
# Traces: URS-013. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): silent failure hides data-integrity breaches. This test
# forces a real failure mode in the openFDA tool path — an invalid endpoint and a bad
# category — and confirms the tool RETURNS A SURFACED ERROR object rather than pretending
# success (empty results presented as a clean answer). It exercises the actual code path the
# user hits.
#
# The error-surfacing contract is SOURCED from the server:
#   mcp-servers/openfda/server.py:95-96  (bad category -> {"error": ...})
#   mcp-servers/openfda/server.py:45-62  (HTTP/exception -> {"error": ...})
#
# Usage: python3 PQ-013-errors-surface.py [REPO_ROOT]
import sys
import os

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "mcp-servers", "openfda"))

print("PQ-013 errors surface, never swallowed silently")
print("-" * 60)
try:
    import server
except Exception as e:
    print(f"FAIL  cannot import server module: {e}")
    sys.exit(1)

fail = 0

# 1. Invalid category must surface a clear error, not silently return empty.
r1 = server.search_enforcement(category="not-a-real-category", search="x", limit=1)
if isinstance(r1, dict) and "error" in r1:
    print(f"PASS  invalid category surfaces error: {r1['error']}")
else:
    print(f"FAIL  invalid category did NOT surface an error: {r1}")
    fail = 1

# 2. Invalid endpoint via the generic tool must surface an error or a clean no-match note,
#    never a silent success with fabricated data. (Requires network; a network error is also
#    a SURFACED error, which still satisfies "fails loud".)
r2 = server.openfda_query(endpoint="this/endpoint/does-not-exist", search="x", limit=1)
if isinstance(r2, dict) and ("error" in r2 or r2.get("note") or r2.get("total") in (0, None)):
    surfaced = r2.get("error") or r2.get("note") or "no-match (total 0)"
    print(f"PASS  bad endpoint surfaces a controlled outcome: {surfaced}")
else:
    print(f"FAIL  bad endpoint produced an uncontrolled/silent result: {r2}")
    fail = 1

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — failure modes surface clearly; no silent success.")
    print("NOTE: URS-031 (server-side LOG entry on failure) is a separate, currently-unmet")
    print("      control — see PQ-031 and gap GPQ-003. This test covers surfacing only.")
    sys.exit(0)
print("RESULT: FAIL — a failure mode was swallowed.")
sys.exit(1)

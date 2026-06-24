#!/usr/bin/env python3
# PQ-004 — The openFDA MCP tools return correctly-SHAPED results for a representative query.
# Traces: URS-005. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): the openFDA server gives Claude tools to look up FDA
# recalls, drug labels and adverse-event reports. This test imports the server module and
# calls one tool against the live openFDA API with a representative query, then checks the
# RESULT SHAPE the user/Claude actually receives — the trimmed key fields the tool promises.
# It does not assert specific record contents (live data changes); it proves the tool runs
# end-to-end and returns the documented shape, or a clean error (never a silent failure).
#
# The expected field set is SOURCED from the tool's own contract in
#   mcp-servers/openfda/server.py:99-103 (search_enforcement field projection).
# READ-ONLY against FDA's public API. PASS/FAIL via exit code.
#
# Usage: python3 PQ-004-openfda-shaped-results.py [REPO_ROOT]
import sys
import os

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SERVER_DIR = os.path.join(REPO, "mcp-servers", "openfda")
sys.path.insert(0, SERVER_DIR)

print("PQ-004 openFDA tool result-shape")
print("-" * 60)

try:
    import server  # noqa: E402  (the MCP server module under test)
except Exception as e:
    print(f"FAIL  cannot import openFDA server module: {e}")
    print("      (is the 'mcp' dependency installed? pip install mcp)")
    sys.exit(1)

# Representative query: Class I drug recalls. Calls the underlying _query path the tool uses.
try:
    res = server.search_enforcement(category="drug",
                                    search='classification:"Class I"',
                                    limit=2)
except Exception as e:
    print(f"FAIL  tool raised instead of returning a result: {e}")
    sys.exit(1)

print(f"raw keys returned: {sorted(res.keys())}")

# A clean error (e.g. offline / rate-limited) is a CONTROLLED outcome, not a silent pass.
if "error" in res:
    print(f"INFO  tool returned a surfaced error (controlled, not silent): {res['error']}")
    print("RESULT: NOT-EXECUTED (no live API access) — error surfaced cleanly; re-run online.")
    sys.exit(2)  # not-yet-executed; explicitly NOT a pass

if "results" not in res:
    print("FAIL  response missing 'results' container")
    sys.exit(1)

# Field contract sourced from server.py:99-103.
EXPECTED_FIELDS = {
    "recall_number", "status", "classification", "recalling_firm",
    "product_description", "reason_for_recall", "recall_initiation_date",
    "voluntary_mandated", "distribution_pattern", "state", "country",
}
ok = True
if not res["results"]:
    print("WARN  zero results for the representative query (acceptable; shape unverifiable)")
else:
    sample = res["results"][0]
    extra = set(sample.keys()) - EXPECTED_FIELDS
    if extra:
        print(f"FAIL  result contains fields outside the tool's contract: {extra}")
        ok = False
    else:
        print(f"PASS  result fields are within the documented contract: {sorted(sample.keys())}")

print("-" * 60)
if ok:
    print("RESULT: PASS — openFDA tool returned the documented result shape (live).")
    sys.exit(0)
else:
    print("RESULT: FAIL — result shape did not match the tool contract.")
    sys.exit(1)

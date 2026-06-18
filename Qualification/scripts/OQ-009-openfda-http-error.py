#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-009 — openFDA 5xx / unexpected HTTP error is surfaced, not swallowed.

Requirement (OQ.md OQ-009): any HTTP error other than 404 or 429 returns
{error:"openFDA HTTP <code>", detail:<body up to 300 chars>}.

Expected values SOURCED from mcp-servers/openfda/server.py:59-60:
    return {"error": f"openFDA HTTP {e.code}",
            "detail": e.read().decode("utf-8", "replace")[:300]}

Read-only / offline: urlopen monkeypatched to raise a 500 with a long body; the test also
checks the body is truncated to <=300 chars. PASS/FAIL emitted.
"""
import io
import sys
import urllib.error

from _oqlib_openfda import load_server

srv = load_server()

BODY = b"Server Error " * 60  # > 300 chars, to verify the 300-char cap


def fake_urlopen(url, timeout=None):
    raise urllib.error.HTTPError(url, 500, "Internal Server Error", {}, io.BytesIO(BODY))


srv.urllib.request.urlopen = fake_urlopen

res = srv._query("drug/label", "x", 5)

ok = (
    isinstance(res, dict)
    and res.get("error") == "openFDA HTTP 500"
    and "detail" in res
    and len(res["detail"]) <= 300
    and "rate_limit" not in res
)

if ok:
    print(f"PASS: 500 -> error={res['error']!r}, detail len={len(res['detail'])} (<=300)")
    sys.exit(0)
print(f"FAIL: expected {{error:'openFDA HTTP 500', detail:<=300 chars}}; got {res!r}")
sys.exit(1)

#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-007 — openFDA HTTP 404 returns an empty result set, not an error.

Requirement (OQ.md OQ-007): a 404 from openFDA is treated as "no matching records"
and returned as {total:0, results:[], note:"No matching records."} — never surfaced
as an error.

Expected values SOURCED from mcp-servers/openfda/server.py:46-47:
    if e.code == 404:
        return {"total": 0, "results": [], "note": "No matching records."}

Read-only / offline: urlopen is monkeypatched to raise a 404 HTTPError. PASS/FAIL emitted;
exits non-zero on FAIL.
"""
import io
import sys
import urllib.error

from _oqlib_openfda import load_server

srv = load_server()


def fake_urlopen(url, timeout=None):
    raise urllib.error.HTTPError(url, 404, "Not Found", {}, io.BytesIO(b"not found"))


srv.urllib.request.urlopen = fake_urlopen

res = srv._query("drug/label", 'openfda.brand_name:"___no_such_drug___"', 5)

ok = (
    isinstance(res, dict)
    and res.get("total") == 0
    and res.get("results") == []
    and "note" in res
    and "error" not in res
)

if ok:
    print(f"PASS: 404 -> {res}")
    sys.exit(0)
print(f"FAIL: expected empty no-match dict (total=0, results=[], note, no error); got {res!r}")
sys.exit(1)

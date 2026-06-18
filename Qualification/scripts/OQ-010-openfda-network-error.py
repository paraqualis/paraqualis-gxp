#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-010 — openFDA network failure / timeout is surfaced, not swallowed.

Requirement (OQ.md OQ-010): a generic Exception (network failure, timeout, parse error)
returns {error: str(e)}.

Expected behaviour SOURCED from mcp-servers/openfda/server.py:61-62:
    except Exception as e:                       # network/timeout/parse
        return {"error": str(e)}

Read-only / offline: urlopen monkeypatched to raise URLError("Connection refused").
NOTE (GOQ-002 / OQ-032): the error is returned to the caller but NOT logged server-side;
that logging gap is verified separately by OQ-032. PASS/FAIL emitted.
"""
import sys
import urllib.error

from _oqlib_openfda import load_server

srv = load_server()

MSG = "Connection refused"


def fake_urlopen(url, timeout=None):
    raise urllib.error.URLError(MSG)


srv.urllib.request.urlopen = fake_urlopen

res = srv._query("drug/label", "x", 5)

ok = (
    isinstance(res, dict)
    and "error" in res
    and MSG in res["error"]
    and "results" not in res
)

if ok:
    print(f"PASS: network failure surfaced as error: {res!r}")
    print("  NOTE (GOQ-002): error returned to caller but not logged server-side — see OQ-032")
    sys.exit(0)
print(f"FAIL: expected {{error: '...{MSG}...'}}; got {res!r}")
sys.exit(1)

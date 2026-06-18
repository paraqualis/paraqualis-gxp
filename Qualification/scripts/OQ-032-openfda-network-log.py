#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-032 — openFDA network-failure path must emit a server-side LOG entry.

Requirement (OQ.md OQ-032): when _query() catches a generic Exception (network failure,
timeout, parse error) it shall emit a log entry IN ADDITION to returning {error:...}, so the
failure is observable in the MCP server log.

Behaviour SOURCED from mcp-servers/openfda/server.py:61-62:
    except Exception as e:                       # network/timeout/parse
        return {"error": str(e)}
There is no logging call here — so this test is EXPECTED TO FAIL per the OQ assessment
(GOQ-002). It captures the gap deterministically: the error is returned to the caller but
nothing is written to stderr/stdout/logging.

Read-only / offline: urlopen monkeypatched to raise; stderr, stdout and the root logging
handlers are captured. Emits PASS only if a log entry is observed; else FAIL (the documented
result). Exits non-zero on FAIL.
"""
import io
import logging
import sys
import urllib.error

from _oqlib_openfda import load_server

srv = load_server()

MSG = "Connection refused"


def fake_urlopen(url, timeout=None):
    raise urllib.error.URLError(MSG)


srv.urllib.request.urlopen = fake_urlopen

# Capture every plausible "server log" channel: stderr, stdout, and the logging subsystem.
log_buf = io.StringIO()
log_handler = logging.StreamHandler(log_buf)
logging.getLogger().addHandler(log_handler)
logging.getLogger().setLevel(logging.DEBUG)

old_err, old_out = sys.stderr, sys.stdout
cap_err, cap_out = io.StringIO(), io.StringIO()
sys.stderr, sys.stdout = cap_err, cap_out
try:
    res = srv._query("drug/label", "x", 5)
finally:
    sys.stderr, sys.stdout = old_err, old_out
    logging.getLogger().removeHandler(log_handler)

logged = bool(cap_err.getvalue().strip() or cap_out.getvalue().strip() or log_buf.getvalue().strip())
error_returned = isinstance(res, dict) and "error" in res and MSG in res["error"]

if error_returned and logged:
    print("PASS: network failure surfaced AND logged server-side")
    print(f"  log evidence: {(cap_err.getvalue() + log_buf.getvalue()).strip()[:120]!r}")
    sys.exit(0)

# Expected per assessment: error returned to caller, but NO server-side log entry.
print("FAIL: network failure returned to caller but NOT logged server-side (GOQ-002)")
print(f"  returned error = {res!r}")
print("  stderr/stdout/logging were all empty during the failure")
sys.exit(1)

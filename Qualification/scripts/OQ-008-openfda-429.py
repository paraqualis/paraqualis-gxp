#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-008 — openFDA HTTP 429 surfaces an actionable, key-aware rate-limit error.

Requirement (OQ.md OQ-008): a 429 returns {error:..., rate_limit:True}. No-key users
get /openfda:setup guidance (message mentions the "shared" tier); keyed users get a
quota-reset message (mentions "quota").

Expected values SOURCED from mcp-servers/openfda/server.py:48-58.

Read-only / offline: urlopen monkeypatched to raise a 429; OPENFDA_API_KEY toggled in
os.environ to drive both branches (restored afterwards). PASS/FAIL emitted.
"""
import io
import os
import sys
import urllib.error

from _oqlib_openfda import load_server

srv = load_server()


def fake_urlopen(url, timeout=None):
    raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, io.BytesIO(b"rate"))


srv.urllib.request.urlopen = fake_urlopen

failures = []
saved_key = os.environ.get("OPENFDA_API_KEY")
try:
    # No-key branch.
    os.environ.pop("OPENFDA_API_KEY", None)
    r_nokey = srv._query("drug/label", "x", 5)
    if not (r_nokey.get("rate_limit") is True and "error" in r_nokey
            and "shared" in r_nokey["error"].lower()):
        failures.append(f"no-key branch wrong: {r_nokey!r}")
    else:
        print(f"PASS: no-key 429 -> rate_limit=True, mentions shared tier: {r_nokey['error'][:60]}...")

    # Keyed branch.
    os.environ["OPENFDA_API_KEY"] = "TESTKEY_OQ008"
    r_key = srv._query("drug/label", "x", 5)
    if not (r_key.get("rate_limit") is True and "error" in r_key
            and "quota" in r_key["error"].lower()):
        failures.append(f"keyed branch wrong: {r_key!r}")
    else:
        print(f"PASS: keyed 429 -> rate_limit=True, mentions quota: {r_key['error'][:60]}...")
finally:
    if saved_key is None:
        os.environ.pop("OPENFDA_API_KEY", None)
    else:
        os.environ["OPENFDA_API_KEY"] = saved_key

if failures:
    for f in failures:
        print(f"FAIL: {f}")
    sys.exit(1)
print("PASS: both 429 branches surface actionable, key-aware errors")
sys.exit(0)

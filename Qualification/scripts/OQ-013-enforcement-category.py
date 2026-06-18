#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-013 — search_enforcement() rejects invalid category after normalisation.

Requirement (OQ.md OQ-013): search_enforcement() returns
{error:"category must be 'drug', 'device', or 'food'"} for any category not in that set,
after normalising case and whitespace.

Behaviour SOURCED from mcp-servers/openfda/server.py:94-96:
    cat = category.lower().strip()
    if cat not in {"drug", "device", "food"}:
        return {"error": "category must be 'drug', 'device', or 'food'"}

Read-only / offline: invalid categories are checked directly (the validation runs before any
network call, so they never reach urlopen). Valid categories DO call _query, so urlopen is
stubbed to a deterministic empty success — this confirms the valid category was ACCEPTED
(passed validation) without hitting the live API. PASS/FAIL emitted.
"""
import sys

from _oqlib_openfda import load_server

srv = load_server()

EXPECTED_ERR = "category must be 'drug', 'device', or 'food'"


def fake_urlopen(url, timeout=None):
    raise AssertionError(
        "urlopen must not be reached for invalid categories; for valid ones it is stubbed"
    )


# For valid categories we want to confirm they pass validation. Stub urlopen to return a
# minimal valid JSON body so _query returns a results dict (not an error) — proving the
# category was accepted rather than rejected.
class _Resp:
    def __init__(self, body):
        self._body = body

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def ok_urlopen(url, timeout=None):
    return _Resp(b'{"meta":{"results":{"total":0}},"results":[]}')


failures = []

# Invalid categories -> error dict. urlopen guarded so a leak would crash loudly.
srv.urllib.request.urlopen = fake_urlopen
for bad in ["pharmaceutical", "Human", ""]:
    r = srv.search_enforcement(category=bad, search="x", limit=1)
    if r.get("error") == EXPECTED_ERR:
        print(f"PASS: category={bad!r} rejected with exact error")
    else:
        failures.append(f"category={bad!r} not rejected correctly: {r!r}")

# Valid categories (incl. case/whitespace variants) -> accepted (no category error).
srv.urllib.request.urlopen = ok_urlopen
for good in ["drug", "Drug", "DRUG", "food "]:
    r = srv.search_enforcement(category=good, search="x", limit=1)
    if r.get("error") == EXPECTED_ERR:
        failures.append(f"category={good!r} wrongly rejected: {r!r}")
    else:
        print(f"PASS: category={good!r} accepted after normalisation")

if failures:
    for f in failures:
        print(f"FAIL: {f}")
    sys.exit(1)
print("PASS: category validation correct for all cases")
sys.exit(0)

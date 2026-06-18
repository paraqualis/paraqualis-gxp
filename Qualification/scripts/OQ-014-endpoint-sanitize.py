#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-014 — openfda_query() sanitises the endpoint before building the URL.

Requirement (OQ.md OQ-014): leading/trailing whitespace and slashes are stripped and a
trailing '.json' suffix is removed from the endpoint parameter.
    "/drug/label/"   -> "drug/label"
    "food/event.json"-> "food/event"
    "  drug/ndc  "   -> "drug/ndc"

Behaviour SOURCED from mcp-servers/openfda/server.py:166:
    endpoint = endpoint.strip().strip("/").removesuffix(".json")
and the URL is built at server.py:41:
    url = f"{BASE}/{endpoint}.json?..."

Read-only / offline: urlopen is stubbed to CAPTURE the URL openfda_query builds, then the
test asserts the URL contains BASE/<sanitised>.json. This exercises the real sanitisation +
URL-building path end to end without a network call. PASS/FAIL emitted.
"""
import sys

from _oqlib_openfda import load_server

srv = load_server()

captured = {"url": None}


class _Resp:
    def read(self):
        return b'{"meta":{"results":{"total":0}},"results":[]}'

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def capturing_urlopen(url, timeout=None):
    captured["url"] = url
    return _Resp()


srv.urllib.request.urlopen = capturing_urlopen

cases = [
    ("/drug/label/", "drug/label"),
    ("food/event.json", "food/event"),
    ("  drug/ndc  ", "drug/ndc"),
]

failures = []
for raw, expected in cases:
    captured["url"] = None
    srv.openfda_query(endpoint=raw, search="x", limit=1)
    url = captured["url"] or ""
    needle = f"{srv.BASE}/{expected}.json?"
    if url.startswith(needle):
        print(f"PASS: {raw!r} -> endpoint {expected!r} (url: {url.split('?')[0]})")
    else:
        failures.append(f"{raw!r} -> built url {url!r}, expected to start with {needle!r}")

if failures:
    for f in failures:
        print(f"FAIL: {f}")
    sys.exit(1)
print("PASS: all endpoints sanitised correctly")
sys.exit(0)

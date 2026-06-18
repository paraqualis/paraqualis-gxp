#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-015 — _trunc(v, n=600) edge-case behaviour.

Requirement (OQ.md OQ-015): _trunc shall join list inputs with spaces; truncate strings
longer than 600 chars and append '…' (1-char Unicode ellipsis); return "" for None; and
NOT truncate a string of exactly 600 chars.

Behaviour SOURCED from mcp-servers/openfda/server.py:78-80:
    def _trunc(v, n=600) -> str:
        s = " ".join(v) if isinstance(v, list) else (v or "")
        return s[:n] + ("…" if len(s) > n else "")

Read-only / offline: pure-function test, no network. PASS/FAIL emitted.
"""
import sys

from _oqlib_openfda import load_server

srv = load_server()

ELLIPSIS = "…"  # single Unicode code point U+2026
failures = []

# 1. list -> joined with single spaces
r = srv._trunc(["a", "b", "c"])
if r == "a b c":
    print("PASS: list joined -> 'a b c'")
else:
    failures.append(f"list join: got {r!r}, expected 'a b c'")

# 2. 700-char string -> 600 + ellipsis = 601 chars
s700 = "x" * 700
r = srv._trunc(s700)
if len(r) == 601 and r.endswith(ELLIPSIS) and r[:600] == "x" * 600:
    print("PASS: 700-char string -> 601 chars (600 + 1-char ellipsis)")
else:
    failures.append(f"700-char truncate: len={len(r)}, endswith ellipsis={r.endswith(ELLIPSIS)}")

# 3. None -> ""
r = srv._trunc(None)
if r == "":
    print("PASS: None -> ''")
else:
    failures.append(f"None: got {r!r}, expected ''")

# 4. exactly 600 chars -> unchanged, no ellipsis
s600 = "y" * 600
r = srv._trunc(s600)
if r == s600 and not r.endswith(ELLIPSIS):
    print("PASS: exactly 600-char string unchanged (no ellipsis)")
else:
    failures.append(f"600-char boundary: len={len(r)}, changed={r != s600}")

if failures:
    for f in failures:
        print(f"FAIL: {f}")
    sys.exit(1)
print("PASS: _trunc edge cases all correct")
sys.exit(0)

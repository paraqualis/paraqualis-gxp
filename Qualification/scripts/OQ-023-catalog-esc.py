#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-023 — build_catalog.esc() escapes pipe characters for Markdown-table safety.

Requirement (OQ.md OQ-023): esc() shall replace every '|' with '\\|' so a description
containing a pipe cannot corrupt the generated Markdown table.
    esc("A | B | C") -> "A \\| B \\| C"

Behaviour SOURCED from docs/build_catalog.py:45-46:
    def esc(s: str) -> str:
        return s.replace("|", "\\|")

Read-only / offline: pure-function test. PASS/FAIL emitted; exits non-zero on FAIL.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "docs")))
import build_catalog  # noqa: E402

failures = []

cases = [
    ("A | B | C", "A \\| B \\| C"),
    ("no pipes here", "no pipes here"),
    ("|", "\\|"),
    ("a|b|c", "a\\|b\\|c"),
]

for raw, expected in cases:
    got = build_catalog.esc(raw)
    if got == expected:
        print(f"PASS: esc({raw!r}) -> {got!r}")
    else:
        failures.append(f"esc({raw!r}) -> {got!r}, expected {expected!r}")

if failures:
    for f in failures:
        print(f"FAIL: {f}")
    sys.exit(1)
print("PASS: esc() escapes all pipe characters")
sys.exit(0)

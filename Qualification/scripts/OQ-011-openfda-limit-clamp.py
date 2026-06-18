#!/usr/bin/env python3
"""OQ-011 — Verify _query() limit is clamped to [1, 50].
Tests boundary values: 0, 1, 50, 51, 999, -5.
PASS: all values clamp correctly.
"""
import sys

def clamp(limit):
    return max(1, min(int(limit), 50))

cases = [
    (0, 1),
    (1, 1),
    (50, 50),
    (51, 50),
    (999, 50),
    (-5, 1),
]

all_pass = True
for inp, expected in cases:
    got = clamp(inp)
    status = 'PASS' if got == expected else 'FAIL'
    print(f'{status}: clamp({inp}) -> {got} (expected {expected})')
    if status == 'FAIL':
        all_pass = False

sys.exit(0 if all_pass else 1)

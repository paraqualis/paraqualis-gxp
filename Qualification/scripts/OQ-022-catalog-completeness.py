#!/usr/bin/env python3
"""OQ-022 — All 18 commands discoverable with non-empty descriptions; 6 families.
PASS: 18 commands, 6 families, 0 empty descriptions.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'docs'))
import build_catalog

fams = build_catalog.commands()
total = sum(len(v) for v in fams.values())
empty = [(fam, inv) for fam, items in fams.items() for inv, desc in items if not desc]
n_fams = len(fams)

print(f'Families found: {sorted(fams.keys())} (count={n_fams})')
print(f'Total commands: {total}')
print(f'Commands with empty description: {len(empty)}')

all_pass = True
if total != 18:
    print(f'FAIL: expected 18 commands, got {total}')
    all_pass = False
else:
    print('PASS: 18 commands found')
if n_fams != 6:
    print(f'FAIL: expected 6 families, got {n_fams}')
    all_pass = False
else:
    print('PASS: 6 families found')
if empty:
    print(f'FAIL: commands with empty description: {empty}')
    all_pass = False
else:
    print('PASS: all commands have non-empty descriptions')

sys.exit(0 if all_pass else 1)

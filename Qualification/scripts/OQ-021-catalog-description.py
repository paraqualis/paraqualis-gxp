#!/usr/bin/env python3
"""OQ-021 — build_catalog.description() handles no-frontmatter and folded blocks.
PASS: correct return value for both input types.
"""
import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'docs'))
import build_catalog
from pathlib import Path

results = []

# Test 1: file with no frontmatter -> ""
tf = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf.write('# Just a heading\nNo frontmatter here.')
tf.close()
got = build_catalog.description(Path(tf.name))
os.unlink(tf.name)
ok = got == ''
results.append(('no-frontmatter', ok, got, '""'))

# Test 2: folded description -> joined string
tf2 = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf2.write('---\ndescription: >-\n  Line one\n  Line two\n---\ncontent')
tf2.close()
got2 = build_catalog.description(Path(tf2.name))
os.unlink(tf2.name)
ok2 = got2 == 'Line one Line two'
results.append(('folded-block', ok2, got2, '"Line one Line two"'))

all_pass = True
for name, ok, actual, expected in results:
    status = 'PASS' if ok else 'FAIL'
    print(f'{status}: {name}: got {actual!r} (expected {expected})')
    if not ok:
        all_pass = False

sys.exit(0 if all_pass else 1)

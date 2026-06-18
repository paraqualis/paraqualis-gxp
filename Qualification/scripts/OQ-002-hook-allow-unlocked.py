#!/usr/bin/env python3
"""OQ-002 — Hook allows edit of unlocked file.
PASS: exit code 0.
"""
import sys, io, json, os, tempfile, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

tf = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf.write('# Normal doc\nNo lock marker.')
tf.close()

event = {'tool_input': {'file_path': tf.name}}
sys.stdin = io.StringIO(json.dumps(event))
result = m.main()
sys.stdin = sys.__stdin__
os.unlink(tf.name)

if result == 0:
    print('PASS: hook allowed unlocked file (exit 0)')
    sys.exit(0)
else:
    print(f'FAIL: expected exit 0, got {result}')
    sys.exit(1)

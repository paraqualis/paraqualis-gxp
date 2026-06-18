#!/usr/bin/env python3
"""OQ-001 — Hook blocks edit of locked file.
PASS: exit code 2, stderr contains 'Blocked'.
"""
import sys, io, json, os, tempfile, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Create a temporary locked file
tf = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf.write('# Approved doc\n<!-- PARAQUALIS-LOCK: approved -->\nContent.')
tf.close()

event = {'tool_input': {'file_path': tf.name}}
sys.stdin = io.StringIO(json.dumps(event))
old_err = sys.stderr
sys.stderr = io.StringIO()
result = m.main()
stderr_out = sys.stderr.getvalue()
sys.stderr = old_err
sys.stdin = sys.__stdin__
os.unlink(tf.name)

if result == 2 and 'Blocked' in stderr_out and tf.name in stderr_out:
    print('PASS: hook blocked locked file (exit 2, correct stderr message)')
    sys.exit(0)
else:
    print(f'FAIL: exit={result}, stderr={stderr_out!r}')
    sys.exit(1)

#!/usr/bin/env python3
"""OQ-003 — Hook allows creation of new (non-existent) file.
PASS: exit code 0 for a path that does not exist.
"""
import sys, io, json, os, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

NONEXISTENT = '/tmp/__oq_003_nonexistent_file_paraqualis__.md'
assert not os.path.exists(NONEXISTENT), f'File unexpectedly exists: {NONEXISTENT}'

event = {'tool_input': {'file_path': NONEXISTENT}}
sys.stdin = io.StringIO(json.dumps(event))
result = m.main()
sys.stdin = sys.__stdin__

if result == 0:
    print('PASS: hook allowed non-existent (new) file (exit 0)')
    sys.exit(0)
else:
    print(f'FAIL: expected exit 0, got {result}')
    sys.exit(1)

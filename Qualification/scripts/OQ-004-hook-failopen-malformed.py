#!/usr/bin/env python3
"""OQ-004 — Hook fails open on malformed JSON.
PASS: exit code 0 (fail-open).
NOTE: GOQ-001 — currently no log emitted on this path; test captures that gap.
"""
import sys, io, os, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

sys.stdin = io.StringIO('{not valid json at all}')
old_err = sys.stderr
sys.stderr = io.StringIO()
result = m.main()
stderr_out = sys.stderr.getvalue()
sys.stderr = old_err
sys.stdin = sys.__stdin__

if result == 0:
    print('PASS: hook fails open on malformed JSON (exit 0)')
    if not stderr_out:
        print('  NOTE (GOQ-001): no log emitted on fail-open path — gap remains open')
    sys.exit(0)
else:
    print(f'FAIL: expected exit 0 (fail-open), got {result}')
    sys.exit(1)

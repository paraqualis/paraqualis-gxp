#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-005 — Hook reads notebook_path (NotebookEdit tool) and blocks a locked notebook.

Requirement (OQ.md OQ-005): the hook shall read the `notebook_path` key as the target path
when `file_path` is absent, covering the NotebookEdit tool call. Blocking a locked .ipynb
targeted via notebook_path must return exit 2 with a "Blocked" message.

Behaviour SOURCED from hooks/protect-approved-documents.py:39:
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
and the block path at protect-approved-documents.py:51-58.

Read-only / offline: creates a temp locked .ipynb, feeds an event with notebook_path on
stdin, captures stderr. PASS/FAIL emitted; exits non-zero on FAIL.
"""
import importlib.util
import io
import json
import os
import sys
import tempfile

HOOK = os.path.join(os.path.dirname(__file__), "..", "..", "hooks", "protect-approved-documents.py")
spec = importlib.util.spec_from_file_location("hook", os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Locked notebook content — the marker just needs to appear anywhere in the text.
tf = tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False)
tf.write('{"cells": [], "metadata": {"note": "<!-- PARAQUALIS-LOCK: approved -->"}}')
tf.close()

# NotebookEdit-style event: notebook_path present, file_path absent.
event = {"tool_input": {"notebook_path": tf.name}}
sys.stdin = io.StringIO(json.dumps(event))
old_err = sys.stderr
sys.stderr = io.StringIO()
try:
    result = m.main()
    stderr_out = sys.stderr.getvalue()
finally:
    sys.stderr = old_err
    sys.stdin = sys.__stdin__
    os.unlink(tf.name)

if result == 2 and "Blocked" in stderr_out and tf.name in stderr_out:
    print("PASS: notebook_path recognised; locked notebook blocked (exit 2)")
    sys.exit(0)
print(f"FAIL: exit={result}, stderr={stderr_out!r}")
sys.exit(1)

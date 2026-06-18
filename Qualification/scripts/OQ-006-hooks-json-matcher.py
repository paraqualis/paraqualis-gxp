#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-006 — hooks.json matcher covers exactly the four file-writing tools.

Requirement (OQ.md OQ-006): the PreToolUse matcher in hooks/hooks.json must equal exactly
"Edit|Write|MultiEdit|NotebookEdit" — the four tools capable of modifying file content — so
no write path bypasses the protection hook.

Expected value SOURCED from hooks/hooks.json:5:
    "matcher": "Edit|Write|MultiEdit|NotebookEdit"

This is the .py artifact named in OQ.md OQ-006's Test artifact field. (A pre-existing
OQ-006-hooks-json-matcher.sh checks the same thing; it is left untouched.)

Read-only: parses hooks.json and compares the matcher string and its tool set.
PASS/FAIL emitted; exits non-zero on FAIL.
"""
import json
import os
import sys

HOOKS_JSON = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "hooks", "hooks.json")
)
EXPECTED = "Edit|Write|MultiEdit|NotebookEdit"
EXPECTED_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}

if not os.path.isfile(HOOKS_JSON):
    print(f"FAIL: hooks.json not found at {HOOKS_JSON}")
    sys.exit(1)

with open(HOOKS_JSON, encoding="utf-8") as f:
    d = json.load(f)

try:
    matcher = d["hooks"]["PreToolUse"][0]["matcher"]
except (KeyError, IndexError, TypeError) as e:
    print(f"FAIL: could not locate PreToolUse[0].matcher in hooks.json ({e})")
    sys.exit(1)

tools = set(matcher.split("|"))
if matcher == EXPECTED and tools == EXPECTED_TOOLS:
    print(f"PASS: matcher = {matcher!r} (covers exactly the four writing tools)")
    sys.exit(0)
print(f"FAIL: matcher = {matcher!r}; expected {EXPECTED!r} (tools {sorted(EXPECTED_TOOLS)})")
sys.exit(1)

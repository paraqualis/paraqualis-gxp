#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-018 — build_docx.render() handles an empty Markdown file without crashing.

Requirement (OQ.md OQ-018): render() on an empty .md file shall produce a valid
(empty-body) .docx without raising an exception. Acceptance: .docx created; no exception.

System under test: qualification-pack-template/build_docx.py:111-171 (render() reads the
file, iterates 0 lines, and saves a valid document).

Read-only / safe: renders an empty temp .md into a private temp dir, then re-opens the
result to confirm it is a structurally valid docx. Requires python-docx; FAILS LOUD if
absent. PASS/FAIL emitted; exits non-zero on FAIL.
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

BUILD_DOCX = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "qualification-pack-template", "build_docx.py")
)

try:
    spec = importlib.util.spec_from_file_location("build_docx", BUILD_DOCX)
    build_docx = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_docx)
    from docx import Document
except ModuleNotFoundError as e:
    print(f"FAIL: required dependency missing for build_docx ({e}). Run: pip install python-docx")
    sys.exit(1)

with tempfile.TemporaryDirectory() as d:
    md_path = Path(d) / "empty.md"
    out_path = Path(d) / "empty.docx"
    md_path.write_text("", encoding="utf-8")
    try:
        build_docx.render(md_path, out_path)
    except Exception as e:
        print(f"FAIL: render() raised an exception on empty markdown: {e!r}")
        sys.exit(1)

    if not out_path.exists():
        print("FAIL: no .docx produced for empty markdown")
        sys.exit(1)
    try:
        Document(str(out_path))  # re-open to confirm structural validity
    except Exception as e:
        print(f"FAIL: produced .docx is not a valid document: {e!r}")
        sys.exit(1)
    print(f"PASS: empty markdown -> valid empty .docx ({out_path.stat().st_size} bytes), no crash")
    sys.exit(0)

#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-016 — build_docx.render() produces a valid branded .docx from representative Markdown.

Requirement (OQ.md OQ-016): render(md_path, out_path) shall produce a non-empty,
structurally valid .docx from Markdown containing headings, tables, code fences,
blockquotes, bullets, bold, and horizontal rules. Acceptance: output created, > 5,000 bytes,
no exception.

System under test: qualification-pack-template/build_docx.py:93-171 (render()).

Read-only / safe: writes ONLY into a private temp directory (never into the repo) and
cleans up. Requires python-docx; if absent it FAILS LOUD (never silently skips).
PASS/FAIL emitted; exits non-zero on FAIL.
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
except ModuleNotFoundError as e:
    print(f"FAIL: required dependency missing for build_docx ({e}). Run: pip install python-docx")
    sys.exit(1)

MD = """# Heading One

Some **bold** body text and a normal paragraph.

## Heading Two

| Col A | Col B |
|---|---|
| 1 | 2 |
| 3 | 4 |

> A blockquote line.

- bullet one
- bullet two

```
code fence line
```

---
"""

with tempfile.TemporaryDirectory() as d:
    md_path = Path(d) / "sample.md"
    out_path = Path(d) / "sample.docx"
    md_path.write_text(MD, encoding="utf-8")
    try:
        build_docx.render(md_path, out_path)
    except Exception as e:
        print(f"FAIL: render() raised an exception: {e!r}")
        sys.exit(1)

    if not out_path.exists():
        print("FAIL: no .docx produced")
        sys.exit(1)
    size = out_path.stat().st_size
    if size > 5000:
        print(f"PASS: rendered valid .docx ({size} bytes, > 5000)")
        sys.exit(0)
    print(f"FAIL: .docx too small ({size} bytes, expected > 5000)")
    sys.exit(1)

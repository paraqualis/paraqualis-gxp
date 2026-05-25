#!/usr/bin/env python3
"""build_docs.py — build the repo's own documentation: refresh the OVERVIEW catalog
from the repo, then render the key docs to branded ParaQualis Word (.docx).

On-demand "build everything" — run this when you want fresh shareable Word:
    python3 docs/build_docs.py

(The git pre-commit hook only refreshes the Markdown catalog — cheap and text-only.
Run THIS to also regenerate the .docx, which are binary and don't need rebuilding on
every commit.)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "docs"))
sys.path.insert(0, str(ROOT / "qualification-pack-template"))

import build_catalog                     # noqa: E402
from build_docx import render            # noqa: E402

build_catalog.main()                     # refresh OVERVIEW.md catalog from the repo
for stem in ("OVERVIEW", "how-to-qualify", "xq-qualification-protocol"):
    md = ROOT / "docs" / f"{stem}.md"
    if md.exists():
        render(md, md.with_suffix(".docx"))
        print(f"  rendered docs/{stem}.docx")
print("docs built: catalog refreshed + Word rendered (ParaQualis-branded, landscape).")

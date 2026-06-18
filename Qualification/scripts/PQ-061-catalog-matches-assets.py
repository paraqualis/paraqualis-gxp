#!/usr/bin/env python3
# PQ-061 — The docs/OVERVIEW.md catalog regenerates to match the actual repo assets (no drift).
# Traces: URS-061. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): the user-facing catalog of commands/skills/sub-agents must
# reflect what is actually installed, never a hand-maintained list that quietly drifts. The
# catalog is produced by build_catalog.py from the repo. This test verifies the catalog block
# CURRENTLY IN docs/OVERVIEW.md lists exactly the commands, skills, and agents present in the
# repo — i.e. it is up to date with the assets. It is read-only: it parses OVERVIEW.md and
# compares names against the filesystem; it does NOT rewrite OVERVIEW.md (that would modify a
# file outside Qualification/).
#
# The asset->catalog mapping rule is SOURCED from docs/build_catalog.py:49-94 (commands as
#   family:name, skills as skill dir name, agents as file stem).
#
# Usage: python3 PQ-061-catalog-matches-assets.py [REPO_ROOT]
import sys
import os
import re

REPO = sys.argv[1] if len(sys.argv) > 1 else "/Users/craigwylie/Devl/paraqualis-skills"
OVERVIEW = os.path.join(REPO, "docs", "OVERVIEW.md")

print("PQ-061 catalog matches actual assets (no drift)")
print("-" * 60)

if not os.path.exists(OVERVIEW):
    print(f"FAIL  catalog file not found: {OVERVIEW}")
    sys.exit(1)

text = open(OVERVIEW, encoding="utf-8", errors="ignore").read()
m = re.search(r"<!-- CATALOG:START -->(.*?)<!-- CATALOG:END -->", text, re.S)
if not m:
    print("FAIL  CATALOG markers not found in OVERVIEW.md")
    sys.exit(1)
block = m.group(1)
fail = 0

# Expected commands as family:name (or /name for top-level), per build_catalog.py.
cmd_base = os.path.join(REPO, "commands")
expected_cmds = set()
for root, _dirs, files in os.walk(cmd_base):
    for f in files:
        if not f.endswith(".md"):
            continue
        rel = os.path.relpath(os.path.join(root, f), cmd_base)
        parts = rel.split(os.sep)
        stem = f[:-3]
        if len(parts) == 1:
            expected_cmds.add(f"/{stem}")
        else:
            expected_cmds.add(f"/{parts[0]}:{stem}")

missing_cmds = [c for c in sorted(expected_cmds) if c not in block]
if missing_cmds:
    print(f"FAIL  catalog missing commands present in repo: {missing_cmds}")
    fail = 1
else:
    print(f"PASS  all {len(expected_cmds)} repo commands appear in the catalog")

# Expected skills (skill dir names).
skills_dir = os.path.join(REPO, "skills")
expected_skills = [d for d in os.listdir(skills_dir)
                   if os.path.exists(os.path.join(skills_dir, d, "SKILL.md"))]
missing_sk = [s for s in expected_skills if s not in block]
if missing_sk:
    print(f"FAIL  catalog missing skills: {missing_sk}")
    fail = 1
else:
    print(f"PASS  all {len(expected_skills)} skills appear in the catalog")

# Expected agents (file stems).
agents_dir = os.path.join(REPO, "agents")
expected_agents = [f[:-3] for f in os.listdir(agents_dir) if f.endswith(".md")]
missing_ag = [a for a in expected_agents if a not in block]
if missing_ag:
    print(f"FAIL  catalog missing sub-agents: {missing_ag}")
    fail = 1
else:
    print(f"PASS  all {len(expected_agents)} sub-agents appear in the catalog")

print("-" * 60)
if fail == 0:
    print("RESULT: PASS — catalog matches the current repo assets (no drift).")
    sys.exit(0)
print("RESULT: FAIL — catalog has drifted from the repo assets (re-run build_catalog.py).")
sys.exit(1)

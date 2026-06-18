#!/usr/bin/env python3
#
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
#
"""OQ-028 — Sub-agent and skill metadata declares correct toolsets and model.

Requirement (OQ.md OQ-028): all three sub-agent files declare tools containing
Read/Grep/Glob/Bash and model: sonnet in their YAML frontmatter; both skill SKILL.md files
have a non-empty description.

Subjects: agents/iq-qualifier.md, agents/oq-qualifier.md, agents/pq-qualifier.md (frontmatter
'tools:' and 'model:'); skills/gamp-advisor/SKILL.md, skills/part11-advisor/SKILL.md
('description:').

Read-only: parses the YAML frontmatter block of each file. No third-party deps (a tiny
frontmatter scanner is used so the test runs in a bare environment). PASS/FAIL emitted;
exits non-zero on FAIL.
"""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

AGENTS = [
    "agents/iq-qualifier.md",
    "agents/oq-qualifier.md",
    "agents/pq-qualifier.md",
]
SKILLS = [
    "skills/gamp-advisor/SKILL.md",
    "skills/part11-advisor/SKILL.md",
]
REQUIRED_TOOLS = {"Read", "Grep", "Glob", "Bash"}
REQUIRED_MODEL = "sonnet"


def frontmatter(path):
    """Return the text of the leading --- ... --- YAML block (or '')."""
    t = open(path, encoding="utf-8").read()
    if not t.startswith("---"):
        return ""
    end = t.find("\n---", 3)
    return t[3:end] if end != -1 else t[3:]


def scalar(fm, key):
    """Pull a simple 'key: value' scalar from the frontmatter, or '' if absent/folded."""
    m = re.search(rf"^\s*{re.escape(key)}:\s*(.*)$", fm, flags=re.M)
    return m.group(1).strip() if m else ""


def has_description(path):
    """True if 'description:' is present with non-empty content (inline or folded block)."""
    fm = frontmatter(path)
    m = re.search(r"^\s*description:\s*(.*)$", fm, flags=re.M)
    if not m:
        return False
    val = m.group(1).strip()
    if val and val not in (">", ">-", "|", "|-"):
        return True
    # folded/literal block: look for at least one indented continuation line
    tail = fm[m.end():]
    return bool(re.search(r"\n\s+\S", tail))


failures = []

for rel in AGENTS:
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path):
        failures.append(f"{rel}: file not found")
        continue
    fm = frontmatter(path)
    tools_raw = scalar(fm, "tools")
    tools = {t.strip() for t in tools_raw.split(",") if t.strip()}
    model = scalar(fm, "model")
    if not REQUIRED_TOOLS.issubset(tools):
        failures.append(f"{rel}: tools missing {sorted(REQUIRED_TOOLS - tools)} (got {sorted(tools)})")
    elif model != REQUIRED_MODEL:
        failures.append(f"{rel}: model={model!r}, expected {REQUIRED_MODEL!r}")
    else:
        print(f"PASS: {rel} declares tools {sorted(REQUIRED_TOOLS)} and model={model}")

for rel in SKILLS:
    path = os.path.join(ROOT, rel)
    if not os.path.isfile(path):
        failures.append(f"{rel}: file not found")
        continue
    if has_description(path):
        print(f"PASS: {rel} has a non-empty description")
    else:
        failures.append(f"{rel}: missing/empty description")

if failures:
    for f in failures:
        print(f"FAIL: {f}")
    sys.exit(1)
print("PASS: all agent/skill metadata correct")
sys.exit(0)

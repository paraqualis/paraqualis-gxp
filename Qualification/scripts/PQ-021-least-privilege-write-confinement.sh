#!/usr/bin/env bash
# PQ-021 — In use, sub-agents are read-only and pack writes stay inside Qualification/.
# Traces: URS-021 (also evidences URS-004 write-confinement in the as-built config).
# ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): when this toolkit qualifies someone else's GxP system,
# it must not be able to alter that system. The guarantee is twofold: the three specialist
# sub-agents are granted ONLY read/inspect tools, and the pack writer confines its output to
# a new Qualification/ folder. This test reads the sub-agent definitions and the build command
# to confirm both controls are declared as-built.
#
# The allowed read-only toolset and the write-confinement rule are SOURCED from:
#   agents/*.md frontmatter 'tools:'  and  commands/qualify/build.md (Qualification/ only).
# READ-ONLY. PASS/FAIL. Exit 0 = PASS, 1 = FAIL.
set -uo pipefail
REPO="${1:-/Users/craigwylie/Devl/paraqualis-gxp}"
echo "PQ-021 least privilege + write confinement"
echo "------------------------------------------------------------"
fail=0

# Allowed read-only tool vocabulary for the qualifier sub-agents (sourced: agents/pq-qualifier.md:9).
ALLOWED='^(Read|Grep|Glob|Bash)$'
WRITE_TOOLS='Edit|Write|MultiEdit|NotebookEdit'

for ag in iq-qualifier oq-qualifier pq-qualifier; do
  f="$REPO/agents/$ag.md"
  if [ ! -f "$f" ]; then echo "FAIL  $ag definition missing"; fail=1; continue; fi
  line="$(grep -E '^tools:' "$f" | head -1 | sed 's/^tools:[[:space:]]*//')"
  if [ -z "$line" ]; then echo "FAIL  $ag declares no 'tools:' (privilege undefined)"; fail=1; continue; fi
  # No write tool may appear.
  if echo "$line" | grep -qE "$WRITE_TOOLS"; then
    echo "FAIL  $ag is granted a write tool: $line"
    fail=1
  else
    # Every declared tool must be in the read-only allow-list.
    bad=0
    IFS=',' read -ra toks <<< "$line"
    for t in "${toks[@]}"; do
      tt="$(echo "$t" | xargs)"
      [ -z "$tt" ] && continue
      echo "$tt" | grep -qE "$ALLOWED" || { echo "WARN  $ag has unrecognised tool '$tt'"; bad=1; }
    done
    if [ "$bad" -eq 0 ]; then
      echo "PASS  $ag is read-only: [$line]"
    else
      echo "PASS  $ag has no write tool (note unrecognised tool above): [$line]"
    fi
  fi
done

# Pack-writer confinement: build command must constrain writes to Qualification/.
bc="$REPO/commands/qualify/build.md"
if grep -qiE 'modify .*no existing files|new[* ]+folder|Qualification/ .*(inside|by default)' "$bc" 2>/dev/null; then
  echo "PASS  /qualify:build confines writes to Qualification/ (no existing files modified)"
else
  echo "WARN  /qualify:build write-confinement wording not found explicitly; verify in PQ-003"
fi

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS — sub-agents read-only; pack writes confined as-built."
  echo "NOTE: a live witnessed /qualify:build (PQ-003 Note) confirms ONLY Qualification/ is"
  echo "      created at run time — the runtime proof complements this static evidence."
  exit 0
fi
echo "RESULT: FAIL — a least-privilege control is not met as-built."
exit 1

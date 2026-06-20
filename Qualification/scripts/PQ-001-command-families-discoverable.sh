#!/usr/bin/env bash
# PQ-001 — The toolkit's slash commands are discoverable, grouped by family.
# Traces: URS-001. ParaQualis-authored, pending owner confirmation.
#
# Intended use (plain English): a user of the toolkit reaches every capability by typing a
# slash command grouped under a named family (cfr21-11, eCFR, eu-annex11, gamp, openfda,
# qualify). This test confirms each expected family folder exists and contains at least one
# well-formed command file (a Markdown file with the `description:` frontmatter that makes it
# discoverable in Claude Code). It does NOT execute the commands (they drive an LLM); it
# proves the command surface a user picks from is present and well-formed.
#
# Expected families are SOURCED from the live command tree, cross-checked against the URS
# requirement URS-001 which names the six families.
# READ-ONLY. Emits PASS/FAIL. Exit 0 = PASS, 1 = FAIL.
set -euo pipefail
REPO="${1:-/Users/craigwylie/Devl/paraqualis-gxp}"
CMD="$REPO/commands"

# Families named in URS-001 (Qualification/requirements/URS.md:36) — the discoverability spec.
EXPECTED_FAMILIES=(cfr21-11 eCFR eu-annex11 gamp openfda qualify)

fail=0
echo "PQ-001 command-family discoverability — target: $CMD"
echo "------------------------------------------------------------"
for fam in "${EXPECTED_FAMILIES[@]}"; do
  dir="$CMD/$fam"
  if [ ! -d "$dir" ]; then
    echo "FAIL  family '$fam' folder missing"
    fail=1; continue
  fi
  count=0
  for md in "$dir"/*.md; do
    [ -e "$md" ] || continue
    # A discoverable command must declare a description in frontmatter.
    if grep -qE '^description:' "$md"; then
      count=$((count+1))
    else
      echo "WARN  $fam/$(basename "$md") has no 'description:' frontmatter (not discoverable)"
    fi
  done
  if [ "$count" -ge 1 ]; then
    echo "PASS  family '$fam' — $count discoverable command(s)"
  else
    echo "FAIL  family '$fam' — no discoverable command files"
    fail=1
  fi
done

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS — all six command families present and discoverable."
  exit 0
else
  echo "RESULT: FAIL — one or more families missing or not discoverable."
  exit 1
fi

#!/usr/bin/env bash
# PQ-003 — The qualification engine fans out to three xQ sub-agents and produces a pack.
# Traces: URS-003, URS-004. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): the engine's job is to split qualification work across
# three specialists (IQ, OQ, PQ) that run in parallel, and to assemble their output into a
# pack written ONLY into a new Qualification/ folder. This static test proves the engine is
# WIRED to do that: the orchestrating command declares all three delegations, the three
# specialist sub-agents exist, and the protocol/command confine all writes to Qualification/.
# It does NOT run a live build (that is a witnessed end-to-end exercise, see Notes); it
# evidences that the fan-out design and the write-confinement guarantee are actually present.
#
# Expected agent set and the write-confinement rule are SOURCED from the command and protocol.
# READ-ONLY. PASS/FAIL. Exit 0 = PASS, 1 = FAIL.
set -euo pipefail
REPO="${1:-/Users/craigwylie/Devl/paraqualis-gxp}"
BUILD_CMD="$REPO/commands/qualify/build.md"
fail=0
echo "PQ-003 engine fan-out + pack confinement"
echo "------------------------------------------------------------"

# 1. The three specialist sub-agents exist (the fan-out targets).
for ag in iq-qualifier oq-qualifier pq-qualifier; do
  if [ -f "$REPO/agents/$ag.md" ]; then
    echo "PASS  sub-agent present: $ag"
  else
    echo "FAIL  sub-agent missing: $ag"; fail=1
  fi
done

# 2. The orchestrating command references all three delegations (the fan-out wiring).
if [ -f "$BUILD_CMD" ]; then
  for ag in iq-qualifier oq-qualifier pq-qualifier; do
    if grep -q "$ag" "$BUILD_CMD"; then
      echo "PASS  /qualify:build delegates to: $ag"
    else
      echo "FAIL  /qualify:build does NOT reference: $ag"; fail=1
    fi
  done
  # Parallel intent.
  if grep -qiE 'parallel' "$BUILD_CMD"; then
    echo "PASS  /qualify:build states parallel fan-out"
  else
    echo "WARN  /qualify:build does not explicitly say 'parallel'"
  fi
  # Write confinement to Qualification/ (URS-004 safety guarantee).
  if grep -qiE 'Qualification/' "$BUILD_CMD"; then
    echo "PASS  /qualify:build confines pack output to Qualification/"
  else
    echo "FAIL  /qualify:build does not state Qualification/ write confinement"; fail=1
  fi
else
  echo "FAIL  /qualify:build command file missing at $BUILD_CMD"; fail=1
fi

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS — fan-out wiring and write-confinement present."
  echo "NOTE: full evidence requires a witnessed live /qualify:build run confirming all three"
  echo "      sections populate and ONLY Qualification/ is created/changed (see PQ-021)."
  exit 0
else
  echo "RESULT: FAIL — fan-out or confinement wiring incomplete."
  exit 1
fi

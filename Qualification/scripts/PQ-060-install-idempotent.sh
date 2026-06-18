#!/usr/bin/env bash
# PQ-060 — The installer is idempotent: running it twice yields the same correct link set.
# Traces: URS-060. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): installing the toolkit must be safely repeatable — running
# install.sh again must not error, must not duplicate or clobber, and must leave exactly the
# same set of symlinks. This test runs the REAL install.sh against a SANDBOX Claude home
# (CLAUDE_HOME pointed at a temp dir), captures the resulting links, runs it a SECOND time,
# and asserts the link set is byte-for-byte identical and the second run exits cleanly. The
# real ~/.claude is never touched.
#
# What a "correct link set" is comes from the repo itself (one link per command family / skill /
# agent) — SOURCED from install.sh:55-57. PASS/FAIL. Exit 0 = PASS, 1 = FAIL.
set -uo pipefail
REPO="${1:-/Users/craigwylie/Devl/paraqualis-skills}"
INSTALL="$REPO/install.sh"

echo "PQ-060 installer idempotency"
echo "------------------------------------------------------------"
[ -f "$INSTALL" ] || { echo "FAIL  install.sh not found at $INSTALL"; exit 1; }

sandbox="$(mktemp -d)"
trap 'rm -rf "$sandbox"' EXIT
export CLAUDE_HOME="$sandbox/.claude"

snapshot() {
  # List every entry under the sandbox with its symlink target, sorted — the canonical state.
  if [ -d "$CLAUDE_HOME" ]; then
    find "$CLAUDE_HOME" -mindepth 1 -maxdepth 2 \( -type l -o -type f -o -type d \) \
      -exec sh -c 'for p; do printf "%s -> %s\n" "$p" "$(readlink "$p" 2>/dev/null || echo DIR/FILE)"; done' _ {} + \
      | sed "s|$sandbox||g" | sort
  fi
}

fail=0

echo "first install run..."
if ! out1="$(bash "$INSTALL" 2>&1)"; then
  echo "FAIL  first install.sh run errored:"; echo "$out1"; exit 1
fi
state1="$(snapshot)"

echo "second install run (must be idempotent)..."
if ! out2="$(bash "$INSTALL" 2>&1)"; then
  echo "FAIL  second install.sh run errored:"; echo "$out2"; exit 1
fi
state2="$(snapshot)"

# 1. Second run exits cleanly (already checked) — report.
echo "PASS  both runs exited 0"

# 2. State identical between runs.
if [ "$state1" = "$state2" ]; then
  echo "PASS  link set identical after the second run (idempotent)"
else
  echo "FAIL  link set differed between runs:"
  diff <(printf '%s\n' "$state1") <(printf '%s\n' "$state2") || true
  fail=1
fi

# 3. Expected link set is present: one link per command family, skill, agent in the repo.
expect_present() {
  local src="$1" dest="$2" label="$3"
  [ -d "$REPO/$src" ] || return 0
  for entry in "$REPO/$src"/*; do
    [ -e "$entry" ] || continue
    local name; name="$(basename "$entry")"
    if [ -L "$CLAUDE_HOME/$dest/$name" ]; then
      :
    else
      echo "FAIL  expected $label link missing: $dest/$name"
      fail=1
    fi
  done
}
expect_present commands commands "command-family"
expect_present skills   skills   "skill"
expect_present agents   agents   "agent"
[ "$fail" -eq 0 ] && echo "PASS  every repo command-family / skill / agent is linked"

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS — installer is idempotent and produces the correct link set."
  exit 0
fi
echo "RESULT: FAIL — installer not idempotent or link set incorrect."
exit 1

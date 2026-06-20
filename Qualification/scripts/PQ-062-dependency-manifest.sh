#!/usr/bin/env bash
# PQ-062 — Python tooling declares its third-party dependencies with version constraints.
# Traces: URS-062. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): the Python tools import third-party libraries
# (python-docx, openpyxl, mcp). Without a dependency manifest that pins versions, a later
# rebuild can pull different library versions than the validated build — breaking
# reproducibility of a validated system. This test checks whether a manifest exists that
# (a) is present and (b) names the libraries the code actually imports, with version
# constraints.
#
# Outcome expectation (honest): the URS itself records that NO manifest exists yet
# (URS.md:93, :114). This test is therefore expected to record a controlled FAIL / NOT-MET
# feeding gap GPQ-005 — it is NOT skipped and NOT inflated to a pass.
#
# The required libraries are SOURCED from the import lines of the shipped code:
#   mcp-servers/openfda/server.py:21 (mcp), Qualification/build_docx.py:14-18 (docx),
#   Qualification/build_xlsx.py:11-12 (openpyxl).
# PASS/FAIL. Exit 0 = PASS, 1 = FAIL (not-met).
set -uo pipefail
REPO="${1:-/Users/craigwylie/Devl/paraqualis-gxp}"
cd "$REPO" || { echo "FAIL  cannot cd to $REPO"; exit 1; }

echo "PQ-062 dependency manifest with version constraints"
echo "------------------------------------------------------------"

# Required runtime libraries the code imports (the manifest must cover these).
REQUIRED_LIBS=(docx openpyxl mcp)   # import names; PyPI: python-docx, openpyxl, mcp

# Look for any standard Python dependency manifest in the repo.
manifests=()
for cand in requirements.txt pyproject.toml setup.py setup.cfg Pipfile poetry.lock environment.yml; do
  [ -f "$cand" ] && manifests+=("$cand")
done
# Also any nested requirements*.txt (excluding the .git dir).
while IFS= read -r m; do manifests+=("$m"); done < <(find . -path ./.git -prune -o -name 'requirements*.txt' -print 2>/dev/null)

if [ "${#manifests[@]}" -eq 0 ]; then
  echo "FAIL  no dependency manifest found anywhere in the repo"
  echo "      code imports: ${REQUIRED_LIBS[*]} (python-docx, openpyxl, mcp) — all undeclared"
  echo "------------------------------------------------------------"
  echo "RESULT: FAIL (control NOT MET) — feeds gap GPQ-005."
  echo "        This is a real recorded FAIL, not a skip and not a pass."
  exit 1
fi

echo "manifest(s) found: ${manifests[*]}"
fail=0
blob="$(cat "${manifests[@]}" 2>/dev/null)"
# Map import name -> expected manifest token. (Plain case, not an associative array,
# so this runs on the macOS system bash 3.2 which lacks `declare -A`.)
for lib in "${REQUIRED_LIBS[@]}"; do
  case "$lib" in
    docx) pkg="python-docx" ;;
    *)    pkg="$lib" ;;
  esac
  if echo "$blob" | grep -qiE "$pkg"; then
    # Check for a version constraint near it.
    if echo "$blob" | grep -iE "$pkg" | grep -qE '[=<>~!]=?|\bversion\b'; then
      echo "PASS  $pkg declared WITH a version constraint"
    else
      echo "FAIL  $pkg declared but WITHOUT a version constraint"
      fail=1
    fi
  else
    echo "FAIL  required library not declared in any manifest: $pkg"
    fail=1
  fi
done

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS — all imported libraries are declared with version constraints."
  exit 0
fi
echo "RESULT: FAIL (control NOT MET) — feeds gap GPQ-005."
exit 1

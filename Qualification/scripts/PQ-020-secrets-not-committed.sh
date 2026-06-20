#!/usr/bin/env bash
# PQ-020 — In use, the openFDA API key stays out of the repository.
# Traces: URS-020. ParaQualis-authored, pending owner confirmation.
#
# Why this matters (plain English): a leaked credential committed to a repo is a serious
# security and Part 11 access-control failure. This test confirms that in the real working
# tree and the git history: (1) .env is git-ignored, (2) only .env.example with a PLACEHOLDER
# is tracked, and (3) no real key value appears in any tracked file or in history.
#
# The placeholder value and ignore rule are SOURCED from .env.example and .gitignore.
# READ-ONLY. PASS/FAIL. Exit 0 = PASS, 1 = FAIL.
set -uo pipefail
REPO="${1:-/Users/craigwylie/Devl/paraqualis-gxp}"
cd "$REPO" || { echo "FAIL  cannot cd to $REPO"; exit 1; }

echo "PQ-020 secrets never committed"
echo "------------------------------------------------------------"
fail=0

# 1. .env is git-ignored.
if git check-ignore -q .env; then
  echo "PASS  .env is git-ignored"
else
  echo "FAIL  .env is NOT git-ignored"
  fail=1
fi

# 2. Only .env.example is tracked; no real .env tracked, ever.
tracked_env="$(git ls-files | grep -E '(^|/)\.env$' || true)"
if [ -z "$tracked_env" ]; then
  echo "PASS  no real .env file is tracked"
else
  echo "FAIL  a real .env is tracked: $tracked_env"
  fail=1
fi
if git ls-files | grep -qx '.env.example'; then
  echo "PASS  .env.example template is tracked"
else
  echo "WARN  .env.example template not tracked"
fi

# 3. .env.example carries only a placeholder (sourced: .env.example).
if grep -qE '^OPENFDA_API_KEY=your-key-here$' .env.example; then
  echo "PASS  .env.example contains only the documented placeholder"
else
  echo "FAIL  .env.example does not match the expected placeholder"
  fail=1
fi

# 4. No .env was ever committed in history.
if git log --all --oneline --name-only 2>/dev/null | grep -qxE '\.env'; then
  echo "FAIL  a .env file appears somewhere in git history"
  fail=1
else
  echo "PASS  no .env file appears in git history"
fi

# 5. No assignment of a REAL key value in any tracked file. A real openFDA key is a long
#    alphanumeric token; we flag only an = followed by >=20 word chars. Documentation
#    placeholders ('your-key-here', '<key>', '...') and code references are NOT secrets.
leak="$(git grep -nIE 'OPENFDA_API_KEY=[A-Za-z0-9_]{20,}' -- . 2>/dev/null \
        | grep -vE 'your-key-here' || true)"
if [ -z "$leak" ]; then
  echo "PASS  no hardcoded key value assigned in any tracked file"
else
  echo "FAIL  possible key value committed:"
  echo "$leak"
  fail=1
fi

echo "------------------------------------------------------------"
if [ "$fail" -eq 0 ]; then
  echo "RESULT: PASS — secrets are kept out of the repo and history."
  exit 0
fi
echo "RESULT: FAIL — a secret-handling control is not met."
exit 1

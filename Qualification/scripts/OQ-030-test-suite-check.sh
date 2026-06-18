#!/usr/bin/env bash
# OQ-030 — Verify an automated test suite exists and can be executed.
# PASS: pytest finds tests, runs them, all pass.
# FAIL (expected per this assessment): no test suite found.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"

if [ ! -d "$REPO/tests" ]; then
    echo "FAIL: no tests/ directory found — no automated test suite (GOQ-004)"
    exit 1
fi

if ! python3 -m pytest --version 2>/dev/null; then
    echo "FAIL: pytest not installed"
    exit 1
fi

python3 -m pytest "$REPO/tests/" -v --tb=short

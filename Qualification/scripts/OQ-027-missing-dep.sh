#!/usr/bin/env bash
# OQ-027 — Verify missing dependencies fail loud (ModuleNotFoundError, not silent).
# Tests openpyxl and mcp. python-docx tested separately (installed).
# PASS: each absent library produces ModuleNotFoundError with non-zero exit.
set -euo pipefail
all_pass=true

for lib in openpyxl mcp; do
    err=$(python3 -c "import $lib" 2>&1)
    code=$?
    if [ $code -ne 0 ] && echo "$err" | grep -q "No module named"; then
        echo "PASS: missing '$lib' -> ModuleNotFoundError (fails loud)"
    elif [ $code -eq 0 ]; then
        echo "INFO: '$lib' IS installed — skip absent-library test for this library"
    else
        echo "FAIL: '$lib' missing but error not a ModuleNotFoundError: $err"
        all_pass=false
    fi
done

$all_pass && exit 0 || exit 1

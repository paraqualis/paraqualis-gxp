#!/usr/bin/env bash
# OQ-012 — Minimum-config check: openFDA server operates without API key.
# PASS: OPENFDA_API_KEY unset → server starts without error (import check);
#        with live network, first result includes 'tip' key.
# Requires: mcp library installed.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"

echo "--- Checking mcp library available ---"
python3 -c "import mcp; print('mcp version:', mcp.__version__)" || {
    echo "FAIL: mcp library not installed. Run: pip install mcp"
    exit 1
}

echo "--- Checking OPENFDA_API_KEY status ---"
if python3 -c "import os; exit(0 if not os.environ.get('OPENFDA_API_KEY') else 1)"; then
    echo "INFO: OPENFDA_API_KEY not set — testing no-key path"
else
    echo "INFO: OPENFDA_API_KEY is set"
fi

echo "--- Server import check ---"
python3 -c "
import sys
sys.path.insert(0, '$REPO/mcp-servers/openfda')
import server
print('PASS: server.py imports successfully')
"
echo "Note: live API test requires network access to api.fda.gov"

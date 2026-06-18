#!/usr/bin/env bash
# IQ-007: Verify the openFDA MCP server is registered with Claude Code.
# Expected: 'openfda' appears in 'claude mcp list' output.
# Read-only.
set -uo pipefail
echo "IQ-007  MCP server registration check"

if ! command -v claude >/dev/null 2>&1; then
  echo "  WARNING: 'claude' CLI not found — cannot verify MCP registration"
  echo "NEEDS-HUMAN-REVIEW  Install claude CLI and re-run"
  exit 0
fi

MCP_LIST=$(claude mcp list 2>&1 || true)
echo "  claude mcp list output:"
echo "$MCP_LIST" | sed 's/^/    /'

if echo "$MCP_LIST" | grep -qi "openfda"; then
  echo "PASS  'openfda' MCP server found in Claude Code registration"
else
  echo "FAIL  'openfda' MCP server NOT found in 'claude mcp list'"
  echo "  Remediation: claude mcp add openfda --scope user -- python3 \"<repo>/mcp-servers/openfda/server.py\""
  exit 1
fi

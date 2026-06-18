#!/usr/bin/env bash
# IQ-005 / IQ-006: Verify required Python packages are installed and importable,
# and that server.py carries the python3 shebang.
# Package list sourced from import statements in the repo's Python files.
# Read-only. Emits PASS or FAIL per package.
set -uo pipefail   # NOTE: no -e — we test failing imports deliberately and check results

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
echo "IQ-005/IQ-006  Python package availability check"
echo "  Python: $(python3 --version 2>&1)"

PACKAGES=("mcp" "docx" "openpyxl")
SRC=("mcp-servers/openfda/server.py (from mcp.server.fastmcp import FastMCP)"
     "qualification-pack-template/build_docx.py (from docx import Document)"
     "qualification-pack-template/build_xlsx.py (from openpyxl import Workbook)")

FAILURES=0
for i in "${!PACKAGES[@]}"; do
  PKG="${PACKAGES[$i]}"
  if python3 -c "import ${PKG}" 2>/dev/null; then
    VER=$(python3 -c "import ${PKG}; print(getattr(${PKG}, '__version__', 'version unknown'))" 2>/dev/null || echo "version unknown")
    echo "  PASS  ${PKG} installed (${VER})  — required by: ${SRC[$i]}"
  else
    echo "  FAIL  ${PKG} NOT installed  — required by: ${SRC[$i]}"
    FAILURES=$((FAILURES + 1))
  fi
done

SERVER="$REPO_DIR/mcp-servers/openfda/server.py"
SHEBANG=$(head -1 "$SERVER")
if [ "$SHEBANG" = "#!/usr/bin/env python3" ]; then
  echo "  PASS  server.py shebang: $SHEBANG"
else
  echo "  FAIL  server.py shebang unexpected: $SHEBANG"; FAILURES=$((FAILURES + 1))
fi

[ $FAILURES -eq 0 ] && { echo "PASS  All packages installed"; exit 0; }
echo "FAIL  $FAILURES package(s) missing or shebang incorrect"
exit 1

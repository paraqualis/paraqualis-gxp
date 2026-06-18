#!/usr/bin/env bash
# IQ-014: Confirm absence of database, queue, and cache infrastructure.
# Records a positive absence finding (absence is a finding, not a skip).
# Read-only. Emits PASS (confirmed absent) or FAIL (evidence of presence found).
set -uo pipefail

REPO_DIR="${1:-$(cd "$(dirname "$0")/../.." && pwd)}"
FAILURES=0
echo "IQ-014  Database / queue / cache absence confirmation"

DB_FILES=$(find "$REPO_DIR" -not -path "*/.git/*" -not -path "*/Qualification/*" \( \
  -name "*.sql" -o -name "*.sqlite" -o -name "*.db" \
  -o -name "schema*" -o -name "migration*" -o -name "alembic.ini" \) 2>/dev/null || true)
if [ -z "$DB_FILES" ]; then echo "  OK    No SQL/schema/migration files found"
else echo "  FAIL  Unexpected DB-related files:"; echo "$DB_FILES" | sed 's/^/    /'; FAILURES=$((FAILURES+1)); fi

DB_IMPORTS=$(grep -rnE "redis|rabbitmq|kafka|celery|sqlite3|psycopg|pymysql|pymongo|sqlalchemy" \
  "$REPO_DIR" --include="*.py" 2>/dev/null | grep -v "/.git/" | grep -v "/Qualification/" || true)
if [ -z "$DB_IMPORTS" ]; then echo "  OK    No DB/broker client imports in Python sources"
else echo "  FAIL  DB/broker imports found:"; echo "$DB_IMPORTS" | sed 's/^/    /'; FAILURES=$((FAILURES+1)); fi

COMPOSE=$(find "$REPO_DIR" -not -path "*/.git/*" \( -name "docker-compose*.yml" -o -name "Dockerfile" -o -name "*.tf" \) 2>/dev/null || true)
[ -n "$COMPOSE" ] && { echo "  INFO  Infra files found (inspect for DB services):"; echo "$COMPOSE" | sed 's/^/    /'; }

[ $FAILURES -eq 0 ] && { echo "PASS  No database, queue, or cache detected — confirmed absent"; exit 0; }
echo "FAIL  Unexpected infrastructure found — requires human review"
exit 1

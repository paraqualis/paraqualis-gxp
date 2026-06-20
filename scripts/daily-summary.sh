#!/usr/bin/env bash
# Last-24h digest for paraqualis-skills.
# Wired as a SessionStart hook (see .claude/settings.local.json) so it prints
# when you start the day, and runnable by hand: ./scripts/daily-summary.sh
#
# Reads the committed stats files (refreshed by the tracker workflows), so it
# is fast and works offline — no network or auth required.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "📊 paraqualis-skills — last 24h digest"
echo "────────────────────────────────────"

# Marketplace listing status
if [ -f stats/community-marketplace-status.json ]; then
  python3 - <<'PY'
import json
try:
    s = json.load(open('stats/community-marketplace-status.json'))
    found = s.get('found')
    print(f"Marketplace: {'✅ LISTED' if found else '⏳ not yet in catalog'} "
          f"(checked {s.get('last_checked_at','?')}, catalog {s.get('total_plugins_in_catalog','?')} plugins)")
    if found and s.get('first_detected_at'):
        print(f"  first detected: {s['first_detected_at']}")
except Exception as e:
    print(f"Marketplace: (status unavailable: {e})")
PY
fi

# Traffic — latest recorded day
if [ -f stats/traffic.csv ]; then
  python3 - <<'PY'
import csv
rows = list(csv.DictReader(open('stats/traffic.csv')))
if rows:
    r = rows[-1]
    print(f"Traffic ({r['date']}): {r['clones_count']} clones / {r['clones_uniques']} unique cloners; "
          f"views {r['views_count']} (views are structurally 0 — this repo is clone-driven)")
PY
fi

# Commits in the last 24h, excluding the automated tracker refreshes
echo "Commits (last 24h):"
log=$(git log --since='24 hours ago' --format='  %h %s' 2>/dev/null | grep -v 'tracker: refresh' || true)
if [ -n "$log" ]; then echo "$log"; else echo "  (none beyond automated tracker refreshes)"; fi

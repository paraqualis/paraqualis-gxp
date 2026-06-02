# stats/

Auto-maintained by the GitHub Actions in `.github/workflows/`. Do not hand-edit —
the bots will overwrite you. No personal data lives here; counts only.

| File | Maintained by | What it records |
|---|---|---|
| `traffic.csv` | `traffic-logger.yml` (runs daily 02:00 UTC) | Daily clone and view counts (total + unique) — GitHub's Traffic API only retains 14 days, this gives us a permanent record. |
| `community-marketplace-status.json` | `community-marketplace-tracker.yml` (runs daily 09:00 UTC) | Whether `paraqualis-skills` is currently listed in [Anthropic's community marketplace](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json), and when it was first detected. The tracker opens a `🎉` issue the first time it sees us listed; quiet thereafter. |

To run either workflow on demand: GitHub → Actions → pick the workflow → "Run workflow".

# stats/

Auto-maintained by the GitHub Actions in `.github/workflows/`. Do not hand-edit —
the bots will overwrite you. No personal data lives here; counts only.

| File | Maintained by | What it records |
|---|---|---|
| `traffic.csv` | `traffic-logger.yml` (runs daily 02:00 UTC) | Daily clone and view counts (total + unique) — GitHub's Traffic API only retains 14 days, this gives us a permanent record. |
| `community-marketplace-status.json` | `community-marketplace-tracker.yml` (runs daily 09:00 UTC) | Whether `paraqualis-gxp` is currently listed in [Anthropic's community marketplace](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json), and when it was first detected. The tracker opens a `🎉` issue the first time it sees us listed; quiet thereafter. |

To run either workflow on demand: GitHub → Actions → pick the workflow → "Run workflow".

## One-time setup for the traffic logger

GitHub's Traffic API requires `Administration: Read` permission, which the
default `GITHUB_TOKEN` issued to workflows cannot grant. The traffic-logger
therefore needs a fine-grained Personal Access Token (PAT), stored as a repo
secret called **`TRAFFIC_TOKEN`**. Five minutes, one-time:

1. **Create the PAT** at
   <https://github.com/settings/personal-access-tokens/new>
   - Token name: `paraqualis-gxp-traffic`
   - Expiration: 1 year (or whatever cadence works for you)
   - Repository access → **Only select repositories** → `paraqualis/paraqualis-gxp`
   - Permissions → Repository permissions → **Administration: Read-only**
     *(Leave everything else as "No access".)*
   - Click **Generate token**, copy the value (shown only once).
2. **Add the secret** at
   <https://github.com/paraqualis/paraqualis-gxp/settings/secrets/actions>
   - Click **New repository secret**.
   - Name: `TRAFFIC_TOKEN`
   - Secret: paste the PAT.
   - Click **Add secret**.
3. **Re-run the traffic-logger** workflow (Actions → Traffic logger → Run workflow).

The community-marketplace-tracker does **not** need this — it just curls
the public catalog JSON.

# Privacy Policy — ParaQualis Skills

*Effective date: 2026-05-31. Last updated: 2026-05-31.*
*Copyright © 2026 ParaQualis LLC · MIT licensed.*

## Summary

**ParaQualis LLC does not collect, store, transmit, or process any personal
data through the `paraqualis-skills` plugin.** The plugin is open-source
software that runs **entirely on your machine** inside Claude Code. We
operate no server, no analytics, no telemetry, and no account system.

If you never set an openFDA API key and never run a command that fetches
external data, the plugin performs no network communication at all.

## Who this policy applies to

This policy covers the **`paraqualis-skills` plugin software**, distributed
from `github.com/paraqualis/paraqualis-skills`. It does not cover:

- Anthropic's Claude Code itself — governed by [Anthropic's privacy policy](https://www.anthropic.com/legal/privacy).
- GitHub, which hosts the source and is touched by Claude Code when it
  clones or updates the plugin — governed by [GitHub's privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
- Any other Claude Code plugin you install alongside this one.

## What the plugin does locally on your machine

When you invoke a command, skill, or sub-agent, the plugin may:

- **Read files in the project you are working on** (so the qualification
  engine can examine your codebase and configuration).
- **Write a `Qualification/` directory inside that project** — Markdown,
  branded Word, Excel, and accompanying scripts and records.
- **Read environment variables** you have set (notably `OPENFDA_API_KEY`,
  if present, so the openFDA MCP server can pass it to the FDA's API).

All of the above happens on your machine. None of it is sent to
ParaQualis LLC.

## Third-party services the plugin may contact

The following endpoints are reached **only when you explicitly invoke a
command or tool that requires them**. We don't proxy any of these — your
machine talks to them directly.

| Endpoint | When | What is sent | Governed by |
|---|---|---|---|
| `api.fda.gov` (openFDA) | You invoke an openFDA MCP tool | Your search query and, if set, `OPENFDA_API_KEY` | [openFDA terms](https://open.fda.gov/terms/) |
| `ecfr.gov/api` | You run an `/eCFR:*` command | A CFR Title/Part/Section reference. No auth, no key. | NARA / GPO public-data terms |
| `raw.githubusercontent.com` / `github.com` | Claude Code clones or updates the plugin | A standard Git request | [GitHub privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement) |

The plugin does not log, cache, or relay the content of these requests
back to ParaQualis LLC.

## What we do not do

- We do not run any backend service for the plugin.
- We do not collect analytics or telemetry of any kind.
- We do not collect IP addresses, device identifiers, usage statistics,
  or crash reports.
- We do not use cookies or any client-side trackers (the plugin has no
  web surface).
- We do not sell, share, or disclose data — because we have none.

## Children

The plugin is not directed at children under 13 (or 16 in jurisdictions
where that is the applicable threshold). We do not knowingly collect any
data, including from children.

## Data-subject rights (GDPR, CCPA, and similar)

Because ParaQualis LLC does not collect personal data through this plugin,
there is no personal data we hold that you could request access to, ask us
to delete, or ask us to port. If you believe this is inaccurate in your
case, contact us at the address below.

## Changes to this policy

Material changes will be made by committing an updated version of this
file to the public repository, with a new effective date and a summary in
[CHANGELOG.md](CHANGELOG.md). The full revision history is available in
the repository's Git log.

## Contact

ParaQualis LLC — Connecticut, United States.
Privacy inquiries: `privacy@paraqualis.com` (subject line: "paraqualis-skills privacy").
For security issues, see [SECURITY.md](SECURITY.md) — `security@paraqualis.com`.

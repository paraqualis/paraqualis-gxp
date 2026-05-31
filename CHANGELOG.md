# Changelog

All notable changes to **paraqualis-skills** are documented here.
This project follows [Semantic Versioning](https://semver.org/) and the
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

*Copyright © 2026 ParaQualis LLC · MIT licensed.*

## [1.0.0] — 2026-05-31

First public release. The toolkit is packaged as a Claude Code plugin and is
installable via the bundled marketplace (`/plugin marketplace add DeepJam/paraqualis-skills`
then `/plugin install paraqualis-skills@paraqualis`).

### Added — slash commands (16, across 5 families)

- **`/gamp:assess`** — categorize a system against GAMP 5 (2nd ed.) and recommend proportionate validation rigor.
- **`/gamp:testplan`** — draft a risk-based GAMP 5 IQ/OQ/PQ test plan, scaled to category and risk.
- **`/cfr21-11:gap`** — gap-assess a system against 21 CFR Part 11 with severity and remediation.
- **`/cfr21-11:checklist`** — tailored Part 11 controls checklist.
- **`/cfr21-11:auditprep`** — FDA inspection-readiness package.
- **`/eu-annex11:gap`** — gap-assess against EU GMP Annex 11 by clause.
- **`/eu-annex11:checklist`** — Annex 11 controls checklist.
- **`/eu-annex11:auditprep`** — EU GMP inspection-readiness.
- **`/eu-annex11:crosswalk`** — map Annex 11 to 21 CFR Part 11.
- **`/eCFR:structure`** — show the heading-only structure of any CFR reference, two levels deep.
- **`/eCFR:text`** — fetch the current regulatory text of a section/part.
- **`/eCFR:search`** — full-text search the eCFR.
- **`/eCFR:changes`** — amendment history of a CFR part.
- **`/eCFR:compare`** — show wording changes between two dates.
- **`/openfda:setup`** — detect or provision a free openFDA API key.
- **`/qualify`** — orchestrator that fans out to the IQ/OQ/PQ sub-agents in parallel and assembles a qualification pack.

### Added — auto-invoked skills (2)

- **`part11-advisor`** — always-available 21 CFR Part 11 expertise, reasoning against the bundled verbatim regulation text.
- **`gamp-advisor`** — always-available GAMP 5 (2nd ed.) expertise including AI/ML and GenAI validation (per the ISPE GAMP Guide: Artificial Intelligence, July 2025, and EU draft Annex 22).

### Added — parallel sub-agents (3)

- **`iq-qualifier`** — Installation Qualification specialist.
- **`oq-qualifier`** — Operational Qualification specialist.
- **`pq-qualifier`** — Performance Qualification specialist.

All three are delegated by `/qualify`, run in parallel in isolated contexts, and produce evidence under the **[xQ Qualification Protocol](docs/xq-qualification-protocol.md)** (requirement + executable test + acceptance criteria + execution record; stage-prefixed `GIQ/GOQ/GPQ-NNN` gap IDs; regulatory traceability matrix; three-layer evidence model for AI/ML systems).

### Added — hooks (1)

- **`protect-approved-documents`** — `PreToolUse` hook that blocks any edit to a file carrying the marker `<!-- PARAQUALIS-LOCK: approved -->`. Wired automatically via `hooks/hooks.json` when installed as a plugin.

### Added — MCP server (opt-in)

- **`mcp-servers/openfda/`** — exposes FDA open data (recalls, drug labels, adverse events) as Claude-callable tools. Opt-in because it needs `pip install mcp`; register with `claude mcp add openfda --scope user -- python3 <path>/server.py`. When the `OPENFDA_API_KEY` environment variable is missing, the server now:
  - Surfaces a single non-intrusive tip on the first successful call (pointing to `/openfda:setup`).
  - Returns a clear setup-pointer message on HTTP 429 (rate-limit hit).
  - Returns a "quota resets midnight UTC" message on 429 when a key is set.

### Added — documentation

- **`docs/OVERVIEW.md`** (+ branded Word) — the whole toolkit at a glance with an auto-generated catalog.
- **`docs/how-to-qualify.md`** (+ Word) — end-to-end guide for running `/qualify` on any application.
- **`docs/xq-qualification-protocol.md`** (+ Word) — the abstraction behind `/qualify` (test cases, scripts, gap register, formats).
- A pre-commit git hook (`.githooks/pre-commit`) refreshes the OVERVIEW catalog automatically on every commit.

### Added — distribution

- **`.claude-plugin/plugin.json`** + **`marketplace.json`** — plugin manifest and a single-plugin marketplace, so the whole toolkit installs in one command.
- **`LICENSE`** — MIT. Copyright © 2026 ParaQualis LLC.
- **`SECURITY.md`** — vulnerability reporting policy.

### Principles

The toolkit holds to: **plain English always**; **no stack assumptions** (the qualifier discovers languages, runtimes, and databases — zero, one, or many — rather than assuming them); **expected values are sourced** from the spec or the system's own declarations, not invented; **honest evidence** (a skipped test is not a pass; errors are never swallowed silently); **markdown is the source of truth** — Word and Excel are generated, never hand-edited.

[1.0.0]: https://github.com/DeepJam/paraqualis-skills/releases/tag/v1.0.0

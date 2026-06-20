# Changelog

All notable changes to **paraqualis-gxp** are documented here.
This project follows [Semantic Versioning](https://semver.org/) and the
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.

*Copyright © 2026 ParaQualis LLC · MIT licensed.*

## [1.2.0] — 2026-06-18

### Changed

- **Plugin renamed** — the installable plugin id is now **`paraqualis-gxp`** (was
  `paraqualis-gxp`), reflecting the toolkit's full GxP/CSV scope rather than just Part 11.
  Install with `/plugin install paraqualis-gxp@paraqualis`. The GitHub repository and the
  `paraqualis` marketplace are unchanged.
- `server_version()` now reads the plugin name and version from `plugin.json` (single source of truth).

## [1.1.0] — 2026-06-17

### Changed — `/qualify` split into the `qualify:` command family

The single `/qualify` command conflated three distinct jobs (generate, verify, and the
implicit requirements obligation) behind one mode-detecting entry point. It is now three
focused commands:

- **`/qualify:build`** — the generate path. Discovers the stack, database schema(s),
  required seed data, and the approved requirements, then fans out to the IQ/OQ/PQ
  sub-agents in parallel and assembles the pack. When no approved requirements document
  exists it still completes IQ, OQ, and partial PQ, raises a critical finding, and offers
  to author a draft URS inline.
- **`/qualify:requirements`** — new. Authors a draft **User Requirements Specification
  (URS)** to `Qualification/requirements/URS.md` when none exists — discharging the
  regulatory obligation to define requirements (GAMP 5 lifecycle; EU Annex 11 cl.4),
  structured so each requirement is testable and traces to a PQ test-case.
- **`/qualify:review`** — the verify path, refocused. Reports what is complete and what is
  outstanding, detects drift against the current system, and produces a gap-closure plan
  split into AI-closable vs. human/witnessed.

Slash-command count is now **18**. The three IQ/OQ/PQ sub-agents are unchanged (shared by
`/qualify:build` in generate mode and `/qualify:review` in verify mode). Docs, README,
the catalog, and the plugin/marketplace manifests updated to match.

### Added — packaging, MCP bundling, logging, and a runtime version surface

- **Dependency manifest** — `requirements.txt` pins `python-docx`, `openpyxl`, and `mcp`, and
  declares Python ≥ 3.10. Pre-flight checks in `build_docx.py`, `build_xlsx.py`, and the
  openFDA server now **fail loud** with install guidance when a dependency (or a new-enough
  Python) is missing — nothing runs silently against a missing dependency.
- **openFDA MCP server bundled in the plugin** — declared in `plugin.json` → `mcpServers`
  (`${CLAUDE_PLUGIN_ROOT}`), so installing the plugin registers it.
- **Server-side logging** — the openFDA server and the document-protection hook log failures
  and fail-open decisions to stderr (21 CFR Part 11 §11.10(e); EU GMP Annex 11 cl.9).
- **`server_version()` MCP tool** — returns the running plugin version + Python runtime.
- **`docs/minimum-configuration.md`** — one page of prerequisites and how to satisfy each.
- **Self-qualification pack** — a DRAFT IQ/OQ/PQ qualification package for the toolkit itself
  under `Qualification/`, plus `PUBLISHING.md` (marketplace publication guide).

### Fixed

- `hooks/README.md` reconciled to document plugin / in-repo / manual hook registration
  consistently (a hard-coded absolute path previously conflicted with the
  `${CLAUDE_PLUGIN_ROOT}` form in `hooks/hooks.json`).

## [1.0.0] — 2026-05-31

First public release. The toolkit is packaged as a Claude Code plugin and is
installable via the bundled marketplace (`/plugin marketplace add paraqualis/paraqualis-gxp`
then `/plugin install paraqualis-gxp@paraqualis`).

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

[1.0.0]: https://github.com/paraqualis/paraqualis-gxp/releases/tag/v1.0.0

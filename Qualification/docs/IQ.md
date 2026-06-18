# Installation Qualification (IQ) — paraqualis-skills v1.2.0

**DRAFT — pending review and approval by appropriately qualified and authorized personnel.**

## IQ Readiness Verdict

Installation evidence is **partially adequate**: the Claude Code plugin structure, symlinks,
command/skill/agent frontmatter, reference corpora, and git-hook path are all correctly
installed and verified. The dependency gaps have since been **resolved** (2026-06-17): a pinned `requirements.txt`
was added, Python 3.12 was installed, and a project virtual environment (`.venv`) now provides
`python-docx==1.2.0`, `openpyxl==3.1.5` and `mcp==1.28.0` — the openFDA server loads under it.
Remediation on 2026-06-17 **closed** those: the openFDA server is registered (✔ Connected)
and bundled in `plugin.json` → `mcpServers` (GIQ-004); a `server_version()` tool surfaces the
version (GIQ-006); and `server.py` and the hook now log to stderr (GIQ-007). The hook is
auto-registered for plugin installs via `hooks/hooks.json` (GIQ-005); the only residual on
this dev box is the opt-in in-repo hook registration (IQ-009). No database, queue, or cache exists (confirmed
by inspection — a valid finding, not a skip).

## 1. Component Inventory

| Component | Expected / Spec | Found (evidence) | Status |
|---|---|---|---|
| **Plugin manifest** (`plugin.json`) | `name`, `version`, `description`, `author` present; valid JSON | All four present; `version = "1.2.0"`; valid JSON (`.claude-plugin/plugin.json:1-17`) | Verified |
| **Marketplace manifest** (`marketplace.json`) | Valid JSON; plugin entry referencing GitHub source | Present and valid (`.claude-plugin/marketplace.json:1-18`) | Verified |
| **Command families** (6) | cfr21-11(3), eCFR(5), eu-annex11(4), gamp(2), openfda(1), qualify(3) = 18 `.md`, each with valid frontmatter + `description` | 18 files across 6 families confirmed | Verified |
| **Sub-agents** (3) | `agents/{iq,oq,pq}-qualifier.md` with `name`/`description`/`tools`/`model` | All present, fields confirmed (`agents/*.md:1-10`) | Verified |
| **Skills** (2) | `skills/{gamp-advisor,part11-advisor}/SKILL.md` + `reference/` corpus | Present; corpora non-empty (see §2) | Verified |
| **Installer** (`install.sh`) | Executable; idempotent symlinking with stale-link pruning | Present, executable; idempotent logic (`install.sh:1-66`) | Verified |
| **Symlinks** | 6 commands + 2 skills + 3 agents in `~/.claude/`, resolving to repo | All 11 present and resolving | Verified |
| **Git hook** | `.githooks/pre-commit` executable; `core.hooksPath = .githooks` | Hook executable; hooksPath confirmed | Verified |
| **Doc-protection hook registration** | Active on install | Plugin: auto via `hooks/hooks.json`; in-repo dev: opt-in `.claude/settings.json` | Closed for plugin (GIQ-005); dev opt-in |
| **MCP server source** | `server.py` present, `python3` shebang, `FastMCP` importable | File + shebang OK (`mcp-servers/openfda/server.py:1-171`) | Verified (import blocked — see below) |
| **MCP server registration** | `openfda` callable | Declared in `plugin.json` mcpServers; registered locally (venv) — ✔ Connected | Verified (GIQ-004 closed) |
| **Python runtime** | Python ≥3.10 (declared); project venv | Python 3.12.13 in `.venv`; min declared in `requirements.txt` | Verified (GIQ-003 closed) |
| **Package `mcp`** | Required by `server.py` (Python ≥3.10) | Installed 1.28.0 in `.venv` | Verified (GIQ-002 closed) |
| **Package `python-docx`** | Required by `build_docx.py` | Installed 1.2.0; pinned in `requirements.txt` | Verified |
| **Package `openpyxl`** | Required by `build_xlsx.py` | Installed 3.1.5; pinned | Verified |
| **Dependency manifest** | requirements.txt / pyproject / lockfile | `requirements.txt` present; all three pinned (`==`) | Verified (GIQ-001 closed) |
| **Config `.env.example`** | Template present; `OPENFDA_API_KEY` documented | Present (`.env.example`); key optional | Verified |
| **CI workflows** | community-marketplace-tracker; traffic-logger | Both present (`.github/workflows/`) | Verified (TRAFFIC_TOKEN not statically checkable) |
| **Runtime version surface** | Deployed version queryable at runtime | `server_version()` MCP tool → 1.2.0 / py 3.12.13 | Verified (GIQ-006 closed) |
| **Server-side logging** | Errors surfaced to a server log, not only to caller | `logging`→stderr in `server.py` (every except) + hook (fail-open/block) | Verified (GIQ-007 closed) |
| **Database / queue / cache** | None declared or expected | None found — confirmed absent | Confirmed absent (valid finding) |

## 2. Schema and Data Readiness

There is no database in this system — it is a stateless, file-based Claude Code plugin. No
relational/document/graph store or cache was found; this absence is a deliberate design
choice, so no schema or migration verification applies.

**Reference / seed corpora** (data required for accurate regulatory advice):

| Corpus file | Required by | Status |
|---|---|---|
| `skills/gamp-advisor/reference/gamp5-category-framework.md` | gamp-advisor | Present, non-empty (57 lines) |
| `skills/gamp-advisor/reference/ai-ml-validation.md` | gamp-advisor | Present, non-empty (65 lines) |
| `skills/part11-advisor/reference/21-cfr-part-11.md` | part11-advisor | Present, non-empty (172 lines) |

Content **accuracy/currency** of these corpora is a subject-matter-expert review item (see
Open Items), not a file-presence check.

## 3. Configuration and Environment Verification

| Item | Confirmed | Flagged |
|---|---|---|
| `OPENFDA_API_KEY` optional (server runs without it; key only raises rate limit) | `server.py:7-13`, `.env.example` | — |
| No required boot-time secrets for the core plugin | commands/skills/agents load with no config | openFDA server runs under `.venv` (3.12) |
| Hook needs `python3` on PATH | Python 3.9.6 (system) / 3.12 (`.venv`) | server must be launched with `.venv/bin/python` |
| Hook registration in `~/.claude/settings.json` | NOT confirmed (0 PreToolUse) | Manual post-install step not completed (GIQ-005) |
| `${CLAUDE_PLUGIN_ROOT}` in `hooks/hooks.json` | Injected by Claude Code at runtime | Needs live verification |

## IQ Test-cases

| ID | Requirement | Regulatory linkage | Test method | Test artifact | Acceptance criteria | Expected result | Execution record |
|---|---|---|---|---|---|---|---|
| **IQ-001** | `plugin.json` is valid JSON and declares `name`, `version`, `description`, `author` | GAMP 5 Cat.3 CM; Annex 11 cl.4 | Automated | `scripts/IQ-001-manifest-check.sh` | JSON parses; all four fields present/non-empty; `version` matches declared | PASS: all fields, `version = 1.2.0` | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-002** | All 18 slash commands exist with valid YAML frontmatter + non-empty `description` | GAMP 5 Cat.3; Annex 11 cl.4 | Automated | `scripts/IQ-002-command-structure.sh` | 18 files; each begins `---`; each has non-empty `description:` | PASS: 18 files valid | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-003** | Python deps pinned to explicit versions in a checked-in manifest | Part 11 §11.10(k); GAMP 5; Annex 11 cl.4 | Automated | `scripts/IQ-003-dependency-pins.sh` | A manifest lists `mcp`,`python-docx`,`openpyxl` pinned with `==` | PASS — `requirements.txt` pins all three | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-004** | Python runtime ≥ declared minimum | GAMP 5 infra; Annex 11 cl.3 | Automated | `scripts/IQ-004-python-version.sh` | `python3 --version` ≥ declared minimum | PASS under `.venv` (3.12 ≥ declared 3.10) | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-005** | `mcp`, `openpyxl`, `docx` installed and importable | GAMP 5 Cat.5 dep; Annex 11 cl.4 | Automated | `scripts/IQ-005-python-packages.sh` | `import` of each exits 0 | PASS under `.venv`: mcp 1.28.0, openpyxl 3.1.5, docx 1.2.0 | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-006** | MCP server present, `python3` shebang, `FastMCP` entry-point importable | GAMP 5 Cat.5; Annex 11 cl.4 | Automated | `scripts/IQ-005-python-packages.sh` | File + shebang OK; import check exits 0 | PASS under `.venv`: FastMCP importable | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-007** | openFDA MCP server registered with Claude Code | GAMP 5 infra; Annex 11 cl.4 | Manual | `scripts/IQ-007-mcp-registration.sh` | `claude mcp list` includes `openfda` | PASS — registered & ✔ Connected (venv); bundled in plugin.json | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-008** | All `install.sh` symlinks exist in `~/.claude/` and resolve to this repo | GAMP 5 Cat.3; Annex 11 cl.4 | Automated | `scripts/IQ-008-symlinks.sh` | 11 symlinks present, non-dangling, targets within repo | PASS — 11 verified | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-009** | Doc-protection hook registered as `PreToolUse` in `~/.claude/settings.json` | Part 11 §11.10(d),(e); Annex 11 cl.9,12 | Automated | `scripts/IQ-009-hook-registration.sh` | A PreToolUse entry references `protect-approved-documents.py` | FAIL — 0 PreToolUse entries | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-010** | Both skills have `SKILL.md` (name+description) and non-empty `reference/` corpora | GAMP 5 Cat.3; Annex 11 cl.4 | Automated | `scripts/IQ-010-skills-reference.sh` | 2 SKILL.md valid; 3 reference files non-empty | PASS | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-AI-011** | The 3 sub-agent files present with complete frontmatter (name/description/tools/model) | ISPE GAMP AI; EU Annex 22 cl.4 | Automated | `scripts/IQ-010-skills-reference.sh` | 3 agent files; each has description/tools/model | PASS | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-012** | git pre-commit hook executable; `core.hooksPath = .githooks` | GAMP 5 CM; Annex 11 cl.4 | Automated | `scripts/IQ-012-githook.sh` | hook executable; hooksPath = `.githooks` | PASS | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-AI-013** | Declared version (`1.2.0`) surfaced at runtime so deployed version is verifiable | Part 11 §11.10(k); GAMP 5 change control; ISPE GAMP AI | Automated + Manual | `scripts/IQ-001-manifest-check.sh` + manual | `plugin.json` version matches a runtime-queryable value | PASS — `server_version()` → 1.2.0 / 3.12.13 | Actual:·By:·Date:·P/F:·Ref: |
| **IQ-014** | No database, queue, or cache present (confirmed absence, not assumption) | GAMP 5 infra scoping; Annex 11 cl.4 | Automated | `scripts/IQ-014-no-db.sh` | No SQL/migration/ORM/DB-client/broker artifacts | PASS — confirmed absent | Actual:·By:·Date:·P/F:·Ref: |

*Test scripts are shipped in `Qualification/scripts/`. Each captures the ACTUAL from the
system and compares it to the DECLARED expected (cited in the script header), emitting
PASS/FAIL. Execution records are blank until witnessed execution.*

## IQ Findings (Gap Register — consolidated into Gap-Analysis.md)

- **GIQ-001 (High) — CLOSED 2026-06-17** — `requirements.txt` added; all three pinned (`==`). IQ-003 PASS.
- **GIQ-002 (High) — CLOSED 2026-06-17** — Python 3.12 installed; `.venv` provides all three (`mcp==1.28.0`). IQ-005 PASS under `.venv`.
- **GIQ-003 (Medium) — CLOSED 2026-06-17** — min Python ≥3.10 declared in `requirements.txt`; 3.12 venv meets it; enforced by `server.py` pre-flight.
- **GIQ-004 (High) — CLOSED 2026-06-17** — declared in `plugin.json` mcpServers; registered locally (venv), ✔ Connected. IQ-007 PASS.
- **GIQ-005 (Critical) — CLOSED for plugin installs 2026-06-17** — `hooks/hooks.json` auto-discovered on install. In-repo dev registration is opt-in (`.claude/settings.json`); IQ-009 still FAILs on this dev box until that opt-in is taken.
- **GIQ-006 (Medium) — CLOSED 2026-06-17** — `server_version()` MCP tool returns the manifest version. IQ-AI-013 PASS.
- **GIQ-007 (Medium) — CLOSED 2026-06-17** — `logging`→stderr added to `server.py` (every except) and the hook (fail-open + block). OQ-031/032 re-run PASS.

## Open IQ Items Requiring Human / Live Verification

| Item | Why human / live verification is required |
|---|---|
| Accuracy & currency of regulatory reference corpora | Whether the bundled regulatory text is correct as of today needs a qualified regulatory SME, not a file-presence check. |
| `TRAFFIC_TOKEN` GitHub secret | Existence/validity is only visible in the repo's Secrets settings, not a local clone. |
| `${CLAUDE_PLUGIN_ROOT}` resolution at hook execution | A live-runtime behaviour; verify by triggering the hook in a session. |
| End-to-end document protection | Once registered (GIQ-005), confirm a locked file is blocked and a fresh file allowed, in a witnessed live session. |
| Plugin discovery after `install.sh` | Confirmed only by restarting Claude Code and issuing a command. |

## Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Author | *ParaQualis qualification engine (AI-generated DRAFT)* | *unsigned* | 2026-06-14 |
| Reviewer | | *unsigned* | |
| QA Approver | | *unsigned* | |

*All findings are DRAFT and traceable to the cited file:line evidence. Execution records are
blank pending witnessed execution. This document must be reviewed and approved by
appropriately qualified and authorized personnel before use as GxP qualification evidence.*

## Version history

*Document control for this pack is by approval sign-off (above) and the version summary below; a separate audit log is not maintained for these documents.*

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 0.1 (DRAFT) | 2026-06-14 | ParaQualis qualification engine | Initial draft generated by `/qualify:build`. |
| 0.2 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Added version-history section. Install evidence updated: dependency manifest added and pre-flight checks introduced (see Gap-Analysis GIQ-001/002/003). |
| 0.4 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Python 3.12 + `.venv` with `mcp==1.28.0`; GIQ-001/002/003 closed; IQ-003/004/005/006 now PASS under the venv runtime. |
| 0.5 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | GIQ-004/006/007 closed and GIQ-005 closed for plugin installs; IQ-007 & IQ-AI-013 now PASS. Only residual: in-repo dev hook opt-in (IQ-009). |
| 0.6 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Qualified-version references updated to v1.2.0 (release bump; remediated build). |
| 0.7 (DRAFT) | 2026-06-18 | ParaQualis qualification engine | Plugin id renamed paraqualis-skills → paraqualis-gxp; version 1.1.0 → 1.2.0 (no functional change). |

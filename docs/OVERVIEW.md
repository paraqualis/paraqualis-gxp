# ParaQualis Skills — Overview

*Author: ParaQualis LLC · © 2026 ParaQualis LLC · MIT licensed.*

A toolkit of Claude Code commands, skills, and sub-agents for life-sciences regulatory
and computer-system-validation work — GAMP 5, 21 CFR Part 11, EU GMP Annex 11, the live
eCFR, openFDA, and an IQ/OQ/PQ qualification engine.

This is the **one place to understand the whole thing**. The catalog near the bottom is
generated from the repo itself, so it always matches what's installed.

---

## The six building blocks

| Block | What it is | You… | Example |
|---|---|---|---|
| **Command** | A saved prompt you trigger with `/name` | type it | `/cfr21-11:gap` |
| **Skill** | Expertise Claude pulls in **automatically** when your request matches it | just ask in plain English | `part11-advisor` |
| **Sub-agent** | A specialist Claude **delegates to**, in its own context (several can run in parallel) | don't invoke directly | `iq-qualifier` |
| **MCP server (tool)** | Real executable **tools** that reach external systems (APIs, databases) — code, not a prompt | just ask; Claude calls the tool | `openfda` (recalls/labels/events) |
| **Hook** | A script Claude Code runs **automatically on an event** (before/after a tool, on a prompt) — deterministic, no model turn | configure once; it fires on its own | `protect-approved-documents` |
| **Plugin** | A **bundle** of all the blocks above, installed in **one command** | install it once | `paraqualis-gxp` |

Built *from* these blocks: **the qualification engine** — the `/qualify:*` commands plus
three sub-agents that produce an IQ/OQ/PQ pack. `/qualify:build <app>` generates it,
`/qualify:requirements <app>` authors the URS it traces against when none exists, and
`/qualify:review <app>` reports status and plans gap-closure. See `how-to-qualify.md`.

**Tools (MCP servers)** live under `mcp-servers/`. The first is **openFDA** — it gives
Claude tools to query FDA recalls, drug labels, and adverse-event reports directly. It's
opt-in (needs `pip install mcp` and a one-line registration); see
`mcp-servers/openfda/README.md`. Unlike commands/skills, an MCP server is a running
program, so it isn't symlinked by `install.sh` — you register it once with Claude Code.

Commands live in `commands/` (a sub-folder = a `family:` prefix). Skills live in
`skills/`. Sub-agents live in `agents/`. `install.sh` symlinks all three into
`~/.claude/` so they're available in **every** project on the machine.

**Hooks** live under `hooks/`. The first is **`protect-approved-documents.py`** — a
`PreToolUse` hook that refuses any edit to a file carrying the marker
`<!-- PARAQUALIS-LOCK: approved -->`, so an approved record can't be overwritten in
place. Hooks fire deterministically on Claude Code events (no model turn); see
`hooks/README.md` to register one. The **plugin** bundles the hook automatically.

**The plugin** (`.claude-plugin/`) wraps everything above into one installable unit.
`plugin.json` is the manifest; `marketplace.json` is the storefront that makes it
installable with a single command (see Quick start). `install.sh` + symlinks remain the
*local dev* workflow; the plugin is the *distribution* path for everyone else.

## Quick start

1. **Install once.** Two ways:
   - **As a plugin (one command):** `/plugin marketplace add paraqualis/paraqualis-gxp`
     then `/plugin install paraqualis-gxp@paraqualis`. (Needs the repo to be public, or
     point the first command at a local path to test.)
   - **From source (dev workflow):** clone the repo (or download the ZIP), run
     `./install.sh`, restart Claude Code. (Full options — SSH/HTTPS/ZIP — in
     `how-to-qualify.md` §1.)
2. **Use a command:** type `/` to see them, e.g. `/eCFR:structure 21 CFR 11`.
3. **Use a skill:** just ask — *"is our cloud LIMS a Part 11 closed or open system?"* —
   and the relevant advisor fires on its own.
4. **Qualify an app:** `/qualify:build <path-to-the-app>` → a draft IQ/OQ/PQ pack in
   `<app>/Qualification/`. No requirements doc yet? `/qualify:requirements <app>` first
   (or let build offer it). Already have a pack? `/qualify:review <app>` for status +
   gap-closure plan. See **`how-to-qualify.md`** for the full walkthrough.

## Key documents

| Document | What it covers |
|---|---|
| `OVERVIEW.md` (this file) | The whole toolkit at a glance + the live catalog |
| `how-to-qualify.md` | How to run the `/qualify:*` commands on any app — setup, what to tell Claude, every output |
| `xq-qualification-protocol.md` | The qualification abstraction: test-cases, scripts, gap register, formats |

## Principles the toolkit holds to

- **Plain English, always** — output is written so any reader follows it without decoding
  jargon; technical detail lives in the fix/script, not the explanation.
- **No stack assumptions** — the qualifier discovers the language, runtime, and databases
  (zero, one, or many) rather than assuming them.
- **Expected values are sourced, not invented** — from the spec or the system's own
  declarations, never hardcoded.
- **Honest evidence** — a skipped test is not a pass; errors are never swallowed silently.
- **Markdown is the source of truth** — Word/Excel are generated, never hand-edited.

## Adding something new

- **A command:** drop a `.md` file in `commands/<family>/` (the folder becomes the
  `family:` prefix). Filename = command name. Body = the prompt.
- **A skill:** make `skills/<name>/SKILL.md` with `name` + `description` frontmatter; bundle
  reference files alongside it. The `description` is what makes Claude auto-invoke it.
- **A sub-agent:** make `agents/<name>.md` with `name` + `description` (+ optional `tools`,
  `model`). Used by the qualification engine.
- **A hook:** add a script in `hooks/` and register it in `settings.json` (or, for the
  plugin, add an entry to `hooks/hooks.json` using `${CLAUDE_PLUGIN_ROOT}`). See
  `hooks/README.md`.
- Then: `./install.sh` (links new families/skills/agents), **restart** Claude Code, and
  `python3 docs/build_catalog.py` to refresh the catalog below. *(Note: the catalog lists
  commands/skills/agents only — hooks and the plugin aren't auto-enumerated yet.)*

## Keeping this document current

The narrative above is hand-written; the **catalog below is generated** from the repo, so
it can't drift. Two levels of automation:

- **Automatic (catalog):** a git **pre-commit hook** (`.githooks/pre-commit`, enabled by
  `install.sh`) re-runs `build_catalog.py` and re-stages this file on every commit — so the
  Markdown catalog is always current without you remembering anything.
- **On demand (Word):** run `python3 docs/build_docs.py` to refresh the catalog **and**
  render the branded Word versions (`OVERVIEW.docx`, `how-to-qualify.docx`,
  `xq-qualification-protocol.docx`). Do this before sharing — the `.docx` are binary, so
  they're not rebuilt on every commit.

You only hand-edit the narrative when the *concepts* change; the lists look after themselves.

---

<!-- CATALOG:START -->
## Catalog

_Auto-generated by `docs/build_catalog.py` from the repo — do not hand-edit between the CATALOG markers; re-run the script instead._

### Commands (you type these)

**cfr21-11**

| Command | What it does |
|---|---|
| `/cfr21-11:auditprep` | Prepare for an FDA inspection of a computerized system against 21 CFR Part 11 (electronic records & signatures) — likely questions, evidence to assemble, and weak points |
| `/cfr21-11:checklist` | Generate a tailored 21 CFR Part 11 controls checklist for a computerized system, to drive validation or audit |
| `/cfr21-11:gap` | Gap-assess a computerized system/process against 21 CFR Part 11, flagging compliance gaps with severity and remediation |

**eCFR**

| Command | What it does |
|---|---|
| `/eCFR:changes` | Show the amendment history of a CFR part (any Title) — which sections changed and when — from the eCFR |
| `/eCFR:compare` | Compare a CFR section/part between two dates (point-in-time) and show exactly what wording changed, from the eCFR |
| `/eCFR:search` | Full-text search the eCFR for a term or phrase and return the matching citations with excerpts |
| `/eCFR:structure` | Show the structure (headings only, no content) two levels below any eCFR reference — any Title, any level |
| `/eCFR:text` | Fetch the full current regulatory TEXT of a CFR section or part (any Title), live from the eCFR |

**eu-annex11**

| Command | What it does |
|---|---|
| `/eu-annex11:auditprep` | Prepare for an EU GMP inspection of a computerized system against Annex 11 — likely inspector questions, evidence, and weak points |
| `/eu-annex11:checklist` | Generate a tailored EU GMP Annex 11 controls checklist for a computerized system, to drive validation or inspection readiness |
| `/eu-annex11:crosswalk` | Crosswalk EU GMP Annex 11 against US 21 CFR Part 11 — where they align, where they diverge, and what satisfies both |
| `/eu-annex11:gap` | Gap-assess a computerized system against EU GMP Annex 11, flagging compliance gaps by clause with severity and remediation |

**gamp**

| Command | What it does |
|---|---|
| `/gamp:assess` | Assess a computerized system against GAMP 5 (2nd ed.) software categories and recommend validation rigor |
| `/gamp:testplan` | Draft a risk-based GAMP 5 validation test plan (IQ/OQ/PQ) for a computerized system, scaled to its category and risk |

**openfda**

| Command | What it does |
|---|---|
| `/openfda:setup` | Check for an openFDA API key and, if it's missing, help the user get a free one and save it to a shell file of their choice |

**qualify**

| Command | What it does |
|---|---|
| `/qualify:build` | Build a draft IQ/OQ/PQ qualification pack for a system — discover the stack, database schema(s), required seed data, and the approved requirements, then fan out to the xQ specialist subagents in parallel |
| `/qualify:requirements` | Author a draft User Requirements Specification (URS) for a system when none exists — discharging the regulatory obligation to define requirements before qualification, structured so each requirement is testable and feeds PQ traceability |
| `/qualify:review` | Review an existing qualification pack — report what is complete and where gaps remain, detect drift against the current system, and produce a plan to close the gaps an AI can close |

### Skills (Claude invokes these automatically)

| Skill | What it does |
|---|---|
| `gamp-advisor` | Expert advisor on GAMP 5 (2nd ed.) risk-based computerized system validation (CSV). Use whenever the user asks about GAMP software categories (1/3/4/5), how to categorize a computerized or GxP system, how much validation rigor a system needs, IQ/OQ/PQ scope, URS/functional/design specifications, supplier/vendor assessment, configured vs. custom (bespoke) software, hybrid systems with custom scripts on a configured platform, or proportionate/risk-based CSV lifecycle deliverables for pharma/medtech systems. Also covers validation of AI/ML- and GenAI/LLM-enabled GxP systems (model validation, training-data integrity, drift monitoring, human oversight) per the ISPE GAMP Guide: Artificial Intelligence. Reasons against the bundled GAMP 5 category framework and AI/ML reference. |
| `part11-advisor` | Expert advisor on FDA 21 CFR Part 11 (electronic records and electronic signatures). Use whenever the user asks about Part 11 compliance, electronic records or signatures, audit trails, closed vs. open systems, e-signature components/controls, record retention or copies for the agency, ALCOA+ data integrity under Part 11, a Part 11 gap or inspection readiness, or whether a computerized/GxP system meets §11.10, §11.30, §11.50, §11.70, §11.100, §11.200, or §11.300. Reasons against the bundled verbatim regulation text and cites the exact paragraph. |

### Sub-agents (run in parallel by `/qualify:build` and `/qualify:review`)

| Sub-agent | What it does |
|---|---|
| `iq-qualifier` | Installation Qualification (IQ) specialist. Use to examine a system's TECH STACK and installed/configured state and produce IQ evidence — or, in verify mode, to pre-check IQ items in an existing qualification pack against what's actually present. Delegated to by /qualify:build (generate) and /qualify:review (verify), typically in parallel with oq-qualifier and pq-qualifier. |
| `oq-qualifier` | Operational Qualification (OQ) specialist. Use to examine HOW a system has been built — its functions, configuration logic, build pipeline, and tests — and produce OQ evidence that it operates per specification; or, in verify mode, pre-check OQ items in an existing pack. Delegated to by /qualify:build (generate) and /qualify:review (verify), usually in parallel with iq-qualifier and pq-qualifier. |
| `pq-qualifier` | Performance Qualification (PQ) specialist. Use to verify a system DOES WHAT IT IS SUPPOSED TO in its intended use — requirements vs. actual behaviour, end-to-end workflows, representative data — and produce PQ evidence; or, in verify mode, pre-check PQ items in an existing pack. Delegated to by /qualify:build (generate) and /qualify:review (verify), usually in parallel with iq-qualifier and oq-qualifier. |

<!-- CATALOG:END -->

# ParaQualis GAMP & 21 CFR Part 11 Skills

Claude Code slash commands for life-sciences computer-system validation (CSV),
GAMP 5, and 21 CFR Part 11 compliance work.

Copyright © 2026 ParaQualis LLC. Released under the [MIT License](LICENSE).

## What's here

Commands are grouped into families. Each family is a folder under `commands/`;
the folder name becomes the command's namespace prefix (`/family:command`).

| Command | What it does |
|---|---|
| `/gamp:assess` | Categorize a system against GAMP 5 (2nd ed.) software categories and recommend proportionate validation rigor. |
| `/gamp:testplan` | Draft a risk-based GAMP 5 validation test plan (IQ/OQ/PQ), scaled to category and risk. |
| `/cfr21-11:auditprep` | Prepare for an FDA inspection against 21 CFR Part 11 — likely questions, evidence to assemble, weak points. |
| `/cfr21-11:gap` | Gap-assess a system/process against Part 11, with severity and remediation. |
| `/cfr21-11:checklist` | Generate a tailored Part 11 controls checklist for validation or audit. |
| `/eCFR:structure` | Show the structure (headings only, no content) two levels below any eCFR reference — any Title. |
| `/eCFR:text` | Fetch the full current regulatory text of a CFR section or part. |
| `/eCFR:search` | Full-text search the eCFR and return matching citations with excerpts. |
| `/eCFR:changes` | Show a part's amendment history — which sections changed and when. |
| `/eCFR:compare` | Compare a section/part between two dates and show exactly what wording changed. |
| `/eu-annex11:gap` | Gap-assess a system against EU GMP Annex 11, by clause, with severity and remediation. |
| `/eu-annex11:checklist` | Generate a tailored Annex 11 controls checklist for validation or inspection readiness. |
| `/eu-annex11:auditprep` | Prepare for an EU GMP inspection against Annex 11 — likely questions, evidence, weak points. |
| `/eu-annex11:crosswalk` | Map Annex 11 against 21 CFR Part 11 — alignment, divergence, and what satisfies both. |
| `/qualify` | Build (or verify) an IQ/OQ/PQ qualification package for a system by fanning out to the xQ subagents **in parallel**. |

The `eCFR:` family pulls live from the public [eCFR API](https://www.ecfr.gov/developers/documentation/api/v1)
at runtime (no key required) and works for any CFR Title, not just 21. The
`eu-annex11:` family reflects the established Annex 11 (2011) and flags the July 2025
draft revision + Annex 22 (AI) as draft.

## Skills

Skills live under `skills/` and are **auto-invoked by Claude** when a request matches
their description — no slash command to type. Each is a folder with a `SKILL.md`
(name + description + instructions) and optional bundled reference files.

| Skill | What it does |
|---|---|
| `part11-advisor` | Always-available 21 CFR Part 11 expertise. Fires on any electronic-records/signatures, audit-trail, or Part 11 compliance question, and reasons against the **verbatim Part 11 text** bundled at `reference/21-cfr-part-11.md`. |
| `gamp-advisor` | Always-available GAMP 5 (2nd ed.) CSV expertise, including **AI/ML & GenAI** validation (per the ISPE GAMP Guide: Artificial Intelligence, July 2025, and EU draft Annex 22). Fires on software-category, validation-rigor, IQ/OQ/PQ-scope, or AI-system questions, reasoning against bundled framework references (original summaries — GAMP 5 and the ISPE AI Guide are ISPE-copyrighted, so their text is not reproduced). |

## Subagents

Subagents live under `agents/` and are specialized sub-Claudes the main agent
delegates to, **each in its own isolated context**. That isolation lets several run
**in parallel**. The `/qualify` command orchestrates these three concurrently:

| Subagent | Stage | Examines |
|---|---|---|
| `iq-qualifier` | Installation Qualification | the tech stack — runtimes, dependencies, infra, config |
| `oq-qualifier` | Operational Qualification | how it's built — functions, config logic, tests, pipeline |
| `pq-qualifier` | Performance Qualification | does it do its job — intended use, requirements ↔ behaviour |

They produce **draft, traceable evidence** (generate mode) or **pre-check an existing
pack** (verify mode); `/qualify` assembles the consolidated package. All output is
stamped draft pending qualified-person review — the generator itself is a GxP-impacting
tool that would require its own qualification before its output is relied upon.

Every item follows the **[xQ Qualification Protocol](docs/xq-qualification-protocol.md)**:
a Requirement paired with an **executable test** (a script/query that is itself a pack
artifact in `scripts/`), acceptance criteria, and an execution record — plus an ID
scheme, automated-vs-manual marking, a regulatory traceability matrix, and a three-layer
evidence model for AI/ML systems.

## Install (any machine)

```bash
git clone git@github.com:DeepJam/paraqualis-skills.git
cd paraqualis-skills
./install.sh
```

`install.sh` symlinks each command family into `~/.claude/commands/` and each skill
into `~/.claude/skills/`, so they stay live globally while this repo remains the
single source of truth. Edit anything here and the change is live everywhere
immediately — no copy step. The installer self-heals: stale links from renamed or
removed items are pruned automatically. **Restart Claude Code after installing** so
it re-scans the commands and skills folders.

## Repo layout

```
.
├── commands/
│   ├── gamp/
│   │   ├── assess.md
│   │   └── testplan.md
│   ├── cfr21-11/
│   │   ├── auditprep.md
│   │   ├── gap.md
│   │   └── checklist.md
│   ├── eCFR/
│   │   ├── structure.md
│   │   ├── text.md
│   │   ├── search.md
│   │   ├── changes.md
│   │   └── compare.md
│   ├── eu-annex11/
│   │   ├── gap.md
│   │   ├── checklist.md
│   │   ├── auditprep.md
│   │   └── crosswalk.md
│   └── qualify.md          # orchestrator: fans out to the xQ subagents
├── agents/                 # subagents the main agent delegates to (run in parallel)
│   ├── iq-qualifier.md
│   ├── oq-qualifier.md
│   └── pq-qualifier.md
├── skills/
│   ├── part11-advisor/
│   │   ├── SKILL.md
│   │   └── reference/
│   │       └── 21-cfr-part-11.md       # verbatim Part 11, bundled
│   └── gamp-advisor/
│       ├── SKILL.md
│       └── reference/
│           ├── gamp5-category-framework.md   # original summary (not ISPE text)
│           └── ai-ml-validation.md           # AI/ML validation themes
├── docs/
│   └── xq-qualification-protocol.md   # the test-case + pack abstraction for /qualify
├── install.sh        # symlinks commands + skills + agents into ~/.claude/
├── LICENSE           # MIT
└── README.md
```

## Conventions

- Every command file carries a ParaQualis LLC copyright header as a YAML comment
  inside the frontmatter, so it never leaks into the prompt sent to the model.
- Command bodies lead with the answer and produce decision-grade, auditable output
  (regulatory citations included), proportionate to risk.

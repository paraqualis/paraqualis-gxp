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

The `eCFR:` family pulls live from the public [eCFR API](https://www.ecfr.gov/developers/documentation/api/v1)
at runtime (no key required) and works for any CFR Title, not just 21.

> An `eu-annex11:` family (EU GMP Annex 11) is planned.

## Install (any machine)

```bash
git clone git@github.com:DeepJam/paraqualis-skills.git
cd paraqualis-skills
./install.sh
```

`install.sh` symlinks each command family into `~/.claude/commands/`, so the
commands stay live globally while this repo remains the single source of truth.
Edit a command here, and the change is live everywhere immediately — no copy step.
**Restart Claude Code after installing** so it re-scans the commands folder.

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
│   └── eCFR/
│       ├── structure.md
│       ├── text.md
│       ├── search.md
│       ├── changes.md
│       └── compare.md
├── install.sh        # symlinks command families into ~/.claude/commands/
├── LICENSE           # MIT
└── README.md
```

## Conventions

- Every command file carries a ParaQualis LLC copyright header as a YAML comment
  inside the frontmatter, so it never leaks into the prompt sent to the model.
- Command bodies lead with the answer and produce decision-grade, auditable output
  (regulatory citations included), proportionate to risk.

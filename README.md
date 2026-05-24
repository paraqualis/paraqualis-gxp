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

> An `eu-annex11:` family (EU GMP Annex 11) is planned.

## Install (any machine)

```bash
git clone <your-github-url> "21.11 and GAMP Skills"
cd "21.11 and GAMP Skills"
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
│   └── cfr21-11/
│       ├── auditprep.md
│       ├── gap.md
│       └── checklist.md
├── install.sh        # symlinks command families into ~/.claude/commands/
├── LICENSE           # MIT
└── README.md
```

## Conventions

- Every command file carries a ParaQualis LLC copyright header as a YAML comment
  inside the frontmatter, so it never leaks into the prompt sent to the model.
- Command bodies lead with the answer and produce decision-grade, auditable output
  (regulatory citations included), proportionate to risk.

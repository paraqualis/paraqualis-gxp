# How to Qualify Any Application — ParaQualis xQ Engine

*Author: ParaQualis LLC · © 2026 ParaQualis LLC · Licensed under the MIT License.*

A practical guide to producing a draft **IQ / OQ / PQ qualification package** for any
application using the ParaQualis xQ engine in Claude Code. The engine examines the system,
fans out to three specialist sub-agents in parallel, and assembles a client-ready pack in
**Markdown, Word, and Excel**, plus executable test scripts and a gap register.

> **Read this first.** The output is **draft evidence**, not a sign-off. It is reviewed and
> executed by appropriately qualified and authorized personnel. The engine itself is a
> GxP-impacting tool that would require its own qualification before its output is relied
> upon as formal evidence. It accelerates and structures the work; it does not self-certify.

---

## 1. One-time setup (per machine)

**Step 1 — get the files.** Use whichever route your access allows. *(The repository is
private — you must first be granted access by ParaQualis, or use a copy they provide.)*
- **SSH** (collaborators with an SSH key on the repo):
  `git clone git@github.com:paraqualis/paraqualis-skills.git`
- **HTTPS** (collaborators — prompts for a GitHub token/login):
  `git clone https://github.com/paraqualis/paraqualis-skills.git`
- **No git, or no access configured:** on the GitHub page choose **Code → Download ZIP**
  and unzip it.

**Step 2 — install.** From the project folder:
```bash
cd paraqualis-skills
./install.sh          # or:  bash install.sh   (use this if it isn't executable, e.g. from a ZIP)
```
This symlinks the commands, skills, and sub-agents into `~/.claude/`. Re-run it any time
you pull updates or add a new command family / skill / agent.

**Step 3 — restart Claude Code** so it registers them. Confirm with `/` → `/qualify` appears.

**Optional — Word/Excel output:** `pip install python-docx openpyxl`. Markdown and the test
scripts work without them.

No assumptions are made about the application's technology: the engine discovers the
language, runtime, databases (zero, one, or many — of any type), and services itself.

---

## 2. What to tell the Claude helping you with the application

Run `/qualify` from a Claude Code session that can see the application. To get grounded,
auditable output, give Claude this context first (the more it knows, the less it has to
assume — and qualification tests are *sourced from the specification*, never invented):

- **Where the system is** — the repo path and, if useful, how to reach the running app.
- **Intended use & GxP context** — what the system is for and why it matters.
- **Regulatory scope** — which apply: 21 CFR Part 11, EU GMP Annex 11, GAMP 5, AI/ML
  guidance (FDA / ISPE GAMP AI / EU Annex 22).
- **Where the specification lives** — URS, functional/design specs, configuration
  baselines. Expected values (versions, schema, thresholds) are read from the spec or the
  system's own declarations (Dockerfile, lockfiles, migrations) — so point Claude at them.
- **Any existing qualification pack** to verify against (enables *verify mode*, below).

You do **not** need to list the tech stack or databases — the engine detects them. Telling
it anyway does no harm.

---

## 3. How to trigger it

**Generate a new pack:**
```
/qualify <path-to-the-application>
```

**Verify an existing pack** (pre-checks the items it can substantiate, leaves the rest for
human sign-off):
```
/qualify <path-to-the-application>   (then reference the existing qualification pack)
```

---

## 4. What happens, and what to expect

1. The orchestrator does a quick scan of the application to scope each stage.
2. It **fans out to three sub-agents in parallel** — `iq-qualifier`, `oq-qualifier`,
   `pq-qualifier` — each examining its slice in its own context:
   - **IQ** — is it installed/configured correctly? tech stack, **database schema(s)**,
     required seed/reference data, boot configuration.
   - **OQ** — does it operate per spec? functions, **unit-test evidence**, edge & error
     conditions, **audit trails**, **electronic signatures/sign-offs**, dependency
     handling (must fail loud, never silently), minimum configuration to *use* the system.
   - **PQ** — does it do its job? intended-use workflows, requirements traceability, and —
     for AI/ML systems — consistency, drift, and (for LLMs) hallucination, with defined
     acceptance outcomes.
3. The orchestrator assembles everything into one consolidated pack.

**Expect a DRAFT.** The test scripts are *draft instruments* derived from examining the
system; you then run them against the live system, and some will need adjustment against
what actually executes. That iteration is the qualification work. **The genuine test of the
system is running the scripts** — reading code is necessarily partial.

---

## 5. What you get — the `Qualification/` directory

By default a `Qualification/` folder is created **inside the project you qualified**
(`<project>/Qualification/`), so it lives and versions with the system and sits where the
gap-loop needs it. The engine *examines* the system read-only and modifies **no existing
files** — it only adds this new folder. (Point it elsewhere if you want a detached
deliverable.) It contains:

```
Qualification/
├── docs/
│   ├── Qualification-Summary.md / .docx   Cover, readiness verdict, scorecard,
│   │                                      regulatory traceability matrix, approvals block
│   ├── IQ.md / .docx                       Installation Qualification test-cases
│   ├── OQ.md / .docx                       Operational Qualification test-cases
│   ├── PQ.md / .docx                       Performance Qualification test-cases
│   ├── Gap-Analysis.md / .docx             The gap register (see §6)
│   └── Qualification-Pack.xlsx             Workbook: Summary, IQ, OQ, PQ, Traceability,
│                                           and Gaps — a sheet per stage
├── scripts/                                The executable test scripts — one file per
│                                           test-case (.sh / .sql / .py) + a README
├── records/                                Execution-record template; one filled record
│                                           per executed test = the evidence
└── build_docx.py · build_xlsx.py           Regenerate the Word/Excel from the Markdown
```

**Every qualification item is a test-case** with: an ID (`IQ-/OQ-/PQ-NNN`, `-AI-` for
AI-specific), the **requirement**, the regulatory linkage, the **executable test** (a
script in `scripts/`, or a manual procedure where it can't be scripted — UI tests usually
are manual), the **acceptance criteria**, the expected result, and a blank **execution
record** to complete when run.

**Formats:** Markdown is the **source of truth**. Word (branded, authored by ParaQualis
LLC) and Excel are **generated** — never hand-edit them. After editing any `.md`, rebuild:
```bash
cd Qualification && python3 build_docx.py && python3 build_xlsx.py
```

---

## 6. Closing the gaps (the loop)

`docs/Gap-Analysis.md` is one file with two jobs: it is the auditable **QA gap register**,
and it is the file you **feed to Claude in the application's repo to close the gaps**. Each
gap row carries its **definition of done = the test-case that must pass**. So:

```
/qualify <app>            → tests + Gap-Analysis.md (each gap: fix + "done = test X passes")
open Gap-Analysis.md in the app repo, hand it to Claude
Claude fixes each gap     → re-run the linked test-case → green → gap closed
re-run /qualify           → a cleaner pack
```

Remediation and evidence are the same chain: a gap is closed only when the test that found
it passes — not on anyone's say-so.

---

## 7. Principles the engine holds to (so you can trust the output)

- **Plain English, always** — verdicts, findings, and gaps are written so any reader
  follows them without decoding jargon (not just a developer): what it is *and why it
  matters*. Technical detail lives in the scripts/remediation, not the narrative.
- **No stack assumptions** — language, runtime, and databases (0/1/many, any type) are
  discovered, not assumed; absence of a component is a valid finding, not a skipped test.
- **Expected values are sourced, not invented** — read from the spec or the system's own
  declarations and cited; never hardcoded literals.
- **Honest evidence** — a skipped/unexecuted test is *not* a pass (skips are only for true
  environment gates); errors are never swallowed silently.
- **Deterministic on compliance-critical paths** — no "usually right" / magic-number logic.
- **Writes only the `Qualification/` folder** — never your `tests/`, `validation/`,
  source, or config. It *reads* those if present (as evidence) and treats their **absence
  as a finding, not an error** — it won't create them. Generated scripts live in
  `Qualification/scripts/`, not in your test tree.
- **Draft, traceable, approval-gated** — every claim cites its evidence; the pack is
  reviewed and approved by appropriately qualified and authorized personnel.

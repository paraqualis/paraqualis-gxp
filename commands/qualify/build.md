---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Build a draft IQ/OQ/PQ qualification pack for a system — discover the stack, database schema(s), required seed data, and the approved requirements, then fan out to the xQ specialist subagents in parallel
argument-hint: <path to the system/repo to qualify>
---

Build a draft **qualification package (IQ / OQ / PQ — "xQ")** for the system below by
examining it directly and delegating each qualification stage to its specialist subagent
**in parallel**. This is the **generate** path — it creates the pack from scratch. To
**review** an existing pack and plan gap-closure, use `/qualify:review`; to author the
requirements it qualifies against, use `/qualify:requirements`.

## Input
$ARGUMENTS

## Step 1 — Orient
Do a brief top-level scan of the target so you can scope each subagent (what kind of
system, where the tech-stack manifests, where tests, config, and docs live). **Discover
the stack; assume nothing** — there may be zero, one, or many databases of any type, plus
queues, caches, services. The absence of a component is a valid finding, never a reason to
skip (see `docs/xq-qualification-protocol.md`).

## Step 2 — Establish the specification inputs
A qualification test compares the system to its **specification**, never to invented
values. Gather the sourced inputs each subagent will compare against:

- **Stack / schema / seed data / boot config** — read from the system's **own
  declarations** (Dockerfile, lockfiles, migrations/DDL, config), and cite them. These
  are what IQ and OQ qualify against; they do **not** require a separate requirements doc.
- **Approved requirements (URS)** — the documented intended use and user/functional
  requirements that **PQ** traces against. **Do not assume a name or location** — see
  Step 2a. Where a requirements doc exists, PQ traces to it.

## Step 2a — Locate the requirements doc (ask, don't assume)
The requirements may have **any name** (URS, FRS, SRS, "Functional Spec", a validation
plan), live in a **subdirectory**, or sit **outside the repo entirely** (a shared drive,
SharePoint/Confluence, a Word/PDF, a ticketing system). So:

1. **Search** the obvious places and report what you find — `<project>/Qualification/requirements/`,
   plus `docs/`, `spec*/`, `requirements*/`, and files matching *URS / FRS / SRS /
   requirement / specification* (any extension).
2. **Ask the user to confirm or point you to it**, e.g.:
   *"I'm looking for the approved requirements/specification this system is qualified
   against. I found <list, or nothing>. Is the requirements document one of these, or is
   it elsewhere — a different name, another folder, or outside the repo (a path, file, or
   link)? If there genuinely isn't one yet, say so."*
3. **Only treat requirements as missing once the user confirms** there is none (or can't
   point to one). A doc that exists but is unfound must **not** be reported as a missing-URS
   finding. If the user points to an external/non-text source, read what you can and note
   anything that needs manual transcription.

## Step 3 — Handle a missing requirements document
**IQ and OQ do not depend on a documented URS — always run them in full.** Only **PQ**
(does it do its *intended job*?) needs the approved requirements.

If the user confirms (per Step 2a) that **no approved requirements document exists**:
1. **Proceed anyway** — complete IQ, OQ, and whatever PQ can be evidenced from the
   system's observed behaviour and intended use.
2. **Raise it as a finding** — record a **critical** gap **`GPQ-001`**: *"No approved
   requirements document exists. A defined specification is required before a system can
   be qualified (GAMP 5 lifecycle; EU GMP Annex 11 cl.4; the basis for PQ traceability).
   PQ completeness is capped until one exists."*
3. **Offer to author one inline** — ask the user:
   *"No approved requirements specification was found. Author a DRAFT URS now (via
   `/qualify:requirements`) so PQ can be completed against it? [y/N]"*
   - **On yes** — run the `/qualify:requirements` flow to author a draft URS at
     `<project>/Qualification/requirements/URS.md`, then complete the PQ section against
     it, with every PQ item traced to a draft requirement **flagged
     "ParaQualis-authored, pending owner confirmation."**
   - **On no** — leave PQ partial, keep `GPQ-001` open, and note that running
     `/qualify:requirements` then re-running `/qualify:build` will complete PQ.

## Step 4 — Fan out IN PARALLEL (the point of this command)
**Launch all three subagents concurrently — issue the three delegations in a single
batch, do not wait for one before starting the next.** Tell each it is in **GENERATE
mode** and give it the target path plus the sourced inputs from Step 2:
- **iq-qualifier** — tech stack / installed & configured state, schema(s), seed data, boot config
- **oq-qualifier** — how it's built: functions, config logic, tests, edge/error handling, audit trails, e-sig mechanics, pipeline
- **pq-qualifier** — does it do its job: intended use, requirements ↔ behaviour (traced to the URS, or to flagged authored use cases if none)

They run independently in their own contexts and return their sections.

**Every item each subagent returns must be a qualification test-case** per the
**xQ Qualification Protocol** (`docs/xq-qualification-protocol.md`): an ID
(`IQ-/OQ-/PQ-NNN`, `-AI-` infix for AI tests) · Requirement · regulatory linkage ·
Test method · **the executable test script** (a real artifact where it can be scripted,
else a manual procedure) · acceptance criteria · expected result · a blank
execution-record block. A requirement without a test is incomplete.

## Step 5 — Assemble the package
Collect the three sections and produce a single, client-ready **Qualification Package**
in a **`Qualification/` directory inside the project being qualified**
(`<project>/Qualification/`) by default — it lives and versions with the system (specify
another location if a detached deliverable is preferred). The agents examined the system
read-only and modify **no existing files**; the pack is a *new* folder added alongside.
Per the protocol's pack layout:

```
Qualification/
  requirements/  URS.md  (+ generated .docx)   # the spec PQ traces to (if authored here)
  docs/          Qualification-Summary.md  IQ.md  OQ.md  PQ.md  Gap-Analysis.md  (+ generated .docx, .xlsx)
  scripts/       # the executable test scripts the subagents authored, one file per test-case
  records/       # execution-record templates (filled when scripts are run)
  build_docx.py  build_xlsx.py   # regenerate Word (branded) + Excel (sheet per xQ) from the md
```

1. **Header & summary** — system identified, date, mode (GENERATE), overall readiness
   verdict, and a consolidated count of test-cases PASS / FAIL / not-yet-executed by stage.
2. **IQ / OQ / PQ sections** — each subagent's test-case tables, in order.
3. **Regulatory traceability matrix** — control (Part 11 § / Annex 11 clause / GAMP
   control / AI-guidance item) → test-case ID(s) → status. Pull control lists from
   `/cfr21-11:checklist`, `/eu-annex11:checklist`, `/gamp:assess` as needed.
4. **scripts/** — collect every script the subagents authored; each named `<ID>-*`.
5. **Gap-Analysis.md** — the gap register. IDs are **stage-prefixed so they never
   collide** across the parallel agents: `GIQ-NNN` / `GOQ-NNN` / `GPQ-NNN` (the missing-URS
   finding above is `GPQ-001` when raised). Each row: source test-case(s) · description ·
   severity · regulatory linkage · recommended remediation · target location · **definition
   of done (the test-case that must pass)** · owner · status. **One ID column only.** Write
   each description in **plain language a quality reviewer can understand — what it is AND
   why it matters** — explain jargon, don't assume it; keep the technical fix in the
   remediation field. **Consolidate & dedupe:** merge a gap surfaced by more than one stage
   into a single entry, named for the stage of **greatest impact** (highest severity),
   listing all contributing test-cases. One file that is both the QA deliverable and the
   file fed to Claude in the target repo to close gaps. See the protocol's Gap Analysis
   section.
6. **Approval & governance block** — see below.

Offer to write the whole pack to disk under `<project>/Qualification/` (or a specified
location), then render the branded **Word** (`build_docx.py`, python-docx, ParaQualis
palette) and **Excel** (`build_xlsx.py`, openpyxl — a sheet per xQ stage + Summary +
Traceability) so it can be handed to a pharma client in md, .docx, and .xlsx. Markdown is
the source of truth; Word/Excel are generated, never hand-edited.

## Governance — non-negotiable
- Stamp the package **"DRAFT — pending review and approval by appropriately qualified and authorized personnel."**
- Every claim must be **traceable to cited evidence**; no unsubstantiated pass/fail.
- Apply the **house engineering-quality acceptance criteria** each subagent carries —
  no silent error handling, honest test evidence (a skip is NOT a pass; skips only for
  true environment gates), deterministic logic on compliance-critical paths, version
  capture, server-observable logging. Surface any violation as a qualification finding,
  and never let a skipped/unexecuted check inflate the readiness verdict.
- Note explicitly that **this generator is itself a GxP-impacting tool that would
  require its own qualification** before its output is relied upon as formal evidence
  — it accelerates and structures the evidence; it does not self-certify.
- Include signature lines for Author / Reviewer / QA Approver — left unsigned.

Lead with the summary verdict. No preamble.

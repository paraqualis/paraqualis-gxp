---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Build (or verify) an IQ/OQ/PQ qualification package for a system by fanning out to the xQ specialist subagents in parallel
argument-hint: <path to the system/repo to qualify; optionally also a path to an existing qualification pack to verify against>
---

Produce a draft **qualification package (IQ / OQ / PQ — "xQ")** for the system below
by examining it directly and delegating each qualification stage to its specialist
subagent **in parallel**.

## Input
$ARGUMENTS

## Step 1 — Determine mode
- If an **existing qualification pack** is referenced → **VERIFY mode**: the subagents
  pre-check items they can substantiate from the system and leave the rest for human
  sign-off.
- Otherwise → **GENERATE mode**: the subagents build the xQ evidence from scratch.

## Step 2 — Quick orientation
Do a brief top-level scan of the target so you can give each subagent the right scope
(what kind of system, where the tech-stack manifests, tests, and docs live).

## Step 3 — Fan out IN PARALLEL (the point of this command)
**Launch all three subagents concurrently — issue the three delegations in a single
batch, do not wait for one before starting the next:**
- **iq-qualifier** — tech stack / installed & configured state
- **oq-qualifier** — how it's built: functions, config, tests, pipeline
- **pq-qualifier** — does it do its job: intended use, requirements ↔ behaviour

Give each the target path and the mode. They run independently in their own contexts
and return their sections.

**Every item each subagent returns must be a qualification test-case** per the
**xQ Qualification Protocol** (`docs/xq-qualification-protocol.md`): an ID
(`IQ-/OQ-/PQ-NNN`, `-AI-` infix for AI tests) · Requirement · regulatory linkage ·
Test method · **the executable test script** (authored as a real artifact where it can
be scripted, else a manual procedure) · acceptance criteria · expected result ·
a blank execution-record block. A requirement without a test is incomplete.

## Step 4 — Assemble the package
Collect the three sections and produce a single, client-ready **Qualification Package**
in a **standalone `Qualification/` directory** (a deliverable — never write into the
system under test, which was examined read-only), per the protocol's pack layout:

```
Qualification/
  docs/      Qualification-Summary.md  IQ.md  OQ.md  PQ.md  (+ generated .docx, .xlsx)
  scripts/   # the executable test scripts the subagents authored, one file per test-case
  records/   # execution-record templates (filled when scripts are run)
  build_docx.py  build_xlsx.py   # regenerate Word (branded) + Excel (sheet per xQ) from the md
```

1. **Header & summary** — system identified, date, mode, overall readiness verdict,
   and a consolidated count of test-cases PASS / FAIL / not-yet-executed by stage.
2. **IQ / OQ / PQ sections** — each subagent's test-case tables, in order.
3. **Regulatory traceability matrix** — control (Part 11 § / Annex 11 clause / GAMP
   control / AI-guidance item) → test-case ID(s) → status. Pull control lists from
   `/cfr21-11:checklist`, `/eu-annex11:checklist`, `/gamp:assess` as needed.
4. **scripts/** — collect every script the subagents authored; each named `<ID>-*`.
5. **Open items register** — everything still requiring live execution or human
   verification, grouped by stage and owner.
6. **Approval & governance block** — see below.

Offer to write the whole pack to disk under a standalone `Qualification/` directory,
then render the branded **Word** (`build_docx.py`, python-docx, ParaQualis palette) and
**Excel** (`build_xlsx.py`, openpyxl — a sheet per xQ stage + Summary + Traceability) so
it can be handed to a pharma client in md, .docx, and .xlsx. Markdown is the source of
truth; Word/Excel are generated, never hand-edited.

## Governance — non-negotiable
- Stamp the package **"DRAFT — pending qualified-person review and approval."**
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

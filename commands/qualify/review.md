---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Review an existing qualification pack — report what is complete and where gaps remain, detect drift against the current system, and produce a plan to close the gaps an AI can close
argument-hint: <path to the system/repo that already has a Qualification/ pack>
---

Review an **existing qualification package** for the system below: report **where things
stand** — what is complete, what is outstanding — check it against the **current state of
the system** (detecting drift), and produce a **plan for closing the gaps**, separating the
gaps an AI can close from those that need human or witnessed execution. This is the
**verify** path. To build a pack from scratch use `/qualify:build`; to author the
requirements it traces against use `/qualify:requirements`.

## Input
$ARGUMENTS

## Step 1 — Locate and read the pack
Find the existing pack (default `<project>/Qualification/`). **If there is no pack**, say
so plainly and **offer to run `/qualify:build`** to generate one — don't *silently* start
generating, but on the user's go-ahead, kick it off, then review the result. Otherwise read
what's there: the `IQ.md` / `OQ.md` / `PQ.md` test-cases, the requirements
(`requirements/URS.md` if present), the execution **records**, the **Gap-Analysis.md**,
and the traceability matrix in the summary.

## Step 1a — Locate the requirements doc (ask, don't assume)
PQ can only be reviewed against the requirements it traces to, so confirm where they are.
**Don't assume a name or location** — the requirements may be named anything (URS, FRS,
SRS, "Functional Spec"), live in a subdirectory, or sit outside the repo (shared drive,
SharePoint/Confluence, a Word/PDF, a link). Check `<project>/Qualification/requirements/`
and the obvious places, report what you find, then **ask the user to confirm or point you
to it**. If the user confirms **none exists**:
- Note it as the same **critical finding** the build path raises (`GPQ-001`) — a missing
  approved spec caps PQ and is required under GAMP 5 / EU Annex 11 cl.4.
- **Offer to establish it**: run `/qualify:requirements` to author a draft URS, then
  **kick off `/qualify:build`** to (re)generate the PQ section traced against it — so the
  review then has something complete to assess. Do this on the user's go-ahead, not silently.

## Step 2 — Fan out IN PARALLEL in VERIFY mode (the point of this command)
**Launch all three subagents concurrently — issue the three delegations in a single
batch.** Tell each it is in **VERIFY mode** and give it the target path plus its section of
the pack:
- **iq-qualifier** — pre-check IQ items against what is actually installed/configured now
- **oq-qualifier** — pre-check OQ items against the current build/tests/behaviour
- **pq-qualifier** — pre-check PQ items against the current intended-use behaviour and the URS

Each one, for every test-case it owns: **mark it evidenced** (cite the current evidence),
**still open** (one-line reason), or **invalidated by drift** — the pack asserts X but the
system now shows Y (e.g. a version, schema, or behaviour changed since the pack was
written). Never check an item it cannot substantiate. They return their per-stage verdicts.

## Step 3 — Produce the Review report
Consolidate into a single **Review report**, lead with the verdict:

1. **Readiness scorecard** — per stage (IQ / OQ / PQ) and overall: test-cases **total /
   evidenced / executed-PASS / FAILED / not-yet-executed / invalidated-by-drift**. A
   skipped or unexecuted test is **not** a pass — never let it inflate the score.
2. **What's complete vs. outstanding** — per stage, in **plain English a quality reviewer
   can follow**: what is solidly evidenced, and what still needs doing and why it matters.
3. **Traceability status** — for each control (Part 11 § / Annex 11 cl. / GAMP / AI), is it
   now evidenced by a passing test-case, or still open? Flag any **requirement with no
   test-case** and any **control with no coverage**.
4. **Drift findings** — everywhere the system has changed since the pack was written, so
   the pack no longer matches reality. Each is a finding to re-evidence.

## Step 4 — Produce the gap-closure plan
Take the existing gap register plus everything newly found (open items, failures, drift),
consolidate and dedupe per the protocol (one entry, named for the stage of greatest
impact), and **split the gaps into two lists**:

- **AI-closable** — gaps a coding agent can close **in the target repo** via the
  Gap-Analysis loop: a code/config/test change whose **definition of done is the linked
  test-case passing**. Order them (severity, then dependency) — this ordered list **is the
  actionable plan**. Each entry: what to change, target location, the test that must go
  green, severity, regulatory linkage.
- **Human / live / witnessed** — gaps that need what an AI cannot do: executing a script in
  a controlled environment, witnessed UI/manual testing, a business decision on an
  undefined acceptance value, or an approval/sign-off. Flag these clearly; do **not**
  auto-attempt or mark them closable.

Write the result back into **`<project>/Qualification/docs/Gap-Analysis.md`** (updating
statuses and adding new rows; `GIQ-/GOQ-/GPQ-NNN` IDs, one ID column, never reused) and
offer to write the Review report to **`<project>/Qualification/docs/Review.md`** (+ branded
Word). The agents examine read-only and the pack stays the only thing written.

**The loop:** hand `Gap-Analysis.md` to Claude in the target repo; it works the
**AI-closable** list, each gap closed only when its linked test-case passes; then re-run
`/qualify:review` for a cleaner pack. Remediation and evidence are the same chain.

## Governance — non-negotiable
- The review and updated pack remain **DRAFT — pending review and approval by appropriately
  qualified and authorized personnel.**
- Every "evidenced / passing" claim must cite current evidence; **honest evidence** — a
  skip or unexecuted test is not a pass, and drift is reported, not glossed.
- This tool is itself a GxP-impacting aid; it structures and accelerates the review, it
  does not self-certify the system as qualified.

Lead with the readiness verdict and the top outstanding gaps. No preamble.

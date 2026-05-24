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

## Step 4 — Assemble the package
Collect the three sections and produce a single, client-ready **Qualification Package**:

1. **Header & summary** — system identified, date, mode, overall readiness verdict,
   and a consolidated count of verified items vs. open items by stage.
2. **IQ / OQ / PQ sections** — each subagent's output, in order.
3. **Consolidated traceability** — requirements/spec → IQ/OQ/PQ evidence.
4. **Open items register** — everything still requiring live execution or human
   verification, grouped by stage and owner.
5. **Approval & governance block** — see below.

Offer to write the package to files (e.g. `qualification/IQ.md`, `OQ.md`, `PQ.md`,
`Qualification-Summary.md`) so it can be used as client documentation.

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

---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Generate a tailored EU GMP Annex 11 controls checklist for a computerized system, to drive validation or inspection readiness
argument-hint: <system; describe its GxP use, lifecycle stage, and whether it uses e-signatures / AI>
---

You are assisting a life-sciences quality/validation professional. Produce a
**tailored EU GMP Annex 11 controls checklist** for the system below — the concrete
controls to verify, scoped to how this system is actually used across its lifecycle.
This is a working verification instrument, not an essay.

## System to build the checklist for
$ARGUMENTS

## Version note

Baseline is **Annex 11 (2011)**. A **draft Annex 11 revision** and new **Annex 22
(AI)** were issued July 2025 — treat as draft; flag rather than assert. If AI/ML is
involved, add Annex 22 considerations.

## Produce, in this order

1. **Scoping note** — one or two lines on which clauses are in scope given the
   system's GxP use and lifecycle stage. Flag any clause that is **Not Applicable**
   and why (e.g. no electronic signatures → clause 14 N/A).

2. **The checklist** — grouped by clause. For each item:
   - **[ ]** checkbox
   - **Clause** reference (e.g. Annex 11 §9 Audit Trails)
   - **Control** — the specific thing to verify, as a checkable statement
   - **Demonstrated by** — the configuration, record, or evidence that proves it

   Cover, tailored to scope: risk management (1) · personnel & training (2) ·
   supplier/service-provider assessment & agreements (3) · validation incl. lifecycle
   & data migration (4) · data integrity (5) · built-in accuracy/plausibility checks
   (6) · secure data storage & backup (7) · printouts incl. change indication (8) ·
   audit trails — generated, reviewed, retained (9) · change & configuration
   management (10) · periodic evaluation (11) · physical & logical security (12) ·
   incident management (13) · electronic signatures (14) · batch certification/release
   (15) · business continuity (16) · archiving & readability (17).

3. **N/A items with rationale** — so the scoping decision is itself auditable.

4. **Open questions** — what to confirm with the system owner before treating the
   checklist as final.

Make it copy-paste usable as a verification worksheet. Lead with the scoping note; no
preamble.

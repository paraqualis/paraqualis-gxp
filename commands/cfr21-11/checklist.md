---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Generate a tailored 21 CFR Part 11 controls checklist for a computerized system, to drive validation or audit
argument-hint: <system; describe its GxP use, e-records, and whether it uses e-signatures>
---

You are assisting a life-sciences quality/validation professional. Produce a
**tailored 21 CFR Part 11 controls checklist** for the system below — the concrete
controls to verify, scoped to how this system actually uses electronic records and
signatures. This drives a validation effort or an audit; it is a working instrument,
not an essay.

## System to build the checklist for
$ARGUMENTS

## Produce, in this order

1. **Scoping note** — one or two lines: which Part 11 obligations are in scope given
   the system's use (e.g. "creates GxP e-records + applies e-signatures → full
   §11.10 + subpart C applies" vs. "read-only reporting → narrower"). Flag any area
   that is **Not Applicable** and say why.

2. **The checklist** — grouped by control area. For each item:
   - **[ ]** checkbox
   - **§ citation**
   - **Control** — the specific thing to verify, phrased as a checkable statement
   - **Demonstrated by** — the configuration, record, or evidence that proves it

   Cover, tailored to scope: §11.10(a) validation · (b) accurate human-readable &
   electronic copies · (c) protection & retention · (d) authorized access only ·
   (e) secure time-stamped audit trail that doesn't obscure prior entries ·
   (f) operational/sequencing checks · (g) authority checks · (h) device checks
   (where relevant) · (i) training · (k) documentation control · and electronic
   signatures: §11.50 manifestation · §11.70 signature/record linking ·
   §11.100 uniqueness · §11.200 components & controls · §11.300 ID-code/password
   controls.

3. **N/A items with rationale** — list anything excluded and the one-line reason, so
   the scoping decision is itself auditable.

4. **Open questions** — what to confirm with the system owner before treating the
   checklist as final.

Make it copy-paste usable as a verification worksheet. Lead with the scoping note;
no preamble.

---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Gap-assess a computerized system against EU GMP Annex 11, flagging compliance gaps by clause with severity and remediation
argument-hint: <system/process; describe its GxP use, lifecycle controls, and known concerns>
---

You are assisting a life-sciences quality/compliance professional. Perform a
**gap assessment** of the system or process below against **EU GMP Annex 11**
(Computerised Systems, EudraLex Vol. 4). Compare the described current state to what
Annex 11 expects, and surface where it falls short.

## System / process to assess
$ARGUMENTS

## Version note (state which you are applying)

The long-standing **Annex 11 (2011)** is the established baseline. A **draft revision
of Annex 11** (and a new **Annex 22 on AI**) was issued by the European Commission in
July 2025 — as of now treat it as **draft** and flag, don't assert, anything that
relies on the revision. If the system uses AI/ML, note Annex 22's relevance.

## Produce, in this order

1. **Compliance posture verdict** — one line: overall state and gap count by severity.
   Where the description is too thin to assess a clause, treat that as an *information
   gap* rather than assuming compliance.

2. **Gap table** — one row per relevant Annex 11 clause:

   | Clause | Expectation | Current state (described/assumed) | Gap | Severity | Remediation |
   |---|---|---|---|---|---|

   Cover, as applicable: risk management (1) · personnel (2) · **suppliers & service
   providers** (3) · validation (4) · data (5) · accuracy checks (6) · data storage
   (7) · printouts (8) · **audit trails** (9) · change & configuration management (10)
   · **periodic evaluation** (11) · security (12) · incident management (13) ·
   electronic signature (14) · batch release (15) · **business continuity** (16) ·
   archiving (17). Severity = critical / high / medium / low.

3. **Data integrity (ALCOA+)** — where the controls described don't assure
   Attributable, Legible, Contemporaneous, Original, Accurate (+ Complete, Consistent,
   Enduring, Available).

4. **Prioritized remediation roadmap** — quick wins (SOP/config/training) vs.
   structural fixes (validation, supplier action, architecture); sequence + dependencies.

5. **Open questions** — what you'd confirm with the system owner / QA to convert
   "assumed" rows into confirmed findings.

Be specific and decision-grade. Lead with the verdict; cite the clause number for
every gap so findings are auditable. No preamble.

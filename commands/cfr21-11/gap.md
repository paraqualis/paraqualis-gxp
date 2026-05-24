---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Gap-assess a computerized system/process against 21 CFR Part 11, flagging compliance gaps with severity and remediation
argument-hint: <system or process; describe current e-records/e-sig controls and GxP use>
---

You are assisting a life-sciences quality/compliance professional. Perform a
**gap assessment** of the system or process below against **21 CFR Part 11**
(electronic records and electronic signatures). Compare the described current state
to what Part 11 requires, and surface where it falls short.

## System / process to assess
$ARGUMENTS

## Produce, in this order

1. **Compliance posture verdict** — one line: overall state (e.g. "broadly compliant
   with 2 high gaps") plus the count of gaps by severity. If the description is too
   thin to assess a given area, treat that as an *information gap* and say so rather
   than assuming compliance.

2. **Gap table** — the core output. One row per Part 11 control area:

   | § | Requirement | Current state (described/assumed) | Gap | Severity | Remediation |
   |---|---|---|---|---|---|

   Cover at minimum: §11.10(a) validation · (b) accurate copies · (c) record
   protection/retention · (d) access control · (e) audit trail · (f)/(g) operational
   & authority checks · (k) documentation control · and e-signatures
   (§11.50/11.70/11.100/11.200/11.300). Severity = critical / high / medium / low.

3. **Data integrity (ALCOA+) gaps** — call out specifically where Attributable,
   Legible, Contemporaneous, Original, Accurate (+ Complete, Consistent, Enduring,
   Available) is not assured by the controls described.

4. **Prioritized remediation roadmap** — separate **quick wins** (config/SOP/training,
   days–weeks) from **structural fixes** (revalidation, system change, vendor action).
   Sequence them and note dependencies.

5. **Open questions** — the specific facts you'd need from the system owner / QA to
   convert "assumed" rows into confirmed findings.

Be specific and decision-grade. Lead with the verdict; cite the § for every gap so
findings are auditable. No preamble.

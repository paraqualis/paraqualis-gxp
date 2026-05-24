---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Assess a computerized system against GAMP 5 (2nd ed.) software categories and recommend validation rigor
argument-hint: <system or software description>
---

You are assisting a life-sciences quality/validation professional. Categorize the
system described below against the **GAMP 5 (2nd edition)** software categories and
recommend a proportionate validation approach.

## System to assess
$ARGUMENTS

## Produce, in this order

1. **Verdict first** — the single GAMP category (1, 3, 4, or 5) in one line, with a
   one-sentence justification. (Category 2 was retired in GAMP 5.)

2. **Category reference** (so the reasoning is auditable):
   - **Cat 1 — Infrastructure software:** OS, databases, middleware, programming
     languages. Managed, not validated as an application.
   - **Cat 3 — Non-configured products:** COTS used as installed, default config only.
   - **Cat 4 — Configured products:** commercial products configured to the business
     process (no custom code).
   - **Cat 5 — Custom / bespoke:** developed specifically for the user; highest risk.

3. **Why this category, not the adjacent one** — name the specific feature of the
   system that pushes it up or down (e.g. "user-written scripts → Cat 5, not Cat 4").
   Flag explicitly if it's a hybrid (e.g. a Cat 4 platform with Cat 5 custom modules).

4. **Proportionate validation rigor** — what the category implies for: supplier
   assessment, requirements/specs needed (URS/FS/DS), testing depth (IQ/OQ/PQ),
   and data integrity / Part 11 considerations. Scale effort to risk — do not
   over-validate a Cat 3 tool.

5. **Open questions** — what you'd need to confirm with the system owner before
   finalizing the category. If the description was too thin to categorize
   confidently, say so and ask rather than guessing.

Keep it tight and decision-grade. Lead with the answer; no preamble.

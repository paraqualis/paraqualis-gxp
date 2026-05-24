---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Draft a risk-based GAMP 5 validation test plan (IQ/OQ/PQ) for a computerized system, scaled to its category and risk
argument-hint: <system description; include GAMP category and key risks if known>
---

You are assisting a life-sciences validation professional. Produce a **risk-based
validation test plan** for the computerized system below, following GAMP 5 (2nd ed.)
principles. Effort must be **proportionate to category and risk** — do not propose
exhaustive testing for a low-risk Cat 3 tool.

## System to plan testing for
$ARGUMENTS

## Produce, in this order

1. **Test strategy in one paragraph** — the overall approach and *why it's sized
   this way*, tied to the system's GAMP category and risk profile. If the category
   or critical risks weren't given, state your assumption explicitly (and flag that
   `/gamp:assess` should be run first if the category is unknown).

2. **Scope** — a short in-scope / out-of-scope table. Be explicit about what is
   leveraged from supplier testing vs. tested by the regulated user.

3. **Test phases (scaled to category):**
   - **IQ — Installation Qualification:** environment, versions, configuration,
     security/access setup is installed correctly.
   - **OQ — Operational Qualification:** functions operate per specification across
     normal, boundary, and challenge (negative) conditions.
   - **PQ — Performance Qualification:** the system performs in the live business
     process with real workflows, data, and users.
   For each phase: objective, what's covered, and roughly how many test cases /
   what depth is warranted given the risk. Omit or minimize a phase if the category
   doesn't warrant it, and say why.

4. **Requirements traceability** — show how test cases map back to requirements
   (URS / functional specs). Include a small illustrative traceability table
   (Requirement → Risk → Test case ID → Phase).

5. **Representative test cases** — 4–8 concrete, high-value test cases. For each:
   ID, objective, preconditions, steps (brief), and **acceptance criteria**.
   Prioritize the cases that cover the highest-risk / GxP-critical functions.

6. **Data integrity & Part 11 checks** — call out specific tests for audit trail,
   access controls, electronic signatures, and record integrity (ALCOA+) where the
   system's GxP use demands it.

7. **Prerequisites & assumptions** — approved specs, test environment, test data,
   trained testers, deviation-handling approach. List what must be true before
   execution starts.

8. **Open questions** — what you'd confirm with the system/process owner before
   finalizing. If the description is too thin to plan responsibly, say so and ask.

Keep it decision-grade and execution-ready. Lead with the strategy; no preamble.

---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Author a draft User Requirements Specification (URS) for a system when none exists — discharging the regulatory obligation to define requirements before qualification, structured so each requirement is testable and feeds PQ traceability
argument-hint: <path to the system/repo>; optionally its intended use and regulatory scope
---

Author a draft **User Requirements Specification (URS)** for the system below. A documented
requirements specification is a **regulatory obligation, not an optional artifact**: it is
the foundation of the validation lifecycle (GAMP 5), the basis an inspector expects under
**EU GMP Annex 11 cl.4** and the Part 11 expectation of a defined, controlled system, and
the thing **Performance Qualification traces against** — without it, PQ has nothing to
prove the system against. This command produces a **DRAFT** URS to be reviewed and approved
by appropriately qualified and authorized personnel; it does not self-approve.

Use this when `/qualify:build` reports no approved requirements doc, or any time the system
lacks one. Once approved, `/qualify:build` reads this file as the sourced input for PQ.

## Input
$ARGUMENTS

## Step 1 — First confirm there isn't one already
**Don't author a duplicate.** A requirements doc may exist under a different name (FRS,
SRS, "Functional Spec"), in a subdirectory, or outside the repo (shared drive,
SharePoint/Confluence, a Word/PDF). Search the obvious places, then **ask the user to
confirm or point you to any existing requirements/specification**. If one exists, offer to
**review/supplement** it rather than overwrite — author only what's genuinely missing.
Proceed to author a new URS only once the user confirms there is none (or it's inadequate).

## Step 2 — Gather what the requirements must reflect
This is a **single focused authoring pass — not a subagent fan-out.** Draw on the
always-available `gamp-advisor` and `part11-advisor` skills for regulatory framing.
Establish, citing evidence and **distinguishing stated fact from inference**:

- **Intended use & GxP context** — what the system is for, who uses it, the GxP-critical
  outcomes it must deliver, the process it supports. Take this from the user where stated;
  where not, **infer it from the system** and flag the inference.
- **Regulatory scope** — which apply: 21 CFR Part 11, EU GMP Annex 11, GAMP 5 (and its
  software category), AI/ML guidance (FDA / ISPE GAMP AI / EU Annex 22). Each applicable
  control the system must satisfy becomes a requirement.
- **Observed capabilities** — read the system (read-only) to see what it actually does:
  features, user roles, data it manages, integrations, audit/sign-off behaviour. Inferred
  requirements are derived from these and **must be flagged**.

## Step 3 — Author the requirements
Write the URS as a numbered set of requirements. **Each requirement is a single,
testable "shall" statement** so it can become a PQ acceptance criterion. For each:

| Field | Meaning |
|---|---|
| **ID** | `URS-NNN`, 3-digit, never reused (`-AI-` infix for AI/ML requirements). |
| **Requirement** | One thing the system **shall** do — plain English, what it is and why it matters, testable. |
| **Category** | functional · data integrity (ALCOA+) · security/access · audit trail · electronic signature · performance · regulatory · operational. |
| **Rationale / intended-use link** | why this is required — the business/GxP need or the control it satisfies. |
| **Regulatory linkage** | Part 11 § / Annex 11 cl. / GAMP control / AI-guidance item, where it derives from a regulation. |
| **Priority** | essential (GxP-critical) · important · desirable. |
| **Acceptance criterion** | the objective, measurable condition that = met — this is what PQ will test against. No magic numbers without a sourced basis. |
| **Source** | **stated** (given by the user/spec) · **inferred-from-behaviour** (derived from the system — flagged) · **regulatory-obligation** (required by an applicable control). |

Cover, at minimum: the intended-use workflows; data integrity & retention; access control
and roles; **audit trail** (Part 11 §11.10(e); Annex 11 cl.9); **electronic
signatures/approvals** where applicable (Part 11 §11.50/§11.70/§11.200; Annex 11 cl.14);
and, for any ML/AI capability, the model requirements (intended use / Context of Use,
consistency, accuracy, drift monitoring, human oversight) per the protocol.

**Source, never invent.** Where a requirement's threshold or value should come from a
business decision that hasn't been made, **state the requirement and flag the value as
"to be defined and approved"** — do not bake in an arbitrary number.

## Step 4 — Write the URS
Write to **`<project>/Qualification/requirements/URS.md`** by default (it sits inside the
single `Qualification/` folder, as a sourced input the pack traces to). Structure:

1. **Header** — system identified, intended use, regulatory scope, GAMP category, date,
   **DRAFT** stamp, and an explicit note that inferred requirements need owner confirmation.
2. **Requirements table(s)** — grouped by category, each row per Step 3.
3. **Traceability hooks** — note that each `URS-NNN` is the trace target for the matching
   `PQ-NNN` test-case, so the pack can link requirement → evidence.
4. **Assumptions & open questions** — every inference made and every value left "to be
   defined", listed for the owner to confirm or correct.
5. **Approval block** — Author / Reviewer / QA Approver signature lines, left unsigned.

Offer to also render the branded **Word** version (`python-docx`, ParaQualis palette)
alongside the Markdown. Markdown is the source of truth.

## Governance — non-negotiable
- The URS is **DRAFT — pending review and approval by appropriately qualified and
  authorized personnel.** It becomes a controlled specification only once reviewed,
  corrected, and approved by the system owner — it is *not* authoritative as generated.
- **Every inferred requirement is explicitly flagged**; the owner must confirm or correct
  it. Do not present inference as fact.
- This authoring tool is itself a GxP-impacting aid — it accelerates and structures the
  requirements, it does not own or approve them.

Lead with a one-line summary of what was authored (count by category, how many inferred vs
stated). No preamble.

# xQ Qualification Protocol

> The shared abstraction behind the `/qualify` command and the IQ/OQ/PQ subagents.
> Every qualification item — in any stage — is a **Requirement paired with an
> executable Test**, and the tests are first-class deliverables in the pack.
> (Abstraction lifted from RegCheck's validation-pack architecture, 2026-05-24.)

## The qualification test-case — the unit of the pack

Every IQ, OQ, or PQ item is **one test-case** with these fields:

| Field | Meaning |
|---|---|
| **ID** | Phase-prefixed, 3-digit, never reused: `IQ-001`, `OQ-042`, `PQ-009`. `-AI-` infix for AI-specific tests: `IQ-AI-003`. |
| **Requirement** | The single thing that must be true (the spec). |
| **Regulatory linkage** | Which control it satisfies — 21 CFR Part 11 §, EU Annex 11 clause, GAMP 5 category control, ISPE GAMP AI / EU Annex 22. Feeds the traceability matrix. |
| **Test method** | *How* it's verified — **automated** (an executable script/query, preferred) or **manual** (a witnessed step-by-step procedure). |
| **Test artifact** | The actual file shipped in the pack: a script in `scripts/<ID>.*`, or a manual procedure in `test_scripts/<ID>.md`. |
| **Acceptance criteria** | The result that = PASS — objective, no magic numbers. |
| **Expected result** | What a passing run produces. |
| **Execution record** | Actual result · executed-by · date · PASS/FAIL · evidence ref. **Blank until executed** — this is the evidence. |

## Test scripts ARE deliverables

The **script is the test**, its **output is the evidence**, and the **execution
record** is where the result and sign-off live. The pack therefore *contains* the
scripts. Examples:

- `IQ-003-versions.sh` — dumps runtime + dependency versions (version capture).
- `IQ-005-schema-check.sql` — asserts expected tables/columns/indexes/constraints exist; returns PASS/FAIL rows (schema verification).
- `IQ-007-seed-data.sql` — confirms required reference/priming rows are present.
- `OQ-012-min-config-check.sh` — verifies the minimum-usable configuration is set.
- `PQ-004-intended-use.sh` — exercises a real end-to-end workflow with representative data.

Verification scripts should emit a clear **PASS/FAIL** and be **read-only/safe**.
Destructive setup belongs in clearly-marked install steps, never in a verification test.

## Automated vs. manual — evidence strength

Mark each test-case `in_harness: true|false`. **Automated > manual:** automated tests
are re-runnable regression evidence; manual procedures get a witnessed execution
record. Prefer scripting anything that *can* be scripted.

## Regulatory traceability matrix

The pack includes a matrix: **control** (Part 11 §, Annex 11 clause, GAMP control,
AI-guidance item) → **test-case(s)** that evidence it → **status**. This is what an
inspector reads first. Source the control lists from the sibling commands —
`/cfr21-11:checklist`, `/eu-annex11:checklist`, `/gamp:assess`.

## AI/ML systems — the three-layer evidence model

For AI-enabled systems, PQ evidence has three **dependent** layers (each needs the one below):

1. **Consistency (within-model)** — same input → same output. Reproducibility.
   Necessary but not sufficient (a consistently-wrong answer is still wrong).
2. **Accuracy (cross-model / external ground truth)** — independent models converge,
   or real-world reference data agrees. The correctness signal.
3. **UX matches qualified behaviour** — what the user sees is the qualified mode and
   version (version stamp on every output; the qualified mode is the default, not an
   admin-only path).

Plus **calibration-as-evidence:** every model/prompt change is a calibration event
that must leave artifacts — recorded baselines, before/after deltas, and a documented
resolution method for each disagreement. The artifacts *are* the qualification
evidence. Discipline: single-variable changes, re-run after every change, snapshot
baselines.

## Pack layout

```
qualification/
  Qualification-Summary.md     # cover · verdict · traceability matrix · open items · approvals
  IQ.md  OQ.md  PQ.md          # the protocols — test-case tables per stage
  scripts/                     # executable tests (the evidence-gathering instruments)
  records/                     # execution records once run (the evidence)
```

## Governance

- Whole pack stamped **DRAFT — pending qualified-person review and approval.**
- **No skip-inflation** — a skipped/unexecuted test is not a pass (house standard).
- The generator itself is a **GxP-impacting tool that would require its own
  qualification**; it structures and accelerates evidence, it does not self-certify.

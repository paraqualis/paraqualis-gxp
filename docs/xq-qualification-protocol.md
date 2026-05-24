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

**Some qualification is always manual — especially the UI.** A test script can be a
**manual procedure**, and UI behaviour (layout, workflow, on-screen content, accessibility,
that what the user sees matches what was qualified) generally must be. So:
- **Capture UI requirements as their own test-cases** with step-by-step manual
  procedures and a **witnessed execution record** (operator, date, PASS/FAIL,
  screenshot/observation as evidence). Don't omit a control just because it can't be
  scripted — a manual UI test-case is still a test-case.
- A manual test is not a weaker *kind* of test; it's a different execution mode. It
  still has a requirement, acceptance criteria, and a recorded result.

## Focus areas that always need explicit test-cases

These are inspection hot-spots and the usual sources of real failure — never leave
them implicit. Each gets its own test-case(s), in the stage shown:

- **Edge conditions** (OQ + PQ) — boundaries, limits, empty/max, first/last, zero/
  overflow, concurrency, large or unusual-but-valid inputs.
- **Error conditions** (OQ + PQ) — invalid input, failed dependencies, timeouts,
  permission denials: handled gracefully **and logged** (no silent catch), with the
  defined behaviour verified.
- **Audit trails** (OQ tests generation/content; PQ tests the business-process trail) —
  secure, time-stamped, who/what/when, does not obscure prior entries, retained and
  reviewable (Part 11 §11.10(e); Annex 11 cl.9).
- **Electronic signatures & sign-offs** (OQ tests the mechanics; PQ tests the workflow)
  — manifestation (name/date-time/meaning), signature↔record linking, and the approval/
  sign-off workflow (Part 11 §11.50/§11.70/§11.200/§11.300; Annex 11 cl.14).

Two stage rules that follow from "every requirement needs a test":
- **OQ must evidence unit testing** — which tests exist, that they were executed, and
  the outcomes (pass/fail, coverage) — not merely that tests are present.
- **PQ must have use cases to test against** — if the requirements doc lacks them,
  author the use cases (flagged for owner confirmation) and test against them.

## Regulatory traceability matrix

The pack includes a matrix: **control** (Part 11 §, Annex 11 clause, GAMP control,
AI-guidance item) → **test-case(s)** that evidence it → **status**. This is what an
inspector reads first. Source the control lists from the sibling commands —
`/cfr21-11:checklist`, `/eu-annex11:checklist`, `/gamp:assess`.

## AI/ML systems — qualifying the model

Applies to **machine-learning models generally — not only LLMs.** Regulators now
require model-specific testing:
- **FDA** — *Considerations for the Use of AI to Support Regulatory Decision-Making
  for Drug and Biological Products* (FDA-2024-D-4689; draft Jan 2025, **finalizing
  Q2 2026**): a risk-based **7-step credibility framework** tied to a defined
  **Context of Use (COU)** — establish the COU, the model risk, and credibility
  evidence proportionate to that risk.
- **FDA/EMA** — *Guiding Principles of Good AI Practice in Drug Development* (Jan 2026, 10 principles).
- **ISPE GAMP Guide: AI** (Jul 2025) and **EU draft Annex 22 (AI)** (Jul 2025).

### What must be tested (define acceptance outcomes for each)

| Theme | Applies to | What the test does | Acceptance outcome (must be defined) |
|---|---|---|---|
| **Consistency — within-model** | all ML, LLMs | run N passes on the same input; measure agreement | e.g. min pairwise coverage ≥ threshold; severity/label agreement ≥ defined % |
| **Consistency — cross-model / cross-seed** | all ML, LLMs | two models/seeds on the same input converge | cross-coverage ≥ defined %; label agreement ≥ defined % |
| **Drift** | all ML | monitor performance vs. the training/validation baseline over time and as input distribution shifts | defined re-validation trigger thresholds; monitoring in place |
| **Accuracy vs. ground truth** | all ML | predefined metrics on a held-out/representative set | accuracy/precision/recall/AUC ≥ defined targets |
| **Hallucination / fabrication** | **LLMs** | verify outputs against cited source / ground truth; flag unsupported claims | defined max unsupported-claim rate; GxP-critical outputs require verification |
| **Explainability & human oversight** | all ML | rationale available proportionate to risk; human-in-the-loop control | defined per COU/risk |

**Reference battery (worked example, from RegCheck's admin consistency tooling):**
within-model N-pass batch ("Tool B") → min/median/mean **pairwise coverage** (default
pass threshold **≥ 0.70**), **severity agreement ≥ 75%**, **category agreement ≥ 70%**,
coverage **saturation curve**, span **Jaccard**; cross-model comparison ("Tool C") →
cross-coverage **≥ 70%** each direction; every disagreement carries a documented
**resolution method** (unanimous / vote / coupling / judge / debate). These numbers are
*examples* — **each system must define and justify its own acceptance thresholds.**

### Evidence layers (each depends on the one below)
1. **Consistency** (within-model) — reproducible. Necessary, not sufficient (a
   consistently-wrong answer is still wrong).
2. **Accuracy** (cross-model / external ground truth) — the correctness signal.
3. **UX matches qualified behaviour** — the user sees the qualified mode + version
   (version stamp on outputs; qualified mode is the default, not an admin-only path).

Plus **calibration-as-evidence:** every model/prompt/retraining change is a
calibration event that must leave artifacts — recorded baselines, before/after deltas,
documented resolution per disagreement. The artifacts *are* the qualification evidence.
Discipline: single-variable changes, re-run after every change, snapshot baselines.

## Pack layout

Write the pack to a **standalone `Qualification/` directory** (a deliverable — do NOT
write into the system under test, which was examined read-only):

```
Qualification/
  docs/                        # Markdown source-of-truth + generated renderings
    Qualification-Summary.md   #   cover · verdict · traceability matrix · open items · approvals
    IQ.md  OQ.md  PQ.md        #   test-case tables per stage
    *.docx                     #   branded ParaQualis Word (generated)
    *-Qualification-Pack.xlsx  #   workbook: a sheet per xQ stage + Summary + Traceability
  scripts/                     # executable tests (the evidence-gathering instruments)
  records/                     # execution-record templates → filled records = evidence
  build_docx.py  build_xlsx.py # regenerate Word/Excel from the Markdown
```

**Output formats — Markdown is the source of truth; Word and Excel are *generated*
renderings, never hand-maintained:**
- **Markdown** (`docs/*.md`) — versionable, diffable, the canonical content.
- **Word** (`docs/*.docx`) — branded ParaQualis (deep-blue headings/table headers, see
  `~/.claude/brand_colors.md`), via `python-docx`; for the client to read/sign.
- **Excel** (`docs/*-Qualification-Pack.xlsx`) — one sheet per xQ stage plus Summary and
  Traceability, via `openpyxl`; QA teams work the trace matrix here.

`build_docx.py` and `build_xlsx.py` ship inside the pack so it is self-rebuilding:
`python3 build_docx.py && python3 build_xlsx.py` after any Markdown edit. (`pandoc` is
NOT required; both builders use pure-Python libraries.)

## Governance

- Whole pack stamped **DRAFT — pending review and approval by appropriately qualified and authorized personnel.**
- **No skip-inflation** — a skipped/unexecuted test is not a pass (house standard).
- The generator itself is a **GxP-impacting tool that would require its own
  qualification**; it structures and accelerates evidence, it does not self-certify.

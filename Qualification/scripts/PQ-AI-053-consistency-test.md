# PQ-AI-053 — AI generation consistency (same inputs → materially equivalent coverage)

**Traces:** URS-AI-053 · ParaQualis-authored, pending owner confirmation.
**Test method:** MANUAL / SEMI-AUTOMATED procedure — requires repeated **live** LLM runs of the engine, which cannot be exercised from a static script.
**Regulatory linkage:** ISPE GAMP Guide: AI (consistency / within-model reproducibility); EU draft Annex 22; protocol §AI (xq-qualification-protocol.md:167-182).
**Status:** **NOT-YET-EXECUTED and threshold-capped** — the acceptance threshold is **to be defined and approved** for this Context of Use. This test-case is defined here but cannot PASS until (a) the threshold is set and (b) the live runs are performed. It is explicitly **not** a pass.

## Why this matters (plain English)
If the engine is given the same system to qualify twice, it should produce materially the same
qualification coverage — the same requirements covered by equivalent test-cases. Consistency is
the base evidence layer for any AI tool: a tool whose output changes substantially run-to-run
cannot be relied on. (Consistency alone is necessary, not sufficient — a consistently-wrong
answer is still wrong; accuracy is a separate layer.)

## The undefined threshold (a gap, not a baked number — see GPQ-004)
The protocol's *worked example* uses min pairwise coverage ≥ 0.70, severity agreement ≥ 75%,
category agreement ≥ 70% (xq-qualification-protocol.md:176-182) — but these are **examples**.
Per the protocol and URS-AI-053, **each system must define and justify its own threshold.** No
number is baked here. The threshold MUST be defined and approved by the system owner before this
test can be executed or pass.

## Procedure (once the threshold is approved)
1. Fix the target system, the engine version/model, and all inputs (single-variable discipline).
2. Run `/qualify:build` against the same target **N times** (N to be defined, e.g. ≥ 3), each in a
   clean context, capturing the generated PQ test-case set each run.
3. For each pair of runs compute **pairwise coverage**: the fraction of requirements (URS-NNN)
   covered by an equivalent test-case in both runs (a documented matching method — exact ID,
   then requirement-text equivalence).
4. Compute min / median / mean pairwise coverage and the per-requirement agreement.
5. Record every disagreement with a documented **resolution method** (the artifacts ARE the
   evidence — calibration discipline, protocol §AI).

## Acceptance criteria
- Min pairwise coverage **≥ the approved threshold** (value **to be defined and approved** —
  do NOT assume a number).
- Each disagreement carries a documented resolution.

## Expected result
Repeated runs on the same target produce equivalent test-case coverage at or above the approved
threshold.

## Execution record (BLANK — NOT-YET-EXECUTED; this is NOT a pass)
| Field | Entry |
|---|---|
| Approved threshold (must be set first) | _to be defined and approved_ |
| N (runs) | |
| Min / median / mean pairwise coverage | |
| Disagreements + resolution method | |
| Executed by | |
| Date / time (UTC) | |
| PASS / FAIL / NOT-YET-EXECUTED | NOT-YET-EXECUTED (threshold undefined) |
| Evidence reference | |
| Reviewer | |
| QA approver | |

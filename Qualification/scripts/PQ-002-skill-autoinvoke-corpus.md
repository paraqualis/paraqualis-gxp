# PQ-002 — Advisory skills auto-invoke and answer from their bundled reference corpus

**Traces:** URS-002 · ParaQualis-authored, pending owner confirmation.
**Test method:** MANUAL (witnessed procedure — auto-invocation is an LLM runtime behaviour that cannot be asserted by a static script).
**Regulatory linkage:** GAMP 5 (Cat 5 functional spec); 21 CFR Part 11; ISPE GAMP AI (grounded output / hallucination control).

## Why this matters (plain English)
The two advisory skills (`gamp-advisor`, `part11-advisor`) are meant to switch on by themselves
when a user asks an in-scope question, and to answer from the regulatory text bundled with the
skill — not from the model's general memory. This test confirms (a) the right skill activates on
a representative question, and (b) the answer is grounded in the bundled reference files, so the
advice is traceable to a source rather than invented.

## Pre-conditions
- The toolkit is installed (`./install.sh` has linked `skills/` into `~/.claude/skills/`).
- A fresh Claude Code session.
- Reference corpora present (sourced):
  - `skills/gamp-advisor/reference/gamp5-category-framework.md`
  - `skills/gamp-advisor/reference/ai-ml-validation.md`
  - `skills/part11-advisor/reference/21-cfr-part-11.md`

## Procedure
1. In a fresh session ask: *"Is a configured LIMS that we've written custom calculation scripts
   for GAMP category 4 or 5, and how much validation rigor does it need?"*
   - Observe which skill activates. **Expected:** `gamp-advisor` auto-invokes (it matches the
     skill `description` — see `skills/gamp-advisor/SKILL.md:2`).
2. Confirm the answer references GAMP category definitions consistent with the bundled corpus
   `skills/gamp-advisor/reference/gamp5-category-framework.md`. Capture the answer text.
3. In a fresh session ask: *"What does 21 CFR Part 11 require for audit trails on a closed
   system, citing the paragraph?"*
   - **Expected:** `part11-advisor` auto-invokes (matches `skills/part11-advisor/SKILL.md:2`)
     and cites a §11.10 paragraph traceable to `skills/part11-advisor/reference/21-cfr-part-11.md`.
4. Spot-check one cited paragraph against the bundled reference file — confirm the wording matches
   the corpus and is not a hallucinated regulation.

## Acceptance criteria
- The correct skill auto-invokes for each representative prompt (no manual command typed).
- Each answer is grounded in / consistent with the bundled `reference/` corpus, and at least one
  cited control is verified against the reference file (no invented regulation).

## Expected result
Both skills activate on their representative prompts and produce answers that trace to the bundled
corpora; the verified citation matches the reference file.

## Execution record (BLANK until executed — an unexecuted test is NOT a pass)
| Field | Entry |
|---|---|
| Actual result (gamp-advisor activation + grounding) | |
| Actual result (part11-advisor activation + citation match) | |
| Executed by | |
| Date / time (UTC) | |
| PASS / FAIL | |
| Evidence reference (transcript / screenshot) | |
| Reviewer | |
| QA approver | |

# PQ-005 — The eCFR commands return LIVE regulatory content for a known citation

**Traces:** URS-006 · ParaQualis-authored, pending owner confirmation.
**Test method:** MANUAL (witnessed) — the eCFR commands drive Claude to fetch live content via `WebFetch`; the fetch + comparison is observed, not asserted by a local script.
**Regulatory linkage:** 21 CFR Part 11; EU GMP Annex 11 (correct/current controls).

## Why this matters (plain English)
Regulatory advice is only safe if it reflects the CURRENT regulation, not a stale copy baked
into the tool. The `eCFR` commands are designed to pull text/structure/search/comparison straight
from the official eCFR service at run time. This test confirms a representative command returns
content that matches the live source for a citation whose text is known.

## Source of the live-fetch design (cited)
- `commands/eCFR/text.md:8` — "Fetch and display the full regulatory text ... live from" eCFR.
- `commands/eCFR/text.md:17-21` — fetches via the eCFR API host `www.ecfr.gov/api/versioner/...`
  using `WebFetch`, dated to "TODAY" so the content is current.

## Procedure
1. Run `/eCFR:text` for a known citation, e.g. **21 CFR 11.10**.
2. Observe that Claude performs a live `WebFetch` to the eCFR API host (URL visible in the
   transcript) rather than reciting from memory.
3. Independently open the live source in a browser:
   `https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11/subpart-B/section-11.10`
4. Compare the returned text of §11.10 against the live page — headings and at least the opening
   controls (a)-(d) must match the live wording.
5. Optionally run `/eCFR:search` for a phrase (e.g. "audit trail") and confirm the returned
   citations match a live full-text search on the same term.

## Acceptance criteria
- The command performs a live fetch (observable in the transcript), not a cached recital.
- The returned §11.10 text matches the live eCFR source on the test date (headings + sampled
  paragraphs identical).

## Expected result
The eCFR command returns content identical to the live eCFR source for the known citation.

## Execution record (BLANK until executed — an unexecuted test is NOT a pass)
| Field | Entry |
|---|---|
| Live fetch observed (URL in transcript)? | |
| §11.10 returned text matches live source? | |
| Executed by | |
| Date / time (UTC) | |
| PASS / FAIL | |
| Evidence reference (transcript + live-source screenshot) | |
| Reviewer | |
| QA approver | |

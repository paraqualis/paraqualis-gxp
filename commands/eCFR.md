---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Show the current structure of any CFR part (any Title) — subparts and section headings — pulled live from the eCFR
argument-hint: <CFR citation, e.g. "21 CFR 11", "40 CFR Part 261", or "21 CFR 11.10">
---

Fetch and display the **current structure** of the CFR citation below, live from the
eCFR. This is any Title — not just 21.

## Citation
$ARGUMENTS

## How to retrieve it (do this — a slash command cannot fetch on its own)

1. **Parse the citation** into:
   - **Title** number (e.g. `21`, `40`, `12`)
   - **Part** number (e.g. `11`, `261`) — strip the word "Part" if present
   - **Section** number if one is given (e.g. `11.10`) — optional

2. **Fetch from the eCFR *API*** with `WebFetch`. Use the API host, NOT the
   `www.ecfr.gov` HTML pages (those are bot-blocked and redirect). Pattern:

   ```
   https://www.ecfr.gov/api/versioner/v1/full/<TODAY>/title-<TITLE>.xml?part=<PART>
   ```

   - `<TODAY>` = today's date as `YYYY-MM-DD`. If that date 404s (no edition yet),
     retry with the most recent prior weekday.
   - Part-only is sufficient — you do NOT need the chapter/subchapter.
   - Ask the fetch to return: Part title, the AUTHORITY and SOURCE citations, and
     every subpart (letter + heading) and section (number + heading) in order.

3. If the part is large and the fetch truncates, that's fine — you only need the
   **heading skeleton** (subparts + section numbers/headings), which is compact.
   Re-fetch asking specifically for just the subpart and section headings if needed.

## Present it as

1. **Header line** — `Title <N> CFR Part <P> — <Part Title>`, plus Authority and
   Source (with the source date) on their own lines.
2. **Structure table** — columns: Subpart (letter + heading) · § · Section heading,
   in document order.
3. **Note on granularity** — if relevant, remind that lettered controls like
   `§11.10(a)` are *paragraphs within* a section, below the eCFR's section level.
4. **If a specific section was cited** (e.g. `11.10`), additionally fetch and show
   that section's own internal structure — its lettered/numbered paragraphs and
   their subject — rather than just the part skeleton.

Lead with the header line. Keep it clean and citable. No preamble.

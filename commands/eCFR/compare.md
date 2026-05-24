---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Compare a CFR section/part between two dates (point-in-time) and show exactly what wording changed, from the eCFR
argument-hint: <citation + two dates, e.g. "21 CFR 11.10 between 2000-01-01 and today">
---

Show what **changed in the wording** of the CFR citation below between two points in
time, using the eCFR's point-in-time editions.

## Citation and dates
$ARGUMENTS

## How to retrieve it (a slash command cannot fetch on its own)

1. **Parse** into Title, Part, optional Section, and the two dates (`<DATE_A>` =
   earlier, `<DATE_B>` = later; "today" → today's `YYYY-MM-DD`).
2. **Confirm whether it even changed** in the window via the version-history API:
   ```
   https://www.ecfr.gov/api/versioner/v1/versions/title-<TITLE>.json?part=<PART>
   ```
   Look for amendment_dates between the two dates for the relevant section(s).
3. **Fetch the text at each date** with `WebFetch`, twice — once per date:
   ```
   https://www.ecfr.gov/api/versioner/v1/full/<DATE_A>/title-<TITLE>.xml?part=<PART>[&section=<SECTION>]
   https://www.ecfr.gov/api/versioner/v1/full/<DATE_B>/title-<TITLE>.xml?part=<PART>[&section=<SECTION>]
   ```
   If a date predates the eCFR's coverage or 404s, say so and use the earliest
   available edition, noting the substitution.

## Present it as

1. **Verdict line** — did it change between `<DATE_A>` and `<DATE_B>`? If unchanged,
   say so plainly and stop (don't manufacture a diff).
2. **Amendment markers** — list the amendment_date(s) in the window from step 2.
3. **What changed** — for each changed passage, show a clear **before → after**:
   quote the old wording and the new wording (verbatim), paragraph by paragraph.
   Mark additions, deletions, and rewordings. Do not paraphrase the regulatory text.
4. **So-what** — one or two sentences on the practical/compliance significance of the
   change, clearly labeled as interpretation.

Lead with the verdict line. Quote both versions faithfully; never invent regulatory text.

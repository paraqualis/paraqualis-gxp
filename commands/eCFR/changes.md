---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Show the amendment history of a CFR part (any Title) — which sections changed and when — from the eCFR
argument-hint: <CFR part, e.g. "21 CFR 11"; optionally "since 2020" to limit the window>
---

Show the **amendment history** of the CFR part below — which sections were changed,
when, and whether the change was substantive — live from the eCFR. Useful for
tracking regulatory drift.

## Part (and optional window)
$ARGUMENTS

## How to retrieve it (a slash command cannot fetch on its own)

1. **Parse** the citation into Title and Part, and any "since <date>" the user gave.
2. **Fetch via the eCFR version-history API** with `WebFetch` (API host, not the
   bot-blocked HTML site):

   ```
   https://www.ecfr.gov/api/versioner/v1/versions/title-<TITLE>.json?part=<PART>
   ```

   - To limit the window, add `&issue_date[gte]=<YYYY-MM-DD>`.
   - Each entry has: `identifier` (section), `name` (heading), `amendment_date`,
     `issue_date`, `substantive` (bool), `removed` (bool), `subpart`. Ask the fetch
     to return these for every entry.

## Present it as

1. **Summary line** — part title, how many sections have changes in the window, and
   the date of the most recent substantive amendment.
2. **Change table**, most recent `amendment_date` first:

   | § | Section heading | Amendment date | Issue date | Substantive? | Notes |
   |---|---|---|---|---|---|

   Mark `removed` sections clearly. Treat non-substantive entries (typos, formatting)
   as such so real regulatory changes stand out.
3. **Drift read** — one or two sentences: is this part stable or actively evolving,
   and which sections are the moving parts? Point to `/eCFR:compare` to see exact
   wording changes for any section.

Lead with the summary line. Report only dates the API returns — never infer amendments.

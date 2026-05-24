---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Full-text search the eCFR for a term or phrase and return the matching citations with excerpts
argument-hint: <search terms, optionally scoped — e.g. "audit trail in 21 CFR" or "data integrity Title 21 Part 211">
---

Run a **full-text search of the eCFR** for the query below and return the regulatory
provisions that match, with citations and excerpts.

## Query
$ARGUMENTS

## How to retrieve it (a slash command cannot fetch on its own)

1. **Separate** the search terms from any scope the user gave (a Title and/or Part,
   e.g. "in 21 CFR 211" → Title 21, Part 211). Scope is optional.
2. **Fetch via the eCFR Search API** with `WebFetch` (URL-encode the query; spaces → `+`):

   ```
   https://www.ecfr.gov/api/search/v1/results?query=<TERMS>&per_page=20
   ```

   - If a Title was given, add `&hierarchy[title]=<N>`; if a Part, add `&hierarchy[part]=<P>`.
   - Ask the fetch to return, per result: the hierarchy (title/part/subpart/section),
     the section heading, the highlighted `full_text_excerpt`, and the relevance score;
     plus the total match count from `meta`.

## Present it as

1. **Result count line** — how many provisions matched (and the scope applied).
2. **Ranked list** — most relevant first, up to ~15. Each item:
   - **Citation** — `Title <N> CFR § <section>` + section heading
   - **Excerpt** — the matching snippet, with the matched terms shown in **bold**
     (convert the API's `<strong>` tags to bold; don't show raw HTML).
3. **Tip line** — if results look too broad/narrow, suggest scoping by Title/Part or
   refining the phrase. Note that `/eCFR:text` will pull the full text of any hit.

Lead with the count line. Report only what the API returned — do not fabricate citations.

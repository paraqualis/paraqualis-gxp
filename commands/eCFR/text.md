---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Fetch the full current regulatory TEXT of a CFR section or part (any Title), live from the eCFR
argument-hint: <CFR citation, e.g. "21 CFR 11.10" (a section) or "21 CFR 11" (a whole part)>
---

Fetch and display the **full regulatory text** of the CFR citation below, live from
the eCFR. Any Title — not just 21.

## Citation
$ARGUMENTS

## How to retrieve it (a slash command cannot fetch on its own)

1. **Parse** the citation into Title, Part, and (if given) Section (e.g. `11.10`).
2. **Fetch via the eCFR API** with `WebFetch` — the API host, NOT the bot-blocked
   `www.ecfr.gov` HTML pages:

   ```
   https://www.ecfr.gov/api/versioner/v1/full/<TODAY>/title-<TITLE>.xml?part=<PART>
   ```

   - `<TODAY>` = today's date `YYYY-MM-DD`; if it 404s, retry the most recent weekday.
   - If a **section** was cited, append `&section=<SECTION>` (e.g. `&section=11.10`)
     to pull just that section; otherwise you get the whole part.
   - Ask the fetch to return the verbatim text with its paragraph structure intact.

3. If a whole part is large and truncates, fetch section by section, or tell the user
   it's large and ask which section(s) they want.

## Present it as

1. **Citation header** — `Title <N> CFR § <section>` (or Part), with the section
   heading and the SOURCE date.
2. **The text, verbatim**, preserving the lettered/numbered paragraph hierarchy
   ((a), (1), (i)…) exactly as written. Do not paraphrase — this is the legal text.
3. If asked or useful, follow the verbatim text with a brief **plain-language gloss**
   clearly labeled as interpretation, kept separate from the quoted regulation.

Lead with the citation header. Quote faithfully; never invent or alter regulatory text.

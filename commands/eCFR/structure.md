---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Show the structure (headings only, no content) two levels below any eCFR reference — any Title, any level
argument-hint: <any CFR reference — e.g. "Title 21", "21 CFR Chapter I", "21 CFR 11", "21 CFR 11 Subpart B", "21 CFR 11.10">
---

Show the **structure only** — no regulatory text — for **exactly two levels below**
the eCFR reference given. Output the identifier and heading of each node and nothing
else.

## Reference
$ARGUMENTS

## What "two levels down" means

Identify the level of the reference, then list its direct children (level 1) and
their children (level 2). Stop at level 2.

| Reference is a… | Level 1 | Level 2 |
|---|---|---|
| Title | Chapters | Subchapters |
| Chapter | Subchapters | Parts |
| Subchapter | Parts | Subparts |
| Part | Subparts | Sections |
| Subpart | Sections | (section paragraphs, if labeled — else none) |
| Section | Paragraphs (a),(b)… | Sub-paragraphs (1),(2)… |

## How to retrieve it (a slash command cannot fetch on its own)

1. **Parse** the reference into Title + the lowest identifier given (chapter / part /
   subpart / section).
2. **Fetch the eCFR structure (no-content) API** with `WebFetch` — the API host, not
   the bot-blocked HTML site:

   ```
   https://www.ecfr.gov/api/versioner/v1/structure/<TODAY>/title-<TITLE>.json
   ```

   `<TODAY>` = today's `YYYY-MM-DD`; if it 404s, retry the most recent weekday.
   This returns the full nested hierarchy with `type`, `identifier`, `label`, and
   `children` — labels only, no text. **Instruct the fetch to navigate to the
   referenced node and return only that node's children and grandchildren** (labels +
   identifiers), so the response stays small even for large Titles.
3. For a **Section** reference, the structure API may stop at the section; get its
   paragraph headings from the section's own markup via
   `…/full/<TODAY>/title-<TITLE>.xml?part=<PART>&section=<SECTION>` and list the
   paragraph designations + their subject headings only (still no body text).

## Present it as

1. **Header line** — the reference, resolved to its full label (e.g. `Title 21 ›
   Chapter I › Part 11 — Electronic Records; Electronic Signatures`).
2. **A two-level indented tree** — each line is `<identifier> — <heading>` and
   nothing else. Level 2 indented under its level-1 parent. Do NOT descend past
   level 2, and do NOT include any regulatory text, excerpts, or commentary.
3. If a level has no children (e.g. a section with no labeled paragraphs), say so in
   one line rather than inventing structure.

Output only the header line and the tree. No preamble, no content, no analysis.

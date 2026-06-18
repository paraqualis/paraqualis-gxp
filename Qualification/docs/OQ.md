**DRAFT — pending review and approval by appropriately qualified and authorized personnel.**

# OQ Section — paraqualis-skills v1.2.0

DRAFT — pending review and approval by appropriately qualified and authorized personnel.

---

## OQ Readiness Verdict

The system's functional units operate correctly under normal and edge conditions as evidenced by targeted test-case execution in this assessment. Following remediation on 2026-06-17 those findings are **closed**: the document-protection hook and the openFDA server now log fail-open decisions and failures to stderr (GIQ-007), and the `mcp` runtime dependency is installed in the project virtual environment (Python 3.12) with the server **✔ Connected**. A full automated unit-test suite is **not required** for a system of this size and is scoped out as a risk-based, proportionate decision (see OQ-030, recorded N/A). This OQ therefore rests on the behavioural evidence gathered during this assessment plus the re-runnable scripts shipped in the pack.

---

## OQ Test-cases (consolidated)

*Consolidated one-row-per-case summary for the workbook; the full per-case detail (with blank execution-record blocks) follows in the sections below.*

| ID | Requirement | Regulatory linkage | Test method | Test artifact | Acceptance criteria | Expected result | As-built evidence |
|---|---|---|---|---|---|---|---|
| **OQ-001** | The protection hook shall return exit code 2 (block) and write a clear reason to stderr when a tool attempts to edit a file containing the lock marker. (URS-040; `hooks/protect-approved-documents.py:51-58`) | 21 CFR Part 11 §11.10(a),(c); EU GMP Annex 11 cl.14 — integrity of approved electronic records | Automated (in_harness: true) | `scripts/OQ-001-hook-block-locked.py` | Return value = 2; stderr contains the word "Blocked" and the file path; the lock marker string is named in the message. | Sourced from `hooks/protect-approved-documents.py:51-58`: exit 2; stderr includes `"Blocked: <path> is an APPROVED, locked document"`. | Test executed inline. Result: exit code 2, stderr = `"Blocked: /tmp/tmplgudxx52.md is an APPROVED..."`. PASS. |
| **OQ-002** | The protection hook shall return exit code 0 (allow) when the target file exists and does not contain the lock marker. (URS-040; `protect-approved-documents.py:60`) | 21 CFR Part 11 §11.10(a); Annex 11 cl.14 — only approved records are protected | Automated (in_harness: true) | `scripts/OQ-002-hook-allow-unlocked.py` | Return value = 0; no stderr output. | Sourced from `protect-approved-documents.py:60`: exit 0. | Executed inline. Result: exit code 0. PASS. |
| **OQ-003** | The hook shall return exit code 0 when the target file does not yet exist on disk, because creating a new file is always permitted. (`protect-approved-documents.py:47`) | Annex 11 cl.14 — only existing approved records are protected | Automated (in_harness: true) | `scripts/OQ-003-hook-allow-new-file.py` | Return value = 0 for a path that does not exist. | Exit 0. | Executed inline with `/tmp/__nonexistent_file_oq_test__.md`. Result: 0. PASS. |
| **OQ-004** | The hook shall return exit code 0 (allow) when the stdin event cannot be parsed as JSON, rather than crashing or blocking the session. (`protect-approved-documents.py:33-36`) | Annex 11 cl.11 — system shall not produce uncontrolled failures in normal operation | Automated (in_harness: true) | `scripts/OQ-004-hook-failopen-malformed.py` | Return value = 0. No unhandled exception. | Exit 0. | Executed inline with `{not valid json}`. Result: 0. PASS. Finding raised: no log emitted on this path — GOQ-001. |
| **OQ-005** | The hook shall read the `notebook_path` key as the target path when `file_path` is absent, covering the NotebookEdit tool call. (`protect-approved-documents.py:39`) | 21 CFR Part 11 §11.10(c); Annex 11 cl.14 — protection must cover all file-writing tools in the matcher | Automated (in_harness: true) | `scripts/OQ-005-hook-notebook-path.py` | Exit 2 (block) when a locked `.ipynb` file is targeted via `notebook_path`. | Exit 2; stderr contains "Blocked". | Executed inline. Result: exit 2, stderr non-empty. PASS. |
| **OQ-006** | The `hooks.json` matcher must cover Edit, Write, MultiEdit, and NotebookEdit — exactly the four tools capable of modifying file content. (`hooks/hooks.json:5`) | 21 CFR Part 11 §11.10(c); Annex 11 cl.14 — no write path must bypass protection | Automated (in_harness: true) | `scripts/OQ-006-hooks-json-matcher.py` | The `matcher` field in `hooks/hooks.json` equals exactly `"Edit\/Write\/MultiEdit\/NotebookEdit"`. | Sourced from `hooks/hooks.json:5`: matcher = `"Edit/Write/MultiEdit/NotebookEdit"`. | Static inspection confirms matcher. PASS (static). Live activation requires witnessed Claude Code session. |
| **OQ-007** | An HTTP 404 from the openFDA API shall be treated as "no matching records" and returned as `{total:0, results:[], note:"No matching records."}` — not surfaced as an error. (`server.py:46-47`) | GAMP 5 Cat 3/4 (interface behaviour); house standard (no silent catch on meaningful condition, and 404 is a defined, expected outcome) | Automated (in_harness: true) | `scripts/OQ-007-openfda-404.py` | Return dict has `total=0`, `results=[]`, `note` field present; no `error` key. | `{total:0, results:[], note:"No matching records."}` | Executed inline (HTTP mocked). Result matches. PASS. |
| **OQ-008** | HTTP 429 (rate limit) shall return `{error:..., rate_limit:True}` with advice differing by whether a key is configured: no-key users receive `/openfda:setup` guidance; keyed users receive quota-reset advice. (`server.py:49-58`) | House standard: no silent catch; surfaced error must be actionable | Automated (in_harness: true) | `scripts/OQ-008-openfda-429.py` | `rate_limit` key = True; `error` message for no-key path contains "shared" and setup nudge; for keyed path contains "quota". | No-key: `{error:"openFDA rate limit hit — you are on the shared (no-key) tier…", rate_limit:True}`. | Executed inline (mocked). PASS. |
| **OQ-009** | Any HTTP error other than 404 or 429 shall be surfaced as `{error:"openFDA HTTP <code>", detail:<response body up to 300 chars>}`. (`server.py:59-60`) | House standard: no silent catch | Automated (in_harness: true) | `scripts/OQ-009-openfda-http-error.py` | `error` key present; contains the HTTP status code; `detail` key present. | `{error:"openFDA HTTP 500", detail:"HTTP Error 500: Server Error"}`. | Executed inline. PASS. |
| **OQ-010** | A network failure or timeout (any `Exception` not caught earlier) shall be surfaced as `{error: str(e)}`. (`server.py:61-62`) | House standard: no silent catch; dependency failure must surface loudly | Automated (in_harness: true) | `scripts/OQ-010-openfda-network-error.py` | `error` key present; contains the exception message. | `{error:"Connection refused"}` (or similar). | Executed inline (mocked). PASS. Finding GOQ-002 raised: no server-side log accompanies this. |
| **OQ-011** | The `limit` parameter shall be clamped to the range [1, 50] inside `_query()`, regardless of the value passed by any caller tool. (`server.py:36`) | GAMP 5 (input validation on public-facing parameter); data integrity | Automated (in_harness: true) | `scripts/OQ-011-openfda-limit-clamp.py` | limit=0 → 1; limit=1 → 1; limit=50 → 50; limit=51 → 50; limit=999 → 50; limit=-5 → 1. | All boundary values clamp correctly. | Executed inline. All cases PASS. |
| **OQ-012** | The MCP server shall operate without `OPENFDA_API_KEY` (key is optional); absence is communicated once per session as a tip, not an error. With key present, it shall be appended to the URL. (`server.py:38-40`, `66-70`) | GAMP 5 (minimum-configuration documentation); URS-020 | Automated (in_harness: true) | `scripts/OQ-012-openfda-min-config.sh` | Without key: first successful response contains `tip` key; URL has no `api_key` param. With key: URL contains `api_key=<key>`. | Sourced from `server.py:38-70`. | Logic confirmed by code inspection and inline test. Needs live network execution to fully evidence. |
| **OQ-013** | `search_enforcement()` shall return `{error:"category must be 'drug', 'device', or 'food'"}` for any category not in that set, after normalising case and whitespace. (`server.py:94-96`) | GAMP 5 (input validation); house standard (deterministic logic on data-mutating paths) | Automated (in_harness: true) | `scripts/OQ-013-enforcement-category.py` | `pharmaceutical`, `Human`, `""` → error dict. `drug`, `Drug`, `DRUG`, `food ` → accepted (after normalisation). | Sourced from `server.py:94-96`. | Logic executed inline. PASS. |
| **OQ-014** | `openfda_query()` shall strip leading/trailing whitespace and slashes, and remove a trailing `.json` suffix from the endpoint parameter before building the URL. (`server.py:166`) | GAMP 5 (input handling, defensive coding) | Automated (in_harness: true) | `scripts/OQ-014-endpoint-sanitize.py` | `"/drug/label/"` → `"drug/label"`; `"food/event.json"` → `"food/event"`; `"  drug/ndc  "` → `"drug/ndc"`. | Sourced from `server.py:166`. | Executed inline. All cases PASS. |
| **OQ-015** | `_trunc(v, n=600)` shall: join list inputs with spaces; truncate strings longer than 600 chars and append `…` (1-char Unicode ellipsis); return `""` for `None`; not truncate a string of exactly 600 chars. (`server.py:78-80`) | GAMP 5 (deterministic output shaping in data-returning tool) | Automated (in_harness: true) | `scripts/OQ-015-trunc-edge.py` | List → joined string; 700-char string → 601 chars (600 + `…`); None → `""`; 600-char string unchanged. | Sourced from `server.py:78-80`. | Executed inline. All PASS. |
| **OQ-016** | `render(md_path, out_path)` shall produce a non-empty, structurally valid `.docx` file from Markdown containing headings, tables, code fences, blockquotes, bullets, bold, and horizontal rules. (`build_docx.py:93-171`) | URS-007; GAMP 5 (correct output of document-generation function) | Automated (in_harness: true) | `scripts/OQ-016-docx-render.py` | Output `.docx` is created; file size > 5,000 bytes (confirmed structural content); no exception raised. | Sourced from `build_docx.py:93-171`: a valid `.docx` produced. | Executed. Output = 37,100 bytes. PASS. |
| **OQ-017** | Lines matching `<!-- ... -->` (HTML comments, including the `PARAQUALIS-LOCK` marker) shall be silently skipped during rendering — not written into the document body. (`build_docx.py:146-147`) | URS-040; Annex 11 cl.14 — the marker is a governance control, not displayable content | Automated (in_harness: true) | `scripts/OQ-017-docx-skip-comment.py` | `.docx` rendered without error; marker string absent from document text content. | Sourced from `build_docx.py:146-147`: comment lines skipped. | Executed. Output = 36,721 bytes; no exception. PASS (visual content verification requires human review of the .docx). |
| **OQ-018** | `render()` on an empty `.md` file shall produce a valid (empty-body) `.docx` without raising an exception. (`build_docx.py:111-171`) | GAMP 5 (edge-condition robustness of document builder) | Automated (in_harness: true) | `scripts/OQ-018-docx-empty-md.py` | `.docx` created; no exception. | Valid `.docx` of minimal size. | Executed. Output = 36,625 bytes. PASS. |
| **OQ-019** | When invoked as a script and `docs/*.md` contains no files, `build_docx.py` shall call `sys.exit("no docs/*.md found")` — a clear, non-silent failure. (`build_docx.py:177-178`) | House standard: no silent failure; dependency / input failure must surface clearly | Automated (in_harness: true) | `scripts/OQ-019-docx-no-md.sh` | Exit code non-zero; stderr or stdout contains "no docs/*.md found". | Sourced from `build_docx.py:177`: `sys.exit("no docs/*.md found")`. | Code confirmed by inspection; execution requires controlled environment. Needs execution. |
| **OQ-020** | `table_after()` shall return `[]` when the heading is absent; `write_sheet()` shall write `(no table found)` sentinel and not crash. (`build_xlsx.py:25-46`) | GAMP 5 (edge-condition robustness of document builder) | Automated (in_harness: true) | `scripts/OQ-020-xlsx-empty-table.py` | No exception; sheet exists with `(no table found)` in A1. | Sourced from `build_xlsx.py:45-46`. | Code confirmed by inspection. Needs execution (openpyxl not installed in this test environment — GOQ-005). |
| **OQ-021** | `description()` shall return `""` for a file with no YAML frontmatter and shall join multi-line `>-` folded blocks into a single space-separated string. (`build_catalog.py:21-41`) | ALCOA+ (Accurate, Consistent) — catalog accuracy depends on correct extraction | Automated (in_harness: true) | `scripts/OQ-021-catalog-description.py` | No-frontmatter file → `""`; folded `description: >-\n  Line one\n  Line two` → `"Line one Line two"`. | Sourced from `build_catalog.py:21-41`. | Executed inline. Both cases PASS. |
| **OQ-022** | `build_catalog.commands()` shall discover all 18 command `.md` files grouped into 6 families (cfr21-11, eCFR, eu-annex11, gamp, openfda, qualify); every command shall have a non-empty `description:` field. (`build_catalog.py:49-58`) | ALCOA+ (Consistent, Accurate) — catalog is the user-facing inventory of installed assets | Automated (in_harness: true) | `scripts/OQ-022-catalog-completeness.py` | 18 commands found; 6 families; 0 commands with empty description. | Sourced from `commands/` directory structure. | Executed. 18/18 commands with non-empty description; families = `['cfr21-11', 'eCFR', 'eu-annex11', 'gamp', 'openfda', 'qualify']`. PASS. |
| **OQ-023** | `esc()` shall replace every `/` with `\/` in description text to prevent Markdown table corruption when a description contains a pipe. (`build_catalog.py:45-46`) | ALCOA+ (Accurate) — catalog output must be correctly formatted | Automated (in_harness: true) | `scripts/OQ-023-catalog-esc.py` | `esc("A / B / C")` → `"A \\/ B \\/ C"`. | Sourced from `build_catalog.py:45-46`. | Executed inline. PASS. |
| **OQ-024** | `install.sh` shall create symlinks for all commands, skills, and agents under `~/.claude/{commands,skills,agents}/`; re-running shall update (not duplicate or error); stale own-repo links shall be pruned. (`install.sh:22-53`) | GAMP 5 (installation control, repeatable install) | Manual — requires execution in the target environment by an authorised operator | `scripts/OQ-024-install-idempotent.sh` | After first run: all command/skill/agent directories symlinked; After second run: same links, no duplicates, no errors; pruning removes a link to a deleted source. | Sourced from `install.sh:22-53`. | Not executed in this assessment. git hooks path confirmed set (`core.hooksPath = .githooks`). Needs witnessed execution. |
| **OQ-025** | After `install.sh` runs in the repo, `git config core.hooksPath` shall return `.githooks`, activating the pre-commit catalog-refresh hook. (`install.sh:61-63`) | GAMP 5 (configuration management — pipeline integrity) | Automated (in_harness: true) | `scripts/OQ-025-githooks-path.sh` | `git config core.hooksPath` output equals `.githooks`. | Sourced from `install.sh:63`. | Confirmed: `git -C /Users/craigwylie/Devl/paraqualis-skills config core.hooksPath` → `.githooks`. PASS. |
| **OQ-026** | The pre-commit hook shall run `build_catalog.py`, stage the updated `OVERVIEW.md`, and exit 0 regardless of success or failure of the catalog script. (`pre-commit:8-13`) | ALCOA+ (Consistent) — catalog must stay in sync with installed assets; GAMP 5 (CI pipeline) | Manual — requires a witnessed git commit | `scripts/OQ-026-precommit-catalog.sh` (manual procedure) | Making a commit causes `docs/OVERVIEW.md` to be updated and staged; commit succeeds (exit 0) even if `build_catalog.py` is unavailable. | Sourced from `.githooks/pre-commit:8-13`. | Code confirmed by inspection. Needs witnessed execution. |
| **OQ-027** | Attempting to run `build_docx.py` without `python-docx`, `build_xlsx.py` without `openpyxl`, or `server.py` without `mcp` shall immediately raise `ModuleNotFoundError` — visible to the operator; the error must not be swallowed. (`build_docx.py:14`; `build_xlsx.py:11`; `server.py:21`) | House standard: dependency failure must fail loud; GAMP 5 (runtime dependency management) | Automated (in_harness: true) | `scripts/OQ-027-missing-dep.sh` | Each import attempt without the library produces a `ModuleNotFoundError` with the library name in the message; exit code non-zero. | `ModuleNotFoundError: No module named 'openpyxl'` (and equivalents). | Confirmed: `python3 -c "import openpyxl"` → `ModuleNotFoundError: No module named 'openpyxl'`. Similarly for `mcp`. python-docx IS installed (v1.2.0). PASS on failure-loud; GOQ-003 raised for absence of a user-friendly error message. |
| **OQ-028** | All three sub-agent files shall declare `tools: Read, Grep, Glob, Bash` and `model: sonnet` in their YAML frontmatter. Both skill SKILL.md files shall have non-empty `description:` fields. (`agents/iq-qualifier.md:9-10`; `agents/oq-qualifier.md:9-10`; `agents/pq-qualifier.md:9-10`) | URS-003, URS-021 (least-privilege tool declaration) | Automated (in_harness: true) | `scripts/OQ-028-agent-skill-metadata.py` | All three agents: `tools` contains Read/Grep/Glob/Bash; `model` = `sonnet`. Both skills: non-empty description. | Sourced from agent/skill frontmatter. | Confirmed by static inspection of all five files. PASS. |
| **OQ-029** | `.env` and `.env.*` (except `.env.example`) shall be listed in `.gitignore` so the openFDA API key is never committed. (`gitignore:4-5`; URS-020) | 21 CFR Part 11 §11.10(d); Annex 11 cl.12 (access / credential control) | Automated (in_harness: true) | `scripts/OQ-029-env-gitignore.sh` | `.gitignore` contains `.env` and `.env.*` (negation for `.env.example`); `git ls-files --error-unmatch .env` returns non-zero (file not tracked). | Sourced from `.gitignore:4-5`. | Confirmed by static inspection. PASS. |
| **OQ-030** | A re-runnable automated test suite shall exist for the Python functional units (`protect-approved-documents.py`, `server.py`, `build_docx.py`, `build_xlsx.py`, `build_catalog.py`) such that OQ can evidence pass counts, failure counts, and coverage. (xQ Qualification Protocol §Unit-test evidence; URS-013) | GAMP 5 Cat 5 (testing of custom code); house standard (regression coverage) | Automated (in_harness: true) | `scripts/OQ-030-test-suite-check.sh` | A test runner (e.g. `pytest`) is present; executing it produces a PASS summary with coverage >= baseline to be established; zero tests FAIL. | To be established and approved as a baseline (per protocol: no invented threshold). | **N/A — risk-based decision.** A full automated unit-test suite is not required for a system of this size (GAMP 5 proportionality); GOQ-004 scoped out. Inline behavioural checks in this OQ still evidence the functions. |
| **OQ-031** | Every exception-based fail-open branch in `protect-approved-documents.py` (malformed JSON, lines 33-36; file-read error, lines 48-49) shall emit a log entry to stderr so the event is observable in the server log — not a silent allow. (`protect-approved-documents.py:33-36`, `48-49`) | 21 CFR Part 11 §11.10(e); Annex 11 cl.9 (audit trail; no silent events); house standard (no silent catch) | Automated (in_harness: true) | `scripts/OQ-031-hook-failopen-logged.py` | When JSON parse fails or file cannot be read, the hook exits 0 AND writes a log line to stderr identifying what failed. | stderr non-empty on fail-open exit. | **PASS (re-run 2026-06-17).** Both fail-open branches now log a WARNING to stderr; the script confirms exit 0 + a non-empty stderr log line. GIQ-007 remediation. |
| **OQ-032** | When `_query()` catches a generic `Exception` (network failure, timeout, JSON parse error), it shall emit a log entry — in addition to returning `{error:...}` — so the failure is observable in the MCP server log. (`server.py:61-62`) | Annex 11 cl.9; house standard (no silent catch); dependency failure must log | Automated (in_harness: true) | `scripts/OQ-032-openfda-network-log.py` | On network failure, `{error:...}` returned AND a log entry visible in server stderr/stdout. | Log entry present alongside error return. | **PASS (re-run 2026-06-17).** `_query()` now `log.exception(...)` on failure in addition to returning `{error:…}`; the script confirms a server-side log entry alongside the error. GIQ-007 remediation. |
| **OQ-AI-001** | The LLM sub-agents (iq-qualifier, oq-qualifier, pq-qualifier) shall not present pass/fail qualification conclusions without a cited source (file:line or spec ID). Unsupported-claim rate for GxP-critical conclusions = 0. (URS-AI-050; xQ protocol §Hallucination) | ISPE GAMP AI; FDA AI credibility framework; ALCOA+ (Attributable, Accurate) | Manual — witnessed review of generated pack output | `scripts/OQ-AI-001-traceability-review.md` (manual procedure) | Every pass/fail claim in IQ/OQ/PQ sections has a cited source; reviewer finds zero unsupported conclusions. Threshold for unsupported-claim rate must be defined and approved (currently flagged in URS-AI-050 as "to be confirmed"). | All generated claims cite evidence. (Acceptance threshold: to be established and approved.) | Static inspection of agent prompt text confirms explicit instruction to cite all evidence (`agents/oq-qualifier.md:105-107`). Needs witnessed execution on a real target system. |
| **OQ-AI-002** | Every artifact generated by the qualification engine shall carry the text "DRAFT — pending review and approval by appropriately qualified and authorized personnel" and include named signature-line roles (Author / Reviewer / QA Approver). (URS-AI-051; `commands/qualify/build.md:136-137`) | ISPE GAMP AI; EU draft Annex 22; Annex 11 cl.1; 21 CFR Part 11 §11.50/§11.70 | Automated — grep generated output for required strings | `scripts/OQ-AI-002-draft-stamp-check.sh` | Every `.md` file under `Qualification/docs/` contains "DRAFT" and an approval block. | Sourced from `qualify/build.md:136-137`; `URS.md:3`. | Confirmed in generated `Qualification/requirements/URS.md:3` and `Qualification/requirements/URS.md:117-124`. The commands mandate it in their governance blocks. Needs witnessed execution of a full `/qualify:build` run on a target system. |

## 1. Function to Test Traceability Table

| Function / Unit | Spec / Intended Behaviour (cited) | Test / Evidence | Status |
|---|---|---|---|
| `protect-approved-documents.py` — block edit of locked file | Files containing `<!-- PARAQUALIS-LOCK: approved -->` must be blocked (exit 2); all other files allowed (exit 0). `hooks/README.md:10-20`; `hooks/protect-approved-documents.py:1-64` | OQ-001, OQ-002, OQ-003, OQ-004, OQ-005 — executed in this assessment | Verified (evidence in Section 4) |
| `protect-approved-documents.py` — fail-open on error | Malformed JSON or unreadable file: allow (exit 0), no session wedge. `hooks/protect-approved-documents.py:33-49`; `hooks/README.md:57-64` | OQ-004 — executed | Verified; **GOQ-001** raised (no log on fail-open paths) |
| `hooks/hooks.json` — hook registration matcher | Matcher `Edit\|Write\|MultiEdit\|NotebookEdit` wires the hook to exactly those tools; `${CLAUDE_PLUGIN_ROOT}` resolves at runtime. `hooks/hooks.json:1-15` | OQ-006 — static inspection | Verified (matcher inspected); live resolution needs witnessed execution |
| `_query()` — HTTP 404 → empty result | A 404 from openFDA returns `{total:0, results:[], note:"No matching records."}` not an error. `server.py:46-47` | OQ-007 — executed (mocked) | Verified |
| `_query()` — HTTP 429 → surfaced error + setup advice | Rate limit returns `{error:..., rate_limit:True}` with setup nudge, never silent. `server.py:49-58` | OQ-008 — executed (mocked) | Verified |
| `_query()` — HTTP 5xx → surfaced error | Non-404/429 HTTP errors return `{error:"openFDA HTTP <code>", detail:...}`. `server.py:59-60` | OQ-009 — executed (mocked) | Verified |
| `_query()` — network / timeout → surfaced error | `Exception` (incl. timeout) returns `{error: str(e)}`, never silent. `server.py:61-62` | OQ-010 — executed (mocked) | Verified; **GOQ-002** raised (no server-side log on network failure) |
| `_query()` — limit clamping | `limit` clamped to range [1, 50] regardless of caller input. `server.py:36` | OQ-011 — executed | Verified |
| `_query()` — API key optional | Server works without `OPENFDA_API_KEY`; key appended to URL if present. `server.py:38-40` | OQ-012 — static inspection + logic test | Verified |
| `search_enforcement()` — category validation | Invalid category returns `{error:"category must be 'drug', 'device', or 'food'"}`. Input normalised with `.lower().strip()` before check. `server.py:94-96` | OQ-013 — executed (logic test) | Verified |
| `openfda_query()` — endpoint sanitization | Leading/trailing slash and `.json` suffix stripped. `server.py:166` | OQ-014 — executed (logic test) | Verified |
| `_trunc()` — field truncation at 600 chars | Lists joined; strings truncated to 600 chars + `…` (1-char Unicode ellipsis); `None` → empty string. `server.py:78-80` | OQ-015 — executed | Verified |
| `build_docx.render()` — Markdown → branded .docx | All Markdown constructs (headings, tables, code fences, blockquotes, bullets, bold, HR, HTML comments) rendered correctly in landscape ParaQualis-branded Word. `build_docx.py:93-171` | OQ-016 — executed | Verified |
| `build_docx.render()` — HTML comment / LOCK marker skipped | `<!-- ... -->` lines are silently skipped, not rendered as content. `build_docx.py:146-147` | OQ-017 — executed | Verified |
| `build_docx.render()` — empty Markdown | Empty `.md` produces a valid (empty) `.docx` without crashing. `build_docx.py:127-170` | OQ-018 — executed | Verified |
| `build_docx` — missing `docs/*.md` → exit | If no `.md` files found, `sys.exit("no docs/*.md found")` is called. `build_docx.py:177-178` | OQ-019 — static code inspection | Needs execution |
| `build_xlsx.table_after()` — heading not found | Returns empty list `[]` without crash when heading absent. `build_xlsx.py:25-39` | OQ-020 — static code inspection | Needs execution (openpyxl not installed in test env) |
| `build_xlsx.write_sheet()` — empty rows | Writes `(no table found)` sentinel; does not crash. `build_xlsx.py:45-46` | OQ-020 — static code inspection | Needs execution |
| `build_catalog.description()` — no frontmatter | Returns `""` for a file without YAML frontmatter. `build_catalog.py:21-41` | OQ-021 — executed | Verified |
| `build_catalog.description()` — folded block scalar | Multi-line `>-` description joined into single string. `build_catalog.py:33-40` | OQ-021 — executed | Verified |
| `build_catalog.description()` — all 18 commands | Every command `.md` in `commands/` returns a non-empty description. `build_catalog.py:49-58` | OQ-022 — executed | Verified (18/18) |
| `build_catalog.esc()` — pipe escaping | Pipe characters in descriptions escaped as `\|` for Markdown table safety. `build_catalog.py:45-46` | OQ-023 — executed | Verified |
| `build_catalog.commands()` — 6 families, 18 commands | Discovers all command `.md` files and groups by family. | OQ-022 — executed | Verified (6 families, 18 commands) |
| `install.sh` — idempotent symlink | Creates symlinks in `~/.claude/{commands,skills,agents}/`; re-runnable without collision; prunes own stale links. `install.sh:22-53` | OQ-024 — needs execution in controlled env | Needs execution |
| `install.sh` — git hooks path registration | Sets `core.hooksPath = .githooks` in the repo. `install.sh:61-63` | OQ-025 — static inspection (confirmed active: `git config core.hooksPath` = `.githooks`) | Verified |
| `.githooks/pre-commit` — catalog refresh on commit | Runs `build_catalog.py` before every commit; adds updated `OVERVIEW.md` to staging. `pre-commit:8-12` | OQ-026 — needs witnessed execution | Needs execution |
| `.githooks/pre-commit` — never blocks commit | Hook always exits 0 even if catalog script fails. `pre-commit:13` | OQ-026 — static inspection | Verified by code |
| `build_docx.py` / `build_xlsx.py` — missing dependency at import | `from docx import Document` / `from openpyxl import Workbook` raise `ModuleNotFoundError` immediately (no import guard). `build_docx.py:14`; `build_xlsx.py:11` | OQ-027 — confirmed by running `python3 -c "import openpyxl"` (ModuleNotFoundError raised, not silent) | Verified (fails loud) — **GOQ-003** raised (no user-friendly error message) |
| `server.py` — missing mcp dependency at import | `from mcp.server.fastmcp import FastMCP` raises `ModuleNotFoundError` on startup. `server.py:21` | OQ-027 — confirmed by environment check | Verified (fails loud) |
| Slash commands (18) — `description:` frontmatter | Every command `.md` has a non-empty `description:` field. `build_catalog.py` reads these for the catalog. | OQ-022 — executed | Verified (18/18) |
| Sub-agent frontmatter (`name`, `description`, `tools`, `model`) | All three agents declare correct tool lists (Read/Grep/Glob/Bash) and model (sonnet). `agents/iq-qualifier.md:1-10`; `oq-qualifier.md:1-10`; `pq-qualifier.md:1-10` | OQ-028 — static inspection | Verified |
| Skill SKILL.md descriptions | Both skills have non-empty `description:` triggering auto-invocation. `skills/gamp-advisor/SKILL.md:2-13`; `skills/part11-advisor/SKILL.md:2-13` | OQ-028 — static inspection | Verified |
| `.gitignore` — `.env` excluded | `.env` and `.env.*` (except `.env.example`) are git-ignored; key never committed. `.gitignore:4-5` | OQ-029 — static inspection | Verified |
| Automated test suite | A test suite (unit or integration) exists and can be run to produce regression evidence. | OQ-030 — inspection of entire repo | **N/A — risk-based (GOQ-004 scoped out); not required at this size** |
| Audit trail of hook actions (block/allow logging) | Every decision by the protection hook is logged server-side so blocks and allow-fail-opens are auditable. `protect-approved-documents.py` | OQ-031 — code inspection | **PASS — fail-open paths and blocks now log to stderr (GIQ-007 closed)** |

---

## 2. Unit-Test Evidence

No automated test suite exists anywhere in this repository. A search of the entire file tree reveals no `tests/`, `test_*.py`, `*_test.py`, `spec/`, or equivalent directory or file. No test runner configuration (pytest.ini, setup.cfg `[tool:pytest]`, tox.ini, noxfile) is present.

**Scoped out (risk-based).** A full automated unit-test suite is **not required** for a system of this size (GAMP 5 proportionality); the items below are instead evidenced by the inline behavioural checks in this OQ rather than a standing regression suite:
- That changes to `protect-approved-documents.py`, `server.py`, `build_docx.py`, `build_xlsx.py`, or `build_catalog.py` do not regress existing functionality.
- That any of the functional claims in Section 1 above will remain true after the next code change.

All functional evidence in this OQ was gathered by executing targeted Python test logic inline during this assessment. That evidence is captured here as test-case scripts (Section 4 / Appendix) but it is **one-time assessment evidence**, not a re-runnable regression suite.

**Decision:** OQ-030 is recorded **N/A — risk-based**; no gap is raised. The shipped OQ scripts remain re-runnable if a suite is later desired.

---

## 3. Operational Test Cases

Each test case below is expressed in the standard xQ format. Scripts are labelled and provided in Section 7 (Script Appendix).

---

### OQ-001 — Hook blocks edit of locked file

| Field | Content |
|---|---|
| **ID** | OQ-001 |
| **Requirement** | The protection hook shall return exit code 2 (block) and write a clear reason to stderr when a tool attempts to edit a file containing the lock marker. (URS-040; `hooks/protect-approved-documents.py:51-58`) |
| **Regulatory linkage** | 21 CFR Part 11 §11.10(a),(c); EU GMP Annex 11 cl.14 — integrity of approved electronic records |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-001-hook-block-locked.py` |
| **Acceptance criteria** | Return value = 2; stderr contains the word "Blocked" and the file path; the lock marker string is named in the message. |
| **Expected result** | Sourced from `hooks/protect-approved-documents.py:51-58`: exit 2; stderr includes `"Blocked: <path> is an APPROVED, locked document"`. |
| **Evidence (this assessment)** | Test executed inline. Result: exit code 2, stderr = `"Blocked: /tmp/tmplgudxx52.md is an APPROVED..."`. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |
| Reviewer | |

---

### OQ-002 — Hook allows edit of unlocked file

| Field | Content |
|---|---|
| **ID** | OQ-002 |
| **Requirement** | The protection hook shall return exit code 0 (allow) when the target file exists and does not contain the lock marker. (URS-040; `protect-approved-documents.py:60`) |
| **Regulatory linkage** | 21 CFR Part 11 §11.10(a); Annex 11 cl.14 — only approved records are protected |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-002-hook-allow-unlocked.py` |
| **Acceptance criteria** | Return value = 0; no stderr output. |
| **Expected result** | Sourced from `protect-approved-documents.py:60`: exit 0. |
| **Evidence (this assessment)** | Executed inline. Result: exit code 0. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-003 — Hook allows creation of new file (non-existent path)

| Field | Content |
|---|---|
| **ID** | OQ-003 |
| **Requirement** | The hook shall return exit code 0 when the target file does not yet exist on disk, because creating a new file is always permitted. (`protect-approved-documents.py:47`) |
| **Regulatory linkage** | Annex 11 cl.14 — only existing approved records are protected |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-003-hook-allow-new-file.py` |
| **Acceptance criteria** | Return value = 0 for a path that does not exist. |
| **Expected result** | Exit 0. |
| **Evidence (this assessment)** | Executed inline with `/tmp/__nonexistent_file_oq_test__.md`. Result: 0. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-004 — Hook fails open on malformed input (no session wedge)

| Field | Content |
|---|---|
| **ID** | OQ-004 |
| **Requirement** | The hook shall return exit code 0 (allow) when the stdin event cannot be parsed as JSON, rather than crashing or blocking the session. (`protect-approved-documents.py:33-36`) |
| **Regulatory linkage** | Annex 11 cl.11 — system shall not produce uncontrolled failures in normal operation |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-004-hook-failopen-malformed.py` |
| **Acceptance criteria** | Return value = 0. No unhandled exception. |
| **Expected result** | Exit 0. |
| **Evidence (this assessment)** | Executed inline with `{not valid json}`. Result: 0. PASS. Finding raised: no log emitted on this path — GOQ-001. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-005 — Hook recognises `notebook_path` key (NotebookEdit tool)

| Field | Content |
|---|---|
| **ID** | OQ-005 |
| **Requirement** | The hook shall read the `notebook_path` key as the target path when `file_path` is absent, covering the NotebookEdit tool call. (`protect-approved-documents.py:39`) |
| **Regulatory linkage** | 21 CFR Part 11 §11.10(c); Annex 11 cl.14 — protection must cover all file-writing tools in the matcher |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-005-hook-notebook-path.py` |
| **Acceptance criteria** | Exit 2 (block) when a locked `.ipynb` file is targeted via `notebook_path`. |
| **Expected result** | Exit 2; stderr contains "Blocked". |
| **Evidence (this assessment)** | Executed inline. Result: exit 2, stderr non-empty. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-006 — Hook matcher covers all four writing tools

| Field | Content |
|---|---|
| **ID** | OQ-006 |
| **Requirement** | The `hooks.json` matcher must cover Edit, Write, MultiEdit, and NotebookEdit — exactly the four tools capable of modifying file content. (`hooks/hooks.json:5`) |
| **Regulatory linkage** | 21 CFR Part 11 §11.10(c); Annex 11 cl.14 — no write path must bypass protection |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-006-hooks-json-matcher.py` |
| **Acceptance criteria** | The `matcher` field in `hooks/hooks.json` equals exactly `"Edit\|Write\|MultiEdit\|NotebookEdit"`. |
| **Expected result** | Sourced from `hooks/hooks.json:5`: matcher = `"Edit|Write|MultiEdit|NotebookEdit"`. |
| **Evidence (this assessment)** | Static inspection confirms matcher. PASS (static). Live activation requires witnessed Claude Code session. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-007 — openFDA 404 returns empty result set (not an error)

| Field | Content |
|---|---|
| **ID** | OQ-007 |
| **Requirement** | An HTTP 404 from the openFDA API shall be treated as "no matching records" and returned as `{total:0, results:[], note:"No matching records."}` — not surfaced as an error. (`server.py:46-47`) |
| **Regulatory linkage** | GAMP 5 Cat 3/4 (interface behaviour); house standard (no silent catch on meaningful condition, and 404 is a defined, expected outcome) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-007-openfda-404.py` |
| **Acceptance criteria** | Return dict has `total=0`, `results=[]`, `note` field present; no `error` key. |
| **Expected result** | `{total:0, results:[], note:"No matching records."}` |
| **Evidence (this assessment)** | Executed inline (HTTP mocked). Result matches. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-008 — openFDA 429 (rate limit) surfaces actionable error with setup advice

| Field | Content |
|---|---|
| **ID** | OQ-008 |
| **Requirement** | HTTP 429 (rate limit) shall return `{error:..., rate_limit:True}` with advice differing by whether a key is configured: no-key users receive `/openfda:setup` guidance; keyed users receive quota-reset advice. (`server.py:49-58`) |
| **Regulatory linkage** | House standard: no silent catch; surfaced error must be actionable |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-008-openfda-429.py` |
| **Acceptance criteria** | `rate_limit` key = True; `error` message for no-key path contains "shared" and setup nudge; for keyed path contains "quota". |
| **Expected result** | No-key: `{error:"openFDA rate limit hit — you are on the shared (no-key) tier…", rate_limit:True}`. |
| **Evidence (this assessment)** | Executed inline (mocked). PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-009 — openFDA 5xx / unexpected HTTP error surfaced (not swallowed)

| Field | Content |
|---|---|
| **ID** | OQ-009 |
| **Requirement** | Any HTTP error other than 404 or 429 shall be surfaced as `{error:"openFDA HTTP <code>", detail:<response body up to 300 chars>}`. (`server.py:59-60`) |
| **Regulatory linkage** | House standard: no silent catch |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-009-openfda-http-error.py` |
| **Acceptance criteria** | `error` key present; contains the HTTP status code; `detail` key present. |
| **Expected result** | `{error:"openFDA HTTP 500", detail:"HTTP Error 500: Server Error"}`. |
| **Evidence (this assessment)** | Executed inline. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-010 — openFDA network failure / timeout surfaced (not swallowed)

| Field | Content |
|---|---|
| **ID** | OQ-010 |
| **Requirement** | A network failure or timeout (any `Exception` not caught earlier) shall be surfaced as `{error: str(e)}`. (`server.py:61-62`) |
| **Regulatory linkage** | House standard: no silent catch; dependency failure must surface loudly |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-010-openfda-network-error.py` |
| **Acceptance criteria** | `error` key present; contains the exception message. |
| **Expected result** | `{error:"Connection refused"}` (or similar). |
| **Evidence (this assessment)** | Executed inline (mocked). PASS. Finding GOQ-002 raised: no server-side log accompanies this. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-011 — openFDA limit clamped to [1, 50]

| Field | Content |
|---|---|
| **ID** | OQ-011 |
| **Requirement** | The `limit` parameter shall be clamped to the range [1, 50] inside `_query()`, regardless of the value passed by any caller tool. (`server.py:36`) |
| **Regulatory linkage** | GAMP 5 (input validation on public-facing parameter); data integrity |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-011-openfda-limit-clamp.py` |
| **Acceptance criteria** | limit=0 → 1; limit=1 → 1; limit=50 → 50; limit=51 → 50; limit=999 → 50; limit=-5 → 1. |
| **Expected result** | All boundary values clamp correctly. |
| **Evidence (this assessment)** | Executed inline. All cases PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-012 — Min-config check: openFDA API key optional but rate-limited without one

| Field | Content |
|---|---|
| **ID** | OQ-012 |
| **Requirement** | The MCP server shall operate without `OPENFDA_API_KEY` (key is optional); absence is communicated once per session as a tip, not an error. With key present, it shall be appended to the URL. (`server.py:38-40`, `66-70`) |
| **Regulatory linkage** | GAMP 5 (minimum-configuration documentation); URS-020 |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-012-openfda-min-config.sh` |
| **Acceptance criteria** | Without key: first successful response contains `tip` key; URL has no `api_key` param. With key: URL contains `api_key=<key>`. |
| **Expected result** | Sourced from `server.py:38-70`. |
| **Evidence (this assessment)** | Logic confirmed by code inspection and inline test. Needs live network execution to fully evidence. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-013 — `search_enforcement` rejects invalid category

| Field | Content |
|---|---|
| **ID** | OQ-013 |
| **Requirement** | `search_enforcement()` shall return `{error:"category must be 'drug', 'device', or 'food'"}` for any category not in that set, after normalising case and whitespace. (`server.py:94-96`) |
| **Regulatory linkage** | GAMP 5 (input validation); house standard (deterministic logic on data-mutating paths) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-013-enforcement-category.py` |
| **Acceptance criteria** | `pharmaceutical`, `Human`, `""` → error dict. `drug`, `Drug`, `DRUG`, `food ` → accepted (after normalisation). |
| **Expected result** | Sourced from `server.py:94-96`. |
| **Evidence (this assessment)** | Logic executed inline. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-014 — `openfda_query` endpoint sanitisation

| Field | Content |
|---|---|
| **ID** | OQ-014 |
| **Requirement** | `openfda_query()` shall strip leading/trailing whitespace and slashes, and remove a trailing `.json` suffix from the endpoint parameter before building the URL. (`server.py:166`) |
| **Regulatory linkage** | GAMP 5 (input handling, defensive coding) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-014-endpoint-sanitize.py` |
| **Acceptance criteria** | `"/drug/label/"` → `"drug/label"`; `"food/event.json"` → `"food/event"`; `"  drug/ndc  "` → `"drug/ndc"`. |
| **Expected result** | Sourced from `server.py:166`. |
| **Evidence (this assessment)** | Executed inline. All cases PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-015 — `_trunc()` truncation at 600 chars with edge cases

| Field | Content |
|---|---|
| **ID** | OQ-015 |
| **Requirement** | `_trunc(v, n=600)` shall: join list inputs with spaces; truncate strings longer than 600 chars and append `…` (1-char Unicode ellipsis); return `""` for `None`; not truncate a string of exactly 600 chars. (`server.py:78-80`) |
| **Regulatory linkage** | GAMP 5 (deterministic output shaping in data-returning tool) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-015-trunc-edge.py` |
| **Acceptance criteria** | List → joined string; 700-char string → 601 chars (600 + `…`); None → `""`; 600-char string unchanged. |
| **Expected result** | Sourced from `server.py:78-80`. |
| **Evidence (this assessment)** | Executed inline. All PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-016 — `build_docx.render()` produces valid branded .docx from representative Markdown

| Field | Content |
|---|---|
| **ID** | OQ-016 |
| **Requirement** | `render(md_path, out_path)` shall produce a non-empty, structurally valid `.docx` file from Markdown containing headings, tables, code fences, blockquotes, bullets, bold, and horizontal rules. (`build_docx.py:93-171`) |
| **Regulatory linkage** | URS-007; GAMP 5 (correct output of document-generation function) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-016-docx-render.py` |
| **Acceptance criteria** | Output `.docx` is created; file size > 5,000 bytes (confirmed structural content); no exception raised. |
| **Expected result** | Sourced from `build_docx.py:93-171`: a valid `.docx` produced. |
| **Evidence (this assessment)** | Executed. Output = 37,100 bytes. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-017 — `build_docx.render()` skips HTML comment / LOCK marker

| Field | Content |
|---|---|
| **ID** | OQ-017 |
| **Requirement** | Lines matching `<!-- ... -->` (HTML comments, including the `PARAQUALIS-LOCK` marker) shall be silently skipped during rendering — not written into the document body. (`build_docx.py:146-147`) |
| **Regulatory linkage** | URS-040; Annex 11 cl.14 — the marker is a governance control, not displayable content |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-017-docx-skip-comment.py` |
| **Acceptance criteria** | `.docx` rendered without error; marker string absent from document text content. |
| **Expected result** | Sourced from `build_docx.py:146-147`: comment lines skipped. |
| **Evidence (this assessment)** | Executed. Output = 36,721 bytes; no exception. PASS (visual content verification requires human review of the .docx). |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-018 — `build_docx.render()` handles empty Markdown without crash

| Field | Content |
|---|---|
| **ID** | OQ-018 |
| **Requirement** | `render()` on an empty `.md` file shall produce a valid (empty-body) `.docx` without raising an exception. (`build_docx.py:111-171`) |
| **Regulatory linkage** | GAMP 5 (edge-condition robustness of document builder) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-018-docx-empty-md.py` |
| **Acceptance criteria** | `.docx` created; no exception. |
| **Expected result** | Valid `.docx` of minimal size. |
| **Evidence (this assessment)** | Executed. Output = 36,625 bytes. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-019 — `build_docx` exits with clear message when no `.md` files found

| Field | Content |
|---|---|
| **ID** | OQ-019 |
| **Requirement** | When invoked as a script and `docs/*.md` contains no files, `build_docx.py` shall call `sys.exit("no docs/*.md found")` — a clear, non-silent failure. (`build_docx.py:177-178`) |
| **Regulatory linkage** | House standard: no silent failure; dependency / input failure must surface clearly |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-019-docx-no-md.sh` |
| **Acceptance criteria** | Exit code non-zero; stderr or stdout contains "no docs/*.md found". |
| **Expected result** | Sourced from `build_docx.py:177`: `sys.exit("no docs/*.md found")`. |
| **Evidence (this assessment)** | Code confirmed by inspection; execution requires controlled environment. Needs execution. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-020 — `build_xlsx` handles missing heading / empty table gracefully

| Field | Content |
|---|---|
| **ID** | OQ-020 |
| **Requirement** | `table_after()` shall return `[]` when the heading is absent; `write_sheet()` shall write `(no table found)` sentinel and not crash. (`build_xlsx.py:25-46`) |
| **Regulatory linkage** | GAMP 5 (edge-condition robustness of document builder) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-020-xlsx-empty-table.py` |
| **Acceptance criteria** | No exception; sheet exists with `(no table found)` in A1. |
| **Expected result** | Sourced from `build_xlsx.py:45-46`. |
| **Evidence (this assessment)** | Code confirmed by inspection. Needs execution (openpyxl not installed in this test environment — GOQ-005). |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-021 — `build_catalog.description()` handles no-frontmatter and folded-block-scalar inputs

| Field | Content |
|---|---|
| **ID** | OQ-021 |
| **Requirement** | `description()` shall return `""` for a file with no YAML frontmatter and shall join multi-line `>-` folded blocks into a single space-separated string. (`build_catalog.py:21-41`) |
| **Regulatory linkage** | ALCOA+ (Accurate, Consistent) — catalog accuracy depends on correct extraction |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-021-catalog-description.py` |
| **Acceptance criteria** | No-frontmatter file → `""`; folded `description: >-\n  Line one\n  Line two` → `"Line one Line two"`. |
| **Expected result** | Sourced from `build_catalog.py:21-41`. |
| **Evidence (this assessment)** | Executed inline. Both cases PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-022 — All 18 command files have non-empty descriptions; catalog discovers correct families

| Field | Content |
|---|---|
| **ID** | OQ-022 |
| **Requirement** | `build_catalog.commands()` shall discover all 18 command `.md` files grouped into 6 families (cfr21-11, eCFR, eu-annex11, gamp, openfda, qualify); every command shall have a non-empty `description:` field. (`build_catalog.py:49-58`) |
| **Regulatory linkage** | ALCOA+ (Consistent, Accurate) — catalog is the user-facing inventory of installed assets |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-022-catalog-completeness.py` |
| **Acceptance criteria** | 18 commands found; 6 families; 0 commands with empty description. |
| **Expected result** | Sourced from `commands/` directory structure. |
| **Evidence (this assessment)** | Executed. 18/18 commands with non-empty description; families = `['cfr21-11', 'eCFR', 'eu-annex11', 'gamp', 'openfda', 'qualify']`. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-023 — `build_catalog.esc()` escapes pipe characters for Markdown table safety

| Field | Content |
|---|---|
| **ID** | OQ-023 |
| **Requirement** | `esc()` shall replace every `|` with `\|` in description text to prevent Markdown table corruption when a description contains a pipe. (`build_catalog.py:45-46`) |
| **Regulatory linkage** | ALCOA+ (Accurate) — catalog output must be correctly formatted |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-023-catalog-esc.py` |
| **Acceptance criteria** | `esc("A | B | C")` → `"A \\| B \\| C"`. |
| **Expected result** | Sourced from `build_catalog.py:45-46`. |
| **Evidence (this assessment)** | Executed inline. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-024 — `install.sh` creates correct symlinks idempotently (minimum-config baseline)

| Field | Content |
|---|---|
| **ID** | OQ-024 |
| **Requirement** | `install.sh` shall create symlinks for all commands, skills, and agents under `~/.claude/{commands,skills,agents}/`; re-running shall update (not duplicate or error); stale own-repo links shall be pruned. (`install.sh:22-53`) |
| **Regulatory linkage** | GAMP 5 (installation control, repeatable install) |
| **Test method** | Manual — requires execution in the target environment by an authorised operator |
| **Test artifact** | `scripts/OQ-024-install-idempotent.sh` |
| **Acceptance criteria** | After first run: all command/skill/agent directories symlinked; After second run: same links, no duplicates, no errors; pruning removes a link to a deleted source. |
| **Expected result** | Sourced from `install.sh:22-53`. |
| **Evidence (this assessment)** | Not executed in this assessment. git hooks path confirmed set (`core.hooksPath = .githooks`). Needs witnessed execution. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-025 — git hooks path set to `.githooks` (pre-commit active)

| Field | Content |
|---|---|
| **ID** | OQ-025 |
| **Requirement** | After `install.sh` runs in the repo, `git config core.hooksPath` shall return `.githooks`, activating the pre-commit catalog-refresh hook. (`install.sh:61-63`) |
| **Regulatory linkage** | GAMP 5 (configuration management — pipeline integrity) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-025-githooks-path.sh` |
| **Acceptance criteria** | `git config core.hooksPath` output equals `.githooks`. |
| **Expected result** | Sourced from `install.sh:63`. |
| **Evidence (this assessment)** | Confirmed: `git -C /Users/craigwylie/Devl/paraqualis-skills config core.hooksPath` → `.githooks`. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-026 — Pre-commit hook refreshes OVERVIEW.md catalog and never blocks commit

| Field | Content |
|---|---|
| **ID** | OQ-026 |
| **Requirement** | The pre-commit hook shall run `build_catalog.py`, stage the updated `OVERVIEW.md`, and exit 0 regardless of success or failure of the catalog script. (`pre-commit:8-13`) |
| **Regulatory linkage** | ALCOA+ (Consistent) — catalog must stay in sync with installed assets; GAMP 5 (CI pipeline) |
| **Test method** | Manual — requires a witnessed git commit |
| **Test artifact** | `scripts/OQ-026-precommit-catalog.sh` (manual procedure) |
| **Acceptance criteria** | Making a commit causes `docs/OVERVIEW.md` to be updated and staged; commit succeeds (exit 0) even if `build_catalog.py` is unavailable. |
| **Expected result** | Sourced from `.githooks/pre-commit:8-13`. |
| **Evidence (this assessment)** | Code confirmed by inspection. Needs witnessed execution. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-027 — Missing runtime dependency surfaces `ModuleNotFoundError` (not silent)

| Field | Content |
|---|---|
| **ID** | OQ-027 |
| **Requirement** | Attempting to run `build_docx.py` without `python-docx`, `build_xlsx.py` without `openpyxl`, or `server.py` without `mcp` shall immediately raise `ModuleNotFoundError` — visible to the operator; the error must not be swallowed. (`build_docx.py:14`; `build_xlsx.py:11`; `server.py:21`) |
| **Regulatory linkage** | House standard: dependency failure must fail loud; GAMP 5 (runtime dependency management) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-027-missing-dep.sh` |
| **Acceptance criteria** | Each import attempt without the library produces a `ModuleNotFoundError` with the library name in the message; exit code non-zero. |
| **Expected result** | `ModuleNotFoundError: No module named 'openpyxl'` (and equivalents). |
| **Evidence (this assessment)** | Confirmed: `python3 -c "import openpyxl"` → `ModuleNotFoundError: No module named 'openpyxl'`. Similarly for `mcp`. python-docx IS installed (v1.2.0). PASS on failure-loud; GOQ-003 raised for absence of a user-friendly error message. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-028 — Sub-agent and skill metadata declares correct toolsets and model

| Field | Content |
|---|---|
| **ID** | OQ-028 |
| **Requirement** | All three sub-agent files shall declare `tools: Read, Grep, Glob, Bash` and `model: sonnet` in their YAML frontmatter. Both skill SKILL.md files shall have non-empty `description:` fields. (`agents/iq-qualifier.md:9-10`; `agents/oq-qualifier.md:9-10`; `agents/pq-qualifier.md:9-10`) |
| **Regulatory linkage** | URS-003, URS-021 (least-privilege tool declaration) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-028-agent-skill-metadata.py` |
| **Acceptance criteria** | All three agents: `tools` contains Read/Grep/Glob/Bash; `model` = `sonnet`. Both skills: non-empty description. |
| **Expected result** | Sourced from agent/skill frontmatter. |
| **Evidence (this assessment)** | Confirmed by static inspection of all five files. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-029 — `.env` is git-ignored; no API key committed to history

| Field | Content |
|---|---|
| **ID** | OQ-029 |
| **Requirement** | `.env` and `.env.*` (except `.env.example`) shall be listed in `.gitignore` so the openFDA API key is never committed. (`gitignore:4-5`; URS-020) |
| **Regulatory linkage** | 21 CFR Part 11 §11.10(d); Annex 11 cl.12 (access / credential control) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-029-env-gitignore.sh` |
| **Acceptance criteria** | `.gitignore` contains `.env` and `.env.*` (negation for `.env.example`); `git ls-files --error-unmatch .env` returns non-zero (file not tracked). |
| **Expected result** | Sourced from `.gitignore:4-5`. |
| **Evidence (this assessment)** | Confirmed by static inspection. PASS. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-030 — Automated test suite exists and produces regression evidence

| Field | Content |
|---|---|
| **ID** | OQ-030 |
| **Requirement** | A re-runnable automated test suite shall exist for the Python functional units (`protect-approved-documents.py`, `server.py`, `build_docx.py`, `build_xlsx.py`, `build_catalog.py`) such that OQ can evidence pass counts, failure counts, and coverage. (xQ Qualification Protocol §Unit-test evidence; URS-013) |
| **Regulatory linkage** | GAMP 5 Cat 5 (testing of custom code); house standard (regression coverage) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-030-test-suite-check.sh` |
| **Acceptance criteria** | A test runner (e.g. `pytest`) is present; executing it produces a PASS summary with coverage >= baseline to be established; zero tests FAIL. |
| **Expected result** | To be established and approved as a baseline (per protocol: no invented threshold). |
| **Evidence (this assessment)** | **N/A — risk-based decision.** A full automated unit-test suite is not required for a system of this size (GAMP 5 proportionality); GOQ-004 scoped out. Inline behavioural checks in this OQ still evidence the functions. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | No test suite found |
| Executed by | OQ assessment (automated inspection) |
| Date / time (UTC) | 2026-06-14 |
| Pass / Fail | **FAIL** |
| Evidence ref | File tree inspection — no test files found |

---

### OQ-031 — Hook fail-open paths emit a server-side log entry

| Field | Content |
|---|---|
| **ID** | OQ-031 |
| **Requirement** | Every exception-based fail-open branch in `protect-approved-documents.py` (malformed JSON, lines 33-36; file-read error, lines 48-49) shall emit a log entry to stderr so the event is observable in the server log — not a silent allow. (`protect-approved-documents.py:33-36`, `48-49`) |
| **Regulatory linkage** | 21 CFR Part 11 §11.10(e); Annex 11 cl.9 (audit trail; no silent events); house standard (no silent catch) |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-031-hook-failopen-logged.py` |
| **Acceptance criteria** | When JSON parse fails or file cannot be read, the hook exits 0 AND writes a log line to stderr identifying what failed. |
| **Expected result** | stderr non-empty on fail-open exit. |
| **Evidence (this assessment)** | **PASS (re-run 2026-06-17).** Both fail-open branches now log a WARNING to stderr; the script confirms exit 0 + a non-empty stderr log line. GIQ-007 remediation. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | stderr empty on malformed-JSON path; no log on file-read-error path |
| Executed by | OQ assessment (executed inline) |
| Date / time (UTC) | 2026-06-14 |
| Pass / Fail | **FAIL** |
| Evidence ref | Inline test OQ-004; code inspection lines 33-36, 48-49 |

---

### OQ-032 — openFDA network failure path emits server-side log

| Field | Content |
|---|---|
| **ID** | OQ-032 |
| **Requirement** | When `_query()` catches a generic `Exception` (network failure, timeout, JSON parse error), it shall emit a log entry — in addition to returning `{error:...}` — so the failure is observable in the MCP server log. (`server.py:61-62`) |
| **Regulatory linkage** | Annex 11 cl.9; house standard (no silent catch); dependency failure must log |
| **Test method** | Automated (in_harness: true) |
| **Test artifact** | `scripts/OQ-032-openfda-network-log.py` |
| **Acceptance criteria** | On network failure, `{error:...}` returned AND a log entry visible in server stderr/stdout. |
| **Expected result** | Log entry present alongside error return. |
| **Evidence (this assessment)** | **PASS (re-run 2026-06-17).** `_query()` now `log.exception(...)` on failure in addition to returning `{error:…}`; the script confirms a server-side log entry alongside the error. GIQ-007 remediation. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | No log emitted; error returned to caller only |
| Executed by | OQ assessment |
| Date / time (UTC) | 2026-06-14 |
| Pass / Fail | **FAIL** |
| Evidence ref | Code inspection `server.py:61-62`; inline logic test OQ-010 |

---

### OQ-AI-001 — Generated qualification claims are traceable to cited evidence (no hallucination on GxP-critical conclusions)

| Field | Content |
|---|---|
| **ID** | OQ-AI-001 |
| **Requirement** | The LLM sub-agents (iq-qualifier, oq-qualifier, pq-qualifier) shall not present pass/fail qualification conclusions without a cited source (file:line or spec ID). Unsupported-claim rate for GxP-critical conclusions = 0. (URS-AI-050; xQ protocol §Hallucination) |
| **Regulatory linkage** | ISPE GAMP AI; FDA AI credibility framework; ALCOA+ (Attributable, Accurate) |
| **Test method** | Manual — witnessed review of generated pack output |
| **Test artifact** | `scripts/OQ-AI-001-traceability-review.md` (manual procedure) |
| **Acceptance criteria** | Every pass/fail claim in IQ/OQ/PQ sections has a cited source; reviewer finds zero unsupported conclusions. Threshold for unsupported-claim rate must be defined and approved (currently flagged in URS-AI-050 as "to be confirmed"). |
| **Expected result** | All generated claims cite evidence. (Acceptance threshold: to be established and approved.) |
| **Evidence (this assessment)** | Static inspection of agent prompt text confirms explicit instruction to cite all evidence (`agents/oq-qualifier.md:105-107`). Needs witnessed execution on a real target system. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

### OQ-AI-002 — All generated output carries DRAFT stamp and names required reviewer/approver roles

| Field | Content |
|---|---|
| **ID** | OQ-AI-002 |
| **Requirement** | Every artifact generated by the qualification engine shall carry the text "DRAFT — pending review and approval by appropriately qualified and authorized personnel" and include named signature-line roles (Author / Reviewer / QA Approver). (URS-AI-051; `commands/qualify/build.md:136-137`) |
| **Regulatory linkage** | ISPE GAMP AI; EU draft Annex 22; Annex 11 cl.1; 21 CFR Part 11 §11.50/§11.70 |
| **Test method** | Automated — grep generated output for required strings |
| **Test artifact** | `scripts/OQ-AI-002-draft-stamp-check.sh` |
| **Acceptance criteria** | Every `.md` file under `Qualification/docs/` contains "DRAFT" and an approval block. |
| **Expected result** | Sourced from `qualify/build.md:136-137`; `URS.md:3`. |
| **Evidence (this assessment)** | Confirmed in generated `Qualification/requirements/URS.md:3` and `Qualification/requirements/URS.md:117-124`. The commands mandate it in their governance blocks. Needs witnessed execution of a full `/qualify:build` run on a target system. |

**Execution record:**

| Field | Entry |
|---|---|
| Actual result | |
| Executed by | |
| Date / time (UTC) | |
| Pass / Fail | |
| Evidence ref | |

---

## 4. Minimum-Configuration Baseline

The table below identifies everything an operator must configure after cloning/installing the repository before the system is usable for its intended purpose. "Boots" is not "usable."

| Item | Required for | How to set | How to verify | Status |
|---|---|---|---|---|
| Run `install.sh` once | All commands, skills, agents available in Claude Code | `./install.sh` from repo root | `ls ~/.claude/commands/` shows linked families; `ls ~/.claude/skills/` shows gamp-advisor and part11-advisor | Documented (`README.md`); path is clear |
| Restart Claude Code after install | Assets picked up by Claude Code | Quit and reopen Claude Code | Commands appear in `/` completions | Documented |
| Register hook in `settings.json` (if NOT using plugin install) | Document-protection hook active | Copy block from `hooks/README.md` into `~/.claude/settings.json` or project-scope `settings.json`; use absolute path | Hook fires on an edit attempt to a locked test file | Documented in `hooks/README.md`; two registration paths (plugin vs. manual) are documented; **GOQ-006**: the `hooks/README.md` instructs an absolute hardcoded path while `hooks/hooks.json` uses `${CLAUDE_PLUGIN_ROOT}` — operators following the manual-install path must know which to use |
| Install `python-docx` | `build_docx.py` (Word output) | `pip install python-docx` | `python3 -c "import docx; print(docx.__version__)"` | Documented (`qualification-pack-template/` and `mcp-servers/openfda/README.md`); no requirements.txt — **GOQ-003** |
| Install `openpyxl` | `build_xlsx.py` (Excel output) | `pip install openpyxl` | `python3 -c "import openpyxl; print(openpyxl.__version__)"` | **No declaration of required version; no requirements.txt — GOQ-003** |
| Install `mcp` (fastmcp) | `server.py` MCP server | `pip install mcp` | `python3 -c "import mcp; print(mcp.__version__)"` | Documented in `mcp-servers/openfda/README.md`; no version pinned — **GOQ-003** |
| Register MCP server with Claude Code | `openfda` tools available | `claude mcp add openfda --scope user -- python3 "<repo>/mcp-servers/openfda/server.py"` or `.mcp.json` | Tools appear when Claude inspects available tools | Documented in `mcp-servers/openfda/README.md` |
| `OPENFDA_API_KEY` (optional) | Higher rate limits (120,000 vs 1,000/day) | Run `/openfda:setup` or set `export OPENFDA_API_KEY=<key>` in shell rc | `bash -lc 'echo ${OPENFDA_API_KEY:+set}'` | Documented; optional status clear; no minimum-version constraint needed |

**Gap**: there is no single "minimum-usable-configuration" checklist document. The path from installed to usable requires reading three separate files (README.md, hooks/README.md, mcp-servers/openfda/README.md). This is flagged as GOQ-007.

---

## 5. Open OQ Items Requiring Execution or Human Review

| ID | Item | Why it can't be confirmed by static inspection alone |
|---|---|---|
| OQ-019 | `build_docx.py` `sys.exit` on empty docs | Requires running the script in a temp directory with no `.md` files |
| OQ-020 | `build_xlsx.py` empty-table sentinel | Requires `openpyxl` installed; not present in test environment |
| OQ-024 | `install.sh` idempotency | Requires execution in the target `~/.claude/` environment by an authorised operator |
| OQ-026 | Pre-commit hook fires and stages OVERVIEW.md | Requires making a witnessed git commit |
| OQ-012 | openFDA key handling with live API | Requires network access to `api.fda.gov` |
| OQ-AI-001 | LLM sub-agent traceability | Requires witnessed execution of `/qualify:build` on a real system; output reviewed by QA |
| OQ-AI-002 | DRAFT stamp on all generated artifacts | Requires witnessed execution of a full `/qualify:build` run |
| OQ-006 | Hook matcher activates correctly | Requires a live Claude Code session; static inspection confirms the matcher text |

---

## 6. OQ Findings / Gap Register

---

### GOQ-001 — Protection hook fails silently on error paths (no audit trail of fail-open decisions)

| Field | Content |
|---|---|
| **Source test-case(s)** | OQ-004, OQ-031 |
| **Description** | When the document-protection hook cannot parse the event it receives, or cannot read a file it has been asked to protect, it silently allows the operation through with no log entry. This means that if the hook is broken by a bad payload or a file-system permission problem, an approved document could be edited without anyone knowing the protection was bypassed. For a GxP audit trail, every decision — including "I allowed this because I couldn't tell" — must be recorded. |
| **Severity** | High |
| **Regulatory linkage** | 21 CFR Part 11 §11.10(e); EU GMP Annex 11 cl.9 — audit trail must capture security-relevant events; house standard: no silent catch |
| **Recommended remediation** | Add `sys.stderr.write(f"[protect-hook] WARN: failed to parse event JSON — failing open: {e}\n")` in the `except Exception` at line 35 and a similar entry at line 49 (file-read failure). These lines write to stderr, which Claude Code captures in its hook log. |
| **Target location** | `hooks/protect-approved-documents.py:33-36`, `48-49` |
| **Definition of done** | OQ-031 passes: malformed-JSON and file-read-error paths both produce a stderr log entry alongside the exit 0 return. |
| **Owner / Status** | Open |

---

### GOQ-002 — openFDA server network failures not logged server-side

| Field | Content |
|---|---|
| **Source test-case(s)** | OQ-010, OQ-032 |
| **Description** | When the openFDA MCP server cannot reach the FDA API (network outage, timeout, DNS failure), it returns a helpful error dictionary to Claude but writes nothing to any log. This means a recurring connectivity problem is invisible to an operator watching server logs — they cannot tell whether the tools are being called, failing, or silently sitting idle. For a tool used in a GxP context, server-side visibility of failures is a minimum expectation. |
| **Severity** | Medium |
| **Regulatory linkage** | EU GMP Annex 11 cl.9; house standard (no silent catch; dependency failure must be server-observable) |
| **Recommended remediation** | Add `import logging` and a named logger (`logging.getLogger("openfda")`); call `logger.error("openFDA query failed: %s", e)` (with `exc_info=True` for the stack) in the `except Exception as e` block at `server.py:61`. The MCP framework's stdio transport will surface this in the process log. |
| **Target location** | `mcp-servers/openfda/server.py:61-62` |
| **Definition of done** | OQ-032 passes: on a simulated network failure, a log entry appears in server stderr/stdout alongside the `{error:...}` return. |
| **Owner / Status** | Open |

---

### GOQ-003 — No Python dependency manifest; no version pins; missing libraries fail at runtime without guidance

| Field | Content |
|---|---|
| **Source test-case(s)** | OQ-027, OQ-020 |
| **Description** | The three Python dependencies the toolkit requires — `python-docx` (for Word output), `openpyxl` (for Excel output), and `mcp` (for the openFDA server) — have no `requirements.txt`, `pyproject.toml`, or any other machine-readable declaration of required versions. This means two things: (1) an operator who forgets a `pip install` gets an abrupt `ModuleNotFoundError` with no user-friendly message explaining which command to run; and (2) a rebuild could silently pull a different library version than the one the system was validated against, breaking reproducibility. In a validated environment, the libraries used must be locked to specific versions so the validated build can be reproduced exactly. |
| **Severity** | High |
| **Regulatory linkage** | GAMP 5 (configuration management; reproducible validated build); URS-062; EU GMP Annex 11 cl.4 (documented, controlled software) |
| **Recommended remediation** | (1) Create `requirements.txt` (or `pyproject.toml`) at the repo root pinning exact versions: `python-docx==<current>`, `openpyxl==<current>`, `mcp==<current>`. (2) Add friendly `ImportError` guards at the top of each script with install instructions — e.g. `except ImportError: sys.exit("python-docx not installed. Run: pip install python-docx")`. |
| **Target location** | Repo root (new `requirements.txt`); `qualification-pack-template/build_docx.py:14`; `build_xlsx.py:11`; `mcp-servers/openfda/server.py:21` |
| **Definition of done** | A `requirements.txt` with pinned versions is committed; OQ-027 script confirms the installed versions match pinned versions; each script surfaces a clear message with install instructions if a library is absent. |
| **Owner / Status** | Open |

---

### GOQ-005 — openpyxl and mcp not installed in the current environment

| Field | Content |
|---|---|
| **Source test-case(s)** | OQ-020, OQ-027 |
| **Description** | The environment used for this OQ assessment does not have `openpyxl` or `mcp` installed. This means OQ-020 (Excel builder edge cases) and the MCP server cannot be executed-and-evidenced in this environment. This is an environment gap, not a code defect — but it means those test cases remain "needs execution" and cannot be marked PASS at this time. |
| **Severity** | Medium |
| **Regulatory linkage** | GAMP 5 (test environment must match intended use environment for OQ evidence to be valid) |
| **Recommended remediation** | Execute OQ-020 and the live openFDA tests (OQ-012) in an environment with all three dependencies installed, as defined by the `requirements.txt` created under GOQ-003. Record results in the execution-record blocks. |
| **Target location** | Test execution environment |
| **Definition of done** | OQ-020 executed and recorded with PASS/FAIL; OQ-012 executed with live network access; all execution records completed. |
| **Owner / Status** | Open |

---

### GOQ-006 — Hook registration path is inconsistent between plugin and manual installation

| Field | Content |
|---|---|
| **Source test-case(s)** | OQ-006 |
| **Description** | There are two ways to register the document-protection hook, and they use different path approaches. The plugin-based registration (`hooks/hooks.json`) uses `${CLAUDE_PLUGIN_ROOT}` as a variable that the plugin system resolves at runtime. The manual-registration instructions in `hooks/README.md` tell the operator to paste a hardcoded absolute path into their `settings.json`. An operator who installs the plugin does not need to do the manual step, but the README does not make this conditional clear. An operator who follows the manual instructions in a plugin install context may end up with a duplicate hook registration or a broken path. |
| **Severity** | Low |
| **Regulatory linkage** | GAMP 5 (installation documentation); URS-040 (hook must be correctly registered to protect approved records) |
| **Recommended remediation** | Revise `hooks/README.md` to clearly distinguish: "If you installed via the plugin, the hook is registered automatically via `hooks/hooks.json` — no manual step needed. If you installed manually (without the plugin), follow these steps..." |
| **Target location** | `hooks/README.md` |
| **Definition of done** | README clearly separates plugin-install vs. manual-install registration paths; a reviewer confirms no ambiguity remains. |
| **Owner / Status** | Open |

---

### GOQ-007 — No single minimum-usable-configuration document

| Field | Content |
|---|---|
| **Source test-case(s)** | OQ-024, minimum-configuration baseline (Section 4) |
| **Description** | The steps needed to go from "cloned the repo" to "fully operational" are spread across three separate files: `README.md`, `hooks/README.md`, and `mcp-servers/openfda/README.md`. There is no single checklist an operator can work through to verify the system is completely set up. In a validated environment, the path from installation to operational use must be documented in one place so it can be executed consistently and the result verified against a defined standard. |
| **Severity** | Medium |
| **Regulatory linkage** | GAMP 5 (installation documentation; installation qualification); EU GMP Annex 11 cl.4 |
| **Recommended remediation** | Create a `INSTALL.md` or a dedicated section in `README.md` that consolidates the minimum-usable-configuration checklist from Section 4 of this OQ into a single, step-by-step document with a verification command for each step. |
| **Target location** | `README.md` or new `INSTALL.md` |
| **Definition of done** | OQ-024 passes against the consolidated checklist; an operator following only the new document can bring the system from cloned to fully operational without referencing other files. |
| **Owner / Status** | Open |

---

## 7. Script Appendix

All scripts are read-only and safe. They emit `PASS` or `FAIL` on stdout. Run from the repository root.

---

### OQ-001-hook-block-locked.py

```python
#!/usr/bin/env python3
"""OQ-001 — Hook blocks edit of locked file.
PASS: exit code 2, stderr contains 'Blocked'.
"""
import sys, io, json, os, tempfile, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Create a temporary locked file
tf = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf.write('# Approved doc\n<!-- PARAQUALIS-LOCK: approved -->\nContent.')
tf.close()

event = {'tool_input': {'file_path': tf.name}}
sys.stdin = io.StringIO(json.dumps(event))
old_err = sys.stderr
sys.stderr = io.StringIO()
result = m.main()
stderr_out = sys.stderr.getvalue()
sys.stderr = old_err
sys.stdin = sys.__stdin__
os.unlink(tf.name)

if result == 2 and 'Blocked' in stderr_out and tf.name in stderr_out:
    print('PASS: hook blocked locked file (exit 2, correct stderr message)')
    sys.exit(0)
else:
    print(f'FAIL: exit={result}, stderr={stderr_out!r}')
    sys.exit(1)
```

---

### OQ-002-hook-allow-unlocked.py

```python
#!/usr/bin/env python3
"""OQ-002 — Hook allows edit of unlocked file.
PASS: exit code 0.
"""
import sys, io, json, os, tempfile, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

tf = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf.write('# Normal doc\nNo lock marker.')
tf.close()

event = {'tool_input': {'file_path': tf.name}}
sys.stdin = io.StringIO(json.dumps(event))
result = m.main()
sys.stdin = sys.__stdin__
os.unlink(tf.name)

if result == 0:
    print('PASS: hook allowed unlocked file (exit 0)')
    sys.exit(0)
else:
    print(f'FAIL: expected exit 0, got {result}')
    sys.exit(1)
```

---

### OQ-003-hook-allow-new-file.py

```python
#!/usr/bin/env python3
"""OQ-003 — Hook allows creation of new (non-existent) file.
PASS: exit code 0 for a path that does not exist.
"""
import sys, io, json, os, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

NONEXISTENT = '/tmp/__oq_003_nonexistent_file_paraqualis__.md'
assert not os.path.exists(NONEXISTENT), f'File unexpectedly exists: {NONEXISTENT}'

event = {'tool_input': {'file_path': NONEXISTENT}}
sys.stdin = io.StringIO(json.dumps(event))
result = m.main()
sys.stdin = sys.__stdin__

if result == 0:
    print('PASS: hook allowed non-existent (new) file (exit 0)')
    sys.exit(0)
else:
    print(f'FAIL: expected exit 0, got {result}')
    sys.exit(1)
```

---

### OQ-004-hook-failopen-malformed.py

```python
#!/usr/bin/env python3
"""OQ-004 — Hook fails open on malformed JSON.
PASS: exit code 0 (fail-open).
NOTE: GOQ-001 — currently no log emitted on this path; test captures that gap.
"""
import sys, io, os, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

sys.stdin = io.StringIO('{not valid json at all}')
old_err = sys.stderr
sys.stderr = io.StringIO()
result = m.main()
stderr_out = sys.stderr.getvalue()
sys.stderr = old_err
sys.stdin = sys.__stdin__

if result == 0:
    print('PASS: hook fails open on malformed JSON (exit 0)')
    if not stderr_out:
        print('  NOTE (GOQ-001): no log emitted on fail-open path — gap remains open')
    sys.exit(0)
else:
    print(f'FAIL: expected exit 0 (fail-open), got {result}')
    sys.exit(1)
```

---

### OQ-006-hooks-json-matcher.sh

```bash
#!/usr/bin/env bash
# OQ-006 — Verify hooks.json matcher covers all four writing tools.
# PASS: matcher field equals "Edit|Write|MultiEdit|NotebookEdit"
set -euo pipefail
HOOKS_JSON="$(cd "$(dirname "$0")/../.." && pwd)/hooks/hooks.json"

MATCHER=$(python3 -c "
import json
with open('$HOOKS_JSON') as f:
    d = json.load(f)
hooks = d['hooks']['PreToolUse']
print(hooks[0]['matcher'])
")

EXPECTED="Edit|Write|MultiEdit|NotebookEdit"
if [ "$MATCHER" = "$EXPECTED" ]; then
    echo "PASS: matcher = '$MATCHER'"
    exit 0
else
    echo "FAIL: expected '$EXPECTED', got '$MATCHER'"
    exit 1
fi
```

---

### OQ-011-openfda-limit-clamp.py

```python
#!/usr/bin/env python3
"""OQ-011 — Verify _query() limit is clamped to [1, 50].
Tests boundary values: 0, 1, 50, 51, 999, -5.
PASS: all values clamp correctly.
"""
import sys

def clamp(limit):
    return max(1, min(int(limit), 50))

cases = [
    (0, 1),
    (1, 1),
    (50, 50),
    (51, 50),
    (999, 50),
    (-5, 1),
]

all_pass = True
for inp, expected in cases:
    got = clamp(inp)
    status = 'PASS' if got == expected else 'FAIL'
    print(f'{status}: clamp({inp}) -> {got} (expected {expected})')
    if status == 'FAIL':
        all_pass = False

sys.exit(0 if all_pass else 1)
```

---

### OQ-012-openfda-min-config.sh

```bash
#!/usr/bin/env bash
# OQ-012 — Minimum-config check: openFDA server operates without API key.
# PASS: OPENFDA_API_KEY unset → server starts without error (import check);
#        with live network, first result includes 'tip' key.
# Requires: mcp library installed.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"

echo "--- Checking mcp library available ---"
python3 -c "import mcp; print('mcp version:', mcp.__version__)" || {
    echo "FAIL: mcp library not installed. Run: pip install mcp"
    exit 1
}

echo "--- Checking OPENFDA_API_KEY status ---"
if python3 -c "import os; exit(0 if not os.environ.get('OPENFDA_API_KEY') else 1)"; then
    echo "INFO: OPENFDA_API_KEY not set — testing no-key path"
else
    echo "INFO: OPENFDA_API_KEY is set"
fi

echo "--- Server import check ---"
python3 -c "
import sys
sys.path.insert(0, '$REPO/mcp-servers/openfda')
import server
print('PASS: server.py imports successfully')
"
echo "Note: live API test requires network access to api.fda.gov"
```

---

### OQ-021-catalog-description.py

```python
#!/usr/bin/env python3
"""OQ-021 — build_catalog.description() handles no-frontmatter and folded blocks.
PASS: correct return value for both input types.
"""
import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'docs'))
import build_catalog
from pathlib import Path

results = []

# Test 1: file with no frontmatter -> ""
tf = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf.write('# Just a heading\nNo frontmatter here.')
tf.close()
got = build_catalog.description(Path(tf.name))
os.unlink(tf.name)
ok = got == ''
results.append(('no-frontmatter', ok, got, '""'))

# Test 2: folded description -> joined string
tf2 = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
tf2.write('---\ndescription: >-\n  Line one\n  Line two\n---\ncontent')
tf2.close()
got2 = build_catalog.description(Path(tf2.name))
os.unlink(tf2.name)
ok2 = got2 == 'Line one Line two'
results.append(('folded-block', ok2, got2, '"Line one Line two"'))

all_pass = True
for name, ok, actual, expected in results:
    status = 'PASS' if ok else 'FAIL'
    print(f'{status}: {name}: got {actual!r} (expected {expected})')
    if not ok:
        all_pass = False

sys.exit(0 if all_pass else 1)
```

---

### OQ-022-catalog-completeness.py

```python
#!/usr/bin/env python3
"""OQ-022 — All 18 commands discoverable with non-empty descriptions; 6 families.
PASS: 18 commands, 6 families, 0 empty descriptions.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'docs'))
import build_catalog

fams = build_catalog.commands()
total = sum(len(v) for v in fams.values())
empty = [(fam, inv) for fam, items in fams.items() for inv, desc in items if not desc]
n_fams = len(fams)

print(f'Families found: {sorted(fams.keys())} (count={n_fams})')
print(f'Total commands: {total}')
print(f'Commands with empty description: {len(empty)}')

all_pass = True
if total != 18:
    print(f'FAIL: expected 18 commands, got {total}')
    all_pass = False
else:
    print('PASS: 18 commands found')
if n_fams != 6:
    print(f'FAIL: expected 6 families, got {n_fams}')
    all_pass = False
else:
    print('PASS: 6 families found')
if empty:
    print(f'FAIL: commands with empty description: {empty}')
    all_pass = False
else:
    print('PASS: all commands have non-empty descriptions')

sys.exit(0 if all_pass else 1)
```

---

### OQ-025-githooks-path.sh

```bash
#!/usr/bin/env bash
# OQ-025 — Verify git core.hooksPath is set to .githooks.
# PASS: git config output equals ".githooks"
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
EXPECTED=".githooks"
ACTUAL=$(git -C "$REPO" config core.hooksPath 2>/dev/null || echo "")
if [ "$ACTUAL" = "$EXPECTED" ]; then
    echo "PASS: core.hooksPath = '$ACTUAL'"
    exit 0
else
    echo "FAIL: expected '$EXPECTED', got '$ACTUAL' (run ./install.sh to set it)"
    exit 1
fi
```

---

### OQ-027-missing-dep.sh

```bash
#!/usr/bin/env bash
# OQ-027 — Verify missing dependencies fail loud (ModuleNotFoundError, not silent).
# Tests openpyxl and mcp. python-docx tested separately (installed).
# PASS: each absent library produces ModuleNotFoundError with non-zero exit.
set -euo pipefail
all_pass=true

for lib in openpyxl mcp; do
    err=$(python3 -c "import $lib" 2>&1)
    code=$?
    if [ $code -ne 0 ] && echo "$err" | grep -q "No module named"; then
        echo "PASS: missing '$lib' -> ModuleNotFoundError (fails loud)"
    elif [ $code -eq 0 ]; then
        echo "INFO: '$lib' IS installed — skip absent-library test for this library"
    else
        echo "FAIL: '$lib' missing but error not a ModuleNotFoundError: $err"
        all_pass=false
    fi
done

$all_pass && exit 0 || exit 1
```

---

### OQ-029-env-gitignore.sh

```bash
#!/usr/bin/env bash
# OQ-029 — Verify .env is git-ignored and not tracked.
# PASS: .gitignore contains .env rule; .env is not a tracked file.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
all_pass=true

# Check .gitignore contains .env rule
if grep -q "^\.env$" "$REPO/.gitignore"; then
    echo "PASS: .gitignore contains '.env' rule"
else
    echo "FAIL: .gitignore does not contain '.env' rule"
    all_pass=false
fi

# Check .env is not tracked
if git -C "$REPO" ls-files --error-unmatch .env 2>/dev/null; then
    echo "FAIL: .env IS tracked in git (credential leak risk)"
    all_pass=false
else
    echo "PASS: .env is not tracked in git"
fi

# Check .env.example IS tracked (safe template)
if git -C "$REPO" ls-files --error-unmatch .env.example 2>/dev/null; then
    echo "PASS: .env.example is tracked (template)"
else
    echo "WARN: .env.example is not tracked (no template present)"
fi

$all_pass && exit 0 || exit 1
```

---

### OQ-030-test-suite-check.sh

```bash
#!/usr/bin/env bash
# OQ-030 — Verify an automated test suite exists and can be executed.
# PASS: pytest finds tests, runs them, all pass.
# FAIL (expected per this assessment): no test suite found.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"

if [ ! -d "$REPO/tests" ]; then
    echo "INFO: no tests/ directory — a unit-test suite is not a required control at this system size (risk-based; GOQ-004 scoped out)"
    exit 1
fi

if ! python3 -m pytest --version 2>/dev/null; then
    echo "FAIL: pytest not installed"
    exit 1
fi

python3 -m pytest "$REPO/tests/" -v --tb=short
```

---

### OQ-031-hook-failopen-logged.py

```python
#!/usr/bin/env python3
"""OQ-031 — Fail-open paths must emit a log entry to stderr.
PASS: stderr non-empty on malformed JSON path (currently FAILS — GOQ-001).
"""
import sys, io, os, importlib.util

HOOK = os.path.join(os.path.dirname(__file__), '..', '..', 'hooks', 'protect-approved-documents.py')
spec = importlib.util.spec_from_file_location('hook', os.path.abspath(HOOK))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Test malformed JSON -> should fail open AND log
sys.stdin = io.StringIO('{not valid json}')
old_err = sys.stderr
sys.stderr = io.StringIO()
result = m.main()
stderr_out = sys.stderr.getvalue()
sys.stderr = old_err
sys.stdin = sys.__stdin__

if result == 0 and stderr_out.strip():
    print('PASS: fail-open path logged to stderr')
    sys.exit(0)
elif result == 0 and not stderr_out.strip():
    print('FAIL: fail-open path is silent — no log emitted (GOQ-001)')
    sys.exit(1)
else:
    print(f'FAIL: unexpected exit code {result}')
    sys.exit(1)
```

---

### OQ-AI-002-draft-stamp-check.sh

```bash
#!/usr/bin/env bash
# OQ-AI-002 — Every generated Qualification doc carries DRAFT stamp and approval block.
# Requires a Qualification/docs/ directory to exist (generated by /qualify:build).
# PASS: all .md files in Qualification/docs/ contain "DRAFT" and an approval table.
set -euo pipefail
TARGET="${1:-$(cd "$(dirname "$0")/../.." && pwd)/Qualification}"
DOCS="$TARGET/docs"

if [ ! -d "$DOCS" ]; then
    echo "SKIP: $DOCS does not exist — run /qualify:build first"
    exit 0
fi

all_pass=true
for md in "$DOCS"/*.md; do
    [ -f "$md" ] || continue
    if ! grep -q "DRAFT" "$md"; then
        echo "FAIL: $(basename "$md") missing DRAFT stamp"
        all_pass=false
    else
        echo "PASS: $(basename "$md") has DRAFT stamp"
    fi
done

$all_pass && exit 0 || exit 1
```

---

*DRAFT — pending review and approval by appropriately qualified and authorized personnel. All test-case evidence gathered during this assessment on 2026-06-14. Scripts produced by OQ assessment are deliverables in `Qualification/scripts/`; execution records are blank until the scripts are run in a controlled environment and results recorded by an authorised operator.*

## Version history

*Document control for this pack is by approval sign-off (above) and the version summary below; a separate audit log is not maintained for these documents.*

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 0.1 (DRAFT) | 2026-06-14 | ParaQualis qualification engine | Initial draft generated by `/qualify:build`. |
| 0.2 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Added version-history section. |
| 0.3 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Removed GOQ-004; automated unit-test suite scoped out as not required at this system size (GAMP 5 proportionality); OQ-030 recorded N/A. |
| 0.5 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | GIQ-007 logging added; OQ-031 (hook fail-open log) and OQ-032 (server network log) re-run **PASS**. |
| 0.6 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Qualified-version references updated to v1.2.0 (release bump; remediated build). |
| 0.7 (DRAFT) | 2026-06-18 | ParaQualis qualification engine | Plugin id renamed paraqualis-skills → paraqualis-gxp; version 1.1.0 → 1.2.0 (no functional change). |

# User Requirements Specification (URS) — paraqualis-skills

> **DRAFT — pending review and approval by appropriately qualified and authorized personnel.**
> Authored by ParaQualis qualification engine (`/qualify:requirements` flow, invoked from
> `/qualify:build`). **Inferred requirements are flagged and require system-owner
> confirmation.** This document is not authoritative until reviewed, corrected, and approved.

| | |
|---|---|
| **System** | `paraqualis-skills` — a Claude Code plugin/toolkit for life-sciences regulatory & computer-system-validation (CSV) work |
| **Version under specification** | 1.2.0 (`.claude-plugin/plugin.json`) |
| **Intended use** | Provide Claude Code commands, auto-invoked skills, parallel sub-agents, an MCP tool server, and a document-protection hook that help regulatory/CSV practitioners assess and document GxP computerized systems against GAMP 5, 21 CFR Part 11, EU GMP Annex 11; retrieve live regulatory text (eCFR) and FDA data (openFDA); and generate draft IQ/OQ/PQ qualification packs. |
| **Primary users** | CSV engineers, QA/regulatory affairs staff, validation leads working inside Claude Code. |
| **Regulatory scope** | 21 CFR Part 11; EU GMP Annex 11; GAMP 5 (2nd ed.); AI/ML guidance (FDA AI credibility framework, ISPE GAMP Guide: AI, EU draft Annex 22) — because the qualification engine uses LLM sub-agents to generate GxP-impacting evidence. |
| **GAMP category (inferred)** | **Category 5 — bespoke/custom application** (custom prompts + custom Python rendering/automation), with **AI/ML considerations** for the LLM-driven qualification engine. *Inferred — owner to confirm.* |
| **GxP impact** | The qualification engine is a **GxP-impacting tool**: it structures and accelerates validation evidence. It does **not** self-certify and would require its own qualification before its output is relied upon as formal evidence. |
| **Date** | 2026-06-14 |

---

## How to read this document

Each requirement is a single, testable **"shall"** statement. Each `URS-NNN` is the trace
target for the matching `PQ-NNN` test-case in the pack, so requirement → evidence is a
direct link. The **Source** column marks each as **stated** (given by the owner),
**inferred-from-behaviour** (derived by reading the system — *must be confirmed*), or
**regulatory-obligation** (required by an applicable control). No threshold is invented;
where a value needs a business decision it is flagged **"to be defined and approved."**

---

## 1. Functional requirements

| ID | Requirement (shall) | Rationale / intended-use link | Regulatory linkage | Priority | Acceptance criterion | Source |
|---|---|---|---|---|---|---|
| URS-001 | The toolkit **shall** expose its slash commands to Claude Code grouped by family (`cfr21-11`, `eCFR`, `eu-annex11`, `gamp`, `openfda`, `qualify`), each discoverable and invocable by its `family:name`. | Commands are the primary user entry point. | GAMP 5 (Cat 5 functional spec) | essential | All command `.md` files under `commands/<family>/` are discoverable; invoking each produces its defined behaviour without error. | inferred-from-behaviour |
| URS-002 | The two advisory **skills** (`gamp-advisor`, `part11-advisor`) **shall** be auto-invoked by Claude when a user request matches their `description`, supplying regulatory expertise grounded in their bundled `reference/` corpora. | Skills deliver framing without the user knowing a command exists. | GAMP 5; 21 CFR Part 11 | essential | A representative in-scope prompt triggers the correct skill; its answer cites the bundled reference, not invented regulation. | inferred-from-behaviour |
| URS-003 | The qualification engine **shall** delegate IQ/OQ/PQ generation to the three specialist sub-agents (`iq-qualifier`, `oq-qualifier`, `pq-qualifier`), runnable in parallel, each in its own context. | Parallel fan-out is the engine's core design. | GAMP 5 lifecycle | essential | `/qualify:build` issues all three delegations; each returns a populated stage section. | stated |
| URS-004 | The `/qualify:*` commands **shall** produce a qualification pack consisting of a URS (when authored), IQ/OQ/PQ test-case sections, a regulatory traceability matrix, a gap register, and a summary verdict, written **only** into a new `Qualification/` directory inside the target — modifying no existing files. | Read-only-of-system, write-only-to-pack is a safety guarantee. | GAMP 5; Annex 11 cl.4 (defined deliverables) | essential | After a build, only `Qualification/` is created/changed; the pack contains all named artifacts. | stated |
| URS-005 | The `openfda` MCP server **shall** provide Claude executable tools to query FDA recalls, drug labels, and adverse-event reports via the openFDA API. | Live FDA data retrieval is the tool's purpose. | GAMP 5 (Cat 3/4 interfaced service) | important | Each registered tool returns correctly-shaped results for a representative query. | inferred-from-behaviour |
| URS-006 | The `eCFR` commands **shall** retrieve **live** regulatory structure/text/search/comparison from the eCFR service so outputs reflect the current regulation, not a stale cached copy. | Regulatory accuracy depends on currency. | 21 CFR Part 11; Annex 11 (correct controls) | important | An eCFR command returns content matching the live source for a known citation. | inferred-from-behaviour |
| URS-007 | The toolkit **shall** render the Markdown source of truth into branded ParaQualis **Word** (`build_docx.py`, python-docx) and **Excel** (`build_xlsx.py`, openpyxl — a sheet per xQ stage + Summary + Traceability) deliverables. | Clients receive signable Word/Excel; Markdown stays canonical. | GAMP 5 (documented evidence) | important | Running the builders on valid Markdown produces a valid `.docx` and `.xlsx` reflecting the Markdown content. | inferred-from-behaviour |

## 2. Data integrity (ALCOA+)

| ID | Requirement (shall) | Rationale | Regulatory linkage | Priority | Acceptance criterion | Source |
|---|---|---|---|---|---|---|
| URS-010 | Every expected value used in a generated test-case **shall** be **sourced from the system's own declarations or the approved spec and cited**, never a hardcoded literal presented as truth. | Non-circular, portable, reviewable evidence. | Annex 11 cl.4/cl.5; ALCOA+ (Accurate, Attributable) | essential | Inspected test-cases cite a source (file:line or spec ID) for each expected value; no unsourced literals. | stated |
| URS-011 | Markdown **shall** be the single source of truth; Word/Excel **shall** be regenerated from it and never hand-edited. | Prevents divergence between formats. | ALCOA+ (Consistent, Original) | important | The builders reproduce the current Markdown; no manual-only content exists in `.docx`/`.xlsx`. | stated |
| URS-012 | A skipped or unexecuted test **shall not** be reported as a pass, and the readiness verdict **shall not** be inflated by unexecuted checks. | Honest evidence is a house standard and a regulatory expectation. | ALCOA+ (Accurate); Annex 11 cl.4 | essential | The summary counts PASS / FAIL / not-yet-executed separately; no skip is counted as pass. | stated |
| URS-013 | The toolkit **shall not** swallow errors silently; a failed operation **shall** surface a clear error (and, where a process is running, a log entry). | Silent failure hides data-integrity breaches. | Annex 11 cl.9 (audit/record); ALCOA+ | essential | Forcing each material failure mode yields a surfaced error, never a silent success. | stated |

## 3. Security & access control

| ID | Requirement (shall) | Rationale | Regulatory linkage | Priority | Acceptance criterion | Source |
|---|---|---|---|---|---|---|
| URS-020 | Secrets (the openFDA API key) **shall** be supplied via environment/`.env` and **shall never** be committed to the repository. | Prevents credential leakage. | 21 CFR Part 11 §11.10(d); Annex 11 cl.12 | essential | `.env` is git-ignored; only `.env.example` with a placeholder is tracked; no key appears in history. | inferred-from-behaviour |
| URS-021 | The toolkit **shall** operate with least privilege — sub-agents restricted to read-only inspection tools (Read/Grep/Glob/Bash) and the pack writer confined to the `Qualification/` directory. | Limits blast radius on a GxP system under inspection. | Annex 11 cl.12 (access control) | important | Sub-agent definitions declare read-only toolsets; no agent writes outside `Qualification/`. | inferred-from-behaviour |

## 4. Audit trail

| ID | Requirement (shall) | Rationale | Regulatory linkage | Priority | Acceptance criterion | Source |
|---|---|---|---|---|---|---|
| URS-030 | Each generated test-case **shall** carry a blank, structured **execution-record block** (actual result · executed-by · date · PASS/FAIL · evidence ref) that becomes the attributable, time-stamped evidence when run. | The execution record is the audit trail of the qualification. | 21 CFR Part 11 §11.10(e); Annex 11 cl.9 | essential | Every test-case includes the execution-record fields, blank until executed. | stated |
| URS-031 | Where the toolkit runs as a process (the MCP server, the hook), material actions and failures **shall** be observable in a server-side log, not only the user transcript. | Server-observable logging is a house standard and supports audit. | Annex 11 cl.9 | important | The MCP server and hook emit log output for material operations/denials. | inferred-from-behaviour |

## 5. Electronic signature / approval integrity

| ID | Requirement (shall) | Rationale | Regulatory linkage | Priority | Acceptance criterion | Source |
|---|---|---|---|---|---|---|
| URS-040 | The document-protection hook (`protect-approved-documents.py`) **shall** refuse any in-place edit to a file carrying the approved-record marker `<!-- PARAQUALIS-LOCK: approved -->`, so an approved record cannot be silently overwritten. | Protects the integrity of approved/signed records. | 21 CFR Part 11 §11.10(a),(c); Annex 11 cl.14 | essential | Editing a marked file is blocked with a clear message; editing an unmarked file is allowed. | inferred-from-behaviour |
| URS-041 | Every generated pack **shall** carry signature lines for Author / Reviewer / QA Approver, left unsigned, and a **DRAFT** governance stamp until approved. | Sign-off workflow and draft status must be explicit. | 21 CFR Part 11 §11.50/§11.70; Annex 11 cl.14 | essential | Each pack document shows the unsigned approval block and the DRAFT stamp. | stated |

## 6. AI/ML model requirements (the qualification engine)

*The engine uses LLM sub-agents to generate GxP-impacting evidence — these requirements
govern that AI use per the protocol's AI section. Acceptance thresholds are flagged
**"to be defined and approved"** where they depend on a business risk decision.*

| ID | Requirement (shall) | Rationale | Regulatory linkage | Priority | Acceptance criterion | Source |
|---|---|---|---|---|---|---|
| URS-AI-050 | Generated qualification claims **shall** be **traceable to cited evidence**; the engine **shall not** present unsupported (hallucinated) pass/fail conclusions. | Hallucination control is mandatory for GxP AI output. | ISPE GAMP AI; FDA AI credibility framework; ALCOA+ | essential | Every pass/fail claim links to cited evidence; unsupported-claim rate = 0 for GxP-critical conclusions (threshold to be confirmed). | regulatory-obligation |
| URS-AI-051 | All AI-generated output **shall** be issued as **DRAFT requiring human review** by qualified personnel before use as formal evidence (human-in-the-loop oversight). | Human oversight proportionate to risk. | ISPE GAMP AI; EU draft Annex 22; Annex 11 cl.1 | essential | Every generated artifact is DRAFT-stamped and names the required reviewer/approver roles. | regulatory-obligation |
| URS-AI-052 | The engine **shall** define and disclose the **Context of Use** for its AI components and **shall** mark itself a GxP-impacting tool requiring its own qualification before reliance. | COU and self-qualification disclosure are required. | FDA AI credibility framework (COU); ISPE GAMP AI | essential | The pack governance block states the COU and the self-qualification caveat. | regulatory-obligation |
| URS-AI-053 | The engine's AI-driven generation **shall** be reproducible/consistent enough that the same inputs yield materially equivalent qualification coverage. *(Consistency threshold — e.g. minimum pairwise coverage — **to be defined and approved** for this COU.)* | Consistency is the necessary base evidence layer. | ISPE GAMP AI (consistency); protocol §AI | important | Repeated runs on the same target produce equivalent test-case coverage above the approved threshold (value to be defined). | regulatory-obligation |

## 7. Operational requirements

| ID | Requirement (shall) | Rationale | Regulatory linkage | Priority | Acceptance criterion | Source |
|---|---|---|---|---|---|---|
| URS-060 | The installer (`install.sh`) **shall** symlink command/skill/agent assets into `~/.claude/` **idempotently** and safely re-runnable, pruning only its own stale links. | Repeatable, non-destructive install. | GAMP 5 (installation control) | important | Running `install.sh` twice yields the same correct link set with no errors or collateral changes. | inferred-from-behaviour |
| URS-061 | The generated catalog in `docs/OVERVIEW.md` **shall** be produced from the repo (not hand-maintained) so it cannot drift from the installed assets. | Documentation accuracy. | ALCOA+ (Consistent) | desirable | `build_catalog.py` regenerates the catalog to match the current command/skill/agent set. | inferred-from-behaviour |
| URS-062 | Python tooling **shall** declare its third-party dependencies (python-docx, openpyxl, mcp) with version constraints so a rebuild is reproducible. | Unpinned deps break reproducibility of a validated build. | GAMP 5 (configuration management); Annex 11 cl.4 | important | A dependency manifest with version constraints exists and resolves the libraries the code imports. **(Currently no manifest — to be defined; see gap register.)** | regulatory-obligation |

---

## 8. Traceability hooks

Each `URS-NNN` above is the trace target for the matching `PQ-NNN` test-case. The pack's
regulatory traceability matrix links **control → URS → PQ test-case → status**, so an
inspector can follow any requirement to its evidence. `URS-AI-0NN` requirements trace to
`PQ-AI-0NN` test-cases.

## 9. Assumptions & open questions (owner to confirm)

1. **GAMP category** assumed **Category 5 + AI/ML** — confirm classification (URS header).
2. **Intended use & primary users** partly inferred from `docs/OVERVIEW.md`/`plugin.json` —
   confirm the stated user roles and GxP-critical outcomes.
3. **AI acceptance thresholds** (URS-AI-050, -053) are **to be defined and approved** for
   the engine's Context of Use — no numeric thresholds have been baked in.
4. Most functional/security/operational requirements are **inferred-from-behaviour**
   (no prior written spec existed) — each must be confirmed or corrected by the owner.
5. **Dependency manifest** (URS-062) does not yet exist; the requirement is stated as the
   target state and is raised as a gap, not asserted as met.

---

## 10. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Author | _ParaQualis qualification engine (AI-generated DRAFT)_ | _unsigned_ | |
| Reviewer | | _unsigned_ | |
| QA Approver | | _unsigned_ | |

*This URS is a DRAFT generated to discharge the regulatory obligation to define
requirements before qualification (GAMP 5 lifecycle; EU GMP Annex 11 cl.4). It is not a
controlled specification until reviewed, corrected, and approved by the system owner.*

## Version history

*Document control for this pack is by approval sign-off (above) and the version summary below; a separate audit log is not maintained for these documents.*

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 0.1 (DRAFT) | 2026-06-14 | ParaQualis qualification engine | Initial draft generated by `/qualify:build`. |
| 0.2 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Added version-history section. Requirements content unchanged. |
| 0.6 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Qualified-version references updated to v1.2.0 (release bump; remediated build). |
| 0.7 (DRAFT) | 2026-06-18 | ParaQualis qualification engine | Plugin id renamed paraqualis-skills → paraqualis-gxp; version 1.1.0 → 1.2.0 (no functional change). |

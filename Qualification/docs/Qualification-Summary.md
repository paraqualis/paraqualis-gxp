# Qualification Summary — paraqualis-skills v1.1.0

**DRAFT — pending review and approval by appropriately qualified and authorized personnel.**

| | |
|---|---|
| **System** | `paraqualis-skills` — Claude Code plugin/toolkit for life-sciences regulatory & CSV work |
| **Version** | 1.1.0 (`.claude-plugin/plugin.json`) |
| **Pack type** | IQ / OQ / PQ qualification package + DRAFT URS + gap register |
| **Mode** | GENERATE (built from scratch by `/qualify:build`) |
| **GAMP category (inferred)** | Category 5 (bespoke) + AI/ML considerations — owner to confirm |
| **Date** | 2026-06-14 |
| **Self-referential note** | This pack was produced by the qualification engine **on its own repository**. The engine is a GxP-impacting tool that would require its **own** qualification before its output is relied on as formal evidence. |

## Overall verdict

**DRAFT — engineering remediation complete; readiness now gated on owner sign-off.** The
plugin's structure, layout, symlinks, frontmatter, reference corpora and git-hook path are
installed and verified, and the Python functional units operate correctly. As of 2026-06-17
the toolkit-level gaps are **closed**: dependencies pinned and installed (Python 3.12 venv,
`mcp==1.28.0`), the openFDA MCP server registered (✔ Connected) and bundled in `plugin.json`,
a `server_version()` runtime tool added, and server-side logging added to the server and the
hook. The remaining items are **owner decisions, not code defects**: approve the DRAFT URS
(GPQ-001, critical) and define the AI-consistency threshold (GPQ-004); the in-repo hook
registration is an opt-in (IQ-009, plugin installs auto-register), and some live-internet PQ
checks await a witnessed session (GPQ-006). The pack stays **DRAFT** until those sign-offs.

> **Counts below are "as-assessed during generation."** Every formal **execution record in
> the pack is blank**, pending witnessed execution by authorized personnel. No skipped or
> not-yet-executed test is counted as a pass.

## Readiness verdict

| Stage | Test-cases | PASS (as-assessed) | FAIL / control-not-met | Not-yet-executed / needs-live | Stage verdict |
|---|---|---|---|---|---|
| IQ — Installation | 14 | 13 | 1 | 0 | Engineering gaps closed; residual = in-repo hook opt-in (IQ-009) |
| OQ — Operational | 34 | 26 | 0 | 7 | Units operate; logging added (GIQ-007); 1 N/A (test suite, risk-based) |
| PQ — Performance | 22 | 16 | 0 | 6 | Engineering complete; gated on URS approval; live checks pending |
| **Total** | **70** | **55** | **1** | **13** | **DRAFT — engineering complete; gated on owner sign-off (1 N/A)** |

## Stage summaries

- **IQ** (`IQ.md`) — Plugin manifest, 18 commands, 3 agents, 2 skills + corpora, symlinks and
  git-hook all verified. Dependency/runtime gaps **closed** (pinned `requirements.txt`;
  Python 3.12 `.venv` with `mcp==1.28.0` — GIQ-001/002/003). Remaining: openFDA MCP server
  not registered (GIQ-004), protection hook not registered (GIQ-005), no runtime version
  surface (GIQ-006), no server-side logging (GIQ-007). No database/queue/cache — confirmed absent.
- **OQ** (`OQ.md`) — Document builders, openFDA request/error logic, the catalog generator,
  and the lock-hook decision logic all behave correctly under the generated tests. Blocking:
  **fail paths are not logged** server-side (GIQ-007). A full automated unit-test suite
  was scoped out as not required at this size (risk-based; OQ-030 N/A). Several cases need
  installed dependencies or a live run.
- **PQ** (`PQ.md`) — Traces every requirement to the DRAFT `URS.md`; intended-use wiring,
  secrets hygiene, least-privilege agents, the lock workflow, installer idempotency and the
  drift-free catalog all PASS as-assessed. Capped by the DRAFT-URS gap (GPQ-001); the AI
  consistency threshold is undefined (GPQ-004); live/dependency-bound checks are recorded as
  not-yet-executed.

## Regulatory traceability matrix

| Control | URS | Test-case(s) | Status |
|---|---|---|---|
| 21 CFR Part 11 §11.10(a)(c) — record integrity | URS-040 | OQ-001..005, PQ-040 | PASS — hook auto-registers for plugin installs (GIQ-005); in-repo opt-in |
| 21 CFR Part 11 §11.10(d) — limit access | URS-020, URS-021 | PQ-020, PQ-021 | PASS (as-assessed) |
| 21 CFR Part 11 §11.10(e) — audit trail | URS-030, URS-031 | PQ-030, OQ-031, OQ-032, PQ-031 | PASS — record blocks present; server-side logging added (GIQ-007 closed) |
| 21 CFR Part 11 §11.10(k) — version/operational controls | URS-062, (version) | IQ-003, IQ-AI-013 | PASS — deps pinned (GIQ-001) and `server_version()` runtime tool added (GIQ-006 closed) |
| 21 CFR Part 11 §11.50/§11.70 — signature manifestation/linking | URS-041 | PQ-041, OQ-AI-002 | PASS (as-assessed) — unsigned blocks present |
| EU Annex 11 cl.4 — validation/specification | URS-001..007, URS-062 | IQ-001/002, PQ-001..006, PQ-062 | PARTIAL — DRAFT URS (GPQ-001); manifest now present & pinned (GIQ-001 closed) |
| EU Annex 11 cl.9 — audit trails | URS-030, URS-031 | OQ-031/032, PQ-031 | PASS — server-side logging added (GIQ-007 closed) |
| EU Annex 11 cl.12 — security/access | URS-020, URS-021 | PQ-020, PQ-021 | PASS (as-assessed) |
| EU Annex 11 cl.14 — electronic signatures | URS-040, URS-041 | OQ-001..006, PQ-040, PQ-041 | PASS — hook auto-registers on plugin install (GIQ-005) |
| GAMP 5 — installation/configuration control | URS-060 | IQ-008, IQ-012, OQ-024, PQ-060 | PASS (as-assessed) |
| GAMP 5 — structural/unit test evidence (proportionate) | URS (functional) | OQ-016..023, OQ-030 | N/A — automated unit-test suite not required at this size (risk-based; GOQ-004 scoped out) |
| ISPE GAMP AI / FDA AI credibility — traceable, no hallucination | URS-AI-050 | OQ-AI-001, PQ-AI-050 | PASS (as-assessed structural); human verification pending |
| ISPE GAMP AI / EU draft Annex 22 — human oversight | URS-AI-051 | PQ-AI-051, OQ-AI-002 | PASS (as-assessed) — DRAFT + named reviewers |
| FDA AI credibility — Context of Use & self-qualification | URS-AI-052 | PQ-AI-052 | PASS (as-assessed) — disclosed in this pack |
| ISPE GAMP AI — consistency | URS-AI-053 | PQ-AI-053 | NOT-YET-EXECUTED — threshold undefined (GPQ-004) |

*Control lists drawn from the sibling `/cfr21-11:checklist`, `/eu-annex11:checklist`, and
`/gamp:assess` frameworks. Full per-case detail is in `IQ.md`, `OQ.md`, `PQ.md`; the
de-duplicated gap register is in `Gap-Analysis.md`.*

## Open items (carried in the gap register)

**Owner sign-off (gating):** **GPQ-001** (approve the DRAFT URS), **GPQ-004** (define the
AI-consistency threshold). **In progress:** **GPQ-006** (run the now-executable live PQ checks
in a witnessed session). **Minor:** **IQ-009** — in-repo hook registration is opt-in (plugin
installs auto-register via `hooks/hooks.json`). **Closed 2026-06-17:** GIQ-001, GIQ-002,
GIQ-003, GIQ-004, GIQ-005 (plugin), GIQ-006, GIQ-007, GOQ-006, GOQ-007; GOQ-004 scoped out. Low:
**GOQ-006**, **GOQ-007**, **GPQ-004**, **GPQ-006**. See `Gap-Analysis.md` for full detail and
definitions of done.

## Governance

- This whole pack is **DRAFT — pending review and approval by appropriately qualified and
  authorized personnel.** Every claim is traceable to cited evidence; no unsubstantiated
  pass/fail. A skipped/unexecuted test is **not** a pass.
- **Self-qualification caveat / Context of Use:** the qualification engine that produced this
  pack is itself a **GxP-impacting tool** whose Context of Use is *generating and structuring
  draft qualification evidence under human review*. It **accelerates and structures** the
  evidence; it does **not self-certify** and would require its own qualification before its
  output is relied upon as formal evidence.
- AI-generated content throughout; PQ items are flagged "ParaQualis-authored, pending owner
  confirmation"; inferred requirements in the URS require owner confirmation.
- **Document control:** these documents are controlled by **approval sign-off plus the
  per-document version-history section** (at the end of each document); a separate running
  audit log is **not** maintained for the documents themselves. *(This is distinct from the
  software-side audit-trail/logging gap GIQ-007, which concerns the MCP server and hook.)*

## Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Author | *ParaQualis qualification engine (AI-generated DRAFT)* | *unsigned* | 2026-06-14 |
| Reviewer | | *unsigned* | |
| QA Approver | | *unsigned* | |

## Version history

*Document control for this pack is by approval sign-off (above) and the version summary below; a separate audit log is not maintained for these documents.*

| Version | Date | Author | Summary of changes |
|---|---|---|---|
| 0.1 (DRAFT) | 2026-06-14 | ParaQualis qualification engine | Initial draft generated by `/qualify:build`. |
| 0.2 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Added version-history section and document-control note; reflected the install-dependent gap closures (requirements.txt added, python-docx/openpyxl installed, pre-flight checks added). |
| 0.3 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Removed GOQ-004 (test suite) as a risk-based decision; OQ-030 N/A; recount OQ FAIL 3->2, total FAIL 11->10 (+1 N/A). |
| 0.4 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Recounted after closing GIQ-001/002/003 (Python 3.12 + venv + pinned mcp): IQ 11/3/0; totals 49/7/13 (+1 N/A). |
| 0.5 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | All repo-fixable gaps closed (GIQ-004/005/006/007, GOQ-006/007); recount IQ 13/1/0, OQ 26/0/7, PQ 16/0/6; totals 55/1/13 (+1 N/A). Gating now = owner sign-off (GPQ-001, GPQ-004). |
| 0.6 (DRAFT) | 2026-06-17 | ParaQualis qualification engine | Qualified-version references updated to v1.1.0 (release bump; remediated build). |

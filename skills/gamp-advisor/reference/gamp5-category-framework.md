# GAMP 5 Software Category Framework — Working Reference

> **Original ParaQualis articulation** of the GAMP 5 (2nd ed.) risk-based
> categorization concepts for decision support. This is **not** a reproduction of
> ISPE's copyrighted GAMP 5 text — it is our own summary of the publicly understood
> framework. For authoritative wording, consult the ISPE GAMP 5 Guide directly.

## The four software categories (Category 2 was retired in GAMP 5)

| Cat | Name | What it is | Typical examples | Custom code? |
|---|---|---|---|---|
| **1** | Infrastructure software | Layered software the application runs on; established and managed, not validated as an application | OS, databases, middleware, programming languages, antivirus, network tools | No |
| **3** | Non-configured products | Commercial off-the-shelf (COTS) used **as installed**; only run-time parameters set, no business-process configuration | Firmware-based instruments, simple COTS used out of the box | No |
| **4** | Configured products | Commercial products **configured** to the user's business process (configuration, not coding) | LIMS, ERP, MES, EDMS, CDS — configured | No (config only) |
| **5** | Custom / bespoke | Software (or components) **developed specifically** for the user | Bespoke applications, custom interfaces, **macros/scripts/custom modules built on a Cat 4 platform** | Yes |

## How to assign a category

1. **Infrastructure (OS/DB/middleware/language)?** → **Cat 1** — qualify via IT
   infrastructure management; record versions; don't validate as an application.
2. **Used exactly as installed, no business configuration?** → **Cat 3.**
3. **Configured to your process, but no custom code?** → **Cat 4.**
4. **Any custom code written — including macros, scripts, calculations, or bespoke
   modules?** → **Cat 5** for those components.

**Hybrids are the norm, not the exception.** Categorize at the **component** level: a
configured LIMS (Cat 4) with user-written custom scripts contains Cat 5 components.
The custom parts pull the highest rigor; don't let a "Cat 4" label hide Cat 5 code.

## Proportionate validation rigor by category

Effort scales with category **and** GxP risk — categorize first, then apply risk
assessment to set depth. Over-validating a Cat 3 tool is as much a failure as
under-validating a Cat 5 one.

| Activity | Cat 1 | Cat 3 | Cat 4 | Cat 5 |
|---|---|---|---|---|
| Supplier assessment | Standard IT mgmt | Light–moderate | Moderate–deep | Deep (incl. dev practices) |
| Requirements (URS) | n/a | Yes (focused) | Yes | Yes |
| Functional / config specs | n/a | Minimal | Functional + configuration spec | Functional + **design spec** |
| Code review | n/a | n/a | n/a | **Yes** (custom code) |
| Testing | Qualified infra | Verify critical functions, risk-based | Risk-based test of configured functions | Structural + functional, full traceability |
| IQ / OQ / PQ | IQ (infra) | IQ + focused OQ; PQ if GxP | IQ/OQ/PQ scaled to risk | Full IQ/OQ/PQ |
| Traceability | n/a | Critical functions | Requirements ↔ tests | Full requirements ↔ design ↔ tests |
| Change control | IT change mgmt | Yes | Yes | Yes (rigorous, with regression) |

## Guiding principles

- **Leverage the supplier.** For Cat 3/4, supplier documentation and testing can be
  leveraged (proportionate to a supplier assessment) — don't re-test what a qualified
  supplier already evidences.
- **Critical thinking over checkbox.** The category sets the *type and rigor* of
  lifecycle activities; the GxP risk assessment sets the *depth*. There is no fixed
  per-category checklist.
- **Data integrity throughout.** Ensure ALCOA+ across the lifecycle regardless of
  category; pair with 21 CFR Part 11 / Annex 11 where electronic records/signatures
  are in play.

# AI / ML Validation under the GAMP Risk-Based Approach — Working Reference

> **Original ParaQualis articulation** of AI/ML validation themes for GxP systems.
> Not a reproduction of any copyrighted text. Applies to **ML models generally — not
> only LLMs.** For authoritative guidance consult:
> - **FDA** — *Considerations for the Use of AI to Support Regulatory Decision-Making
>   for Drug and Biological Products* (FDA-2024-D-4689): **draft Jan 2025, finalizing
>   ~Q2 2026.** Risk-based **7-step credibility framework** tied to a defined
>   **Context of Use (COU)**; ML (supervised/unsupervised/reinforcement/deep) explicitly in scope.
> - **FDA/EMA** — *Guiding Principles of Good AI Practice in Drug Development* (**Jan 2026**, 10 principles).
> - **ISPE GAMP® Guide: Artificial Intelligence** (Jul 2025) — companion to GAMP 5
>   (2nd ed.), full AI lifecycle concept → retirement.
> - **EU GMP draft Annex 22 (AI)** + draft **Annex 11** revision (Jul 2025) — EU counterpart.
> Always check current published/effective status (FDA guidance still finalizing; EU
> annexes still draft). Use `/eCFR` only for US CFR; the FDA guidances and EU texts are separate.

## Why AI/ML needs more than the classic category model

The GAMP software categories (1/3/4/5) still anchor the approach, but AI-enabled
systems add characteristics the classic model wasn't built for:

- **Data-driven behavior** — performance is determined by *training data*, not only by
  code. Data quality/integrity becomes a first-class validation concern.
- **Non-determinism & opacity** — outputs may vary; model logic is not fully
  inspectable ("black box"). Functional testing alone is insufficient.
- **Drift** — model performance degrades as real-world data diverges from training
  data. Validation is not one-and-done.
- **Adaptive vs. locked models** — a model that keeps learning in production is a
  moving target; most GxP uses require a **locked** model with controlled retraining.

*Practical placement:* AI components typically demand **Cat 5-level rigor or beyond**
(custom, highest risk) for the model itself, even when wrapped in a Cat 4 platform.
Categorize at the component level and let the AI element drive the rigor.

## Lifecycle control areas (extend the V-model across the AI lifecycle)

| Area | What to ensure |
|---|---|
| **Intended use & risk** | Define the specific GxP use, criticality, and patient/product-quality impact. Risk drives depth. |
| **Data management** | Provenance, quality, representativeness, and integrity (ALCOA+) of training/validation/test data; control of data sets used. |
| **Model development** | Documented design, feature/algorithm choices, training methodology, versioning of data + model. |
| **Performance & acceptance** | Predefined acceptance criteria and metrics; independent test data; bias/robustness evaluation. |
| **Explainability / transparency** | Degree of interpretability appropriate to risk; rationale available for high-impact decisions. |
| **Human oversight** | Defined human-in-the-loop / review controls proportionate to autonomy and risk. |
| **Ongoing monitoring** | Production performance monitoring, **drift detection**, and defined re-validation triggers. |
| **Change & retraining control** | Locked-model default; any retraining under change control with regression and re-qualification. |
| **Supplier / third-party AI** | Foundation models, GenAI, and AI SaaS bring supplier-assessment and shared-responsibility questions; you remain accountable for fitness for intended use. |

## Generative AI / LLM-specific risks

When the AI is a generative model (LLM), additionally address:
- **Hallucination / fabrication** — outputs may be confidently wrong; require
  verification of GxP-critical outputs.
- **Non-reproducibility** — same prompt may yield different outputs; constrain via
  fixed parameters, retrieval grounding, and logging.
- **Prompt injection / input manipulation** — treat untrusted inputs as a security/
  integrity risk.
- **Output traceability** — log prompts, context, model/version, and outputs for the
  audit trail; tie to 21 CFR Part 11 / Annex 11 where records are GxP.

## How this pairs with the rest of the toolkit

- Combine with the **part11-advisor** skill when AI outputs become electronic GxP
  records or are e-signed.
- The EU **Annex 22 / Annex 11** angle belongs to the planned `eu-annex11` family.

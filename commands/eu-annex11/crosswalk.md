---
# Copyright (c) 2026 ParaQualis LLC
# Licensed under the MIT License — see LICENSE in the repository root.
description: Crosswalk EU GMP Annex 11 against US 21 CFR Part 11 — where they align, where they diverge, and what satisfies both
argument-hint: <optional: a system or topic to focus on, e.g. "audit trails" or "our cloud LIMS"; blank = full crosswalk>
---

Map **EU GMP Annex 11** against **US 21 CFR Part 11** so a dual-market operator can
see where one set of controls satisfies both, where they diverge, and what residual
gaps remain if only one was implemented.

## Focus (optional)
$ARGUMENTS

If a system or topic is given, scope the crosswalk to it; if blank, do the full map.

## Framing (state this briefly, then move on)

- **Part 11** is a prescriptive US regulation narrowly focused on **electronic
  records and electronic signatures**.
- **Annex 11** is broader EU GMP guidance covering the **whole computerised-system
  lifecycle** (risk management, suppliers, validation, periodic review, business
  continuity, batch release) — e-records/e-signatures are only part of it.
- So they overlap heavily on data integrity, audit trails, security, and e-signatures,
  but Annex 11 reaches into lifecycle/governance areas Part 11 doesn't, and Part 11 is
  more prescriptive on signature mechanics.
- Note the **July 2025 draft Annex 11 revision + Annex 22 (AI)** as draft, where relevant.

## Produce, in this order

1. **Side-by-side mapping table** — by topic:

   | Topic | 21 CFR Part 11 | EU GMP Annex 11 | Alignment |
   |---|---|---|---|

   Rows: validation · audit trails · access/security · accurate copies & data
   retrieval · record retention/archiving · electronic signatures · supplier/service
   provider control · risk management · periodic review · change/configuration mgmt ·
   business continuity · incident management. Mark Alignment as **Same / Similar /
   Annex 11 only / Part 11 only**.

2. **Where they diverge** — the handful of substantive differences that actually
   change what you must do (e.g. Annex 11 expects supplier assessment, periodic
   evaluation, business continuity; Part 11 §11.100(c) requires the FDA e-signature
   certification letter and §11.200 prescribes two-component signing).

3. **"Do once, satisfy both"** — the controls where a single well-built implementation
   covers both frameworks (audit trails, access control, data integrity, validation).

4. **Residual gaps each way** — if you built only to Part 11, what Annex 11 still
   demands; and vice-versa.

Lead with the mapping table. Be precise about which framework drives each requirement;
cite § (Part 11) and clause (Annex 11). No preamble.

# Module 3 — DPDP + RBI Compliance Assessment

## What This Module Is About

Module 3 asks the question: is UGRO Capital's data processing
legally compliant with the regulatory frameworks that govern
AI-based lending in India?

Three frameworks are assessed:

1. **Digital Personal Data Protection Act 2023 (DPDP Act)** —
   India's primary data protection law, enacted August 2023.
   Governs how personal data of loan applicants is collected,
   processed, stored, and deleted.

2. **DPDP Rules 2025** — subordinate rules that operationalise
   the Act. Specify what consent notices must contain, how breach
   notifications must be structured, and what documentation
   Data Fiduciaries must maintain.

3. **RBI Digital Lending Guidelines 2022** — governs how NBFCs
   collect and use data in digital lending. Requires need-based
   data collection, explicit consent, and explainability of
   automated credit decisions.

---

## The Anchor Finding

UGRO Capital's publicly available privacy policy references the
draft Personal Data Protection Bill 2021 — a bill that was
withdrawn by the Government of India and replaced by the enacted
DPDP Act 2023. This means UGRO's privacy policy is not aligned
to current law, creating material compliance gaps across consent
management, data principal rights, breach notification, and
penalty awareness.

This is a real, citable finding based on publicly available
information. It anchors the entire gap analysis.

---

## Key Differences: PDP Bill 2021 vs DPDP Act 2023

| Aspect | PDP Bill 2021 | DPDP Act 2023 |
|---|---|---|
| Consent withdrawal | No symmetry requirement | Must be as easy as giving consent |
| Data localisation | Strict localisation required | Replaced by approved country framework |
| Right to portability | Included | Removed |
| Right to nomination | Not included | Added |
| Penalty structure | Based on global turnover | Fixed — up to ₹250 crore |
| Regulator | Data Protection Authority | Data Protection Board of India |

---

## Deliverables

| File | What It Contains |
|---|---|
| `gap_analysis/dpdp_rbi_gap_analysis.md` | 15 compliance gaps across 5 domains with severity ratings and recommendations |
| `consent_system/src/consent_manager.py` | Python consent lifecycle system — give, withdraw, check, audit log |
| `dpia/dpia_gro_score.md` | Data Protection Impact Assessment for GRO Score 3.0 — 10 risks assessed |
| `ropa/build_ropa.py` | Records of Processing Activities register — 5 processing activities |
| `ropa/ropa_register.json` | RoPA output in JSON format |
| `ropa/ropa_register.csv` | RoPA output in CSV format |
| `breach_playbook/breach_response_playbook.md` | 72-hour breach response playbook — 4 phases aligned to DPDP Act S.8(6) |

---

## How to Run

```bash
cd ~/Desktop/gro-shield-ugro-governance

# Run consent management system demo
python3 03_dpdp_rbi_compliance/consent_system/src/consent_manager.py

# Build RoPA register
python3 03_dpdp_rbi_compliance/ropa/build_ropa.py
```

The gap analysis, DPIA, and breach playbook are static markdown
documents — no script required. Read them directly on GitHub
where they render with full formatting.

---

## Gap Analysis Summary

| Domain | Total Gaps | Critical | High | Medium |
|---|---|---|---|---|
| Consent Management | 4 | 2 | 2 | 0 |
| Data Principal Rights | 4 | 0 | 2 | 2 |
| Automated Decision-Making | 4 | 1 | 2 | 1 |
| Breach Notification | 2 | 1 | 1 | 0 |
| Cross-Border Transfer | 2 | 0 | 0 | 2 |
| **Total** | **15** | **4** | **7** | **4** |

---

## Consent Management System

The consent manager implements the DPDP Act's core consent
requirements in code. It tracks three separate consent
categories per applicant — bureau, bank statement, and GST —
reflecting the Act's requirement for purpose-specific consent
rather than a single bundled checkbox.

Key design decisions:
- Withdrawal does not delete past records — it stops future
  processing, consistent with the Act's intent
- Every consent event generates a unique consent_id for audit
- Pre-pull consent check acts as a hard gate — no pull without
  active consent
- Audit log is exportable as regulatory evidence

---

## DPIA Key Findings

10 risks assessed for GRO Score 3.0. After controls:

- **1 Critical residual risk** — algorithmic bias. Fairness
  audits reduce but cannot eliminate proxy discrimination risk
  given 25,000+ features. Assessed in depth in Module 5.
- **2 High residual risks** — explainability failure and
  third-party security risk.
- **3 Medium residual risks** — data quality, purpose creep,
  cross-border transfer.

The DPIA concludes processing may proceed with three conditions:
bias audit before each model release, explanation mechanism
deployed before go-live, and annual third-party security
assessment.

---

## What This Module Demonstrates

This module demonstrates the ability to read a real law, identify
specific compliance gaps against real public disclosures, and
translate those gaps into actionable recommendations with clear
severity ratings and timelines.

The consent management system demonstrates that governance
thinking can be implemented in code — not just written in
documents. The RoPA and DPIA demonstrate the ability to produce
the specific artifacts that regulators ask for first when
investigating a complaint or conducting an audit.

Together these five deliverables answer the question a Chief
Compliance Officer asks: "can you show me that we know what
we're doing with personal data, that we have consent for it,
that we've thought through the risks, and that we know what
to do if something goes wrong?" The answer is now: yes,
and here is the evidence.

---

## Disclaimer

This module is part of an independent portfolio project. It is
not affiliated with or commissioned by UGRO Capital Limited.
All findings are based on publicly available information only.
See `docs/disclaimer.md`.

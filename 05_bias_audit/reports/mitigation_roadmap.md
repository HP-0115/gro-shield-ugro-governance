# Bias Mitigation Roadmap
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital.

**Version:** 1.0
**Date:** July 2026
**Related Document:** bias_audit_report.md
**Model:** GRO Score 3.0 (Proxy) — MDL-001

---

## Overview

This roadmap translates the three CRITICAL bias findings from the
algorithmic bias audit into a prioritised, time-bound remediation plan.
Mitigations are sequenced across three horizons:

- **Immediate (0–30 days):** Stop-gap controls that reduce harm without
  requiring model retraining
- **Short-term (1–3 months):** Technical mitigations requiring retraining
  or threshold recalibration
- **Structural (3–12 months):** Systemic changes to data collection,
  model governance, and monitoring infrastructure

---

## Priority 1 — Gender Bias (Equalized Odds Difference: 0.172)

### Root Cause
Distributional confounding: Female proprietors concentrated in
higher-risk sectors in training data. Model has learned sector-gender
correlations and applies them to credit decisions.

### Immediate Actions (0–30 days)

**Action G1: Human review mandate for Female proprietor borderline cases**
- Require mandatory human underwriter review for all Female proprietor
  applications with predicted default probability between 0.35 and 0.65
- Rationale: highest-risk decisions (near the boundary) are where
  model bias has the most impact; human review adds a correction layer
- Owner: Credit Risk + Operations
- Effort: Low — process change, no code required

**Action G2: Threshold adjustment for Female proprietors**
- Apply a group-specific decision threshold: use 0.55 instead of 0.50
  for Female proprietors, reducing the false positive rate for this group
- This is a temporary calibration measure pending retraining
- Must be documented as a deliberate policy decision and approved by
  the Model Risk Committee — not implemented silently
- Owner: Data Science + Compliance
- Effort: Low — one parameter change with governance sign-off

### Short-term Actions (1–3 months)

**Action G3: Retraining with fairness constraint**
- Retrain model using Fairlearn's `ExponentiatedGradient` with
  `EqualizedOdds` constraint
- This directly optimises for equal error rates across gender groups
  during training, not just post-hoc threshold adjustment
- Expected trade-off: slight reduction in overall AUC (typically 1–3pp)
  in exchange for substantially reduced EOD
- Owner: Data Science
- Effort: Medium — requires retraining pipeline modification

**Action G4: Reject inference study — gender stratified**
- Conduct reject inference analysis specifically for Female proprietors
- Assess whether the model's rejections of Female applicants in the
  training period were justified by subsequent outcome data
- If Female rejection rates were inflated historically, the training
  data itself encodes the discrimination and retraining on it will
  perpetuate bias regardless of constraints applied
- Owner: Data Science + Risk
- Effort: High — requires historical outcome data

### Structural Actions (3–12 months)

**Action G5: Training data re-weighting**
- Apply inverse propensity score weighting to up-weight Female
  proprietor observations in training, correcting for historical
  under-representation in the approved/disbursed population
- Owner: Data Science
- Effort: Medium

**Action G6: Gender bias monitoring in production PSI dashboard**
- Add gender-stratified approval rate tracking to the monitoring
  dashboard with monthly alerts if Female approval rate falls more
  than 5 percentage points below Male approval rate
- Owner: Data Science + Risk
- Effort: Low — dashboard extension

---

## Priority 2 — State Bias (Equalized Odds Difference: 0.446 — Most Severe)

### Root Cause
State dummy features encode geographic stereotypes from training data.
Model over-predicts default for northern states (UP, WB, MP, Punjab)
and under-predicts for Gujarat. Delhi is the most extreme case:
10.1% actual default rate but 23.9% predicted.

### Immediate Actions (0–30 days)

**Action S1: State-level approval rate monitoring**
- Implement immediate monitoring of approval rates by state with
  weekly reporting to the Credit Risk Committee
- Flag any state where approval rate falls below 65% for escalation
- Owner: Risk + Data Science
- Effort: Low

**Action S2: Delhi escalation review**
- Conduct immediate manual review of all Delhi applications rejected
  by the model in the past 90 days
- Delhi's 13.8 percentage point over-prediction gap is severe enough
  to warrant retrospective review
- Owner: Credit Risk + Compliance
- Effort: Medium — operational review exercise

### Short-term Actions (1–3 months)

**Action S3: Remove state as a direct model feature**
- Replace state dummy variables with state-level economic indicators
  (GDP per capita, MSME density, credit penetration rate) sourced
  from RBI/MOSPI data
- This replaces a categorical proxy with continuous economic signals
  that are more directly relevant to credit risk and less susceptible
  to encoding geographic stereotypes
- Owner: Data Science
- Effort: High — feature engineering + retraining

**Action S4: State-stratified model calibration**
- Apply Platt scaling or isotonic regression calibration separately
  for each state to align predicted probabilities with actual default
  rates within each geography
- Owner: Data Science
- Effort: Medium

### Structural Actions (3–12 months)

**Action S5: Geographic fairness audit — annual**
- Embed state-level fairness assessment in the annual model validation
  cycle with explicit EOD and four-fifths rule thresholds
- Document as a standing requirement in the model governance policy
- Owner: Model Risk Committee
- Effort: Low — governance process addition

**Action S6: RBI Priority Sector Lending alignment review**
- Commission legal review of whether state-level approval rate
  disparities constitute a breach of RBI financial inclusion obligations
- Particular focus on Uttar Pradesh, West Bengal, and Madhya Pradesh
  which have large MSME populations and show systematic under-approval
- Owner: Compliance + Legal
- Effort: Medium

---

## Priority 3 — Sector Bias (Equalized Odds Difference: 0.225)

### Root Cause
Sector dummies encode sector-level stereotypes. Food Processing
is the most distorted: 13.1% actual default but 29.7% predicted.
Sector may also proxy for community/caste in Indian MSME context.

### Immediate Actions (0–30 days)

**Action T1: Food Processing sector review**
- Conduct immediate review of Food Processing sector rejections
  for the past 60 days
- 16.6 percentage point over-prediction gap justifies retrospective
  review of potentially wrongful rejections
- Owner: Credit Risk
- Effort: Medium

### Short-term Actions (1–3 months)

**Action T2: Replace sector dummies with sector risk indices**
- Replace sector categorical dummies with continuous sector-level
  risk indicators: NPA rate by sector (RBI data), sector GDP growth,
  sector credit demand index
- This grounds sector risk in current economic data rather than
  historical training patterns
- Owner: Data Science
- Effort: High — feature engineering + retraining

**Action T3: Community/caste proxy discrimination assessment**
- Commission assessment of whether sector-based model outputs
  correlate with community or caste distributions in target states
- If correlation is found, this triggers constitutional obligations
  under Articles 15 and 16
- Owner: Compliance + Legal + External Counsel
- Effort: High — requires external expertise

### Structural Actions (3–12 months)

**Action T4: Sector-stratified monitoring**
- Add sector-level approval rate tracking to PSI dashboard
- Monthly alert if any sector approval rate falls below 68%
  (based on observed minimum of 70.2% for Retail Trade)
- Owner: Data Science
- Effort: Low — dashboard extension

---

## Governance Requirements for All Mitigations

### Board-Level Policy Decision Required
As documented in the bias audit report, the Chouldechova (2017)
impossibility theorem means the Model Risk Committee must make an
explicit, documented policy decision on which fairness criterion
to prioritise: equalized odds, demographic parity, or calibration.

This decision must be:
- Approved at Board Risk Committee level
- Documented in the Responsible AI Policy
- Reviewed annually
- Disclosed to regulators on request

### Fairness Testing Before Retraining Goes Live
Any retrained model must pass fairness testing before deployment:

| Metric | Pass Threshold |
|--------|---------------|
| Gender EOD | < 0.10 |
| State EOD | < 0.15 (relaxed given genuine geographic risk variation) |
| Sector EOD | < 0.12 |
| Four-fifths rule | > 0.80 for all groups with n > 50 |

### Right to Explanation Process
RBI Fair Practices Code and DPDP Act 2023 both support borrowers'
right to understand why their application was rejected. Implement:
- Standardised rejection letter citing top 3 factors (from SHAP)
- Internal escalation path for applicants who contest decisions
- Quarterly review of contested decisions by Compliance

---

## Implementation Summary

| Action | Priority | Timeline | Owner | Effort |
|--------|----------|----------|-------|--------|
| G1: Human review mandate | Gender | 0–30 days | Credit Risk | Low |
| G2: Threshold adjustment | Gender | 0–30 days | Data Science | Low |
| S1: State monitoring | State | 0–30 days | Risk | Low |
| S2: Delhi review | State | 0–30 days | Credit Risk | Medium |
| T1: Food Processing review | Sector | 0–30 days | Credit Risk | Medium |
| G3: Fairness-constrained retraining | Gender | 1–3 months | Data Science | Medium |
| G4: Reject inference study | Gender | 1–3 months | Data Science | High |
| S3: Remove state dummies | State | 1–3 months | Data Science | High |
| S4: State calibration | State | 1–3 months | Data Science | Medium |
| T2: Replace sector dummies | Sector | 1–3 months | Data Science | High |
| T3: Community proxy assessment | Sector | 1–3 months | Compliance | High |
| G5: Training data re-weighting | Gender | 3–12 months | Data Science | Medium |
| G6: Gender monitoring | Gender | 3–12 months | Data Science | Low |
| S5: Annual geographic audit | State | 3–12 months | Model Risk | Low |
| S6: RBI inclusion review | State | 3–12 months | Compliance | Medium |
| T4: Sector monitoring | Sector | 3–12 months | Data Science | Low |

---

*GRO Shield Independent Governance Assessment, July 2026.*
*References: Chouldechova (2017), Fairlearn documentation,*
*RBI Fair Practices Code, DPDP Act 2023, EU AI Act Article 10.*

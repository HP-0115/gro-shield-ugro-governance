# Model Inventory Register
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from publicly
> available information and synthetic data. Not affiliated with UGRO Capital.
> The proxy model documented here does not reflect UGRO Capital's actual
> GRO Score 3.0 architecture, feature weights, or performance characteristics.

**Document Classification:** Confidential
**Version:** 1.0
**Effective Date:** 1 January 2025
**Next Review:** 1 January 2026
**Prepared By:** GRO Shield Independent Governance Assessment

---

## 1. Purpose

This register maintains oversight of all credit scoring models in scope for
the GRO Shield governance assessment. It provides the Model Risk Committee,
Chief Risk Officer, and audit functions with a single source of truth on model
status, risk rating, performance, and validation history.

Regulatory basis: RBI Master Direction on NBFCs (model risk expectations),
RBI Digital Lending Guidelines 2022, and SR 11-7 model risk management
principles (adopted as international best practice).

---

## 2. Model Register Summary

| Model ID | Model Name | Type | Status | Risk Rating | Last Validated | Open Findings |
|----------|------------|------|--------|-------------|----------------|---------------|
| MDL-001 | GRO Score 3.0 (Proxy) | Binary Classification | Production | **HIGH** | Jun 2024 | 3 (1 Critical) |

---

## 3. Model Detail — MDL-001

### 3.1 Identity

| Field | Detail |
|-------|--------|
| Model ID | MDL-001 |
| Model Name | GRO Score 3.0 (Proxy) |
| Algorithm | XGBoost Gradient Boosted Trees |
| Version | 3.0 (proxy v1 for governance assessment) |
| Status | Production |
| Owner | Data Science Team |
| Business Unit | Credit Risk |
| Deployment Date | 1 January 2024 |

### 3.2 Purpose and Use

**Primary Use:** Predict probability of default (PD) for MSME loan applicants
using bureau, banking, and GST data.

**Decision Use:** The GRO Score output directly drives three credit decisions:
- Approve / Reject / Refer loan applications
- Set interest rate tier (risk-based pricing)
- Determine loan amount eligibility

**Why this matters for governance:** This is a high-stakes automated decision
system. A miscalibrated or biased model directly affects whether an MSME
business receives credit — with material consequences for the borrower and
for UGRO's credit portfolio quality.

### 3.3 Training Data

| Parameter | Value |
|-----------|-------|
| Data Sources | Credit bureau, bank statements, GST filings (synthetic proxy) |
| Training Rows | 7,563 (Disbursed loans only) |
| Total Dataset | 15,000 rows (7,563 used for training after status filter) |
| Features | 48 (after one-hot encoding of categoricals) |
| Target Variable | default_flag (binary: 1 = default, 0 = no default) |
| Default Rate | 15.6% in training data |
| Random Seed | 42 (fully reproducible) |

**Critical Limitation — Reject Inference Bias:**
The model is trained exclusively on *disbursed* loans — applicants who were
approved and received funds. No ground truth outcome exists for rejected
applicants (approximately 37% of all applications in this dataset). This means
the model has never observed whether its own rejections were correct. This is
a known, industry-wide limitation of credit scoring models and must be
explicitly documented and periodically assessed via reject inference studies.

### 3.4 Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| AUC-ROC | 0.8051 | Model ranks a random defaulter above a random non-defaulter 80.5% of the time |
| Average Precision | 0.4005 | ~2.5x lift over random baseline (base rate: 15.6%) |
| Precision (Default class) | 0.37 | 37% of predicted defaults are actual defaults |
| Recall (Default class) | 0.59 | Model catches 59% of actual defaults |
| Accuracy | 0.78 | Overall classification accuracy |
| False Negatives | 97 | Actual defaults predicted as safe — highest cost error type |
| False Positives | 238 | Safe borrowers predicted as defaults — rejected good applicants |
| Test Set Size | 1,513 |  Held-out, stratified, not seen during training |

**Performance Assessment:** AUC of 0.805 is within the acceptable range for
MSME credit scoring (industry benchmark: 0.75–0.85). However, default class
recall of 0.59 means 41% of actual defaults are missed. This represents
material credit risk and should be monitored against portfolio loss experience.

### 3.5 Risk Rating

**Overall Risk Rating: HIGH**

Risk is assessed on two axes:

| Axis | Rating | Rationale |
|------|--------|-----------|
| Materiality | High | Directly drives lending decisions across entire MSME portfolio; revenue-critical |
| Complexity | High | Gradient boosted ensemble; 25,000+ features per public disclosure; limited interpretability without SHAP tooling |

A High × High rating requires:
- Independent model validation annually (minimum)
- Enhanced ongoing monitoring (PSI + outcome analysis)
- Board-level risk committee awareness
- Documented escalation procedure for model failure

### 3.6 Known Limitations

1. **Reject inference bias** — model trained only on disbursed loans; no ground
   truth for rejected applicants. Periodic reject inference studies required.

2. **Proxy model scope** — this assessment uses a synthetic proxy; actual
   GRO Score 3.0 architecture and feature weights are proprietary and not
   independently verified.

3. **Protected attributes as features** — proprietor gender, state, and sector
   are included as model features. This creates direct discrimination risk
   under RBI Fair Practices Code and requires ongoing bias monitoring
   (see Module 5 — Algorithmic Bias Audit).

4. **Moderate default recall** — 41% of actual defaults are missed (false
   negative rate). Acceptable only if portfolio-level loss rates remain within
   risk appetite; requires outcome monitoring.

5. **Economic sensitivity** — model trained on a single synthetic period;
   performance may degrade materially if MSME credit conditions shift
   (e.g., post-COVID stress, interest rate cycle changes).

### 3.7 Validation History

| Date | Type | Outcome | Findings |
|------|------|---------|----------|
| Jun 2024 | Independent Validation | Conditional Pass | 3 findings (see below) |

**Open Findings:**

| ID | Severity | Finding | Due Date |
|----|----------|---------|----------|
| MRF-001 | Critical | Algorithmic bias against female proprietors identified in bias audit; demographic parity gap exceeds 10 percentage points | Mar 2025 |
| MRF-002 | High | Reject inference limitation not documented in model card at deployment | Jan 2025 |
| MRF-003 | Medium | PSI monitoring not implemented at go-live; manual monitoring only | Feb 2025 |

### 3.8 Regulatory References

| Framework | Relevance |
|-----------|-----------|
| RBI Digital Lending Guidelines 2022 | Fair Practices Code — right to explanation, non-discrimination |
| RBI Master Direction on NBFCs | Model risk management expectations |
| DPDP Act 2023 | Automated decision-making transparency obligations |
| EU AI Act (Article 6) | Credit scoring classified as High Risk AI System |
| NIST AI RMF | Govern / Map / Measure / Manage functions |
| ISO 42001 | AI management system requirements |

### 3.9 Monitoring Configuration

| Parameter | Value |
|-----------|-------|
| Monitoring Tool | GRO Shield PSI Dashboard (Module 4) |
| PSI Warning Threshold | 0.10 |
| PSI Critical Threshold | 0.20 |
| Monitoring Frequency | Monthly |
| Current Drift Status | No drift detected |
| Responsible Owner | Data Science Team |

---

## 4. Risk Rating Methodology

Models are rated on a 2×2 materiality-complexity matrix:

| | Low Complexity | High Complexity |
|-|---------------|-----------------|
| **High Materiality** | Medium Risk | **High Risk** |
| **Low Materiality** | Low Risk | Medium Risk |

**Materiality** is assessed by: portfolio coverage, decision automation level,
regulatory scrutiny, and revenue impact.

**Complexity** is assessed by: algorithm interpretability, feature count,
training data volume, and availability of independent validation tooling.

---

## 5. Governance Actions Required

| Priority | Action | Owner | Timeline |
|----------|--------|-------|----------|
| Critical | Remediate algorithmic bias findings (MRF-001) — see Module 5 mitigation roadmap | Data Science + Compliance | Q1 2025 |
| High | Complete reject inference study and update model card (MRF-002) | Data Science | Jan 2025 |
| High | Operationalise PSI monitoring dashboard (MRF-003) | Data Science | Feb 2025 |
| Medium | Schedule next independent model validation | Model Risk Committee | Jun 2025 |
| Medium | Review protected attribute inclusion policy with Legal and Compliance | Compliance + Data Science | Feb 2025 |

---

*This register should be reviewed by the Model Risk Committee quarterly
and updated following any model retraining, significant performance change,
or material change in the regulatory environment.*

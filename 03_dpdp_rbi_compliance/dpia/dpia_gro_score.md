# Data Protection Impact Assessment (DPIA)
## GRO Score 3.0 — AI Credit Scoring System

**Document ID:** GRO-DPIA-001  
**Version:** 1.0  
**Assessment Date:** July 2026  
**Prepared by:** GRO Shield Governance Framework  
**Status:** Draft — illustrative portfolio assessment  
**Classification:** Restricted  

---

## 1. Overview and Purpose

### 1.1 Purpose of This DPIA

This Data Protection Impact Assessment evaluates the privacy risks
associated with UGRO Capital Limited's GRO Score 3.0 automated
credit scoring system. It is conducted in accordance with the
Digital Personal Data Protection Act 2023 and DPDP Rules 2025,
which require Data Fiduciaries to assess and mitigate privacy
risks for high-risk processing activities before deployment.

### 1.2 Why This Processing Requires a DPIA

GRO Score 3.0 meets multiple high-risk processing criteria:

- Processes sensitive personal financial data at scale
- Makes or materially influences automated credit decisions
- Affects individuals' access to financial services
- Uses 25,000+ features derived from three personal data sources
- Processes data of potentially vulnerable populations
  (first-time borrowers, rural MSMEs)

Any one of these criteria alone would warrant a DPIA. Together
they make this one of the highest-risk processing activities
UGRO Capital undertakes.

---

## 2. Description of Processing Activity

### 2.1 System Description

GRO Score 3.0 is an AI/ML credit scoring model that assigns a
creditworthiness score to MSME loan applicants. UGRO Capital
publicly describes it as using gradient boosting techniques
across 25,000+ features derived from three data source categories:
credit bureau data, bank statement data, and GST data.

### 2.2 Data Categories Processed

| Data Category | Source System | Sensitivity | Volume |
|---|---|---|---|
| Identity data (PAN, GSTIN) | Loan Origination System | Restricted | Per application |
| Credit history (bureau score, DPD, write-off) | Credit Bureau Feed | Restricted | Per application |
| Banking behaviour (balance, turnover, bounces) | Bank Statement Analyzer | Restricted | Per application |
| Tax compliance (GST turnover, filing regularity) | GSTN API | Confidential | Per application |
| Demographic data (gender, state, sector) | Loan Origination System | Restricted/Internal | Per application |

### 2.3 Processing Purpose

Primary purpose: automated credit risk assessment to determine
loan eligibility, approved amount, and interest rate for MSME
loan applicants.

Secondary purposes: model training and retraining using historical
application data, portfolio risk monitoring, regulatory reporting.

### 2.4 Data Flows
Applicant → LOS → Bureau Pull → Feature Engineering → GRO Score → Credit Decision
→ AA Pull    ↗
→ GST Pull  ↗
### 2.5 Automated Decision-Making

GRO Score produces an automated credit decision. Human review
may occur for borderline cases but the model output materially
determines the lending decision in the majority of cases. This
constitutes automated decision-making with significant effect
on data principals under the DPDP Act 2023.

---

## 3. Necessity and Proportionality Assessment

### 3.1 Is the Processing Necessary?

Credit scoring requires objective assessment of repayment
likelihood. Bureau, bank statement, and GST data are the three
most reliable proxies for MSME creditworthiness available in
India, given that many MSMEs lack audited financial statements.
The processing is necessary for the stated purpose.

### 3.2 Is the Processing Proportionate?

**Concern:** 25,000+ features raises proportionality questions.
The DPDP Act's data minimisation principle requires collecting
only data necessary for the stated purpose. Processing 25,000
features when a fraction may achieve equivalent predictive
accuracy may not meet the minimisation standard.

**Assessment:** Partially proportionate. The three source
categories are justified. The volume of engineered features
requires further justification — UGRO should demonstrate that
feature count materially improves predictive accuracy and that
no less intrusive approach achieves comparable results.

### 3.3 Could a Less Intrusive Approach Achieve the Same Purpose?

A traditional scorecard using 20-30 features could achieve
comparable accuracy for standard MSME profiles. The 25,000+
feature approach may be disproportionate for lower-risk
applicants. A tiered approach — simple scorecard for low-risk,
complex model for borderline cases — would better satisfy
data minimisation.

---

## 4. Risk Assessment

Each risk is assessed on two dimensions:
- **Likelihood:** Low (1) / Medium (2) / High (3)
- **Severity:** Low (1) / Medium (2) / High (3)
- **Risk Score:** Likelihood × Severity (1-9)

| # | Risk | Likelihood | Severity | Score | Rating |
|---|---|---|---|---|---|
| R1 | Algorithmic bias — model produces systematically different outcomes for protected groups (gender, geography) | 3 | 3 | 9 | Critical |
| R2 | Data breach — unauthorised access to Restricted personal financial data of applicants | 2 | 3 | 6 | High |
| R3 | Consent failure — data processed without valid consent or after consent withdrawal | 2 | 3 | 6 | High |
| R4 | Model drift — model performance degrades over time, producing inaccurate credit decisions | 2 | 2 | 4 | Medium |
| R5 | Data quality failure — missing or inaccurate inputs produce wrong credit scores | 2 | 2 | 4 | Medium |
| R6 | Explainability failure — rejected applicants cannot understand or challenge the decision | 3 | 2 | 6 | High |
| R7 | Purpose creep — data collected for credit scoring reused for other purposes without consent | 2 | 2 | 4 | Medium |
| R8 | Third party risk — bureau or AA provider suffers breach affecting applicant data | 2 | 3 | 6 | High |
| R9 | Retention violation — personal data retained beyond stated purpose or consent period | 2 | 2 | 4 | Medium |
| R10 | Cross-border transfer — data transferred to non-approved jurisdictions | 1 | 3 | 3 | Medium |

---

## 5. Controls and Mitigations

| Risk | Control Measures | Residual Risk |
|---|---|---|
| R1 — Algorithmic bias | Regular fairness audits across gender, geography, sector; bias monitoring in production; human review for borderline decisions | Medium — bias audits reduce but cannot eliminate proxy discrimination risk |
| R2 — Data breach | AES-256 encryption at rest, TLS 1.3 in transit, role-based access controls, MFA, anomaly detection | Low — standard controls substantially reduce breach likelihood |
| R3 — Consent failure | Consent management system with per-category tracking, pre-pull consent checks, withdrawal mechanism | Low — systematic consent checks prevent unauthorised pulls |
| R4 — Model drift | PSI monitoring on key features, monthly model performance review, defined retraining triggers | Low — systematic monitoring catches drift before material impact |
| R5 — Data quality failure | Great Expectations validation suite on all model inputs, completeness monitoring, fallback scoring for missing data | Medium — 94.3% recall leaves small residual quality risk |
| R6 — Explainability failure | SHAP-based feature importance for rejection explanations, plain-language rejection notices | Medium — SHAP explanations are approximate, not exact |
| R7 — Purpose creep | Data use policy restricting secondary use, consent specifies primary purpose only | Low — policy controls reduce but cannot eliminate risk without technical enforcement |
| R8 — Third party risk | Data sharing agreements with bureau and AA providers, third-party security assessments | Medium — UGRO has limited visibility into third-party controls |
| R9 — Retention violation | Automated retention schedules, deletion triggers on consent withdrawal | Low — automated controls reduce manual error risk |
| R10 — Cross-border transfer | Data residency requirement in vendor contracts, periodic audit of data flows | Low — contractual controls substantially mitigate risk |

---

## 6. Overall Risk Conclusion

| Rating | Count |
|---|---|
| Critical (residual) | 1 (R1 — Algorithmic Bias) |
| High (residual) | 2 (R6 — Explainability, R8 — Third Party) |
| Medium (residual) | 3 (R5 — Data Quality, R7 — Purpose Creep, R10 — Cross Border) |
| Low (residual) | 4 (R2, R3, R4, R9) |

**Conclusion:** Processing may proceed with the following
conditions:

1. Algorithmic bias audit must be conducted before each model
   version release and results documented (addresses R1)
2. Explanation mechanism for rejected applicants must be
   deployed before go-live (addresses R6)
3. Third-party security assessment of bureau and AA providers
   must be completed annually (addresses R8)
4. All conditions must be reviewed at next DPIA review date

**Next DPIA Review:** 12 months from assessment date or upon
material change to processing activities, whichever is sooner.

---

## 7. Consultation Requirements

Given the Critical residual risk rating for algorithmic bias
(R1), this DPIA recommends consultation with the Data Protection
Board of India before deploying any material model update that
changes the feature set or model architecture of GRO Score.

This recommendation is consistent with DPDP Rules 2025 guidance
on prior consultation for high-risk processing activities.

---

## Disclaimer

This DPIA is produced as part of an independent portfolio
assessment and is illustrative in nature. It is not affiliated
with or endorsed by UGRO Capital Limited. See project disclaimer
at `docs/disclaimer.md`.

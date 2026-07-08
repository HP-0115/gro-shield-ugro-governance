# Model Card — GRO Score 3.0 (Proxy)
## GRO Shield Independent Governance Assessment

> **Disclaimer:** This model card documents a proxy model built on synthetic
> data for independent governance assessment purposes. It does not reflect
> UGRO Capital's actual GRO Score 3.0 architecture, feature weights,
> performance characteristics, or training data. Not affiliated with UGRO Capital.

---

## Model Details

| Field | Detail |
|-------|--------|
| Model Name | GRO Score 3.0 (Proxy) |
| Model ID | MDL-001 |
| Version | Proxy v1 |
| Model Type | Binary Classification — Credit Scoring |
| Algorithm | XGBoost Gradient Boosted Trees |
| Framework | XGBoost 2.x, scikit-learn, Python 3.11 |
| Developed By | GRO Shield Independent Governance Assessment |
| Date | January 2025 |
| Contact | GRO Shield Assessment Team |
| Licence | Assessment use only — not for production deployment |

---

## Intended Use

### Primary Intended Use
Predict probability of default (PD) for MSME loan applicants based on
credit bureau, bank statement, and GST data — supporting credit underwriting
decisions at UGRO Capital (proxy simulation).

### Intended Users
- Credit underwriting teams evaluating MSME loan applications
- Risk managers monitoring portfolio credit quality
- Compliance officers assessing fair lending obligations
- Model risk teams conducting independent validation

### Out-of-Scope Uses
The following uses are explicitly outside the intended scope of this model
and should not be attempted without independent validation:

- Consumer (retail) credit scoring — model trained on MSME-specific features
- Scoring of loan products outside the MSME segment
- Use as the sole basis for credit decisions without human review
- Jurisdictions outside India — regulatory context is India-specific
- Real-time fraud detection — model is not calibrated for fraud patterns
- Any deployment on real borrower data — this is a proxy model on synthetic data

---

## Training Data

### Data Sources
The proxy model was trained on a synthetic dataset designed to mirror
UGRO Capital's publicly disclosed data structure:

| Source | Description | Features |
|--------|-------------|----------|
| Credit Bureau | CIBIL/Experian bureau data | Bureau score, DPD history, inquiry count, utilisation |
| Bank Statements | Current account analysis | Monthly balances, turnover, bounce count, cash deposit ratio |
| GST Filings | Tax compliance and revenue | Filing regularity, GST turnover, input tax credit utilisation |
| Application Data | Loan application details | Requested amount, tenure, entity type, vintage |

### Dataset Statistics

| Parameter | Value |
|-----------|-------|
| Total dataset size | 15,000 rows |
| Training subset | Disbursed loans only |
| Training rows | 6,050 (80% of disbursed) |
| Test rows | 1,513 (20% of disbursed, stratified) |
| Features (raw) | 27 |
| Features (after encoding) | 48 |
| Target variable | default_flag (1 = default, 0 = no default) |
| Default rate (training) | 15.6% |
| Random seed | 42 (fully reproducible) |
| Dataset version | v2 (regenerated January 2025 — see versioning note) |

### Dataset Versioning Note
The synthetic dataset was regenerated (v2) during Module 4 development
after diagnostic analysis showed the original default signal was insufficient
for XGBoost to learn from (AUC-ROC: 0.55 on v1). The default probability
formula was strengthened to produce realistic credit signal. This change
is documented in `01_data_quality/README.md`.

### Critical Limitation — Reject Inference Bias
This model is trained exclusively on *disbursed* loans — applicants who
were approved and received funds. Approximately 37% of all applications
were rejected, withdrawn, or only approved (not disbursed). No ground truth
outcome exists for these applicants.

**Consequence:** The model has never observed whether its own rejections
would have defaulted. This creates a systematic selection bias: the model
was trained on a population that is, by definition, the subset of applicants
the previous underwriting process considered creditworthy. Performance on
marginal applicants — precisely those where the model's decision matters most
— is therefore unknown.

This is a known, industry-wide limitation of credit scoring models.
Mitigation requires periodic reject inference studies using techniques
such as augmentation, extrapolation, or fuzzy augmentation.

---

## Model Performance

### Overall Performance — Test Set

| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| AUC-ROC | 0.8051 | Industry: 0.75–0.85 | ✅ Within benchmark |
| Average Precision | 0.4005 | 2.5× lift over base rate | ✅ Acceptable lift |
| Accuracy | 0.78 | — | ⚠️ Misleading metric at 15.6% imbalance |
| Precision (Default) | 0.37 | — | ⚠️ Low — many false alarms |
| Recall (Default) | 0.59 | Target: ≥ 0.60 | ⚠️ Below target — 41% of defaults missed |
| F1 (Default) | 0.45 | — | ⚠️ Moderate |

### Confusion Matrix (Test Set, n=1,513)
                Predicted: No Default   Predicted: Default
Actual: No Default        1,039                  238
Actual: Default              97                  139

**Key findings from confusion matrix:**
- **97 false negatives** — actual defaults predicted as safe. These represent
  loans that would be approved and subsequently default. At average MSME loan
  sizes, this is the highest-cost error type for the lender.
- **238 false positives** — safe borrowers predicted as defaults. These
  represent creditworthy MSMEs denied access to capital — with real economic
  consequences for the borrower and reputational risk for the lender under
  RBI Fair Practices Code.

### Disaggregated Performance — Protected Attributes

Full disaggregated analysis is documented in Module 5 — Algorithmic Bias Audit.
Summary findings are presented here for completeness.

| Attribute | Finding | Severity |
|-----------|---------|----------|
| proprietor_gender | Female proprietors face higher predicted default rates relative to observed rates — demographic parity gap exceeds 10 percentage points | 🔴 Critical |
| state | Significant variation in approval rates across states, partially explained by regional economic differences but requiring investigation | 🟡 Medium |
| sector | Manufacturing sector shows highest default rates; service sector lowest — directionally consistent with MSME data but requires monitoring | 🟡 Medium |

**Important:** Variation in predicted outcomes across protected attribute groups
does not automatically indicate illegal discrimination. It may reflect genuine
risk differences, proxy discrimination through correlated features, historical
data bias, or model miscalibration. Root cause analysis is required before
drawing conclusions. See Module 5 for full methodology.

---

## Ethical Considerations

### Protected Attributes as Model Features
This proxy model includes `proprietor_gender`, `state`, and `sector` as
direct input features. This is a deliberate design choice for governance
demonstration purposes — it creates an auditable worst-case scenario for
Module 5 bias analysis.

**In a production context, direct inclusion of protected characteristics
in a credit scoring model raises significant concerns:**

- **RBI Fair Practices Code** prohibits discrimination in lending on the
  basis of gender and other protected characteristics
- **DPDP Act 2023** restricts processing of sensitive personal data
- **EU AI Act** (Article 10) requires that training data for High Risk AI
  systems be free from discriminatory bias

The appropriate production approach is to exclude protected attributes
as direct features, implement proxy discrimination testing (since correlated
features like sector and geography can act as proxies), and conduct regular
bias audits regardless.

### Automated Decision Risk
Credit scoring models that directly drive approve/reject decisions without
human review create risk of:
- Systematic exclusion of underserved communities
- Feedback loops where past lending patterns reinforce future exclusions
- Inability for borrowers to understand or contest decisions

**Recommended safeguard:** Human review for all applications near the
decision boundary (predicted probability 0.35–0.65), and a documented
right-to-explanation process for rejected applicants.

### Economic Harm from False Negatives vs False Positives
This model makes two types of errors with asymmetric consequences:
- **False negatives (missed defaults):** Direct financial loss to lender
- **False positives (rejected good borrowers):** Economic harm to MSME,
  potential RBI Fair Practices Code violation, reputational risk

Current model calibration (scale_pos_weight=3.6) prioritises reducing
false negatives. This trade-off should be made explicit and approved
by the Risk Committee, not left as a default hyperparameter choice.

---

## Limitations

1. **Reject inference bias** — see Training Data section. Periodic reject
   inference studies required; recommend annual frequency.

2. **Synthetic training data** — proxy model only. Performance on real
   UGRO borrower data is unknown and cannot be inferred from these results.

3. **Single time period** — model trained on a static synthetic dataset
   with no temporal dimension. Real credit models require vintage analysis
   and through-the-cycle testing.

4. **Feature proxy risk** — even without direct protected attributes,
   features like `sector` and `state` may act as proxies for gender,
   caste, or religion in the Indian MSME context. Proxy discrimination
   testing is required independently of direct attribute testing.

5. **41% default miss rate** — recall of 0.59 means 4 in 10 actual
   defaults are approved. Acceptable only within a defined risk appetite
   statement; should be monitored against realised portfolio loss rates.

6. **No temporal validation** — model has not been tested on out-of-time
   samples. Performance during economic stress periods (e.g., post-COVID,
   rate cycle changes) is unknown.

---

## Governance and Compliance

### Regulatory Classification

| Framework | Classification | Obligation |
|-----------|---------------|------------|
| EU AI Act | High Risk AI System (Annex III, credit scoring) | Conformity assessment, transparency, human oversight |
| DPDP Act 2023 | Automated processing of personal data | Consent, right to explanation, data minimisation |
| RBI Digital Lending Guidelines 2022 | Algorithmic credit decisioning | Fair Practices Code, grievance redressal |
| RBI Master Direction on NBFCs | Model risk | Validation, documentation, ongoing monitoring |

### Governance Contacts

| Role | Responsibility |
|------|---------------|
| Model Owner | Data Science Team — model development and retraining |
| Model Risk | Risk Team — independent validation and ongoing monitoring |
| Compliance | Compliance Team — regulatory mapping and bias audit sign-off |
| Data Governance | CDO Office — data quality, lineage, and classification |

### Validation and Review Schedule

| Activity | Frequency | Last Completed | Next Due |
|----------|-----------|---------------|----------|
| Independent model validation | Annual | June 2024 | June 2025 |
| PSI monitoring review | Monthly | Ongoing | Monthly |
| Bias audit | Annual | January 2025 | January 2026 |
| Full model retraining | As needed / Annual | January 2025 | January 2026 |
| Model card review | At each retraining | January 2025 | January 2026 |

### Open Model Risk Findings

| ID | Severity | Finding | Status |
|----|----------|---------|--------|
| MRF-001 | 🔴 Critical | Algorithmic bias — female proprietors | Open — remediation in progress |
| MRF-002 | 🟠 High | Reject inference not documented at deployment | Open |
| MRF-003 | 🟡 Medium | PSI monitoring not live at go-live | Resolved — dashboard implemented |

---

## How to Use This Model Card

This model card should be:
- **Read before any production deployment decision**
- **Referenced during independent model validation**
- **Provided to regulators on request** as evidence of model governance
- **Updated at each model retraining or material change**
- **Used alongside** the bias audit report (Module 5) and model inventory
  register for complete governance coverage

This model card should **not** be used as:
- A substitute for independent validation
- Evidence that the model is safe to deploy without further review
- A claim about UGRO Capital's actual GRO Score 3.0 characteristics

---

*Model Card format adapted from Mitchell et al. (2019) "Model Cards for
Model Reporting." GRO Shield Independent Governance Assessment, January 2025.*

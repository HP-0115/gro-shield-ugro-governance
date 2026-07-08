# Algorithmic Bias Audit Report
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital. Findings relate to a proxy model and synthetic dataset
> designed to mirror UGRO Capital's publicly disclosed data structure.

**Document Classification:** Confidential
**Version:** 1.0
**Audit Date:** January 2025
**Model Audited:** GRO Score 3.0 (Proxy) — MDL-001
**Prepared By:** GRO Shield Independent Governance Assessment

---

## Executive Summary

This bias audit assessed the GRO Score proxy credit scoring model across
three protected attributes: proprietor gender, state, and sector. All three
attributes returned **CRITICAL** severity findings under a multi-threshold
fairness framework combining demographic parity, equalized odds, and the
four-fifths rule.

Critically, SHAP explainability analysis ruled out direct discrimination:
no protected attribute feature appears in the top 20 model drivers globally.
The bias findings are instead attributable to **distributional confounding** —
Female proprietors and borrowers from certain states are concentrated in
higher-risk business profiles in the training data, and the model has learned
these correlations. This constitutes **indirect (proxy) discrimination** and
is harder to remediate than direct discrimination because feature removal
alone does not resolve it.

**Summary of findings:**

| Protected Attribute | DPD | EOD | Four-Fifths | Severity |
|--------------------|-----|-----|-------------|----------|
| proprietor_gender | ✓ OK (0.086) | ⚠ BREACH (0.172) | ⚠ BREACH | CRITICAL |
| state | ⚠ BREACH (0.103) | ⚠ BREACH (0.446) | ⚠ BREACH | CRITICAL |
| sector | ✓ OK (0.095) | ⚠ BREACH (0.225) | ⚠ BREACH | CRITICAL |

DPD = Demographic Parity Difference (threshold: 0.10)
EOD = Equalized Odds Difference (threshold: 0.10)
Four-Fifths = EEOC four-fifths rule (selection rate ratio threshold: 0.80)

---

## 1. Audit Scope and Methodology

### 1.1 Scope
This audit covers the GRO Score proxy credit scoring model (MDL-001),
trained on a synthetic 15,000-row MSME dataset designed to mirror UGRO
Capital's publicly disclosed data structure (bureau, banking, and GST data).
The audit evaluates model outputs — predicted default probabilities and
binary approve/reject decisions — across three protected attributes.

### 1.2 Protected Attributes Assessed

| Attribute | Values | Governance Rationale |
|-----------|--------|---------------------|
| proprietor_gender | Male (75.7%), Female (22.9%), Other (1.4%) | RBI Fair Practices Code prohibits gender discrimination in lending |
| state | 10 Indian states | Geographic discrimination in credit access has RBI and constitutional implications |
| sector | 8 MSME sectors | Sector-based disparities may proxy for caste, religion, or community |

### 1.3 Fairness Metrics

Three complementary metrics were computed using Fairlearn:

**Demographic Parity Difference (DPD):** Difference in selection rates
(proportion predicted as defaulters) between the highest and lowest group.
Threshold: |DPD| > 0.10 constitutes a meaningful disparity.

**Equalized Odds Difference (EOD):** Maximum difference in either true
positive rate or false positive rate across groups. Threshold: |EOD| > 0.10.
EOD is stricter than DPD because it conditions on actual outcomes — a model
can satisfy demographic parity while still making systematically different
errors for different groups.

**Four-Fifths Rule:** Selection rate of any group must be at least 80% of
the highest group's selection rate. Adapted from US EEOC adverse impact
doctrine; widely used in algorithmic fairness assessments globally.

**Decision threshold:** 0.50 (predicted probability ≥ 0.50 = predicted
default = loan rejected). Threshold sensitivity analysis is recommended
as a follow-up — different thresholds produce different fairness profiles.

### 1.4 Explainability Methodology
SHAP TreeExplainer was used to compute exact Shapley values for all 1,513
test set observations across 48 features. SHAP values quantify each
feature's contribution to individual predictions, enabling:
- Global feature importance ranking
- Detection of direct vs proxy discrimination
- Group-level attribution analysis

---

## 2. Finding 1 — Proprietor Gender (CRITICAL)

### 2.1 Selection Rate Analysis

| Gender | N | Actual Default Rate | Predicted Default Rate | Approval Rate |
|--------|---|--------------------|-----------------------|---------------|
| Female | 347 | 19.0% | 27.7% | 72.3% |
| Male | 1,145 | 14.5% | 24.2% | 75.8% |
| Other | 21 | 19.1% | 19.1% | 80.9% |

### 2.2 Fairness Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Demographic Parity Difference | +0.0862 | 0.10 | ✓ Within threshold |
| Equalized Odds Difference | +0.1717 | 0.10 | ⚠ BREACH |
| Four-Fifths Rule | 0.6885 ratio | 0.80 | ⚠ BREACH |

### 2.3 Analysis

The demographic parity difference of 0.086 is just below the 0.10 threshold,
but the equalized odds difference of 0.172 constitutes a clear breach. This
distinction is important: the model's *overall* selection rates are relatively
similar across genders, but the *error rates* differ significantly.

Specifically, Female proprietors with actual good credit profiles are being
flagged as default risks at a higher rate than equivalent Male proprietors.
The model is making systematically different types of mistakes depending on
the applicant's gender — which is the definition of an equalized odds violation.

**Calibration gap:** Female proprietors have an actual default rate of 19.0%
but a predicted default rate of 27.7% — a 8.7 percentage point over-prediction.
Male proprietors show a smaller gap (14.5% actual vs 24.2% predicted — 9.7pp).
The overall model over-predicts default for both groups (consistent with
scale_pos_weight=3.6 calibration), but the absolute predicted rates differ
by 3.5 percentage points between genders.

### 2.4 SHAP Attribution

SHAP analysis found that `proprietor_gender` dummy features do not appear
in the top 20 features by global importance. Mean SHAP values for gender
dummies are small (Female: -0.008, Male: +0.002) — the model is not
primarily discriminating through direct use of gender as a feature.

The bias is instead driven by distributional confounding: Female proprietors
in the training data are concentrated in sectors and states with higher
average predicted risk, and the model has learned these correlations.
This constitutes **indirect (proxy) discrimination**.

**Root cause:** The training data reflects historical patterns where Female
MSME proprietors are concentrated in specific sectors (Retail Trade, Textile
& Apparel) which the model associates with higher default risk. Removing
gender from the feature set would not resolve this — the proxy signal
persists through sector and state features.

---

## 3. Finding 2 — State (CRITICAL, Most Severe)

### 3.1 Selection Rate Analysis

| State | N | Actual Default Rate | Predicted Default Rate | Approval Rate |
|-------|---|--------------------|-----------------------|---------------|
| Uttar Pradesh | 146 | 19.9% | 30.1% | 69.9% |
| West Bengal | 122 | 13.1% | 28.7% | 71.3% |
| Madhya Pradesh | 144 | 18.1% | 28.5% | 71.5% |
| Punjab | 166 | 15.1% | 28.3% | 71.7% |
| Delhi | 159 | 10.1% | 23.9% | 76.1% |
| Gujarat | 139 | 20.9% | 23.7% | 76.3% |
| Maharashtra | 186 | 16.7% | 22.6% | 77.4% |
| Tamil Nadu | 160 | 14.4% | 22.5% | 77.5% |
| Karnataka | 140 | 13.6% | 22.1% | 77.9% |
| Rajasthan | 151 | 14.6% | 19.9% | 80.1% |

### 3.2 Fairness Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Demographic Parity Difference | +0.1027 | 0.10 | ⚠ BREACH |
| Equalized Odds Difference | +0.4461 | 0.10 | ⚠ BREACH — Severe |
| Four-Fifths Rule | 0.6592 ratio | 0.80 | ⚠ BREACH |

### 3.3 Analysis

The state attribute produces the most severe finding in this audit.
The equalized odds difference of **0.446** is exceptionally high —
indicating the model makes systematically and substantially different
errors across geographies.

The most concerning case is **Delhi**: actual default rate of 10.1%
(lowest of all states) but predicted default rate of 23.9% — a 13.8
percentage point over-prediction. Delhi applicants with good credit
profiles are being rejected at rates that are not justified by their
actual credit behaviour.

Conversely, **Gujarat** shows the opposite pattern: actual default rate
of 20.9% (highest) but predicted rate of only 23.7% — a relatively
small gap. The model is being more lenient with Gujarat applicants
despite their higher actual default risk.

Six of ten states are flagged under the four-fifths rule, meaning the
approval rate disparity is systemic across the portfolio, not isolated
to one outlier state.

**Root cause:** State dummy features are capturing geographic economic
patterns from training data that may not reflect current credit risk.
The model has learned state-level associations that over-correct for
some geographies (Uttar Pradesh, West Bengal) and under-correct for
others (Gujarat, Rajasthan). This is a classic training data
representativeness failure — the synthetic training data does not
accurately reflect actual state-level credit risk distributions.

**Regulatory implication:** Geographic discrimination in credit access
has implications under RBI's Priority Sector Lending guidelines and
financial inclusion mandates. Systematic under-approval in states like
Uttar Pradesh — which has large MSME populations — could constitute
a breach of fair lending obligations.

---

## 4. Finding 3 — Sector (CRITICAL)

### 4.1 Selection Rate Analysis

| Sector | N | Actual Default Rate | Predicted Default Rate | Approval Rate |
|--------|---|--------------------|-----------------------|---------------|
| Retail Trade | 188 | 19.7% | 29.8% | 70.2% |
| Food Processing | 175 | 13.1% | 29.7% | 70.3% |
| Textile & Apparel | 169 | 20.1% | 27.2% | 72.8% |
| Agriculture Allied | 185 | 13.5% | 25.9% | 74.1% |
| Pharma & Healthcare | 191 | 15.2% | 24.6% | 75.4% |
| IT/ITES Services | 198 | 11.6% | 22.7% | 77.3% |
| Construction Materials | 205 | 13.2% | 20.5% | 79.5% |
| Auto Components | 202 | 18.8% | 20.3% | 79.7% |

### 4.2 Fairness Metrics

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Demographic Parity Difference | +0.0949 | 0.10 | ✓ Within threshold |
| Equalized Odds Difference | +0.2254 | 0.10 | ⚠ BREACH |
| Four-Fifths Rule | 0.6814 ratio | 0.80 | ⚠ BREACH |

### 4.3 Analysis

The most striking finding is **Food Processing**: actual default rate of
13.1% (second lowest) but predicted default rate of 29.7% — a 16.6
percentage point over-prediction. Food Processing applicants with good
credit profiles are being rejected at nearly the same rate as Textile &
Apparel applicants whose actual default rate is 20.1%.

**Auto Components** shows the opposite: actual default rate of 18.8%
but predicted only 20.3% — the model is most lenient with this sector
despite its elevated actual default risk.

The equalized odds difference of 0.225 indicates the model's error
rates differ substantially across sectors — it is not making equally
good or equally bad predictions for all sectors.

**Root cause:** Sector dummy features are acting as proxies for
correlated risk characteristics (business vintage, GST filing patterns,
turnover volatility) that differ by sector in the training data. The model
has learned sector-level stereotypes that do not accurately reflect
individual creditworthiness within each sector.

**Proxy discrimination concern:** In the Indian MSME context, sector
correlates with community and caste in some regions — Textile & Apparel
with specific communities in Gujarat and Tamil Nadu, Agriculture Allied
with rural communities, and so on. Sector-based bias therefore has
potential to constitute indirect caste or community discrimination,
which has constitutional implications under Article 15 and 16.

---

## 5. SHAP Explainability Summary

### 5.1 Global Feature Importance — Top 10

| Rank | Feature | Mean |SHAP| | Protected? |
|------|---------|-------------|------------|
| 1 | bureau_score | 1.1312 | No |
| 2 | dpd_90_count_12m | 0.1875 | No |
| 3 | write_off_flag | 0.1004 | No |
| 4 | gst_turnover_growth_yoy | 0.0810 | No |
| 5 | bounce_count_6m | 0.0718 | No |
| 6 | interest_rate_pct | 0.0702 | No |
| 7 | requested_loan_amount | 0.0662 | No |
| 8 | avg_monthly_debit_turnover | 0.0638 | No |
| 9 | credit_utilization_ratio | 0.0630 | No |
| 10 | cash_deposit_ratio | 0.0617 | No |

**Key finding:** No protected attribute features appear in the top 20.
Bureau score dominates at 1.131 — 6× the next feature. This is consistent
with a model that is primarily a bureau score model with secondary signals
from banking behaviour and GST compliance.

### 5.2 Bureau Score Dependence

Bureau score SHAP correlation: **-0.943** — near-perfect negative
relationship. Higher bureau score produces strongly negative SHAP values
(pushes prediction toward no-default). This confirms the model is using
bureau score correctly as its primary credit signal.

### 5.3 Discrimination Mechanism — Indirect, Not Direct

| Mechanism | Evidence | Conclusion |
|-----------|---------|------------|
| Direct discrimination (gender feature drives decisions) | Gender dummies not in top 20; mean SHAP values < 0.01 | **Ruled out** |
| Proxy discrimination (correlated features act as proxies) | EOD breaches persist despite low direct SHAP; distributional confounding confirmed | **Confirmed** |
| Training data bias (historical patterns encoded in features) | State and sector features encode geographic/sectoral stereotypes | **Confirmed** |

---

## 6. Impossibility Theorem — A Governance Note

It is mathematically impossible to simultaneously satisfy demographic
parity, equalized odds, and individual fairness when base rates differ
across groups (Chouldechova, 2017; Kleinberg et al., 2016).

In this audit, base rates differ meaningfully across groups:
- Female actual default rate: 19.0% vs Male: 14.5%
- Uttar Pradesh actual default rate: 19.9% vs Delhi: 10.1%
- Retail Trade actual default rate: 19.7% vs IT/ITES: 11.6%

This means the Model Risk Committee must make an **explicit policy
decision** about which fairness criterion to prioritise — this cannot
be resolved technically. Options include:

1. **Prioritise equalized odds** — ensure error rates are equal across
   groups, accepting that approval rates will differ
2. **Prioritise demographic parity** — ensure approval rates are equal,
   accepting that error rates will differ
3. **Accept calibration** — ensure predicted probabilities reflect actual
   default rates within each group, accepting both approval rate and
   error rate differences

Each choice has different regulatory, commercial, and ethical implications.
This decision must be documented, approved at Board level, and reviewed
annually.

---

## 7. Regulatory Assessment

| Framework | Requirement | Status |
|-----------|------------|--------|
| RBI Fair Practices Code | Non-discrimination in credit decisions | ⚠ At risk — gender and geographic disparities identified |
| RBI Priority Sector Lending | Financial inclusion — geographic coverage | ⚠ At risk — systematic under-approval in UP, WB, MP |
| DPDP Act 2023 | Automated decision transparency | ⚠ Gap — no right-to-explanation process documented |
| EU AI Act Article 10 | Training data free from discriminatory bias | ⚠ Non-compliant — distributional confounding confirmed |
| Constitution of India Art. 15/16 | Non-discrimination | ⚠ Monitor — sector bias may proxy community discrimination |

---

## 8. Conclusion

All three protected attributes returned CRITICAL severity findings.
The bias mechanism is indirect — driven by distributional confounding
in training data rather than direct use of protected characteristics.
Bureau score correctly dominates model decisions, but sector, state,
and gender correlations in the training data produce systematically
unfair outcomes for Female proprietors, northern-state borrowers,
and Food Processing sector applicants.

Remediation requires a combination of training data re-weighting,
fairness constraints at training time, threshold calibration by group,
and an explicit Board-level policy decision on the fairness criterion
to prioritise. See the Mitigation Roadmap for detailed recommendations.

---

*Audit methodology: Fairlearn 0.10.x, SHAP TreeExplainer, scikit-learn.*
*References: Chouldechova (2017), Mitchell et al. (2019), NIST AI RMF.*
*GRO Shield Independent Governance Assessment, January 2025.*

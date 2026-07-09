# GRO Shield — Independent Data & AI Governance Assessment of UGRO Capital

An independent, external Data & AI governance portfolio project assessing
UGRO Capital, a publicly listed Indian "DataTech NBFC" that uses an AI
credit scoring model called GRO Score 3.0 for MSME lending.

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data only. Not affiliated
> with, endorsed by, or connected to UGRO Capital in any way.
> See `docs/disclaimer.md` for full disclaimer.

---

## Assessment Date

**This assessment was conducted in January 2025** and covers regulatory
frameworks, public disclosures, and technical standards current as of
that date. Specific frameworks referenced include DPDP Act 2023,
DPDP Rules 2025 (draft), NIST AI RMF 1.0 (January 2023), NIST AI 600-1
(July 2024), and EU AI Act. Readers reviewing this assessment after
January 2025 should verify whether referenced regulations or standards
have been updated.

---

## Why UGRO Capital

UGRO Capital publicly describes itself as a DataTech NBFC and discloses
that GRO Score 3.0 uses 25,000+ features from credit bureau, bank
statement, and GST data. Their published privacy policy references the
withdrawn PDP Bill 2021 rather than the enacted DPDP Act 2023 — a real,
citable compliance gap that anchors the Module 3 analysis.

---

## Modules

| Module | Topic | Status |
|--------|-------|--------|
| 01 | Data Quality Assessment | ✅ Complete |
| 02 | Data Catalogue and Lineage | ✅ Complete |
| 03 | DPDP + RBI Compliance | ✅ Complete |
| 04 | Model Risk Management | ✅ Complete |
| 05 | Algorithmic Bias Audit | ✅ Complete |
| 06 | AI Risk Framework | ✅ Complete |
| 07 | GenAI Governance | ✅ Complete |
| 08 | Change Management | 🔄 In Progress |

---

## Key Findings

- **Module 3:** 15 compliance gaps identified (4 critical) — anchor finding
  is UGRO Capital's privacy policy referencing withdrawn PDP Bill 2021
  instead of enacted DPDP Act 2023
- **Module 4:** Proxy XGBoost model trained on 7,563 MSME loan records
  achieves AUC-ROC 0.805; reject inference bias documented in model card
- **Module 5:** All three protected attributes (gender, state, sector)
  return CRITICAL bias findings — state equalized odds difference 0.446,
  gender EOD 0.172; SHAP analysis rules out direct discrimination,
  confirms proxy bias via distributional confounding
- **Module 6:** NIST AI RMF assessment — GOVERN and MANAGE rated maturity
  level 2; 32-risk AI risk register with 12 Critical ratings
- **Module 7:** GenAI guardrail system with PII scanner (Aadhaar/PAN/GSTIN),
  topic boundary enforcement, hallucination detection, and audit logging;
  NIST AI 600-1 assessment across all 12 GenAI risk categories

---

## Tech Stack

Python, Great Expectations, XGBoost, scikit-learn, Fairlearn, SHAP,
FastAPI, Streamlit, Plotly, ReportLab, Faker, pandas

---

## Dataset Note

All analysis uses a synthetic 15,000-row MSME dataset generated with
`seed=42` for reproducibility. The dataset was regenerated as v2 during
Module 4 development — see `01_data_quality/README.md` for details.
No real borrower data is used anywhere in this project.

---

## Reproducing the Analysis

```bash
# Clone and set up
git clone https://github.com/<your-username>/gro-shield-ugro-governance
cd gro-shield-ugro-governance
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Regenerate synthetic dataset
cd 01_data_quality/src && python3 generate_synthetic_data.py && cd ../..
python3 01_data_quality/src/inject_quality_issues.py \
  --in 01_data_quality/data/raw/ugro_msme_clean.csv \
  --out 01_data_quality/data/raw/ugro_msme_dirty.csv \
  --log 01_data_quality/reports/injected_issues_log.csv

# Train model (Module 4)
python3 04_model_risk_management/src/train_model.py

# Run bias audit (Module 5)
python3 05_bias_audit/src/bias_analysis.py
python3 05_bias_audit/src/shap_explainability.py

# Run GenAI guardrail demo (Module 7)
python3 07_genai_governance/guardrails/src/guardrail_system.py

# Launch dashboards
streamlit run 04_model_risk_management/dashboard/monitoring_dashboard.py
streamlit run 07_genai_governance/dashboard/observability_dashboard.py
```

---

*GRO Shield — Independent Data & AI Governance Assessment*
*Assessment date: January 2025*

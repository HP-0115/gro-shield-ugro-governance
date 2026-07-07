"""
build_asset_inventory.py
Builds a structured JSON inventory of all data assets in the
UGRO Capital data ecosystem, based on publicly available information
about GRO Score 3.0's data sources.

Output: catalogue/data_assets.json
"""

import json
from datetime import date


ASSETS = [
    {
        "asset_id": "SRC-001",
        "name": "Loan Origination System (LOS)",
        "description": (
            "The primary system of record for MSME loan applications. "
            "Captures applicant identity, business profile, and loan "
            "request details at the point of application. All loan "
            "journeys begin here."
        ),
        "asset_type": "Source System",
        "owner": "Retail Credit Business Unit",
        "steward": "Core Banking Technology Team",
        "sensitivity": "Restricted",
        "refresh_frequency": "Real-time (event-driven)",
        "downstream_consumers": [
            "Credit Bureau Feed (SRC-002)",
            "Bank Statement Analyzer (SRC-003)",
            "GSTN API Feed (SRC-004)",
            "GRO Score Feature Store (DRV-001)",
        ],
        "known_limitations": [
            "Manual data entry fields (state, sector) subject to "
            "free-text contamination",
            "No real-time PAN format validation at point of entry",
        ],
        "fields": [
            "applicant_id", "application_date", "state", "sector",
            "entity_type", "business_vintage_years", "proprietor_gender",
            "pan_number", "requested_loan_amount", "tenure_months",
        ],
        "regulatory_relevance": [
            "DPDP Act 2023 — personal data of applicant",
            "RBI Digital Lending Guidelines — KYC data",
        ],
    },
    {
        "asset_id": "SRC-002",
        "name": "Credit Bureau Feed (CIBIL/Experian)",
        "description": (
            "Automated pull of credit bureau data for each loan applicant "
            "triggered at application submission. Returns bureau score, "
            "active loan count, delinquency history, and credit utilization "
            "metrics. UGRO Capital publicly discloses bureau data as one of "
            "three primary GRO Score input categories."
        ),
        "asset_type": "Source System",
        "owner": "Credit Risk Team",
        "steward": "Data Engineering Team",
        "sensitivity": "Restricted",
        "refresh_frequency": "Per application (triggered pull)",
        "downstream_consumers": [
            "GRO Score Feature Store (DRV-001)",
        ],
        "known_limitations": [
            "Returns null for new-to-credit applicants with no bureau history",
            "Score reflects position at pull date — stale if pulled >30 days "
            "before underwriting decision",
            "Does not capture informal credit obligations",
        ],
        "fields": [
            "bureau_score", "active_loan_count", "credit_inquiries_6m",
            "total_outstanding_amount", "dpd_30_count_12m",
            "dpd_90_count_12m", "credit_utilization_ratio",
            "oldest_credit_line_age_months", "write_off_flag",
        ],
        "regulatory_relevance": [
            "DPDP Act 2023 — financial personal data",
            "RBI Fair Practices Code — data used in credit decisions",
            "Credit Information Companies Regulation Act 2005",
        ],
    },
    {
        "asset_id": "SRC-003",
        "name": "Bank Statement Analyzer (Account Aggregator)",
        "description": (
            "Processes 12 months of bank statement data obtained via the "
            "RBI Account Aggregator framework or direct statement upload. "
            "Extracts cash flow metrics, balance patterns, and banking "
            "behaviour indicators used as GRO Score inputs. UGRO Capital "
            "publicly discloses bank statement analysis as a core data "
            "category for GRO Score 3.0."
        ),
        "asset_type": "Processed Dataset",
        "owner": "Credit Risk Team",
        "steward": "Data Science Team",
        "sensitivity": "Restricted",
        "refresh_frequency": "Per application",
        "downstream_consumers": [
            "GRO Score Feature Store (DRV-001)",
        ],
        "known_limitations": [
            "PDF parsing failures result in missing values for ~4% of "
            "applications",
            "Does not capture cash transactions outside banking system",
            "Multi-bank applicants require consolidation logic",
        ],
        "fields": [
            "avg_monthly_balance", "avg_monthly_credit_turnover",
            "avg_monthly_debit_turnover", "bounce_count_6m",
            "cash_deposit_ratio", "banking_relationship_count",
        ],
        "regulatory_relevance": [
            "DPDP Act 2023 — financial personal data",
            "RBI Account Aggregator Framework",
            "RBI Digital Lending Guidelines",
        ],
    },
    {
        "asset_id": "SRC-004",
        "name": "GSTN API Feed",
        "description": (
            "Pull of GST filing and turnover data from the Goods and "
            "Services Tax Network (GSTN) API for each applicant business. "
            "Provides verified turnover figures, filing compliance history, "
            "and tax credit utilization metrics. UGRO Capital publicly "
            "discloses GST data as the third primary GRO Score input category, "
            "noting it provides an independent verification of business revenue "
            "that complements bank statement data."
        ),
        "asset_type": "Source System",
        "owner": "Credit Risk Team",
        "steward": "Data Engineering Team",
        "sensitivity": "Confidential",
        "refresh_frequency": "Per application (triggered pull)",
        "downstream_consumers": [
            "GRO Score Feature Store (DRV-001)",
        ],
        "known_limitations": [
            "Only available for GST-registered businesses — excludes "
            "businesses below GST threshold (turnover < ₹20 lakh)",
            "Newly registered businesses may have insufficient filing history",
            "GSTN API occasionally returns stale data for recently "
            "filed returns",
        ],
        "fields": [
            "gst_number", "gst_registration_date",
            "gst_filing_regularity_pct", "monthly_avg_gst_turnover",
            "gst_turnover_growth_yoy", "input_tax_credit_utilization_pct",
        ],
        "regulatory_relevance": [
            "DPDP Act 2023 — business financial data",
            "GST Act 2017 — data sharing provisions",
            "RBI Digital Lending Guidelines",
        ],
    },
]


DERIVED_ASSETS = [
    {
        "asset_id": "DRV-001",
        "name": "GRO Score Feature Store",
        "description": (
            "Derived dataset containing engineered features assembled from "
            "all three primary source categories — credit bureau, bank "
            "statement, and GST data — for input into the GRO Score 3.0 "
            "model. UGRO Capital publicly states this feature store contains "
            "25,000+ features per applicant."
        ),
        "asset_type": "Derived Dataset",
        "owner": "Data Science Team",
        "steward": "Data Science Team",
        "sensitivity": "Restricted",
        "refresh_frequency": "Per application",
        "downstream_consumers": [
            "GRO Score 3.0 Model (MDL-001)",
        ],
        "known_limitations": [
            "Feature definitions not publicly documented",
            "25,000+ features creates high dimensionality risk",
            "Derived features may encode protected attributes indirectly",
        ],
        "fields": [
            "Engineered features from SRC-001, SRC-002, SRC-003, SRC-004"
        ],
        "regulatory_relevance": [
            "RBI Model Risk Guidelines",
            "RBI Fair Practices Code — explainability of credit decisions",
            "EU AI Act — high risk AI system documentation requirements",
        ],
    },
    {
        "asset_id": "MDL-001",
        "name": "GRO Score 3.0 Model Output",
        "description": (
            "Output of the GRO Score 3.0 credit scoring model. Produces "
            "a credit score and loan eligibility decision for each MSME "
            "applicant. UGRO Capital publicly describes this as an "
            "AI/ML model using gradient boosting techniques across "
            "25,000+ features."
        ),
        "asset_type": "Model Output",
        "owner": "Chief Risk Officer",
        "steward": "Data Science Team",
        "sensitivity": "Restricted",
        "refresh_frequency": "Per application",
        "downstream_consumers": [
            "Loan Management System (LMS)",
            "Credit Decision Engine",
        ],
        "known_limitations": [
            "Model explainability limited given feature dimensionality",
            "Potential for indirect discrimination via proxy features",
            "Model drift monitoring cadence not publicly disclosed",
        ],
        "fields": [
            "gro_score", "loan_status", "approved_loan_amount",
            "interest_rate_pct", "tenure_months", "default_flag",
        ],
        "regulatory_relevance": [
            "RBI Digital Lending Guidelines — automated credit decisions",
            "RBI Fair Practices Code — right to explanation",
            "DPDP Act 2023 — automated decision making",
            "EU AI Act — high risk AI system (credit scoring)",
        ],
    },
]


def main():
    all_assets = ASSETS + DERIVED_ASSETS

    output = {
        "catalogue_version": "1.0",
        "assessment_date": str(date.today()),
        "organisation": "UGRO Capital Limited",
        "prepared_by": "GRO Shield Governance Framework",
        "total_assets": len(all_assets),
        "assets": all_assets,
    }

    output_path = "../catalogue/data_assets.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Data asset inventory written -> {output_path}")
    print(f"Total assets documented: {len(all_assets)}")
    print()
    print("Assets:")
    for asset in all_assets:
        print(f"  {asset['asset_id']} | {asset['asset_type']:20s} | {asset['name']}")


if __name__ == "__main__":
    main()

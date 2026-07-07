"""
build_ropa.py
Builds a Records of Processing Activities (RoPA) register for
UGRO Capital's personal data processing activities associated
with GRO Score 3.0.

Aligned to DPDP Act 2023 accountability obligations and
DPDP Rules 2025 documentation requirements.

Output: ropa_register.json and ropa_register.csv
"""

import json
import csv
from datetime import date

ROPA_RECORDS = [
    {
        "record_id": "ROPA-001",
        "processing_activity": "Loan Application Processing",
        "purpose": (
            "Collection and verification of applicant identity and "
            "business information to initiate MSME loan application "
            "and trigger downstream data pulls."
        ),
        "legal_basis": "Consent (DPDP Act 2023, Section 6)",
        "data_categories": [
            "Identity data (PAN, GSTIN)",
            "Business information (sector, entity type, vintage)",
            "Demographic data (gender, state)",
            "Loan request details (amount, tenure)",
        ],
        "data_subjects": "MSME loan applicants",
        "estimated_volume": "~50,000 applications annually",
        "data_sources": ["Applicant self-declaration", "LOS"],
        "recipients": [
            "Credit Bureau (CIBIL/Experian) — for bureau pull",
            "Account Aggregator — for bank statement pull",
            "GSTN API — for GST data pull",
        ],
        "retention_period": "7 years from application date (RBI requirement)",
        "cross_border_transfer": "No",
        "security_measures": [
            "AES-256 encryption at rest",
            "TLS 1.3 in transit",
            "Role-based access controls",
            "MFA for system access",
        ],
        "dpia_required": "Yes — triggers GRO-DPIA-001",
        "data_owner": "Retail Credit Business Unit",
    },
    {
        "record_id": "ROPA-002",
        "processing_activity": "Credit Bureau Data Pull",
        "purpose": (
            "Automated retrieval of applicant credit history from "
            "CIBIL/Experian to assess repayment behaviour and "
            "creditworthiness as input to GRO Score 3.0."
        ),
        "legal_basis": "Consent (DPDP Act 2023, Section 6)",
        "data_categories": [
            "Bureau score (300-900)",
            "Active loan count",
            "DPD history (30-day and 90-day)",
            "Total outstanding amount",
            "Credit utilization ratio",
            "Write-off flag",
            "Credit inquiry history",
        ],
        "data_subjects": "MSME loan applicants",
        "estimated_volume": "~50,000 bureau pulls annually",
        "data_sources": ["CIBIL TransUnion", "Experian India"],
        "recipients": [
            "GRO Score Feature Engineering Pipeline (internal)",
        ],
        "retention_period": "7 years from application date (RBI requirement)",
        "cross_border_transfer": "No — bureau data stays in India",
        "security_measures": [
            "AES-256 encryption at rest",
            "TLS 1.3 in transit",
            "Restricted access — credit risk team only",
            "Pull audit log maintained",
        ],
        "dpia_required": "Yes — covered under GRO-DPIA-001",
        "data_owner": "Credit Risk Team",
    },
    {
        "record_id": "ROPA-003",
        "processing_activity": "Bank Statement Analysis",
        "purpose": (
            "Retrieval and analysis of 12 months of bank statement "
            "data via Account Aggregator framework to assess cash "
            "flow patterns and banking behaviour as GRO Score inputs."
        ),
        "legal_basis": "Consent (DPDP Act 2023, Section 6)",
        "data_categories": [
            "Average monthly balance",
            "Monthly credit and debit turnover",
            "Cheque bounce count",
            "Cash deposit ratio",
            "Banking relationship count",
        ],
        "data_subjects": "MSME loan applicants",
        "estimated_volume": "~50,000 statement pulls annually",
        "data_sources": ["RBI Account Aggregator Framework"],
        "recipients": [
            "GRO Score Feature Engineering Pipeline (internal)",
        ],
        "retention_period": (
            "Duration of loan + 7 years (RBI requirement)"
        ),
        "cross_border_transfer": "No",
        "security_measures": [
            "AES-256 encryption at rest",
            "TLS 1.3 in transit",
            "AA framework consent verification before pull",
            "Restricted access — data science team only",
        ],
        "dpia_required": "Yes — covered under GRO-DPIA-001",
        "data_owner": "Credit Risk Team",
    },
    {
        "record_id": "ROPA-004",
        "processing_activity": "GST Data Pull",
        "purpose": (
            "Retrieval of GST filing history and turnover data from "
            "GSTN API to provide independently verified revenue "
            "figures as GRO Score inputs."
        ),
        "legal_basis": "Consent (DPDP Act 2023, Section 6)",
        "data_categories": [
            "GSTIN",
            "GST registration date",
            "GST filing regularity percentage",
            "Monthly average GST turnover",
            "Year-on-year turnover growth",
            "Input tax credit utilization",
        ],
        "data_subjects": "MSME loan applicants (GST-registered businesses)",
        "estimated_volume": "~45,000 GST pulls annually",
        "data_sources": ["Goods and Services Tax Network (GSTN) API"],
        "recipients": [
            "GRO Score Feature Engineering Pipeline (internal)",
        ],
        "retention_period": "7 years from application date",
        "cross_border_transfer": "No",
        "security_measures": [
            "AES-256 encryption at rest",
            "TLS 1.3 in transit",
            "GSTN API access credentials rotated quarterly",
        ],
        "dpia_required": "Yes — covered under GRO-DPIA-001",
        "data_owner": "Credit Risk Team",
    },
    {
        "record_id": "ROPA-005",
        "processing_activity": "GRO Score Model Training",
        "purpose": (
            "Periodic retraining of GRO Score 3.0 using historical "
            "application data and loan outcomes to maintain model "
            "accuracy and address model drift."
        ),
        "legal_basis": (
            "Legitimate interest — model maintenance for accurate "
            "credit assessment; consent obtained at application "
            "covers primary scoring purpose"
        ),
        "data_categories": [
            "All data categories from ROPA-001 through ROPA-004",
            "Historical loan outcomes (default flag, repayment history)",
        ],
        "data_subjects": "Historical MSME loan applicants",
        "estimated_volume": "Full historical portfolio — ~200,000+ records",
        "data_sources": ["Internal loan management system", "Historical feature store"],
        "recipients": [
            "Data Science Team (internal — model training only)",
        ],
        "retention_period": (
            "Training datasets retained for model audit purposes "
            "— maximum 10 years"
        ),
        "cross_border_transfer": "No",
        "security_measures": [
            "Training data access restricted to data science team",
            "Training environment isolated from production",
            "Pseudonymisation of training data where feasible",
        ],
        "dpia_required": "Yes — covered under GRO-DPIA-001",
        "data_owner": "Data Science Team",
    },
]


def main():
    output = {
        "ropa_version": "1.0",
        "assessment_date": str(date.today()),
        "organisation": "UGRO Capital Limited",
        "prepared_by": "GRO Shield Governance Framework",
        "total_records": len(ROPA_RECORDS),
        "records": ROPA_RECORDS,
    }

    json_path = "ropa_register.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2)

    csv_path = "ropa_register.csv"
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "processing_activity", "purpose",
            "legal_basis", "data_subjects", "estimated_volume",
            "retention_period", "cross_border_transfer",
            "dpia_required", "data_owner",
        ])
        writer.writeheader()
        for record in ROPA_RECORDS:
            writer.writerow({
                "record_id": record["record_id"],
                "processing_activity": record["processing_activity"],
                "purpose": record["purpose"],
                "legal_basis": record["legal_basis"],
                "data_subjects": record["data_subjects"],
                "estimated_volume": record["estimated_volume"],
                "retention_period": record["retention_period"],
                "cross_border_transfer": record["cross_border_transfer"],
                "dpia_required": record["dpia_required"],
                "data_owner": record["data_owner"],
            })

    print(f"RoPA register written -> {json_path}")
    print(f"RoPA CSV written -> {csv_path}")
    print(f"Total processing activities documented: {len(ROPA_RECORDS)}")
    print()
    print("Processing activities:")
    for record in ROPA_RECORDS:
        print(f"  {record['record_id']} | {record['processing_activity']}")


if __name__ == "__main__":
    main()

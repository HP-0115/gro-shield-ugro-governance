"""
schema.py
Defines the controlled vocabulary and structure for the synthetic
MSME loan dataset. This is the single source of truth other scripts
will import from, so values stay consistent across the whole module.
"""

INDIAN_STATES = [
    "Maharashtra", "Gujarat", "Tamil Nadu", "Karnataka", "Rajasthan",
    "Uttar Pradesh", "West Bengal", "Madhya Pradesh", "Delhi", "Punjab",
]

SECTORS = [
    "Textile & Apparel", "Food Processing", "Auto Components",
    "Pharma & Healthcare", "IT/ITES Services", "Retail Trade",
    "Construction Materials", "Agriculture Allied",
]

ENTITY_TYPES = [
    "Proprietorship",
    "Partnership",
    "Private Limited",
    "LLP",
]

GENDERS = ["Male", "Female", "Other"]

# Gender distribution weights (index-aligned with GENDERS list above).
# Source: Ministry of MSME via PIB press release, women-owned MSMEs
# constitute 20.5% of Udyam-registered enterprises (as of Jan 2024).
# "Other" modeled at 1% — no official figure exists; used as a
# floor to avoid completely excluding the category.
GENDER_WEIGHTS = [0.785, 0.205, 0.01]

LOAN_STATUSES = ["Approved", "Rejected", "Disbursed", "Withdrawn"]

# Numeric ranges encode domain knowledge about physically or regulatorily
# possible values. Used by both the data generator (to stay within bounds)
# and the Great Expectations suite (to flag out-of-range values).
NUMERIC_RANGES = {
    "bureau_score": (300, 900),
    "business_vintage_years": (0, 60),
    "credit_utilization_ratio": (0.0, 1.0),
    "gst_filing_regularity_pct": (0.0, 100.0),
    "input_tax_credit_utilization_pct": (0.0, 100.0),
    "interest_rate_pct": (8.0, 36.0),
    "tenure_months": (3, 84),
}

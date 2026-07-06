"""
generate_synthetic_data.py
Generates a clean 15,000-row synthetic MSME loan dataset.
Run this first, then inject_quality_issues.py second.

Usage:
    python generate_synthetic_data.py --rows 15000 --seed 42 --out ../data/raw/ugro_msme_clean.csv
"""

import argparse
import random
import string

import numpy as np
import pandas as pd
from faker import Faker

from schema import (
    INDIAN_STATES, SECTORS, ENTITY_TYPES,
    GENDERS, GENDER_WEIGHTS, LOAN_STATUSES, NUMERIC_RANGES,
)

fake = Faker("en_IN")


# Maps each state name to its official 2-digit GST state code.
STATE_CODES = {
    "Maharashtra": "27", "Gujarat": "24", "Tamil Nadu": "33",
    "Karnataka": "29", "Rajasthan": "08", "Uttar Pradesh": "09",
    "West Bengal": "19", "Madhya Pradesh": "23", "Delhi": "07",
    "Punjab": "03",
}


def make_pan():
    """Returns a synthetic PAN in valid format: AAAAA9999A."""
    letters = "".join(random.choices(string.ascii_uppercase, k=5))
    digits = "".join(random.choices(string.digits, k=4))
    last = random.choice(string.ascii_uppercase)
    return f"{letters}{digits}{last}"


def make_gstin(state, pan):
    """Returns a synthetic GSTIN built on the given state and PAN."""
    state_code = STATE_CODES[state]
    entity_code = random.choice("123456789")
    check_char = random.choice(string.ascii_uppercase + string.digits)
    return f"{state_code}{pan}{entity_code}Z{check_char}"


def generate(n_rows, seed):
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

    rows = []

    for i in range(n_rows):
        # --- Application / KYC fields ---
        state = random.choice(INDIAN_STATES)
        sector = random.choice(SECTORS)
        entity_type = random.choices(
            ENTITY_TYPES, weights=[0.45, 0.20, 0.25, 0.10]
        )[0]
        gender = random.choices(GENDERS, weights=GENDER_WEIGHTS)[0]
        pan = make_pan()
        gstin = make_gstin(state, pan)

        application_date = fake.date_between(
            start_date="-3y", end_date="today"
        )
        gst_registration_date = fake.date_between(
            start_date="-10y", end_date=application_date
        )
        business_vintage_years = round(
            float(np.clip(np.random.exponential(scale=6), 0.5, 50)), 1
        )

        # --- Credit Bureau fields ---
        bureau_score = int(np.clip(
            np.random.normal(loc=670, scale=80), 300, 900
        ))
        active_loan_count = int(np.random.poisson(lam=2))
        credit_inquiries_6m = int(np.random.poisson(lam=1.5))
        total_outstanding_amount = round(
            float(np.clip(np.random.lognormal(mean=12, sigma=1.2), 0, 5000000)), 2
        )
        dpd_30_count_12m = int(np.random.poisson(lam=0.5))
        dpd_90_count_12m = int(np.random.poisson(lam=0.15))
        credit_utilization_ratio = round(
            float(np.clip(np.random.beta(a=2, b=5), 0, 1)), 3
        )
        oldest_credit_line_age_months = int(np.clip(
            np.random.exponential(scale=40), 0, 300
        ))
        write_off_flag = int(np.random.choice([0, 1], p=[0.95, 0.05]))

        # --- Bank Statement fields ---
        avg_monthly_balance = round(
            float(np.clip(np.random.lognormal(mean=10, sigma=1.1), 1000, 10000000)), 2
        )
        avg_monthly_credit_turnover = round(
            float(np.clip(np.random.lognormal(mean=12, sigma=1.0), 5000, 50000000)), 2
        )
        avg_monthly_debit_turnover = round(
            float(avg_monthly_credit_turnover * np.random.uniform(0.7, 0.98)), 2
        )
        bounce_count_6m = int(np.random.poisson(lam=0.8))
        cash_deposit_ratio = round(
            float(np.clip(np.random.beta(a=2, b=6), 0, 1)), 3
        )
        banking_relationship_count = int(np.random.choice(
            [1, 2, 3, 4], p=[0.5, 0.3, 0.15, 0.05]
        ))

        # --- GST fields ---
        gst_filing_regularity_pct = round(
            float(np.clip(np.random.beta(a=6, b=2) * 100, 0, 100)), 1
        )
        monthly_avg_gst_turnover = round(
            float(np.clip(np.random.lognormal(mean=11.5, sigma=1.0), 5000, 50000000)), 2
        )
        gst_turnover_growth_yoy = round(
            float(np.random.normal(loc=8, scale=15)), 2
        )
        input_tax_credit_utilization_pct = round(
            float(np.clip(np.random.beta(a=4, b=3) * 100, 0, 100)), 1
        )

        # --- Loan Outcome fields ---
        requested_loan_amount = round(
            float(np.clip(np.random.lognormal(mean=13, sigma=0.8), 50000, 10000000)), 2
        )
        loan_status = random.choices(
            LOAN_STATUSES, weights=[0.25, 0.20, 0.50, 0.05]
        )[0]
        approved_loan_amount = round(
            float(requested_loan_amount * np.random.uniform(0.6, 1.0)), 2
        ) if loan_status in ("Approved", "Disbursed") else 0.0
        interest_rate_pct = round(
            float(np.clip(np.random.normal(loc=18, scale=4), 8, 36)), 2
        )
        tenure_months = int(random.choices(
            [12, 18, 24, 36, 48, 60],
            weights=[0.10, 0.15, 0.25, 0.30, 0.12, 0.08]
        )[0])

        # default_flag: only meaningful for disbursed loans.
        # Weakly correlated with bureau score and DPD history.
        if loan_status == "Disbursed":
            default_probability = float(np.clip(
                0.25
                - (bureau_score - 600) / 1500
                + dpd_90_count_12m * 0.06,
                0.02, 0.60
            ))
            default_flag = int(np.random.rand() < default_probability)
        else:
            default_flag = 0

        # --- Assemble row ---
        rows.append({
            "applicant_id": f"UGRO-APP-{100000 + i}",
            "application_date": application_date,
            "state": state,
            "sector": sector,
            "entity_type": entity_type,
            "business_vintage_years": business_vintage_years,
            "proprietor_gender": gender,
            "pan_number": pan,
            "gstin": gstin,
            "gst_registration_date": gst_registration_date,
            "bureau_score": bureau_score,
            "active_loan_count": active_loan_count,
            "credit_inquiries_6m": credit_inquiries_6m,
            "total_outstanding_amount": total_outstanding_amount,
            "dpd_30_count_12m": dpd_30_count_12m,
            "dpd_90_count_12m": dpd_90_count_12m,
            "credit_utilization_ratio": credit_utilization_ratio,
            "oldest_credit_line_age_months": oldest_credit_line_age_months,
            "write_off_flag": write_off_flag,
            "avg_monthly_balance": avg_monthly_balance,
            "avg_monthly_credit_turnover": avg_monthly_credit_turnover,
            "avg_monthly_debit_turnover": avg_monthly_debit_turnover,
            "bounce_count_6m": bounce_count_6m,
            "cash_deposit_ratio": cash_deposit_ratio,
            "banking_relationship_count": banking_relationship_count,
            "gst_filing_regularity_pct": gst_filing_regularity_pct,
            "monthly_avg_gst_turnover": monthly_avg_gst_turnover,
            "gst_turnover_growth_yoy": gst_turnover_growth_yoy,
            "input_tax_credit_utilization_pct": input_tax_credit_utilization_pct,
            "requested_loan_amount": requested_loan_amount,
            "approved_loan_amount": approved_loan_amount,
            "interest_rate_pct": interest_rate_pct,
            "tenure_months": tenure_months,
            "loan_status": loan_status,
            "default_flag": default_flag,
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic MSME loan dataset"
    )
    parser.add_argument("--rows", type=int, default=15000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default="../data/raw/ugro_msme_clean.csv")
    args = parser.parse_args()

    print(f"Generating {args.rows:,} rows with seed {args.seed}...")
    df = generate(args.rows, args.seed)

    df.to_csv(args.out, index=False)
    print(f"Done. Written to {args.out}")
    print(f"Shape: {df.shape}")
    print(f"\nColumn names:\n{list(df.columns)}")
    print(f"\nNull counts (should all be 0):\n{df.isnull().sum()}")

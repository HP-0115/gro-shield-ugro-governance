"""
inject_quality_issues.py
Takes the clean dataset and deliberately injects data quality issues
across all 6 DQ dimensions. Logs every single change to a ground truth
file so we can later measure how well Great Expectations catches them.

Usage:
    python inject_quality_issues.py \
        --in ../data/raw/ugro_msme_clean.csv \
        --out ../data/raw/ugro_msme_dirty.csv \
        --log ../../reports/injected_issues_log.csv \
        --seed 42
"""

import argparse
import random
import string

import numpy as np
import pandas as pd

from schema import INDIAN_STATES, SECTORS, LOAN_STATUSES

ISSUE_LOG = []


def log_issue(df, idx, column, dimension, issue_type, original, injected):
    ISSUE_LOG.append({
        "row_index": idx,
        "applicant_id": df.at[idx, "applicant_id"],
        "column": column,
        "dq_dimension": dimension,
        "issue_type": issue_type,
        "original_value": original,
        "injected_value": injected,
    })


def inject_completeness_issues(df, rng):
    # Bureau score missing ~2% of rows (new-to-credit applicants)
    n = int(len(df) * 0.02)
    idxs = rng.choice(df.index, size=n, replace=False)
    for idx in idxs:
        original = df.at[idx, "bureau_score"]
        df.at[idx, "bureau_score"] = np.nan
        log_issue(df, idx, "bureau_score", "Completeness",
                  "missing_value", original, np.nan)

    # Bank statement fields missing ~4% of rows (upload failure)
    n = int(len(df) * 0.04)
    idxs = rng.choice(df.index, size=n, replace=False)
    for idx in idxs:
        col = rng.choice(["avg_monthly_balance",
                          "avg_monthly_credit_turnover",
                          "bounce_count_6m"])
        original = df.at[idx, col]
        df.at[idx, col] = np.nan
        log_issue(df, idx, col, "Completeness",
                  "missing_value", original, np.nan)

    # GST fields missing ~3% of rows (new registration, not yet synced)
    n = int(len(df) * 0.03)
    idxs = rng.choice(df.index, size=n, replace=False)
    for idx in idxs:
        col = rng.choice(["gst_filing_regularity_pct",
                          "monthly_avg_gst_turnover"])
        original = df.at[idx, col]
        df.at[idx, col] = np.nan
        log_issue(df, idx, col, "Completeness",
                  "missing_value", original, np.nan)

    return df


def inject_accuracy_issues(df, rng):
    # Bureau score outside valid range 300-900 (system integration bug)
    n = int(len(df) * 0.008)
    idxs = rng.choice(df.index, size=n, replace=False)
    for idx in idxs:
        original = df.at[idx, "bureau_score"]
        injected = float(rng.choice([0, 950, 999, -1]))
        df.at[idx, "bureau_score"] = injected
        log_issue(df, idx, "bureau_score", "Accuracy",
                  "out_of_range_value", original, injected)

    # Negative loan amounts (sign-flip bug in ETL pipeline)
    n = int(len(df) * 0.006)
    idxs = rng.choice(df.index, size=n, replace=False)
    for idx in idxs:
        original = df.at[idx, "requested_loan_amount"]
        injected = -abs(original)
        df.at[idx, "requested_loan_amount"] = injected
        log_issue(df, idx, "requested_loan_amount", "Accuracy",
                  "negative_value", original, injected)

    # Interest rate decimal shift (1800 instead of 18.00)
    n = int(len(df) * 0.005)
    idxs = rng.choice(df.index, size=n, replace=False)
    for idx in idxs:
        original = df.at[idx, "interest_rate_pct"]
        injected = round(original * 100, 2)
        df.at[idx, "interest_rate_pct"] = injected
        log_issue(df, idx, "interest_rate_pct", "Accuracy",
                  "decimal_shift_error", original, injected)

    # GST filing regularity exceeding 100%
    n = int(len(df) * 0.005)
    idxs = rng.choice(df.index, size=n, replace=False)
    for idx in idxs:
        original = df.at[idx, "gst_filing_regularity_pct"]
        injected = round(float(rng.uniform(101, 250)), 1)
        df.at[idx, "gst_filing_regularity_pct"] = injected
        log_issue(df, idx, "gst_filing_regularity_pct", "Accuracy",
                  "percentage_over_100", original, injected)

    return df



def inject_consistency_issues(df, rng):

    # approved_loan_amount > requested_loan_amount (should never happen)

    n = int(len(df) * 0.006)

    idxs = rng.choice(df.index, size=n, replace=False)

    for idx in idxs:

        original = df.at[idx, "approved_loan_amount"]

        injected = round(float(df.at[idx, "requested_loan_amount"] * rng.uniform(1.1, 1.5)), 2)

        df.at[idx, "approved_loan_amount"] = injected

        log_issue(df, idx, "approved_loan_amount", "Consistency",

                  "approved_exceeds_requested", original, injected)

    # loan_status Rejected but approved_loan_amount > 0

    rejected_idx = df[df["loan_status"] == "Rejected"].index

    n = min(int(len(df) * 0.005), len(rejected_idx))

    idxs = rng.choice(rejected_idx, size=n, replace=False)

    for idx in idxs:

        original = df.at[idx, "approved_loan_amount"]

        injected = round(float(rng.uniform(50000, 500000)), 2)

        df.at[idx, "approved_loan_amount"] = injected

        log_issue(df, idx, "approved_loan_amount", "Consistency",

                  "rejected_with_approved_amount", original, injected)

    # gst_registration_date after application_date

    n = int(len(df) * 0.004)

    idxs = rng.choice(df.index, size=n, replace=False)

    for idx in idxs:

        app_date = pd.to_datetime(df.at[idx, "application_date"])

        original = df.at[idx, "gst_registration_date"]

        injected = (app_date + pd.Timedelta(days=int(rng.integers(5, 200)))).strftime("%Y-%m-%d")

        df.at[idx, "gst_registration_date"] = injected

        log_issue(df, idx, "gst_registration_date", "Consistency",

                  "registration_after_application", original, injected)

    return df

def inject_timeliness_issues(df, rng):

    # Bureau data pulled more than 90 days before application (stale)

    n = int(len(df) * 0.012)

    idxs = rng.choice(df.index, size=n, replace=False)

    for idx in idxs:

        app_date = pd.to_datetime(df.at[idx, "application_date"])

        original = df.at[idx, "application_date"]

        injected = (app_date - pd.Timedelta(days=int(rng.integers(91, 400)))).strftime("%Y-%m-%d")

        df.at[idx, "application_date"] = injected

        log_issue(df, idx, "application_date", "Timeliness",

                  "stale_bureau_pull", original, injected)

    return df

def inject_validity_issues(df, rng):

    # Malformed PAN (wrong length)

    n = int(len(df) * 0.006)

    idxs = rng.choice(df.index, size=n, replace=False)

    for idx in idxs:

        original = df.at[idx, "pan_number"]

        injected = original[:7]

        df.at[idx, "pan_number"] = injected

        log_issue(df, idx, "pan_number", "Validity",

                  "malformed_pan", original, injected)

    # State value outside controlled vocabulary

    n = int(len(df) * 0.004)

    idxs = rng.choice(df.index, size=n, replace=False)

    bad_states = ["MH", "TamilNadu", "delhi ncr", "N/A", "Unknown"]

    for idx in idxs:

        original = df.at[idx, "state"]

        injected = rng.choice(bad_states)

        df.at[idx, "state"] = injected

        log_issue(df, idx, "state", "Validity",

                  "invalid_categorical_value", original, injected)

    # Loan status outside controlled vocabulary

    n = int(len(df) * 0.003)

    idxs = rng.choice(df.index, size=n, replace=False)

    bad_statuses = ["Pending", "Under Review", "NA", "1", "approved"]

    for idx in idxs:

        original = df.at[idx, "loan_status"]

        injected = rng.choice(bad_statuses)

        df.at[idx, "loan_status"] = injected

        log_issue(df, idx, "loan_status", "Validity",

                  "invalid_categorical_value", original, injected)

    return df

def inject_uniqueness_issues(df, rng):

    # Duplicate applicant_id (primary key collision)

    n = int(len(df) * 0.004)

    source_idxs = rng.choice(df.index, size=n, replace=False)

    target_idxs = rng.choice(df.index, size=n, replace=False)

    for src, tgt in zip(source_idxs, target_idxs):

        if src == tgt:

            continue

        original = df.at[tgt, "applicant_id"]

        injected = df.at[src, "applicant_id"]

        df.at[tgt, "applicant_id"] = injected

        log_issue(df, tgt, "applicant_id", "Uniqueness",

                  "duplicate_primary_key", original, injected)

    return df





def main():
    parser = argparse.ArgumentParser(
        description="Inject data quality issues into clean dataset"
    )
    parser.add_argument("--in", dest="infile",
                        default="../data/raw/ugro_msme_clean.csv")
    parser.add_argument("--out", dest="outfile",
                        default="../data/raw/ugro_msme_dirty.csv")
    parser.add_argument("--log", dest="logfile",
                        default="../../reports/injected_issues_log.csv")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    rng = np.random.default_rng(args.seed)
    random.seed(args.seed)

    print(f"Loading clean dataset from {args.infile}...")
    df = pd.read_csv(args.infile)
    original_rows = len(df)

    print("Injecting issues...")
    df = inject_completeness_issues(df, rng)
    df = inject_accuracy_issues(df, rng)
    df = inject_consistency_issues(df, rng)
    df = inject_timeliness_issues(df, rng)
    df = inject_validity_issues(df, rng)
    df = inject_uniqueness_issues(df, rng)

    df.to_csv(args.outfile, index=False)

    log_df = pd.DataFrame(ISSUE_LOG)
    log_df.to_csv(args.logfile, index=False)

    print(f"\nDirty dataset written -> {args.outfile}")
    print(f"Ground truth log written -> {args.logfile}")
    print(f"\nTotal issues injected: {len(log_df)}")
    print(f"\nBreakdown by dimension:")
    print(log_df["dq_dimension"].value_counts())
    print(f"\nBreakdown by issue type:")
    print(log_df["issue_type"].value_counts())


if __name__ == "__main__":
    main()

"""
dq_scorecard.py
Reads the ground truth issue log and GE validation results to produce
a per-dimension DQ scorecard.

Usage:
    python dq_scorecard.py \
        --log ../../reports/injected_issues_log.csv \
        --results ../../reports/validation_results.json \
        --out ../../reports/dq_scorecard.csv
"""

import argparse
import json

import pandas as pd

DIMENSION_EXPECTATION_MAP = {
    "Completeness": ["expect_column_values_to_not_be_null"],
    "Accuracy": ["expect_column_values_to_be_between"],
    "Validity": [
        "expect_column_values_to_be_in_set",
        "expect_column_values_to_match_regex",
    ],
    "Uniqueness": ["expect_column_values_to_be_unique"],
    "Consistency": ["expect_column_pair_values_a_to_be_greater_than_b"],
    "Timeliness": ["expect_column_values_to_be_between"],
}

TOTAL_ROWS = 15000


def calculate_scorecard(log_path, results_path):
    log = pd.read_csv(log_path)
    with open(results_path) as f:
        results = json.load(f)

    # Build a set of failed expectation types from GE results
    failed_expectations = set(
        r["expectation_type"] for r in results if not r["success"]
    )

    rows = []
    for dimension in [
        "Completeness", "Accuracy", "Validity",
        "Uniqueness", "Consistency", "Timeliness"
    ]:
        # Count issues injected for this dimension
        dim_issues = log[log["dq_dimension"] == dimension]
        issue_count = len(dim_issues)

        # Violation rate: unique rows affected / total rows
        rows_affected = dim_issues["row_index"].nunique()
        violation_rate = rows_affected / TOTAL_ROWS

        # Dimension score: 0-100
        score = round((1 - violation_rate) * 100, 1)

        # GE status: did any expectation for this dimension fail?
        expected_types = DIMENSION_EXPECTATION_MAP[dimension]
        ge_flagged = any(
            exp_type in failed_expectations
            for exp_type in expected_types
        )
        ge_status = "FLAGGED" if ge_flagged else "PASSED"

        rows.append({
            "dimension": dimension,
            "issues_injected": issue_count,
            "rows_affected": rows_affected,
            "violation_rate_pct": round(violation_rate * 100, 2),
            "dimension_score": score,
            "ge_status": ge_status,
        })

    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Generate DQ scorecard from validation results"
    )
    parser.add_argument("--log", type=str,
                        default="../../reports/injected_issues_log.csv")
    parser.add_argument("--results", type=str,
                        default="../../reports/validation_results.json")
    parser.add_argument("--out", type=str,
                        default="../../reports/dq_scorecard.csv")
    args = parser.parse_args()

    print("Calculating scorecard...")
    scorecard = calculate_scorecard(args.log, args.results)

    print("\n--- DQ SCORECARD ---")
    print(scorecard.to_string(index=False))

    overall = round(scorecard["dimension_score"].mean(), 1)
    print(f"\nOverall DQ Score: {overall} / 100")

    scorecard.to_csv(args.out, index=False)
    print(f"\nScorecard saved to {args.out}")


if __name__ == "__main__":
    main()

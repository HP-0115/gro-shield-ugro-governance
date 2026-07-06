"""
run_validation.py
Runs the Great Expectations validation suite against the dirty dataset
and saves results to a JSON file for the scorecard script to read.

Usage:
    python run_validation.py \
        --data ../data/raw/ugro_msme_dirty.csv \
        --out ../../reports/validation_results.json
"""

import argparse
import json

import pandas as pd
import great_expectations as gx


def build_datasource(context, df):
    datasource = context.data_sources.add_pandas(name="msme_datasource")
    asset = datasource.add_dataframe_asset(name="msme_loan_data")
    batch_definition = asset.add_batch_definition_whole_dataframe(
        name="full_batch"
    )
    return batch_definition



def build_expectation_suite(context):
    suite = gx.ExpectationSuite(name="msme_dq_suite")

    # --- COMPLETENESS ---
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
        column="bureau_score", mostly=0.99
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
        column="avg_monthly_balance", mostly=0.99
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
        column="avg_monthly_credit_turnover", mostly=0.99
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToNotBeNull(
        column="gst_filing_regularity_pct", mostly=0.99
    ))

    # --- ACCURACY ---
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
        column="bureau_score", min_value=300, max_value=900, mostly=0.995
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
        column="interest_rate_pct", min_value=8, max_value=36, mostly=0.995
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
        column="gst_filing_regularity_pct", min_value=0, max_value=100,
        mostly=0.995
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
        column="requested_loan_amount", min_value=0, max_value=None,
        mostly=0.995
    ))

    # --- VALIDITY ---
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
        column="state",
        value_set=[
            "Maharashtra", "Gujarat", "Tamil Nadu", "Karnataka",
            "Rajasthan", "Uttar Pradesh", "West Bengal",
            "Madhya Pradesh", "Delhi", "Punjab"
        ],
        mostly=0.995
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeInSet(
        column="loan_status",
        value_set=["Approved", "Rejected", "Disbursed", "Withdrawn"],
        mostly=0.997
    ))
    suite.add_expectation(gx.expectations.ExpectColumnValuesToMatchRegex(
        column="pan_number", regex=r"^[A-Z]{5}[0-9]{4}[A-Z]$", mostly=0.995
    ))

    # --- UNIQUENESS ---
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeUnique(
        column="applicant_id"
    ))

    # --- CONSISTENCY ---
    suite.add_expectation(gx.expectations.ExpectColumnPairValuesAToBeGreaterThanB(
        column_A="requested_loan_amount",
        column_B="approved_loan_amount",
        or_equal=True
    ))

    # --- TIMELINESS ---
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
        column="application_date",
        min_value="2022-01-01",
        max_value="2026-12-31",
        mostly=0.99
    ))

    # --- CONSISTENCY (date) ---
    suite.add_expectation(gx.expectations.ExpectColumnValuesToBeBetween(
        column="gst_registration_date",
        min_value="2005-01-01",
        max_value="2026-12-31",
        mostly=0.99
    ))
    
    return suite



def main():
    parser = argparse.ArgumentParser(
        description="Run Great Expectations validation suite"
    )
    parser.add_argument("--data", type=str,
                        default="../data/raw/ugro_msme_dirty.csv")
    parser.add_argument("--out", type=str,
                        default="../../reports/validation_results.json")
    args = parser.parse_args()

    print(f"Loading data from {args.data}...")
    df = pd.read_csv(args.data)
    print(f"Loaded {len(df):,} rows")

    print("Building context and datasource...")
    context = gx.get_context(mode="ephemeral")
    batch_definition = build_datasource(context, df)

    print("Building expectation suite...")
    suite = build_expectation_suite(context)
    context.suites.add(suite)

    print("Running validation...")
    batch_parameters = {"dataframe": df}
    validation_definition = gx.ValidationDefinition(
        name="msme_dq_validation",
        data=batch_definition,
        suite=suite,
    )
    context.validation_definitions.add(validation_definition)
    results = validation_definition.run(
        batch_parameters=batch_parameters
    )

    print("\n--- VALIDATION RESULTS ---")
    passed = 0
    failed = 0
    output = []
    for result in results.results:
        status = "PASS" if result.success else "FAIL"
        expectation_type = result.expectation_config.type
        column = result.expectation_config.kwargs.get("column", "N/A")
        if result.success:
            passed += 1
        else:
            failed += 1
        print(f"  {status} | {expectation_type} | {column}")
        output.append({
            "expectation_type": expectation_type,
            "column": column,
            "success": result.success,
            "result": str(result.result),
        })

    print(f"\nTotal: {passed} passed, {failed} failed")

    with open(args.out, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {args.out}")


if __name__ == "__main__":
    main()

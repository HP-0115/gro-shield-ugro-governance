"""
Module 5: Algorithmic Bias Audit
bias_analysis.py — Fairness analysis across protected attributes.

Analyses the GRO Score proxy model for demographic parity,
equalized odds, and selection rate disparities across:
  - proprietor_gender
  - state
  - sector

References:
  - Fairlearn: https://fairlearn.org
  - RBI Fair Practices Code (non-discrimination in lending)
  - EU AI Act Article 10 (bias in training data)
  - Chouldechova (2017) impossibility theorem
"""

import pandas as pd
import numpy as np
import json
import os
from fairlearn.metrics import (
    MetricFrame,
    demographic_parity_difference,
    demographic_parity_ratio,
    equalized_odds_difference,
    false_positive_rate,
    false_negative_rate,
    selection_rate
)
from sklearn.metrics import accuracy_score, precision_score, recall_score

# ── Constants ─────────────────────────────────────────────────────────────────
TEST_DATA_PATH  = "04_model_risk_management/data/test_set_with_predictions.csv"
REPORTS_DIR     = "05_bias_audit/reports"
DECISION_THRESHOLD = 0.5

PROTECTED_ATTRIBUTES = ["proprietor_gender", "state", "sector"]

# Fairness thresholds — industry and regulatory guidance
# Demographic parity difference > 0.10 = meaningful disparity
# Equalized odds difference > 0.10 = meaningful disparity
# Selection rate ratio < 0.80 = "four-fifths rule" (US EEOC, widely adopted)
DPD_THRESHOLD  = 0.10   # demographic parity difference
EOD_THRESHOLD  = 0.10   # equalized odds difference
SRR_THRESHOLD  = 0.80   # selection rate ratio (four-fifths rule)


# ── Data loading ──────────────────────────────────────────────────────────────
def load_test_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"Test set loaded: {df.shape}")
    print(f"Columns: {list(df.columns)}\n")
    return df


def apply_threshold(predicted_proba: pd.Series,
                    threshold: float = DECISION_THRESHOLD) -> pd.Series:
    """
    Convert predicted probabilities to binary decisions.
    1 = predicted default (reject loan)
    0 = predicted no default (approve loan)
    """
    return (predicted_proba >= threshold).astype(int)


# ── Selection rate analysis ───────────────────────────────────────────────────
def compute_selection_rates(df: pd.DataFrame,
                            y_pred: pd.Series,
                            attribute: str) -> pd.DataFrame:
    """
    Compute approval rate (selection rate for no-default prediction)
    and default prediction rate by group.

    In credit scoring:
      - selection_rate = proportion predicted as DEFAULT (flagged)
      - approval_rate  = 1 - selection_rate
    """
    temp = df[[attribute, "default_flag"]].copy()
    temp["y_pred"] = y_pred.values
    temp["predicted_proba"] = df["predicted_proba"].values

    group_stats = temp.groupby(attribute).agg(
        n=("default_flag", "count"),
        actual_default_rate=("default_flag", "mean"),
        predicted_default_rate=("y_pred", "mean"),
        avg_predicted_proba=("predicted_proba", "mean")
    ).round(4).reset_index()

    group_stats["approval_rate"] = (
        1 - group_stats["predicted_default_rate"]
    ).round(4)

    group_stats = group_stats.sort_values(
        "predicted_default_rate", ascending=False
    ).reset_index(drop=True)

    return group_stats


# ── Fairlearn metric computation ──────────────────────────────────────────────
def compute_fairness_metrics(df: pd.DataFrame,
                             y_true: pd.Series,
                             y_pred: pd.Series,
                             attribute: str) -> dict:
    """
    Compute Fairlearn fairness metrics for a single protected attribute.

    Returns dict with:
      - demographic_parity_difference
      - demographic_parity_ratio
      - equalized_odds_difference
      - per-group MetricFrame summary
    """
    sensitive = df[attribute]

    # Core fairness metrics
    dpd = demographic_parity_difference(
        y_true, y_pred, sensitive_features=sensitive
    )
    dpr = demographic_parity_ratio(
        y_true, y_pred, sensitive_features=sensitive
    )
    eod = equalized_odds_difference(
        y_true, y_pred, sensitive_features=sensitive
    )

    # Per-group breakdown using MetricFrame
    mf = MetricFrame(
        metrics={
            "accuracy":       accuracy_score,
            "precision":      precision_score,
            "recall":         recall_score,
            "selection_rate": selection_rate,
            "fpr":            false_positive_rate,
            "fnr":            false_negative_rate,
        },
        y_true=y_true,
        y_pred=y_pred,
        sensitive_features=sensitive
    )

    # Flag which groups breach thresholds
    sr_by_group = mf.by_group["selection_rate"]
    max_sr = sr_by_group.max()
    flagged_groups = sr_by_group[
        sr_by_group < max_sr * SRR_THRESHOLD
    ].index.tolist()

    result = {
        "attribute": attribute,
        "demographic_parity_difference": round(float(dpd), 4),
        "demographic_parity_ratio":      round(float(dpr), 4),
        "equalized_odds_difference":     round(float(eod), 4),
        "dpd_breach":  abs(dpd) > DPD_THRESHOLD,
        "eod_breach":  abs(eod) > EOD_THRESHOLD,
        "four_fifths_breach": len(flagged_groups) > 0,
        "flagged_groups": flagged_groups,
        "by_group": mf.by_group.round(4).to_dict()
    }

    return result


# ── Severity classification ───────────────────────────────────────────────────
def classify_severity(metrics: dict) -> str:
    """
    Classify finding severity based on number and type of threshold breaches.
    Critical: 2+ breaches or demographic parity difference > 0.15
    High:     1 breach
    Medium:   near-breach (within 20% of threshold)
    Low:      no breach
    """
    breaches = sum([
        metrics["dpd_breach"],
        metrics["eod_breach"],
        metrics["four_fifths_breach"]
    ])
    dpd = abs(metrics["demographic_parity_difference"])

    if breaches >= 2 or dpd > 0.15:
        return "CRITICAL"
    elif breaches == 1:
        return "HIGH"
    elif dpd > DPD_THRESHOLD * 0.8:
        return "MEDIUM"
    else:
        return "LOW"


# ── Main analysis ─────────────────────────────────────────────────────────────
def run_bias_analysis():
    os.makedirs(REPORTS_DIR, exist_ok=True)

    # Load data
    df = load_test_data(TEST_DATA_PATH)
    y_true = df["default_flag"].astype(int)
    y_pred = apply_threshold(df["predicted_proba"])

    print(f"Decision threshold: {DECISION_THRESHOLD}")
    print(f"Predicted default rate (overall): {y_pred.mean():.4f}")
    print(f"Actual default rate (overall):    {y_true.mean():.4f}\n")

    all_results = {}
    all_selection_rates = {}

    for attr in PROTECTED_ATTRIBUTES:
        if attr not in df.columns:
            print(f"WARNING: {attr} not found in test data — skipping")
            continue

        print(f"{'='*55}")
        print(f"PROTECTED ATTRIBUTE: {attr.upper()}")
        print(f"{'='*55}")

        # Selection rates
        sr_df = compute_selection_rates(df, y_pred, attr)
        all_selection_rates[attr] = sr_df
        print(f"\nSelection rates by {attr}:\n{sr_df.to_string(index=False)}")

        # Fairness metrics
        metrics = compute_fairness_metrics(df, y_true, y_pred, attr)
        severity = classify_severity(metrics)
        metrics["severity"] = severity

        print(f"\nFairness Metrics:")
        print(f"  Demographic Parity Difference : {metrics['demographic_parity_difference']:+.4f}  {'⚠ BREACH' if metrics['dpd_breach'] else '✓ OK'}")
        print(f"  Demographic Parity Ratio      : {metrics['demographic_parity_ratio']:.4f}  {'⚠ BREACH' if metrics['four_fifths_breach'] else '✓ OK'} (four-fifths rule)")
        print(f"  Equalized Odds Difference     : {metrics['equalized_odds_difference']:+.4f}  {'⚠ BREACH' if metrics['eod_breach'] else '✓ OK'}")
        print(f"  Flagged groups                : {metrics['flagged_groups']}")
        print(f"  Severity                      : {severity}\n")

        all_results[attr] = metrics

    # Save results
    results_path = os.path.join(REPORTS_DIR, "bias_analysis_results.json")
    # Convert any non-serialisable types
    serialisable = {}
    for attr, m in all_results.items():
        serialisable[attr] = {
            k: v for k, v in m.items() if k != "by_group"
        }
        serialisable[attr]["by_group_summary"] = {
            group: {metric: round(float(val), 4)
                    for metric, val in vals.items()}
            for group, vals in m["by_group"].items()
        }

    with open(results_path, "w") as f:
        json.dump(serialisable, f, indent=2, default=lambda x: bool(x) if hasattr(x, "item") else str(x))
    print(f"\nBias analysis results saved: {results_path}")

    # Save selection rate CSVs
    for attr, sr_df in all_selection_rates.items():
        sr_path = os.path.join(REPORTS_DIR, f"selection_rates_{attr}.csv")
        sr_df.to_csv(sr_path, index=False)
        print(f"Selection rates saved: {sr_path}")

    return all_results, all_selection_rates


if __name__ == "__main__":
    results, selection_rates = run_bias_analysis()
    print("\nBias analysis complete.")

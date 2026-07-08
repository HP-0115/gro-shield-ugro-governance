"""
Module 4: Model Risk Management
psi_monitor.py — Population Stability Index (PSI) calculation engine.

PSI measures distributional drift between a reference (training) dataset
and a current (production) dataset for each model feature.

Interpretation thresholds (industry standard):
  PSI < 0.10  : No significant change — model stable
  PSI < 0.20  : Moderate change — monitor closely
  PSI >= 0.20 : Significant change — model review required
"""

import pandas as pd
import numpy as np
from typing import Optional


PSI_WARNING  = 0.10
PSI_CRITICAL = 0.20
N_BINS       = 10  # standard for PSI calculation


def _psi_single_feature(
    expected: pd.Series,
    actual: pd.Series,
    bins: int = N_BINS,
    epsilon: float = 1e-6
) -> float:
    """
    Compute PSI for a single numeric feature.

    epsilon prevents log(0) when a bin is empty in one distribution.
    Both series are binned using the same edges (derived from expected),
    so drift in the actual distribution is measured against the training
    baseline — not against itself.
    """
    # Derive bin edges from the expected (training) distribution
    breakpoints = np.linspace(
        expected.min() - epsilon,
        expected.max() + epsilon,
        bins + 1
    )

    # Bin both distributions using the same edges
    expected_counts = pd.cut(expected, bins=breakpoints).value_counts(sort=False)
    actual_counts   = pd.cut(actual,   bins=breakpoints).value_counts(sort=False)

    # Convert to proportions, add epsilon to avoid division by zero
    expected_pct = (expected_counts / len(expected)) + epsilon
    actual_pct   = (actual_counts   / len(actual))   + epsilon

    # PSI formula: Σ (actual - expected) * ln(actual / expected)
    psi_value = np.sum(
        (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
    )
    return float(psi_value)


def compute_psi_report(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    feature_cols: Optional[list] = None,
    bins: int = N_BINS
) -> pd.DataFrame:
    """
    Compute PSI for all numeric features between reference and current datasets.

    Args:
        reference_df : training / baseline dataset (expected distribution)
        current_df   : production / current dataset (actual distribution)
        feature_cols : list of columns to evaluate; defaults to all numeric cols
        bins         : number of bins for PSI calculation

    Returns:
        DataFrame with columns: feature, psi, status, interpretation
    """
    if feature_cols is None:
        feature_cols = reference_df.select_dtypes(include=[np.number]).columns.tolist()
        # Exclude target and prediction columns from drift analysis
        feature_cols = [c for c in feature_cols
                        if c not in ["default_flag", "predicted_proba"]]

    results = []
    for col in feature_cols:
        if col not in current_df.columns:
            continue
        if reference_df[col].nunique() < 2:
            continue  # skip constant columns

        psi_val = _psi_single_feature(
            reference_df[col].dropna(),
            current_df[col].dropna(),
            bins=bins
        )

        if psi_val < PSI_WARNING:
            status = "STABLE"
            interpretation = "No significant change"
        elif psi_val < PSI_CRITICAL:
            status = "WARNING"
            interpretation = "Moderate drift — monitor closely"
        else:
            status = "CRITICAL"
            interpretation = "Significant drift — model review required"

        results.append({
            "feature": col,
            "psi": round(psi_val, 4),
            "status": status,
            "interpretation": interpretation
        })

    report = pd.DataFrame(results).sort_values("psi", ascending=False)
    return report.reset_index(drop=True)


def simulate_production_drift(
    reference_df: pd.DataFrame,
    drift_strength: float = 0.3,
    seed: int = 42
) -> pd.DataFrame:
    """
    Simulate a production dataset with realistic drift for dashboard demo.

    In a real deployment, this would be replaced by actual production data.
    Here we inject controlled drift into key features to produce a meaningful
    PSI dashboard — standard practice for demonstrating monitoring infrastructure
    without live production traffic.

    drift_strength controls how much shift is applied:
      0.0 = no drift (PSI ~ 0 everywhere)
      0.3 = moderate drift on selected features (some WARNING, few CRITICAL)
      1.0 = severe drift across all features
    """
    rng = np.random.default_rng(seed)
    production_df = reference_df.copy()

    numeric_cols = reference_df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols
                    if c not in ["default_flag", "predicted_proba"]]

    # Apply drift to a realistic subset of features
    # Bureau score: slight deterioration in production (economic stress scenario)
    if "bureau_score" in production_df.columns:
        shift = drift_strength * 25
        production_df["bureau_score"] = np.clip(
            production_df["bureau_score"] - shift
            + rng.normal(0, 10, len(production_df)),
            300, 900
        ).astype(int)

    # DPD 90 count: increase (more stress in production)
    if "dpd_90_count_12m" in production_df.columns:
        production_df["dpd_90_count_12m"] = np.clip(
            production_df["dpd_90_count_12m"]
            + rng.poisson(drift_strength * 0.8, len(production_df)),
            0, 6
        ).astype(int)

    # Bounce count: increase (cash flow stress)
    if "bounce_count_6m" in production_df.columns:
        production_df["bounce_count_6m"] = np.clip(
            production_df["bounce_count_6m"]
            + rng.poisson(drift_strength * 1.2, len(production_df)),
            0, 12
        ).astype(int)

    # GST filing regularity: slight decline
    if "gst_filing_regularity_pct" in production_df.columns:
        production_df["gst_filing_regularity_pct"] = np.clip(
            production_df["gst_filing_regularity_pct"]
            - drift_strength * 8
            + rng.normal(0, 3, len(production_df)),
            0, 100
        )

    # Credit utilization: increase
    if "credit_utilization_ratio" in production_df.columns:
        production_df["credit_utilization_ratio"] = np.clip(
            production_df["credit_utilization_ratio"]
            + drift_strength * 0.08
            + rng.normal(0, 0.02, len(production_df)),
            0, 1
        )

    return production_df


if __name__ == "__main__":
    # Quick self-test
    test_df = pd.read_csv(
        "04_model_risk_management/data/test_set_with_predictions.csv"
    )
    print(f"Reference dataset: {test_df.shape}")

    production_df = simulate_production_drift(test_df, drift_strength=0.3)
    print(f"Simulated production dataset: {production_df.shape}")

    report = compute_psi_report(test_df, production_df)
    print(f"\nPSI Report — {len(report)} features evaluated")
    print(f"\nTop 10 features by PSI:\n{report.head(10).to_string(index=False)}")
    print(f"\nStatus summary:\n{report['status'].value_counts().to_string()}")

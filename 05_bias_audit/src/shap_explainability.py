"""
Module 5: Algorithmic Bias Audit
shap_explainability.py — SHAP feature importance and explainability analysis.

Identifies which features drive credit decisions globally and
whether protected attributes or their proxies dominate model output.

Key questions answered:
  1. Which features does the model rely on most? (global importance)
  2. Is bureau_score the primary driver, as expected? (sanity check)
  3. Do protected attributes appear as top drivers? (direct discrimination)
  4. Do correlated features act as proxies? (indirect discrimination)
  5. How do SHAP values differ by gender group? (group-level attribution)
"""

import pandas as pd
import numpy as np
import json
import os
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for file output
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import xgboost as xgb
import shap

# ── Constants ─────────────────────────────────────────────────────────────────
TEST_DATA_PATH   = "04_model_risk_management/data/test_set_with_predictions.csv"
MODEL_PATH       = "04_model_risk_management/models/gro_score_proxy_v1.json"
FEATURE_NAMES_PATH = "04_model_risk_management/models/feature_names.json"
PLOTS_DIR        = "05_bias_audit/plots"
REPORTS_DIR      = "05_bias_audit/reports"

PROTECTED_ATTRIBUTES = ["proprietor_gender", "state", "sector"]
TOP_N_FEATURES   = 20  # features to show in importance plot


# ── Load model and data ───────────────────────────────────────────────────────
def load_model_and_data():
    # Load model
    model = xgb.XGBClassifier()
    model.load_model(MODEL_PATH)
    print(f"Model loaded: {MODEL_PATH}")

    # Load feature names
    with open(FEATURE_NAMES_PATH) as f:
        feature_names = json.load(f)
    print(f"Feature names loaded: {len(feature_names)} features")

    # Load test data
    df = pd.read_csv(TEST_DATA_PATH)
    print(f"Test data loaded: {df.shape}")

    # Extract feature matrix (encoded columns only)
    X_test = df[feature_names].copy()
    print(f"Feature matrix: {X_test.shape}\n")

    return model, df, X_test, feature_names


# ── Compute SHAP values ───────────────────────────────────────────────────────
def compute_shap_values(model, X_test):
    """
    Compute SHAP values using TreeExplainer.
    TreeExplainer is exact (not approximate) for tree-based models
    and is orders of magnitude faster than KernelExplainer.
    Returns shap_values array shape (n_samples, n_features).
    """
    print("Computing SHAP values (TreeExplainer)...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    print(f"SHAP values shape: {shap_values.shape}\n")
    return explainer, shap_values


# ── Global feature importance ─────────────────────────────────────────────────
def plot_global_importance(shap_values, feature_names, top_n=TOP_N_FEATURES):
    """
    Plot mean absolute SHAP values — global feature importance.
    Flags protected attribute features in red for audit visibility.
    """
    mean_abs_shap = np.abs(shap_values).mean(axis=0)
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "mean_abs_shap": mean_abs_shap
    }).sort_values("mean_abs_shap", ascending=False).head(top_n)

    # Identify protected attribute features
    protected_keywords = [
        "proprietor_gender", "state_", "sector_", "entity_type_"
    ]
    importance_df["is_protected"] = importance_df["feature"].apply(
        lambda f: any(kw in f for kw in protected_keywords)
    )

    print(f"Top {top_n} features by mean absolute SHAP value:")
    print(importance_df[["feature", "mean_abs_shap",
                          "is_protected"]].to_string(index=False))

    # Plot
    colors = ["#e74c3c" if p else "#3498db"
              for p in importance_df["is_protected"]]

    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(
        importance_df["feature"][::-1],
        importance_df["mean_abs_shap"][::-1],
        color=colors[::-1]
    )
    ax.set_xlabel("Mean |SHAP Value|", fontsize=12)
    ax.set_title(
        f"GRO Score Proxy — Top {top_n} Features by SHAP Importance\n"
        "Red = Protected attribute or proxy | Blue = Risk feature",
        fontsize=12
    )
    blue_patch = mpatches.Patch(color="#3498db", label="Risk feature")
    red_patch  = mpatches.Patch(color="#e74c3c", label="Protected attribute / proxy")
    ax.legend(handles=[blue_patch, red_patch], loc="lower right")
    plt.tight_layout()

    path = os.path.join(PLOTS_DIR, "shap_global_importance.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nPlot saved: {path}")

    return importance_df


# ── Bureau score dependence plot ──────────────────────────────────────────────
def plot_bureau_score_dependence(shap_values, X_test, feature_names):
    """
    SHAP dependence plot for bureau_score.
    Should show clean negative relationship:
    higher bureau score -> lower SHAP value -> lower predicted default risk.
    Non-monotonic pattern would indicate the model is not using
    bureau score as the primary credit signal.
    """
    if "bureau_score" not in feature_names:
        print("bureau_score not in features — skipping dependence plot")
        return

    idx = feature_names.index("bureau_score")
    shap_bureau = shap_values[:, idx]
    bureau_vals = X_test["bureau_score"].values

    fig, ax = plt.subplots(figsize=(9, 5))
    scatter = ax.scatter(
        bureau_vals, shap_bureau,
        alpha=0.3, c=bureau_vals,
        cmap="RdYlGn", s=10
    )
    plt.colorbar(scatter, ax=ax, label="Bureau Score")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Bureau Score", fontsize=12)
    ax.set_ylabel("SHAP Value (contribution to default prediction)", fontsize=12)
    ax.set_title(
        "SHAP Dependence — Bureau Score\n"
        "Negative SHAP = reduces default prediction (good credit signal)",
        fontsize=12
    )
    plt.tight_layout()

    path = os.path.join(PLOTS_DIR, "shap_bureau_dependence.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Plot saved: {path}")

    # Compute correlation as a sanity check
    corr = np.corrcoef(bureau_vals, shap_bureau)[0, 1]
    print(f"Bureau score vs SHAP correlation: {corr:.4f} "
          f"(expected strongly negative)")
    return corr


# ── Gender group SHAP attribution ─────────────────────────────────────────────
def analyse_gender_shap(shap_values, X_test, df, feature_names):
    """
    Compare mean SHAP values by gender group to identify:
    1. Direct discrimination: proprietor_gender features have high SHAP
    2. Proxy discrimination: correlated features (sector, state) differ by gender
    """
    if "proprietor_gender" not in df.columns:
        print("proprietor_gender not in df — skipping gender SHAP analysis")
        return

    shap_df = pd.DataFrame(shap_values, columns=feature_names)
    shap_df["proprietor_gender"] = df["proprietor_gender"].values

    # Mean SHAP by gender for gender-related features
    gender_features = [f for f in feature_names if "proprietor_gender" in f]
    state_features  = [f for f in feature_names if "state_" in f]
    sector_features = [f for f in feature_names if "sector_" in f]

    print("\n=== Mean SHAP by Gender — Direct Attribution ===")
    gender_shap = shap_df.groupby("proprietor_gender")[gender_features].mean()
    print(gender_shap.round(4).to_string())

    print("\n=== Mean Total SHAP by Gender (sum of all features) ===")
    total_shap = shap_df.groupby("proprietor_gender")[feature_names].sum()
    # Recompute properly
    shap_cols = [c for c in shap_df.columns if c != "proprietor_gender"]
    shap_df["total_shap"] = shap_df[shap_cols].sum(axis=1)
    mean_total = shap_df.groupby("proprietor_gender")["total_shap"].mean()
    print(mean_total.round(4).to_string())
    print("(Higher total SHAP = model pushes toward higher default prediction)")

    print("\n=== Mean SHAP for State Features by Gender ===")
    state_shap_by_gender = shap_df.groupby(
        "proprietor_gender")[state_features].mean().sum(axis=1)
    print(state_shap_by_gender.round(4).to_string())

    print("\n=== Mean SHAP for Sector Features by Gender ===")
    sector_shap_by_gender = shap_df.groupby(
        "proprietor_gender")[sector_features].mean().sum(axis=1)
    print(sector_shap_by_gender.round(4).to_string())

    # Plot: total SHAP distribution by gender
    fig, ax = plt.subplots(figsize=(9, 5))
    gender_groups = shap_df["proprietor_gender"].unique()
    colors_map = {"Male": "#3498db", "Female": "#e74c3c", "Other": "#2ecc71"}
    for g in gender_groups:
        subset = shap_df[shap_df["proprietor_gender"] == g]["total_shap"]
        ax.hist(subset, bins=40, alpha=0.6,
                label=f"{g} (n={len(subset)})",
                color=colors_map.get(g, "grey"))
    ax.axvline(0, color="black", linewidth=1, linestyle="--")
    ax.set_xlabel("Total SHAP Value (sum across all features)", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_title(
        "Distribution of Total SHAP Values by Gender\n"
        "Rightward shift = model predicts higher default risk",
        fontsize=12
    )
    ax.legend()
    plt.tight_layout()

    path = os.path.join(PLOTS_DIR, "shap_gender_distribution.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nPlot saved: {path}")

    return mean_total


# ── Top feature rank for protected attributes ─────────────────────────────────
def report_protected_attribute_ranks(importance_df):
    """
    Report where protected attribute features rank in global importance.
    Any protected attribute in top 10 is a governance finding.
    """
    print("\n=== Protected Attribute Feature Rankings ===")
    importance_ranked = importance_df.reset_index(drop=True)
    importance_ranked.index += 1  # 1-based rank

    protected_rows = importance_ranked[importance_ranked["is_protected"]]
    if len(protected_rows) > 0:
        print(protected_rows[["feature", "mean_abs_shap"]].to_string())
        top10_protected = protected_rows[protected_rows.index <= 10]
        if len(top10_protected) > 0:
            print(f"\n⚠ FINDING: {len(top10_protected)} protected attribute "
                  f"feature(s) in top 10 — direct discrimination evidence")
        else:
            print(f"\n✓ No protected attributes in top 10 features")
    else:
        print("No protected attribute features found in importance ranking")


# ── Save SHAP summary ─────────────────────────────────────────────────────────
def save_shap_summary(importance_df, bureau_corr, mean_total_shap):
    """Save key SHAP findings as JSON for the audit report."""
    summary = {
        "top_10_features": importance_df.head(10)[
            ["feature", "mean_abs_shap", "is_protected"]
        ].to_dict(orient="records"),
        "bureau_score_shap_correlation": round(float(bureau_corr), 4),
        "mean_total_shap_by_gender": {
            k: round(float(v), 4)
            for k, v in mean_total_shap.items()
        },
        "protected_features_in_top10": importance_df.head(10)[
            importance_df.head(10)["is_protected"]
        ]["feature"].tolist()
    }

    path = os.path.join(REPORTS_DIR, "shap_summary.json")
    with open(path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSHAP summary saved: {path}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    model, df, X_test, feature_names = load_model_and_data()
    explainer, shap_values = compute_shap_values(model, X_test)

    print("=" * 55)
    print("GLOBAL FEATURE IMPORTANCE")
    print("=" * 55)
    importance_df = plot_global_importance(shap_values, feature_names)
    report_protected_attribute_ranks(importance_df)

    print("\n" + "=" * 55)
    print("BUREAU SCORE DEPENDENCE")
    print("=" * 55)
    bureau_corr = plot_bureau_score_dependence(
        shap_values, X_test, feature_names
    )

    print("\n" + "=" * 55)
    print("GENDER GROUP SHAP ATTRIBUTION")
    print("=" * 55)
    mean_total_shap = analyse_gender_shap(
        shap_values, X_test, df, feature_names
    )

    save_shap_summary(importance_df, bureau_corr, mean_total_shap)
    print("\nSHAP explainability analysis complete.")

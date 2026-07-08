"""
Module 4: Model Risk Management
monitoring_dashboard.py — Streamlit model monitoring dashboard.

Displays PSI drift detection, model performance metrics, and
feature importance for GRO Score proxy model.

Run from project root:
    streamlit run 04_model_risk_management/dashboard/monitoring_dashboard.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath("04_model_risk_management/src"))

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import plotly.express as px
from psi_monitor import (
    compute_psi_report, simulate_production_drift
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GRO Shield — Model Monitoring",
    page_icon="🛡️",
    layout="wide"
)

# ── Constants ─────────────────────────────────────────────────────────────────
TEST_DATA_PATH    = "04_model_risk_management/data/test_set_with_predictions.csv"
METRICS_PATH      = "04_model_risk_management/reports/model_metrics.json"
PSI_WARNING       = 0.10
PSI_CRITICAL      = 0.20

PSI_COLORS = {
    "STABLE":   "#2ecc71",
    "WARNING":  "#f39c12",
    "CRITICAL": "#e74c3c"
}

# ── Data loaders ──────────────────────────────────────────────────────────────
@st.cache_data
def load_test_data():
    return pd.read_csv(TEST_DATA_PATH)

@st.cache_data
def load_metrics():
    with open(METRICS_PATH) as f:
        return json.load(f)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛡️ GRO Shield — Model Risk Monitoring Dashboard")
st.caption(
    "Independent governance assessment of UGRO Capital GRO Score 3.0 (proxy). "
    "Built from publicly available information and synthetic data. "
    "Not affiliated with UGRO Capital."
)
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
try:
    reference_df = load_test_data()
    metrics      = load_metrics()
except FileNotFoundError as e:
    st.error(f"Data file not found: {e}. Run train_model.py first.")
    st.stop()

# ── Sidebar controls ──────────────────────────────────────────────────────────
st.sidebar.header("Monitoring Controls")
drift_strength = st.sidebar.slider(
    "Simulated Drift Strength",
    min_value=0.0, max_value=1.0, value=0.3, step=0.05,
    help="0 = no drift, 1 = severe drift. Simulates production data shift."
)
st.sidebar.caption(
    "In production, current data would be replaced by live scoring requests. "
    "This slider simulates economic stress scenarios for demonstration."
)
st.sidebar.divider()
st.sidebar.markdown("**Model:** GRO Score 3.0 (Proxy)")
st.sidebar.markdown("**Model ID:** MDL-001")
st.sidebar.markdown("**Risk Rating:** 🔴 HIGH")
st.sidebar.markdown("**Monitoring Frequency:** Monthly")

# ── Section 1: Model Performance KPIs ────────────────────────────────────────
st.subheader("📊 Model Performance — Training Baseline")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("AUC-ROC",           f"{metrics['auc_roc']:.4f}",      delta="Target: 0.75+")
k2.metric("Avg Precision",     f"{metrics['average_precision']:.4f}")
k3.metric("Default Recall",    f"{metrics['recall_default']:.2%}", delta="-41% missed")
k4.metric("Default Precision", f"{metrics['precision_default']:.2%}")
k5.metric("Test Set Size",     f"{metrics['n_test']:,}")

st.divider()

# ── Section 2: PSI Drift Detection ────────────────────────────────────────────
st.subheader("📡 Population Stability Index — Drift Detection")

production_df = simulate_production_drift(reference_df, drift_strength=drift_strength)
psi_report    = compute_psi_report(reference_df, production_df)

# Summary metrics
n_critical = (psi_report["status"] == "CRITICAL").sum()
n_warning  = (psi_report["status"] == "WARNING").sum()
n_stable   = (psi_report["status"] == "STABLE").sum()
max_psi    = psi_report["psi"].max()

c1, c2, c3, c4 = st.columns(4)
c1.metric("🔴 Critical Features", n_critical,
          delta="Review required" if n_critical > 0 else None,
          delta_color="inverse")
c2.metric("🟡 Warning Features",  n_warning,
          delta="Monitor closely" if n_warning > 0 else None,
          delta_color="inverse")
c3.metric("🟢 Stable Features",   n_stable)
c4.metric("Max PSI",              f"{max_psi:.4f}",
          delta="CRITICAL" if max_psi >= PSI_CRITICAL
          else "WARNING" if max_psi >= PSI_WARNING else "STABLE",
          delta_color="inverse" if max_psi >= PSI_WARNING else "normal")

# PSI bar chart
psi_display = psi_report[psi_report["psi"] > 0].copy()
psi_display["color"] = psi_display["status"].map(PSI_COLORS)

fig_psi = go.Figure()
fig_psi.add_trace(go.Bar(
    x=psi_display["feature"],
    y=psi_display["psi"],
    marker_color=psi_display["color"],
    text=psi_display["status"],
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>PSI: %{y:.4f}<br>Status: %{text}<extra></extra>"
))
fig_psi.add_hline(y=PSI_WARNING,  line_dash="dash",
                  line_color="#f39c12", annotation_text="Warning (0.10)")
fig_psi.add_hline(y=PSI_CRITICAL, line_dash="dash",
                  line_color="#e74c3c", annotation_text="Critical (0.20)")
fig_psi.update_layout(
    title="PSI by Feature — Reference vs Simulated Production",
    xaxis_title="Feature",
    yaxis_title="PSI Value",
    xaxis_tickangle=-45,
    height=450,
    showlegend=False
)
st.plotly_chart(fig_psi, use_container_width=True)

# PSI detail table
st.markdown("**PSI Detail Table**")
styled = psi_report.copy()
styled["status"] = styled["status"].map({
    "CRITICAL": "🔴 CRITICAL",
    "WARNING":  "🟡 WARNING",
    "STABLE":   "🟢 STABLE"
})
st.dataframe(styled, use_container_width=True, hide_index=True)

st.divider()

# ── Section 3: Score Distribution ─────────────────────────────────────────────
st.subheader("📈 Predicted Score Distribution — Reference vs Production")

prod_scores = simulate_production_drift(
    reference_df, drift_strength=drift_strength
)

fig_dist = go.Figure()
fig_dist.add_trace(go.Histogram(
    x=reference_df["predicted_proba"],
    name="Reference (Training)",
    opacity=0.6,
    nbinsx=40,
    marker_color="#3498db"
))

# Simulate production scores: apply drift to predictions proportionally
prod_score_shift = drift_strength * 0.08
prod_scores_vals = np.clip(
    reference_df["predicted_proba"] + prod_score_shift
    + np.random.default_rng(42).normal(0, 0.02, len(reference_df)),
    0, 1
)
fig_dist.add_trace(go.Histogram(
    x=prod_scores_vals,
    name="Simulated Production",
    opacity=0.6,
    nbinsx=40,
    marker_color="#e74c3c"
))
fig_dist.update_layout(
    barmode="overlay",
    title="Predicted Default Probability Distribution",
    xaxis_title="Predicted Probability of Default",
    yaxis_title="Count",
    height=380
)
st.plotly_chart(fig_dist, use_container_width=True)

st.divider()

# ── Section 4: Default Rate by Segment ────────────────────────────────────────
st.subheader("🔍 Observed Default Rate by Segment")

seg_col = st.selectbox(
    "Select segment variable",
    ["proprietor_gender", "sector", "state"],
    help="These are the protected attributes monitored for bias in Module 5."
)

if seg_col in reference_df.columns:
    seg_data = (
        reference_df.groupby(seg_col)["default_flag"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "default_rate", "count": "n"})
        .sort_values("default_rate", ascending=False)
    )
    fig_seg = px.bar(
        seg_data, x=seg_col, y="default_rate",
        text=seg_data["default_rate"].map("{:.1%}".format),
        title=f"Default Rate by {seg_col}",
        labels={"default_rate": "Default Rate"},
        color="default_rate",
        color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"]
    )
    fig_seg.update_traces(textposition="outside")
    fig_seg.update_layout(height=400, coloraxis_showscale=False)
    st.plotly_chart(fig_seg, use_container_width=True)

    st.caption(
        "⚠️ Variation in default rates across protected attributes may reflect "
        "genuine risk differences, systemic bias, or data artefacts. "
        "See Module 5 — Algorithmic Bias Audit for full analysis."
    )

st.divider()

# ── Section 5: Governance Summary ─────────────────────────────────────────────
st.subheader("📋 Governance Status")

gov_data = {
    "Check": [
        "AUC-ROC ≥ 0.75",
        "Default Recall ≥ 0.60",
        "No CRITICAL PSI features",
        "Bias audit complete",
        "Model card documented",
        "Independent validation current"
    ],
    "Status": [
        "✅ Pass"  if metrics["auc_roc"] >= 0.75 else "❌ Fail",
        "✅ Pass"  if metrics["recall_default"] >= 0.60 else "⚠️ Below threshold",
        "✅ Pass"  if n_critical == 0 else f"❌ {n_critical} feature(s) in CRITICAL",
        "✅ Complete (Module 5)",
        "✅ Complete (Module 4)",
        "⚠️ Due Jun 2025"
    ],
    "Detail": [
        f"AUC = {metrics['auc_roc']}",
        f"Recall = {metrics['recall_default']:.2%} — 41% of defaults missed",
        f"Max PSI = {max_psi:.4f} at drift strength {drift_strength}",
        "See bias_audit_report.md",
        "See model_card.md",
        "Last validated Jun 2024"
    ]
}
st.dataframe(pd.DataFrame(gov_data), use_container_width=True, hide_index=True)

st.caption(
    "GRO Shield — Independent Data & AI Governance Assessment | "
    "Not affiliated with UGRO Capital | "
    "Built from publicly available information and synthetic data."
)

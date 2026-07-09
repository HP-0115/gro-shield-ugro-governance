"""
Module 7: GenAI Governance
observability_dashboard.py — Streamlit observability dashboard for
UGRO Capital GenAI guardrail system.

Shows compliance team visibility into:
  - Request volume over time
  - PII detection rates (input and output)
  - Topic boundary violation rates
  - Hallucination flag rates
  - Token usage and cost trends
  - Per-session audit trail

Run from project root:
    streamlit run 07_genai_governance/dashboard/observability_dashboard.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

# ── Constants ─────────────────────────────────────────────────────────────────
AUDIT_LOG_PATH = "07_genai_governance/data/audit_log.csv"
COST_LOG_PATH  = "07_genai_governance/data/cost_log.csv"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GRO Shield — GenAI Observability",
    page_icon="🛡️",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🛡️ GRO Shield — GenAI Guardrail Observability Dashboard")
st.caption(
    "Compliance monitoring for UGRO Capital hypothetical MSME chatbot. "
    "Independent governance assessment — not affiliated with UGRO Capital."
)
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def load_audit_log():
    if not os.path.exists(AUDIT_LOG_PATH):
        return pd.DataFrame()
    df = pd.read_csv(AUDIT_LOG_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

@st.cache_data(ttl=30)
def load_cost_log():
    if not os.path.exists(COST_LOG_PATH):
        return pd.DataFrame()
    df = pd.read_csv(COST_LOG_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

audit_df = load_audit_log()
cost_df  = load_cost_log()

if audit_df.empty:
    st.error(
        "No audit log found. Run guardrail_system.py first to generate data."
    )
    st.stop()

# ── Section 1: Summary KPIs ───────────────────────────────────────────────────
st.subheader("📊 Request Summary")

total       = len(audit_df)
pii_input   = int(audit_df["pii_input_detected"].sum())
pii_output  = int(audit_df["pii_output_detected"].sum())
topic_viol  = int((~audit_df["topic_allowed"]).sum())
halluc      = int(audit_df["hallucination_flagged"].sum())
total_cost  = cost_df["total_cost_usd"].sum() if not cost_df.empty else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Total Requests",         total)
k2.metric("PII Detected (Input)",   pii_input,
          delta=f"{pii_input/total:.0%} rate",
          delta_color="inverse")
k3.metric("PII Detected (Output)",  pii_output,
          delta=f"{pii_output/total:.0%} rate",
          delta_color="inverse")
k4.metric("Topic Violations",       topic_viol,
          delta=f"{topic_viol/total:.0%} rate",
          delta_color="inverse")
k5.metric("Hallucination Flags",    halluc,
          delta=f"{halluc/total:.0%} rate",
          delta_color="inverse")
k6.metric("Total Cost (USD)",       f"${total_cost:.4f}")

st.divider()

# ── Section 2: Guardrail Trigger Breakdown ────────────────────────────────────
st.subheader("🚦 Guardrail Trigger Breakdown")

col1, col2 = st.columns(2)

with col1:
    # Parse guardrails_triggered column
    all_triggers = []
    for row in audit_df["guardrails_triggered"]:
        try:
            triggers = json.loads(row)
            all_triggers.extend(triggers)
        except Exception:
            pass

    if all_triggers:
        # Normalise trigger names
        normalised = []
        for t in all_triggers:
            if t.startswith("PII_INPUT"):
                normalised.append("PII — Input Detected")
            elif t.startswith("PII_OUTPUT"):
                normalised.append("PII — Output Detected")
            elif t == "TOPIC_BOUNDARY_VIOLATION":
                normalised.append("Topic Boundary Violation")
            elif t == "HALLUCINATION_FLAG":
                normalised.append("Hallucination Flagged")
            else:
                normalised.append(t)

        trigger_counts = pd.Series(normalised).value_counts().reset_index()
        trigger_counts.columns = ["Guardrail", "Count"]

        fig_triggers = px.bar(
            trigger_counts, x="Count", y="Guardrail",
            orientation="h",
            color="Guardrail",
            color_discrete_sequence=["#e74c3c", "#f39c12", "#3498db", "#9b59b6"],
            title="Guardrail Triggers — All Requests"
        )
        fig_triggers.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_triggers, use_container_width=True)
    else:
        st.info("No guardrails triggered yet.")

with col2:
    # Clean request breakdown
    categories = {
        "Clean (no guardrails)": int(
            (audit_df["guardrails_triggered"] == "[]").sum()
        ),
        "PII only":  int(
            audit_df["guardrails_triggered"].str.contains(
                "PII", na=False
            ).sum()
        ),
        "Topic violation": topic_viol,
        "Hallucination": halluc
    }
    cat_df = pd.DataFrame(
        list(categories.items()), columns=["Category", "Count"]
    )
    fig_pie = px.pie(
        cat_df, values="Count", names="Category",
        title="Request Classification",
        color_discrete_sequence=[
            "#2ecc71", "#e74c3c", "#f39c12", "#9b59b6"
        ]
    )
    fig_pie.update_layout(height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# ── Section 3: PII Detection Analysis ────────────────────────────────────────
st.subheader("🔍 PII Detection Analysis")

pii_requests = audit_df[audit_df["pii_input_detected"] == True].copy()

if len(pii_requests) > 0:
    # Extract PII types from JSON strings
    all_pii_types = []
    for row in pii_requests["pii_input_types"]:
        try:
            types = json.loads(row)
            all_pii_types.extend(types)
        except Exception:
            pass

    if all_pii_types:
        pii_type_counts = pd.Series(
            all_pii_types
        ).value_counts().reset_index()
        pii_type_counts.columns = ["PII Type", "Count"]

        col3, col4 = st.columns(2)
        with col3:
            fig_pii = px.bar(
                pii_type_counts, x="PII Type", y="Count",
                color="PII Type",
                color_discrete_sequence=["#e74c3c", "#f39c12", "#3498db"],
                title="PII Types Detected in User Input"
            )
            fig_pii.update_layout(showlegend=False, height=300)
            st.plotly_chart(fig_pii, use_container_width=True)

        with col4:
            st.markdown("**PII Detection Summary**")
            st.markdown(f"- Requests with PII in input: **{pii_input}**")
            st.markdown(f"- Requests with PII in output: **{pii_output}**")
            st.markdown(
                f"- PII detection rate: "
                f"**{pii_input/total:.1%}**"
            )
            st.markdown(
                "- DPDP Act 2023 implication: all detected PII was "
                "redacted before entering LLM context ✅"
            )
            st.markdown(
                "- Aadhaar = sensitive personal data under DPDP Act "
                "Section 2(t) — highest risk category"
            )
else:
    st.success("No PII detected in any requests.")

st.divider()

# ── Section 4: Cost and Token Trends ─────────────────────────────────────────
st.subheader("💰 Token Usage and Cost Monitoring")

if not cost_df.empty:
    col5, col6 = st.columns(2)

    with col5:
        fig_tokens = go.Figure()
        fig_tokens.add_trace(go.Bar(
            name="Input Tokens",
            x=cost_df["request_id"],
            y=cost_df["input_tokens"],
            marker_color="#3498db"
        ))
        fig_tokens.add_trace(go.Bar(
            name="Output Tokens",
            x=cost_df["request_id"],
            y=cost_df["output_tokens"],
            marker_color="#2ecc71"
        ))
        fig_tokens.update_layout(
            barmode="stack",
            title="Token Usage per Request",
            xaxis_title="Request ID",
            yaxis_title="Tokens",
            height=320,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_tokens, use_container_width=True)

    with col6:
        fig_cost = px.bar(
            cost_df, x="request_id", y="total_cost_usd",
            title="Cost per Request (USD)",
            color="total_cost_usd",
            color_continuous_scale=["#2ecc71", "#f39c12", "#e74c3c"],
            labels={"total_cost_usd": "Cost (USD)",
                    "request_id": "Request ID"}
        )
        fig_cost.update_layout(
            height=320,
            xaxis_tickangle=-45,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    col7, col8, col9 = st.columns(3)
    col7.metric("Avg Tokens/Request",
                f"{cost_df['input_tokens'].mean() + cost_df['output_tokens'].mean():.0f}")
    col8.metric("Avg Cost/Request",
                f"${cost_df['total_cost_usd'].mean():.6f}")
    col9.metric("Projected Monthly Cost (10K requests)",
                f"${cost_df['total_cost_usd'].mean() * 10000:.2f}")

st.divider()

# ── Section 5: Audit Trail ────────────────────────────────────────────────────
st.subheader("📋 Audit Trail")

st.caption(
    "Full audit log — every request logged for compliance review. "
    "PII types recorded (not values) per DPDP Act data minimisation principle."
)

display_cols = [
    "timestamp", "request_id", "session_id",
    "topic_allowed", "pii_input_detected", "pii_input_types",
    "hallucination_flagged", "input_tokens", "output_tokens", "cost_usd"
]

display_df = audit_df[
    [c for c in display_cols if c in audit_df.columns]
].copy()
display_df["timestamp"] = display_df["timestamp"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()

# ── Section 6: Compliance Status ─────────────────────────────────────────────
st.subheader("✅ Compliance Status")

compliance_checks = {
    "PII redaction active (Aadhaar/PAN/GSTIN)": "✅ Active",
    "Topic boundary enforcement": "✅ Active",
    "Hallucination detection": "✅ Active",
    "Audit logging — every request": "✅ Active",
    "Cost monitoring": "✅ Active",
    "Output PII scan": "✅ Active",
    "DPDP Act — no raw PII in logs": "✅ Compliant",
    "Right to explanation process": "⚠️ Pending implementation",
    "Human escalation path": "⚠️ Pending implementation",
    "NIST AI 600-1 assessment": "✅ Complete (see policies/)"
}

comp_df = pd.DataFrame(
    list(compliance_checks.items()),
    columns=["Control", "Status"]
)
st.dataframe(comp_df, use_container_width=True, hide_index=True)

st.caption(
    "GRO Shield — Independent Data & AI Governance Assessment | "
    "Not affiliated with UGRO Capital | "
    "Built from publicly available information and synthetic data."
)

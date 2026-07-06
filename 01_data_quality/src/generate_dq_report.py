"""
generate_dq_report.py
Generates a professional Data Quality Assessment Report PDF
written for a Chief Data Officer audience.

Usage:
    python generate_dq_report.py \
        --scorecard ../../reports/dq_scorecard.csv \
        --out ../../reports/dq_assessment_report.pdf
"""

import argparse
from datetime import date

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


# Brand colors for the report
DARK_BLUE = colors.HexColor("#1B3A6B")
MEDIUM_BLUE = colors.HexColor("#2E6DA4")
LIGHT_BLUE = colors.HexColor("#EBF3FB")
ACCENT_GREEN = colors.HexColor("#27AE60")
ACCENT_RED = colors.HexColor("#E74C3C")
ACCENT_ORANGE = colors.HexColor("#F39C12")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
MID_GRAY = colors.HexColor("#7F8C8D")


def build_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        fontSize=22,
        textColor=DARK_BLUE,
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="ReportSubtitle",
        fontSize=13,
        textColor=MEDIUM_BLUE,
        spaceAfter=4,
        alignment=TA_CENTER,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        name="SectionHeading",
        fontSize=13,
        textColor=DARK_BLUE,
        spaceBefore=14,
        spaceAfter=6,
        fontName="Helvetica-Bold",
    ))
    styles.add(ParagraphStyle(
        name="BodyText2",
        fontSize=10,
        textColor=colors.black,
        spaceAfter=6,
        leading=16,
        alignment=TA_JUSTIFY,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        name="BulletText",
        fontSize=10,
        textColor=colors.black,
        spaceAfter=4,
        leading=14,
        leftIndent=16,
        fontName="Helvetica",
    ))
    styles.add(ParagraphStyle(
        name="Disclaimer",
        fontSize=8,
        textColor=MID_GRAY,
        spaceAfter=4,
        leading=12,
        alignment=TA_JUSTIFY,
        fontName="Helvetica-Oblique",
    ))

    return styles


def build_report_content(scorecard, styles):
    story = []
    overall_score = round(scorecard["dimension_score"].mean(), 1)

    # --- COVER ---
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("DATA QUALITY ASSESSMENT REPORT", styles["ReportTitle"]))
    story.append(Paragraph("GRO Shield — Independent Governance Assessment", styles["ReportSubtitle"]))
    story.append(Paragraph("Subject: UGRO Capital Limited (Synthetic Dataset)", styles["ReportSubtitle"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Assessment Date: {date.today().strftime('%d %B %Y')}", styles["ReportSubtitle"]))
    story.append(Paragraph("Prepared by: GRO Shield Governance Framework", styles["ReportSubtitle"]))
    story.append(Spacer(1, 1*cm))

    # Overall score banner
    score_color = ACCENT_GREEN if overall_score >= 95 else ACCENT_ORANGE if overall_score >= 85 else ACCENT_RED
    score_data = [[f"Overall DQ Score: {overall_score} / 100"]]
    score_table = Table(score_data, colWidths=[16*cm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), score_color),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 16),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    score_table.hAlign = "CENTER"    
    story.append(Spacer(1, 0.5*cm))
    story.append(score_table)
    story.append(Spacer(1, 1*cm))
    story.append(PageBreak())

    # --- SECTION 1: EXECUTIVE SUMMARY ---
    story.append(Paragraph("1. Executive Summary", styles["SectionHeading"]))
    story.append(Paragraph(
        f"This report presents the findings of an independent data quality assessment "
        f"conducted on a synthetic MSME loan dataset modeled on the data categories "
        f"publicly described by UGRO Capital Limited for its GRO Score 3.0 credit "
        f"scoring model. The assessment evaluated 15,000 loan application records "
        f"across six internationally recognised data quality dimensions: Completeness, "
        f"Accuracy, Validity, Uniqueness, Consistency, and Timeliness.",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        f"The dataset achieved an overall DQ score of {overall_score}/100. "
        f"The most significant finding is in the Completeness dimension, where 8.83% "
        f"of records contain missing values across bank statement and GST data fields — "
        f"the two external data source categories most critical to GRO Score model "
        f"inputs. Underwriting decisions made on incomplete bureau, bank statement, or "
        f"GST data carry elevated credit risk and potential fair lending exposure.",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        f"Three priority recommendations are made: (1) implement automated "
        f"completeness monitoring with a 99% threshold on all model input fields, "
        f"(2) establish a data freshness policy requiring bureau and GST data pulls "
        f"within 30 days of application date, and (3) deploy format validation checks "
        f"on PAN and GSTIN fields at the point of data ingestion rather than "
        f"post-processing.",
        styles["BodyText2"]
    ))

    # --- SECTION 2: SCOPE AND METHODOLOGY ---
    story.append(Paragraph("2. Scope and Methodology", styles["SectionHeading"]))
    story.append(Paragraph(
        "The assessment was conducted on a 15,000-row synthetic dataset structured "
        "to mirror UGRO Capital's publicly disclosed data categories: credit bureau "
        "data, bank statement data, and GST data, supplemented by loan application "
        "metadata and outcomes. No real customer, credit bureau, or financial data "
        "was used at any stage.",
        styles["BodyText2"]
    ))
    story.append(Paragraph(
        "A ground-truth methodology was employed: data quality issues were "
        "deliberately injected across all six dimensions before validation, with "
        "every injection logged. This enabled calculation of suite recall — the "
        "percentage of known issues the validation suite actually detected — "
        "producing a recall rate of 94.3% across 2,370 injected issues. "
        "Validation was performed using Great Expectations v1.x.",
        styles["BodyText2"]
    ))

    # --- SECTION 3: FINDINGS BY DIMENSION ---
    story.append(Paragraph("3. Findings by Dimension", styles["SectionHeading"]))

    dimension_narratives = {
        "Completeness": (
            "8.83% of records contain missing values, concentrated in bank "
            "statement fields (avg_monthly_balance, avg_monthly_credit_turnover) "
            "and GST filing data. The most likely root cause is upstream data "
            "pipeline failures — PDF bank statement parsing errors and GSTN API "
            "sync delays for recently registered businesses. Missing model inputs "
            "require fallback scoring logic; without it, affected applications "
            "may be incorrectly declined or approved on partial information."
        ),
        "Accuracy": (
            "2.38% of records contain inaccurate values including bureau scores "
            "outside the valid 300-900 range, negative loan amounts caused by "
            "ETL sign-flip errors, and interest rates with decimal shift errors "
            "(e.g. 1800% instead of 18%). While the overall rate is low, "
            "inaccurate bureau scores directly corrupt the primary credit signal "
            "in GRO Score, making this a high-severity finding despite its "
            "relatively low frequency."
        ),
        "Validity": (
            "1.29% of records contain values outside defined controlled "
            "vocabularies or format specifications. PAN numbers failing the "
            "standard 10-character alphanumeric format and state names not "
            "matching the approved list indicate free-text contamination from "
            "manual data entry or inconsistent source system mappings. "
            "Invalid identifiers break downstream KYC and deduplication processes."
        ),
        "Uniqueness": (
            "0.40% of applicant IDs are duplicated, indicating primary key "
            "collisions likely caused by merge or upsert bugs during data "
            "pipeline execution. While the rate is low, duplicate primary keys "
            "are a critical data integrity failure — they make it impossible to "
            "reliably link records across systems and can result in the same "
            "applicant being processed twice."
        ),
        "Consistency": (
            "1.50% of records contain cross-field contradictions: approved loan "
            "amounts exceeding requested amounts, non-zero approved amounts on "
            "rejected applications, and GST registration dates postdating the "
            "loan application. These violations indicate insufficient "
            "cross-field validation at the point of data entry and create "
            "downstream reconciliation failures between the LOS and LMS."
        ),
        "Timeliness": (
            "1.20% of records show application dates suggesting bureau data "
            "was pulled more than 90 days before the underwriting decision. "
            "Stale credit data is a recognised underwriting risk — a borrower's "
            "credit profile can change materially over 90 days. RBI Digital "
            "Lending Guidelines implicitly require that data used for credit "
            "decisions reflects the applicant's current financial position."
        ),
    }

    for _, row in scorecard.iterrows():
        dim = row["dimension"]
        score = row["dimension_score"]
        status = row["ge_status"]
        color = ACCENT_GREEN if score >= 98 else ACCENT_ORANGE if score >= 95 else ACCENT_RED

        dim_data = [[
            f"{dim}",
            f"Score: {score}/100",
            f"GE: {status}"
        ]]
        dim_table = Table(dim_data, colWidths=[6*cm, 5*cm, 5*cm])
        dim_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), color),
            ("BACKGROUND", (1, 0), (2, 0), LIGHT_BLUE),
            ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
            ("TEXTCOLOR", (1, 0), (2, 0), DARK_BLUE),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("BOX", (0, 0), (-1, -1), 0.5, MID_GRAY),
        ]))
        dim_table.hAlign = "CENTER"    
        story.append(dim_table)
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(
            dimension_narratives[dim], styles["BodyText2"]
        ))

    # --- SECTION 4: SCORECARD TABLE ---
    story.append(PageBreak())
    story.append(Paragraph("4. Overall DQ Scorecard", styles["SectionHeading"]))

    table_data = [["Dimension", "Issues", "Rows Affected",
                   "Violation Rate", "Score", "GE Status"]]
    for _, row in scorecard.iterrows():
        table_data.append([
            row["dimension"],
            str(row["issues_injected"]),
            str(row["rows_affected"]),
            f"{row['violation_rate_pct']}%",
            f"{row['dimension_score']}/100",
            row["ge_status"],
        ])
    table_data.append([
        "OVERALL", "", "", "",
        f"{overall_score}/100", ""
    ])

    scorecard_table = Table(table_data, colWidths=[3.5*cm, 2*cm, 3*cm, 3*cm, 2.5*cm, 2.5*cm])
    scorecard_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, LIGHT_GRAY]),
        ("BACKGROUND", (0, -1), (-1, -1), LIGHT_BLUE),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BOX", (0, 0), (-1, -1), 0.5, MID_GRAY),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, MID_GRAY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    scorecard_table.hAlign = "CENTER"
    story.append(scorecard_table)

    # --- SECTION 5: RECOMMENDATIONS ---
    story.append(Paragraph("5. Recommendations", styles["SectionHeading"]))

    recommendations = [
        ("P1 — Completeness Monitoring",
         "Implement automated null-value monitoring on all GRO Score model "
         "input fields with a 99% completeness threshold. Alert on breach "
         "within 1 business day. Establish fallback scoring logic for "
         "new-to-credit applicants with no bureau history."),
        ("P2 — Data Freshness Policy",
         "Define and enforce a maximum data age policy: bureau data no older "
         "than 30 days at point of underwriting decision, GST data no older "
         "than 60 days. Automate pull-date validation at ingestion."),
        ("P3 — Point-of-Ingestion Validation",
         "Deploy PAN and GSTIN format validation at the data ingestion layer "
         "rather than post-processing. Reject malformed identifiers at source "
         "to prevent downstream KYC and deduplication failures."),
    ]

    for title, body in recommendations:
        story.append(Paragraph(f"<b>{title}</b>", styles["BodyText2"]))
        story.append(Paragraph(body, styles["BulletText"]))
        story.append(Spacer(1, 0.2*cm))

    # --- DISCLAIMER ---
    story.append(PageBreak())
    story.append(Paragraph("Disclaimer", styles["SectionHeading"]))
    story.append(Paragraph(
        "This report is an independent, self-initiated portfolio project. "
        "It is not affiliated with, endorsed by, or commissioned by UGRO Capital "
        "Limited. All findings are based on a synthetic dataset generated by the "
        "author and do not reflect UGRO Capital's actual data quality posture. "
        "No real customer, credit bureau, bank statement, or GST data was used. "
        "This report is produced solely to demonstrate data governance assessment "
        "methodology for career portfolio purposes.",
        styles["Disclaimer"]
    ))

    return story


def main():
    parser = argparse.ArgumentParser(
        description="Generate DQ Assessment Report PDF"
    )
    parser.add_argument("--scorecard", type=str,
                        default="../../reports/dq_scorecard.csv")
    parser.add_argument("--out", type=str,
                        default="../../reports/dq_assessment_report.pdf")
    args = parser.parse_args()

    print("Loading scorecard...")
    scorecard = pd.read_csv(args.scorecard)

    print("Building styles...")
    styles = build_styles()

    print("Building report content...")
    story = build_report_content(scorecard, styles)

    print(f"Generating PDF -> {args.out}...")
    doc = SimpleDocTemplate(
        args.out,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )
    doc.build(story)
    print("Done.")


if __name__ == "__main__":
    main()

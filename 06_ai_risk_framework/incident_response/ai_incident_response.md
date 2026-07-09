# AI Incident Response Procedure
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital.

**Version:** 1.0
**Effective Date:** 1 January 2025
**Owner:** Chief Risk Officer
**Next Review:** 1 January 2026

---

## 1. Purpose

This procedure defines how UGRO Capital detects, responds to, and
learns from AI incidents — events where an AI system produces
incorrect, harmful, biased, or non-compliant outputs that affect
borrowers, portfolio quality, or regulatory standing.

AI incidents are distinct from general IT incidents. A system outage
is an IT incident. A model that has been running correctly for six
months but has silently drifted to produce discriminatory outputs
is an AI incident — harder to detect, harder to scope, and with
potentially larger affected populations.

---

## 2. Incident Classification

### P1 — Critical (Response: 4 hours)
AI system is causing or has caused material harm at scale.

**Examples:**
- Model confirmed producing discriminatory outputs for a protected
  group — e.g., Female proprietors being rejected at rates inconsistent
  with actual credit risk, confirmed by fairness audit
- PSI CRITICAL breach (> 0.20) on bureau score or DPD-90 confirmed
  to be causing material mispricing across portfolio
- DPDP Act data breach involving AI training or scoring data
- Regulatory enforcement action initiated related to AI system
- Model producing outputs outside any reasonable range
  (e.g., predicting 90%+ default for all applicants)

**Escalation:** CRO notified within 1 hour; Board Risk Committee
notified within 4 hours; RBI notification assessed within 24 hours;
DPDP Act breach notification to Data Protection Board within 72 hours
if personal data involved.

### P2 — High (Response: 24 hours)
AI system performance has degraded significantly or a material
governance gap has been identified.

**Examples:**
- AUC-ROC drops below 0.70 on quarterly validation
- PSI WARNING (0.10–0.20) on two or more key features simultaneously
- EOD breach above 0.20 for any protected attribute on quarterly review
- Independent validation returns Fail (not Conditional Pass)
- Open Critical finding in model inventory not remediated within SLA
- Human oversight mechanism failure — borderline cases processed
  automatically without review

**Escalation:** CRO notified within 4 hours; Model Risk Committee
convened within 24 hours; remediation plan within 5 business days.

### P3 — Medium (Response: 72 hours)
Localised AI issue with limited scope or individual impact.

**Examples:**
- Individual applicant receives incorrect rejection explanation
- Data quality issue affecting a subset of scoring inputs
- PSI WARNING on a non-critical feature
- Model card or documentation gap identified
- Single false negative (default missed) identified through
  portfolio monitoring — within expected model error rate

**Escalation:** Data Science Lead and Compliance notified within
24 hours; investigation within 72 hours; remediation within
10 business days.

### P4 — Low (Response: 5 business days)
Administrative or documentation issue with no immediate borrower impact.

**Examples:**
- Monitoring dashboard unavailable for less than 24 hours
- Model card not updated within SLA after minor parameter change
- Training log missing for a non-production experiment
- Regulatory horizon scan overdue

**Escalation:** Logged in risk register; assigned owner; resolved
within next review cycle.

---

## 3. Response Procedure

### Phase 1: Detection and Triage (0–1 hour for P1/P2)

**Detection sources:**
- PSI monitoring dashboard — automated monthly alerts
- Quarterly fairness metric review — Compliance team
- Quarterly model performance validation — Data Science
- Borrower complaints — escalated through grievance redressal
- Regulator enquiry or audit finding
- Internal whistleblower report
- Portfolio loss rate deviating from model predictions

**Triage steps:**
1. Incident reporter logs event in AI incident register with:
   - Date and time of detection
   - Description of observed behaviour
   - Data source that surfaced the issue
   - Preliminary scope estimate (how many applicants affected?)
2. On-call Data Science lead classifies P1/P2/P3/P4 within 30 minutes
3. If P1 or P2: immediate escalation per Section 2
4. Incident assigned to Investigation Lead

### Phase 2: Containment (P1: within 2 hours; P2: within 8 hours)

**Containment options — in order of preference:**

**Option A — Threshold adjustment**
If the incident is a calibration issue (model systematically
over- or under-predicting for a specific group), apply a temporary
group-specific threshold adjustment pending retraining.
- Requires: Data Science Lead + Compliance sign-off
- Documented as a temporary measure with defined expiry date
- Must not be used for more than 90 days without retraining

**Option B — Human review mandate**
Suspend automated decisions for the affected population segment
and route all cases to human underwriter review.
- Requires: CRO approval
- Operationally intensive but safest option for borrowers
- Preferred for P1 incidents involving confirmed discrimination

**Option C — Model suspension**
Suspend the AI model entirely and revert to manual underwriting
or a previously validated model version.
- Requires: CRO + CDO approval
- Last resort — significant operational impact
- Required if model is producing outputs harmful to all applicants

**Option D — Feature quarantine**
Identify and neutralise the specific feature(s) driving the incident
by setting them to a neutral value while the full fix is prepared.
- Requires: Data Science Lead + Model Risk Committee approval
- Only viable if root cause is isolated to specific features

### Phase 3: Investigation (P1: within 24 hours; P2: within 5 days)

**Investigation checklist:**

**Data investigation:**
- [ ] Check PSI for all features — identify drift pattern
- [ ] Check data quality for features involved in incident
- [ ] Check for upstream data source changes (bureau, GST, banking)
- [ ] Check training data distribution for affected population segment
- [ ] Check consent validity for data used in affected decisions

**Model investigation:**
- [ ] Run SHAP analysis on affected population segment
- [ ] Compare predicted vs actual default rates for affected group
- [ ] Check for recent model version changes
- [ ] Run fairness metrics on affected period's scoring outputs
- [ ] Check model monitoring logs for early warning signals missed

**Process investigation:**
- [ ] Were monitoring alerts triggered? If yes, were they acted on?
- [ ] Were quarterly reviews completed on schedule?
- [ ] Was human oversight mechanism functioning?
- [ ] Were open model risk findings relevant to this incident?

**Scope determination:**
- How many applicants were affected?
- What time period?
- What is the estimated financial impact on affected borrowers?
- What is the estimated portfolio impact?

### Phase 4: Remediation (timeline depends on severity)

**P1 remediation timeline:**
- Containment: within 2 hours
- Root cause identified: within 24 hours
- Interim fix deployed: within 72 hours
- Permanent fix (retraining or process change): within 30 days
- Post-incident review: within 14 days of permanent fix
- Regulatory notification: per applicable timelines (see Section 5)

**P2 remediation timeline:**
- Containment: within 8 hours
- Root cause identified: within 5 business days
- Remediation plan: within 10 business days
- Permanent fix: within 60 days
- Post-incident review: within 30 days of permanent fix

### Phase 5: Affected Borrower Remediation

For P1 incidents involving confirmed wrongful rejections:

1. **Identify affected applicants** — all applicants rejected during
   the affected period by the affected model segment
2. **Re-score affected applications** — run corrected model or
   human review on all affected applications
3. **Proactive outreach** — contact affected applicants to offer
   re-assessment; do not wait for them to complain
4. **Remediation offers** — for applicants who would have been
   approved under correct scoring: expedited re-application,
   waived processing fees, priority underwriting
5. **Documentation** — maintain full record of affected applicants,
   outreach attempts, and outcomes for regulatory evidence

### Phase 6: Post-Incident Review

Every P1 and P2 incident must have a formal post-incident review
(PIR) within 14–30 days of resolution.

**PIR output must include:**
- Timeline of events from root cause to resolution
- What detection mechanisms existed and why they did or did not
  surface the incident earlier
- Root cause analysis (5-Whys or equivalent)
- What controls failed and why
- What new controls will prevent recurrence
- Model risk register updates required
- Policy or procedure updates required
- Training requirements identified

**PIR must be reviewed by:** Model Risk Committee
**PIR must be retained for:** 7 years (regulatory evidence)

---

## 4. Roles and Responsibilities

| Role | P1 Responsibility | P2 Responsibility |
|------|------------------|------------------|
| CRO | Incident commander; Board notification; regulatory assessment | Notified within 4 hours; approves containment |
| CDO | Data investigation lead; upstream data source assessment | Supports investigation |
| Data Science Lead | Technical investigation; containment implementation; retraining | Leads investigation; implements fix |
| Compliance Officer | Regulatory notification; affected borrower remediation; PIR | Fairness assessment; remediation plan |
| DPO | DPDP Act breach assessment; Data Protection Board notification | Data privacy impact assessment |
| Model Risk Committee | Convened within 4 hours for P1 | Convened within 24 hours for P2 |
| Communications | Stakeholder communication if public disclosure required | Internal communication |

---

## 5. Regulatory Notification Requirements

| Regulation | Trigger | Timeline | Recipient |
|-----------|---------|----------|-----------|
| DPDP Act 2023 Section 8(6) | Personal data breach affecting AI training or scoring data | 72 hours | Data Protection Board of India |
| RBI Digital Lending Guidelines | Material breach of Fair Practices Code — confirmed discrimination | As soon as practicable | RBI Regional Office |
| RBI NBFC Reporting | Material model risk event affecting portfolio quality | Per RBI reporting calendar | RBI Supervisory Portal |
| EU AI Act Article 73 | Serious incident involving High Risk AI system | 15 days (death/serious harm); 3 days (systemic risk) | Market Surveillance Authority |

**Important:** Regulatory notification decisions must involve Legal
counsel. This procedure provides a framework — specific notification
obligations depend on the nature and scope of each incident.

---

## 6. AI Incident Register

All incidents must be logged in the AI Incident Register maintained
by the Compliance team. Minimum fields:

| Field | Description |
|-------|-------------|
| incident_id | Sequential — AI-INC-YYYY-NNN |
| detection_date | Date incident was identified |
| detection_source | How it was found (monitoring/complaint/audit/etc.) |
| severity | P1/P2/P3/P4 |
| model_affected | Model ID from model inventory |
| description | Plain language description of the incident |
| affected_population | Number and characteristics of affected applicants |
| root_cause | Confirmed root cause after investigation |
| containment_action | Action taken to stop ongoing harm |
| permanent_fix | Long-term remediation implemented |
| regulatory_notified | Yes/No — which regulator, when |
| pir_completed | Yes/No — date of PIR |
| lessons_learned | Key findings from PIR |
| status | Open/Contained/Resolved/Closed |

The AI Incident Register is reviewed at every Model Risk Committee
meeting and included in the annual AI governance report to the Board.

---

## 7. Lessons Learned and Continuous Improvement

Every closed incident must feed into at least one of:
- Model risk register update (new or modified risk entry)
- Monitoring threshold adjustment
- Policy or procedure update
- Training requirement
- Model retraining trigger

NIST AI RMF requires that MANAGE feeds back into GOVERN —
this feedback loop is operationalised through the post-incident
review process and the quarterly Model Risk Committee review.

---

*AI Incident Response Procedure v1.0*
*Aligned with: NIST AI RMF MG-4, ISO 42001 Clause 10,*
*DPDP Act 2023 Section 8(6), RBI Digital Lending Guidelines 2022.*
*GRO Shield Independent Governance Assessment, January 2025.*

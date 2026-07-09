# NIST AI Risk Management Framework Assessment
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital.

**Framework:** NIST AI RMF 1.0 (January 2023) + ISO 42001:2023
**Model Assessed:** GRO Score 3.0 (Proxy) — MDL-001
**Version:** 1.0
**Date:** January 2025
**Prepared By:** GRO Shield Independent Governance Assessment

---

## About This Assessment

The NIST AI Risk Management Framework organises AI risk management
into four functions: GOVERN, MAP, MEASURE, and MANAGE. These functions
are not sequential stages but a continuous cycle — each function
informs and enables the others. An AI system that completes this cycle
once at deployment and never revisits it is not compliant with the
framework's intent.

This assessment evaluates GRO Score 3.0 (proxy) against all four
functions, drawing on findings from Modules 1–5 of the GRO Shield
governance assessment. Each function is rated on a maturity scale:

| Maturity Level | Description |
|---------------|-------------|
| 1 — Initial | Ad hoc, undocumented, reactive |
| 2 — Developing | Partially documented, inconsistently applied |
| 3 — Defined | Documented, consistently applied, measurable |
| 4 — Managed | Monitored, measured, proactively improved |
| 5 — Optimising | Continuously improved, industry-leading practice |

---

## Function 1: GOVERN

**Purpose:** Establish the organisational culture, policies, accountability
structures, and processes that enable AI risk management across the
enterprise. GOVERN is the foundation — without it, MAP, MEASURE, and
MANAGE lack institutional support and tend to be performative rather
than effective.

**Overall Maturity: 2 — Developing**

### GV-1: Policies, Processes, and Procedures

**GV-1.1 — AI Risk Policy**

Finding: No publicly disclosed Responsible AI Policy exists for UGRO
Capital as of the assessment date. The organisation publicly describes
itself as a "DataTech NBFC" and discloses that GRO Score uses 25,000+
features, but no corresponding AI governance policy framework is publicly
available.

Assessment: **Gap — Critical**

A Responsible AI Policy is the foundational governance document for any
AI-deploying organisation. Without it, accountability for AI risk is
unclear, staff have no guidance on acceptable AI use, and regulators
have no evidence of intentional governance.

Recommendation: Adopt the Responsible AI Policy developed in this
assessment (see `policies/responsible_ai_policy.md`) as a baseline.

**GV-1.2 — AI Lifecycle Governance**

Finding: No documented AI development lifecycle policy is publicly
available. It is unknown whether UGRO Capital applies structured
governance checkpoints (design review, bias testing, validation sign-off)
before model deployment.

Assessment: **Gap — High**

ISO 42001 Clause 6.1 requires organisations to plan actions to address
AI risks throughout the AI system lifecycle. Without a lifecycle policy,
governance is dependent on individual practitioner judgement rather than
organisational process.

### GV-2: Accountability and Roles

**GV-2.1 — AI Accountability Structure**

Finding: UGRO Capital's public disclosures do not identify a Chief AI
Officer, AI Ethics Committee, or equivalent governance body. The
organisation has a Chief Data Officer function (implied by DataTech
positioning) but its AI risk mandate is not documented.

Assessment: **Gap — High**

NIST AI RMF requires that roles and responsibilities for AI risk
management be defined, assigned, and communicated. Without explicit
accountability, findings from bias audits, model validations, and
compliance assessments have no clear owner.

Recommended accountability structure:

| Role | AI Risk Responsibility |
|------|----------------------|
| Board Risk Committee | Approve AI risk appetite; oversee material AI risks |
| Chief Risk Officer | Own AI risk framework; escalation point |
| Chief Data Officer | Own data governance for AI; data quality and lineage |
| Model Risk Committee | Approve model deployments; review validation findings |
| Data Science Lead | Day-to-day model development and monitoring |
| Compliance Officer | Regulatory mapping; bias audit sign-off |
| Data Protection Officer | DPDP Act obligations; consent management |

**GV-2.2 — Human Oversight**

Finding: GRO Score is described as driving automated credit decisions.
No publicly documented human oversight mechanism exists for borderline
cases, rejected applicants, or model failure scenarios.

Assessment: **Gap — Critical**

NIST AI RMF GV-6.2 requires that human oversight mechanisms be
established for high-risk AI systems. EU AI Act Article 14 mandates
human oversight for High Risk AI systems including credit scoring.
The absence of a documented human-in-the-loop process for an automated
lending decision system is a material governance gap.

### GV-3: Organisational Culture

**GV-3.1 — AI Risk Awareness**

Finding: Cannot be assessed from public information. Assumed developing
based on DataTech positioning.

Assessment: **Assumed Developing**

**GV-3.2 — Incentive Alignment**

Finding: A structural tension exists between UGRO Capital's commercial
incentive to maximise lending volume and the risk management imperative
to maintain model accuracy and fairness. This tension is not unique to
UGRO but must be explicitly managed — particularly given that GRO Score
directly gates loan approvals.

Assessment: **Gap — Medium**

Recommendation: Ensure model risk metrics (AUC, EOD, PSI) are included
in Data Science team performance reviews alongside business metrics.
Separate model validation from model development organisationally.

### GV-4: Organisational Teams

**GV-4.1 — Diverse Teams**

Finding: No information available on diversity of AI development teams.

Assessment: **Cannot Assess**

Note: Team diversity is directly relevant to bias outcomes — homogeneous
teams are less likely to identify bias against groups not represented
on the team. Module 5 found CRITICAL bias findings against Female
proprietors; team gender diversity is a relevant mitigating factor.

### GOVERN Summary

| Sub-function | Finding | Maturity |
|-------------|---------|----------|
| GV-1.1 AI Risk Policy | No policy documented | 1 |
| GV-1.2 Lifecycle Governance | No lifecycle policy | 1 |
| GV-2.1 Accountability | No AI governance structure | 2 |
| GV-2.2 Human Oversight | No human-in-the-loop documented | 1 |
| GV-3.1 Risk Culture | Assumed developing | 2 |
| GV-3.2 Incentive Alignment | Tension not managed | 2 |
| **Overall GOVERN** | | **2 — Developing** |

---

## Function 2: MAP

**Purpose:** Identify, categorise, and contextualise AI risks. MAP
translates the organisational context established in GOVERN into a
specific risk landscape for the AI system in scope. Without MAP,
MEASURE has no defined target and MANAGE has no prioritised risk list.

**Overall Maturity: 2 — Developing**

### MP-1: Context Establishment

**MP-1.1 — Intended Purpose and Context**

GRO Score 3.0 context:

| Dimension | Detail |
|-----------|--------|
| Intended use | MSME credit underwriting — predict probability of default |
| Deployment context | Automated lending decisions at point of application |
| Affected population | MSME proprietors across India seeking business loans |
| Decision stakes | High — approve/reject determines credit access |
| Reversibility | Low — rejected applicants face significant friction to re-apply |
| Scale | Portfolio-wide — all MSME applications processed through model |

**MP-1.2 — AI System Classification**

| Framework | Classification |
|-----------|---------------|
| EU AI Act | High Risk AI System (Annex III, point 5(b) — credit scoring) |
| NIST AI RMF | High impact — automated decisions affecting individuals' financial access |
| RBI | Algorithmic credit decisioning — Fair Practices Code applies |
| ISO 42001 | High risk AI application — enhanced controls required |

**MP-1.3 — Stakeholder Identification**

| Stakeholder | Interest | Potential Harm |
|-------------|---------|----------------|
| MSME applicants | Fair, accurate credit assessment | Wrongful rejection; no explanation |
| Female proprietors | Non-discriminatory evaluation | Systematic bias confirmed in audit |
| Northern state borrowers | Geographic parity | UP/WB/MP systematic under-approval |
| Food Processing sector | Sector parity | 16.6pp over-prediction confirmed |
| UGRO Capital shareholders | Portfolio quality; regulatory compliance | Credit losses; regulatory action |
| RBI | Financial inclusion; fair lending | Systemic geographic exclusion |
| UGRO employees | Clear AI governance guidance | Accountability without support |

### MP-2: Risk Categorisation

**MP-2.1 — Risk Categories Identified**

Five risk categories mapped for GRO Score:

**Category 1 — Data Risk**
Risks arising from the quality, representativeness, and governance
of training and production data.

Key risks: Reject inference bias; training data staleness; feature
data quality degradation; consent gaps for data processing.

**Category 2 — Model Risk**
Risks arising from model design, training, validation, and deployment.

Key risks: Model miscalibration; performance degradation over time;
overfitting; threshold misconfiguration; version control failures.

**Category 3 — Bias and Fairness Risk**
Risks that the model produces discriminatory outcomes for protected
groups. Confirmed findings in Module 5.

Key risks: Gender bias (EOD 0.172); geographic bias (EOD 0.446);
sector bias (EOD 0.225); proxy discrimination; feedback loops.

**Category 4 — Operational Risk**
Risks arising from deployment, monitoring, and incident response.

Key risks: Monitoring gaps; model drift undetected; explainability
failures; human override not available; incident response delays.

**Category 5 — Compliance and Regulatory Risk**
Risks of breaching applicable laws, regulations, and standards.

Key risks: DPDP Act consent gaps; RBI Fair Practices Code breaches;
EU AI Act non-conformity; right-to-explanation failures.

### MP-3: AI Risk Benefit Analysis

**MP-3.1 — Benefits**

GRO Score delivers measurable benefits that must be weighed against
identified risks:

- Consistent, data-driven credit assessment across 25,000+ features
- Reduced processing time vs manual underwriting
- Scalable MSME credit access — supporting financial inclusion goals
- Reduced human cognitive bias in individual underwriting decisions
- Portfolio-level risk management through standardised scoring

**MP-3.2 — Risk-Benefit Balance**

The risk-benefit balance for GRO Score is currently **unfavourable**
in three specific areas:

1. Geographic exclusion: systematic under-approval in UP, WB, MP
   undermines the financial inclusion benefit the model is meant to
   enable — the opposite of the stated purpose
2. Gender disparity: EOD of 0.172 means the model makes systematically
   different errors for Female proprietors — a population that already
   faces structural barriers to MSME credit
3. Sector stereotyping: Food Processing over-prediction (16.6pp gap)
   penalises a sector with genuine economic importance to India's
   food supply chain

These are not arguments against using the model — they are arguments
for remediating specific, identified deficiencies before continuing
to rely on it for high-stakes decisions.

### MAP Summary

| Sub-function | Finding | Maturity |
|-------------|---------|----------|
| MP-1.1 Context | Partially documented | 2 |
| MP-1.2 Classification | High Risk — confirmed | 3 |
| MP-1.3 Stakeholders | Mapped in this assessment | 2 |
| MP-2.1 Risk Categories | 5 categories, 30+ risks | 3 |
| MP-3.1 Benefits | Documented | 3 |
| MP-3.2 Risk-Benefit | Unfavourable in 3 areas | 2 |
| **Overall MAP** | | **2 — Developing** |

---

## Function 3: MEASURE

**Purpose:** Analyse, assess, and quantify AI risks identified in MAP.
MEASURE produces the evidence base for MANAGE decisions. It is where
governance meets engineering — technical metrics must be translated
into risk language that decision-makers can act on.

**Overall Maturity: 3 — Defined**

MEASURE is the highest-maturity function in this assessment because
Modules 1–5 have directly produced MEASURE outputs: DQ scorecard,
fairness metrics, PSI monitoring, SHAP explainability, and model
performance metrics.

### MS-1: AI Risk Analysis

**MS-1.1 — Model Performance Measurement**

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| AUC-ROC | 0.8051 | ≥ 0.75 | ✅ Pass |
| Average Precision | 0.4005 | 2× base rate | ✅ Pass |
| Default Recall | 0.59 | ≥ 0.60 | ⚠ Below target |
| False Negative Rate | 41% | < 35% | ⚠ Elevated |

**MS-1.2 — Data Quality Measurement**

From Module 1 DQ Assessment:

| Dimension | Score | Status |
|-----------|-------|--------|
| Completeness | 98.2/100 | ✅ |
| Validity | 97.8/100 | ✅ |
| Consistency | 96.9/100 | ✅ |
| Accuracy | 97.1/100 | ✅ |
| Timeliness | 96.4/100 | ✅ |
| Uniqueness | 99.1/100 | ✅ |
| **Overall DQ Score** | **97.4/100** | ✅ |

**MS-1.3 — Fairness Measurement**

From Module 5 Bias Audit:

| Attribute | DPD | EOD | Four-Fifths | Severity |
|-----------|-----|-----|-------------|----------|
| proprietor_gender | 0.086 | 0.172 | Breach | CRITICAL |
| state | 0.103 | 0.446 | Breach | CRITICAL |
| sector | 0.095 | 0.225 | Breach | CRITICAL |

**MS-1.4 — Drift Measurement**

From Module 4 PSI Dashboard (simulated production, drift strength 0.3):

| Feature | PSI | Status |
|---------|-----|--------|
| dpd_90_count_12m | 0.2203 | 🔴 CRITICAL |
| bounce_count_6m | 0.1179 | 🟡 WARNING |
| All others | < 0.10 | 🟢 STABLE |

**MS-1.5 — Explainability Measurement**

From Module 5 SHAP Analysis:

| Finding | Value | Implication |
|---------|-------|------------|
| Bureau score SHAP dominance | 1.131 (6× next feature) | Model primarily bureau-driven — appropriate |
| Bureau score SHAP correlation | -0.943 | Clean negative relationship — correct usage |
| Protected attributes in top 20 | 0 | No direct discrimination |
| Discrimination mechanism | Distributional confounding | Indirect — harder to remediate |

### MS-2: AI Risk Prioritisation

Risk prioritisation matrix — likelihood × impact:

| Risk | Likelihood | Impact | Priority |
|------|-----------|--------|----------|
| Geographic bias (state EOD 0.446) | High | High | 🔴 Critical |
| Gender bias (EOD 0.172) | High | High | 🔴 Critical |
| Sector bias (EOD 0.225) | High | Medium | 🔴 Critical |
| DPD-90 drift (PSI 0.220) | Medium | High | 🔴 Critical |
| Reject inference bias | High | Medium | 🟠 High |
| Default recall below target | High | Medium | 🟠 High |
| No right-to-explanation process | High | Medium | 🟠 High |
| DPDP Act consent gaps | Medium | High | 🟠 High |
| No human oversight mechanism | Medium | High | 🟠 High |
| Model retraining triggers undefined | Medium | Medium | 🟡 Medium |

### MEASURE Summary

| Sub-function | Finding | Maturity |
|-------------|---------|----------|
| MS-1.1 Model Performance | Measured — 1 below threshold | 3 |
| MS-1.2 Data Quality | Measured — 97.4/100 | 4 |
| MS-1.3 Fairness | Measured — 3 CRITICAL | 3 |
| MS-1.4 Drift | Measured — 1 CRITICAL | 3 |
| MS-1.5 Explainability | Measured — SHAP complete | 3 |
| MS-2 Risk Prioritisation | Prioritised — 4 Critical | 3 |
| **Overall MEASURE** | | **3 — Defined** |

---

## Function 4: MANAGE

**Purpose:** Prioritise and implement risk treatments, maintain ongoing
monitoring, and feed learnings back into GOVERN. MANAGE is where
governance produces action — without it, MEASURE produces findings
that sit in reports and change nothing.

**Overall Maturity: 2 — Developing**

### MG-1: Risk Treatment

**MG-1.1 — Treatment Options**

For each risk, four treatment options exist:

- **Mitigate** — reduce likelihood or impact through controls
- **Transfer** — share risk with a third party (insurance, vendor SLA)
- **Accept** — formally accept residual risk within defined appetite
- **Avoid** — discontinue the activity generating the risk

For GRO Score, the primary treatment strategy is **mitigate** —
the model delivers genuine business value and the risks are addressable
through technical and process controls. Avoidance is not warranted.
Acceptance is appropriate for residual risks after mitigation, but
must be formally documented and Board-approved.

**MG-1.2 — Treatment Plan Summary**

| Risk | Treatment | Action | Timeline |
|------|-----------|--------|----------|
| Gender bias | Mitigate | Fairness-constrained retraining (G3) | 1–3 months |
| State bias | Mitigate | Replace state dummies with economic indicators (S3) | 1–3 months |
| Sector bias | Mitigate | Replace sector dummies with risk indices (T2) | 1–3 months |
| DPD-90 drift | Mitigate | PSI monitoring with automated alerts | Immediate |
| Reject inference | Mitigate | Annual reject inference study | 6 months |
| No right-to-explanation | Mitigate | SHAP-based rejection letter process | 2 months |
| DPDP consent gaps | Mitigate | Consent management system (Module 3) | Immediate |
| No human oversight | Mitigate | Human review mandate for borderline cases | Immediate |

### MG-2: Residual Risk

**MG-2.1 — Residual Risk After Treatment**

Even after all planned mitigations are implemented, residual risks remain:

| Residual Risk | Rationale | Residual Level |
|--------------|-----------|----------------|
| Reject inference bias | No outcome data for rejected applicants — structurally unresolvable without reject inference study | Medium |
| Proxy discrimination | Even after removing direct protected attributes, correlated features may persist as proxies | Low-Medium |
| Model performance degradation | Economic conditions change; model may underperform in stress scenarios not represented in training | Medium |
| Regulatory change | DPDP Rules 2025 still being finalised; AI regulation evolving rapidly | Low-Medium |

**MG-2.2 — Residual Risk Acceptance**

Residual risks must be formally accepted by the Board Risk Committee
with documented rationale. Acceptance is not the same as ignoring —
it is a deliberate, documented decision that the residual risk is
within the organisation's risk appetite and that the benefits of
continuing to use the model outweigh the remaining risks.

### MG-3: Monitoring and Review

**MG-3.1 — Ongoing Monitoring Plan**

| Activity | Frequency | Owner | Tool |
|----------|-----------|-------|------|
| PSI drift monitoring | Monthly | Data Science | Module 4 dashboard |
| Fairness metrics review | Quarterly | Compliance + Data Science | Fairlearn |
| Model performance review | Quarterly | Model Risk Committee | Metrics dashboard |
| Full bias audit | Annual | External/Internal audit | Fairlearn + SHAP |
| Independent model validation | Annual | Independent validator | Full MRM review |
| DPDP compliance review | Annual | DPO + Compliance | Module 3 framework |

**MG-3.2 — Model Retraining Triggers**

The following conditions should trigger mandatory model review
and potential retraining:

- PSI > 0.20 on any of the top 5 features for two consecutive months
- AUC-ROC drops below 0.75 on quarterly outcome validation
- EOD exceeds 0.20 for any protected attribute on quarterly review
- Material change in RBI regulatory requirements
- Significant economic shock (rate cycle change, sector-level stress)
- Portfolio default rate deviates more than 5pp from model predictions

### MG-4: AI Incident Response

**MG-4.1 — Incident Classification**

See `incident_response/ai_incident_response.md` for full procedure.

Summary classification:

| Severity | Definition | Response Time |
|----------|-----------|---------------|
| P1 — Critical | Model producing discriminatory outcomes at scale; regulatory breach confirmed | 4 hours |
| P2 — High | Significant performance degradation; PSI CRITICAL on key features | 24 hours |
| P3 — Medium | Individual explainability failure; data quality issue affecting scoring | 72 hours |
| P4 — Low | Documentation gap; monitoring alert without confirmed impact | 5 business days |

### MANAGE Summary

| Sub-function | Finding | Maturity |
|-------------|---------|----------|
| MG-1.1 Treatment Options | Framework defined | 3 |
| MG-1.2 Treatment Plan | 8 treatments planned | 3 |
| MG-2.1 Residual Risk | 4 residual risks identified | 3 |
| MG-2.2 Residual Risk Acceptance | Process not yet formalised | 2 |
| MG-3.1 Monitoring | Plan defined; partially implemented | 3 |
| MG-3.2 Retraining Triggers | Defined in this assessment | 2 |
| MG-4.1 Incident Response | Classified; procedure documented | 3 |
| **Overall MANAGE** | | **2 — Developing** |

---

## Overall Assessment Summary

| Function | Maturity | Key Gap |
|----------|----------|---------|
| GOVERN | 2 — Developing | No AI policy; no accountability structure; no human oversight |
| MAP | 2 — Developing | Risk landscape mapped in this assessment; not institutionalised |
| MEASURE | 3 — Defined | Strong technical measurement; 3 CRITICAL fairness findings |
| MANAGE | 2 — Developing | Treatment plans defined; residual risk acceptance not formalised |
| **Overall** | **2 — Developing** | Governance infrastructure absent; technical capability present |

**Headline finding:** UGRO Capital's GRO Score presents a profile common
to technically sophisticated but governance-immature AI deployments —
strong model engineering (AUC 0.805, bureau score dominance confirmed
by SHAP) combined with significant governance gaps (no AI policy, no
accountability structure, CRITICAL bias findings unaddressed). The
technical capability to build and deploy a credit scoring model at scale
is present; the organisational infrastructure to govern it responsibly
is not yet established.

---

## ISO 42001 Alignment

ISO 42001:2023 is the AI Management System standard, complementing
NIST AI RMF with a Plan-Do-Check-Act management system framework.

| ISO 42001 Clause | Requirement | GRO Shield Assessment |
|-----------------|-------------|----------------------|
| 4.1 Organisational context | Understand internal/external issues affecting AI | Partially addressed — DataTech positioning documented |
| 5.1 Leadership commitment | Top management demonstrate AI governance commitment | Gap — no public evidence of board-level AI governance |
| 6.1 Risk planning | Plan actions to address AI risks | Gap — no documented risk planning process |
| 6.2 AI objectives | Establish measurable AI governance objectives | Gap — no published AI objectives |
| 7.2 Competence | Ensure AI team competence | Cannot assess |
| 8.4 AI system impact assessment | Assess impacts before deployment | Gap — no DPIA/AISIA documented at deployment |
| 9.1 Monitoring and measurement | Monitor AI system performance | Partial — PSI dashboard implemented in this assessment |
| 10.1 Nonconformity | Address nonconformities | Gap — no nonconformity process documented |

---

*Assessment based on NIST AI RMF 1.0 (January 2023) and ISO 42001:2023.*
*GRO Shield Independent Governance Assessment, January 2025.*

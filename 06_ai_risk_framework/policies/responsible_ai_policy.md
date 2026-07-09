# Responsible AI Policy
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital. This policy is a governance recommendation, not a
> statement of UGRO Capital's actual policies.

**Version:** 1.0
**Effective Date:** 1 January 2025
**Next Review:** 1 January 2026
**Owner:** Chief Risk Officer
**Approved By:** Board Risk Committee (recommended)

---

## 1. Purpose and Scope

### 1.1 Purpose
This Responsible AI Policy establishes the principles, standards, and
accountability structures governing the development, deployment, and
monitoring of artificial intelligence and machine learning systems at
UGRO Capital. It translates UGRO Capital's commitment to responsible
lending into specific obligations for AI systems that influence credit
decisions affecting MSME borrowers across India.

### 1.2 Scope
This policy applies to:
- All AI and ML models used in credit underwriting, including GRO Score
- All data systems that feed AI models (bureau, banking, GST data)
- All teams involved in AI development, deployment, and monitoring
- Third-party AI systems or data providers used in credit decisioning
- Future AI applications including customer-facing systems

### 1.3 Relationship to Other Policies
This policy operates alongside and should be read with:
- Data Classification Policy (Module 2)
- DPDP Act Compliance Framework (Module 3)
- Model Risk Management Policy (Module 4)
- AI Incident Response Procedure (Module 6)

---

## 2. AI Principles

UGRO Capital's AI systems must embody six core principles. These are
not aspirational — they are operational requirements with associated
controls, metrics, and accountability.

### Principle 1: Fairness
AI systems must not discriminate against individuals or groups on the
basis of gender, geography, religion, caste, community, or other
protected characteristics — either directly through explicit feature
use or indirectly through correlated proxy features.

**Operational requirement:** All credit scoring models must pass
fairness testing before deployment and on a quarterly basis in
production. Equalized Odds Difference must be below 0.10 for gender
and 0.15 for geographic attributes. CRITICAL bias findings must be
remediated within 90 days of identification.

### Principle 2: Transparency
AI systems must be explainable to the individuals they affect. MSME
borrowers who are rejected must be able to understand the primary
factors that influenced their assessment.

**Operational requirement:** SHAP-based explanations must be generated
for all credit decisions. Rejection communications must include the
top 3 factors contributing to the decision in plain language. A formal
right-to-explanation process must be maintained by the Compliance team.

### Principle 3: Accountability
Responsibility for AI outcomes must be clearly assigned. Every AI
system must have a named model owner, a named compliance owner, and
Board Risk Committee oversight. No AI system may be deployed without
documented accountability.

**Operational requirement:** Model inventory register must be maintained
with named owners for all production models. Model Risk Committee must
meet quarterly to review open findings. Board Risk Committee must
receive annual AI governance report.

### Principle 4: Safety and Reliability
AI systems must perform reliably within defined parameters. Performance
degradation, data drift, and model failure must be detected and
addressed before they cause harm to borrowers or portfolio quality.

**Operational requirement:** PSI monitoring must run monthly for all
production credit models. AUC-ROC must be validated quarterly against
realised outcomes. Retraining triggers must be defined and enforced.
A human review mechanism must exist for borderline cases.

### Principle 5: Privacy
AI systems must process personal data only with valid consent, for
legitimate purposes, with appropriate security, and in compliance with
the DPDP Act 2023 and applicable RBI data governance requirements.

**Operational requirement:** A Records of Processing Activities register
must be maintained for all AI-related data processing. Consent must be
obtained per category of data processing. Data minimisation must be
applied — features must be justified by predictive value, not collected
by default.

### Principle 6: Human Oversight
High-risk AI decisions must be subject to meaningful human oversight.
Fully automated decisions that materially affect individuals' financial
access require defined escalation paths and human review mechanisms.

**Operational requirement:** All applications with predicted default
probability between 0.35 and 0.65 must receive human underwriter
review before final decision. All rejected applications must have an
accessible appeals process. No model may be deployed in a fully
automated mode without Board Risk Committee approval.

---

## 3. AI Risk Governance Structure

### 3.1 Board Risk Committee
**Responsibilities:**
- Approve AI risk appetite statement annually
- Receive annual AI governance report
- Approve residual risk acceptance for Critical AI risks
- Make explicit policy decisions on fairness criteria
  (demographic parity vs equalized odds vs calibration)

### 3.2 Chief Risk Officer
**Responsibilities:**
- Own this Responsible AI Policy
- Chair Model Risk Committee
- Escalation point for P1 AI incidents
- Sign off on material model deployments

### 3.3 Chief Data Officer
**Responsibilities:**
- Own data quality, lineage, and classification for AI systems
- Maintain data catalogue and business glossary
- Oversee DPDP Act compliance for data processing

### 3.4 Model Risk Committee
**Responsibilities:**
- Review and approve all new model deployments
- Oversee independent model validation programme
- Review open model risk findings quarterly
- Approve model retraining decisions

**Composition:** CRO (Chair), CDO, Head of Data Science,
Head of Compliance, Head of Credit Risk, Independent Member

**Meeting frequency:** Quarterly (minimum); ad hoc for P1/P2 incidents

### 3.5 Data Science Team
**Responsibilities:**
- Implement fairness testing before every model deployment
- Maintain PSI monitoring dashboard
- Produce model cards for all production models
- Remediate technical model risk findings within agreed timelines

### 3.6 Compliance Team
**Responsibilities:**
- Map AI systems against regulatory requirements
- Sign off bias audit findings
- Maintain right-to-explanation process
- Conduct DPDP Act compliance reviews

### 3.7 Data Protection Officer
**Responsibilities:**
- Oversee DPDP Act consent management
- Conduct Data Protection Impact Assessments for new AI systems
- Manage data breach response for AI-related incidents
- Liaison with Data Protection Board of India

---

## 4. AI Lifecycle Requirements

Every AI system at UGRO Capital must pass through defined governance
checkpoints at each lifecycle stage.

### Stage 1: Concept and Design
Before any model development begins:
- [ ] Business case documented with intended use and affected population
- [ ] Stakeholder impact assessment completed
- [ ] Data sources identified and consent basis confirmed
- [ ] Preliminary risk classification (High / Medium / Low)
- [ ] CDO sign-off on data access

### Stage 2: Development
During model development:
- [ ] Data quality assessment completed (DQ score ≥ 90/100)
- [ ] Training data bias assessment — protected attribute distribution documented
- [ ] Feature selection justified by predictive value and data minimisation
- [ ] Model card drafted
- [ ] Version control applied from first commit

### Stage 3: Pre-Deployment Validation
Before any production deployment:
- [ ] Independent model validation completed
- [ ] Fairness testing passed (EOD < 0.10 gender, < 0.15 geographic)
- [ ] SHAP explainability analysis completed
- [ ] PSI monitoring configured and tested
- [ ] Human oversight mechanism documented
- [ ] Right-to-explanation process ready
- [ ] Compliance sign-off obtained
- [ ] Model Risk Committee approval obtained
- [ ] Model inventory register updated

### Stage 4: Production Monitoring
After deployment:
- [ ] PSI monitoring running monthly
- [ ] Fairness metrics reviewed quarterly
- [ ] Model performance validated against realised outcomes quarterly
- [ ] Annual independent validation scheduled
- [ ] Annual bias audit scheduled

### Stage 5: Retirement
Before model decommissioning:
- [ ] Replacement model has completed Stage 3
- [ ] Historical model outputs retained per data retention policy
- [ ] Regulatory notification if required
- [ ] Model inventory register updated with retirement date

---

## 5. Prohibited Uses of AI

The following uses of AI are explicitly prohibited at UGRO Capital:

1. **Direct use of protected characteristics** — AI models must not use
   gender, religion, caste, community, or political affiliation as direct
   input features in credit scoring or any other decision system

2. **Fully automated adverse decisions without appeal** — any AI system
   that makes a decision materially adverse to an individual must have
   an accessible human appeals process

3. **AI systems without documented accountability** — no AI system may
   be deployed without a named model owner and compliance owner in the
   model inventory register

4. **Processing sensitive personal data without consent** — financial,
   biometric, or health data may not be processed for AI purposes without
   explicit, granular consent under DPDP Act 2023

5. **Deploying a model with open Critical findings** — no model with an
   unresolved Critical finding in the model inventory register may be
   deployed or continue in production without Board Risk Committee
   explicit approval and documented risk acceptance

---

## 6. Fairness Standards

### 6.1 Quantitative Thresholds

| Metric | Protected Attribute | Pass Threshold |
|--------|--------------------|--------------:|
| Equalized Odds Difference | Gender | < 0.10 |
| Equalized Odds Difference | State/Geography | < 0.15 |
| Equalized Odds Difference | Sector | < 0.12 |
| Four-Fifths Rule | All attributes | > 0.80 |
| Demographic Parity Difference | All attributes | < 0.10 |

### 6.2 Fairness Criterion Policy
The Board Risk Committee must make and document an explicit decision
on which fairness criterion takes precedence when criteria conflict
(as they mathematically must when base rates differ across groups).
This decision must be:
- Reviewed annually
- Documented in board minutes
- Communicated to the Data Science team as a design constraint
- Disclosed to regulators on request

### 6.3 Proxy Discrimination Testing
Removing protected attributes from model features is necessary but
not sufficient. All models must also be tested for proxy discrimination
— whether correlated features (sector, geography, vintage) produce
disparate outcomes for protected groups even in the absence of direct
protected attribute use.

---

## 7. Regulatory Compliance Obligations

| Regulation | Key Obligation | Owner |
|-----------|---------------|-------|
| DPDP Act 2023 | Consent management; right to erasure; breach notification within 72 hours | DPO |
| DPDP Rules 2025 | Data fiduciary obligations; consent manager framework | DPO + Legal |
| RBI Digital Lending Guidelines 2022 | Fair Practices Code; grievance redressal; no discriminatory pricing | Compliance |
| RBI NBFC Master Direction | Model risk management; independent validation | Model Risk Committee |
| EU AI Act | High Risk AI conformity assessment; transparency; human oversight | Compliance + Legal |
| ISO 42001:2023 | AI management system; risk planning; competence; monitoring | CDO + CRO |

---

## 8. Policy Breach and Escalation

### 8.1 Breach Classification

| Breach Type | Example | Response |
|-------------|---------|----------|
| Critical | Deploying model with open Critical bias finding without Board approval | Immediate escalation to CRO and Board; potential model suspension |
| High | Failure to conduct quarterly fairness review | Escalation to Model Risk Committee; 30-day remediation plan |
| Medium | Model card not updated after retraining | Escalation to CDO; 14-day remediation |
| Low | Documentation gap with no immediate risk | Logged in risk register; next review cycle |

### 8.2 Whistleblower Protection
Staff who raise concerns about AI governance breaches in good faith
are protected from retaliation under UGRO Capital's whistleblower
policy. Concerns may be raised directly with the CRO, DPO, or
through the anonymous reporting channel.

---

## 9. Training and Awareness

All staff involved in AI development, deployment, or oversight must
complete:
- AI ethics and governance awareness training (annual)
- DPDP Act data protection training (annual)
- Role-specific technical training (Data Science: fairness testing,
  SHAP; Compliance: bias audit interpretation; Risk: model risk metrics)

---

## 10. Policy Review

This policy must be reviewed:
- Annually by the Model Risk Committee
- Following any material regulatory change
- Following any P1 AI incident
- Following any material change to the AI system landscape

---

*Responsible AI Policy v1.0 — GRO Shield Independent Governance Assessment*
*Aligned with: NIST AI RMF 1.0, ISO 42001:2023, EU AI Act,*
*DPDP Act 2023, RBI Digital Lending Guidelines 2022.*

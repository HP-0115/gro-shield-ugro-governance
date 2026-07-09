# Communication and Training Framework
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital.

**Version:** 1.0
**Date:** July 2026
**Prepared By:** GRO Shield Independent Governance Assessment

---

## Framework Philosophy

Governance communication fails in two predictable ways:

**Too technical for the audience** — bias audit reports written
for data scientists get forwarded to the CRO who reads the first
page and files it. Risk registers with 32 rows get reviewed once
and never opened again. The finding never becomes action.

**Too vague for the audience** — high-level governance principles
communicated to the Data Science team produce no behaviour change
because there is no operational content to act on. "We are
committed to responsible AI" is not a sprint ticket.

This framework matches message, format, and frequency to audience —
so that every stakeholder receives governance information in the
form they can act on, at the cadence that keeps it current without
creating noise.

---

## 1. Stakeholder Communication Matrix

### 1.1 Board Risk Committee

**What they need to know:**
- Is our AI governance adequate to protect the organisation from
  regulatory, financial, and reputational risk?
- Are we aware of our material AI risks and are they being managed?
- Are we meeting our obligations under DPDP Act, RBI, and EU AI Act?

**What they do not need:**
- AUC-ROC scores, PSI values, or SHAP importance rankings
- Technical implementation details of the consent management system
- Feature engineering decisions in the bias remediation

**Communication format:**
Annual AI Governance Report — maximum 10 pages, structured as:
1. Executive summary — 3 critical risks and their status (1 page)
2. Regulatory compliance status — traffic light per framework (1 page)
3. Model risk summary — AUC, bias findings in plain language (2 pages)
4. Incidents and near-misses in the past 12 months (1 page)
5. Governance maturity trajectory — where we were, where we are,
   where we are going (2 pages)
6. Decisions required from the Board (1 page)
7. Investment summary (1 page)

**Frequency:** Annual report + ad hoc for P1 incidents and
material regulatory changes

**Tone:** Risk-focused, decisive, outcome-oriented. The Board
needs to make decisions, not understand methodology.

**Sample message (bias findings):**
"Our independent bias audit identified that the GRO Score model
produces systematically higher rejection rates for Female proprietors
and borrowers in Uttar Pradesh, West Bengal, and Madhya Pradesh
than their actual credit risk justifies. This creates regulatory
exposure under RBI Fair Practices Code. We have implemented interim
controls and a 90-day remediation plan. Board approval is requested
for the fairness criterion policy decision outlined in Appendix A."

---

### 1.2 Chief Risk Officer

**What they need to know:**
- Which AI risks are Critical and what is being done about them?
- What is our regulatory exposure and timeline for closure?
- What decisions require CRO authority?
- Are we within risk appetite on model performance and fairness?

**Communication format:**

*Monthly:* AI Risk Dashboard — one page
- PSI status (STABLE/WARNING/CRITICAL per feature)
- Open Critical findings count and days-open
- Fairness metrics — traffic light (pass/breach per attribute)
- Incidents in the month

*Quarterly:* Model Risk Committee pack — 5–8 pages
- Full AI risk register review — new risks, closed risks, changes
- Model performance metrics vs thresholds
- Fairness metrics with trend
- Remediation plan status update
- Decisions required

*Immediate:* P1/P2 incident briefing — verbal + 1-page summary
within 4 hours (P1) or 24 hours (P2)

**Tone:** Risk-quantified, action-oriented. The CRO thinks in
likelihood × impact. Frame findings accordingly: "The state bias
finding (EOD 0.446) has High likelihood of regulatory examination
and High impact if found — this is our highest-priority open risk."

---

### 1.3 Chief Data Officer

**What they need to know:**
- Is our data infrastructure meeting governance standards?
- What is the status of the data catalogue, lineage, and quality?
- What technical governance work is scheduled and resourced?
- How does our governance maturity compare to industry standards?

**Communication format:**

*Monthly:* Data Governance Dashboard — 2 pages
- DQ scorecard (current vs baseline 97.4/100)
- Data catalogue completeness — assets documented vs total
- PSI monitoring status
- Open data quality findings

*Quarterly:* Governance Programme Status — 5 pages
- Phase progress vs roadmap
- Technical remediation status (bias, DPDP, monitoring)
- Resource utilisation vs plan
- Upcoming governance milestones

*Annual:* NIST AI RMF maturity re-assessment — shared with CRO
and Board

**Tone:** Technical and strategic. The CDO speaks both languages —
can receive PSI values and AUC scores, but also needs the
strategic narrative for Board and investor conversations.

---

### 1.4 Data Science Team

**What they need to know:**
- What governance requirements apply to their current sprint?
- What tools and templates are available to make governance easier?
- What are the technical specifications for fairness testing and
  monitoring?
- When do governance checkpoints occur in the delivery cycle?

**Communication format:**

*Sprint-embedded:* Governance checklist in sprint planning —
which governance actions are in scope for this sprint?
Not a separate communication — embedded in existing tooling
(Jira ticket, GitHub PR checklist, or equivalent).

*Monthly:* Technical governance sync — 30-minute working session
- PSI dashboard review — anything drifting?
- Fairness metrics — any approaching breach?
- Open technical model risk findings — status?
- Upcoming governance milestones in next 30 days

*As needed:* Technical deep-dive sessions
- SHAP interpretation workshop
- Fairlearn metrics walkthrough
- Bias-constrained retraining methodology
- PSI threshold calibration

**Tone:** Technical, peer-to-peer, tool-focused. The Data Science
team responds to concrete technical content, not governance
abstractions. Lead with the code, not the policy.

**Sample message (bias findings):**
"The Module 5 audit confirmed EOD 0.172 for gender — above our
0.10 threshold. Root cause is distributional confounding, not
direct discrimination (SHAP confirms gender dummies not in top 20).
The fix is fairness-constrained retraining using Fairlearn's
ExponentiatedGradient with EqualizedOdds constraint. Expected
AUC trade-off: 1–2pp. This is a Board-approved design decision,
not a model failure. Ticket in backlog — target sprint 14."

---

### 1.5 Compliance Team

**What they need to know:**
- What are our regulatory obligations and are we meeting them?
- What is the plain-language interpretation of technical findings?
- What actions are required of the Compliance team specifically?
- What is our regulatory notification status?

**Communication format:**

*Monthly:* Compliance status report — 2 pages
- DPDP Act gap closure status — 15 gaps, 4 critical, RAG status
- RBI Fair Practices Code exposure — bias finding status
- Consent management system metrics
- Right-to-explanation process metrics (when live)

*Quarterly:* Regulatory horizon scan — 1 page
- New or updated regulations affecting AI in NBFC lending
- DPDP Rules 2025 developments
- RBI guidance updates
- EU AI Act implementation timeline

*As needed:* Plain-language translation sessions
- "What does EOD 0.172 mean for our RBI Fair Practices Code
  obligations?" (Answer: the model makes systematically different
  errors for Female proprietors — this is the definition of
  unequal treatment under the Fair Practices Code)
- "What triggers a DPDP Act breach notification?" (Answer:
  any personal data breach — including inadvertent PII disclosure
  in AI model outputs — requires notification within 72 hours)

**Tone:** Regulatory, plain-language, action-specific. The Compliance
team needs to know what the regulation says, what we are doing
about it, and what they need to sign off on — not how gradient
boosting works.

---

### 1.6 Business and Sales Team

**What they need to know:**
- How does governance affect their approval rates and targets?
- What market opportunities does bias remediation open up?
- What is the regulatory risk of not addressing these findings?
- What, specifically, is being asked of them?

**Communication format:**

*One-time:* Business impact briefing — 30 minutes + 2-page summary
Delivered before Phase 1 implementation begins.
Content:
- What the bias findings mean in business terms (not EOD values)
- Market opportunity in under-served segments (Delhi, Food Processing,
  Female proprietors)
- Regulatory risk scenario — what happens if RBI finds this first
- What governance asks of the Business team (almost nothing
  operationally — governance is largely invisible to them)

*Quarterly:* Business governance update — 1 page
- Approval rate trends by segment — showing bias remediation impact
- Regulatory status — traffic light
- Any business-facing process changes

*As needed:* Escalation briefing if regulatory risk increases

**Tone:** Commercial, outcomes-focused, regulatory risk-framed.
Never lead with methodology. Always lead with business impact.

**Sample message (bias findings — business version):**
"Our credit model is currently rejecting a significant proportion
of Delhi MSME applicants despite Delhi having one of the lowest
actual default rates of any state we lend in. We're leaving
creditworthy borrowers on the table in one of India's highest-
value MSME markets. The bias remediation programme fixes this —
it's a growth initiative as much as a governance one."

---

## 2. Communication Channels and Cadence

| Audience | Channel | Frequency | Format |
|----------|---------|-----------|--------|
| Board Risk Committee | Board pack + annual report | Annual + ad hoc | PDF report |
| CRO | Risk dashboard + MRC pack | Monthly + quarterly | Dashboard + slides |
| CDO | Governance dashboard + programme update | Monthly + quarterly | Dashboard + doc |
| Data Science | Sprint checklist + monthly sync | Per sprint + monthly | Ticket + meeting |
| Compliance | Compliance status report + horizon scan | Monthly + quarterly | Document |
| Business/Sales | Business impact briefing + quarterly update | One-time + quarterly | Slide deck |
| All staff | AI governance awareness | Annual training | e-learning |

---

## 3. Training Framework

### 3.1 Training by Role

**All staff — AI Governance Awareness (Annual, 1 hour)**

Content:
- What is AI governance and why does it matter at UGRO Capital?
- What is GRO Score and how does it work (non-technical)?
- What are our obligations under DPDP Act 2023?
- What to do if you suspect an AI governance issue?
- How to raise concerns (whistleblower process)

Format: e-learning module, completion tracked by HR
Assessment: 10-question quiz, 80% pass mark required

**Data Science Team — Technical Governance (Annual, 4 hours)**

Module 1 (1 hour): Fairness metrics — demographic parity,
equalized odds, four-fifths rule. How to run Fairlearn.
How to interpret findings. What constitutes a breach.

Module 2 (1 hour): SHAP explainability — how to run
TreeExplainer, how to interpret global importance, how to
identify direct vs proxy discrimination.

Module 3 (1 hour): PSI monitoring — how to calculate PSI,
how to interpret thresholds, when to escalate.

Module 4 (1 hour): Model card completion — mandatory fields,
how to document limitations honestly, how to update after
retraining.

Format: Workshop led by Data Science Lead or external trainer
Assessment: Complete a model card and bias audit for a
practice dataset

**Compliance Team — AI Regulatory Mapping (Annual, 3 hours)**

Module 1 (1 hour): DPDP Act 2023 for AI systems — consent
requirements, breach notification, right to explanation,
data minimisation.

Module 2 (1 hour): RBI Fair Practices Code — non-discrimination
requirements, grievance redressal, what triggers a regulatory
obligation.

Module 3 (1 hour): Reading technical findings — how to interpret
bias audit outputs, PSI reports, and model performance metrics
without a data science background.

Format: Workshop led by DPO + external legal counsel
Assessment: Regulatory scenario exercise — given a set of
findings, identify the regulatory obligations and actions

**Model Risk Committee — AI Risk Governance (Annual, 2 hours)**

Content:
- NIST AI RMF — four functions and how they apply to UGRO Capital
- How to read the AI risk register
- Model validation — what to look for in a validation report
- Incident response — roles and responsibilities
- Board reporting — what to escalate and how

Format: Facilitated workshop
Assessment: Tabletop incident response exercise

**CRO and CDO — Executive AI Governance (Annual, 1 hour)**

Content:
- AI governance maturity — where UGRO Capital is and where
  it needs to be
- Regulatory landscape — DPDP Act, RBI, EU AI Act, NIST AI RMF
- Key decisions requiring Board or executive approval
- How to read the annual AI governance report

Format: One-on-one briefing with Governance Lead
Assessment: None — executive awareness, not skills training

### 3.2 Training Calendar

| Month | Training Event | Audience |
|-------|---------------|----------|
| January | AI Governance Awareness (all staff) | All staff |
| February | Technical Governance Workshop | Data Science |
| March | AI Regulatory Mapping | Compliance |
| April | Model Risk Committee Governance | MRC members |
| May | Executive AI Governance Briefing | CRO, CDO |
| Ongoing | New joiner onboarding — AI governance module | New staff |
| October | Annual refresher — regulatory updates | Compliance + Data Science |

### 3.3 Training Effectiveness Measurement

| Metric | Measurement Method | Target |
|--------|-------------------|--------|
| Training completion rate | HR learning management system | 100% of mandatory roles |
| Assessment pass rate | Quiz/exercise scores | ≥ 80% |
| Governance incident rate | AI incident register | Decreasing year-on-year |
| Time to escalate AI issues | Incident log — detection to escalation | P1: < 1 hour |
| Bias audit findings addressed on time | Model risk register | 100% within SLA |

---

## 4. Governance Reporting Calendar

| Report | Audience | Frequency | Owner | Due Date |
|--------|----------|-----------|-------|----------|
| AI Risk Dashboard | CRO | Monthly | Data Science | 5th of month |
| Data Governance Dashboard | CDO | Monthly | CDO Office | 5th of month |
| Compliance Status Report | Compliance | Monthly | DPO | 10th of month |
| PSI Monitoring Report | Data Science + CRO | Monthly | Data Science | 15th of month |
| Model Risk Committee Pack | MRC | Quarterly | CRO | 2 weeks before MRC |
| Governance Programme Update | CDO | Quarterly | Governance Lead | Quarter end |
| Regulatory Horizon Scan | Compliance | Quarterly | DPO + Legal | Quarter end |
| Annual AI Governance Report | Board | Annual | CRO + CDO | January |
| Annual Bias Audit | Board + MRC | Annual | Data Science + External | Q1 |
| Annual Model Validation | MRC | Annual | External validator | Q2 |

---

## 5. Measuring Governance Adoption

Governance adoption is measured across three dimensions:

**Process adoption** — are the governance processes being followed?

| Metric | Target | Measurement |
|--------|--------|-------------|
| Pre-deployment checklist completion | 100% of model releases | Sprint tracking |
| Monthly PSI review completion | 12/12 per year | Dashboard logs |
| Quarterly fairness review completion | 4/4 per year | Compliance log |
| Model card currency | Updated within 30 days of retraining | Model inventory |

**Outcome improvement** — is governance producing better AI outcomes?

| Metric | Baseline | Target (12 months) |
|--------|----------|-------------------|
| Gender EOD | 0.172 | < 0.10 |
| State EOD | 0.446 | < 0.15 |
| Sector EOD | 0.225 | < 0.12 |
| DPDP gaps open | 15 (4 critical) | 0 critical, < 5 total |
| NIST AI RMF GOVERN maturity | 2 | 3 |

**Cultural adoption** — is governance becoming part of how we work?

| Indicator | Measurement Method |
|-----------|-------------------|
| Governance issues raised proactively (not reactively) | Incident log — source of detection |
| Data Science team completing model cards without prompting | Model inventory audit |
| Business team referencing governance metrics in disbursement reviews | MRC minutes |
| Compliance team interpreting bias findings independently | Compliance report quality |

---

*GRO Shield Independent Governance Assessment, July 2026.*

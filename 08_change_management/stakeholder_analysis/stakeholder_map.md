# Stakeholder Map and Resistance Analysis
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital.

**Version:** 1.0
**Date:** July 2026
**Prepared By:** GRO Shield Independent Governance Assessment

---

## Overview

Effective governance adoption requires understanding that each
stakeholder group experiences governance differently — as an
enabler, a constraint, a risk reducer, or an overhead — depending
on their role, incentives, and prior experience with governance
initiatives that succeeded or failed.

This analysis maps five key stakeholder groups at UGRO Capital,
their relationship to the GRO Shield findings, their likely
resistance points, and the engagement strategies most likely
to convert resistance into active participation.

The framing principle throughout: **governance is not something
done to stakeholders — it is something built with them.** Resistance
is information, not obstruction. Every resistance point named below
is a legitimate concern that deserves a genuine answer, not a
communications workaround.

---

## Stakeholder 1 — Chief Data Officer (CDO)

### Role and Context
The CDO is the primary internal champion for data governance at
UGRO Capital. As a self-described DataTech NBFC, UGRO Capital's
CDO carries significant organisational weight — data strategy is
central to the business model, not a support function. The CDO
is likely to be the most receptive governance stakeholder but
also the most technically demanding audience.

### Interest in Governance
**High and aligned.** The GRO Shield findings directly support
the CDO's mandate:
- Module 1 DQ scorecard (97.4/100) provides evidence of data
  infrastructure quality to present to the Board
- Module 2 data catalogue gives the CDO visibility into data
  assets that may have been undocumented
- Module 5 bias findings create urgency for the CDO to lead
  remediation — positioning the CDO as proactive rather than reactive
- Module 7 GenAI governance fills a gap the CDO likely knows exists
  but hasn't had bandwidth to address

### Likely Resistance Points

**Resistance 1: "We already have data governance processes."**
UGRO Capital's DataTech positioning implies existing data
infrastructure. The CDO may perceive GRO Shield as duplicating
work already done internally or implying the current state is
worse than it is.

*Response:* Frame GRO Shield as an independent external
validation, not a criticism. External assessments add credibility
that internal assessments cannot — the same way an external audit
adds credibility that internal audit cannot. The 97.4/100 DQ
score is a finding to be proud of and to communicate externally.

**Resistance 2: "The bias findings will create regulatory attention
we're not ready for."**
The CDO may be concerned that documenting CRITICAL bias findings
creates a paper trail that becomes a liability in a regulatory
examination.

*Response:* The opposite is true. Regulators view undocumented
problems as negligence; documented problems with remediation plans
as governance maturity. A regulator who discovers bias findings
through their own examination and finds no internal documentation
is far more serious than a regulator who sees a bias audit, open
findings, and a mitigation roadmap.

**Resistance 3: "We don't have the team bandwidth for this."**
Governance implementation requires sustained effort from data
science and data engineering teams who are already delivering
product features.

*Response:* Sequence governance implementation around existing
delivery cycles. Phase 1 Foundation work (policies, documentation)
can be done alongside feature development. Phase 2 and 3 are
scheduled with sufficient runway. Provide ready-made artefacts
(model card template, bias audit methodology) that reduce effort
rather than adding to it.

### Engagement Strategy
- **Primary message:** "GRO Shield gives you the external validation
  and documentation to defend UGRO Capital's DataTech positioning
  to regulators, investors, and borrowers."
- **Format:** Executive summary with DQ scorecard, bias findings
  summary, and remediation roadmap — one page per module
- **Frequency:** Monthly governance steering meeting
- **Quick win:** Share the 97.4/100 DQ scorecard as a positive
  finding in the first engagement — establish credibility before
  presenting gap findings

---

## Stakeholder 2 — Chief Risk Officer (CRO)

### Role and Context
The CRO owns model risk, credit risk, and operational risk —
three of the five risk categories in the GRO Shield AI risk
register. The CRO's primary lens is risk appetite: what level
of risk is acceptable, and what controls are in place to keep
risk within that appetite. The CRO is also the most likely
escalation point for regulatory examination findings.

### Interest in Governance
**High but conditional.** The CRO's interest is directly engaged
by several GRO Shield findings:
- 12 Critical risks in the AI risk register require CRO awareness
  and several require CRO approval to treat
- The state bias finding (EOD 0.446) has direct regulatory
  implications under RBI Fair Practices Code — the CRO needs to
  know this before RBI does
- The absence of a human-in-the-loop mechanism for a High Risk
  AI system is an operational risk the CRO should be uncomfortable
  with
- The AI incident response procedure requires CRO as incident
  commander for P1 events

### Likely Resistance Points

**Resistance 1: "These are model risk findings, not CRO-level issues."**
The CRO may delegate AI governance to the Model Risk Committee
and not engage directly, treating it as a technical matter.

*Response:* The CRITICAL bias findings and DPDP Act compliance
gap are not technical findings — they are regulatory and
reputational risks that sit squarely in the CRO's portfolio.
Frame specifically: "If RBI identifies the state bias finding
before we do, this becomes a CRO-level regulatory matter, not
a data science matter."

**Resistance 2: "Bias remediation will reduce approval rates
and affect portfolio targets."**
The CRO may be concerned that fairness-constrained retraining
reduces the model's ability to price risk accurately — increasing
credit losses.

*Response:* The Chouldechova impossibility theorem documented
in Module 5 makes this a genuine policy trade-off, not a false
dilemma. Present it honestly: "Remediating equalized odds bias
may marginally reduce discrimination between risk groups, but
the current model is over-predicting default for Delhi applicants
by 13.8 percentage points — that means we're also rejecting good
credit at scale. Remediation likely improves portfolio quality
for the affected segments, not just fairness."

**Resistance 3: "We need regulatory legal opinion before acting
on these findings."**
The CRO may want to defer action pending legal review of whether
the bias findings constitute an actual regulatory breach.

*Response:* Legal review is appropriate and should be commissioned.
But interim controls (human review mandate for borderline cases,
threshold adjustment) can be implemented immediately and do not
require legal sign-off — they are risk management decisions
within the CRO's authority.

### Engagement Strategy
- **Primary message:** "GRO Shield identifies 12 Critical AI risks
  before your regulator does — and gives you a remediation roadmap
  to address them."
- **Format:** AI risk register summary with Critical findings
  highlighted; one-page regulatory exposure assessment
- **Frequency:** Quarterly Model Risk Committee presentation;
  immediate briefing on CRITICAL findings
- **Quick win:** Human review mandate for borderline cases —
  implementable within 30 days, no code required, directly reduces
  regulatory exposure

---

## Stakeholder 3 — Data Science Team

### Role and Context
The Data Science team built and maintains GRO Score. They are
simultaneously the most technically capable audience and the most
emotionally invested — the bias findings and model risk findings
are, in a real sense, findings about their work. How this is
framed determines whether the Data Science team becomes governance
champions or governance resistors.

### Interest in Governance
**Mixed — capability aligned, culture misaligned.**
Data scientists typically care deeply about model quality and
are often more aware of model limitations than anyone else in
the organisation. The GRO Shield findings validate concerns they
may have already raised internally. However, governance processes
can feel like overhead that slows down the work they find
meaningful.

### Likely Resistance Points

**Resistance 1: "We already knew about these limitations."**
The reject inference bias, the performance limitations, and
potentially even the bias findings may be things the Data Science
team identified during development but couldn't prioritise for
remediation.

*Response:* "Yes — and GRO Shield gives you the documented,
external evidence to prioritise them. Internal concerns that
don't get escalated don't get resourced. A governance framework
with named findings, severity ratings, and remediation timelines
gives you the organisational leverage to get this work funded
and scheduled."

**Resistance 2: "Model cards and bias audits are additional
documentation overhead on top of already tight delivery timelines."**
Every governance artefact added to the model development process
is time that isn't spent building features.

*Response:* GRO Shield provides ready-made templates for model
cards, bias audit methodology, and PSI monitoring code. The
marginal effort to complete a model card for a new model version
is small when the template already exists. Embed governance
checkpoints in the existing sprint cycle rather than adding
a separate governance track.

**Resistance 3: "Fairness constraints will reduce model performance."**
Fairness-constrained retraining (Action G3 in the mitigation
roadmap) typically reduces overall AUC by 1–3 percentage points.
Data scientists may resist this as a quality regression.

*Response:* Frame it as a design choice, not a regression.
"We are deliberately trading 1–2pp of AUC for a reduction in
equalized odds difference from 0.172 to below 0.10. That is
a documented, Board-approved policy decision — not a model failure.
It belongs in the model card as a design decision, not a limitation."

**Resistance 4: "SHAP and Fairlearn add computational overhead
to the training pipeline."**
Additional evaluation steps slow down iteration cycles.

*Response:* SHAP TreeExplainer on 1,513 test samples runs in
under 30 seconds. Fairlearn metrics add negligible compute time.
The PSI dashboard runs asynchronously and doesn't block training.
Demonstrate the actual runtime before this becomes a perceived barrier.

### Engagement Strategy
- **Primary message:** "GRO Shield gives you the tools, templates,
  and organisational backing to do the model governance work you
  already know needs doing."
- **Format:** Technical deep-dives; working sessions on SHAP
  interpretation and Fairlearn metrics; code handover of GRO Shield
  monitoring tools
- **Frequency:** Weekly during implementation phases; embedded
  in sprint reviews
- **Quick win:** Hand over the PSI monitoring dashboard code —
  something the team can run immediately and that visibly improves
  their monitoring capability with minimal effort

---

## Stakeholder 4 — Compliance Team

### Role and Context
The Compliance team is responsible for regulatory mapping,
breach notification, and ensuring UGRO Capital's practices
align with RBI, DPDP Act, and other applicable frameworks.
They are likely the most natural governance ally — but may
lack the technical background to interpret model risk and
bias findings without translation.

### Interest in Governance
**High and urgent.** The DPDP Act compliance gap — privacy
policy referencing withdrawn PDP Bill 2021 — is a finding
the Compliance team needs to act on immediately. It is a
publicly citable gap that creates direct regulatory exposure.
The bias findings also create RBI Fair Practices Code exposure
that sits in the Compliance team's domain.

### Likely Resistance Points

**Resistance 1: "We don't have the technical background to
interpret bias metrics and model risk findings."**
Equalized odds difference, PSI thresholds, and SHAP values
are not concepts covered in legal or compliance training.

*Response:* GRO Shield is designed to bridge this gap. The
bias audit report translates EOD 0.172 into plain language:
"The model makes systematically different errors for Female
proprietors — flagging them as default risks at a higher rate
than their actual credit behaviour justifies." The compliance
team doesn't need to understand the mathematics — they need
to understand the regulatory implication and the remediation
action required.

**Resistance 2: "Acting on the DPDP compliance gap will require
significant legal and operational work."**
Updating the privacy policy, implementing the consent management
system, and appointing a DPO all require legal review, board
approval, and operational implementation.

*Response:* Sequence the remediation. The privacy policy update
is a one-day task that removes the most publicly visible gap.
The consent management system (Module 3) is already built.
DPO appointment is a board decision with a clear regulatory
deadline. Break it into steps rather than treating it as a
single overwhelming remediation project.

**Resistance 3: "We need to understand our regulatory exposure
before disclosing these findings internally."**
The Compliance team may want to contain the bias findings until
they have legal opinion on whether they constitute actual
regulatory breaches.

*Response:* Internal disclosure to the CRO and CDO is not a
regulatory disclosure — it is governance. Delaying internal
escalation of known Critical findings increases, not decreases,
regulatory exposure. If RBI discovers the findings through an
examination and finds no internal escalation trail, that is
evidence of governance failure, not governance caution.

### Engagement Strategy
- **Primary message:** "GRO Shield translates complex technical
  findings into regulatory language your team can act on —
  and gives you the documentation to demonstrate proactive
  compliance to RBI."
- **Format:** Plain-language regulatory exposure summary;
  compliance gap analysis with regulatory citations; breach
  notification templates
- **Frequency:** Monthly compliance review; immediate briefing
  on DPDP Act gaps
- **Quick win:** Privacy policy update — remove reference to
  withdrawn PDP Bill 2021, replace with DPDP Act 2023 citation.
  Single highest-visibility gap closed in one day.

---

## Stakeholder 5 — Business and Sales Team

### Role and Context
The Business and Sales team owns disbursement targets, client
relationships, and revenue. They experience governance primarily
as friction — processes that slow down approvals, add documentation
requirements, or (in their view) reduce the number of loans
that get approved. They are the most likely source of sustained
resistance to governance implementation and the stakeholder group
most often neglected in governance design.

### Interest in Governance
**Low initially — but genuinely alignable.**
The Business team's interest in governance is indirect but real:
- Regulatory enforcement action stops disbursements entirely —
  far more disruptive than governance overhead
- Bias remediation in Module 5 may actually *increase* approval
  rates for under-served segments (Female proprietors, northern
  states, Food Processing) — growing the addressable market
- DPDP Act compliance builds borrower trust — relevant for
  repeat lending and referrals
- ESG governance credentials increasingly matter to institutional
  funding partners

### Likely Resistance Points

**Resistance 1: "Bias remediation will reduce our approval rates
and affect disbursement targets."**
This is the most common and most predictable business objection
to fairness work — and it deserves a direct, honest answer.

*Response:* "The current model is over-predicting default for
Delhi applicants by 13.8 percentage points and for Food Processing
by 16.6 percentage points. These are creditworthy borrowers
being rejected. Bias remediation expands your addressable market
in these segments — it doesn't shrink it. The segments with
confirmed over-prediction are growth opportunities, not risks."

**Resistance 2: "Governance processes add friction to the
loan application journey and hurt conversion rates."**
Additional consent steps, explanation requirements, and review
processes all add time and complexity to the borrower experience.

*Response:* Well-designed governance is invisible to borrowers.
The consent management system (Module 3) is a one-time setup.
The right-to-explanation process only activates on rejection.
PSI monitoring runs in the background. The governance overhead
the Business team experiences is primarily internal documentation —
not borrower-facing friction.

**Resistance 3: "This is a data science and compliance problem,
not a business problem."**
The Business team may disengage entirely, treating governance
as someone else's responsibility.

*Response:* Regulatory enforcement under RBI Fair Practices Code
becomes a business problem very quickly. Frame it with a concrete
scenario: "If RBI examines our lending data and finds a 13.8
percentage point approval rate gap between Delhi and Rajasthan
that isn't explained by actual credit risk, the response will
involve the business team, not just compliance. Getting ahead
of this is a business decision, not a technical one."

**Resistance 4: "We've been running GRO Score successfully for
years — why change what works?"**
Status quo bias — if the model has been producing acceptable
portfolio outcomes, the Business team may not see the urgency.

*Response:* "The model has been producing acceptable *portfolio*
outcomes. The bias findings are about outcomes for individual
borrowers — specifically, whether we are systematically excluding
creditworthy borrowers from segments where we have growth
opportunity. Portfolio performance and fairness performance are
different metrics and both matter."

### Engagement Strategy
- **Primary message:** "Bias remediation opens up growth
  opportunities in under-served segments — Female proprietors,
  northern states, and Food Processing — where the model is
  currently over-predicting risk."
- **Format:** Business impact one-pager; market opportunity
  analysis for under-served segments; regulatory risk scenario
- **Frequency:** Quarterly business review; one-time briefing
  on regulatory exposure before implementation begins
- **Quick win:** Frame the Delhi finding as a market opportunity:
  "We have 159 Delhi applicants in our test set with a 10.1%
  actual default rate — one of the lowest of any state — but
  we're predicting 23.9% default and rejecting many of them.
  That's a creditworthy market segment we're not serving."

---

## Resistance Heat Map

| Stakeholder | Technical Resistance | Process Resistance | Cultural Resistance | Overall |
|-------------|--------------------|--------------------|--------------------|---------| 
| CDO | Low | Medium | Low | 🟡 Medium |
| CRO | Low | Medium | Medium | 🟡 Medium |
| Data Science | Medium | Medium | High | 🟠 Medium-High |
| Compliance | High | Medium | Low | 🟡 Medium |
| Business/Sales | Low | High | High | 🔴 High |

**Implication:** Business/Sales requires the most sustained engagement
and the most carefully framed messaging. Data Science requires the
most technical credibility to win over. Compliance requires
translation support. CDO and CRO are natural allies but need
specific, regulatory-grounded evidence to act.

---

## Coalition Building Strategy

Governance implementation succeeds fastest when it has an internal
coalition — at least two senior stakeholders who actively champion
the programme, not just tolerate it.

**Recommended coalition:**
1. **CDO as primary champion** — owns the data governance mandate,
   has the most to gain from GRO Shield validation, most receptive
   to the findings
2. **CRO as risk authority** — the Critical risk register findings
   give the CRO a direct interest in being seen to address them
   before RBI does

**With CDO + CRO aligned**, the Data Science team has executive
air cover for governance work, the Compliance team has escalation
authority for the DPDP gaps, and the Business team faces a unified
senior message rather than a governance team asking for cooperation.

---

*GRO Shield Independent Governance Assessment, July 2026.*

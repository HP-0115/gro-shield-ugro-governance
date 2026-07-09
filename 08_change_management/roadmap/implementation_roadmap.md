# Governance Implementation Roadmap
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital.

**Version:** 1.0
**Date:** July 2026
**Prepared By:** GRO Shield Independent Governance Assessment

---

## Roadmap Philosophy

Three principles govern the sequencing of this roadmap:

**Foundation before operationalisation.** Governance processes
embedded in workflows without supporting policy, accountability,
and tooling tend to be abandoned within 90 days. Phases 1 and 2
are sequenced so that every Phase 2 action has a Phase 1 foundation
to rest on.

**Quick wins before structural changes.** Each phase opens with
actions that are high-visibility, low-effort, and immediately
demonstrable. Quick wins build internal credibility for the
governance programme — particularly important with the Business
and Sales stakeholder group, who need to see governance delivering
value before committing to sustained cooperation.

**Regulatory urgency drives prioritisation.** The DPDP Act
compliance gap and the CRITICAL bias findings are not optional
to address — they carry regulatory and legal exposure. These
are sequenced in Phase 1 regardless of stakeholder appetite.

---

## Phase 1 — Foundation (Months 1–3)

**Objective:** Establish the governance infrastructure that all
subsequent work depends on. By the end of Phase 1, UGRO Capital
should have: documented accountability, critical regulatory gaps
closed, basic monitoring operational, and a governance coalition
of CDO + CRO actively championing the programme.

### Month 1 — Accountability and Critical Gaps

**Week 1–2: Governance structure establishment**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Appoint Data Protection Officer | Board/CEO | Low | None |
| Establish Model Risk Committee with defined terms of reference | CRO | Low | None |
| Assign model owner and compliance owner to MDL-001 in model inventory | CDO + CRO | Low | None |
| Brief CDO and CRO on GRO Shield findings — establish coalition | Governance Lead | Low | None |

Rationale: Accountability gaps are the highest-risk governance
finding because they mean no one is responsible when something
goes wrong. These actions require no technical work — they are
organisational decisions that can be made in week 1.

**Week 3–4: DPDP Act critical gap closure**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Update privacy policy — replace PDP Bill 2021 reference with DPDP Act 2023 | Legal + DPO | Low | DPO appointed |
| Deploy consent management system (Module 3) to staging | Data Engineering | Medium | None |
| Register as Data Fiduciary under DPDP Act (when portal live) | DPO + Legal | Low | DPO appointed |
| Brief Compliance team on 15 DPDP gaps and prioritise top 4 critical | Governance Lead + Compliance | Low | None |

Rationale: The privacy policy update is the single highest-visibility
gap in the entire assessment — it is publicly citable and takes
one day to fix. There is no justification for leaving it open
beyond week 1.

### Month 2 — Monitoring and Interim Bias Controls

**Bias interim controls (no retraining required)**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Implement human review mandate for borderline cases (predicted probability 0.35–0.65) | Credit Risk + Operations | Low | CRO approval |
| Apply threshold adjustment for Female proprietors (0.55 vs 0.50) | Data Science | Low | Model Risk Committee approval |
| Implement state-level approval rate monitoring — weekly report to CRO | Data Science | Low | None |
| Conduct Delhi retrospective review — last 90 days rejected applications | Credit Risk | Medium | CRO approval |

Rationale: These actions reduce regulatory exposure immediately
without requiring model retraining. They are temporary measures
with defined expiry (90 days maximum per the mitigation roadmap)
pending permanent technical fixes in Phase 2.

**Monitoring infrastructure**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Deploy PSI monitoring dashboard (Module 4) to production | Data Science | Low | None |
| Configure monthly PSI alerts — email to Data Science Lead and CRO | Data Science | Low | Dashboard deployed |
| Run first quarterly fairness metrics review | Data Science + Compliance | Medium | None |
| Add dpd_90_count_12m CRITICAL PSI finding to model risk register | Data Science | Low | None |

### Month 3 — Policy and Documentation

**Policy adoption**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Adopt Responsible AI Policy — Board Risk Committee approval | CRO + Board | Low | Coalition established |
| Adopt GenAI Governance Policy — CDO approval | CDO | Low | None |
| Complete model card for GRO Score (Module 4) — internal sign-off | Data Science + Compliance | Low | None |
| Publish model inventory register — circulate to Model Risk Committee | CDO | Low | None |

**Training — Phase 1**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| DPDP Act awareness training — all staff handling personal data | DPO | Medium | DPO appointed |
| Bias audit findings briefing — Data Science team | Governance Lead | Low | None |
| AI risk register walkthrough — CRO and Model Risk Committee | Governance Lead | Low | None |

### Phase 1 Success Criteria

By end of Month 3, the following must be true:

- [ ] DPO appointed
- [ ] Model Risk Committee established and meeting
- [ ] Privacy policy updated — DPDP Act 2023 referenced
- [ ] Consent management system in staging
- [ ] Human review mandate operational for borderline cases
- [ ] PSI monitoring dashboard live
- [ ] Responsible AI Policy Board-approved
- [ ] CDO and CRO actively engaged as governance champions
- [ ] Model inventory register circulated

**Phase 1 governance maturity target:** GOVERN: 2→3 | MANAGE: 2→3

---

## Phase 2 — Operationalisation (Months 4–9)

**Objective:** Embed governance into day-to-day workflows so that
it runs without requiring a dedicated governance initiative to
sustain it. By the end of Phase 2, governance should feel like
part of how UGRO Capital builds and runs models — not a separate
programme running alongside the main business.

### Months 4–6: Technical Remediation

**Bias remediation — model retraining**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Commission reject inference study — gender stratified | Data Science | High | Phase 1 complete |
| Replace state dummy variables with state-level economic indicators | Data Science | High | Feature data sourced |
| Replace sector dummies with sector risk indices (RBI NPA data) | Data Science | High | Feature data sourced |
| Retrain model with Fairlearn EqualizedOdds constraint | Data Science | Medium | Features updated |
| Fairness testing on retrained model — EOD must pass thresholds | Data Science + Compliance | Medium | Retraining complete |
| Independent validation of retrained model | External validator | High | Retraining complete |
| Deploy retrained model — update model inventory register | Data Science + CDO | Medium | Validation passed |

Rationale: Months 4–6 give the Data Science team the runway to
do the technical bias remediation properly. Rushing retraining
without the feature engineering work (state and sector replacement)
would produce a model that passes fairness tests on the current
data but fails on new production data through the same proxy
channels.

**DPDP Act operationalisation**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Deploy consent management system to production | Data Engineering | Medium | Staging complete |
| Implement right-to-explanation process — SHAP-based rejection letters | Data Science + Compliance | Medium | SHAP pipeline stable |
| Complete Records of Processing Activities register (Module 3) | DPO | Medium | None |
| Conduct first Data Protection Impact Assessment for new AI system | DPO + Data Science | High | DPO trained |
| Implement data breach detection and 72-hour notification procedure | DPO + IT Security | High | None |

### Months 7–9: Process Embedding

**Model development lifecycle**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Embed pre-deployment checklist in model development workflow | CDO + Data Science | Low | Checklist defined |
| Add bias testing as mandatory sprint gate for model releases | Data Science Lead | Low | Fairlearn pipeline stable |
| Add model card completion as mandatory pre-deployment requirement | CDO | Low | Template available |
| First annual bias audit on retrained model | Data Science + External | High | Retrained model live |
| First annual independent model validation on retrained model | External validator | High | Retrained model live |

**GenAI governance**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Select LLM provider — complete data processing agreement review | Legal + CDO | High | GenAI use case approved |
| Deploy GenAI guardrail system to production (if chatbot approved) | Data Science | Medium | Provider selected |
| Deploy GenAI observability dashboard | Data Science | Low | Guardrail system live |
| First quarterly GenAI metrics review | Compliance | Low | Dashboard live |
| Prompt injection red-team testing | Data Science + Security | Medium | Guardrail system live |

**Training — Phase 2**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Fairness metrics interpretation training — Compliance team | Data Science | Medium | Bias audit complete |
| Model risk metrics training — CRO and Model Risk Committee | Governance Lead | Low | None |
| AI incident response tabletop exercise | CRO + Data Science + Compliance | Medium | IR procedure adopted |

### Phase 2 Success Criteria

By end of Month 9, the following must be true:

- [ ] Retrained model live — EOD below threshold for all attributes
- [ ] Consent management system in production
- [ ] Right-to-explanation process operational
- [ ] Pre-deployment checklist embedded in model development workflow
- [ ] Bias testing as mandatory sprint gate
- [ ] Annual bias audit scheduled
- [ ] AI incident response procedure tested via tabletop exercise
- [ ] GenAI governance decision made (deploy or defer)

**Phase 2 governance maturity target:** MEASURE: 3→4 | MAP: 2→3

---

## Phase 3 — Optimisation (Months 10–12)

**Objective:** Move from governance as a compliance activity to
governance as a competitive advantage. By end of Phase 3, UGRO
Capital's AI governance should be proactive — anticipating risks
before they materialise, contributing to regulatory dialogue,
and demonstrating governance maturity to investors and partners.

### Month 10–11: Maturity and Measurement

**Governance maturity assessment**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Conduct 12-month governance maturity re-assessment against NIST AI RMF | Governance Lead | Medium | Phase 2 complete |
| Update AI risk register — close resolved risks, add new risks | CRO + Data Science | Low | None |
| Prepare annual AI governance report for Board Risk Committee | CRO + CDO | Medium | All data available |
| Benchmark governance maturity against industry peers | Governance Lead | Medium | None |

**Continuous improvement**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Implement automated fairness monitoring — quarterly alerts | Data Science | Medium | Retrained model live |
| Extend PSI monitoring to all top-10 features | Data Science | Low | Dashboard live |
| Implement feedback loop tracking — monitor whether bias remediation segments show improved approval rates | Data Science + Credit Risk | Medium | Retrained model live |
| Conduct post-implementation review — did bias remediation expand addressable market? | Business + Data Science | Medium | 3 months of retrained model data |

### Month 12: Strategic Positioning

**External positioning**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Publish Responsible AI Policy — public facing version | CDO + Legal | Low | Policy Board-approved |
| Engage RBI on AI governance approach — proactive regulatory dialogue | CRO + Compliance | Medium | Phase 2 complete |
| Include AI governance metrics in ESG disclosure | CFO + CDO | Low | Metrics available |
| Submit governance case study to industry body (FIDC, IBA) | CDO | Low | Phase 2 complete |

**Planning for Year 2**

| Action | Owner | Effort | Dependency |
|--------|-------|--------|------------|
| Schedule Year 2 independent model validation | Model Risk Committee | Low | None |
| Plan annual bias audit — expanded to include proxy discrimination testing | Data Science + Compliance | Low | None |
| Assess ISO 42001 certification readiness | CDO + External consultant | Medium | Phase 3 complete |
| Review Responsible AI Policy — annual cycle | CRO + CDO | Low | 12 months elapsed |

### Phase 3 Success Criteria

By end of Month 12, the following must be true:

- [ ] NIST AI RMF maturity re-assessed — GOVERN target 3, MANAGE target 3
- [ ] Annual AI governance report delivered to Board
- [ ] Responsible AI Policy published externally
- [ ] Automated fairness monitoring operational
- [ ] ISO 42001 certification readiness assessed
- [ ] Year 2 validation and audit schedule confirmed

**Phase 3 governance maturity target:** GOVERN: 3 | MAP: 3 | MEASURE: 4 | MANAGE: 3

---

## Roadmap Summary

| Phase | Timeline | Theme | Key Outcome |
|-------|----------|-------|-------------|
| Foundation | Months 1–3 | Accountability + critical gap closure | DPO appointed; privacy policy updated; PSI dashboard live; Responsible AI Policy adopted |
| Operationalisation | Months 4–9 | Technical remediation + process embedding | Bias remediated; consent system live; governance in sprint workflow |
| Optimisation | Months 10–12 | Maturity + strategic positioning | Board AI governance report; public policy; ISO 42001 readiness |

## Investment Estimate

| Phase | Internal Effort | External Cost (indicative) |
|-------|----------------|--------------------------|
| Phase 1 | ~120 person-days | ₹10–15 lakhs (legal, DPO setup) |
| Phase 2 | ~300 person-days | ₹25–40 lakhs (validation, training, tooling) |
| Phase 3 | ~80 person-days | ₹10–15 lakhs (certification readiness, external audit) |
| **Total** | **~500 person-days** | **₹45–70 lakhs** |

Note: Investment estimates are indicative only, based on typical
governance programme costs for a mid-sized NBFC. Actual costs
depend on team rates, vendor selection, and scope decisions.

---

*GRO Shield Independent Governance Assessment, July 2026.*

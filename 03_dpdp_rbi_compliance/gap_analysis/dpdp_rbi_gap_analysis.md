# Compliance Gap Analysis
## DPDP Act 2023, DPDP Rules 2025, and RBI Digital Lending Guidelines
### Subject: UGRO Capital Limited — GRO Score 3.0 Data Processing Practices

**Document ID:** GRO-GAP-001  
**Version:** 1.0  
**Assessment Date:** July 2026  
**Prepared by:** GRO Shield Governance Framework  
**Classification:** Confidential  

---

## 1. Executive Summary

This gap analysis assesses UGRO Capital Limited's publicly disclosed
data processing practices against three regulatory frameworks:

1. Digital Personal Data Protection Act 2023 (DPDP Act)
2. Digital Personal Data Protection Rules 2025 (DPDP Rules)
3. RBI Digital Lending Guidelines, September 2022

The assessment is based exclusively on publicly available information
— UGRO Capital's published privacy policy, annual reports, investor
presentations, and press releases. It does not reflect UGRO Capital's
internal compliance posture, which the author has no visibility into.

**Anchor Finding:** UGRO Capital's publicly available privacy policy
references the draft Personal Data Protection Bill, 2021 — a bill
that was withdrawn by the Government of India and replaced by the
enacted DPDP Act 2023. This indicates the privacy policy has not
been updated to reflect current law, creating material compliance
gaps across consent management, data principal rights, breach
notification, and penalty awareness.

**Total gaps identified:** 15 across 5 compliance domains  
**Critical gaps:** 4  
**High gaps:** 7  
**Medium gaps:** 4  

---

## 2. Scope and Methodology

### 2.1 Scope

This assessment covers data processing activities associated with
UGRO Capital's GRO Score 3.0 credit scoring model, specifically:

- Collection of personal data from loan applicants
- Processing of bureau, bank statement, and GST data
- Automated credit decision-making via GRO Score
- Data retention and deletion practices
- Breach notification procedures
- Data principal rights management

### 2.2 Methodology

Each regulatory requirement was assessed against UGRO Capital's
publicly disclosed practices using a four-point rating scale:

| Rating | Definition |
|---|---|
| **Compliant** | Public disclosures demonstrate requirement is met |
| **Partial** | Some evidence of compliance but gaps exist |
| **Gap** | No evidence of compliance in public disclosures |
| **Critical Gap** | Non-compliance with a fundamental requirement |

### 2.3 Sources Reviewed

- UGRO Capital Privacy Policy (publicly available on ugrocapital.com)
- UGRO Capital Annual Report 2023-24
- UGRO Capital Investor Presentations 2023-24
- Digital Personal Data Protection Act 2023
- Digital Personal Data Protection Rules 2025
- RBI Digital Lending Guidelines, September 2022
- RBI Fair Practices Code for NBFCs

---

## 3. Gap Analysis — Domain 1: Consent Management

Consent is the primary lawful basis for processing personal data
under the DPDP Act 2023. Section 6 requires consent to be free,
specific, informed, and unambiguous, with withdrawal as easy as
giving consent.

| # | Requirement | Current State | Gap | Severity | Recommendation |
|---|---|---|---|---|---|
| 1.1 | DPDP Act S.6: Consent must be free, specific, informed, and unambiguous before processing begins | Privacy policy references PDP Bill 2021 consent framework, not DPDP Act 2023 | Policy not aligned to enacted law — consent mechanism may not meet 2023 Act standards | Critical | Update privacy policy immediately to reference DPDP Act 2023; redesign consent flow to meet Section 6 requirements |
| 1.2 | DPDP Act S.6(4): Withdrawal of consent must be as easy as giving consent | No public evidence of a consent withdrawal mechanism for bureau, bank statement, or GST data pulls | No withdrawal mechanism disclosed — violates symmetry requirement | Critical | Implement one-click consent withdrawal in loan applicant portal; document withdrawal procedure in privacy policy |
| 1.3 | DPDP Rules 2025: Consent notice must specify each purpose, each category of data, and each third party receiving data | Privacy policy uses broad, generic language about data use | Insufficient granularity — bureau pull, AA pull, and GST pull require separate, purpose-specific consent notices | High | Implement layered consent notices — one per data source pull — specifying exact data categories and third-party recipients |
| 1.4 | DPDP Act S.6(1): Separate consent required for each distinct processing purpose | Single consent appears to cover all data processing activities | Bundled consent does not meet DPDP Act's purpose-specific requirement | High | Unbundle consent into at minimum three separate notices: (1) bureau pull, (2) bank statement/AA, (3) GSTN query |

---

## 4. Gap Analysis — Domain 2: Data Principal Rights

The DPDP Act 2023 grants data principals (loan applicants) specific
rights over their personal data. These rights differ materially from
those in the 2021 Bill that UGRO's policy references.

| # | Requirement | Current State | Gap | Severity | Recommendation |
|---|---|---|---|---|---|
| 2.1 | DPDP Act S.11: Right to access — data principal can request summary of personal data processed | No public evidence of a data access request mechanism for loan applicants | No access mechanism disclosed | High | Implement a data access request portal or process; commit to response within statutory timeframe |
| 2.2 | DPDP Act S.12: Right to correction and erasure of inaccurate or incomplete personal data | No public correction or erasure process disclosed | No correction mechanism for applicants to challenge inaccurate data used in credit decisions | High | Implement correction request process; define procedure for updating bureau or GST data disputes |
| 2.3 | DPDP Act S.14: Right to nominate — data principal can nominate another person to exercise rights on death or incapacity | Privacy policy references 2021 Bill rights framework which did not include nomination right | Data principals not informed of nomination right — a right that exists under current law | Medium | Add nomination right to privacy policy and implement nomination registration process |
| 2.4 | DPDP Act S.13: Right to grievance redressal — data principal can file complaint with Data Fiduciary | No public grievance redressal mechanism specifically for data processing complaints disclosed | Grievance mechanism may exist for loan complaints but not specifically for data processing rights | Medium | Establish and publish a dedicated data grievance redressal process separate from general loan complaint process |

---

## 5. Gap Analysis — Domain 3: Automated Decision-Making

GRO Score 3.0 is an automated credit scoring system making or
materially influencing lending decisions affecting individuals.
This triggers specific obligations under both the DPDP Act and
RBI guidelines.

| # | Requirement | Current State | Gap | Severity | Recommendation |
|---|---|---|---|---|---|
| 3.1 | RBI Digital Lending Guidelines S.6: Borrower must receive explanation for automated credit decision on request | UGRO publicly describes GRO Score as AI-based but does not disclose an explanation mechanism for rejected applicants | No public evidence of explanation process for rejected applicants | Critical | Implement explanation mechanism for GRO Score rejections — minimum: top factors driving rejection in plain language |
| 3.2 | RBI Fair Practices Code: Reasons for loan rejection must be communicated to applicant | Standard requirement for all NBFCs | No public disclosure of how GRO Score rejection reasons are communicated | High | Document and publish rejection communication process; ensure GRO Score outputs include human-readable rejection reasons |
| 3.3 | DPDP Act S.17: Significant Data Fiduciaries must conduct periodic DPIA for high-risk processing | Automated credit scoring using sensitive personal data of large applicant base likely qualifies as high-risk processing | No public evidence of DPIA conducted for GRO Score | High | Conduct and document a DPIA for GRO Score 3.0 — template provided in Module 3 DPIA deliverable |
| 3.4 | EU AI Act (emerging global standard): Credit scoring AI classified as High Risk requiring conformity assessment | UGRO operates in India — EU AI Act not directly applicable — but represents emerging global best practice | No conformity assessment or high-risk AI documentation publicly disclosed | Medium | Voluntarily adopt EU AI Act high-risk documentation standards as best practice — model card provided in Module 4 |

---

## 6. Gap Analysis — Domain 4: Breach Notification

The DPDP Act 2023 introduces mandatory breach notification
obligations that did not exist in the 2021 Bill in the same form.

| # | Requirement | Current State | Gap | Severity | Recommendation |
|---|---|---|---|---|---|
| 4.1 | DPDP Act S.8(6): Data Fiduciary must notify Data Protection Board and affected Data Principals of personal data breach without delay | Privacy policy references 2021 Bill which had different breach notification requirements | Breach notification procedure not aligned to DPDP Act 2023 — no 72-hour timeline disclosed | Critical | Implement DPDP Act-aligned breach response procedure — template provided in Module 3 breach playbook |
| 4.2 | DPDP Rules 2025: Breach notification must include nature of breach, categories of data affected, and remedial measures taken | No public breach notification template or procedure disclosed | No evidence of a structured breach notification process meeting Rules 2025 requirements | High | Develop breach notification template aligned to DPDP Rules 2025 requirements |

---

## 7. Gap Analysis — Domain 5: Cross-Border Data Transfer

The DPDP Act 2023 replaced the 2021 Bill's strict data localisation
requirements with a government-approved country framework.

| # | Requirement | Current State | Gap | Severity | Recommendation |
|---|---|---|---|---|---|
| 5.1 | DPDP Act S.16: Personal data may only be transferred to countries notified by Central Government | Privacy policy references 2021 Bill's localisation framework which has been superseded | Cross-border transfer policy based on withdrawn legislation | Medium | Update cross-border transfer policy to reference DPDP Act S.16 approved country framework |
| 5.2 | DPDP Rules 2025: Standard contractual clauses required for transfers to non-notified countries | No public disclosure of data transfer agreements with third-party service providers | No evidence of contractual safeguards for international data transfers | Medium | Audit all third-party data sharing arrangements; implement standard contractual clauses where required |

---

## 8. Summary of Findings

| Domain | Total Gaps | Critical | High | Medium |
|---|---|---|---|---|
| Consent Management | 4 | 2 | 2 | 0 |
| Data Principal Rights | 4 | 0 | 2 | 2 |
| Automated Decision-Making | 4 | 1 | 2 | 1 |
| Breach Notification | 2 | 1 | 1 | 0 |
| Cross-Border Transfer | 2 | 0 | 0 | 2 |
| **Total** | **15** | **4** | **7** | **4** |

---

## 9. Priority Recommendations

### Immediate Actions (Critical Gaps — within 30 days)

**R1 — Update Privacy Policy**
Replace all references to the Personal Data Protection Bill 2021
with the enacted Digital Personal Data Protection Act 2023.
Update rights disclosures to reflect current law including the
nomination right. Remove reference to the proposed Data Protection
Authority and replace with Data Protection Board of India.

**R2 — Implement Consent Withdrawal Mechanism**
Deploy a consent withdrawal function in the loan applicant portal
that allows applicants to withdraw consent for any or all data
processing activities with immediate effect. Document the
withdrawal process in the updated privacy policy.

**R3 — Implement GRO Score Explanation Mechanism**
Deploy a plain-language explanation process for GRO Score
rejections, disclosing the primary factors driving the decision
without revealing proprietary model logic. This satisfies both
RBI Digital Lending Guidelines and Fair Practices Code requirements.

**R4 — Align Breach Notification Procedure**
Update internal breach response procedures to meet DPDP Act
Section 8(6) requirements — notification to the Data Protection
Board and affected data principals without delay, with content
meeting DPDP Rules 2025 specification.

### Short-Term Actions (High Gaps — within 90 days)

**R5 — Unbundle Consent Notices**
Replace single bundled consent with three separate, purpose-specific
consent notices for bureau pull, Account Aggregator access, and
GSTN query. Each notice must specify exact data categories,
processing purpose, and third-party recipients.

**R6 — Implement Data Access and Correction Process**
Deploy a data access request mechanism allowing applicants to
request a summary of personal data held about them. Implement
a correction request process for challenging inaccurate data
used in credit decisions.

**R7 — Conduct DPIA for GRO Score**
Conduct a Data Protection Impact Assessment for GRO Score 3.0
documenting processing purposes, data categories, risks, and
mitigating controls. Template provided in this module's DPIA
deliverable.

---

## 10. Disclaimer

This gap analysis is an independent, self-initiated portfolio
assessment. It is not affiliated with, endorsed by, or commissioned
by UGRO Capital Limited. All findings are based on publicly
available information only and do not reflect UGRO Capital's
internal compliance posture. The anchor finding regarding the
privacy policy referencing the PDP Bill 2021 is based on the
publicly available version of UGRO Capital's privacy policy
at the time of writing. UGRO Capital may have updated its
privacy policy since this assessment was conducted.

See full project disclaimer at `docs/disclaimer.md`.

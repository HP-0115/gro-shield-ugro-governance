# Data Breach Response Playbook
## UGRO Capital Limited — GRO Score 3.0 Data Processing Operations

**Document ID:** GRO-PLAY-001  
**Version:** 1.0  
**Assessment Date:** July 2026  
**Prepared by:** GRO Shield Governance Framework  
**Classification:** Restricted — Internal Use Only  
**Status:** Draft — illustrative portfolio assessment  

---

## 1. Purpose

This playbook defines the step-by-step procedure for detecting,
containing, assessing, notifying, and remediating personal data
breaches affecting UGRO Capital's MSME loan applicant data.

It is designed to ensure compliance with:
- DPDP Act 2023 Section 8(6) — breach notification obligation
- DPDP Rules 2025 — notification content requirements
- RBI Digital Lending Guidelines — incident reporting

The 72-hour notification window is the binding constraint
throughout this playbook. All timings are measured from the
moment of breach discovery, not from when the breach occurred.

---

## 2. Breach Definition

A personal data breach is any event that results in accidental
or unlawful:
- **Unauthorised access** to personal data
- **Disclosure** of personal data to unintended recipients
- **Alteration** of personal data without authorisation
- **Destruction or loss** of personal data

Examples relevant to UGRO Capital's operations:
- Unauthorised access to the loan application database
- Accidental email of applicant PAN numbers to wrong recipient
- Ransomware encrypting the GRO Score feature store
- Bureau feed data exposed via misconfigured API endpoint
- Employee downloading applicant data to personal device

---

## 3. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| **Incident Commander** | Chief Risk Officer — overall accountability for breach response |
| **Data Protection Officer (DPO)** | Leads regulatory notification and data principal communication |
| **IT Security Lead** | Leads technical containment and forensic investigation |
| **Legal Counsel** | Advises on regulatory obligations and liability |
| **Communications Lead** | Manages internal and external communications |
| **Data Owner** | Provides context on affected data assets and business impact |

---

## 4. Phase 1 — Detect and Contain (0 to 4 Hours)

### 4.1 Detection

A breach may be detected through:
- Automated security monitoring alerts
- Employee report of suspicious activity
- Third-party notification (bureau provider, AA provider)
- Regulatory notification from Data Protection Board
- Applicant complaint about unauthorised data use

**Immediate action on detection:**
 Record exact date and time of discovery
□ Do NOT attempt to fix or delete anything before preserving evidence
□ Alert IT Security Lead immediately
□ Alert Data Protection Officer immediately
□ Start the breach log (Section 7 of this playbook)
□ Activate the incident response team

### 4.2 Initial Containment
□ Isolate affected systems from network if breach is ongoing
□ Revoke compromised credentials immediately
□ Preserve system logs — do not allow automatic log rotation
□ Take forensic snapshot of affected systems before any changes
□ Block any ongoing unauthorised data exfiltration
□ Notify cloud/infrastructure provider if applicable

### 4.3 Initial Assessment (by Hour 4)

The IT Security Lead must provide an initial assessment covering:
□ What systems are affected?
□ What data categories are involved?
(bureau data / bank statement data / GST data / identity data)
□ Estimated number of data principals affected
□ Is the breach contained or ongoing?
□ What is the likely cause?

**Decision gate at Hour 4:**
If personal data is confirmed or suspected to be involved →
activate Phase 2 immediately. Do not wait for full confirmation.
The 72-hour clock is running.

---

## 5. Phase 2 — Assess and Investigate (4 to 24 Hours)

### 5.1 Breach Assessment

The DPO leads a structured assessment to determine notification
obligations. Answer each question:
□ What personal data was affected?
(List specific data categories from RoPA register)
□ How many data principals are affected?
(Exact count or best estimate with methodology)
□ What is the likely harm to affected individuals?
□ Financial loss risk (exposed bank data, loan amounts)
□ Identity theft risk (exposed PAN, GSTIN)
□ Discrimination risk (exposed gender, sector data)
□ Reputational harm risk
□ No significant harm likely
□ Was the data encrypted at the time of breach?
(If yes, notification threshold may be lower)
□ Has the breach been fully contained?
□ What is the root cause?
□ External attack
□ Internal actor (malicious or accidental)
□ Third-party provider failure
□ System misconfiguration
□ Process failure

### 5.2 Notification Decision

| Scenario | Action Required |
|---|---|
| Personal data confirmed breached, significant harm possible | Notify Data Protection Board AND affected data principals |
| Personal data confirmed breached, harm unlikely (encrypted data) | Notify Data Protection Board only |
| No personal data involved | No regulatory notification required — document decision |
| Uncertain whether personal data involved | Treat as confirmed breach — notify to be safe |

### 5.3 Prepare Notification Content

DPDP Rules 2025 require the notification to include:
□ Nature of the personal data breach
□ Categories and approximate number of data principals affected
□ Categories and approximate volume of personal data records affected
□ Likely consequences of the breach
□ Measures taken or proposed to address the breach
□ Contact details of the Data Protection Officer
□ Steps data principals should take to protect themselves

---

## 6. Phase 3 — Notify and Remediate (24 to 72 Hours)

### 6.1 Notify the Data Protection Board (by Hour 72)
□ Submit breach notification to Data Protection Board of India
via official notification portal
□ Include all content items from Section 5.3
□ Retain submission confirmation and reference number
□ Log notification timestamp in breach log

**Critical:** Notification must be submitted by Hour 72 from
discovery. Late notification is itself a violation of DPDP Act
Section 8(6) and attracts separate penalties.

### 6.2 Notify Affected Data Principals
□ Identify communication channel for each affected applicant
(registered email, registered mobile, in-app notification)
□ Send notification in plain language — avoid legal jargon
□ Include:

What happened (brief, factual description)
What data was affected
What UGRO is doing about it
What the applicant should do to protect themselves
DPO contact details for questions
□ Log notification timestamps for each applicant
□ Retain copies of all notifications sent


### 6.3 Notify RBI (if applicable)

If the breach affects more than 10,000 data principals or
involves systemic failure of a regulated system, notify RBI
via the existing cybersecurity incident reporting framework
within 6 hours of confirmation.

### 6.4 Remediation Actions
□ Patch or fix the vulnerability that caused the breach
□ Reset all potentially compromised credentials
□ Implement additional monitoring on affected systems
□ Review and update access controls
□ Conduct security assessment of related systems
□ Brief board and senior management

---

## 7. Phase 4 — Review and Improve (Post 72 Hours)

### 7.1 Post-Incident Review

Within 14 days of breach containment, the incident response
team must conduct a post-incident review covering:
□ Root cause analysis — what actually caused the breach?
□ Timeline reconstruction — when did it start, when detected?
□ Response effectiveness — what worked, what didn't?
□ Control gaps — what control would have prevented this?
□ Regulatory response — was notification sufficient?
□ Data principal impact — what harm occurred or was prevented?

### 7.2 Corrective Actions
□ Document all corrective actions with owner and deadline
□ Update DPIA risk register with new or changed risks
□ Update this playbook if process gaps were identified
□ Schedule follow-up review to confirm actions completed
□ Report to board risk committee

---

## 8. Breach Log Template

Every breach must be logged from the moment of discovery.
This log is a regulatory document — retain for minimum 7 years.

| Field | Entry |
|---|---|
| Breach reference number | GRO-BREACH-[YYYY]-[NNN] |
| Discovery date and time | |
| Reported by | |
| Systems affected | |
| Data categories affected | |
| Estimated data principals affected | |
| Breach contained (Y/N) | |
| DPB notification submitted (timestamp) | |
| Data principal notifications sent (timestamp) | |
| RBI notification required (Y/N) | |
| Root cause (preliminary) | |
| Incident Commander | |
| DPO assigned | |

---

## 9. Key Contacts

| Role | Contact |
|---|---|
| Data Protection Officer | [DPO name and contact] |
| IT Security Lead | [Security lead contact] |
| Legal Counsel | [Legal contact] |
| Data Protection Board of India | [Official DPB portal URL] |
| RBI Cybersecurity Reporting | [RBI CSITE portal] |
| CERT-In | incidents@cert-in.org.in |

---

## 10. Playbook Review Schedule

This playbook must be reviewed:
- Annually as part of the DPIA review cycle
- After any actual breach event
- When DPDP Rules are updated
- When material changes occur to data processing systems

---

## Disclaimer

This playbook is produced as part of an independent portfolio
assessment and is illustrative in nature. It is not affiliated
with or endorsed by UGRO Capital Limited. See project disclaimer
at `docs/disclaimer.md`.

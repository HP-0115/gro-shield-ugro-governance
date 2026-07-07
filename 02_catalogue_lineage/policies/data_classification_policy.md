# Data Classification Policy

**Document ID:** GRO-POL-001  
**Version:** 1.0  
**Prepared by:** GRO Shield Governance Framework  
**Review Date:** Annually or upon material change to data processing activities  
**Status:** Draft — for illustrative purposes as part of independent portfolio assessment  

---

## 1. Purpose

This policy establishes a framework for classifying data assets held
and processed by UGRO Capital Limited according to their sensitivity
and the potential harm their unauthorised disclosure, modification,
or loss could cause to data principals, the organisation, or the
broader financial system.

Data classification is the foundation of effective data governance.
It enables consistent application of access controls, encryption
requirements, retention periods, and incident response priorities
across all data assets. It also provides the basis for demonstrating
compliance with the Digital Personal Data Protection Act 2023 (DPDP
Act), RBI Digital Lending Guidelines, and RBI Fair Practices Code.

---

## 2. Scope

This policy applies to all data assets processed by UGRO Capital
in connection with its MSME lending operations, including data
received from external sources (credit bureaus, GSTN, Account
Aggregators), data generated internally (loan origination, credit
decisions), and derived data (engineered model features, analytical
outputs).

---

## 3. Classification Tiers

### Tier 1 — Public

**Definition:** Data that is intentionally made available to the
general public or whose disclosure causes no harm to any party.

**Examples:** Published interest rate ranges, general product
information, publicly filed regulatory disclosures, press releases.

**Handling requirements:**
- No access restrictions required
- No encryption required for storage or transmission
- No special retention or disposal requirements
- May be shared freely internally and externally

---

### Tier 2 — Internal

**Definition:** Data intended for use within UGRO Capital that
is not sensitive enough to cause significant harm if disclosed
externally, but is not intended for public release.

**Examples:** Loan status (Approved/Rejected/Disbursed), tenure,
sector classification, state, entity type, aggregated portfolio
statistics, internal process documentation.

**Handling requirements:**
- Access restricted to UGRO Capital employees and authorised
  contractors on a need-to-know basis
- Standard encryption in transit (TLS 1.2+)
- Retention per standard business records policy (7 years)
- Must not be shared externally without business justification

---

### Tier 3 — Confidential

**Definition:** Sensitive business or financial data whose
unauthorised disclosure could cause material harm to UGRO Capital's
competitive position, or to the financial interests of business
entities whose data is processed.

**Examples:** GST turnover figures, GST filing regularity,
input tax credit utilization, monthly average GST turnover,
business vintage, interest rate offered to specific applicants,
approved loan amounts.

**Handling requirements:**
- Access restricted to authorised personnel with explicit
  business need — credit risk team, data science team,
  senior management
- Encryption at rest (AES-256) and in transit (TLS 1.2+)
- Logging of all access events
- Retention limited to regulatory minimum (as per RBI guidelines)
- Requires data sharing agreements before disclosure to
  third parties
- Must be anonymised or aggregated before use in reporting

---

### Tier 4 — Restricted

**Definition:** Personal data of individuals and highly sensitive
financial data whose unauthorised disclosure could cause significant
harm to data principals, including financial loss, identity theft,
discrimination, or reputational damage. This tier constitutes
personal data and sensitive personal data under the DPDP Act 2023.

**Examples:** PAN number, GSTIN (as it embeds PAN), proprietor
gender, bureau score, DPD history, write-off flag, total
outstanding amount, credit utilization ratio, average monthly
balance, bank statement data, cash deposit ratio, applicant ID
(as a unique personal identifier), default flag.

**Handling requirements:**
- Access restricted to minimum necessary personnel — strictly
  need-to-know basis with role-based access controls
- Encryption at rest (AES-256) and in transit (TLS 1.3)
- Multi-factor authentication required for system access
- All access events logged and monitored for anomalies
- Explicit, informed consent required before collection and
  processing (DPDP Act 2023, Section 6)
- Data minimisation — collect only what is necessary for the
  stated purpose
- Retention strictly limited — delete when purpose is fulfilled
  or consent is withdrawn
- Cross-border transfer prohibited without DPDP Act compliance
- Breach notification to Data Protection Board within 72 hours
  of discovery
- Must never be used in external reporting without full
  anonymisation

---

## 4. Field-Level Classification Register

| Field | Classification | Justification |
|---|---|---|
| applicant_id | Restricted | Unique personal identifier linking to an individual |
| application_date | Internal | Operational date, no personal data |
| state | Internal | Geographic region, not personally identifying |
| sector | Internal | Business category, not personally identifying |
| entity_type | Internal | Legal structure, publicly registerable information |
| business_vintage_years | Confidential | Business financial characteristic |
| proprietor_gender | Restricted | Personal characteristic of individual — protected attribute |
| pan_number | Restricted | Primary personal tax identifier under IT Act 1961 |
| gstin | Restricted | Embeds PAN — inherits Restricted classification |
| gst_registration_date | Confidential | Business registration information |
| bureau_score | Restricted | Personal financial data — creditworthiness of individual |
| active_loan_count | Restricted | Personal financial data |
| credit_inquiries_6m | Restricted | Personal financial behaviour data |
| total_outstanding_amount | Restricted | Personal financial data |
| dpd_30_count_12m | Restricted | Personal repayment behaviour — highly sensitive |
| dpd_90_count_12m | Restricted | Personal repayment behaviour — highly sensitive |
| credit_utilization_ratio | Restricted | Personal financial data |
| oldest_credit_line_age_months | Restricted | Personal financial history |
| write_off_flag | Restricted | Severe negative personal financial event |
| avg_monthly_balance | Restricted | Personal bank account data |
| avg_monthly_credit_turnover | Restricted | Personal bank account data |
| avg_monthly_debit_turnover | Restricted | Personal bank account data |
| bounce_count_6m | Restricted | Personal banking behaviour data |
| cash_deposit_ratio | Restricted | Personal banking behaviour data |
| banking_relationship_count | Confidential | Count of banking relationships |
| gst_filing_regularity_pct | Confidential | Business tax compliance behaviour |
| monthly_avg_gst_turnover | Confidential | Business revenue data |
| gst_turnover_growth_yoy | Confidential | Business financial performance |
| input_tax_credit_utilization_pct | Confidential | Business tax data |
| requested_loan_amount | Confidential | Business financial requirement |
| approved_loan_amount | Confidential | Business financial data |
| interest_rate_pct | Confidential | Pricing data — commercially sensitive |
| tenure_months | Internal | Loan structural parameter |
| loan_status | Internal | Operational outcome |
| default_flag | Restricted | Personal financial failure event — highly sensitive |

---

## 5. Roles and Responsibilities

**Data Owner** — the senior business leader accountable for a data
asset's accuracy, appropriate use, and compliance with this policy.
Responsible for approving access requests and periodic review of
classification decisions.

**Data Steward** — the technical team member responsible for
implementing the handling requirements defined by this policy for
a specific data asset. Responsible for access control configuration,
encryption implementation, and retention enforcement.

**Data Protection Officer (DPO)** — responsible for overseeing
compliance with this policy and the DPDP Act 2023. Point of contact
for data principal rights requests and regulatory inquiries.

**All Employees** — responsible for handling data in accordance
with its classification tier and reporting suspected classification
violations or data incidents immediately.

---

## 6. Policy Violations

Violations of this policy — including unauthorised access to
Restricted or Confidential data, failure to encrypt data at the
required tier, or unauthorised disclosure of personal data — will
be treated as serious disciplinary matters. Violations involving
personal data may also constitute breaches under the DPDP Act 2023,
attracting penalties of up to ₹250 crore per incident.

---

## 7. Review and Maintenance

This policy shall be reviewed annually and updated when:
- A new data source or processing activity is introduced
- A material change occurs in applicable regulation
- A data incident reveals a gap in classification or handling
- The DPDP Rules are updated or new guidance is issued

---

## Disclaimer

This policy is produced as part of an independent portfolio
assessment and is illustrative in nature. It is not affiliated
with or endorsed by UGRO Capital Limited. See project disclaimer
at `docs/disclaimer.md`.

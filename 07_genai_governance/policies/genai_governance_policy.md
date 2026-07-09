# GenAI Governance Policy
## GRO Shield Independent Governance Assessment — UGRO Capital

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital. This policy is a governance recommendation.

**Version:** 1.0
**Effective Date:** 1 January 2025
**Next Review:** 1 January 2026
**Owner:** Chief Data Officer
**Approved By:** Board Risk Committee (recommended)

---

## 1. Purpose and Scope

### 1.1 Purpose
This policy governs the development, deployment, and monitoring of
Generative AI (GenAI) systems at UGRO Capital. It establishes specific
controls for GenAI risks that are distinct from predictive AI risks —
particularly hallucination, unbounded output space, PII leakage, prompt
injection, and regulatory non-compliance in customer-facing applications.

### 1.2 Scope
This policy applies to:
- All GenAI models used in customer-facing applications including
  chatbots, virtual assistants, and automated communication systems
- All internal GenAI tools used by staff for document generation,
  code assistance, or decision support
- Third-party GenAI APIs integrated into UGRO Capital systems
- Any system that generates free-form text, images, or other content
  using a large language model

### 1.3 Relationship to Other Policies
This policy operates alongside:
- Responsible AI Policy (Module 6)
- DPDP Act Compliance Framework (Module 3)
- AI Incident Response Procedure (Module 6)
- Data Classification Policy (Module 2)

---

## 2. GenAI Risk Taxonomy

GenAI systems present a distinct risk profile from predictive AI.
The following risk categories must be assessed for every GenAI deployment.

### 2.1 Hallucination Risk
GenAI models may generate confident, fluent, and entirely false
statements — including incorrect interest rates, wrong eligibility
criteria, fabricated regulatory requirements, or non-existent product
features. In a financial services context, hallucinated information
given to a borrower may constitute mis-selling or misleading conduct
under RBI Consumer Protection Framework.

**Control requirement:** Hallucination detection must be active for
all customer-facing GenAI outputs. Any response containing uncertainty
indicators must be flagged and a verification disclaimer appended.
High-stakes outputs (loan amounts, interest rates, eligibility
decisions) must be verified against a structured knowledge base
before delivery.

### 2.2 PII Leakage Risk
GenAI models may reproduce PII from their context window in outputs —
including Aadhaar numbers, PAN numbers, account details, or transaction
history shared by the user. Under DPDP Act 2023, inadvertent PII
disclosure in model outputs constitutes a data breach.

**Control requirement:** PII scanning must run on both user inputs
(before entering LLM context) and model outputs (before delivery to
user). Aadhaar, PAN, and GSTIN must be redacted at both layers.
Audit logs must record that PII was detected without storing the
actual PII values — data minimisation principle.

### 2.3 Topic Boundary Risk
Customer-facing chatbots may be manipulated into providing advice
outside their intended scope — investment advice, legal guidance,
medical information, or competitor analysis. Providing unlicensed
financial advice constitutes a regulatory risk under SEBI and RBI
frameworks.

**Control requirement:** Topic boundary enforcement must be active
for all customer-facing GenAI deployments. A defined allowed-topic
list must be maintained and reviewed quarterly. Off-topic requests
must be blocked and redirected to appropriate channels.

### 2.4 Prompt Injection Risk
Malicious users may attempt to override system instructions through
carefully crafted inputs — instructing the model to ignore its
guidelines, reveal its system prompt, or perform prohibited actions.

**Control requirement:** System prompts must not be disclosed to
users. Input sanitisation must remove or neutralise common injection
patterns. Unusual instruction-like inputs must be logged for security
review. Regular red-team testing of prompt injection resistance
must be conducted quarterly.

### 2.5 Regulatory Compliance Risk
GenAI outputs in financial services may inadvertently constitute
unlicensed investment advice, discriminatory lending guidance, or
misleading financial promotions — all of which carry regulatory
consequences under RBI, SEBI, and ASCI frameworks.

**Control requirement:** All customer-facing GenAI responses must
be constrained to factual product information. The system must not
make lending decisions, provide personalised financial advice, or
make statements that could constitute a financial promotion without
regulatory clearance.

---

## 3. Guardrail Requirements

All customer-facing GenAI systems must implement the following
guardrail layers before deployment. This is a mandatory pre-deployment
checklist, not a recommendation.

### Layer 1 — Input PII Scanning
- Scan all user inputs for Aadhaar, PAN, GSTIN, and other PII
- Redact detected PII before passing to LLM context
- Log detection event (type and count, not value) to audit log
- Alert compliance team if PII detection rate exceeds 15% of requests

### Layer 2 — Topic Boundary Enforcement
- Maintain approved topic list reviewed quarterly by Compliance
- Block and redirect all off-topic requests
- Log all topic violations to audit log
- Alert if topic violation rate exceeds 20% (may indicate adversarial use)

### Layer 3 — Output PII Scanning
- Scan all LLM outputs for PII before delivery to user
- Redact any PII found in outputs
- Log detection event — PII in output is higher severity than input
  (indicates potential context leakage)

### Layer 4 — Hallucination Detection
- Flag outputs containing uncertainty language indicators
- Append verification disclaimer to flagged responses
- Do not deliver unverified factual claims about rates, amounts,
  or eligibility without a knowledge-base cross-check

### Layer 5 — Audit Logging
- Log every request and response with: timestamp, session ID, user ID,
  guardrails triggered, PII detection results, token count, cost
- Retain audit logs for minimum 3 years (RBI record-keeping requirements)
- Audit logs must be immutable — append-only, no deletion
- PII values must never be stored in audit logs

---

## 4. Approved and Prohibited GenAI Use Cases

### 4.1 Approved Use Cases

| Use Case | Risk Level | Required Controls |
|----------|-----------|------------------|
| MSME loan product information chatbot | Medium | All 5 guardrail layers |
| Internal document summarisation (non-PII) | Low | PII scan + audit log |
| Code assistance for Data Science team | Low | Audit log; no production data |
| Automated rejection letter generation | High | Human review + template constraints |
| FAQ response generation | Low | Topic boundary + hallucination detection |

### 4.2 Prohibited Use Cases

The following GenAI use cases are explicitly prohibited without
Board Risk Committee approval and regulatory legal review:

1. **Automated credit decisions** — GenAI must not make or explain
   credit approval/rejection decisions autonomously
2. **Personalised financial advice** — GenAI must not provide
   advice tailored to an individual's financial situation
3. **Processing of Aadhaar data in LLM context** — Aadhaar is
   sensitive personal data under DPDP Act 2023; must be redacted
   before any LLM processing
4. **Customer impersonation or synthetic identity** — GenAI must
   not generate content that impersonates real individuals
5. **Training on customer data without consent** — LLM fine-tuning
   on UGRO Capital customer data requires explicit DPDP Act consent
6. **Unmonitored production deployment** — no GenAI system may run
   in production without active observability and audit logging

---

## 5. Data Governance for GenAI

### 5.1 Training Data
- Customer PII must not be used for LLM training or fine-tuning
  without explicit, granular DPDP Act consent
- Any fine-tuning dataset must pass data quality assessment
  (minimum DQ score 90/100)
- Training data lineage must be documented in the data catalogue

### 5.2 Context Window Management
- Sensitive data (Aadhaar, PAN, account numbers) must be redacted
  before inclusion in LLM context window
- Context windows must not retain information across sessions
  unless explicit user consent is obtained
- Session data must be purged after session end

### 5.3 Model Selection
- Only approved LLM providers may be used in production
- Provider data processing agreements must be reviewed by Legal
  and DPO before deployment
- Data residency requirements must be confirmed — customer data
  must not leave India without RBI and DPDP Act clearance

---

## 6. Monitoring and Observability

### 6.1 Required Metrics
The following metrics must be monitored and reported monthly to
the Model Risk Committee:

| Metric | Warning Threshold | Critical Threshold |
|--------|-----------------|-------------------|
| PII detection rate (input) | > 10% | > 20% |
| Topic violation rate | > 15% | > 30% |
| Hallucination flag rate | > 25% | > 50% |
| Output PII detection rate | > 2% | > 5% |
| Average cost per request | > $0.01 | > $0.05 |
| Monthly total cost | > $500 | > $2,000 |

### 6.2 Observability Dashboard
A real-time observability dashboard must be maintained showing
all metrics above. The dashboard must be accessible to the
Compliance team without requiring technical access to raw logs.

### 6.3 Incident Escalation
- PII in output detected → immediate P2 incident (Section 5 of
  AI Incident Response Procedure)
- Topic violation rate > 30% → P2 incident (potential adversarial use)
- Hallucination flag rate > 50% → P2 incident (model degradation)
- Any confirmed regulatory non-compliance in output → P1 incident

---

## 7. NIST AI 600-1 Alignment

This policy is aligned with NIST AI 600-1 (Generative AI Profile,
July 2024) — the NIST framework specifically addressing GenAI risks.
Key alignments:

| NIST AI 600-1 Risk | GRO Shield Control |
|-------------------|-------------------|
| CBRN Information | Topic boundary enforcement |
| Confabulation (Hallucination) | Hallucination detection layer |
| Data Privacy | PII scanner — input and output |
| Human-AI Configuration | Human escalation path requirement |
| Information Integrity | Knowledge-base verification requirement |
| Harmful Bias | Topic boundary + audit logging |
| Obscured System Provenance | Disclosure that user is speaking with AI |

See `nist_ai_600_1_assessment.md` for full assessment.

---

## 8. Roles and Responsibilities

| Role | GenAI Responsibility |
|------|---------------------|
| CDO | Policy owner; approve new GenAI use cases |
| DPO | DPDP Act compliance for GenAI data processing |
| Data Science Lead | Implement guardrail system; maintain dashboard |
| Compliance Officer | Monthly metrics review; incident escalation |
| Legal | LLM provider agreements; regulatory compliance review |
| Model Risk Committee | Quarterly GenAI risk review |

---

## 9. Policy Review and Updates

This policy must be reviewed:
- Annually by the CDO and Compliance team
- When a new GenAI system is proposed for deployment
- When NIST AI 600-1 or applicable regulation is updated
- Following any P1 or P2 GenAI incident

---

*GenAI Governance Policy v1.0*
*Aligned with: NIST AI 600-1 (2024), DPDP Act 2023,*
*RBI Consumer Protection Framework, EU AI Act.*
*GRO Shield Independent Governance Assessment, January 2025.*

# NIST AI 600-1 Assessment
## Generative AI Profile — UGRO Capital Hypothetical MSME Chatbot

> **Disclaimer:** This is an independent external assessment built from
> publicly available information and synthetic data. Not affiliated with
> UGRO Capital.

**Framework:** NIST AI 600-1 (July 2024) — Artificial Intelligence
Risk Management Framework: Generative AI Profile
**System Assessed:** UGRO Capital Hypothetical MSME Customer Support Chatbot
**Version:** 1.0
**Date:** July 2026

---

## About NIST AI 600-1

NIST AI 600-1 is a companion resource to the NIST AI RMF 1.0,
published July 2024, specifically addressing the unique risks of
generative AI systems. It identifies 12 GenAI-specific risk categories
and maps them to suggested actions across the GOVERN, MAP, MEASURE,
and MANAGE functions.

This assessment evaluates the GRO Shield guardrail system against
all 12 NIST AI 600-1 risk categories.

---

## Risk Assessment — All 12 NIST AI 600-1 Categories

### 1. CBRN Information
**Definition:** GenAI providing information that could be used to
create chemical, biological, radiological, or nuclear weapons.

**Relevance to UGRO Chatbot:** Low — financial services chatbot
with topic boundary enforcement. No CBRN information would be
within scope of MSME lending queries.

**Control Implemented:** Topic boundary enforcement blocks all
off-topic requests including any that could relate to harmful
information. Tested in guardrail demo — medical and non-financial
queries blocked.

**Residual Risk:** Negligible
**Status:** ✅ Adequately Controlled

---

### 2. Confabulation (Hallucination)
**Definition:** GenAI generating false information presented with
apparent confidence — incorrect facts, fabricated sources, invented
product details.

**Relevance to UGRO Chatbot:** High — a chatbot stating incorrect
interest rates, wrong eligibility criteria, or fabricated regulatory
requirements to an MSME borrower constitutes misleading conduct
under RBI Consumer Protection Framework.

**Control Implemented:**
- Hallucination detection layer flags outputs containing uncertainty
  indicators (15 patterns including "I think", "probably", "I'm not sure")
- Verification disclaimer appended to all flagged responses
- In guardrail demo: 4 of 15 requests (26.7%) triggered hallucination
  flag — consistent with expected rate for templated responses

**Gap:** Heuristic-only detection — does not semantically verify
factual accuracy against a knowledge base. A production system
should cross-check factual claims (rates, amounts, dates) against
a structured product knowledge base before delivery.

**Residual Risk:** Medium
**Status:** ⚠️ Partially Controlled — knowledge-base verification needed

---

### 3. Data Privacy
**Definition:** GenAI exposing, reproducing, or leaking personal
data — including data shared by users in the conversation or
data memorised from training.

**Relevance to UGRO Chatbot:** Critical — MSME borrowers routinely
share Aadhaar, PAN, and GSTIN in loan-related conversations.
Under DPDP Act 2023, Aadhaar is sensitive personal data. Any
reproduction in model output constitutes a data breach.

**Control Implemented:**
- PII scanner active on both input and output
- Aadhaar, PAN, GSTIN detected and redacted before LLM context
- Output scan catches any PII the model attempts to repeat
- Audit log records detection events without storing PII values
- In guardrail demo: 4 of 15 requests (26.7%) contained input PII —
  all successfully redacted

**Gap:** Scanner covers structured PII (Aadhaar/PAN/GSTIN) but not
unstructured PII (account numbers, addresses, phone numbers).
Extend scanner to cover additional PII types in production.

**Residual Risk:** Low-Medium
**Status:** ⚠️ Substantially Controlled — scanner scope extension needed

---

### 4. Human-AI Configuration
**Definition:** Users not understanding they are interacting with
an AI system, or AI systems not appropriately deferring to humans
for high-stakes decisions.

**Relevance to UGRO Chatbot:** High — if borrowers believe they
are speaking with a human loan officer, they may place inappropriate
reliance on chatbot responses for credit decisions.

**Control Implemented:**
- System designed to redirect high-stakes queries to human team
- Off-topic and borderline queries blocked and redirected to
  customer support number
- Hallucination disclaimer identifies response as AI-generated
  when uncertainty detected

**Gap:** No explicit AI identity disclosure at session start.
NIST AI 600-1 recommends proactive disclosure that the user is
interacting with an AI. EU AI Act Article 52 mandates disclosure
for AI systems interacting with humans.

**Residual Risk:** Medium
**Status:** ⚠️ Partially Controlled — session-start AI disclosure needed

---

### 5. Information Integrity
**Definition:** GenAI generating or amplifying false, misleading,
or manipulated information that affects decision-making.

**Relevance to UGRO Chatbot:** High — incorrect product information
provided to borrowers may affect their financial decisions and
constitute mis-selling.

**Control Implemented:**
- Topic boundary limits responses to loan-related factual information
- Hallucination detection flags uncertain outputs
- Mock responses use conservative, factual language

**Gap:** No structured knowledge base verification. Responses are
template-based in the demo — production LLM responses would require
grounding against current product data (rates, eligibility criteria,
fees) that may change.

**Residual Risk:** Medium
**Status:** ⚠️ Partially Controlled — RAG or knowledge-base grounding needed

---

### 6. Information Security
**Definition:** GenAI systems being exploited to compromise
cybersecurity — prompt injection, system prompt extraction,
jailbreaking, or use as an attack vector.

**Relevance to UGRO Chatbot:** Medium — financial services chatbots
are targets for prompt injection attacks designed to extract
system prompts, bypass guardrails, or obtain unauthorised information.

**Control Implemented:**
- Topic boundary enforcement blocks instruction-like off-topic inputs
- Session isolation — no cross-session data persistence
- Audit logging captures all inputs for security review

**Gap:** No explicit prompt injection pattern detection. No red-team
testing conducted. System prompt not hardened against extraction.
Quarterly adversarial testing recommended.

**Residual Risk:** Medium
**Status:** ⚠️ Partially Controlled — prompt injection hardening needed

---

### 7. Intellectual Property
**Definition:** GenAI reproducing copyrighted content, trade secrets,
or proprietary information without authorisation.

**Relevance to UGRO Chatbot:** Low — chatbot responses are constrained
to product information. Low risk of reproducing copyrighted material
in MSME lending query responses.

**Control Implemented:** Topic boundary enforcement limits response
scope. Template-based responses reduce reproduction risk.

**Residual Risk:** Low
**Status:** ✅ Adequately Controlled for current scope

---

### 8. Obscured System Provenance
**Definition:** Lack of transparency about what AI system is being
used, how it was trained, or what its limitations are.

**Relevance to UGRO Chatbot:** Medium — borrowers and regulators
should be able to understand what AI system is handling their
queries, particularly given DPDP Act transparency obligations.

**Control Implemented:**
- GRO Shield observability dashboard provides full audit trail
- Guardrail system logs all requests with metadata
- GenAI Governance Policy documents system architecture

**Gap:** No public-facing disclosure of AI system use in chatbot.
No model card for the GenAI system. RBI and DPDP Act both support
transparency about automated processing of personal data.

**Residual Risk:** Medium
**Status:** ⚠️ Partially Controlled — public disclosure and model card needed

---

### 9. Harmful Bias and Homogenisation
**Definition:** GenAI systems producing outputs that discriminate
against protected groups or that homogenise perspectives in harmful ways.

**Relevance to UGRO Chatbot:** Medium — if the chatbot provides
different quality or accuracy of information to different user groups
(based on language, literacy, or query sophistication), it creates
an equity gap in financial access.

**Control Implemented:**
- Multi-language support field captured in audit log
- Topic boundary enforcement applied uniformly across all users
- Audit log enables analysis of response quality by user segment

**Gap:** No formal bias testing of chatbot responses across user
groups. No assessment of whether responses are equally accessible
to users with varying financial literacy. Hindi and regional language
support not implemented.

**Residual Risk:** Medium
**Status:** ⚠️ Partially Controlled — bias testing and multilingual support needed

---

### 10. Value Chain and Component Integration
**Definition:** Risks arising from third-party LLM providers,
APIs, or components integrated into the GenAI system.

**Relevance to UGRO Chatbot:** High — UGRO Capital would rely on
a third-party LLM provider (OpenAI, Anthropic, Google, or equivalent)
for the underlying language model. Data processing agreements, data
residency, and model updates all introduce third-party risk.

**Control Implemented:**
- GRO Shield guardrail system wraps any underlying LLM — provider
  is abstracted behind the guardrail API
- Mock LLM in demo — no actual third-party data transmission

**Gap:** No LLM provider selection policy. No data processing
agreement template. No assessment of whether customer data sent
to third-party LLM APIs would constitute a cross-border data
transfer under DPDP Act 2023 Chapter III.

**Residual Risk:** High
**Status:** ⚠️ Not Controlled — provider governance framework needed

---

### 11. Dangerous or Violent Recommendations
**Definition:** GenAI providing recommendations that could cause
physical harm to users or third parties.

**Relevance to UGRO Chatbot:** Low — financial services chatbot
with strict topic boundary enforcement. No dangerous content
would be within scope of MSME lending queries.

**Control Implemented:** Topic boundary enforcement blocks all
non-lending queries including any that could relate to harmful
content. Medical and personal advice queries blocked in demo.

**Residual Risk:** Negligible
**Status:** ✅ Adequately Controlled

---

### 12. Data Privacy — Training Data
**Definition:** GenAI training data containing personal information
that may be memorised and reproduced in outputs.

**Relevance to UGRO Chatbot:** High if fine-tuned on customer data.
Medium for base model usage — base models may have memorised
publicly available financial information.

**Control Implemented:**
- GRO Shield policy explicitly prohibits fine-tuning on customer
  PII without DPDP Act consent
- Output PII scanner catches any memorised PII in model outputs
- No customer data used in demo guardrail system

**Gap:** No assessment of whether the selected base LLM was
trained on any data that could constitute a DPDP Act privacy risk.
Vendor transparency on training data composition required before
production deployment.

**Residual Risk:** Medium
**Status:** ⚠️ Partially Controlled — vendor training data assessment needed

---

## Overall Assessment Summary

| Risk Category | Relevance | Status | Residual Risk |
|--------------|-----------|--------|---------------|
| 1. CBRN Information | Low | ✅ Controlled | Negligible |
| 2. Confabulation | High | ⚠️ Partial | Medium |
| 3. Data Privacy (outputs) | Critical | ⚠️ Substantial | Low-Medium |
| 4. Human-AI Configuration | High | ⚠️ Partial | Medium |
| 5. Information Integrity | High | ⚠️ Partial | Medium |
| 6. Information Security | Medium | ⚠️ Partial | Medium |
| 7. Intellectual Property | Low | ✅ Controlled | Low |
| 8. Obscured Provenance | Medium | ⚠️ Partial | Medium |
| 9. Harmful Bias | Medium | ⚠️ Partial | Medium |
| 10. Value Chain | High | ⚠️ Not Controlled | High |
| 11. Dangerous Content | Low | ✅ Controlled | Negligible |
| 12. Training Data Privacy | Medium | ⚠️ Partial | Medium |

**Priority gaps for production readiness:**
1. LLM provider governance framework (Risk 10 — High residual)
2. Knowledge-base grounding for factual verification (Risk 2, 5)
3. Explicit AI identity disclosure at session start (Risk 4)
4. Prompt injection hardening and red-team testing (Risk 6)
5. PII scanner scope extension beyond Aadhaar/PAN/GSTIN (Risk 3)

---

*Assessment based on NIST AI 600-1 (July 2024).*
*GRO Shield Independent Governance Assessment, July 2026.*

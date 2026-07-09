"""
Module 7: GenAI Governance
guardrail_system.py — FastAPI guardrail system for UGRO Capital
hypothetical customer support chatbot.

Every request passes through five guardrail layers:
  1. PII scanning — detect and redact Aadhaar/PAN/GSTIN in input
  2. Topic boundary — block off-topic requests
  3. Mock LLM response — simulate chatbot response
  4. PII scanning — redact any PII in model output
  5. Hallucination flag — flag uncertain or fabricated content

All requests and responses are audit logged to CSV.
Token usage is tracked per request for cost monitoring.

Run from project root:
    uvicorn 07_genai_governance.guardrails.src.guardrail_system:app --reload
    or for demo:
    python3 07_genai_governance/guardrails/src/guardrail_system.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath("07_genai_governance/guardrails/src"))

import re
import csv
import json
import random
import hashlib
from datetime import datetime
from typing import Optional
from pii_scanner import scan_text, get_audit_summary

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not available — running in demo mode")


# ── Constants ─────────────────────────────────────────────────────────────────
AUDIT_LOG_PATH = "07_genai_governance/data/audit_log.csv"
COST_LOG_PATH  = "07_genai_governance/data/cost_log.csv"

# Approximate token costs (GPT-4 class model pricing as reference)
COST_PER_INPUT_TOKEN  = 0.00003   # $0.03 per 1K tokens
COST_PER_OUTPUT_TOKEN = 0.00006   # $0.06 per 1K tokens

# Topic boundary — allowed topics for UGRO Capital MSME chatbot
ALLOWED_TOPICS = [
    "loan", "msme", "interest", "emi", "repayment", "eligibility",
    "application", "document", "credit", "score", "bureau", "gst",
    "turnover", "collateral", "tenure", "disbursal", "sanction",
    "ugro", "noc", "foreclosure", "prepayment", "overdraft",
    "working capital", "term loan", "balance", "outstanding",
    "statement", "account", "branch", "rate", "fee", "charge",
    "apply", "status", "track", "grievance", "complaint"
]

# Hallucination indicators — phrases that suggest uncertain or
# fabricated content in model output
HALLUCINATION_INDICATORS = [
    "i think", "i believe", "i'm not sure", "probably",
    "might be", "could be", "i cannot verify", "as far as i know",
    "i'm not certain", "you should check", "i may be wrong",
    "approximately", "roughly", "around", "i don't have access",
    "my information may be outdated"
]


# ── Request/Response Models ───────────────────────────────────────────────────
# Defined only when FastAPI/Pydantic is available

if FASTAPI_AVAILABLE:
    class ChatRequest(BaseModel):
        session_id:  str
        user_id:     str
        message:     str
        language:    Optional[str] = "en"

    class ChatResponse(BaseModel):
        session_id:          str
        response:            str
        guardrails_triggered: list
        pii_detected_input:  bool
        pii_detected_output: bool
        topic_allowed:       bool
        hallucination_flag:  bool
        tokens_used:         dict
        cost_usd:            float
        request_id:          str


# ── Guardrail Functions ───────────────────────────────────────────────────────

def check_topic_boundary(text: str) -> tuple:
    """
    Check if the message is within allowed MSME lending topics.
    Returns (is_allowed: bool, matched_topics: list).

    Off-topic examples: stock tips, personal medical advice,
    competitor product comparisons, legal advice, political content.
    """
    text_lower = text.lower()
    matched = [t for t in ALLOWED_TOPICS if t in text_lower]
    is_allowed = len(matched) > 0
    return is_allowed, matched


def estimate_tokens(text: str) -> int:
    """
    Rough token estimation: ~4 characters per token (GPT-style tokenisation).
    For production, use tiktoken or the model provider's token counter.
    """
    return max(1, len(text) // 4)


def flag_hallucination(text: str) -> tuple:
    """
    Flag model output that contains uncertainty indicators.
    Returns (is_flagged: bool, indicators_found: list).

    This is a heuristic, not a semantic hallucination detector.
    Production systems should use a dedicated hallucination detection
    model or consistency checking against a knowledge base.
    """
    text_lower = text.lower()
    found = [ind for ind in HALLUCINATION_INDICATORS if ind in text_lower]
    return len(found) > 0, found


def generate_mock_response(message: str, topic_allowed: bool) -> str:
    """
    Generate a mock chatbot response for demonstration.
    In production, this is replaced by an actual LLM API call.

    Responses are templated to be realistic for UGRO Capital's
    MSME lending context.
    """
    if not topic_allowed:
        return (
            "I'm sorry, I can only assist with questions related to "
            "UGRO Capital's MSME loan products, application process, "
            "repayment, and account queries. For other questions, "
            "please contact our customer support team at 1800-XXX-XXXX."
        )

    msg_lower = message.lower()

    if any(w in msg_lower for w in ["interest", "rate"]):
        return (
            "UGRO Capital's MSME loan interest rates typically range "
            "from 14% to 24% per annum, based on your GRO Score, "
            "business vintage, and loan amount. I think the exact rate "
            "for your profile would depend on a credit assessment — "
            "you may want to check with our credit team for a precise quote."
        )
    elif any(w in msg_lower for w in ["eligibility", "eligible", "qualify"]):
        return (
            "To be eligible for an UGRO Capital MSME loan, your business "
            "typically needs a minimum vintage of 2 years, a CIBIL score "
            "above 650, and GST registration. Loan amounts range from "
            "₹10 lakhs to ₹10 crores depending on your business profile."
        )
    elif any(w in msg_lower for w in ["document", "kyc", "required"]):
        return (
            "The documents typically required for an MSME loan application "
            "include: PAN card, Aadhaar card, GST registration certificate, "
            "last 12 months bank statements, and business registration proof. "
            "Our team will guide you through the complete list after your "
            "initial application."
        )
    elif any(w in msg_lower for w in ["status", "track", "application"]):
        return (
            "To track your loan application status, please visit our portal "
            "at ugrocapital.com or call 1800-XXX-XXXX with your application "
            "reference number. I don't have access to live application data "
            "in this chat interface."
        )
    elif any(w in msg_lower for w in ["emi", "repayment", "payment"]):
        return (
            "EMI repayments can be made via NACH auto-debit, NEFT, or "
            "through the UGRO Capital borrower portal. If you're facing "
            "repayment difficulties, please contact our collections team "
            "as soon as possible to discuss restructuring options."
        )
    else:
        return (
            "Thank you for your query about UGRO Capital's MSME loan "
            "products. I'm here to help with questions about loan "
            "eligibility, interest rates, documentation, application "
            "status, and repayment. Could you please provide more "
            "details about what you'd like to know?"
        )


# ── Audit Logging ─────────────────────────────────────────────────────────────

def init_logs():
    """Initialise audit and cost log CSV files with headers."""
    os.makedirs("07_genai_governance/data", exist_ok=True)

    if not os.path.exists(AUDIT_LOG_PATH):
        with open(AUDIT_LOG_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "request_id", "session_id", "user_id",
                "topic_allowed", "pii_input_detected", "pii_input_types",
                "pii_input_count", "pii_output_detected", "pii_output_types",
                "hallucination_flagged", "hallucination_indicators",
                "guardrails_triggered", "input_tokens", "output_tokens",
                "cost_usd", "language"
            ])

    if not os.path.exists(COST_LOG_PATH):
        with open(COST_LOG_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "request_id", "session_id",
                "input_tokens", "output_tokens",
                "input_cost_usd", "output_cost_usd", "total_cost_usd"
            ])


def log_request(request_id, session_id, user_id, topic_allowed,
                input_scan, output_scan, hallucination_flag,
                hallucination_indicators, guardrails_triggered,
                input_tokens, output_tokens, cost_usd, language):
    """Append one row to the audit log."""
    with open(AUDIT_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            request_id, session_id, user_id,
            topic_allowed,
            input_scan["pii_detected"],
            json.dumps(input_scan["pii_types_found"]),
            input_scan["finding_count"],
            output_scan["pii_detected"],
            json.dumps(output_scan["pii_types_found"]),
            hallucination_flag,
            json.dumps(hallucination_indicators),
            json.dumps(guardrails_triggered),
            input_tokens, output_tokens, cost_usd, language
        ])


def log_cost(request_id, session_id, input_tokens, output_tokens):
    """Append one row to the cost log."""
    input_cost  = input_tokens  * COST_PER_INPUT_TOKEN
    output_cost = output_tokens * COST_PER_OUTPUT_TOKEN
    total_cost  = input_cost + output_cost
    with open(COST_LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            request_id, session_id,
            input_tokens, output_tokens,
            round(input_cost, 6), round(output_cost, 6),
            round(total_cost, 6)
        ])
    return round(total_cost, 6)


# ── Core Processing Pipeline ──────────────────────────────────────────────────

def process_request(session_id: str, user_id: str,
                    message: str, language: str = "en") -> dict:
    """
    Core guardrail pipeline — runs independently of FastAPI.
    Called by both the API endpoint and the demo runner.
    """
    request_id = hashlib.md5(
        f"{session_id}{datetime.utcnow().isoformat()}".encode()
    ).hexdigest()[:12]

    guardrails_triggered = []

    # Layer 1: PII scan on input
    input_scan_result = scan_text(message)
    input_audit = get_audit_summary(input_scan_result)
    safe_input = input_scan_result.redacted_text

    if input_scan_result.pii_detected:
        guardrails_triggered.append(
            f"PII_INPUT:{','.join(input_scan_result.pii_types_found)}"
        )

    # Layer 2: Topic boundary check
    topic_allowed, matched_topics = check_topic_boundary(safe_input)
    if not topic_allowed:
        guardrails_triggered.append("TOPIC_BOUNDARY_VIOLATION")

    # Layer 3: Generate mock LLM response
    raw_response = generate_mock_response(safe_input, topic_allowed)

    # Layer 4: PII scan on output
    output_scan_result = scan_text(raw_response)
    output_audit = get_audit_summary(output_scan_result)
    safe_response = output_scan_result.redacted_text

    if output_scan_result.pii_detected:
        guardrails_triggered.append(
            f"PII_OUTPUT:{','.join(output_scan_result.pii_types_found)}"
        )

    # Layer 5: Hallucination flag
    hallucination_flag, hallucination_indicators = flag_hallucination(
        safe_response
    )
    if hallucination_flag:
        guardrails_triggered.append("HALLUCINATION_FLAG")
        safe_response += (
            "\n\n⚠️ *This response may contain uncertain information. "
            "Please verify with our customer support team before acting.*"
        )

    # Token counting and cost
    input_tokens  = estimate_tokens(message)
    output_tokens = estimate_tokens(safe_response)
    cost_usd = log_cost(request_id, session_id, input_tokens, output_tokens)

    # Audit log
    log_request(
        request_id, session_id, user_id, topic_allowed,
        input_audit, output_audit,
        hallucination_flag, hallucination_indicators,
        guardrails_triggered, input_tokens, output_tokens,
        cost_usd, language
    )

    return {
        "session_id":           session_id,
        "request_id":           request_id,
        "response":             safe_response,
        "guardrails_triggered": guardrails_triggered,
        "pii_detected_input":   input_scan_result.pii_detected,
        "pii_detected_output":  output_scan_result.pii_detected,
        "topic_allowed":        topic_allowed,
        "hallucination_flag":   hallucination_flag,
        "tokens_used": {
            "input":  input_tokens,
            "output": output_tokens,
            "total":  input_tokens + output_tokens
        },
        "cost_usd": cost_usd
    }


# ── FastAPI App ───────────────────────────────────────────────────────────────

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="GRO Shield — GenAI Guardrail System",
        description=(
            "Guardrail system for UGRO Capital hypothetical MSME "
            "customer support chatbot. Implements PII scanning, "
            "topic boundary enforcement, hallucination detection, "
            "and audit logging."
        ),
        version="1.0.0"
    )

    @app.on_event("startup")
    async def startup():
        init_logs()

    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest):
        result = process_request(
            request.session_id, request.user_id,
            request.message, request.language
        )
        return ChatResponse(**result)

    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "GRO Shield Guardrail"}

    @app.get("/audit/summary")
    async def audit_summary():
        """Return summary stats from audit log."""
        if not os.path.exists(AUDIT_LOG_PATH):
            return {"error": "No audit log found"}
        import pandas as pd
        df = pd.read_csv(AUDIT_LOG_PATH)
        return {
            "total_requests":      len(df),
            "pii_input_detected":  int(df["pii_input_detected"].sum()),
            "topic_violations":    int((~df["topic_allowed"]).sum()),
            "hallucination_flags": int(df["hallucination_flagged"].sum()),
            "total_cost_usd":      round(df["cost_usd"].sum(), 4)
        }


# ── Demo Runner ───────────────────────────────────────────────────────────────

def run_demo():
    """
    Run a set of demo requests through the guardrail pipeline
    without starting the FastAPI server. Generates audit log data
    for the observability dashboard.
    """
    init_logs()

    demo_requests = [
        # Normal loan query
        ("S001", "U001", "What is the interest rate for an MSME loan?"),
        # PII in input — Aadhaar
        ("S002", "U002", "My Aadhaar is 2345 6789 0123, can I apply?"),
        # PII in input — PAN
        ("S003", "U003", "My PAN is ABCDE1234F, check my eligibility"),
        # Off-topic — stock tips
        ("S004", "U004", "Which stocks should I buy this week?"),
        # Off-topic — medical
        ("S005", "U005", "What medicine should I take for fever?"),
        # Normal eligibility query
        ("S006", "U006", "What documents do I need for a working capital loan?"),
        # PAN + GSTIN together
        ("S007", "U007",
         "PAN ABCDE1234F GSTIN 27ABCDE1234F1Z5 what is my loan status?"),
        # Will trigger hallucination flag
        ("S008", "U008", "What is the exact interest rate for my loan?"),
        # Normal repayment query
        ("S009", "U009", "How do I make my EMI payment?"),
        # Off-topic — competitor
        ("S010", "U010", "Is Lendingkart better than UGRO Capital?"),
        # Normal application status
        ("S011", "U011", "How do I track my loan application status?"),
        # Aadhaar unspaced
        ("S012", "U012", "Aadhaar 234567890123 please check my account"),
        # Normal GST query
        ("S013", "U013",
         "My GST turnover is 50 lakhs, am I eligible for a term loan?"),
        # Off-topic — personal finance
        ("S014", "U014", "Should I invest in mutual funds or FD?"),
        # Normal foreclosure query
        ("S015", "U015", "What are the foreclosure charges for prepayment?"),
    ]

    print("=" * 60)
    print("GRO SHIELD — GUARDRAIL SYSTEM DEMO")
    print("=" * 60)

    for session_id, user_id, message in demo_requests:
        result = process_request(session_id, user_id, message)
        print(f"\nSession: {session_id} | User: {user_id}")
        print(f"Input:   {message[:70]}{'...' if len(message)>70 else ''}")
        print(f"Topic:   {'✅ Allowed' if result['topic_allowed'] else '🚫 Blocked'}")
        print(f"PII In:  {'⚠ ' + str(result['pii_detected_input']) if result['pii_detected_input'] else '✓ None'}")
        print(f"Halluc:  {'⚠ Flagged' if result['hallucination_flag'] else '✓ OK'}")
        print(f"Guards:  {result['guardrails_triggered'] if result['guardrails_triggered'] else 'None'}")
        print(f"Cost:    ${result['cost_usd']:.6f} | "
              f"Tokens: {result['tokens_used']['total']}")

    print(f"\n{'='*60}")
    print(f"Audit log: {AUDIT_LOG_PATH}")
    print(f"Cost log:  {COST_LOG_PATH}")
    print(f"Requests processed: {len(demo_requests)}")


if __name__ == "__main__":
    run_demo()

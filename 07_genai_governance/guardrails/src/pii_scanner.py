"""
Module 7: GenAI Governance
pii_scanner.py — PII detection and redaction for UGRO Capital chatbot.

Detects and redacts three PII types critical to Indian MSME lending:
  - Aadhaar number (UIDAI — sensitive personal data under DPDP Act 2023)
  - PAN number (Income Tax Department — KYC identifier)
  - GSTIN (GST Network — business identifier)

Design: regex-based (not ML) because these are structured formats
with deterministic patterns. Regex gives zero false negatives on
valid format matches and is fully auditable.

DPDP Act 2023 relevance:
  - Aadhaar = sensitive personal data (Section 2(t))
  - PAN = personal data requiring protection
  - GSTIN = business identifier linked to proprietor identity
"""

import re
from dataclasses import dataclass, field
from typing import Optional


# ── PII Pattern Definitions ───────────────────────────────────────────────────

# Aadhaar: 12 digits, optionally space/hyphen separated in groups of 4
# Valid: 1234 5678 9012 | 123456789012 | 1234-5678-9012
# First digit cannot be 0 or 1 (UIDAI specification)
AADHAAR_PATTERN = re.compile(
    r'\b[2-9]\d{3}[\s\-]?\d{4}[\s\-]?\d{4}\b'
)

# PAN: 5 uppercase letters, 4 digits, 1 uppercase letter
# Valid: ABCDE1234F | UGROP1234K
# 4th character encodes entity type (P=individual, C=company, etc.)
PAN_PATTERN = re.compile(
    r'\b[A-Z]{5}[0-9]{4}[A-Z]\b'
)

# GSTIN: 15 characters
# Format: 2-digit state code + 10-char PAN + entity number + Z + check digit
# Valid: 27ABCDE1234F1Z5 | 29UGROP1234K1Z3
GSTIN_PATTERN = re.compile(
    r'\b[0-3][0-9][A-Z]{5}[0-9]{4}[A-Z][0-9A-Z]Z[0-9A-Z]\b'
)

PATTERNS = {
    "AADHAAR": AADHAAR_PATTERN,
    "PAN":     PAN_PATTERN,
    "GSTIN":   GSTIN_PATTERN,
}

REDACTION_PLACEHOLDERS = {
    "AADHAAR": "[AADHAAR_REDACTED]",
    "PAN":     "[PAN_REDACTED]",
    "GSTIN":   "[GSTIN_REDACTED]",
}


# ── Data Structures ───────────────────────────────────────────────────────────

@dataclass
class PIIFinding:
    """A single PII detection finding."""
    pii_type:     str    # AADHAAR | PAN | GSTIN
    matched_text: str    # the actual matched string
    start:        int    # character position in original text
    end:          int    # character position in original text
    redacted_as:  str    # replacement placeholder


@dataclass
class ScanResult:
    """Result of scanning a single text string."""
    original_text:  str
    redacted_text:  str
    findings:       list = field(default_factory=list)
    pii_detected:   bool = False
    finding_count:  int  = 0
    pii_types_found: list = field(default_factory=list)


# ── Core Scanner Functions ────────────────────────────────────────────────────

def scan_text(text: str) -> ScanResult:
    """
    Scan text for PII and return findings with redacted version.

    Detection and redaction are performed in a single pass.
    Findings include type, position, and matched text for audit logging.
    The redacted_text replaces all PII with safe placeholders.

    Note: matched_text is stored in findings for audit purposes —
    the audit log records THAT PII was found, not WHAT it was.
    The redacted_text is what gets passed to/from the LLM.
    """
    if not text or not isinstance(text, str):
        return ScanResult(
            original_text=text or "",
            redacted_text=text or "",
            pii_detected=False
        )

    findings = []
    redacted = text

    # Scan for each PII type
    for pii_type, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            finding = PIIFinding(
                pii_type=pii_type,
                matched_text=match.group(),
                start=match.start(),
                end=match.end(),
                redacted_as=REDACTION_PLACEHOLDERS[pii_type]
            )
            findings.append(finding)

    # Apply redactions (replace in text — work on original to avoid
    # position drift from multiple replacements)
    for pii_type, pattern in PATTERNS.items():
        redacted = pattern.sub(
            REDACTION_PLACEHOLDERS[pii_type], redacted
        )

    pii_types_found = list({f.pii_type for f in findings})

    return ScanResult(
        original_text=text,
        redacted_text=redacted,
        findings=findings,
        pii_detected=len(findings) > 0,
        finding_count=len(findings),
        pii_types_found=pii_types_found
    )


def scan_input_and_output(
    user_input: str,
    model_output: str
) -> tuple:
    """
    Scan both user input and model output.
    Returns (input_result, output_result).

    Both directions must be scanned:
    - Input: user may share their own Aadhaar/PAN — must not enter LLM context
    - Output: LLM may hallucinate or repeat PII from context — must be redacted
    """
    input_result  = scan_text(user_input)
    output_result = scan_text(model_output)
    return input_result, output_result


def get_audit_summary(result: ScanResult) -> dict:
    """
    Return audit-safe summary — records THAT PII was found,
    not WHAT it was. Safe to write to audit logs.
    """
    return {
        "pii_detected":    result.pii_detected,
        "finding_count":   result.finding_count,
        "pii_types_found": result.pii_types_found,
        "text_length":     len(result.original_text),
    }


# ── Self-test ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    test_cases = [
        {
            "description": "Aadhaar number — spaced format",
            "text": "My Aadhaar is 2345 6789 0123 and I need a loan."
        },
        {
            "description": "Aadhaar number — unspaced format",
            "text": "Aadhaar: 234567890123"
        },
        {
            "description": "PAN number",
            "text": "My PAN is ABCDE1234F for KYC verification."
        },
        {
            "description": "GSTIN",
            "text": "Our GSTIN is 27ABCDE1234F1Z5 registered in Maharashtra."
        },
        {
            "description": "Multiple PII types",
            "text": "PAN ABCDE1234F, Aadhaar 2345 6789 0123, GSTIN 27ABCDE1234F1Z5"
        },
        {
            "description": "No PII",
            "text": "What is the interest rate for an MSME loan of 10 lakhs?"
        },
        {
            "description": "PAN in lowercase — should NOT match",
            "text": "my pan is abcde1234f"
        },
    ]

    print("=" * 60)
    print("PII SCANNER — SELF TEST")
    print("=" * 60)

    for tc in test_cases:
        result = scan_text(tc["text"])
        print(f"\nTest: {tc['description']}")
        print(f"  Input:    {tc['text']}")
        print(f"  Redacted: {result.redacted_text}")
        print(f"  PII found: {result.pii_detected} "
              f"| Types: {result.pii_types_found} "
              f"| Count: {result.finding_count}")

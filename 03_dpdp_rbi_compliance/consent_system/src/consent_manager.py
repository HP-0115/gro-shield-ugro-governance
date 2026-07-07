"""
consent_manager.py
Implements a consent lifecycle management system for UGRO Capital's
three data pull categories: bureau, bank_statement, and gst.

Tracks consent given, withdrawn, and audit history for each
applicant and data category, aligned to DPDP Act 2023 Section 6.

Usage:
    python consent_manager.py
"""

import json
import uuid
from datetime import datetime
from enum import Enum


class DataCategory(Enum):
    BUREAU = "bureau"
    BANK_STATEMENT = "bank_statement"
    GST = "gst"


class ConsentStatus(Enum):
    GIVEN = "given"
    WITHDRAWN = "withdrawn"
    NOT_GIVEN = "not_given"



class ConsentManager:
    """
    Manages consent lifecycle for UGRO Capital loan applicants.
    Tracks consent given, withdrawn, and full audit history
    per applicant per data category.
    """

    def __init__(self):
        # In production this would be a database.
        # For demonstration we use an in-memory dictionary.
        self.consent_records = {}
        self.audit_log = []

    def _timestamp(self):
        return datetime.utcnow().isoformat() + "Z"

    def _get_or_create_record(self, applicant_id):
        if applicant_id not in self.consent_records:
            self.consent_records[applicant_id] = {
                "applicant_id": applicant_id,
                "created_at": self._timestamp(),
                "categories": {
                    cat.value: {
                        "status": ConsentStatus.NOT_GIVEN.value,
                        "given_at": None,
                        "withdrawn_at": None,
                        "consent_id": None,
                    }
                    for cat in DataCategory
                },
            }
        return self.consent_records[applicant_id]

    def give_consent(self, applicant_id, category: DataCategory, purpose: str):
        """
        Records consent given by an applicant for a specific data category.
        Generates a unique consent_id for audit purposes.
        """
        record = self._get_or_create_record(applicant_id)
        consent_id = str(uuid.uuid4())
        timestamp = self._timestamp()

        record["categories"][category.value] = {
            "status": ConsentStatus.GIVEN.value,
            "given_at": timestamp,
            "withdrawn_at": None,
            "consent_id": consent_id,
            "purpose": purpose,
        }

        self.audit_log.append({
            "event": "CONSENT_GIVEN",
            "applicant_id": applicant_id,
            "category": category.value,
            "consent_id": consent_id,
            "purpose": purpose,
            "timestamp": timestamp,
        })

        return consent_id

    def withdraw_consent(self, applicant_id, category: DataCategory):
        """
        Records consent withdrawal for a specific data category.
        Does not delete existing records -- withdrawal means stop
        future processing and delete data, not undo past processing.
        """
        record = self._get_or_create_record(applicant_id)
        timestamp = self._timestamp()

        current = record["categories"][category.value]
        if current["status"] != ConsentStatus.GIVEN.value:
            return {
                "success": False,
                "reason": f"No active consent found for {category.value}",
            }

        current["status"] = ConsentStatus.WITHDRAWN.value
        current["withdrawn_at"] = timestamp

        self.audit_log.append({
            "event": "CONSENT_WITHDRAWN",
            "applicant_id": applicant_id,
            "category": category.value,
            "consent_id": current["consent_id"],
            "timestamp": timestamp,
        })

        return {
            "success": True,
            "withdrawn_at": timestamp,
            "action_required": (
                f"Delete {category.value} data for {applicant_id} "
                f"and cease all further processing."
            ),
        }

    def check_consent(self, applicant_id, category: DataCategory):
        """
        Returns True only if active consent exists for this
        applicant and data category. Used as a gate before
        any data pull is triggered.
        """
        if applicant_id not in self.consent_records:
            return False
        status = (
            self.consent_records[applicant_id]
            ["categories"][category.value]["status"]
        )
        return status == ConsentStatus.GIVEN.value

    def get_consent_summary(self, applicant_id):
        """
        Returns a full consent summary for an applicant --
        satisfies the data principal's right to access
        under DPDP Act 2023 Section 11.
        """
        if applicant_id not in self.consent_records:
            return {"applicant_id": applicant_id, "message": "No records found"}
        return self.consent_records[applicant_id]

    def export_audit_log(self, path):
        """
        Exports the full audit log to JSON.
        Audit logs are evidence of consent management
        for regulatory purposes.
        """
        with open(path, "w") as f:
            json.dump(self.audit_log, f, indent=2)
        print(f"Audit log exported -> {path} ({len(self.audit_log)} events)")



def demo():
    """
    Demonstrates a realistic consent lifecycle for one applicant:
    1. Applicant applies and gives consent for all three data pulls
    2. System checks consent before each pull
    3. Applicant later withdraws bank statement consent
    4. System correctly blocks a subsequent bank statement pull
    5. Bureau and GST consent remain active
    6. Audit log exported
    """
    print("=" * 60)
    print("UGRO Capital — Consent Management System Demo")
    print("Aligned to DPDP Act 2023, Section 6")
    print("=" * 60)

    manager = ConsentManager()
    applicant_id = "UGRO-APP-100042"

    # Step 1 — Applicant gives consent for all three data pulls
    print("\n--- Step 1: Consent Collection at Application ---")
    bureau_id = manager.give_consent(
        applicant_id,
        DataCategory.BUREAU,
        purpose="Credit risk assessment via CIBIL/Experian bureau pull"
    )
    print(f"Bureau consent recorded. Consent ID: {bureau_id}")

    bank_id = manager.give_consent(
        applicant_id,
        DataCategory.BANK_STATEMENT,
        purpose="Cash flow analysis via Account Aggregator"
    )
    print(f"Bank statement consent recorded. Consent ID: {bank_id}")

    gst_id = manager.give_consent(
        applicant_id,
        DataCategory.GST,
        purpose="Revenue verification via GSTN API"
    )
    print(f"GST consent recorded. Consent ID: {gst_id}")

    # Step 2 — System checks consent before each pull
    print("\n--- Step 2: Pre-Pull Consent Checks ---")
    for category in DataCategory:
        status = manager.check_consent(applicant_id, category)
        print(f"{category.value}: {'APPROVED' if status else 'BLOCKED'}")

    # Step 3 — Applicant withdraws bank statement consent
    print("\n--- Step 3: Applicant Withdraws Bank Statement Consent ---")
    result = manager.withdraw_consent(applicant_id, DataCategory.BANK_STATEMENT)
    print(f"Withdrawal successful: {result['success']}")
    print(f"Action required: {result['action_required']}")

    # Step 4 — System blocks subsequent bank statement pull
    print("\n--- Step 4: Post-Withdrawal Consent Checks ---")
    for category in DataCategory:
        status = manager.check_consent(applicant_id, category)
        print(f"{category.value}: {'APPROVED' if status else 'BLOCKED'}")

    # Step 5 — Full consent summary for applicant
    print("\n--- Step 5: Consent Summary (Right to Access) ---")
    summary = manager.get_consent_summary(applicant_id)
    for cat, details in summary["categories"].items():
        print(f"{cat}: status={details['status']}, "
              f"given_at={details['given_at'][:19] if details['given_at'] else 'N/A'}, "
              f"withdrawn_at={details['withdrawn_at'][:19] if details['withdrawn_at'] else 'N/A'}")

    # Step 6 — Export audit log
    print("\n--- Step 6: Audit Log Export ---")
    import os
    os.makedirs("../../reports", exist_ok=True)
    manager.export_audit_log("../../reports/consent_audit_log.json")
    print(f"Total audit events: {len(manager.audit_log)}")


if __name__ == "__main__":
    demo()

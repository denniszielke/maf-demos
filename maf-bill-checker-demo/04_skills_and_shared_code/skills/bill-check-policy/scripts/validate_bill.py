from __future__ import annotations

import json
import sys


def validate(bill: dict) -> dict:
    issues: list[str] = []
    if bill.get("total", 0) > 10000:
        issues.append("Total exceeds auto-approve threshold")
    if not bill.get("supplier_vat_id"):
        issues.append("Missing supplier VAT ID")
    if bill.get("payment_terms_days", 0) > 60:
        issues.append("Payment terms exceed 60 days")
    if bill.get("currency") not in {"EUR", "USD", "GBP"}:
        issues.append("Currency not allowed")

    address = bill.get("ship_to_address", {})
    for key in ["street", "city", "postal_code", "country"]:
        if not address.get(key):
            issues.append(f"Address missing {key}")

    return {
        "bill_id": bill.get("bill_id"),
        "passed": not issues,
        "issues": issues,
        "recommended_action": "approve_for_payment" if not issues else "hold_for_review",
    }


if __name__ == "__main__":
    payload = json.loads(sys.stdin.read())
    print(json.dumps(validate(payload)))

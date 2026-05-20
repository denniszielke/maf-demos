from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib import request

from middleware import validate_tool_params

ROOT = Path(__file__).resolve().parents[1]
CUSTOMER_PATH = ROOT / "05_enterprise_mcp_server" / "data" / "customer_master.json"


class ExtractorAgent:
    def run(self, bill: dict[str, Any]) -> dict[str, Any]:
        return {
            "bill_id": bill["bill_id"],
            "customer_id": bill["customer_id"],
            "currency": bill["currency"],
            "line_items": bill["line_items"],
            "subtotal": bill["subtotal"],
            "vat_total": bill["vat_total"],
            "total": bill["total"],
            "ship_to_address": bill["ship_to_address"],
            "payment_terms_days": bill["payment_terms_days"],
            "supplier_vat_id": bill.get("supplier_vat_id", ""),
        }


class ArithmeticValidatorAgent:
    def run(self, extracted: dict[str, Any]) -> list[str]:
        issues: list[str] = []
        line_subtotal = round(sum(i["qty"] * i["unit_price"] for i in extracted["line_items"]), 2)
        line_vat = round(sum(i["qty"] * i["unit_price"] * i["vat_rate"] for i in extracted["line_items"]), 2)
        line_total = round(line_subtotal + line_vat, 2)

        if line_subtotal != round(extracted["subtotal"], 2):
            issues.append(f"Subtotal mismatch expected {line_subtotal}")
        if line_vat != round(extracted["vat_total"], 2):
            issues.append(f"VAT mismatch expected {line_vat}")
        if line_total != round(extracted["total"], 2):
            issues.append(f"Total mismatch expected {line_total}")
        return issues


class CustomerValidatorAgent:
    def __init__(self, mcp_base_url: str | None = None) -> None:
        self.mcp_base_url = mcp_base_url
        self._local_customers = {
            row["customer_id"]: row
            for row in json.loads(CUSTOMER_PATH.read_text(encoding="utf-8"))
        }

    def _http_tool(self, tool: str, payload: dict[str, Any]) -> dict[str, Any]:
        req = request.Request(
            f"{self.mcp_base_url}/tools/{tool}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=4) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_customer_master(self, customer_id: str) -> dict[str, Any]:
        payload = validate_tool_params("get_customer_master", {"customer_id": customer_id})
        if self.mcp_base_url:
            return self._http_tool("get_customer_master", payload)
        return {"customer": self._local_customers.get(payload["customer_id"])}

    def validate_address(self, address: dict[str, Any]) -> dict[str, Any]:
        payload = validate_tool_params("validate_address", {"address": address})
        if self.mcp_base_url:
            return self._http_tool("validate_address", payload)
        normalized = payload["address"]
        return {
            "valid": bool(normalized.get("street") and normalized.get("city") and normalized.get("postal_code")),
            "normalized": normalized,
        }

    def run(self, extracted: dict[str, Any]) -> list[str]:
        issues: list[str] = []
        customer = self.get_customer_master(extracted["customer_id"]).get("customer")
        if not customer:
            issues.append("Customer not found in master data")

        address_result = self.validate_address(extracted["ship_to_address"])
        if not address_result.get("valid"):
            issues.append("Address validation failed")

        if extracted.get("payment_terms_days", 0) > 60:
            issues.append("Payment terms exceed max policy")
        if not extracted.get("supplier_vat_id"):
            issues.append("Supplier VAT ID missing")

        return issues


class AggregatorAgent:
    def run(self, bill_id: str, arithmetic_issues: list[str], customer_issues: list[str]) -> dict[str, Any]:
        issues = arithmetic_issues + customer_issues
        passed = not issues
        return {
            "bill_id": bill_id,
            "passed": passed,
            "issues": issues,
            "recommended_action": "approve_for_payment" if passed else "hold_for_review",
        }

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from azure.identity import DefaultAzureCredential
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

from middleware import redact_sensitive_fields, validate_tool_args

ROOT = Path(__file__).resolve().parents[1]
BILL_PATH = ROOT / "00_scenario" / "sample_bill.json"
CUSTOMER_PATH = ROOT / "05_enterprise_mcp_server" / "data" / "customer_master.json"


def _load_customer_data() -> dict[str, Any]:
    if CUSTOMER_PATH.exists():
        rows = json.loads(CUSTOMER_PATH.read_text(encoding="utf-8"))
        return {row["customer_id"]: row for row in rows}
    return {}


class BillCheckerAgent:
    def __init__(self) -> None:
        self.customers = _load_customer_data()

    def get_customer_master(self, customer_id: str) -> dict[str, Any]:
        args = validate_tool_args("get_customer_master", {"customer_id": customer_id})
        return self.customers.get(args["customer_id"], {})

    def validate_address(self, address: dict[str, Any]) -> dict[str, Any]:
        args = validate_tool_args("validate_address", {"address": address})
        candidate = args["address"]
        return {"valid": bool(candidate.get("street") and candidate.get("city")), "normalized": candidate}

    def run(self, bill: dict[str, Any]) -> dict[str, Any]:
        issues: list[str] = []
        subtotal = sum(item["qty"] * item["unit_price"] for item in bill["line_items"])
        vat = sum(item["qty"] * item["unit_price"] * item["vat_rate"] for item in bill["line_items"])
        total = subtotal + vat
        if round(subtotal, 2) != round(bill["subtotal"], 2):
            issues.append("Subtotal mismatch")
        if round(vat, 2) != round(bill["vat_total"], 2):
            issues.append("VAT mismatch")
        if round(total, 2) != round(bill["total"], 2):
            issues.append("Total mismatch")
        if not bill.get("supplier_vat_id"):
            issues.append("Supplier VAT ID is required")

        address_check = self.validate_address(bill.get("ship_to_address", {}))
        if not address_check["valid"]:
            issues.append("Ship-to address failed validation")
        if not self.get_customer_master(str(bill.get("customer_id", ""))):
            issues.append("Unknown customer_id")

        passed = len(issues) == 0
        action = "approve_for_payment" if passed else "hold_for_review"
        summary = f"Bill {bill['bill_id']} from {bill['supplier_name']} in {bill['currency']} for {bill['total']:.2f}"
        return {
            "summary": summary,
            "passed": passed,
            "reasons": issues or ["No issues found"],
            "recommended_action": action,
            "bill": redact_sensitive_fields(bill),
        }


def _build_devui_app(agent: BillCheckerAgent) -> FastAPI:
    app = FastAPI(title="BillChecker DevUI")

    @app.get("/", response_class=HTMLResponse)
    async def index() -> str:
        return (
            "<html><body><h1>Bill Checker DevUI</h1>"
            "<p>Programmatic serve(...) demo.</p>"
            "<button onclick=\"fetch('/run',{method:'POST'}).then(r=>r.json()).then(d=>document.getElementById('o').textContent=JSON.stringify(d,null,2))\">Run bill check</button>"
            "<pre id='o'></pre></body></html>"
        )

    @app.post("/run")
    async def run() -> JSONResponse:
        bill = json.loads(BILL_PATH.read_text(encoding="utf-8"))
        return JSONResponse(agent.run(bill))

    return app


def serve(*, agents: list[BillCheckerAgent], host: str = "127.0.0.1", port: int = 8010) -> None:
    # Programmatic serve(...) style aligned with DevUI sample intent.
    uvicorn.run(_build_devui_app(agents[0]), host=host, port=port)


def main(devui: bool, port: int) -> None:
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "<not set>")
    model = os.getenv("FOUNDRY_MODEL", "<not set>")
    credential = DefaultAzureCredential()
    print(f"Foundry config -> endpoint: {endpoint} | model: {model}")
    print(f"Auth: {type(credential).__name__}")

    agent = BillCheckerAgent()
    bill = json.loads(BILL_PATH.read_text(encoding="utf-8"))
    if devui:
        serve(agents=[agent], port=port)
        return
    print(json.dumps(agent.run(bill), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--devui", action="store_true")
    parser.add_argument("--port", type=int, default=8010)
    args = parser.parse_args()
    main(devui=args.devui, port=args.port)

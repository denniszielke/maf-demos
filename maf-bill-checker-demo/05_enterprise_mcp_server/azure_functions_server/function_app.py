from __future__ import annotations

import json
from pathlib import Path

import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

ROOT = Path(__file__).resolve().parents[1]
CUSTOMERS = json.loads((ROOT / "data" / "customer_master.json").read_text(encoding="utf-8"))
BY_ID = {c["customer_id"]: c for c in CUSTOMERS}


@app.route(route="tools/{tool}", methods=["POST"])
def tools(req: func.HttpRequest) -> func.HttpResponse:
    tool = req.route_params.get("tool", "")
    payload = req.get_json()

    if tool == "get_customer_master":
        body = {"customer": BY_ID.get(payload.get("customer_id"))}
    elif tool == "validate_address":
        address = dict(payload.get("address", {}))
        address["country"] = str(address.get("country", "")).upper()
        address["postal_code"] = str(address.get("postal_code", "")).replace(" ", "").upper()
        body = {"valid": bool(address.get("street") and address.get("city") and address.get("postal_code") and address.get("country")), "normalized": address}
    elif tool == "match_customer_by_name":
        needle = str(payload.get("name", "")).strip().lower()
        match = next((c for c in CUSTOMERS if needle in c["name"].lower()), None)
        body = {"match": match}
    else:
        return func.HttpResponse(json.dumps({"error": "Unknown tool"}), status_code=404, mimetype="application/json")

    return func.HttpResponse(json.dumps(body), mimetype="application/json")

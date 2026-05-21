from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "customer_master.json"
CUSTOMERS = json.loads(DATA_PATH.read_text(encoding="utf-8"))
BY_ID = {c["customer_id"]: c for c in CUSTOMERS}

app = FastAPI(title="Enterprise MCP Server")


class AddressPayload(BaseModel):
    address: dict


class CustomerPayload(BaseModel):
    customer_id: str


class NamePayload(BaseModel):
    name: str


@app.get("/healthz")
async def healthz() -> dict:
    return {"ok": True, "customers_loaded": len(CUSTOMERS)}


@app.post("/tools/get_customer_master")
async def get_customer_master(payload: CustomerPayload) -> dict:
    return {"customer": BY_ID.get(payload.customer_id)}


@app.post("/tools/validate_address")
async def validate_address(payload: AddressPayload) -> dict:
    address = dict(payload.address)
    address["country"] = str(address.get("country", "")).upper()
    address["postal_code"] = str(address.get("postal_code", "")).replace(" ", "").upper()
    valid = bool(address.get("street") and address.get("city") and address.get("postal_code") and address.get("country"))
    return {"valid": valid, "normalized": address}


@app.post("/tools/match_customer_by_name")
async def match_customer_by_name(payload: NamePayload) -> dict:
    needle = payload.name.strip().lower()
    match = next((c for c in CUSTOMERS if needle in c["name"].lower()), None)
    return {"match": match}


if __name__ == "__main__":
    print(f"Loaded {len(CUSTOMERS)} customers from {DATA_PATH}")
    uvicorn.run(app, host="127.0.0.1", port=9000)

from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "02_workflow_orchestration"))
from main import run_workflow  # type: ignore  # noqa: E402

BILL_PATH = ROOT / "00_scenario" / "sample_bill.json"


class BillRequest(BaseModel):
    bill: dict | None = None


app = FastAPI(title="Bill Checker A2A Server")


@app.post("/a2a/bill-check")
async def bill_check(req: BillRequest) -> dict:
    bill = req.bill or json.loads(BILL_PATH.read_text(encoding="utf-8"))
    result = run_workflow(bill, stream=False, mcp_base_url=None)
    return {"result": result.model_dump()}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9100)

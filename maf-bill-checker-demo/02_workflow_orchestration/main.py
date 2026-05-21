from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from agents import AggregatorAgent, ArithmeticValidatorAgent, CustomerValidatorAgent, ExtractorAgent
from models import BillCheckResult

ROOT = Path(__file__).resolve().parents[1]
BILL_PATH = ROOT / "00_scenario" / "sample_bill.json"


def run_workflow(bill: dict[str, Any], stream: bool = False, mcp_base_url: str | None = None) -> BillCheckResult:
    extractor = ExtractorAgent()
    arithmetic = ArithmeticValidatorAgent()
    customer = CustomerValidatorAgent(mcp_base_url=mcp_base_url)
    aggregator = AggregatorAgent()

    if stream:
        print("[workflow] ExtractorAgent...")
    extracted = extractor.run(bill)

    if stream:
        print("[workflow] ArithmeticValidatorAgent...")
    arithmetic_issues = arithmetic.run(extracted)

    if stream:
        print("[workflow] CustomerValidatorAgent (MCP tools)...")
    customer_issues = customer.run(extracted)

    if stream:
        print("[workflow] AggregatorAgent...")
    result = aggregator.run(extracted["bill_id"], arithmetic_issues, customer_issues)

    return BillCheckResult.model_validate(result)


def main(stream: bool) -> None:
    bill = json.loads(BILL_PATH.read_text(encoding="utf-8"))
    mcp_url = os.getenv("ENTERPRISE_MCP_BASE_URL")
    result = run_workflow(bill, stream=stream, mcp_base_url=mcp_url)
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()
    main(stream=args.stream)

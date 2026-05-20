from __future__ import annotations

import json
import sys
from pathlib import Path

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "02_workflow_orchestration"))
from main import run_workflow  # type: ignore  # noqa: E402


provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("bill-checker-demo")


def main() -> None:
    bill = json.loads((ROOT / "00_scenario" / "sample_bill.json").read_text(encoding="utf-8"))

    with tracer.start_as_current_span("bill_check_run") as span:
        span.set_attribute("bill.id", bill["bill_id"])
        result = run_workflow(bill, stream=True, mcp_base_url=None)
        span.set_attribute("bill.passed", result.passed)
        span.set_attribute("bill.issue_count", len(result.issues))

    print("metrics.bill_checks_total=1")
    print(f"metrics.bill_checks_passed_total={1 if result.passed else 0}")
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    main()

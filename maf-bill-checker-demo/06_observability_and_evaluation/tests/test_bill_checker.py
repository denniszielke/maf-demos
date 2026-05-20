from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "02_workflow_orchestration"))
from main import run_workflow  # type: ignore  # noqa: E402


BILL_PATH = ROOT / "00_scenario" / "sample_bill.json"


def test_bill_checker_passes_sample_bill() -> None:
    bill = json.loads(BILL_PATH.read_text(encoding="utf-8"))
    result = run_workflow(bill, stream=False, mcp_base_url=None)
    assert result.passed is True
    assert result.recommended_action == "approve_for_payment"


def test_bill_checker_fails_on_arithmetic_mismatch() -> None:
    bill = json.loads(BILL_PATH.read_text(encoding="utf-8"))
    bill["total"] = bill["total"] + 1
    result = run_workflow(bill, stream=False, mcp_base_url=None)
    assert result.passed is False
    assert any("Total mismatch" in issue for issue in result.issues)
    assert result.recommended_action == "hold_for_review"

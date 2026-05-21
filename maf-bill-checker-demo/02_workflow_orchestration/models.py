from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class BillCheckResult(BaseModel):
    bill_id: str
    passed: bool
    issues: list[str]
    recommended_action: str


class WorkflowState(BaseModel):
    bill: dict[str, Any]
    extracted: dict[str, Any] = {}
    arithmetic_issues: list[str] = []
    customer_issues: list[str] = []

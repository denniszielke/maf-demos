from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BILL_PATH = ROOT / "00_scenario" / "sample_bill.json"
SKILL_ROOT = Path(__file__).resolve().parent / "skills" / "bill-check-policy"


def main() -> None:
    print("[skills] Advertised skill: bill-check-policy")

    skill_md = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    print("\n[skills] Loaded instructions on demand:")
    print("\n".join(skill_md.splitlines()[:8]))

    policy_md = (SKILL_ROOT / "references" / "POLICY.md").read_text(encoding="utf-8")
    print("\n[skills] Loaded policy reference when needed:")
    print(policy_md)

    bill = BILL_PATH.read_text(encoding="utf-8")
    script_path = SKILL_ROOT / "scripts" / "validate_bill.py"
    result = subprocess.check_output(["python", str(script_path)], input=bill.encode("utf-8"))
    print("\n[skills] Script execution result:")
    print(json.dumps(json.loads(result.decode("utf-8")), indent=2))


if __name__ == "__main__":
    main()

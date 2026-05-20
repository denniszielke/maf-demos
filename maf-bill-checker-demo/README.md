# Bill Checker 20-minute presenter script

This demo stays in one scenario: validate a supplier bill and produce a pass/fail plus payable draft recommendation.

## Setup (2 minutes)

```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Checkpoint 1 — DevUI local agent + Foundry model endpoint (4 minutes)

```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/01_devui_local_agent
python main.py --devui --port 8010
```

What to observe:
- BillCheckerAgent reads `../00_scenario/sample_bill.json`.
- Middleware redacts `supplier_vat_id` in rendered output.
- Middleware validates tool args (`validate_address`, `get_customer_master`).
- If Foundry env vars are set, the banner shows endpoint/model being used.

## Checkpoint 2 — Workflow orchestration + middleware + remote dependency (4 minutes)

```bash
# terminal A
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/05_enterprise_mcp_server/local_server
python server.py

# terminal B
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/02_workflow_orchestration
python main.py --stream
```

What to observe:
- Streaming stage logs from Extractor → ArithmeticValidator → CustomerValidator → Aggregator.
- CustomerValidator invokes remote MCP tools.
- Middleware normalises postal code and blocks invalid tool parameters.

## Checkpoint 3 — A2A + Foundry hosted agent + Foundry Toolbox (4 minutes)

```bash
# terminal A
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/03_protocols_and_foundry
python a2a_server.py

# terminal B
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/03_protocols_and_foundry
python a2a_client.py
```

What to observe:
- Single `BillCheckResult` returned over an A2A-style endpoint.
- Hosted-agent artifacts under `foundry_hosted_agent/` include Responses protocol skeleton and toolbox notes.

## Checkpoint 4 — File-based Agent Skill (4 minutes)

```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/04_skills_and_shared_code
python main.py
```

What to observe:
- Agent advertises `bill-check-policy` skill first.
- Instructions and `POLICY.md` are loaded only when needed.
- Script execution (`validate_bill.py`) returns policy validation JSON.

## Checkpoint 5 — Observability + evaluation + tests (4 minutes)

```bash
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/06_observability_and_evaluation
python local_observability.py
pytest -q tests/test_bill_checker.py
```

What to observe:
- Local OpenTelemetry traces and metrics-like counters emitted to console.
- Automated gate: one passing case and one failing case.
- `foundry_eval_notes.md` outlines hosted-agent traces/metrics and eval gate in Foundry.

## Demo cheat sheet (live prompts)

1. "Check this invoice and explain pass/fail in 3 bullets for AP reviewer."
2. "Run a full bill validation workflow and show me intermediate stage outputs."
3. "Call the remote Bill Checker over A2A and return only BillCheckResult JSON."
4. "Apply bill-check-policy skill progressively; only open policy docs if needed."
5. "Evaluate this hosted Bill Checker run and fail it if arithmetic or address checks regress."

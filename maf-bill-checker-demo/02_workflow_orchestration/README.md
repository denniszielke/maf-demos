# 02 Workflow orchestration

Run this:
```bash
# optional but recommended for remote dependency demo
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/05_enterprise_mcp_server/local_server
python server.py

# in a second terminal
cd /home/runner/work/maf-demos/maf-demos/maf-bill-checker-demo/02_workflow_orchestration
python main.py --stream
```

Observe this:
- Streamed workflow progress.
- CustomerValidatorAgent middleware normalizes and validates tool params.
- Final `BillCheckResult` JSON with pass/fail and recommendation.
